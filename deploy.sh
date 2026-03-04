#!/bin/bash
source .env
VERSION="$1"

appImg=overwatch-app:v$VERSION
dashboardImg=overwatch-frontend:v$VERSION

# update images
cd app/
docker build -t $appImg .
cd ..
cd overwatch-dashboard/

docker build -t $dashboardImg .
cd ..


# push image to local repo
docker tag $appImg $REGISTRY_HOST/$appImg
docker tag $dashboardImg $REGISTRY_HOST/$dashboardImg

docker push  $REGISTRY_HOST/$appImg
docker push $REGISTRY_HOST/$dashboardImg