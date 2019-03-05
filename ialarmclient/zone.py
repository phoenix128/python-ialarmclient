class IalarmZone:
    def __init__(
        self,
        number: int,
        zone_type: int,
        alarm_mode: int,
        name: str
    ):
        self._name = name
        self._alarm_mode = alarm_mode
        self._number = number
        self._zone_type = zone_type
        self._status = 0

    @property
    def status(self) -> int:
        return self._status

    @status.setter
    def status(self, value: int):
        self._status = value

    @property
    def number(self) -> int:
        return self._number

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> int:
        return self._zone_type

    @property
    def alarm_mode(self) -> int:
        return self._alarm_mode

    @property
    def status_alarm(self) -> bool:
        return self._status & 3 != 0

    @property
    def status_bypass(self) -> bool:
        return self._status & 8 != 0

    @property
    def status_fault(self) -> bool:
        return self._status & 16 != 0

    @property
    def status_lost(self) -> bool:
        return not self.status_bypass and (self._status & 64 != 0)

    @property
    def status_low_battery(self) -> bool:
        return not self.status_bypass and (self._status & 32 != 0)
    
    def __repr__(self):
        return str(self.name)
