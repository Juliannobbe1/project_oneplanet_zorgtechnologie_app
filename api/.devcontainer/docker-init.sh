#!/bin/bash

docker network create zorgtechnologie_api &> /dev/null
if [ "$?" -ne "0" ]; then
  echo "Network 'zorgtechnologie_api' already exists"
else
  echo "Created docker network 'zorgtechnologie_api'"
fi