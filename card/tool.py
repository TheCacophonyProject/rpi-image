import contextlib
import os
from os import path
import sys
import tempfile
from textwrap import dedent

from plumbum import cli
from plumbum.cmd import fdisk, partprobe
from wpasupplicantconf import WpaSupplicantConf

from .mount import Mount

# Used for configuration & installation access
PROTECTED_SSID = "bushnet"

PI_UID = 1000
PI_GID = 1000


class Tool(cli.Application):
    """Update the identity & WiFi details of a Cacophony Project Raspbian
    image stored on a SD card
    """

    PROGNAME = "cardtool"

    def main(self, *args):
        if args:
            print("Unknown command {0!r}".format(args[0]))
            return 1
        if not self.nested_command:
            print("No command given")
            return 1
        return 0


@Tool.subcommand("id")
class IdCommand(cli.Application):
    """Set the identity of a Cacophony Project Raspbian image
    """

    apiUrl = cli.SwitchAttr(
        "--url",
        str,
        default="https://api.cacophony.org.nz",
        help="the API server URL to upload to",
    )

    def main(self, device, name, group):
        with RaspbianMount(device) as mount_dir:
            set_minion_id(mount_dir, name)
            set_hostname(mount_dir, name)
            update_hosts(mount_dir, name)
            set_uploader_conf(mount_dir)
            set_device_conf(mount_dir, self.url, name, group)

        print("Card updated.")


@Tool.subcommand("wifi")
class WifiCommand(cli.Application):
    """Manipulate the wifi connection details stored in a Raspbian image
    """

    def main(self, *args):
        if args:
            print("Unknown command {0!r}".format(args[0]))
            return 1
        if not self.nested_command:
            print("No subcommand given")
            return 1
        return 0


@WifiCommand.subcommand("list")
class WifiListCommand(cli.Application):
    """Show the configured wifi networks on the SD card
    """

    def main(self, device):
        with RaspbianMount(device) as mount_dir:
            print("Configured wifi networks:")
            conf = parse_wpa_supplicant_conf(mount_dir)
            networks = conf.networks()
            if networks:
                for name in conf.networks().keys():
                    print(name)
            else:
                print("(none)")


@WifiCommand.subcommand("set")
class WifiSetCommand(cli.Application):
    """Adds or updates a WiFi network on the SD card
    """

    def main(self, device, ssid, password):
        if ssid == PROTECTED_SSID:
            sys.exit("This SSID can't be changed.")
        with RaspbianMount(device) as mount_dir:
            conf = parse_wpa_supplicant_conf(mount_dir)
            conf.add_network(ssid, psk='"{}"'.format(password))
            write_wpa_supplicant_conf(mount_dir, conf)

        print("{} network configured.".format(ssid))


@WifiCommand.subcommand("remove")
class WifiRemoveCommand(cli.Application):
    """Remove a WiFi network from the SD card
    """

    def main(self, device, ssid):
        if ssid == PROTECTED_SSID:
            sys.exit("This SSID can't be removed.")
        with RaspbianMount(device) as mount_dir:
            conf = parse_wpa_supplicant_conf(mount_dir)
            conf.remove_network(ssid)
            write_wpa_supplicant_conf(mount_dir, conf)

        print("{} network removed.".format(ssid))


@WifiCommand.subcommand("clear")
class WifiClearCommand(cli.Application):
    """Remove all WiFi networks from the SD card
    """

    def main(self, device):
        with RaspbianMount(device) as mount_dir:
            conf = parse_wpa_supplicant_conf(mount_dir)
            for name in list(conf.networks().keys()):
                if name != PROTECTED_SSID:
                    conf.remove_network(name)
            write_wpa_supplicant_conf(mount_dir, conf)

        print("All WiFi networks removed.")


@WifiCommand.subcommand("country")
class WifiCountryCommand(cli.Application):
    """Set the WiFi country code
    """

    def main(self, device, country):
        country = country.upper()
        with RaspbianMount(device) as mount_dir:
            conf = parse_wpa_supplicant_conf(mount_dir)
            conf.fields()["country"] = country
            write_wpa_supplicant_conf(mount_dir, conf)

        print("WiFi country changed to '{}'.".format(country))


@Tool.subcommand("ssh")
class SshCommand(cli.Application):
    """SSH related commands.
    """

    def main(self, *args):
        if args:
            print("Unknown command {0!r}".format(args[0]))
            return 1
        if not self.nested_command:
            print("No subcommand given")
            return 1
        return 0


