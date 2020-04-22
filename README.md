# Butter Robot

[![Docker Repository on Quay](https://quay.io/repository/fmartingr/butterrobot/status "Docker Repository on Quay")](https://quay.io/repository/fmartingr/butterrobot)

Python framework to create bots for several platforms.

![Butter Robot](./assets/icon@120.png)

> What is my purpose?

## Supported platforms

| Name            | Receive messages | Send messages |
| --------------- | ---------------- | ------------- |
| Slack (app)     | Yes              | Yes           |
| Slack (webhook) | Planned          | No[^1]            |
| Telegram        | Yes              | Yes           |

[^1]: Slack webhooks only supports answering to incoming event, not
      sending messages on demand.

## Provided plugins

### Butter robot

- [ ] Help
- [ ] Usage
- [ ] Changelog

### Development

- [x] Ping

### Fun and entertainment

- [ ] Dice roll
- [x] Loquito

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

The `fmartingr/butterrobot` container image is published on quay.io to
use with your favourite tool:

```
podman run -d --name butterrobot -p 8080:8080 quay.io/fmartingr/butterrobot
```

## Contributing

To run the project locally you will need [poetry](https://python-poetry.org/).

```
git clone git@github.com:fmartingr/butterrobot.git
cd butterrobot
poetry install
```

Create a `.env-local` file with the required environment variables,
you have [an example file](.env-example).

```
SLACK_TOKEN=xxx
TELEGRAM_TOKEN=xxx
...
```

And then you can run it directly with poetry

TODO: Autoload .env-local

```
docker run -it --rm --env-file .env-local -p 5000:5000 -v $PWD/butterrobot:/etc/app/butterrobot local/butterrobot python -m butterrobot
```
