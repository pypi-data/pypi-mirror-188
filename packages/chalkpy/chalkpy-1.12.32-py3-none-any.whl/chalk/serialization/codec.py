from __future__ import annotations

import warnings
from datetime import datetime
from typing import TYPE_CHECKING, Any, Type, Union, cast

import cattrs
import pytz
from dateutil import parser

if TYPE_CHECKING:
    import polars as pl

    from chalk.features import Feature


def is_numeric(dtype: Union[pl.DataType, Type[pl.DataType]]) -> bool:
    warnings.warn(DeprecationWarning("This method is deprecated"))
    # This function is used only by the engine
    import polars as pl

    return dtype in (
        pl.Float32,
        pl.Float64,
        pl.Int16,
        pl.Int8,
        pl.Int32,
        pl.Int64,
        pl.UInt8,
        pl.UInt16,
        pl.UInt32,
        pl.UInt64,
    )


class FeatureCodec:
    def __init__(self) -> None:
        self.converter = cattrs.Converter()
        self.converter.register_structure_hook(datetime, lambda v, _: parser.isoparse(v))
        self.converter.register_unstructure_hook(
            datetime,
            lambda v: (
                cast(datetime, v) if cast(datetime, v).tzinfo else pytz.utc.localize(cast(datetime, v))
            ).isoformat(),
        )

    def encode(
        self,
        feature: Feature,
        value: Any,
    ):
        # This method is only used by the engine
        warnings.warn(
            DeprecationWarning(
                "FeatureCodec.encode is deprecated. Instead, use `feature.converter.from_rich_to_json(...)`"
            )
        )
        return feature.converter.from_rich_to_json(value)

    def encode_fqn(self, fqn: str, value: Any):
        # This method is only used by the engine
        from chalk.features import Feature

        return self.encode(Feature.from_root_fqn(fqn), value)

    def decode(
        self,
        feature: Feature,
        value: Any,
    ):
        # This method is only used by the engine
        warnings.warn(
            DeprecationWarning(
                "FeatureCodec.decode is deprecated. Instead, use `feature.converter.from_json_to_rich(...)`"
            )
        )

        return feature.converter.from_json_to_rich(value)

    def get_polars_dtype(self, fqn: str) -> Union[pl.DataType, Type[pl.DataType]]:
        # This function is used only by the engine
        warnings.warn(
            DeprecationWarning(
                (
                    "FeatureCodec.get_polars_dtype is deprecated. Instead, use switch to PyArrow dtypes. "
                    "The PyArrow dtype can be found at `feature.converter.pyarrow_dtype`"
                )
            )
        )
        import polars as pl

        from chalk.features import Feature

        feature = Feature.from_root_fqn(fqn)

        if feature.is_has_one or feature.is_has_many:
            warnings.warn("FeatureCodec.get_polars_dtype should not be called on has-one / has-many features")
            return pl.Object
        else:
            return feature.converter.polars_dtype


FEATURE_CODEC = FeatureCodec()
