#!/bin/bash

set -e

if (( $# != 1 )); then
    echo "Should have one parameter <card-mount-point>"
    exit 1
fi

sdCard=$1
date=`date +%Y-%m-%d`
name="thermal-recorder-$date.img"

echo "Removing wifi details"
./cardtool wifi clear $sdCard
echo "Reading image"
./read-image $sdCard $name
echo "Shrinking image"
sudo ./pishrink.sh $name
echo "Compressing image"
zip $name.zip $name
