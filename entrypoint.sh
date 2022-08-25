#!/bin/bash
USER_ID=${UID:-1000}
GROUP_ID=${GID:-1000}

echo "Starting with UID : $USER_ID, GID: $GROUP_ID"
sudo usermod -u $USER_ID $USER
sudo groupmod -g $GROUP_ID $USER
