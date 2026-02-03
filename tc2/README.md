## Making TC2 Images

### Image setup
- Download image https://downloads.raspberrypi.org/raspios_lite_arm64/images/raspios_lite_arm64-2023-12-11/
- Flash with Raspbery Pi Imager with these options:
  - hostname to 'tc2'
  - 'Allow public-key authentication only'
  - Set authorized keys to the cacophony-pi.pub key
  - Add your wifi network if you won't be using the ethernet port.

### Salt setup
- Follow instructions for installing salt for Major onedir Debian 12
- Is there is a specific Raspbian salt release then use that (not one available when writing this for RasPiOS 12, just 10 and 11)
- https://docs.saltproject.io/salt/install-guide/en/latest/topics/install-by-operating-system/debian.html#install-salt-on-debian-12-bookworm-arm64
- `sudo apt install salt-minion`

### Packages and Raspberry Pi Config (//TODO, make this done through salt)
- Install `pymcuprog`
  - `sudo apt-get install pipx -y`
  - `sudo PIPX_BIN_DIR=/usr/local/bin pipx install pymcuprog==3.14.2.9`
- Install `openocd`, `sudo apt-get install openocd -y`
- Install dnsmasq, `sudo apt install dnsmasq` For some reason the command `dnsmasq` is available on a fresh install but not the service, so installing it with apt fixes this.

`sudo mkdir -p /var/log/journal`
`sudo systemd-tmpfiles --create --prefix /var/log/journal`


### Install Cacophony software
- Checkout the latest saltops and run `./state-apply-test-tc2.sh tc2.local`
- Might have to run it a couple of times.

### Tidy up image
- `sudo new-image-tidy.sh`

### Make OS Image
- Power off Raspberry Pi
- Remove SD card and put in computer.
- Make copy of image `sudo ./image-finalise.sh /dev/mmcblk0`
