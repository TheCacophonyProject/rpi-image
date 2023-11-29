# Creating a new image for tc2

These instructions describe how to create a new Raspberry Pi image for
us with the Cacophony Project.

- Download the last Raspbian 64 bit OS
- Plug a SD card into your computer
- Prepare the image using the Raspberry Pi Imager tool https://www.raspberrypi.com/software
- //TODO check what settings are needed for imager tool.
- Eject the SD card from the computer and install it into a Pi then power it on.
- Ensure that you can ssh onto the pi without user input (this ensures the configure script doesn't need your input)
- Run the config script.
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