@SshCommand.subcommand("enable")
class SshEnableCommand(cli.Application):
    """Enable SSH daemon at boot.
    """

    def main(self, device):
        with RaspbianMount(device) as mount_dir:
            open(path.join(mount_dir, "boot", "ssh"), "w").close()

        print("SSH daemon enabled at boot.")


@SshCommand.subcommand("add-key")
class SshAddKeyCommand(cli.Application):
    """Add a SSH public key for the "pi" user.
    """

    def main(self, device, key_path):
        with open(key_path) as key_file:
            key = key_file.read().strip()

        with RaspbianMount(device) as mount_dir:
            ssh_dir = path.join(mount_dir, "home", "pi", ".ssh")
            os.makedirs(ssh_dir, mode=0o700, exist_ok=True)

            auth_keys_path = path.join(ssh_dir, "authorized_keys")
            with open(auth_keys_path, "a") as auth_file:
                auth_file.write("\n" + key + "\n")

            os.chown(ssh_dir, PI_UID, PI_GID)
            os.chown(auth_keys_path, PI_UID, PI_GID)

        print('SSH public key added for "pi" user.')


class RaspbianMount:
    def __init__(self, device):
        # Ensure the kernel has the latest partition table for the SD
        # card (in case it's just been imaged).
        partprobe(device)

        self.stack = None
        self.boot_device, self.root_device = get_raspbian_devices(device)

    def __enter__(self):
        with contextlib.ExitStack() as stack:
            mount_dir = stack.enter_context(tempfile.TemporaryDirectory())
            stack.enter_context(Mount(self.root_device, mount_dir))

            boot_dir = path.join(mount_dir, "boot")
            stack.enter_context(Mount(self.boot_device, boot_dir))

            if not is_raspian(mount_dir):
                raise OSError("Not a Raspbian image?")

            self.stack = stack.pop_all()
            return mount_dir

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stack.close()


def get_raspbian_devices(device):
    partitions = get_parititions(device)
    if len(partitions) != 2:
        raise ValueError("expected 2 partitions, found {}".format(len(partitions)))
    return partitions


def get_parititions(device):
    return [
        line.split()[0]
        for line in fdisk("-l", device).splitlines()
        if line.startswith(device)
    ]


def is_raspian(root_dir):
    with open(path.join(root_dir, "etc", "os-release")) as f:
        return any(line.startswith("ID=raspbian") for line in f)


def set_minion_id(root_dir, name):
    with open(path.join(root_dir, "etc", "salt", "minion_id"), "w") as f:
        f.write(name)


def set_hostname(root_dir, hostname):
    with open(path.join(root_dir, "etc", "hostname"), "w") as f:
        f.write(hostname + "\n")


def update_hosts(root_dir, hostname):
    hosts_path = path.join(root_dir, "etc", "hosts")
    lines = []
    with open(hosts_path) as f:
        for line in f:
            if line.startswith("127.0.0.1"):
                lines.append("127.0.0.1 localhost " + hostname + "\n")
            else:
                lines.append(line)

    with open(hosts_path, "w") as f:
        f.write("".join(lines))


def set_uploader_conf(root_dir):
    with open(path.join(root_dir, "etc", "thermal-uploader.yaml"), "w") as f:
        f.write(
            dedent(
                """\
            directory: "/var/spool/cptv"
            """
            )
        )

    try_delete(path.join(root_dir, "etc", "thermal-uploader-priv.yaml"))


def set_device_conf(root_dir, url, name, group):
    with open(path.join(root_dir, "etc", "cacophony", "device.yaml"), "w") as f:
        f.write(
            dedent(
                """\
            server-url: "{url}"
            group: "{group}"
            device-name: "{name}"
            """
            ).format(url=url, group=group, name=name)
        )

    try_delete(path.join(root_dir, "etc", "cacophony", "device-priv.yaml"))


def parse_wpa_supplicant_conf(root):
    with open(wpa_supplicant_path(root)) as f:
        return WpaSupplicantConf(f)


def write_wpa_supplicant_conf(root, conf):
    with open(wpa_supplicant_path(root), "wt") as f:
        conf.write(f)


def wpa_supplicant_path(root):
    return path.join(root, "etc", "wpa_supplicant", "wpa_supplicant.conf")


def try_delete(filename):
    try:
        os.unlink(filename)
    except FileNotFoundError:
        pass


if __name__ == "__main__":
    if os.geteuid() != 0:
        sys.exit("Not running as root. sudo?")
    Tool.run()
