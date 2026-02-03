# New Camera Setup

## Requirements

- Camera.
- SD card.
- bushnet hotspot setup that has internet access. See notes for options on how to set this up.
- Laptop/Computer connected to the bushnet network.

## Steps

- Make sure the bushnet network is up and has internet access. Also make sure no other cameras are around that are hosting their own bushnet hotspot.
- Flash the SD card with the latest image.
- Put SD card in the camera and power it up.
- Wait for LED to turn solid green. This means that it has connected to a wifi network, hopefully your bushnet network.
- Find the IP or hostname (name-group.local) of the device. If the host name is `tc2-image` wait for it to get a new name and restart. You will see it come up again after it gets a new name and restarts. On linux I run this to see the devices `avahi-browse --resolve _cacophonator-management._tcp` 
- Open up a browser and connect to the device through your computer using the hostname or IP address.
- Go to the `About` page. `Advanced` -> `About`
- Get the `Salt Minion ID` and then accept it to salt.
- Every few seconds refresh the salt page until it shows it starting a salt update. This should happen automatically onces the camera sees that it is accepted to salt.
- Once the salt update is done (might see some errors about modinfo, just ignore those for now) you can rename/change group of the device to what you want.

## Notes

### Bushnet Network

A wifi network with SSID (name) of `bushnet` and password of `feathers` needs to be setup for the camera to connect to.
If this is not setup the camera will host its own bushnet network, you will have to connect and then give it the details of another wifi network to connect to so it has internet access.

This can easily be done using an Android phone (iphone not so easy?) by enabling the phones hotspot with the correct name and password for bushnet. Then if your phone is connect to your wifi network (new phones can both connect to a wifi network and host a hotspot at the same time) it can then route your wifi internet to its bushnet hotspot it is hosting.

If doing this a lot you might want to setup a dedicated bushnet router.

### SD card

Our cameras do a lot of writing to the SD cards and we have found that lower quality SD cards will break after an amount of time.
Using SanDisk ones seams to work well.

Get the SD cards from a trusted supplier as there are lots of "fake" SD cards sold by sites like AliExpress and Temu.

When flashing the SD card make sure you use a program that will verify the SD card write like [etcher](https://etcher.balena.io/).
