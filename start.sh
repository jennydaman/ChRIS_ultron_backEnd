#!/bin/bash -e
# Purpose: `podman-compose up` wrapper for ChRIS_ultron_backEnd
#          This script fills in for features of `docker-compose` which are not supported by `podman-compose`

set -o pipefail

# `cd` into the project directory
HERE="${BASH_SOURCE[0]%/*}"
cd "$HERE"

# Enable sharing of source code directory with container
export UID=$(id -u) GID=$(id -g)
export USERNS_MODE=keep-id


tput sgr0
tput bold
echo '

        STARTING SERVICES

--------------------------------------------------------------------------------
'
tput sgr0
tput dim

# Build images and start services
podman-compose up -d --build

# Workaround for https://github.com/containers/podman-compose/issues/575
# podman-compose does not honor long syntax of depends_on

function get_labeled_service () {
  local container_id=$(podman ps -aq -f label=org.chrisproject.chris_ultron_backend="$1")
  if [ -z "$container_id" ]; then
    echo "error: container for $1 not found."
    return 1
  fi
  echo $container_id
}


tput sgr0
tput bold
echo '

        WAITING FOR DATABASE

--------------------------------------------------------------------------------
'
tput sgr0
tput dim

# Wait for database to be ready
db="$(get_labeled_service db)"
podman wait --condition=healthy $db
podman-compose up -d


tput sgr0
tput bold
echo '

        RUNNING DATABASE MIGRATIONS

--------------------------------------------------------------------------------
'
tput sgr0
tput dim

# Wait for database migrations to finish
db_migrate="$(get_labeled_service db_migrate)"
podman logs $db_migrate
if [ "$(podman inspect -f '{{ .State.ExitCode }}' $db_migrate)" != "0" ]; then
  echo "error: database migrations failed"
  exit 1
fi


tput sgr0
tput bold
echo '

        STARTING ChRIS BACKEND

--------------------------------------------------------------------------------
'
tput sgr0
tput dim

podman-compose up -d

tput sgr0
tput bold
echo '

         .--"--.           
       / -     - \                
      / (O)   (O) \        
   ~~~| -=(,Y,)=- |                   
    .---. /`  \   |~~               ALL DONE!
 ~/  o  o \~~~~.----. ~~   
  | =(X)= |~  / (O (O) \        ChRIS backend is running on podman-compose
   ~~~~~~~  ~| =(Y_)=-  |         
  ~~~~    ~~~|   U      |~~ 

--------------------------------------------------------------------------------
'
tput sgr0
