#!/bin/bash

set -e

if (( $# != 1 )); then
    echo "Should have one parameter <sd-card-device>"
    exit 1
fi

sdCard=$1
date=`date +%Y-%m-%d`
name="tc2-$date.img"

echo "Reading image"
./read-image $sdCard $name
echo "Shrinking image"
sudo ./pishrink.sh $name
echo "Compressing image"
zip $name.zip $name
