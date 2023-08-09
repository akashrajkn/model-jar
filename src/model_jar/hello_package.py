from __future__ import annotations


def hello_package(i: int = 0) -> str:
    """Doc String."""
    print("hello package")
    return f"string-{i}"
