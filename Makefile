# Local development
setup:
	poetry install

podman@build:
	podman build -t fmartingr/butterrobot -f docker/Dockerfile docker

podman@build-dev:
	podman build -t fmartingr/butterrobot:dev -f Dockerfile.dev .

podman@tag-dev:
	podman tag fmartingr/butterrobot:dev registry.int.fmartingr.network/fmartingr/butterrobot:dev

podman@push-dev:
	docker push registry.int.fmartingr.network/fmartingr/butterrobot:dev

podman@dev:
	make podman@build-dev
	make podman@tag-dev
	make docker@push-dev

clean:
	rm -rf dist
	rm -rf butterrobot.egg-info
