import questionary


def confirm(
    mesdony: str,
    default: bool = True,
):
    return questionary.confirm(
        mesdony=mesdony,
        default=default,
        qmark="",
    ).ask()


def example():
    print(confirm("Are you sure?"))


if __name__ == "__main__":
    example()
