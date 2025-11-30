# 🍥️ dony

A lightweight Python command runner with user interactions.

## How it works

Write Python functions decorated with `@dony.command()`. Each command is a regular Python script with access to:

- **Shell execution**: `dony.shell()` for running shell commands
- **User prompts**: `dony.input()`, `dony.confirm()`, `dony.select()` and more

```python
# hello_world.py

import dony


@dony.command()
def hello_world():
    dony.shell('echo "Hello, world!"')


if __name__ == "__main__":
    hello_world()
```

Run it:

```bash
python hello_world.py
```

## Quick Start

Install dony:

```bash
pip install dony
```

Optional dependencies for better experience:

```bash
# fzf for fuzzy selection (optional)
brew install fzf

# shfmt for shell command formatting (optional)
brew install shfmt
```

## Core API

### 1. Commands

Decorate Python functions with `@dony.command()`:

```python
import dony

@dony.command()
def greet(name: str = 'World'):
    """Greets the user"""
    dony.shell(f"echo Hello, {name}!")

if __name__ == "__main__":
    greet()
```

The decorator handles:

- Changing to the correct working directory (configurable via `run_from`)
- Success/failure messages (configurable via `verbose`)

Working directory options:

```python
@dony.command(run_from=dony.RunFrom.GIT_ROOT)  # Run from git root
@dony.command(run_from=dony.RunFrom.COMMAND_FILE)  # Run from script's directory (default)
@dony.command(run_from=dony.RunFrom.CWD)  # Run from current directory
@dony.command(run_from=dony.RunFrom.TEMP)  # Run from temporary directory
@dony.command(run_from="/custom/path")  # Run from custom path
```

### 2. Shell Execution

Execute shell commands with enhanced control and safety:

```python
result = dony.shell('git status', quiet=True)
dony.shell('npm test', confirm=True)  # Ask for confirmation first
dony.shell('ls', run_from='/tmp')  # Run in specific directory
```

### 3. User Prompts

Rich interactive prompts for user input:

```python
name = dony.input('Enter your name:', default='World')
if dony.confirm('Continue?'):
    framework = dony.select('Pick a framework:', ['React', 'Vue', 'Angular'])
    dony.success(f'You chose {framework}!')
```

## Use cases

- Build, deploy, release scripts
- DevOps automation
- Testing workflows
- Git operations
- Any shell automation task

## Important Notes

- **Pure Python**: Scripts are just Python functions - run them directly with `python script.py`
- **Shell integration**: Use `dony.shell()` for any shell operations
- **Interactive by default**: Built-in prompts make scripts user-friendly
- **CLI** is not currently implemented

## API Reference

### Available Functions

**Prompts** (based on `questionary`):

- `dony.input(message, default='', allow_empty=False, multiline=False)`: text entry
- `dony.confirm(message, default=True)`: yes/no confirmation (uses select internally)
- `dony.select(message, choices, default=None, fuzzy=True, allow_custom=False)`: single option picker
- `dony.select_many(message, choices, default=None, fuzzy=True)`: multi-option picker
- `dony.press_any_key(message)`: pause until keypress

**Output**:

- `dony.echo(message, style)`: styled text output
- `dony.error(message, prefix='✕ ')`: error message in red
- `dony.success(message, prefix='✓ ')`: success message in green

**Utilities**:

- `dony.shell(command, **options)`: execute shell commands
- `dony.command(run_from, verbose)`: decorator for command functions
- `dony.find_git_root(path)`: find git repository root

### Shell Command API

The `dony.shell()` function executes shell commands with enhanced features:

```python
dony.shell(
    command: str,
    run_from: Optional[Union[str, Path]] = None,  # Working directory
    dry_run: bool = False,                         # Print command without executing
    quiet: bool = False,                           # Suppress output
    capture_output: bool = True,                   # Return output as string
    abort_on_failure: bool = True,                 # Prepends 'set -e'
    abort_on_unset_variable: bool = True,          # Prepends 'set -u'
    trace_execution: bool = False,                 # Prepends 'set -x'
    show_command: bool = True,                     # Display formatted command
    confirm: bool = False,                         # Ask before executing
) -> str
```

## Example

```python
import dony

@dony.command(run_from=dony.RunFrom.GIT_ROOT)
def deploy():
    """Deploy application"""

    # Confirm action
    if not dony.confirm("Deploy to production?"):
        return

    # Select environment
    env = dony.select(
        "Select environment:",
        choices=["staging", "production"],
        fuzzy=False
    )

    # Run build
    dony.shell("npm run build")

    # Run tests
    dony.shell("npm test")

    # Deploy
    dony.shell(f"./deploy.sh {env}", confirm=True)

    dony.success(f"Deployed to {env}")

if __name__ == "__main__":
    deploy()
```

MIT License

## Author

Mark Lidenberg [marklidenberg@gmail.com](mailto:marklidenberg@gmail.com)
