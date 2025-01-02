#!/bin/bash

# Start the D-Bus service
service dbus start

# Start the NetworkManager service
service NetworkManager start

# Start your Python application
exec "$@"
