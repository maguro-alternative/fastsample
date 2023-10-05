#!/bin/bash
set -eu

DEPLOY_ENV="xxx"

SCRIPT_DIR=$(cd $(dirname $0); pwd)
APP_ENGINE_DIR="app_engine"

if [ -e $APP_ENGINE_DIR ]; then
    rm -r $APP_ENGINE_DIR
fi
mkdir -p $APP_ENGINE_DIR

# gcloud deploy ではハッシュがあるとうまくいかないので、オプションで指定
poetry export -f requirements.txt --without-hashes --output $APP_ENGINE_DIR/requirements.txt

APP_YAML="app.$DEPLOY_ENV.yaml"
ln -s $SCRIPT_DIR/$APP_YAML $APP_ENGINE_DIR/$APP_YAML
ln -s $SCRIPT_DIR/src/package_name$APP_ENGINE_DIR/

# デプロイ
cd $SCRIPT_DIR/$APP_ENGINE_DIR
gcloud app deploy $APP_YAML --project project-name