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

## Quick Example

```python
import dony

@dony.command(run_from=dony.RunFrom.GIT_ROOT)
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

## Core Features

### Commands

The `@dony.command()` decorator handles working directory management and success/failure messaging:

```python
@dony.command(run_from=dony.RunFrom.GIT_ROOT)     # Run from git root
@dony.command(run_from=dony.RunFrom.COMMAND_FILE) # Run from script's directory (default)
@dony.command(run_from=dony.RunFrom.CWD)          # Run from current directory
@dony.command(run_from=dony.RunFrom.TEMP)         # Run from temporary directory
@dony.command(run_from="/custom/path")            # Run from custom path
```

### Shell Execution

```python
dony.shell(
    command: str,
    run_from: Optional[Union[str, Path]] = None,  # Working directory
    dry_run: bool = False,                         # Print without executing
    quiet: bool = False,                           # Suppress output
    capture_output: bool = True,                   # Return output as string
    abort_on_failure: bool = True,                 # Prepends 'set -e'
    abort_on_unset_variable: bool = True,          # Prepends 'set -u'
    trace_execution: bool = False,                 # Prepends 'set -x'
    show_command: bool = True,                     # Display formatted command
    confirm: bool = False,                         # Ask before executing
) -> str
    ...

result = dony.shell('git status', quiet=True)
dony.shell('npm test', confirm=True)
dony.shell('ls', run_from='/tmp')
```

### User Prompts

```python
# Text input
name = dony.input('Enter your name:', default='World')

# Confirmation
if dony.confirm('Continue?', default=True):
    pass

# Single selection
framework = dony.select('Pick a framework:', ['React', 'Vue', 'Angular'], fuzzy=True)

# Multiple selection
features = dony.select_many('Pick features:', ['auth', 'api', 'ui'], fuzzy=True)

# Pause
dony.press_any_key('Press any key to continue...')

dony.echo('Message', style='bold')
dony.success('Operation completed!')  # Green with ✓
dony.error('Operation failed!')       # Red with ✕
```


## Use Cases

- Build, deploy, and release scripts
- DevOps automation
- Testing workflows
- Git operations

## License

MIT License

## Author

Mark Lidenberg [marklidenberg@gmail.com](mailto:marklidenberg@gmail.com)
