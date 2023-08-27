from fastapi import APIRouter, Header
import deezer

router = APIRouter()


@router.get('/deezer/tracks/{track_id}')
async def get_track_by_id(track_id: int, deezer_arl_token: str = Header(None, alias="X-DEEZER-ARL-TOKEN")):
    dz = deezer.Deezer()
    dz.login_via_arl(arl=deezer_arl_token)
    track = dz.api.get_track(track_id)
    return track


@router.get('/deezer/favorites')
async def get_user_favorite_tracks(deezer_arl_token: str = Header(None, alias="X-DEEZER-ARL-TOKEN")):
    dz = deezer.Deezer()
    dz.login_via_arl(arl=deezer_arl_token)
    user = dz.get_session()['current_user']
    user_playlists = dz.api.get_user_playlists(user['id'])
    favorites_playlist = next(
        (playlist for playlist in user_playlists['data'] if playlist['title'] == "Loved tracks"), None
    )

    favorites_tracks = dz.api.get_playlist_tracks(favorites_playlist['id'])
    return favorites_tracks
