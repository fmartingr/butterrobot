## Contributing

To run the project locally you will need [poetry](https://python-poetry.org/).

```
git clone git@github.com:fmartingr/butterrobot.git
cd butterrobot
make setup
```

Create a `.env-local` file with the required environment variables, you have [an example file](.env-example).

```
SLACK_TOKEN=xxx
TELEGRAM_TOKEN=xxx
...
```

And then you can run it directly with poetry:

```
poetry run python -m butterrobot
```
