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
	podman push registry.int.fmartingr.network/fmartingr/butterrobot:dev --tls-verify=false

podman@dev:
	make podman@build-dev
	make podman@tag-dev
	make podman@push-dev

test:
	poetry run pytest --cov=butterrobot --cov=butterrobot_plugins_contrib

clean:
	rm -rf dist
	rm -rf butterrobot.egg-info
