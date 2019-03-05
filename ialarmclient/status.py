"""DTO for ialarm status definition"""

from typing import List
from .zone import IalarmZone


class IalarmStatus:
    def __init__(
            self,
            sys_status: int,
            arm_status: int,
            alarmed_zones: List[IalarmZone]
    ):
        self._sys_status = sys_status
        self._arm_status = arm_status
        self._alarmed_zones = alarmed_zones

    @property
    def sys_status(self) -> int:
        return self._sys_status

    @property
    def power_source_failure(self):
        return self.sys_status & 1 != 0

    @property
    def low_battery(self):
        return self.sys_status & 2 != 0

    @property
    def panic_alarm(self):
        return self.sys_status & 4 != 0

    @property
    def arm_status(self) -> int:
        return self._arm_status

    @property
    def alarmed_zones(self) -> List[IalarmZone]:
        return self._alarmed_zones
