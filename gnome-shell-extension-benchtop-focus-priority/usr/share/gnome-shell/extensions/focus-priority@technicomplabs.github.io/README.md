# s76-scheduler
Tiny GNOME extension that updates process priorities using the [System76 Scheduler](https://github.com/pop-os/system76-scheduler).

## Installation
### Prerequisites
You must install [System76 Scheduler](https://github.com/pop-os/system76-scheduler) separately.

Ensure that the `com.system76.Scheduler` service is enabled:
```
sudo systemctl enable --now com.system76.Scheduler.service
```

### From source (recommended)
```bash
git clone https://github.com/ossianwinter/s76-scheduler ~/.local/share/gnome-shell/extensions/s76-scheduler@winter.vg
```

### Other installation methods
- `gnome-shell-extension-s76-scheduler` in the [Arch Linux User Repository](https://aur.archlinux.org/packages/gnome-shell-extension-s76-scheduler)
- `gnome-shell-extension-s76-scheduler` in the [Arch Linux Chinese Community Repository](https://github.com/archlinuxcn/repo/tree/master/archlinuxcn/gnome-shell-extension-s76-scheduler) (maintained by [@everyx](https://github.com/everyx))
