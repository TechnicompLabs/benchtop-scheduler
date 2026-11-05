// SPDX-License-Identifier: MPL-2.0
// Benchtop Focus Priority, the Technicomp Benchtop Linux fork of s76-scheduler
// by Ossian Winter (https://github.com/ossianwinter/s76-scheduler).

import { Extension } from 'resource:///org/gnome/shell/extensions/extension.js';

import Gio from 'gi://Gio';

const SCHEDULER_INTERFACE = '<node> \
  <interface name="com.system76.Scheduler"> \
    <method name="SetForegroundProcess"> \
      <arg name="pid" type="u" direction="in" /> \
    </method> \
  </interface> \
</node> \
';

const SchedulerProxy = Gio.DBusProxy.makeProxyWrapper(SCHEDULER_INTERFACE);

export default class FocusPriorityExtension extends Extension {
  enable() {
    this._foreground = 0;

    // TCBL: the proxy is made here rather than when the module loads, and
    // asynchronously, so that enabling never blocks the shell
    const cancellable = new Gio.Cancellable();
    this._cancellable = cancellable;
    new SchedulerProxy(Gio.DBus.system, 'com.system76.Scheduler', '/com/system76/Scheduler', (proxy, error) => {
      if (cancellable.is_cancelled()) {
        return;
      }

      if (error) {
        logError(error);
        return;
      }

      this._proxy = proxy;
    }, cancellable, Gio.DBusProxyFlags.DO_NOT_LOAD_PROPERTIES);

    this._handler = global.display.connect('notify::focus-window', () => {
      if (!this._proxy) {
        return;
      }

      const meta_window = global.display.get_focus_window();
      if (!meta_window) {
        return;
      }

      const pid = meta_window.get_pid();
      if (!pid || pid === this._foreground) {
        return;
      }

      this._foreground = pid;
      this._proxy.SetForegroundProcessRemote(pid, (result, error) => {
        if (!error) {
          return;
        }

        logError(error);
      });
    });
  }

  disable() {
    global.display.disconnect(this._handler);
    this._handler = null;

    // TCBL: release the proxy and forget the last process
    this._cancellable.cancel();
    this._cancellable = null;
    this._proxy = null;
    this._foreground = 0;
  }
}
