Tooling for creating Cacophony Project Raspberry Pi image.

# Python dependencies
Requires:
* plumbum
* WpaSupplicantConf

e.g.
python3 -m pip install plumbum WpaSupplicantConf

# Writing a pre-existing Cacophony Project image

* Insert an SD card.
* Write the image to the SD card:
```
./write-image <img.lrz> /dev/mmcblk0
```

* Insert into and then power on camera. The camera will automatically register. The name and group can be changed through the management interface.

# Creating a new image

These instructions describe how to create a new Raspberry Pi image for
us with the Cacophony Project. The resulting image will be based on
the latest Raspbian Lite image and will include the latest software
and configuration used by the Cacophony Project.

* ~~Download the latest Raspian Lite image from https://www.raspberrypi.org/downloads/raspbian/~~
* Download the last Raspbian Lite Strech image (have not tested buster yet)
https://downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2019-04-09/
* Plug a SD card (8GB works best) into your computer
* Prepare the image
```
./image-prepare <image.zip> <sd-mount-point>
```
* If needed set WiFi country and add your local WiFi details. Bushnet is added by default.
```
./cardtool wifi country /dev/mmcblk0 NZ
./cardtool wifi set /dev/mmcblk0 <ssid> <psk>
```
* Eject the SD card from the computer install it into a Pi and boot it.
* Ensure that you can ssh onto the pi without user input (this ensures the configure script doesn't need your input)
* Run the config sctipt
```
./image-configure.sh
```
* Insert the SD card back into your computer.
* Run the finalise script
```
./image-finalise
```
* if pishrink.sh is causing issues try looking here https://github.com/gmenezesg/fix_orphaned_inode_list
* Copy image file to Google Drive.
