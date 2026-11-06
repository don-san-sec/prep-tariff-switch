"""The in-memory tariff catalog."""

from __future__ import annotations

from tariffs.models import Tariff


class Catalog:
    """The tariffs Brightwatt currently offers.

    In-memory here; production is backed by the product database. Tariffs
    are keyed by id, so a customer on a retired tariff won't resolve.
    """

    def __init__(self) -> None:
        self._tariffs: dict[str, Tariff] = {}

    def add(self, tariff: Tariff) -> None:
        """Add a tariff to the catalog, keyed by its id."""
        self._tariffs[tariff.tariff_id] = tariff

    def list(self) -> list[Tariff]:
        """Every tariff in the catalog."""
        return list(self._tariffs.values())

    def get(self, tariff_id: str) -> Tariff:
        """Fetch a tariff by id. Raises KeyError for unknown ids."""
        return self._tariffs[tariff_id]