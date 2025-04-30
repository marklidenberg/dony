# 🧙‍♂️ dony

A lightweight Python command runner providing a simple, consistent workflow for managing and executing project 
commands. dony serves as an alternative to `Justfile`, leveraging Python for flexibility and extensibility.

## Installation

Install via `pipx`:

```bash
pipx install dony
```

Ensure you have the following prerequisites:

- Python 3.8 or higher
- `pipx` for isolated installation (`brew install pipx` on macOS
- `fzf` for fuzzy command selection (`brew install fzf` on macOS)

## Getting Started

Initialize your project:

```bash
dony init
```

This creates a `dony/` directory containing:

- A `commands/` directory containing a sample command
- A virtual environment (`uv/` directory)

Run commands interactively:

```bash
dony
```

Run a command directly:

```bash
dony <command_name> [--arg1 value --arg2 value]
```

## Defining Commands

Create commands as Python functions. All parameters must have defaults to allow invocation without explicit arguments.

```python
# dony/commands/my_global_command.py

from marklidenberg.dony import dony


@dony.command(path='my/custom/path')
def greet(
        greeting: str = 'Hello',
        suffix: str = lambda: ',',
        real_greeting: str = lambda kwargs: kwargs['greeting'] + kwargs['suffix'],
        name: str = lambda: dony.input('What is your name?')
):
    dony.shell(f"echo {real_greeting}, {name}!")
```

- All arguments should have to be `str` or `List[str]` for now. I plan to add support for other types in the future
- `@dony.command(path)` registers the function under a custom path (defaults to file-relative path).
- Default values may be literals or callables:
	- Simple defaults (`'Hello'`)
	- Lazily-evaluated callables (`lambda: ...`)
	- Access to other arguments via `kwargs`
	- Interactive prompts via `dony.input`, select, confirm, etc.
- `dony.shell(...)` runs shell commands and raises on errors.

## Project Structure

```text
dony/
├── uv/                  # virtual environment
├── commands/            # command modules
│   ├── my_global_command.py # single-file command
│   ├── my-service/          # grouped commands
│   │   ├── service_task.py  # one command per file
│   │   └── _helper.py       # private module (ignored)
```

- Files and directories under `commands/` define your CLI tasks.
- Files or folders prefixed with `_` are excluded from discovery.

## Udony Examples

Run an interactive command list:

```bash
dony
```

Execute a specific command:

```bash
dony my/custom/path --greeting Hi --suffix "!"
```

Combined with arguments and environment variables:

```bash
dony build --env production
```

## Advanced Features

- Fuzzy search via `fzf` for rapid command lookup.
- Interactive prompts (`input`, `select`, `confirm`) powered by `questionary`.
- Customizable command namespaces and paths.

## License

MIT License. See [LICENSE](LICENSE) for details.

## Author

Mark Lidenberg [marklidenberg@gmail.com](mailto\:marklidenberg@gmail.com)

