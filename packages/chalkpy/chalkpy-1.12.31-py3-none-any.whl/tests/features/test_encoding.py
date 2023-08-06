import base64
import enum
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal
from typing import Any, Dict, FrozenSet, List, NamedTuple, Optional, Set, Tuple, TypedDict, cast

import attrs
import pyarrow as pa
import pytest
from pydantic import BaseModel

from chalk.features import DataFrame, feature, features, unwrap_feature
from chalk.features._encoding.serialized_dtype import (
    BaseSerializedDType,
    BinaryDType,
    DTypeCode,
    ListDType,
    SingletonDType,
    StructDType,
    StructField,
    TimestampDType,
    TimeUnitCode,
    TimeUnitDType,
)

try:
    import polars as pl
except ImportError:
    pytest.skip(reason="Polars not installed", allow_module_level=True)


class StrEnumFeature(enum.Enum):
    BLUE = "blue"
    GREEN = "green"
    ORANGE = "orange"


class IntEnumFeature(enum.IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3


PL_STRUCT_SCHEMA = pl.Struct(
    [
        pl.Field("foo", pl.Int64),
        pl.Field("bar", pl.Utf8),
        pl.Field("baz", pl.Int64),
        pl.Field("sub_list", pl.List(pl.Int64)),
    ]
)

PA_STRUCT_SCHEMA = pa.struct(
    [
        pa.field("foo", pa.int64()),
        pa.field("bar", pa.utf8()),
        pa.field("baz", pa.int64()),
        pa.field("sub_list", pa.list_(pa.int64())),
    ]
)

SERIALIZED_STRUCT_DTYPE = StructDType(
    type_code=DTypeCode.STRUCT,
    fields=[
        StructField(name="foo", dtype=SingletonDType(type_code=DTypeCode.INT64)),
        StructField(name="bar", dtype=SingletonDType(type_code=DTypeCode.STRING)),
        StructField(name="baz", dtype=SingletonDType(type_code=DTypeCode.INT64)),
        StructField(
            name="sub_list",
            dtype=ListDType(type_code=DTypeCode.LIST, inner_dtype=SingletonDType(type_code=DTypeCode.INT64), length=-1),
        ),
    ],
)


class CustomClass:
    def __init__(self, foo: int, bar: str, baz: Optional[int], sub_list: List[int]):
        self.foo = foo
        self.bar = bar
        self.baz = baz
        self.sub_list = sub_list

    def __eq__(self, other: object):
        if not isinstance(other, CustomClass):
            return NotImplemented
        return (
            self.foo == other.foo
            and self.bar == other.bar
            and self.baz == other.baz
            and self.sub_list == other.sub_list
        )

    @classmethod
    def encoder(cls, instance: "CustomClass"):
        return instance.__dict__

    @classmethod
    def decoder(cls, x: Dict[str, Any]) -> "CustomClass":
        return CustomClass(**x)


@dataclass
class MyDataclass:
    foo: int
    bar: str
    baz: Optional[int]
    sub_list: List[int]


class MyNamedTuple(NamedTuple):
    foo: int
    bar: str
    baz: Optional[int]
    sub_list: List[int]


class MyTypedDict(TypedDict):
    foo: int
    bar: str
    baz: Optional[int]
    sub_list: List[int]


class PydanticFeature(BaseModel):
    foo: int
    bar: str
    baz: Optional[int]
    sub_list: List[int]


@attrs.define
class AttrsFeature:
    foo: int
    bar: str
    baz: Optional[int]
    sub_list: List[int]


class TypedDictFeature(TypedDict):
    foo: int
    bar: str
    baz: Optional[int]
    sub_list: List[int]


class SubStruct(TypedDict):
    name: str


class StructOfOptionalStructFeature(TypedDict):
    sub: Optional[SubStruct]


@features
class CodecFs:
    str_feature: str
    bool_feature: bool
    int_feature: int
    unsigned_int_feature: int = feature(dtype=pa.uint64())
    float_feature: float
    datetime_feature: datetime
    datetime_without_timezone_feature: datetime = feature(dtype=pa.timestamp("us"))
    time_feature: time
    date_feature: date
    duration_feature: timedelta
    binary_feature: bytes
    decimal_feature: Decimal
    str_enum_feature: StrEnumFeature
    int_enum_feature: IntEnumFeature
    dataclass_feature: MyDataclass
    named_tuple_feature: MyNamedTuple
    pydantic_feature: PydanticFeature
    attrs_feature: AttrsFeature
    typed_dict_feature: MyTypedDict
    custom_feature: CustomClass = feature(
        encoder=CustomClass.encoder,
        decoder=CustomClass.decoder,
        dtype=PA_STRUCT_SCHEMA,
    )
    list_feature: List[int]
    set_feature: Set[int]
    set_str_feature: Set[str]
    frozenset_feature: FrozenSet[str]
    homogenous_tuple_feature: Tuple[int, ...]
    list_of_struct_feature: List[MyNamedTuple]
    nested_struct: StructOfOptionalStructFeature


MISSING = object()


@dataclass
class Parameterization:
    wrapped_feature: Any
    expected_pa_dtype: pa.DataType
    expected_pl_dtype: pa.DataType
    expected_serialized_dtype: BaseSerializedDType

    rich: Any
    prim: Any
    json: Any

    canonical_rich: Any = MISSING

    should_error: bool = False

    @property
    def feature(self):
        return unwrap_feature(self.wrapped_feature)

    @property
    def pa(self):
        return pa.array([self.prim], self.expected_pa_dtype)

    def __post_init__(self):
        if self.canonical_rich is MISSING:
            self.canonical_rich = self.rich


@pytest.mark.parametrize(
    "p",
    [
        pytest.param(
            Parameterization(
                CodecFs.str_feature,
                pa.utf8(),
                pl.Utf8(),
                rich=None,
                prim=None,
                json=None,
                expected_serialized_dtype=SingletonDType(type_code=DTypeCode.STRING),
            ),
            id="str_null",
        ),
        pytest.param(
            Parameterization(
                CodecFs.str_feature,
                pa.utf8(),
                pl.Utf8(),
                rich="hi",
                prim="hi",
                json="hi",
                expected_serialized_dtype=SingletonDType(type_code=DTypeCode.STRING),
            ),
            id="str",
        ),
        pytest.param(
            Parameterization(
                CodecFs.bool_feature,
                pa.bool_(),
                pl.Boolean(),
                rich=True,
                prim=True,
                json=True,
                expected_serialized_dtype=SingletonDType(type_code=DTypeCode.BOOL),
            ),
            id="bool",
        ),
        pytest.param(
            Parameterization(
                CodecFs.bool_feature,
                pa.bool_(),
                pl.Boolean(),
                rich="t",
                canonical_rich=True,
                prim=True,
                json=True,
                expected_serialized_dtype=SingletonDType(type_code=DTypeCode.BOOL),
            ),
            id="bool_str",
        ),
        pytest.param(
            Parameterization(
                CodecFs.bool_feature,
                pa.bool_(),
                pl.Boolean(),
                rich=0,
                canonical_rich=False,
                prim=False,
                json=False,
                expected_serialized_dtype=SingletonDType(type_code=DTypeCode.BOOL),
            ),
            id="bool_int",
        ),
        pytest.param(
            Parameterization(
                CodecFs.int_feature,
                pa.int64(),
                pl.Int64(),
                rich=2,
                canonical_rich=2,
                prim=2,
                json=2,
                expected_serialized_dtype=SingletonDType(type_code=DTypeCode.INT64),
            ),
            id="int",
        ),
        pytest.param(
            Parameterization(
                CodecFs.int_feature,
                pa.int64(),
                pl.Int64(),
                rich=2.0,
                canonical_rich=2,
                prim=2,
                json=2,
                expected_serialized_dtype=SingletonDType(type_code=DTypeCode.INT64),
            ),
            id="float_as_int",
        ),
        pytest.param(
            Parameterization(
                CodecFs.unsigned_int_feature,
                pa.uint64(),
                pl.UInt64(),
                rich=2**64 - 1,
                prim=2**64 - 1,
                json=2**64 - 1,
                expected_serialized_dtype=SingletonDType(type_code=DTypeCode.UINT64),
            ),
            id="unsigned_int",
        ),
        pytest.param(
            Parameterization(
                CodecFs.float_feature,
                pa.float64(),
                pl.Float64(),
                rich=3.14,
                prim=3.14,
                json=3.14,
                expected_serialized_dtype=SingletonDType(type_code=DTypeCode.FLOAT64),
            ),
            id="float",
        ),
        pytest.param(
            Parameterization(
                CodecFs.float_feature,
                pa.float64(),
                pl.Float64(),
                canonical_rich=3.0,
                rich=3,
                prim=3.0,
                json=3.0,
                expected_serialized_dtype=SingletonDType(type_code=DTypeCode.FLOAT64),
            ),
            id="int_as_float",
        ),
        pytest.param(
            Parameterization(
                CodecFs.datetime_feature,
                pa.timestamp("us", "UTC"),
                pl.Datetime("us", "UTC"),
                rich=datetime(2000, 1, 1, 3, 45, 56, 789, timezone.utc),
                prim=datetime(2000, 1, 1, 3, 45, 56, 789, timezone.utc),
                json="2000-01-01T03:45:56.000789+00:00",
                expected_serialized_dtype=TimestampDType(
                    type_code=DTypeCode.TIMESTAMP,
                    time_unit=TimeUnitCode.MICROSECONDS,
                    timezone="UTC",
                ),
            ),
            id="datetime",
        ),
        pytest.param(
            Parameterization(
                CodecFs.datetime_feature,
                pa.timestamp("us", "UTC"),
                pl.Datetime("us", "UTC"),
                rich="2000-01-01T03:45:56.000789Z",
                canonical_rich=datetime(2000, 1, 1, 3, 45, 56, 789, timezone.utc),
                prim=datetime(2000, 1, 1, 3, 45, 56, 789, timezone.utc),
                json="2000-01-01T03:45:56.000789+00:00",
                expected_serialized_dtype=TimestampDType(
                    type_code=DTypeCode.TIMESTAMP,
                    time_unit=TimeUnitCode.MICROSECONDS,
                    timezone="UTC",
                ),
            ),
            id="str_as_datetime",
        ),
        pytest.param(
            Parameterization(
                CodecFs.datetime_without_timezone_feature,
                pa.timestamp("us"),
                pl.Datetime("us"),
                rich=datetime(2000, 1, 1, 3, 45, 56, 789),
                prim=datetime(2000, 1, 1, 3, 45, 56, 789),
                json="2000-01-01T03:45:56.000789",
                expected_serialized_dtype=TimestampDType(
                    type_code=DTypeCode.TIMESTAMP,
                    time_unit=TimeUnitCode.MICROSECONDS,
                    timezone=None,
                ),
            ),
            id="datetime_wo_timezone",
        ),
        pytest.param(
            Parameterization(
                CodecFs.datetime_without_timezone_feature,
                pa.timestamp("us"),
                pl.Datetime("us"),
                rich="2000-01-01T03:45:56.000789",
                canonical_rich=datetime(2000, 1, 1, 3, 45, 56, 789),
                prim=datetime(2000, 1, 1, 3, 45, 56, 789),
                json="2000-01-01T03:45:56.000789",
                expected_serialized_dtype=TimestampDType(
                    type_code=DTypeCode.TIMESTAMP,
                    time_unit=TimeUnitCode.MICROSECONDS,
                    timezone=None,
                ),
            ),
            id="str_datetime_wo_timezone",
        ),
        pytest.param(
            Parameterization(
                CodecFs.datetime_without_timezone_feature,
                pa.timestamp("us", None),
                pl.Datetime("us", None),
                rich="2023-01-25 17:31:40.074654",
                canonical_rich=datetime(2023, 1, 25, 17, 31, 40, 74654),
                prim=datetime(2023, 1, 25, 17, 31, 40, 74654),
                json="2023-01-25T17:31:40.074654",
                expected_serialized_dtype=TimestampDType(
                    type_code=DTypeCode.TIMESTAMP,
                    time_unit=TimeUnitCode.MICROSECONDS,
                    timezone=None,
                ),
            ),
            id="non_iso_str_as_datetime",
        ),
        pytest.param(
            Parameterization(
                CodecFs.datetime_without_timezone_feature,
                pa.timestamp("us", None),
                pl.Datetime("us", None),
                rich="2023-01-25",
                canonical_rich=datetime(2023, 1, 25),
                prim=datetime(2023, 1, 25),
                json="2023-01-25T00:00:00",
                expected_serialized_dtype=TimestampDType(
                    type_code=DTypeCode.TIMESTAMP,
                    time_unit=TimeUnitCode.MICROSECONDS,
                    timezone=None,
                ),
            ),
            id="date_str_as_datetime",
        ),
        pytest.param(
            Parameterization(
                CodecFs.time_feature,
                pa.time64("us"),
                pl.Time(),
                rich=time(3, 45, 56, 789),
                canonical_rich=time(3, 45, 56, 789),
                prim=time(3, 45, 56, 789),
                json="03:45:56.000789",
                expected_serialized_dtype=TimeUnitDType(
                    type_code=DTypeCode.TIME64,
                    time_unit=TimeUnitCode.MICROSECONDS,
                ),
            ),
            id="time",
        ),
        pytest.param(
            Parameterization(
                CodecFs.time_feature,
                pa.time64("us"),
                pl.Time(),
                rich=time(3, 45, 56, 789),
                canonical_rich=time(3, 45, 56, 789),
                prim=time(3, 45, 56, 789),
                json="03:45:56.000789",
                expected_serialized_dtype=TimeUnitDType(
                    type_code=DTypeCode.TIME64,
                    time_unit=TimeUnitCode.MICROSECONDS,
                ),
            ),
            id="str_time",
        ),
        pytest.param(
            Parameterization(
                CodecFs.date_feature,
                pa.date64(),
                # Polars parses dates as ms datetimes
                pl.Datetime("ms", None),
                rich=date(2000, 1, 1),
                prim=date(2000, 1, 1),
                json="2000-01-01",
                expected_serialized_dtype=SingletonDType(
                    type_code=DTypeCode.DATE64,
                ),
            ),
            id="datetime_date",
        ),
        pytest.param(
            Parameterization(
                CodecFs.date_feature,
                pa.date64(),
                # Polars parses dates as ms datetimes
                pl.Datetime("ms", None),
                rich="2000-01-01",
                canonical_rich=date(2000, 1, 1),
                prim=date(2000, 1, 1),
                json="2000-01-01",
                expected_serialized_dtype=SingletonDType(
                    type_code=DTypeCode.DATE64,
                ),
            ),
            id="str_date",
        ),
        pytest.param(
            Parameterization(
                CodecFs.date_feature,
                pa.date64(),
                # Polars parses dates as ms datetimes
                pl.Datetime("ms", None),
                rich=datetime(2000, 1, 1),
                canonical_rich=date(2000, 1, 1),
                prim=date(2000, 1, 1),
                json="2000-01-01",
                expected_serialized_dtype=SingletonDType(
                    type_code=DTypeCode.DATE64,
                ),
            ),
            id="date",
        ),
        pytest.param(
            Parameterization(
                CodecFs.duration_feature,
                pa.duration("us"),
                pl.Duration(),
                rich=timedelta(minutes=5),
                prim=timedelta(minutes=5),
                json="PT5M",
                expected_serialized_dtype=TimeUnitDType(
                    type_code=DTypeCode.DURATION,
                    time_unit=TimeUnitCode.MICROSECONDS,
                ),
            ),
            id="timedelta",
        ),
        pytest.param(
            Parameterization(
                CodecFs.duration_feature,
                pa.duration("us"),
                pl.Duration(),
                rich="P0Y0MT5M0S",
                canonical_rich=timedelta(minutes=5),
                prim=timedelta(minutes=5),
                json="PT5M",
                expected_serialized_dtype=TimeUnitDType(
                    type_code=DTypeCode.DURATION,
                    time_unit=TimeUnitCode.MICROSECONDS,
                ),
            ),
            id="timedelta_iso",
        ),
        pytest.param(
            Parameterization(
                CodecFs.binary_feature,
                pa.binary(),
                pl.Binary(),
                rich=b"Hello",
                prim=b"Hello",
                json=base64.b64encode(b"Hello").decode("utf8"),
                expected_serialized_dtype=BinaryDType(
                    type_code=DTypeCode.BINARY,
                    length=-1,
                ),
            ),
            id="binary",
        ),
        pytest.param(
            Parameterization(
                # We encode decimals as strings, as polars does not support
                # pyarrow decimal
                CodecFs.decimal_feature,
                pa.utf8(),
                pl.Utf8(),
                rich=Decimal("0.33"),
                prim="0.33",
                json="0.33",
                expected_serialized_dtype=SingletonDType(
                    type_code=DTypeCode.STRING,
                ),
            ),
            id="decimal",
        ),
        pytest.param(
            Parameterization(
                CodecFs.decimal_feature,
                pa.utf8(),
                pl.Utf8(),
                rich=Decimal("2.0000"),
                canonical_rich=Decimal("2"),
                prim="2",
                json="2",
                expected_serialized_dtype=SingletonDType(
                    type_code=DTypeCode.STRING,
                ),
            ),
            id="decimal_no_sig_figs",
        ),
        pytest.param(
            Parameterization(
                CodecFs.decimal_feature,
                pa.utf8(),
                pl.Utf8(),
                rich=2,
                canonical_rich=Decimal("2"),
                prim="2",
                json="2",
                expected_serialized_dtype=SingletonDType(
                    type_code=DTypeCode.STRING,
                ),
            ),
            id="decimal_int",
        ),
        pytest.param(
            Parameterization(
                CodecFs.decimal_feature,
                pa.utf8(),
                pl.Utf8(),
                rich=2.0,
                canonical_rich=Decimal("2"),
                prim="2",
                json="2",
                expected_serialized_dtype=SingletonDType(
                    type_code=DTypeCode.STRING,
                ),
            ),
            id="decimal_float",
        ),
        pytest.param(
            Parameterization(
                CodecFs.decimal_feature,
                pa.utf8(),
                pl.Utf8(),
                rich="2.0",
                canonical_rich=Decimal("2"),
                prim="2",
                json="2",
                expected_serialized_dtype=SingletonDType(
                    type_code=DTypeCode.STRING,
                ),
            ),
            id="decimal_str",
        ),
        pytest.param(
            Parameterization(
                CodecFs.str_enum_feature,
                pa.utf8(),
                pl.Utf8(),
                rich=StrEnumFeature.BLUE,
                prim="blue",
                json="blue",
                expected_serialized_dtype=SingletonDType(
                    type_code=DTypeCode.STRING,
                ),
            ),
            id="str_enum",
        ),
        pytest.param(
            Parameterization(
                CodecFs.str_enum_feature,
                pa.utf8(),
                pl.Utf8(),
                rich="blue",
                canonical_rich=StrEnumFeature.BLUE,
                prim="blue",
                json="blue",
                expected_serialized_dtype=SingletonDType(
                    type_code=DTypeCode.STRING,
                ),
            ),
            id="str_enum_val",
        ),
        pytest.param(
            Parameterization(
                CodecFs.str_enum_feature,
                pa.utf8(),
                pl.Utf8(),
                rich="BLUE",
                canonical_rich=StrEnumFeature.BLUE,
                prim="blue",
                json="blue",
                expected_serialized_dtype=SingletonDType(
                    type_code=DTypeCode.STRING,
                ),
            ),
            id="str_enum_key",
        ),
        pytest.param(
            Parameterization(
                CodecFs.int_enum_feature,
                pa.int64(),
                pl.Int64(),
                rich=IntEnumFeature.ONE,
                prim=1,
                json=1,
                expected_serialized_dtype=SingletonDType(
                    type_code=DTypeCode.INT64,
                ),
            ),
            id="int_enum",
        ),
        pytest.param(
            Parameterization(
                CodecFs.int_enum_feature,
                pa.int64(),
                pl.Int64(),
                rich=1,
                canonical_rich=IntEnumFeature.ONE,
                prim=1,
                json=1,
                expected_serialized_dtype=SingletonDType(
                    type_code=DTypeCode.INT64,
                ),
            ),
            id="int_enum_val",
        ),
        pytest.param(
            Parameterization(
                CodecFs.int_enum_feature,
                pa.int64(),
                pl.Int64(),
                rich="ONE",
                canonical_rich=IntEnumFeature.ONE,
                prim=1,
                json=1,
                expected_serialized_dtype=SingletonDType(
                    type_code=DTypeCode.INT64,
                ),
            ),
            id="int_enum_key",
        ),
        pytest.param(
            Parameterization(
                CodecFs.dataclass_feature,
                PA_STRUCT_SCHEMA,
                PL_STRUCT_SCHEMA,
                rich=None,
                canonical_rich=MyDataclass(
                    foo=cast(int, None), bar=cast(str, None), baz=None, sub_list=cast(list, None)
                ),
                prim={"foo": None, "bar": None, "baz": None, "sub_list": None},
                json=[None, None, None, None],
                expected_serialized_dtype=SERIALIZED_STRUCT_DTYPE,
            ),
            id="null_struct",
        ),
        pytest.param(
            Parameterization(
                CodecFs.dataclass_feature,
                PA_STRUCT_SCHEMA,
                PL_STRUCT_SCHEMA,
                rich=(None, None, None, None),
                canonical_rich=MyDataclass(
                    foo=cast(int, None), bar=cast(str, None), baz=None, sub_list=cast(list, None)
                ),
                prim={"foo": None, "bar": None, "baz": None, "sub_list": None},
                json=[None, None, None, None],
                expected_serialized_dtype=SERIALIZED_STRUCT_DTYPE,
            ),
            id="dataclass_struct_null_tuple",
        ),
        pytest.param(
            Parameterization(
                CodecFs.dataclass_feature,
                PA_STRUCT_SCHEMA,
                PL_STRUCT_SCHEMA,
                rich=MyDataclass(foo=cast(int, None), bar=cast(str, None), baz=None, sub_list=cast(list, None)),
                prim={"foo": None, "bar": None, "baz": None, "sub_list": None},
                json=[None, None, None, None],
                expected_serialized_dtype=SERIALIZED_STRUCT_DTYPE,
            ),
            id="dataclass_struct_null",
        ),
        pytest.param(
            Parameterization(
                CodecFs.dataclass_feature,
                PA_STRUCT_SCHEMA,
                PL_STRUCT_SCHEMA,
                rich=MyDataclass(50, "hi", None, [100]),
                prim={"foo": 50, "bar": "hi", "baz": None, "sub_list": [100]},
                json=[50, "hi", None, [100]],
                expected_serialized_dtype=SERIALIZED_STRUCT_DTYPE,
            ),
            id="dataclass_struct",
        ),
        pytest.param(
            Parameterization(
                CodecFs.named_tuple_feature,
                PA_STRUCT_SCHEMA,
                PL_STRUCT_SCHEMA,
                rich=MyNamedTuple(50, "hi", None, [100]),
                prim={"foo": 50, "bar": "hi", "baz": None, "sub_list": [100]},
                json=[50, "hi", None, [100]],
                expected_serialized_dtype=SERIALIZED_STRUCT_DTYPE,
            ),
            id="namedtuple_struct",
        ),
        pytest.param(
            Parameterization(
                CodecFs.named_tuple_feature,
                PA_STRUCT_SCHEMA,
                PL_STRUCT_SCHEMA,
                rich=MyNamedTuple(foo=cast(int, None), bar=cast(str, None), baz=None, sub_list=cast(list, None)),
                prim={"foo": None, "bar": None, "baz": None, "sub_list": None},
                json=[None, None, None, None],
                expected_serialized_dtype=SERIALIZED_STRUCT_DTYPE,
            ),
            id="namedtuple_struct_nulls",
        ),
        pytest.param(
            Parameterization(
                CodecFs.pydantic_feature,
                PA_STRUCT_SCHEMA,
                PL_STRUCT_SCHEMA,
                rich=PydanticFeature(foo=50, bar="hi", baz=None, sub_list=[100]),
                prim={"foo": 50, "bar": "hi", "baz": None, "sub_list": [100]},
                json=[50, "hi", None, [100]],
                expected_serialized_dtype=SERIALIZED_STRUCT_DTYPE,
            ),
            id="pydantic_struct",
        ),
        pytest.param(
            Parameterization(
                CodecFs.pydantic_feature,
                PA_STRUCT_SCHEMA,
                PL_STRUCT_SCHEMA,
                rich=PydanticFeature.construct(foo=None, bar=None, baz=None, sub_list=None),
                prim={"foo": None, "bar": None, "baz": None, "sub_list": None},
                json=[None, None, None, None],
                expected_serialized_dtype=SERIALIZED_STRUCT_DTYPE,
            ),
            id="pydantic_struct_nulls",
        ),
        pytest.param(
            Parameterization(
                CodecFs.typed_dict_feature,
                PA_STRUCT_SCHEMA,
                PL_STRUCT_SCHEMA,
                rich={"foo": 50, "bar": "hi", "baz": None, "sub_list": [100]},
                prim={"foo": 50, "bar": "hi", "baz": None, "sub_list": [100]},
                json=[50, "hi", None, [100]],
                expected_serialized_dtype=SERIALIZED_STRUCT_DTYPE,
            ),
            id="typed_dict_struct",
        ),
        pytest.param(
            Parameterization(
                CodecFs.typed_dict_feature,
                PA_STRUCT_SCHEMA,
                PL_STRUCT_SCHEMA,
                rich={"foo": None, "bar": None, "baz": None, "sub_list": None},
                prim={"foo": None, "bar": None, "baz": None, "sub_list": None},
                json=[None, None, None, None],
                expected_serialized_dtype=SERIALIZED_STRUCT_DTYPE,
            ),
            id="typed_dict_struct_nulls",
        ),
        pytest.param(
            Parameterization(
                CodecFs.attrs_feature,
                PA_STRUCT_SCHEMA,
                PL_STRUCT_SCHEMA,
                rich=AttrsFeature(foo=50, bar="hi", baz=None, sub_list=[100]),
                prim={"foo": 50, "bar": "hi", "baz": None, "sub_list": [100]},
                json=[50, "hi", None, [100]],
                expected_serialized_dtype=SERIALIZED_STRUCT_DTYPE,
            ),
            id="attrs_struct",
        ),
        pytest.param(
            Parameterization(
                CodecFs.attrs_feature,
                PA_STRUCT_SCHEMA,
                PL_STRUCT_SCHEMA,
                rich=AttrsFeature(foo=cast(int, None), bar=cast(str, None), baz=None, sub_list=cast(list, None)),
                prim={"foo": None, "bar": None, "baz": None, "sub_list": None},
                json=[None, None, None, None],
                expected_serialized_dtype=SERIALIZED_STRUCT_DTYPE,
            ),
            id="attrs_struct_nulls",
        ),
        pytest.param(
            Parameterization(
                CodecFs.list_feature,
                pa.list_(pa.int64()),
                pl.List(pl.Int64()),
                rich=None,
                prim=None,
                json=None,
                expected_serialized_dtype=ListDType(
                    type_code=DTypeCode.LIST,
                    inner_dtype=SingletonDType(type_code=DTypeCode.INT64),
                    length=-1,
                ),
            ),
            id="null_list",
        ),
        pytest.param(
            Parameterization(
                CodecFs.list_feature,
                pa.list_(pa.int64()),
                pl.List(pl.Int64()),
                rich=[None],
                prim=[None],
                json=[None],
                expected_serialized_dtype=ListDType(
                    type_code=DTypeCode.LIST,
                    inner_dtype=SingletonDType(type_code=DTypeCode.INT64),
                    length=-1,
                ),
            ),
            id="list_of_null",
        ),
        pytest.param(
            Parameterization(
                CodecFs.list_feature,
                pa.list_(pa.int64()),
                pl.List(pl.Int64()),
                rich=[2, 3],
                prim=[2, 3],
                json=[2, 3],
                expected_serialized_dtype=ListDType(
                    type_code=DTypeCode.LIST,
                    inner_dtype=SingletonDType(type_code=DTypeCode.INT64),
                    length=-1,
                ),
            ),
            id="real_list",
        ),
        pytest.param(
            Parameterization(
                CodecFs.set_feature,
                pa.list_(pa.int64()),
                pl.List(pl.Int64()),
                rich=set((2, 3)),
                prim=[2, 3],
                json=[2, 3],
                expected_serialized_dtype=ListDType(
                    type_code=DTypeCode.LIST,
                    inner_dtype=SingletonDType(type_code=DTypeCode.INT64),
                    length=-1,
                ),
            ),
            id="set",
        ),
        pytest.param(
            Parameterization(
                CodecFs.set_feature,
                pa.list_(pa.int64()),
                pl.List(pl.Int64()),
                # even though the insertion order is (3, 2), it should be serialized in the same order
                # as the above test, which is (2, 3)
                rich=set((3, 2)),
                prim=[2, 3],
                json=[2, 3],
                expected_serialized_dtype=ListDType(
                    type_code=DTypeCode.LIST,
                    inner_dtype=SingletonDType(type_code=DTypeCode.INT64),
                    length=-1,
                ),
            ),
            id="set_ordering",
        ),
        pytest.param(
            Parameterization(
                CodecFs.set_str_feature,
                pa.list_(pa.utf8()),
                pl.List(pl.Utf8()),
                rich=set(("c", "a", "b")),
                prim=["a", "b", "c"],
                json=["a", "b", "c"],
                expected_serialized_dtype=ListDType(
                    type_code=DTypeCode.LIST,
                    inner_dtype=SingletonDType(type_code=DTypeCode.STRING),
                    length=-1,
                ),
            ),
            id="set_ordering_str",
        ),
        pytest.param(
            Parameterization(
                CodecFs.frozenset_feature,
                pa.list_(pa.utf8()),
                pl.List(pl.Utf8()),
                rich=frozenset(("c", "a", "b")),
                prim=["a", "b", "c"],
                json=["a", "b", "c"],
                expected_serialized_dtype=ListDType(
                    type_code=DTypeCode.LIST,
                    inner_dtype=SingletonDType(type_code=DTypeCode.STRING),
                    length=-1,
                ),
            ),
            id="frozenset_feature",
        ),
        pytest.param(
            Parameterization(
                CodecFs.homogenous_tuple_feature,
                pa.list_(pa.int64()),
                pl.List(pl.Int64()),
                rich=(2, 3),
                prim=[2, 3],
                expected_serialized_dtype=ListDType(
                    type_code=DTypeCode.LIST,
                    inner_dtype=SingletonDType(type_code=DTypeCode.INT64),
                    length=-1,
                ),
                json=[2, 3],
            ),
            id="homogenous_tuple_feature",
        ),
        pytest.param(
            Parameterization(
                CodecFs.custom_feature,
                PA_STRUCT_SCHEMA,
                PL_STRUCT_SCHEMA,
                rich=CustomClass(foo=50, bar="hi", baz=None, sub_list=[100]),
                prim={"foo": 50, "bar": "hi", "baz": None, "sub_list": [100]},
                json=[50, "hi", None, [100]],
                expected_serialized_dtype=SERIALIZED_STRUCT_DTYPE,
            ),
            id="custom",
        ),
        pytest.param(
            Parameterization(
                CodecFs.custom_feature,
                PA_STRUCT_SCHEMA,
                PL_STRUCT_SCHEMA,
                rich=CustomClass(foo=cast(int, None), bar=cast(str, None), baz=None, sub_list=cast(list, None)),
                prim={"foo": None, "bar": None, "baz": None, "sub_list": None},
                json=[None, None, None, None],
                expected_serialized_dtype=SERIALIZED_STRUCT_DTYPE,
            ),
            id="custom_nulls",
        ),
        pytest.param(
            Parameterization(
                CodecFs.custom_feature,
                PA_STRUCT_SCHEMA,
                PL_STRUCT_SCHEMA,
                rich=None,
                canonical_rich=CustomClass(
                    foo=cast(int, None), bar=cast(str, None), baz=None, sub_list=cast(list, None)
                ),
                prim={"foo": None, "bar": None, "baz": None, "sub_list": None},
                json=[None, None, None, None],
                expected_serialized_dtype=SERIALIZED_STRUCT_DTYPE,
            ),
            id="null_custom",
        ),
        pytest.param(
            Parameterization(
                CodecFs.list_of_struct_feature,
                pa.list_(PA_STRUCT_SCHEMA),
                pl.List(PL_STRUCT_SCHEMA),
                rich=None,
                prim=None,
                json=None,
                expected_serialized_dtype=ListDType(
                    type_code=DTypeCode.LIST,
                    inner_dtype=SERIALIZED_STRUCT_DTYPE,
                    length=-1,
                ),
            ),
            id="null_list_of_struct",
        ),
        pytest.param(
            Parameterization(
                CodecFs.list_of_struct_feature,
                pa.list_(PA_STRUCT_SCHEMA),
                pl.List(PL_STRUCT_SCHEMA),
                rich=[],
                prim=[],
                json=[],
                expected_serialized_dtype=ListDType(
                    type_code=DTypeCode.LIST,
                    inner_dtype=SERIALIZED_STRUCT_DTYPE,
                    length=-1,
                ),
            ),
            id="list_of_struct_empty",
        ),
        pytest.param(
            Parameterization(
                CodecFs.list_of_struct_feature,
                pa.list_(PA_STRUCT_SCHEMA),
                pl.List(PL_STRUCT_SCHEMA),
                rich=[MyNamedTuple(foo=cast(int, None), bar=cast(str, None), baz=None, sub_list=cast(list, None))],
                prim=[{"foo": None, "bar": None, "baz": None, "sub_list": None}],
                json=[[None, None, None, None]],
                expected_serialized_dtype=ListDType(
                    type_code=DTypeCode.LIST,
                    inner_dtype=SERIALIZED_STRUCT_DTYPE,
                    length=-1,
                ),
            ),
            id="list_of_null_struct",
        ),
        pytest.param(
            Parameterization(
                CodecFs.list_of_struct_feature,
                pa.list_(PA_STRUCT_SCHEMA),
                pl.List(PL_STRUCT_SCHEMA),
                rich=[MyNamedTuple(50, "hi", None, [100])],
                prim=[{"foo": 50, "bar": "hi", "baz": None, "sub_list": [100]}],
                json=[[50, "hi", None, [100]]],
                expected_serialized_dtype=ListDType(
                    type_code=DTypeCode.LIST,
                    inner_dtype=SERIALIZED_STRUCT_DTYPE,
                    length=-1,
                ),
            ),
            id="list_of_struct",
        ),
        pytest.param(
            Parameterization(
                CodecFs.nested_struct,
                pa.struct([pa.field("sub", pa.struct([pa.field("name", pa.utf8())]))]),
                pl.Struct([pl.Field("sub", pl.Struct([pl.Field("name", pl.Utf8())]))]),
                rich={"sub": None},
                canonical_rich={"sub": {"name": None}},
                prim={"sub": {"name": None}},
                json=[[None]],
                expected_serialized_dtype=StructDType(
                    type_code=DTypeCode.STRUCT,
                    fields=[
                        StructField(
                            name="sub",
                            dtype=StructDType(
                                type_code=DTypeCode.STRUCT,
                                fields=[
                                    StructField(
                                        name="name",
                                        dtype=SingletonDType(type_code=DTypeCode.STRING),
                                    ),
                                ],
                            ),
                        )
                    ],
                ),
            ),
            id="sub_struct",
        ),
    ],
)
class TestEncoder:
    def test_infer_pa_dtype(self, p: Parameterization):
        assert p.feature.converter.pyarrow_dtype == p.expected_pa_dtype

    def test_infer_pl_dtype(self, p: Parameterization):
        assert p.feature.converter.polars_dtype == p.expected_pl_dtype

    def test_rich_to_pyarrow(self, p: Parameterization):
        assert p.feature.converter.from_rich_to_pyarrow([p.rich]) == p.pa

    def test_rich_to_prim(self, p: Parameterization):
        assert p.feature.converter.from_rich_to_primitive(p.rich) == p.prim

    def test_rich_to_json(self, p: Parameterization):
        assert p.feature.converter.from_rich_to_json(p.rich) == p.json

    def test_prim_to_pyarrow(self, p: Parameterization):
        assert p.feature.converter.from_primitive_to_pyarrow([p.prim]) == p.pa

    def test_prim_to_rich(self, p: Parameterization):
        converted = p.feature.converter.from_primitive_to_rich(p.prim)
        assert isinstance(converted, type(p.canonical_rich))
        assert converted == p.canonical_rich

    def test_prim_to_json(self, p: Parameterization):
        assert p.feature.converter.from_primitive_to_json(p.prim) == p.json

    def test_pyarrow_to_rich(self, p: Parameterization):
        converted = p.feature.converter.from_pyarrow_to_rich(p.pa)
        assert len(converted) == 1
        x = converted[0]
        assert isinstance(x, type(p.canonical_rich))
        assert x == p.canonical_rich

    def test_pyarrow_to_prim(self, p: Parameterization):
        assert p.feature.converter.from_pyarrow_to_primitive(p.pa) == [p.prim]

    def test_pyarrow_to_json(self, p: Parameterization):
        assert p.feature.converter.from_pyarrow_to_json(p.pa) == [p.json]

    def test_json_to_pyarrow(self, p: Parameterization):
        assert p.feature.converter.from_json_to_pyarrow([p.json]) == p.pa

    def test_json_to_prim(self, p: Parameterization):
        assert p.feature.converter.from_json_to_primitive(p.json) == p.prim

    def test_json_to_rich(self, p: Parameterization):
        converted = p.feature.converter.from_json_to_rich(p.json)
        assert isinstance(converted, type(p.canonical_rich))
        assert converted == p.canonical_rich

    def test_rich_to_dataframe(self, p: Parameterization):
        df = DataFrame(
            {
                p.feature: [p.rich],
            }
        )
        self._validate_df(df, p)

    def _validate_df(self, df: DataFrame, p: Parameterization):
        fs = df.to_features()
        assert len(fs) == 1
        val = getattr(fs[0], p.feature.attribute_name)
        assert isinstance(val, type(p.canonical_rich))
        assert val == p.canonical_rich

    def test_prim_to_dataframe(self, p: Parameterization):
        df = DataFrame(
            {
                p.feature: [p.prim],
            }
        )
        self._validate_df(df, p)

    def test_df_from_pyarrow(self, p: Parameterization):
        series = pl.from_arrow(p.pa)
        assert isinstance(series, pl.Series)
        pl_df = pl.DataFrame({p.feature.fqn: series})
        df = DataFrame(pl_df)
        self._validate_df(df, p)

    def test_serialized_dtype(self, p: Parameterization):
        assert p.feature.converter.serialized_dtype == p.expected_serialized_dtype
        assert p.feature.converter.serialized_dtype.to_pyarrow_dtype() == p.expected_pa_dtype
