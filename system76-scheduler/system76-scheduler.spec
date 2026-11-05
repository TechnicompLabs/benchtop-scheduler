#
# spec file for package system76-scheduler
# Technicomp Benchtop Linux - System76 Scheduler, from a pinned upstream
# commit.
#
# Built from git (OBS scmsync, this subdirectory). The two source archives are
# made by update-sources.sh, which names the upstream commit: upstream's tree,
# and the crates it needs on x86-64 Linux (vendor.tar.zst).
#
# The daemon watches new processes with execsnoop. It is built against the
# libbpf version from openSUSE's bcc package (bpf-execsnoop: compiled BPF that
# uses the kernel's BTF), which prints the same columns as bcc's Python
# execsnoop and needs neither kernel headers nor LLVM at run time.
%global execsnoop %{_sbindir}/bpf-execsnoop
Name:           system76-scheduler
Version:        2.0.2+git20261027.20fe902
Release:        0
Summary:        Process priorities and CPU scheduler settings for desktop responsiveness
# the program (MPL-2.0) and the crates it is built with, from their Cargo
# metadata at this commit, x86-64 Linux
License:        MPL-2.0 AND MIT AND Apache-2.0 AND (Apache-2.0 OR MIT) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND Apache-2.0 WITH LLVM-exception AND (Apache-2.0 OR BSL-1.0) AND BSD-3-Clause AND ISC AND Unicode-DFS-2016 AND (Unlicense OR MIT) AND Zlib
URL:            https://github.com/pop-os/system76-scheduler
Source0:        %{name}-%{version}.tar.zst
Source1:        vendor.tar.zst
BuildRequires:  cargo-packaging
# bindgen, for the pipewire crate
BuildRequires:  clang-devel
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  systemd-rpm-macros
BuildRequires:  zstd
Requires:       libbpf-tools
%{?systemd_ordering}

%description
System76 Scheduler assigns process priorities (nice, I/O priority and
scheduling policy) by configurable profiles: the sound server and audio
applications first, then the focused application, then other applications,
user session services, system services, package managers and batch jobs. It
also switches the kernel's CPU scheduler settings between a responsive profile
on AC power and the kernel defaults on battery. The focused application is
reported over D-Bus (com.system76.Scheduler), on GNOME by the Benchtop Focus
Priority extension.

%prep
%autosetup -p1 -a1

%build
export EXECSNOOP_PATH=%{execsnoop}
# the workspace's only program is the daemon; the other members are its libraries
%{cargo_build}

%install
install -D -m 0755 target/release/system76-scheduler %{buildroot}%{_bindir}/system76-scheduler
# the distribution configuration (/usr/share); /etc/system76-scheduler overrides it
install -D -m 0644 data/config.kdl %{buildroot}%{_datadir}/system76-scheduler/config.kdl
install -D -m 0644 data/pop_os.kdl %{buildroot}%{_datadir}/system76-scheduler/process-scheduler/pop_os.kdl
install -D -m 0644 data/com.system76.Scheduler.service %{buildroot}%{_unitdir}/com.system76.Scheduler.service
install -D -m 0644 data/com.system76.Scheduler.conf %{buildroot}%{_datadir}/dbus-1/system.d/com.system76.Scheduler.conf

%pre
%service_add_pre com.system76.Scheduler.service

%post
%service_add_post com.system76.Scheduler.service

%preun
%service_del_preun com.system76.Scheduler.service

%postun
%service_del_postun com.system76.Scheduler.service

%files
%license LICENSE
%doc README.md
%{_bindir}/system76-scheduler
%dir %{_datadir}/system76-scheduler
%dir %{_datadir}/system76-scheduler/process-scheduler
%{_datadir}/system76-scheduler/config.kdl
%{_datadir}/system76-scheduler/process-scheduler/pop_os.kdl
%{_unitdir}/com.system76.Scheduler.service
%dir %{_datadir}/dbus-1
%dir %{_datadir}/dbus-1/system.d
%{_datadir}/dbus-1/system.d/com.system76.Scheduler.conf

%changelog
