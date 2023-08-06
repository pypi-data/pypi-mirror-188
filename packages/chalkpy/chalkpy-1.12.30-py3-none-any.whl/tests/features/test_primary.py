from chalk.features import Primary, feature, features, has_one, is_primary

P = Primary


@features
class PrimaryCls:
    myid: Primary[str]


@features
class ImplicitIdFeatures:
    id: str


@features
class PrimaryCls2:
    myid: Primary[str] = feature(max_staleness="3d")
    id: str


@features
class PrimaryClsWithForwardRef:
    myid: "Primary[str]" = feature()


@features
class PrimaryClsWithForwardRefRenamed:
    myid: "P[str]" = feature()


@features
class NestedFeatures:
    id: str
    sub_features_id: str
    sub_features: ImplicitIdFeatures = has_one(lambda: ImplicitIdFeatures.id == NestedFeatures.sub_features_id)


def test_primary():
    assert is_primary(ImplicitIdFeatures.id)
    assert is_primary(PrimaryCls.myid)
    assert is_primary(PrimaryCls2.myid)
    assert is_primary(PrimaryClsWithForwardRef.myid)
    assert is_primary(PrimaryClsWithForwardRefRenamed.myid)
    assert not is_primary(PrimaryCls2.id)


def test_nested_features_primary():
    assert is_primary(NestedFeatures.sub_features.id)
