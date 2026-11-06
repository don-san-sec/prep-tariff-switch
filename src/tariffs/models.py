"""Tariff and customer-tariff models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum


class Fuel(StrEnum):
    """A billed fuel. Electricity and gas are billed separately."""

    ELEC = "ELEC"
    GAS = "GAS"


class TariffKind(StrEnum):
    """Fixed tariffs have a contract; variable tariffs do not."""

    FIXED = "FIXED"
    VARIABLE = "VARIABLE"


@dataclass
class Tariff:
    """A tariff as offered in the catalog. Amounts are whole pence.

    Fixed tariffs carry a contract end date and an exit fee; variable
    tariffs carry neither.
    """

    tariff_id: str
    kind: TariffKind
    name: str
    monthly_price_pence: int
    exit_fee_pence: int = 0
    contract_end: date | None = None


@dataclass
class CustomerTariff:
    """The tariff a customer is currently on, and for which fuels."""

    customer_id: str
    tariff_id: str
    fuels: list[Fuel] = field(default_factory=list)