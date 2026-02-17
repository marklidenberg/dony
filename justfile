set dotenv-load

release_patch:
    uv run python scripts/release.py --version patch --uv-publish-token $UV_PUBLISH_TOKEN

release_minor:
    uv run python scripts/release.py --version minor --uv-publish-token $UV_PUBLISH_TOKEN

release_major:
    uv run python scripts/release.py --version major --uv-publish-token $UV_PUBLISH_TOKEN
