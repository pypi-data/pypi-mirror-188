from __future__ import annotations

import functools
from typing import TYPE_CHECKING, Generic, Optional, Protocol, Sequence, Type, TypeVar, Union, cast

import pyarrow as pa

from chalk.features._encoding.json import structure_json_to_primitive, unstructure_primitive_to_json
from chalk.features._encoding.primitive import TPrimitive
from chalk.features._encoding.pyarrow import pyarrow_to_polars, pyarrow_to_primitive, rich_to_pyarrow
from chalk.features._encoding.rich import structure_primitive_to_rich, unstructure_rich_to_primitive
from chalk.features._encoding.serialized_dtype import serialize_pyarrow_dtype
from chalk.utils.json import TJSON

if TYPE_CHECKING:
    import polars as pl

_TRich = TypeVar("_TRich")
_TRichCo = TypeVar("_TRichCo", covariant=True)
_TRichCon = TypeVar("_TRichCon", contravariant=True)

_TPrim = TypeVar("_TPrim", bound=TPrimitive)
_TPrimCo = TypeVar("_TPrimCo", bound=TPrimitive, covariant=True)
_TPrimCon = TypeVar("_TPrimCon", bound=TPrimitive, contravariant=True)


class TEncoder(Protocol[_TPrimCo, _TRichCon]):
    def __call__(self, value: _TRichCon, /) -> _TPrimCo:
        ...


class TDecoder(Protocol[_TPrimCon, _TRichCo]):
    def __call__(self, value: _TPrimCon, /) -> _TRichCo:
        ...


class _UnknownType:
    ...


_UNKNOWN = _UnknownType()


