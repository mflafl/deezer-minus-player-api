import csv
import time
import math
import deezer
import os

from mzapi.models.track import Track, Data
from mzapi.core.database import database

# Provide your Deezer ARL token here
deezer_arl_token = ''

# Specify the path to your CSV file (assumes it's in the same folder as the script)
csv_file_path = os.path.join(os.path.dirname(__file__), 'tracks.csv')

# Specify the offset and limit for rows
offset = 0  # Start processing from the first row
limit = 10

session = database.get_session()


def read_csv_file(csv_file_path, offset=0, limit=None):
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)  # Read all rows into a list

        # Apply offset and limit to rows
        if offset < len(rows):
            rows = rows[offset:]
        else:
            rows = []

        if limit is not None and limit < len(rows):
            rows = rows[:limit]

        for row in rows:
            title = row['Title']
            album = row['Album']
            artist = row['Artist']
            duration = row['Duration']
            added = row['Added']

            # Convert duration to seconds
            duration_seconds = (sum(x * int(t) for x, t in zip([3600, 60, 1], duration.split(":")))) / 60

            dz = deezer.Deezer()
            dz.login_via_arl(arl=deezer_arl_token)

            search_results = dz.api.advanced_search(artist=artist, album=album, track=title,
                                                    dur_min=math.floor(duration_seconds),
                                                    dur_max=math.ceil(duration_seconds))

            # Verify and process the track if found
            found_track = None
            for track in search_results['data']:
                if track['album']['title'].lower() == album.lower():
                    found_track = track
                    break
                else:
                    print(
                        f"Found track with matching artist and title, but different album: {track['title']} - {track['artist']['name']} / {track['album']['title']}")

            # Process the track if found
            if found_track:
                deezer_id = found_track['id']
                track_details = dz.api.get_track(deezer_id)

                print(f"Found track: {found_track['title']} - {found_track['artist']['name']} / {deezer_id}")

                # Create a Track object
                track = Track()
                track.external_source = 'deezer'
                track.external_id = deezer_id
                track.external_source_added_at = added
                track.length = track_details['duration']
                track.title = track_details['title']
                track.artist = track_details['artist']['name']
                track.album = track_details['album']['title']
                track.data = track_details

                session.add(track)
                session.commit()

            else:
                print(f"No matching track found for: {title} - {artist}")

        time.sleep(2)  # Sleep for 1 second to avoid rate limiting


# Read the CSV file and search for tracks with offset and limit
read_csv_file(csv_file_path, offset=offset, limit=limit)

# Close the session
session.close()
