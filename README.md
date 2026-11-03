# rpi-image

Tooling and instructions for making Raspberry Pi OS images for Thermal Camera 2 (TC2).

To set up a camera from an existing image, see [new-camera-setup.md](new-camera-setup.md).

## Making a new image

Each image is based on the previous one.

1. Flash the latest image to an SD card, put it in a camera and power it up.
2. Run a salt update on the camera.
3. On the camera, tidy the image. `new-image-tidy.sh` is installed by salt.

   ```bash
   sudo new-image-tidy.sh
   ```

4. Power off the camera, then put the SD card in your computer.
5. From this repo, make the image. This needs `pv` and `zip`.

   ```bash
   sudo ./image-finalise.sh /dev/mmcblk0
   ```

   This creates `tc2-<date>.img` and `tc2-<date>.img.zip` in the current folder.
6. Copy the zip to Google Drive.

If `pishrink.sh` has problems, try <https://github.com/gmenezesg/fix_orphaned_inode_list>

## How the base image was made

You shouldn't need this unless you have to start again without a previous image. Some of
these steps aren't done by salt, so the images only have them because each one builds on the last.

1. Download [Raspberry Pi OS Lite arm64 2023-12-11](https://downloads.raspberrypi.org/raspios_lite_arm64/images/raspios_lite_arm64-2023-12-11/).
2. Flash it with Raspberry Pi Imager, using these options:
   - Set the hostname to `tc2`.
   - Allow public-key authentication only, with the key from `tc2/auth/cacophony-pi.pub` in saltops.
   - Add your WiFi network if you won't be using the ethernet port.
3. [Install salt](https://docs.saltproject.io/salt/install-guide/en/latest/topics/install-by-operating-system/debian.html#install-salt-on-debian-12-bookworm-arm64), then `sudo apt install salt-minion`.
4. Install the packages and create the journal folder:

   ```bash
   sudo apt-get install -y pipx openocd dnsmasq
   sudo PIPX_BIN_DIR=/usr/local/bin pipx install pymcuprog==3.14.2.9
   sudo mkdir -p /var/log/journal
   sudo systemd-tmpfiles --create --prefix /var/log/journal
   ```

5. Run a salt update. It might take a couple of runs.
