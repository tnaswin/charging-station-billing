"""
    Model class for charges to parse and store 
    transaction data from JSON response.
"""
from dataclasses import dataclass
from typing import Optional, Any, TypeVar, Type, cast
from datetime import datetime
from uuid import UUID
import dateutil.parser


T = TypeVar("T")


def from_float(x: Any) -> float:
    if isinstance(x, str):
        x = x.replace(",",".")
        if x.upper() == "FALSE":
            return None
    return float(x)

def from_none(x: Any) -> Any:
    assert x is None or x == ""
    return None


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_bool(x: Any) -> bool:
    if isinstance(x, str):
        if x.upper() == "TRUE":
            x = True
        elif x.upper() == "FALSE":
            x = False
    assert isinstance(x, bool)
    return x


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Transaction:
    metering_signature: Optional[str] = None
    charging_end: Optional[datetime] = None
    charging_start: Optional[datetime] = None
    country_code: Optional[str] = None
    evseid: Optional[str] = None
    meter_value_end: Optional[float] = None
    meter_value_start: Optional[float] = None
    partner_product_id: Optional[bool] = None
    proveider_id: Optional[str] = None
    session_id: Optional[UUID] = None
    session_end: Optional[datetime] = None
    session_start: Optional[datetime] = None
    uid: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Transaction':
        assert isinstance(obj, dict)
        metering_signature = from_union([from_str, from_none], obj.get("Metering signature"))
        charging_end = from_union([from_datetime, from_none], obj.get("Charging end"))
        charging_start = from_union([from_datetime, from_none], obj.get("Charging start"))
        country_code = from_union([from_str, from_none], obj.get("CountryCode"))
        evseid = from_union([from_str, from_none], obj.get("EVSEID"))
        meter_value_end = from_union([from_float, from_none], obj.get("Meter value end"))
        meter_value_start = from_union([from_float, from_none], obj.get("Meter value start"))
        partner_product_id = from_union([from_bool, from_str ,from_none], obj.get("Partner product ID"))
        proveider_id = from_union([from_str, from_none], obj.get("Proveider ID"))
        session_id = from_union([lambda x: UUID(x), from_none], obj.get("Session ID"))
        session_end = from_union([from_datetime, from_none], obj.get("Session end"))
        session_start = from_union([from_datetime, from_none], obj.get("Session start"))
        uid = from_union([from_str, from_none], obj.get("UID"))
        return Transaction(metering_signature, charging_end, charging_start, country_code, evseid, meter_value_end, meter_value_start, partner_product_id, proveider_id, session_id, session_end, session_start, uid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Metering signature"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.metering_signature)
        result["Charging end"] = from_union([lambda x: x.isoformat(), from_none], self.charging_end)
        result["Charging start"] = from_union([lambda x: x.isoformat(), from_none], self.charging_start)
        result["CountryCode"] = from_union([from_str, from_none], self.country_code)
        result["EVSEID"] = from_union([from_str, from_none], self.evseid)
        result["Meter value end"] = from_union([from_str, from_none], self.meter_value_end)
        result["Meter value start"] = from_union([from_str, from_none], self.meter_value_start)
        result["Partner product ID"] = from_union([from_bool, from_none], self.partner_product_id)
        result["Proveider ID"] = from_union([from_str, from_none], self.proveider_id)
        result["Session ID"] = from_union([lambda x: str(x), from_none], self.session_id)
        result["Session end"] = from_union([lambda x: x.isoformat(), from_none], self.session_end)
        result["Session start"] = from_union([lambda x: x.isoformat(), from_none], self.session_start)
        result["UID"] = from_union([from_str, from_none], self.uid)
        return result


def transaction_from_dict(s: Any) -> Transaction:
    return Transaction.from_dict(s)


def transaction_to_dict(x: Transaction) -> Any:
    return to_class(Transaction, x)
