# SPDX-License-Identifier: MIT
# Copyright (c) 2022 MBition GmbH
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .odxlink import OdxDocFragment, OdxLinkDatabase, OdxLinkId


@dataclass
class StateTransition:
    """
    Corresponds to STATE.
    """

    odx_id: OdxLinkId
    short_name: str
    long_name: Optional[str]
    source_short_name: Optional[str]
    target_short_name: Optional[str]

    @staticmethod
    def from_et(et_element, doc_frags: List[OdxDocFragment]) -> "StateTransition":

        short_name = et_element.findtext("SHORT-NAME")
        odx_id = OdxLinkId.from_et(et_element, doc_frags)
        assert odx_id is not None

        long_name = et_element.findtext("LONG-NAME")
        source_short_name = (
            et_element.find("SOURCE-SNREF").attrib["SHORT-NAME"]
            if et_element.find("SOURCE-SNREF") is not None else None)
        target_short_name = (
            et_element.find("TARGET-SNREF").attrib["SHORT-NAME"]
            if et_element.find("TARGET-SNREF") is not None else None)

        return StateTransition(
            odx_id=odx_id,
            short_name=short_name,
            long_name=long_name,
            source_short_name=source_short_name,
            target_short_name=target_short_name,
        )

    def _build_odxlinks(self) -> Dict[OdxLinkId, Any]:
        return {self.odx_id: self}

    def _resolve_references(self, odxlinks: OdxLinkDatabase) -> None:
        pass
