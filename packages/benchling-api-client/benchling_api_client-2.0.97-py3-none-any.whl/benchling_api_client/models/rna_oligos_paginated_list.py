from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.rna_oligo import RnaOligo
from ..types import UNSET, Unset

T = TypeVar("T", bound="RnaOligosPaginatedList")


@attr.s(auto_attribs=True, repr=False)
class RnaOligosPaginatedList:
    """  """

    _rna_oligos: Union[Unset, List[RnaOligo]] = UNSET
    _next_token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("rna_oligos={}".format(repr(self._rna_oligos)))
        fields.append("next_token={}".format(repr(self._next_token)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "RnaOligosPaginatedList({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        rna_oligos: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._rna_oligos, Unset):
            rna_oligos = []
            for rna_oligos_item_data in self._rna_oligos:
                rna_oligos_item = rna_oligos_item_data.to_dict()

                rna_oligos.append(rna_oligos_item)

        next_token = self._next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if rna_oligos is not UNSET:
            field_dict["rnaOligos"] = rna_oligos
        if next_token is not UNSET:
            field_dict["nextToken"] = next_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_rna_oligos() -> Union[Unset, List[RnaOligo]]:
            rna_oligos = []
            _rna_oligos = d.pop("rnaOligos")
            for rna_oligos_item_data in _rna_oligos or []:
                rna_oligos_item = RnaOligo.from_dict(rna_oligos_item_data, strict=False)

                rna_oligos.append(rna_oligos_item)

            return rna_oligos

        try:
            rna_oligos = get_rna_oligos()
        except KeyError:
            if strict:
                raise
            rna_oligos = cast(Union[Unset, List[RnaOligo]], UNSET)

        def get_next_token() -> Union[Unset, str]:
            next_token = d.pop("nextToken")
            return next_token

        try:
            next_token = get_next_token()
        except KeyError:
            if strict:
                raise
            next_token = cast(Union[Unset, str], UNSET)

        rna_oligos_paginated_list = cls(
            rna_oligos=rna_oligos,
            next_token=next_token,
        )

        rna_oligos_paginated_list.additional_properties = d
        return rna_oligos_paginated_list

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def rna_oligos(self) -> List[RnaOligo]:
        if isinstance(self._rna_oligos, Unset):
            raise NotPresentError(self, "rna_oligos")
        return self._rna_oligos

    @rna_oligos.setter
    def rna_oligos(self, value: List[RnaOligo]) -> None:
        self._rna_oligos = value

    @rna_oligos.deleter
    def rna_oligos(self) -> None:
        self._rna_oligos = UNSET

    @property
    def next_token(self) -> str:
        if isinstance(self._next_token, Unset):
            raise NotPresentError(self, "next_token")
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value

    @next_token.deleter
    def next_token(self) -> None:
        self._next_token = UNSET
