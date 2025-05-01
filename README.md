# 🍥️ dony

A lightweight Python command runner with simple and consistent workflow for managing project 
commands. A `Justfile` alternative.

## How it works

Define your commands in `dony/` in the root of your project.

```python
# dony/commands/hello_world.py
import dony

@dony.command()
def hello_world(name: str = "John"):
    print(f"Hello, {name}!")	
```

Run `dony` to fuzzy-search your commands from anywhere in your project.

Common use cases: build, release, publish, test, deploy, configure, format, run static analyzers, manage databases, 
generate documentation, run benchmarks, get useful links, create release notes and much more

## Defining Commands

Create commands as Python functions. All parameters MUST have defaults to allow invocation without explicit arguments. Use prompts to get inputs from the user
```python
import dony

@dony.command()
def greet(
	greeting: str = 'Hello', 
	suffix: str = lambda: ',',
	real_greeting: str = lambda kwargs: kwargs['greeting'] + kwargs['suffix'],
	name: str = lambda: dony.input('What is your name?')
):
    dony.shell(f"echo {real_greeting}, {name}!")
```

- All arguments should have to be `str` or `List[str]` for now. Support for other types may come later
- Default values may be literals or callables:
	- Simple defaults (`'Hello'`)
	- Lazily-evaluated callables (`lambda: ...` or `lambda kwargs: ...`)
	- Interactive prompts via `dony.input`, `dony.select`, `dony.confirm`, etc.
	- `dony.shell(...)` runs shell commands from the directory, where `dony/` is located

## Running commands

Run commands interactively:

```bash
dony
```

Run commands directly:

```bash
dony <command_name> [--arg1 value --arg2 value]
```

## Installation

Ensure you have the following prerequisites:
- Python 3.8 or higher
- `pipx` for isolated installation (`brew install pipx` on macOS)
- `fzf` for fuzzy command selection (`brew install fzf` on macOS)

Then install the package with `pipx`:
```bash
pipx install dony
```

Initialize your project:

```bash
dony --init
```

This creates a `dony/` directory containing:
- A `commands/` directory containing a sample command
- A `uv` virtual environment

## Dony directory structure

```text
dony/
... (uv environment) 
├── commands/
│   ├── my_global_command.py # one command per file
│   ├── my-service/         
│   │   ├── service_command.py  # will be displayed as `my-service/service_command`
│   │   └── _helper.py       # private module (ignored)
```

## License

MIT License. See [LICENSE](LICENSE) for details.

## Author

Mark Lidenberg [marklidenberg@gmail.com](mailto\:marklidenberg@gmail.com)

