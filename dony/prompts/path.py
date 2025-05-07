import questionary


def path(
    message: str,
    provided_answer: str = None,
):
    if provided_answer is not None:
        return provided_answer

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
