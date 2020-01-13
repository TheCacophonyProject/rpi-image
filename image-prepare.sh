#!/bin/bash
set -e
if (( $# != 2 )); then
    echo "Should have two parameters <image.zip> <card_mount_point>"
    exit 1
fi

image=$1
sdCard=$2

echo "Mounting image $image onto $sdCard"
echo "This will take a few minutes"
./write-image $image $sdCard

./cardtool ssh enable $sdCard
./cardtool ssh add-key $sdCard ./cacophony-pi.pub

./cardtool wifi country $sdCard NZ
./cardtool wifi set $sdCard bushnet feathers

echo "SD card prepare finished. Eject from computer and put in Raspberry Pi"
