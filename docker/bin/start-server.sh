#!/bin/sh -xe

hypercorn butterrobot.app -b "0.0.0.0:${APP_PORT}"