class FeatureConverter(Generic[_TPrim, _TRich]):
    def __init__(
        self,
        name: str,
        rich_type: Union[Type[_TRich], _UnknownType] = _UNKNOWN,
        pyarrow_dtype: Optional[pa.DataType] = None,
        encoder: Optional[TEncoder[_TPrim, _TRich]] = None,
        decoder: Optional[TDecoder[_TPrim, _TRich]] = None,
    ) -> None:
        self._name = name
        self._rich_type = rich_type
        if pyarrow_dtype is None:
            if isinstance(rich_type, _UnknownType):
                raise ValueError("Either the `rich_type` or `pyarrow_dtype` must be provided")

            pyarrow_dtype = rich_to_pyarrow(rich_type, name)
        self._pyarrow_dtype = pyarrow_dtype
        self._primitive_type = pyarrow_to_primitive(self._pyarrow_dtype, name)
        if isinstance(rich_type, _UnknownType):
            if encoder is not None:
                raise ValueError("An encoder cannot be specified without also specifying the `rich_type`")
            if decoder is not None:
                raise ValueError("An encoder cannot be specified without also specifying the `rich_type`")
        self._encoder = encoder
        self._decoder = decoder
        self._serialized_dtype = serialize_pyarrow_dtype(self._pyarrow_dtype)

    def _to_primitive(self, val: Optional[_TRich]) -> Optional[_TPrim]:
        if val is None or self._encoder is None:
            # Structuring null values to the primitive type to ensure that a singular null for an entire struct
            # is propagated to individual struct fields -- e.g.
            # class LatLong:
            #     lat: Optional[float]
            #     long: Optional[float]
            # then self._from_prim(None) == LatLong(None, None)
            # Using self.primitive_type, rather than self._rich_type, as the primitive type
            # might not be registered on the converter for custom classes
            try:
                x = unstructure_rich_to_primitive(val)
                y = structure_primitive_to_rich(x, cast(Type[_TRich], self.primitive_type))
                return cast(Optional[_TPrim], y)
            except (TypeError, ValueError) as e:
                raise TypeError(f"Could not convert '{val}' to `{self.primitive_type}`") from e
        return self._encoder(val)

    def _from_prim(self, val: Optional[Union[_TPrim, _TRich]]) -> Optional[_TRich]:
        if isinstance(self._rich_type, _UnknownType):
            raise ValueError(
                "Rich types cannot be used as the FeatureConverter was created without providing a `rich_type`"
            )
        if val is None:
            # Structuring null values to the primitive type to ensure that a singular null for an entire struct
            # is propagated to individual struct fields -- e.g.
            # class LatLong:
            #     lat: Optional[float]
            #     long: Optional[float]
            # then self._from_prim(None) == LatLong(None, None)
            # Using self.primitive_type, rather than self._rich_type, as the primitive type
            # might not be registered on the converter for custom classes
            try:
                val = structure_primitive_to_rich(cast(_TPrim, val), cast(Type[_TRich], self.primitive_type))
            except (TypeError, ValueError) as e:
                raise TypeError(f"Could not convert '{val}' to `{self.primitive_type}`") from e

        if self._decoder is None:
            try:
                return structure_primitive_to_rich(cast(_TPrim, val), self._rich_type)
            except (TypeError, ValueError) as e:
                raise TypeError(f"Could not convert '{val}' to `{self._rich_type}`") from e
        if isinstance(val, self._rich_type):
            return cast(_TRich, val)
        return self._decoder(cast(_TPrim, val))

    def from_rich_to_pyarrow(self, values: Sequence[Optional[_TRich]], /) -> pa.Array:
        prim_values = [self.from_rich_to_primitive(x) for x in values]
        return self.from_primitive_to_pyarrow(prim_values)

    def from_rich_to_primitive(self, value: Optional[_TRich]) -> Optional[_TPrim]:
        # Ensure that the rich value is indeed the rich type
        # For example, if a string is passed in for a datetime value, convert it into a datetime
        value = self.from_primitive_to_rich(cast(_TPrim, value))
        return self._to_primitive(value)

    def from_rich_to_json(self, value: Optional[_TRich]) -> TJSON:
        prim_val = self.from_rich_to_primitive(value)
        return self.from_primitive_to_json(prim_val)

    def from_pyarrow_to_rich(self, values: pa.Array, /) -> Sequence[Optional[_TRich]]:
        return [self.from_primitive_to_rich(x) for x in values.to_pylist()]

    def from_pyarrow_to_json(self, values: pa.Array) -> Sequence[TJSON]:
        return [self.from_primitive_to_json(x) for x in self.from_pyarrow_to_primitive(values)]

    def from_pyarrow_to_primitive(self, values: pa.Array) -> Sequence[Optional[_TPrim]]:
        return values.to_pylist()

    def from_primitive_to_rich(self, value: Optional[_TPrim]) -> Optional[_TRich]:
        return self._from_prim(value)

    def from_primitive_to_pyarrow(self, value: Sequence[Optional[_TPrim]]) -> pa.Array:
        x = pa.array(value, type=self._pyarrow_dtype)
        return x

    def from_primitive_to_json(self, value: Optional[_TPrim]) -> TJSON:
        return unstructure_primitive_to_json(value)

    def from_json_to_rich(self, value: TJSON) -> Optional[_TRich]:
        prim_val = self.from_json_to_primitive(value)
        return self.from_primitive_to_rich(prim_val)

    def from_json_to_pyarrow(self, values: Sequence[TJSON]) -> pa.Array:
        primitive_vals = [cast(_TPrim, self.from_json_to_primitive(x)) for x in values]
        return self.from_primitive_to_pyarrow(primitive_vals)

    def from_json_to_primitive(self, value: TJSON) -> Optional[_TPrim]:
        try:
            return cast(Optional[_TPrim], structure_json_to_primitive(value, self._primitive_type))
        except (ValueError, TypeError) as e:
            raise TypeError(f"Could not convert '{value}' to `{self._primitive_type}`") from e

    @property
    def pyarrow_dtype(self):
        return self._pyarrow_dtype

    @property
    def rich_type(self) -> Type[_TRich]:
        if isinstance(self._rich_type, _UnknownType):
            raise ValueError(
                "Rich types cannot be used as the FeatureConverter was created without providing a `rich_type`"
            )
        return self._rich_type

    @property
    def primitive_type(self) -> Type[TPrimitive]:
        return self._primitive_type

    @functools.cached_property
    def polars_dtype(self) -> Union[pl.DataType, Type[pl.DataType]]:
        return pyarrow_to_polars(self.pyarrow_dtype, self._name)

    @property
    def serialized_dtype(self):
        return self._serialized_dtype
