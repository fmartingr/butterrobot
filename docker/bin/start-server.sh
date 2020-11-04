#!/bin/sh -xe

waitress-serve --port=${APP_PORT} 'butterrobot.app:app'