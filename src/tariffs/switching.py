"""In-app tariff switching (TARF-31).

Records a customer moving from their current tariff onto a new one: when the
switch takes effect, any exit fee due, and the confirmation notification the
customer receives.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from tariffs.catalog import Catalog
from tariffs.models import CustomerTariff, Tariff, TariffKind
from tariffs.notifications import Notifier

SWITCH_CONFIRMATION_TEMPLATE = "tariff_switch_confirmation"


class SameTariffError(ValueError):
    """The customer is already on the tariff they asked to switch to."""


@dataclass
class SwitchResult:
    """The outcome of a switch. Amounts are whole pence.

    effective_date   the day the new tariff applies from
    exit_fee_pence   the exit fee charged for leaving the old tariff
    """

    effective_date: date
    exit_fee_pence: int


def switch_tariff(
    catalog: Catalog,
    current: CustomerTariff,
    new_tariff: Tariff,
    today: date,
    notifier: Notifier,
) -> SwitchResult:
    """Switch the customer onto new_tariff and send the confirmation."""
    current_tariff = catalog.get(current.tariff_id)

    if new_tariff.tariff_id == current.tariff_id:
        raise SameTariffError(f"already on {new_tariff.tariff_id}")

    exit_fee_pence = (
        current_tariff.exit_fee_pence
        if current_tariff.kind == TariffKind.FIXED
        else 0
    )

    notifier.send(
        current.customer_id,
        SWITCH_CONFIRMATION_TEMPLATE,
        new_tariff=new_tariff.name,
        exit_fee_pence=exit_fee_pence,
    )

    return SwitchResult(effective_date=today, exit_fee_pence=exit_fee_pence)