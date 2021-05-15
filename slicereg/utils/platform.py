import platform

from packaging import version


def is_mac_big_sur() -> bool:
    """
    platform.system(): 'Darwin'
    platform.release(): '20.3.0' or '20.4.0'
    platform.mac_ver(): ('10.16', ('', '', ''), 'arm64') or ('10.16', ('', '', ''), 'x86_64') or ('11.3', ('', '', ''), 'arm64')
    """
    return platform.system() == 'Darwin' and version.parse(platform.mac_ver()[0]) >= version.parse('10.16')