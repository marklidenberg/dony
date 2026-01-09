# 🍥️ dony

A lightweight Python command runner with shell execution and user interactions.

Commands are just Python functions. You run them by running Python files directly (`python deploy.py`).

## Installation

```bash
pip install dony
```

Optional dependencies:

```bash
brew install fzf     # For fuzzy selection
brew install shfmt   # For shell command formatting
```

## Example

```python
import asyncio
import dony

@dony.command()
async def deploy():
    """Deploy application"""

    if not await dony.confirm("Deploy to production?"):
        return

    env = await dony.select("Select environment:", ["staging", "production"])

    await dony.shell(f"""
        npm run build
        npm test
        ./deploy.sh {env}
    """)

    await dony.success(f"Deployed to {env}")

if __name__ == "__main__":
    asyncio.run(deploy())
```

Run with `python deploy.py`

## CLI Support

For CLI support, use [fire](https://github.com/google/python-fire) or any other CLI framework:

```python
import asyncio
import dony
import fire

@dony.command()
async def build(env: str = None):
    """Build application"""

    env = env or await dony.select("Select environment:", ["staging", "production"])

    await dony.shell(f"""
        npm run build --env={env}
        npm test
    """)

    await dony.success(f"Built for {env}")

if __name__ == "__main__":
    fire.Fire(build)
```

Run interactively: `python build.py`
Run with CLI args: `python build.py --env=production`

## Recipes

### Working from git repo root

```python
import asyncio
from functools import partial
import dony

async def main():
    shell = partial(dony.shell, run_from=dony.find_repo_root(__file__))

    await shell("npm run build")
    await shell("npm test")

if __name__ == "__main__":
    asyncio.run(main())
```

## Things to know

- `@dony.command()`: marker decorator for commands (currently a no-op)
- Available prompts based on [questionary](https://github.com/tmbo/questionary):
  - `dony.input()`: free-text entry
  - `dony.confirm()`: yes/no ([Y/n] or [y/N])
  - `dony.select()`: option picker (supports fuzzy)
  - `dony.select_many()`: multiple option picker (supports fuzzy)
  - `dony.press_any_key()`: pause until keypress
  - `dony.echo()`: styled text output
  - `dony.error()`: ✕ error message
  - `dony.success()`: ✓ success message

## API Reference

```python
async def dony.shell(
    command: str,
    run_from: Optional[Union[str, Path]] = None,   # Working directory
    dry_run: bool = False,                         # Print without executing
    quiet: bool = False,                           # Suppress printing output
    capture_output: bool = True,                   # Return output as string
    abort_on_failure: bool = True,                 # Prepends 'set -e'
    abort_on_unset_variable: bool = True,          # Prepends 'set -u'
    trace_execution: bool = False,                 # Prepends 'set -x'
    show_command: bool = True,                     # Print formatted command
    confirm: bool = False,                         # Ask before executing
) -> str:
    ...

def dony.find_repo_root(path: Union[str, Path]) -> Path:
    """Find the git root directory starting from the given path."""
    ...
```

## License

MIT License

## Author

Mark Lidenberg [marklidenberg@gmail.com](mailto:marklidenberg@gmail.com)
