# Benchtop Focus Priority

GNOME Shell extension that tells [System76 Scheduler](https://github.com/pop-os/system76-scheduler) which process owns the focused window, so that the scheduler gives it its foreground priority. Part of Technicomp Benchtop Linux, which packages it as `gnome-shell-extension-benchtop-focus-priority`.

A fork of [s76-scheduler](https://github.com/ossianwinter/s76-scheduler) by Ossian Winter, under the same license, the Mozilla Public License 2.0 (`LICENSE`). Changes from it: the name and UUID; GNOME 50 and 51 declared; the D-Bus proxy made, asynchronously, when the extension is enabled instead of when it loads, and released when it is disabled.

Requires System76 Scheduler, with `com.system76.Scheduler.service` running.
