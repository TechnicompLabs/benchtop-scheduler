#
# spec file for package gnome-shell-extension-benchtop-focus-priority
# Technicomp Benchtop Linux - tells System76 Scheduler which process owns the
# focused window.
#
# Built directly from git (OBS scmsync, this subdirectory). The extension is
# laid out as a filesystem tree (usr/) that mirrors its install path; the spec
# installs that tree verbatim, as tc-benchtop-settings does.
#
%global uuid focus-priority@technicomplabs.github.io
%global extdir %{_datadir}/gnome-shell/extensions/%{uuid}
Name:           gnome-shell-extension-benchtop-focus-priority
Version:        1
Release:        0
Summary:        GNOME Shell extension that gives the focused application priority
# a fork of s76-scheduler by Ossian Winter (MPL-2.0)
License:        MPL-2.0
URL:            https://github.com/TechnicompLabs/benchtop-scheduler
BuildArch:      noarch
Requires:       gnome-shell >= 46
Requires:       system76-scheduler

%description
Benchtop Focus Priority tells System76 Scheduler which process owns the
focused window, so that the scheduler gives that process its foreground
priority and the processes of other windows its background priority. A fork of
s76-scheduler by Ossian Winter, for Technicomp Benchtop Linux.

%prep

%build

%install
treeroot=
for base in "%{_sourcedir}" "%{_sourcedir}/%{name}-%{version}" "%{_topdir}/SOURCES" "%{_builddir}/%{name}-%{version}" "%{_builddir}" "$PWD"; do
    if [ -d "$base/usr/share/gnome-shell/extensions/%{uuid}" ]; then
        treeroot="$base"
        break
    fi
done
if [ -z "$treeroot" ]; then
    echo "ERROR: file tree (usr/) not found under the build sources" >&2
    exit 1
fi
install -d "%{buildroot}"
( cd "$treeroot" && cp -a --no-preserve=ownership usr "%{buildroot}/" )

%files
%dir %{_datadir}/gnome-shell
%dir %{_datadir}/gnome-shell/extensions
%dir %{extdir}
%{extdir}/extension.js
%{extdir}/metadata.json
%doc %{extdir}/README.md
%license %{extdir}/LICENSE

%changelog
