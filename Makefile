# Local development
setup:
	poetry install

docker@build:
	docker build -t fmartingr/butterrobot .

podman@build:
	podman build -t fmartingr/butterrobot .

docker@save:
	make docker@build
	docker image save fmartingr/butterrobot -o fmartingr-butterrobot-docker-image.tar

clean:
	rm -rf dist
	rm -rf butterrobot.egg-info
