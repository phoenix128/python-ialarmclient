import re
import aiohttp
from typing import List
import lxml.html

from .log import Log
from .const import *
from .status import IalarmStatus
from .zone import IalarmZone


"""
Client for Ialarm
"""


class IalarmClient:
    def __init__(self, username: str, password: str, url: str):
        self._password = password
        self._username = username
        self._url = url
        self._zones = None
        self._status = None

    async def arm_stay(self) -> bool:
        return await self._set_status(STATUS_ARMED_STAY)

    async def disarm(self) -> bool:
        return await self._set_status(STATUS_DISARMED)

    async def arm_away(self) -> bool:
        return await self._set_status(STATUS_ARMED_AWAY)

    async def cancel_alarm(self) -> bool:
        return await self._set_status(STATUS_CANCEL_ALARM)

    def _get_auth(self) -> aiohttp.BasicAuth:
        return aiohttp.BasicAuth(login=self._username, password=self._password)

    async def _set_status(self, command: int) -> bool:
        data = {
            'Ctrl': command,
            'BypassNum': '00',
            'BypassOpt': '0'
        }

        endpoint_url = self._url + '/RemoteCtr.htm'
        async with aiohttp.ClientSession(auth=self._get_auth()) as session:
            async with session.post(endpoint_url, data=data) as response:
                if response.status == 200:
                    return True

        return False

    async def _load_zones(self):
        if self._zones is None:
            self._zones = []

            for i in range(0, MAX_ZONES):
                Log.info('Reading zone {} information'.format(i + 1))

                endpoint_url = self._url + '/Zone.htm'
                data = {
                    'zoneNo': str(i+1)
                }
                async with aiohttp.ClientSession(auth=self._get_auth()) as session:
                    async with session.post(endpoint_url, data=data) as response:
                        if response.status == 200:
                            dom = lxml.html.fromstring(await response.text())

                            zone_type_path = "//select[@name='ZoneType']/option[@selected='selected']"
                            alarm_mode_path = "//select[@name='ZoneBell']/option[@selected='selected']"
                            zone_name_path = "//input[@name='ZoneName']"

                            zone_type = int(dom.xpath(zone_type_path)[0].attrib['value'])
                            alarm_mode = int(dom.xpath(alarm_mode_path)[0].attrib['value'])
                            zone_name = str(dom.xpath(zone_name_path)[0].attrib['value'])

                            self._zones.append(IalarmZone(
                                zone_type=zone_type,
                                alarm_mode=alarm_mode,
                                number=i+1,
                                name=zone_name
                            ))

    async def get_zones(self) -> List[IalarmZone]:
        return self._zones

    async def get_status(self) -> IalarmStatus:
        return self._status

    async def refresh(self) -> None:
        Log.info('Refreshing status')
        await self._load_zones()

        endpoint_url = self._url + '/RemoteCtr.htm'
        async with aiohttp.ClientSession(auth=self._get_auth()) as session:
            async with session.get(endpoint_url) as response:
                if response.status == 200:
                    html = await response.text()
                    dom = lxml.html.fromstring(html)

                    status_path = "//option[@selected='selected']"
                    arm_status = int(dom.xpath(status_path)[0].attrib['value'])

                    m = re.search(r'var ZoneMsg = new Array\((.+?)\)', html)
                    zones_status_codes = m.group(1).split(',')

                    m = re.search(r'var SysMsg = (\d+);', html)
                    sys_status = int(m.group(1))

                    alarmed_zones = []
                    for i in range(0, len(zones_status_codes)):
                        self._zones[i].status = int(zones_status_codes[i])
                        if self._zones[i].status_alarm:
                            alarmed_zones.append(self._zones[i])

                    self._status = IalarmStatus(
                        sys_status=sys_status,
                        arm_status=arm_status,
                        alarmed_zones=alarmed_zones
                    )
