import questionary


def path(message: str):
    return questionary.path(
        message=message,
        qmark="•",
    ).ask()


def example():
    print(
        path(
            "Give me that path",
        )
    )


if __name__ == "__main__":
    example()
