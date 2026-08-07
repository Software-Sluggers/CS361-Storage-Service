# models.py
# CS 361 - Summer 2026
# Daniel Magann
# 8/6/2026
# Sources:
# FastAPI documentation: https://fastapi.tiangolo.com/
# Official Pydanctic Documentation: https://pydantic.dev/docs/validation/dev/concepts/models/
# Python UUID module: https://docs.python.org/3/library/uuid.html
# Pydantic Guide: https://www.datacamp.com/tutorial/pydantic?utm_cid=23781701475&utm_aid=196565213275&utm_campaign=260417_1-ps-dscia~amx-tofu~python_2-b2c_3-nam_4-prc_5-na_6-na_7-le_8-pdsh-go_9-nb-e_10-na_11-na&utm_loc=1014529-&utm_mtd=p-c&utm_kw=modules%20python&utm_source=google&utm_medium=paid_search&utm_content=ps-dscia~nam-en~amx~tofu~tutorial~python&gad_source=1&gad_campaignid=23781701475&gbraid=0AAAAADQ9WsFEHsoXvoiuB85-dyLFzRb5D&gclid=CjwKCAjwhNbTBhB4EiwAsFSg-qLMPzcxd3E0iNa0UVTPNXI-LgWLOltXXPzHCEkP4GJXGr9za8CE2xoChCwQAvD_BwE
# Description: This file contains Pydantic models used by the storage service.

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class StoreDataRequest(BaseModel):
    """
    Payload accepted
    """

    data: Dict[str, Any] = Field(..., description="Application data payload")
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Optional metadata associated with the record",
    )


class StoreDataResponse(BaseModel):
    """
    Response returned
    """

    id: str


class RecordResponse(BaseModel):
    """
    Response returned
    """

    id: str
    client_id: str
    data: Dict[str, Any]
    metadata: Dict[str, Any]