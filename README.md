# benchtop-scheduler

Technicomp Benchtop Linux packaging of [System76 Scheduler](https://github.com/pop-os/system76-scheduler), and Benchtop Focus Priority, the GNOME Shell extension that reports the focused window to it. Each subdirectory is one OBS package in home:technicomp:benchtop, connected by scmsync (`?subdir=`).

- `system76-scheduler/` builds `system76-scheduler` from a pinned upstream commit, named in `update-sources.sh`. After changing the commit there, run the script on Linux (it needs cargo and cargo-vendor-filterer); it remakes the source archive and `vendor.tar.zst` (the crates for x86-64 Linux, about 7 MB), and prints the version to set in the spec. Remove the previous source archive from git. The daemon uses `bpf-execsnoop` (libbpf-tools) to see new processes. The configuration is upstream's, unchanged, installed as the distribution configuration in `/usr/share/system76-scheduler`; `/etc/system76-scheduler/config.kdl` overrides it.
- `gnome-shell-extension-benchtop-focus-priority/` builds the extension, a fork of [s76-scheduler](https://github.com/ossianwinter/s76-scheduler) by Ossian Winter, whose history is kept here. It is under the Mozilla Public License 2.0, as the original is (its `LICENSE`).

tc-benchtop-settings enables the service (preset) and the extension (GSettings); patterns-tc-benchtop-base requires both packages.
