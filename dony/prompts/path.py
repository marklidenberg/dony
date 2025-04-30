import questionary


def path(mesdony: str):
    return questionary.path(
        mesdony=mesdony,
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
