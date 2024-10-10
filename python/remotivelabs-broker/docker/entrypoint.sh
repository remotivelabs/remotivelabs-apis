#!/bin/bash
#
# Docker entrypoint
#
# Creates a dummy user (hostuser) with the same UID/GID as the host user and executes the build script (build.sh) with that user.
# This has several benefits, including:
# - hostuser has its own HOME directory, which it has full permissions to.
# - hostuser will have full access to the mounted host directory.
# - hostuser will produce output files with the correct permissions for host to access them later.
# - you may pass on environment variables to hostuser by appending them to /home/hostuser/.bashrc
#
set -e

create_group_if_not_exists() {
    local gid=$1
    if ! getent group "$gid" >/dev/null 2>&1; then
        addgroup --gid "$gid" hostgroup --quiet
    fi
}

create_user_if_not_exists() {
    local uid=$1
    local gid=$2
    if ! getent passwd "$uid" >/dev/null 2>&1; then
        adduser --uid "$uid" --gid "$gid" --disabled-password --gecos "" hostuser --quiet
    fi
}

# We know that working dir is set to the mounted host volume. Get the UID/GID of the owner so that we can run as that user in the container.
HOST_UID=$(stat -c "%u" "$PWD")
HOST_GID=$(stat -c "%g" "$PWD")

CURRENT_UID=$(id -u)
CURRENT_GID=$(id -g)

create_group_if_not_exists "$HOST_GID"
create_user_if_not_exists "$HOST_UID" "$HOST_GID"

if [ "$CURRENT_UID" -eq "$HOST_UID" ] && [ "$CURRENT_GID" -eq "$HOST_GID" ]; then
    exec /usr/local/bin/build.sh "$@"
else
    user=$(getent passwd "$HOST_UID" | cut -d: -f1)
    exec su - "$user" -c "/usr/local/bin/build.sh $@"
fi
