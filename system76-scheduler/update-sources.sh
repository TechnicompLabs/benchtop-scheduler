#!/bin/bash
# SPDX-License-Identifier: MIT
# Makes the two source archives of system76-scheduler.spec from the upstream
# commit named below:
#   system76-scheduler-VERSION.tar.zst  upstream's tree at COMMIT
#   vendor.tar.zst                      the crates it needs on x86-64 Linux,
#                                       with the .cargo/config.toml that uses them
# Needs curl, tar, zstd, cargo and cargo-vendor-filterer (cargo install
# cargo-vendor-filterer), on Linux. After changing COMMIT, BASE and DATE: run
# it here, git rm the previous source archive, and set Version in the spec to
# the version it prints. An already downloaded tarball of COMMIT from GitHub
# can be given as the first argument instead of downloading it.
set -euo pipefail

COMMIT=20fe9020b48efcce0cb790f35402914c6cabc669  # master, October 27, 2026
BASE=2.0.2                                       # the last release before COMMIT
DATE=20261027                                    # COMMIT's date

version="${BASE}+git${DATE}.${COMMIT:0:7}"
here=$(cd "$(dirname "$0")" && pwd)
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

if [ $# -ge 1 ]; then
    tar -xzf "$1" -C "$work"
else
    curl -sSfL "https://codeload.github.com/pop-os/system76-scheduler/tar.gz/${COMMIT}" | tar -xz -C "$work"
fi
mv "$work/system76-scheduler-${COMMIT}" "$work/system76-scheduler-${version}"
src="$work/system76-scheduler-${version}"

# reproducible archives: sorted names, no timestamps or owners
pack() {
    local out=$1 dir=$2
    shift 2
    tar --sort=name --mtime=@0 --owner=0 --group=0 --numeric-owner -C "$dir" -cf - "$@" | zstd -q -19 -T0 -f -o "$out"
}

pack "$here/system76-scheduler-${version}.tar.zst" "$work" "system76-scheduler-${version}"

# crates for other platforms are left as empty stubs, which keeps the archive
# small (about 7 MB)
( cd "$src" && mkdir -p .cargo && cargo vendor-filterer --platform=x86_64-unknown-linux-gnu vendor > .cargo/config.toml )
pack "$here/vendor.tar.zst" "$src" vendor .cargo/config.toml

echo "Version: ${version}"
