# Butter Robot

> [!WARNING]
> This chatbot was functional at the time but my main programming language changed from Python to Golang so I archived this repository.
> I'm currently working on a refactored version of this in Golang [at this repository](https://git.nakama.town/fmartingr/butterrobot).

| Stable | Master |
| --- | --- |
| ![Build stable tag docker image](https://github.com/fmartingr/butterrobot/workflows/Build%20stable%20tag%20docker%20image/badge.svg?branch=stable) | ![Build latest tag docker image](https://github.com/fmartingr/butterrobot/workflows/Build%20latest%20tag%20docker%20image/badge.svg?branch=master) |
| ![Pytest](https://github.com/fmartingr/butterrobot/workflows/Pytest/badge.svg?branch=stable) | ![Pytest](https://github.com/fmartingr/butterrobot/workflows/Pytest/badge.svg?branch=master) |

Python framework to create bots for several platforms.

![Butter Robot](./assets/icon@120.png)

> What is my purpose?

## Documentation

[Go to documentation](./docs)

## Installation

### PyPi

You can run it directly by installing the package and calling it
with `python` though this is not recommended and only intended for
development purposes.

```
$ pip install --user butterrobot
$ python -m butterrobot
```

### Containers

The `fmartingr/butterrobot/butterrobot` container image is published on Github packages to use with your favourite tool:

```
docker pull docker.pkg.github.com/fmartingr/butterrobot/butterrobot:latest
podman run -d --name fmartingr/butterrobot/butterrobot -p 8080:8080
```

## Contributing

To run the project locally you will need [poetry](https://python-poetry.org/).

```
git clone git@github.com:fmartingr/butterrobot.git
cd butterrobot
poetry install
```

Create a `.env-local` file with the required environment variables, you have [an example file](.env-example).

```
SLACK_TOKEN=xxx
TELEGRAM_TOKEN=xxx
...
```

And then you can run it directly with poetry

```
docker run -it --rm --env-file .env-local -p 5000:5000 -v $PWD/butterrobot:/etc/app/butterrobot local/butterrobot python -m butterrobot
```
