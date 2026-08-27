#!/usr/bin/env bash
# Cloud Agent environment bootstrap for the 1C AI Development Kit.
#
# The kit ships cross-platform PowerShell helper scripts (skills 1c-mxl,
# 1c-forms, 1c-roles) that compile / validate / analyze 1C artifacts.
# PowerShell Core (pwsh) is the only runtime dependency; there is no npm/pip
# project to bootstrap. This script installs pwsh idempotently.
set -euo pipefail

if command -v pwsh >/dev/null 2>&1; then
	echo "[install] pwsh already present: $(pwsh --version)"
	exit 0
fi

echo "[install] Installing PowerShell Core..."

. /etc/os-release
UBUNTU_VERSION="${VERSION_ID:-24.04}"

TMP_DEB="$(mktemp --suffix=.deb)"
trap 'rm -f "$TMP_DEB"' EXIT

sudo apt-get update -qq
sudo apt-get install -y -qq wget apt-transport-https software-properties-common ca-certificates

wget -q "https://packages.microsoft.com/config/ubuntu/${UBUNTU_VERSION}/packages-microsoft-prod.deb" -O "$TMP_DEB"
sudo dpkg -i "$TMP_DEB"
sudo apt-get update -qq
sudo apt-get install -y -qq powershell

echo "[install] Done: $(pwsh --version)"
