def test_version() -> None:
    from teleskope import __version__

    assert __version__ is not None
