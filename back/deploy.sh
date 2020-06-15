#!/bin/bash


export PROJECT_ROOT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd ${PROJECT_ROOT_PATH}


BUCKET_NAME="www.covidometro.info"

export FRONT_DIRPATH="../front"
export TEMPLATES_DIRPATH="${FRONT_DIRPATH}/templates"
export PUBLIC_DIRPATH="${FRONT_DIRPATH}/public"


while true;
do
    date

    printf "\nFetching fresh data.\n"
    python gsheets-data-fetcher.py
    printf "Building page.\n\n"
    python page_builder.py

    printf "Uploading resources.\n"
    gsutil cp ${PUBLIC_DIRPATH}/index.html gs://${BUCKET_NAME}/index.html
    gsutil cp -r ${PUBLIC_DIRPATH}/styles gs://${BUCKET_NAME}
    gsutil cp -r ${PUBLIC_DIRPATH}/js gs://${BUCKET_NAME}

    printf "\nSleeping for 10 minutes.\n\n"
    sleep 10m
done
