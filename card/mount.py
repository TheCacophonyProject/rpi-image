import os
from os import path

from plumbum.cmd import mount, umount


class Mount:
    """This context manager handles mounting and unmounting of a
    device. The mount is created when the context manager is entered
    and unmounted when the context manager exits.
    """

    def __init__(self, device, mount_point):
        self.mount_point = mount_point
        self.args = [
            device,
            mount_point,
        ]

    def __enter__(self):
        if not path.isdir(self.mount_point):
            os.makedirs(self.mount_point)
        mount(*self.args)

    def __exit__(self, _, __, ___):
        umount(self.mount_point)


def try_delete(filename):
    try:
        os.unlink(filename)
    except FileNotFoundError:
        pass
