from gettext import gettext as _
from typing import TYPE_CHECKING

from blueman.bluez import Adapter
from blueman.Functions import create_menuitem, launch
from blueman.gui.manager.ManagerDeviceMenu import MenuItemsProvider, DeviceMenuItem
from blueman.plugins.ManagerPlugin import ManagerPlugin

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


if TYPE_CHECKING:
    from blueman.main.Manager import Blueman


ADDRESS_BLOCKS = ['C0:28:8D']


def turn_on(device_addr: str, blueman: "Blueman"):
    adapter = Adapter(obj_path=blueman.List.get_adapter_path())
    adapter_addr: str = adapter['Address']
    value = adapter_addr.replace(':', '').upper() + '01'
    launch(f"gatttool -b {device_addr} --char-write-req -a 0x0003 -n {value}")


class UeBoom(ManagerPlugin, MenuItemsProvider):
    def on_request_menu_items(self, manager_menu, device, powered):
        addr = device['Address']
        if isinstance(addr, str) and addr[0:8] in ADDRESS_BLOCKS:
            item = create_menuitem(_("Turn _on speaker"), "switch-on-symbolic")
            item.props.tooltip_text = _("Turn on the Ultimate Ears speaker remotely")
            item.connect('activate', lambda x: turn_on(addr, self.parent))
            return [DeviceMenuItem(item, DeviceMenuItem.Group.ACTIONS, 600)]
        else:
            return []
