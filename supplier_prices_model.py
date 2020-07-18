"""
    Model class for supplier data to parse and store 
    supplier price data from JSON response.
"""
from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Callable, Type, cast
from uuid import UUID


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


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    print("********************")
    print(x)
    assert False


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_bool(x: Any) -> bool:
    if isinstance(x, str):
        if x.upper() == "TRUE":
            x = True
        elif x.upper() == "FALSE":
            x = False
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class TimePrice:
    billing_each_timeframe: Optional[float] = None
    hour_from: Optional[float] = None
    hour_to: Optional[float] = None
    minute_price: Optional[str] = None
    kwh_price: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'TimePrice':
        assert isinstance(obj, dict)
        billing_each_timeframe = from_union([from_float, from_none], obj.get("billing_each_timeframe"))
        hour_from = from_union([from_float, from_none], obj.get("hour from"))
        hour_to = from_union([from_float, from_none], obj.get("hour to"))
        minute_price = from_union([from_str, from_none], obj.get("minute price"))
        kwh_price = from_union([from_str, from_none], obj.get("kwh price"))
        return TimePrice(billing_each_timeframe, hour_from, hour_to, minute_price, kwh_price)

    def to_dict(self) -> dict:
        result: dict = {}
        result["billing_each_timeframe"] = from_union([to_float, from_none], self.billing_each_timeframe)
        result["hour from"] = from_union([from_float, from_none], self.hour_from)
        result["hour to"] = from_union([from_float, from_none], self.hour_to)
        result["minute price"] = from_union([from_str, from_none], self.minute_price)
        result["kwh price"] = from_union([from_str, from_none], self.kwh_price)
        return result


@dataclass
class SupplierPrice:
    company_name: Optional[str] = None
    currency: Optional[List[str]] = None
    evse_id: Optional[str] = None
    identifier: Optional[UUID] = None
    product_id: Optional[str] = None
    has_complex_minute_price: Optional[bool] = None
    has_hour_day: Optional[bool] = None
    has_max_session_fee: Optional[bool] = None
    has_minimum_billing_threshold: Optional[bool] = None
    has_session_fee: Optional[bool] = None
    has_kwh_price: Optional[bool] = None
    interval: Optional[str] = None
    max_session_fee: Optional[str] = None
    min_billing_amount: Optional[str] = None
    min_duration: Optional[str] = None
    session_fee: Optional[str] = None
    kwh_price: Optional[float] = None
    min_cosumed_energy: Optional[float] = None
    simple_minute_price: Optional[str] = None
    time_price: Optional[List[TimePrice]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SupplierPrice':
        assert isinstance(obj, dict)
        company_name = from_union([from_str, from_none], obj.get("Company name"))
        currency = from_union([lambda x: from_list(from_str, x), from_none], obj.get("Currency"))
        evse_id = from_union([from_str, lambda x: str(x), from_none], obj.get("EVSE ID"))
        identifier = from_union([lambda x: UUID(x), from_none], obj.get("Identifier"))
        product_id = from_union([from_str, lambda x: str(x) ,from_none], obj.get("Product ID"))
        has_complex_minute_price = from_union([from_bool, from_none], obj.get("has complex minute price"))
        has_hour_day = from_union([from_bool, from_none], obj.get("has hour day"))
        has_max_session_fee = from_union([from_bool, from_none], obj.get("has max session Fee"))
        has_minimum_billing_threshold = from_union([from_bool, from_none], obj.get("has minimum billing threshold"))
        has_session_fee = from_union([from_bool, from_none], obj.get("has session fee"))
        has_kwh_price = from_union([from_bool, from_none], obj.get("has kwh price"))
        interval = from_union([from_str, from_none], obj.get("interval"))
        max_session_fee = from_union([from_str, from_none], obj.get("max_session fee"))
        min_billing_amount = from_union([from_str, from_none], obj.get("min billing amount"))
        min_duration = from_union([from_str, from_none], obj.get("min duration"))
        session_fee = from_union([from_str, from_none], obj.get("session Fee"))
        kwh_price = from_union([from_float, from_none], obj.get("kwh Price"))
        min_cosumed_energy = from_union([from_float, from_none], obj.get("min cosumed energy"))
        simple_minute_price = from_union([from_str, from_none], obj.get("simple minute price"))
        time_price = from_union([lambda x: from_list(TimePrice.from_dict, x), from_none], obj.get("time_price"))
        return SupplierPrice(company_name, currency, evse_id, identifier, product_id, has_complex_minute_price, has_hour_day, has_max_session_fee, has_minimum_billing_threshold, has_session_fee, has_kwh_price, interval, max_session_fee, min_billing_amount, min_duration, session_fee, kwh_price, min_cosumed_energy, simple_minute_price, time_price)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Company name"] = from_union([from_str, from_none], self.company_name)
        result["Currency"] = from_union([lambda x: from_list(from_str, x), from_none], self.currency)
        result["EVSE ID"] = from_union([from_str, from_none], self.evse_id)
        result["Identifier"] = from_union([lambda x: str(x), from_none], self.identifier)
        result["Product ID"] = from_union([from_bool, from_none], self.product_id)
        result["has complex minute price"] = from_union([from_bool, from_none], self.has_complex_minute_price)
        result["has hour day"] = from_union([from_bool, from_none], self.has_hour_day)
        result["has max session Fee"] = from_union([from_bool, from_none], self.has_max_session_fee)
        result["has minimum billing threshold"] = from_union([from_bool, from_none], self.has_minimum_billing_threshold)
        result["has session fee"] = from_union([from_bool, from_none], self.has_session_fee)
        result["has kwh price"] = from_union([from_bool, from_none], self.has_kwh_price)
        result["interval"] = from_union([from_str, from_none], self.interval)
        result["max_session fee"] = from_union([from_str, from_none], self.max_session_fee)
        result["min billing amount"] = from_union([from_str, from_none], self.min_billing_amount)
        result["min duration"] = from_union([from_str, from_none], self.min_duration)
        result["session Fee"] = from_union([from_str, from_none], self.session_fee)
        result["kwh Price"] = from_union([from_str, from_none], self.kwh_price)
        result["min cosumed energy"] = from_union([from_str, from_none], self.min_cosumed_energy)
        result["simple minute price"] = from_union([from_str, from_none], self.simple_minute_price)
        result["time_price"] = from_union([lambda x: from_list(lambda x: to_class(TimePrice, x), x), from_none], self.time_price)
        return result


def supplier_price_from_dict(s: Any) -> SupplierPrice:
    return SupplierPrice.from_dict(s)


def supplier_price_to_dict(x: SupplierPrice) -> Any:
    return to_class(SupplierPrice, x)
    