import dony


def main():
    dony.shell("""
        set -euo pipefail
        uv tool install detect-secrets
        uvx detect-secrets scan > .secrets.baseline
    """)
