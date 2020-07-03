# Local development
setup:
	poetry install

docker@build:
	docker build -t fmartingr/butterrobot -f docker/Dockerfile docker

docker@build-dev:
	docker build -t fmartingr/butterrobot:dev -f Dockerfile.dev .

docker@tag-dev:
	docker tag fmartingr/butterrobot:dev registry.int.fmartingr.network/fmartingr/butterrobot:dev

docker@push-dev:
	docker push registry.int.fmartingr.network/fmartingr/butterrobot:dev

docker@dev:
	make docker@build-dev
	make docker@tag-dev
	make docker@push-dev

docker@save:
	make docker@build
	docker image save fmartingr/butterrobot -o fmartingr-butterrobot-docker-image.tar

clean:
	rm -rf dist
	rm -rf butterrobot.egg-info
