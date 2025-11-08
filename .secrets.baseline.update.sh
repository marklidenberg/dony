#!/usr/bin/env bash

set -euo pipefail
uv tool install detect-secrets
uvx detect-secrets scan > .secrets.baseline