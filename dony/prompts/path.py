import questionary


def path(message: str):
    result = questionary.path(
        message=message,
        qmark="•",
    ).ask()

    if result is None:
        raise KeyboardInterrupt


def example():
    print(
        path(
            "Give me that path",
        )
    )


if __name__ == "__main__":
    example()
