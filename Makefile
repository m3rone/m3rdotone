mkcss:
	sass --stop-on-error --no-source-map static/scss:static/css

mktest: mkcss
	. venv_dev/bin/activate
	gunicorn start:application &
	linkchecker 'http://127.0.0.1:8000' || pkill -9 gunicorn
	pkill -9 gunicorn

mkimg: mkcss
	docker build -t $(M3R_DOCKER_IMG_NAME):latest .

pushimg: mkimg
	docker login --username $(M3R_DOCKER_USERNAME) --password $(M3R_DOCKER_PASSWORD) $(M3R_DOCKER_SERVER)
	docker push $(M3R_DOCKER_IMG_NAME)
	ssh m3r.one 'cd m3r && make update'

mkdev:
	sass --no-source-map -w static/scss:static/css

prod:
	docker compose up -d

down: 
	docker compose down
