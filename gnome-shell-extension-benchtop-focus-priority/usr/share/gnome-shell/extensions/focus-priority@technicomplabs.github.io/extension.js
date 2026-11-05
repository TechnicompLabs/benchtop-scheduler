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
const schedulerProxy = new SchedulerProxy(Gio.DBus.system, 'com.system76.Scheduler', '/com/system76/Scheduler');

export default class System76SchedulerExtension extends Extension {
  enable() {
    this._foreground = 0;

    this._handler = global.display.connect('notify::focus-window', () => {
      const meta_window = global.display.get_focus_window();
      if (!meta_window) {
        return;
      }

      const pid = meta_window.get_pid();
      if (!pid || pid === this._foreground) {
        return;
      }

      this._foreground = pid;
      schedulerProxy.SetForegroundProcessRemote(pid, (result, error) => {
        if (!error) {
          return;
        }

        logError(error);
      });
    });
  }

  disable() {
    global.display.disconnect(this._handler);
  }
}
