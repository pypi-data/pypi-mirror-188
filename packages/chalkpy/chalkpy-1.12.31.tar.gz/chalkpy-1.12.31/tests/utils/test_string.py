from chalk.utils.string import removesuffix


def test_remove_suffix():
    assert removesuffix("joe's waffles", "waffles") == "joe's "
    assert removesuffix("joe's waffles", "bananas") == "joe's waffles"
