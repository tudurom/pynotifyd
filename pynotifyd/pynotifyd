#!/usr/bin/env python3
from typing import Any, List, Dict, Tuple
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)
import dbus.service
import dbus
import threading
import queue
import time
import json
import os
import os.path
import tempfile
import sys

DEFAULT_TIMEOUTS = [3000, 5000, 0]
q = queue.Queue()

class Notification:
    id: int
    app_name: str
    app_icon: str
    summary: str
    body: str
    actions: List[Tuple[str, str]]
    urgency: int

    def __init__(self, id: int, app_name: str, app_icon: str, summary: str, body: str, actions: List[str], hints: Dict[str, Any]):
        self.id = id
        self.app_name = app_name
        self.app_icon = app_icon
        self.summary = summary
        self.body = body

        for i in range(0, len(actions), 2):
            self.actions.append((actions[i], actions[i + 1]))

        if 'urgency' in hints:
            self.urgency = hints['urgency']
        else:
            self.urgency = 2

    def __str__(self) -> str:
        return '[{app_name}] ({summary}) {body}'.format(app_name = self.app_name, summary = self.summary, body = self.body)

class IPC:
    q: queue.Queue

    def __writer(self):
        self.q = queue.Queue()
        while True:
            d = self.q.get()
            print(d.replace('\n', '\\n')+'\n')
            sys.stdout.flush()

    def __init__(self):
        threading.Thread(target=self.__writer).start()

    def __send_event(self, action: str, **kwargs):
        self.q.put(json.dumps({'action': action, **kwargs}), block=False)

    def notify(self, n: Notification):
        self.__send_event('notify', notification=vars(n))

    def delete(self, id: int):
        self.__send_event('delete', id=id)

    def replace(self, replaces_id: int, n: Notification):
        self.__send_event('replace', replaces_id=replaces_id, notification=vars(n))

ipc = IPC()

class Notifications(dbus.service.Object):
    active: Dict[int, Notification] = {}
    next_id: int = 1

    def __init__(self, bus_name: str, object_path: str):
        dbus.service.Object.__init__(self, bus_name, object_path)

    @dbus.service.method(dbus_interface='org.freedesktop.Notifications', out_signature='as')
    def GetCapabilities(self) -> List[str]:
        return ['body', 'persistent']

    @dbus.service.method(dbus_interface='org.freedesktop.Notifications', in_signature='susssasa{sv}i', out_signature='u')
    def Notify(self, app_name: str, replaces_id: int, app_icon: str, summary: str, body: str, actions: List[str], hints: Dict[str, Any], expire_timeout: int) -> int:
        new_id = replaces_id
        if replaces_id == 0:
            new_id = self.next_id
            self.next_id += 1

        n = Notification(new_id, app_name, app_icon, summary, body, actions, hints)
        self.active[new_id] = n
        print(new_id, expire_timeout, n, '!' * (n.urgency + 1), file=sys.stderr)
        if expire_timeout == -1:
            expire_timeout = DEFAULT_TIMEOUTS[n.urgency]
        if expire_timeout > 0:
            q.put((new_id, expire_timeout, self.active))
        if replaces_id == 0:
            ipc.notify(n)
        else:
            ipc.replace(replaces_id, n)
        return replaces_id

    @dbus.service.method(dbus_interface='org.freedesktop.Notifications', out_signature='ssss')
    def GetServerInformation(self) -> Tuple[str, str, str, str]:
        return ('lel', 'tudor', '0.0', '1.2')

def apply_timeout(notification_id: int, millis: int, active: Dict[int, Notification]):
    time.sleep(millis / 1000)
    if notification_id in active:
        del active[notification_id]
        print('Notification {} expired after {} millis'.format(notification_id, millis), file=sys.stderr)
        ipc.delete(notification_id)

def main():
    loop = GLib.MainLoop()
    bus = dbus.SessionBus()
    bus_name = dbus.service.BusName('org.freedesktop.Notifications', bus=bus)
    Notifications(bus_name, '/org/freedesktop/Notifications')

    loop.run()

def timeouter():
    while True:
        t = q.get()
        threading.Thread(target=apply_timeout, args=t).start()

if __name__ == "__main__":
    main_thread = threading.Thread(target=main)
    timeouter_thread = threading.Thread(target=timeouter)
    timeouter_thread.start()
    main_thread.start()
