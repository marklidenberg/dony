# 🍥️ dony

A lightweight Python command runner with shell execution and user interactions.

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
import dony

@dony.command(run_from="git_root")
def deploy():
    """Deploy application"""

    if not dony.confirm("Deploy to production?"):
        return

    env = dony.select("Select environment:", ["staging", "production"])

    dony.shell(f"""
        npm run build
        npm test
        ./deploy.sh {env}
    """)

    dony.success(f"Deployed to {env}")

if __name__ == "__main__":
    deploy()
```

Run with `python deploy.py`

### CLI arguments

To support non-interactive mode, keep all interactions within arguments:

```python
import dony

@dony.command(run_from="git_root")
def build(env: str | None = None):
    """Build application"""

    # CLI arg if provided, otherwise prompt interactively
    env = env or dony.select("Select environment:", ["staging", "production"])

    dony.shell(f"""
        npm run build --env={env}
        npm test
    """)

    dony.success(f"Built for {env}")

if __name__ == "__main__":
    build()
```

Run interactively: `python build.py`
Run with CLI args: `python build.py --env=production`

CLI argument parsing is powered by [typer](https://github.com/fastapi/typer).

## Things to know

- Available directories to run from:
  - `"current_dir"` (default)
  - `"git_root"`
  - `"command_file"`
  - `"temp_dir"`
  - Custom path string
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
def command(
    run_from: Union[str, Path, Literal[ "current_dir", "git_root", "command_file", "temp_dir"]] = "current_dir",
    verbose: bool = True,
) -> Callable[[F], F]:
    ...

def dony.shell(
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
```

## License

MIT License

## Author

Mark Lidenberg [marklidenberg@gmail.com](mailto:marklidenberg@gmail.com)
