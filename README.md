# deezer-minus-player-api

API for downloading song source from deezer and split to stems

Steps:

1. Run python app
2. Start redis

[//]: # (sudo service redis-server start)

3. start celery

[//]: # (celery -A mzapi worker -l info -P threads)
