Tooling for creating Cacophony Project Raspberry Pi image.

# Writing a pre-existing Cacophony Project image

* Insert an SD card.
* Write the image to the SD card:
```
./write-image <img.lrz> /dev/mmcblk0
```

* Set the Cacophony Project id for the card:
```
./cardtool id /dev/mmcblk0 [name] [group]
```

# Creating a new image

These instructions describe how to create a new Raspberry Pi image for
us with the Cacophony Project. The resulting image will be based on
the latest Raspbian Lite image and will include the latest software
and configuration used by the Cacophony Project.

## Prepare Image

* Download the latest Raspian Lite image from https://www.raspberrypi.org/downloads/raspbian/
* Write the image to an SD card (this will take a little while):
```
./write-image <image.zip> /dev/mmcblk0`
```

* Enable SSH server & add Cacophony public SSH key:
```
./cardtool ssh enable /dev/mmcblk0
./cardtool ssh add-key /dev/mmcblk0 ~/.ssh/cacophony-pi.pub
```

* Set WiFi country and add your local WiFi details:
```
./cardtool wifi country /dev/mmcblk0 NZ
./cardtool wifi set /dev/mmcblk0 <ssid> <psk>
```

TODO: automate the above further.

## Configure Image

* Eject the SD card from the computer install it into a Pi and boot it.
* Copy the setup script to the Pi:
```
scp cacophony-setup.sh pi@raspberrypi:
```

* Run the setup script:
```
ssh pi@raspberrypi cacophony-setup.sh
```

This will take a while. When it's done the Pi wil shut down.


## Finalise Image

* Insert the SD card back into your computer.
* Remove WiFi credentials from the image (TODO: do this as part of cacophony-setup.sh)
```
./cardtool wifi clear /dev/mmcblk0
```
* (TODO: delete log files)
* Copy the image off the card:
```
./read-image /dev/mmcblk0 [out.img]
```

* Shrink the image:
```
sudo ./pishrink.sh [out.img]
```

* Compress the image:
```
lrzip <out.img>
```

* Copy image file to Google Drive.

TODO: automate the above further.
