import questionary


def confirm(
    message: str,
    default: bool = True,
):
    return questionary.confirm(
        message=message,
        default=default,
        qmark="",
    ).ask()


def example():
    print(confirm("Are you sure?"))


if __name__ == "__main__":
    example()
