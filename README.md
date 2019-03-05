# Python client for iAlarm

Also compatible with Meiantech, Allarmi365, and others

## Usage example

```
#!/usr/bin/env python
import asyncio

from ialarmclient import IalarmClient


async def start():
    ialarm = IalarmClient(
        username="username", # <- Your alarm web interface username
        password="password", # <- Your alarm web interface password
        url="http://192.168.123.123" # <- Your alarm web interface URL (no trailing slash)
    )

    # Refresh alarm status, to be called every time you need to read updated information
    # May take up to 30-40 seconds the first time. Subsequent calls will be almost immediate.
    await ialarm.refresh() 
    
    # Retrieve information about your alarm zones (name, status, etc...)
    zones = await ialarm.get_zones()
    for zone in zones:
        if zone.type != ialarmclient.ZONE_TYPE_DISABLED:
            print("Zone {} is {}".format(zone.number, zone.name))
            # Other information can be read (see IalarmZone)
    
    # Retrieve alarm status (armed, disarmed, power failure, etc...)
    status = await ialarm.get_status()
    
    # Commands to arm/disarm your system
    await ialarm.arm_stay()
    await ialarm.arm_away()
    await ialarm.disarm()
    await ialarm.cancel_alarm()
    
    # List all zones in alarm
    status = await ialarm.get_status()
    for alarmed_zone in status.alarmed_zones:
        print("Zone {} is alarmed".format(alarmed_zone.name))
    
    # Status information for your system
    if status.power_source_failure:
        print("Power failure")
        
    if status.low_battery:
        print("Low battery")
    
    if status.panic_alarm:
        print("Panic alarm triggered")
        
    if status.arm_status == ialarmclient.STATUS_ARMED_AWAY:
        print("System armed")
    elif status.arm_status == ialarmclient.STATUS_ARMED_STAY:
        print("System armed (STAY)")
    elif status.arm_status == ialarmclient.STATUS_DISARMED:
        print("System disarmed")    

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())

```