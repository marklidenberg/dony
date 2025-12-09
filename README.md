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

    dony.shell("npm run build")
    dony.shell("npm test")
    dony.shell(f"./deploy.sh {env}", confirm=True)

    dony.success(f"Deployed to {env}")

if __name__ == "__main__":
    deploy()
```

Run with `python deploy.py`

## Notes

- Available directories to run from: `"current_dir"` (default), `"git_root"`, `"command_file"`, `"temp_dir"`, or custom path string
- User prompts: `dony.input()`, `dony.confirm()`, `dony.select()`, `dony.select_many()`, `dony.press_any_key()`

## API Reference

```python
# Command decorator
@dony.command(
    run_from: Union[str, Path, Literal["git_root", "command_file", "current_dir", "temp_dir"]] = "current_dir",
    verbose: bool = True,
)

# Shell execution
dony.shell(
    command: str,
    run_from: Optional[Union[str, Path]] = None,
    dry_run: bool = False,
    quiet: bool = False,
    capture_output: bool = True,
    abort_on_failure: bool = True,
    abort_on_unset_variable: bool = True,
    trace_execution: bool = False,
    show_command: bool = True,
    confirm: bool = False,
) -> str

# User prompts
dony.input(prompt: str, default: str = "") -> str
dony.confirm(message: str, default: bool = False) -> bool
dony.select(message: str, choices: list, fuzzy: bool = False) -> str
dony.select_many(message: str, choices: list, fuzzy: bool = False) -> list[str]
dony.press_any_key(message: str = "Press any key to continue...")

# Output
dony.echo(message: str, style: str = "")
dony.success(message: str)
dony.error(message: str)
```

## License

MIT License

## Author

Mark Lidenberg [marklidenberg@gmail.com](mailto:marklidenberg@gmail.com)
