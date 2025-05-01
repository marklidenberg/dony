import dony


@dony.command()
def hello_world(name: str = "John"):
    print(f"Hello, {name}!")
