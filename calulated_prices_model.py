"""Billing Model for CSV report"""

from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class CalculatedPrice:
    fee_price: float
    time_price: float
    kwh_price: float
    total_price: float
    session_id: str
    supplier_price_id: str

    @staticmethod
    def from_dict(obj: Any) -> 'CalculatedPrice':
        assert isinstance(obj, dict)
        fee_price = from_float(obj.get("fee_price"))
        time_price = from_float(obj.get("time_price"))
        kwh_price = from_float(obj.get("kwh_price"))
        total_price = from_float(obj.get("total_price"))
        session_id = from_str(obj.get("session_id"))
        supplier_price_id = from_str(obj.get("supplier_price_id"))
        return CalculatedPrice(fee_price, time_price, kwh_price, total_price, session_id, supplier_price_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["fee_price"] = to_float(self.fee_price)
        result["time_price"] = to_float(self.time_price)
        result["kwh_price"] = to_float(self.kwh_price)
        result["total_price"] = to_float(self.total_price)
        result["session_id"] = from_str(self.session_id)
        result["supplier_price_id"] = from_str(self.supplier_price_id)
        return result


def calculated_price_from_dict(s: Any) -> List[CalculatedPrice]:
    return from_list(CalculatedPrice.from_dict, s)


def calculated_price_to_dict(x: List[CalculatedPrice]) -> Any:
    return from_list(lambda x: to_class(CalculatedPrice, x), x)