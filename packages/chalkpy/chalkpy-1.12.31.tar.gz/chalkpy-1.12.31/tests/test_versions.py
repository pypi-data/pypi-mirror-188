import json
from pathlib import Path

import pytest

from chalk.features import feature, features, has_one
from chalk.parsed.user_types_to_json import get_registered_types_as_json


@features
class VChild1:
    id: str
    evolving: int = feature(version=2, default_version=1)


@features
class VChild:
    id: str
    evolving: int = feature(version=2, default_version=2)


@features
class VParent:
    id: str
    child: VChild = has_one(lambda: VChild.id == VParent.id)
    child1: VChild1 = has_one(lambda: VChild1.id == VParent.id)


@features
class VGrandParent:
    id: str
    parent: VParent = has_one(lambda: VGrandParent.id == VParent.id)


def test_versioned_feature_names():
    assert str(VChild.evolving) == "v_child.evolving:v2"
    assert str(VChild.evolving_v2) == "v_child.evolving:v2"
    assert str(VChild.evolving_v1) == "v_child.evolving"
    assert str(VParent.child.evolving) == "v_parent.child.evolving:v2"
    assert str(VGrandParent.parent.child.evolving) == "v_grand_parent.parent.child.evolving:v2"


def test_applying_versions():
    assert str(VParent.child.evolving @ 2) == "v_parent.child.evolving:v2"
    assert str(VGrandParent.parent.child.evolving @ 2) == "v_grand_parent.parent.child.evolving:v2"

    assert str(VParent.child.evolving @ 1) == "v_parent.child.evolving"
    assert str(VGrandParent.parent.child.evolving @ 1) == "v_grand_parent.parent.child.evolving"


def test_applying_versions_default_1():
    assert str(VParent.child1.evolving @ 2) == "v_parent.child1.evolving:v2"
    assert str(VGrandParent.parent.child1.evolving @ 2) == "v_grand_parent.parent.child1.evolving:v2"

    assert str(VParent.child1.evolving @ 1) == "v_parent.child1.evolving"
    assert str(VGrandParent.parent.child1.evolving @ 1) == "v_grand_parent.parent.child1.evolving"


def test_unversioned():
    with pytest.raises(ValueError) as e:
        str(VParent.id @ 3)

    assert str(e.value) == (
        "Cannot request version 3 of feature 'v_parent.id', because this feature doesn't "
        "have a version set at definition. To set a version, write \n"
        "    @features\n"
        "    class VParent:\n"
        "        id: ... = feature(version=3)\n"
        "        ...\n"
    )


def test_too_many_versions():
    with pytest.raises(ValueError) as e:
        str(VParent.child.evolving @ 3)

    assert str(e.value) == (
        "Cannot request version 3 of feature 'v_parent.child.evolving', because "
        "this feature has a maximum version of 2 < 3. To add versions, write \n"
        "    @features\n"
        "    class VChild:\n"
        "   -    evolving: ... = feature(version=2)\n"
        "   +    evolving: ... = feature(version=3)\n"
        "        ...\n"
    )


def test_supplying_two_versions():
    dual_versioned = VChild(evolving_v2=2, evolving_v1=1)
    assert dual_versioned.evolving_v2 == 2
    assert dual_versioned.evolving_v1 == 1
    # The default is v2
    assert dual_versioned.evolving == 2

    dual_versioned = VChild1(evolving_v2=2, evolving_v1=1)
    assert dual_versioned.evolving_v2 == 2
    assert dual_versioned.evolving_v1 == 1
    # The default is v2
    assert dual_versioned.evolving == 1


def test_aliases_unique():
    with pytest.raises(ValueError) as e:
        VChild(evolving=2, evolving_v2=1)

    assert (
        str(e.value)
        == "The features 'evolving' and 'evolving_v2' are aliases of each other. Only one can be specified, but both were given."
    )


def test_default_constructor():
    assert VChild(evolving=2, evolving_v1=1).evolving == 2
    assert VChild1(evolving=2, evolving_v2=1).evolving == 2
    assert VChild(evolving_v2=2, evolving_v1=1).evolving == 2


def test_setters():
    existing = VChild(evolving=2)
    assert existing.evolving == 2
    existing.evolving_v2 = 5
    assert existing.evolving_v2 == 5
    assert existing.evolving == 5

    existing = VChild(evolving=2)
    existing.evolving = 5
    assert existing.evolving == 5
    assert existing.evolving_v2 == 5


def test_collision():
    with pytest.raises(ValueError) as e:

        @features
        class X:
            v: int = feature(version=2)
            v_v2: int

    assert e.value.args[0] == (
        "The class 'X' has an existing annotation 'v_v2' "
        "that collides with a versioned feature. Please remove "
        "the existing annotation, or lower the version."
    )


@features
class Funky:
    id: str
    trumpet: str = feature(version=1)
    saxophone: str = feature(version=3)


@pytest.mark.filterwarnings("ignore:`feature.typ.underlying`:DeprecationWarning")
def test_registry():
    assert [
        feature_json["id"]["fqn"]
        for feature_json in json.loads(
            get_registered_types_as_json(
                Path("/"),
                failed=[],
            )
        )["features"]
        if feature_json["id"]["namespace"] == "funky"
    ] == [
        "funky.id",
        "funky.trumpet",
        "funky.saxophone",
        "funky.saxophone:v2",
        "funky.saxophone:v3",
    ]
