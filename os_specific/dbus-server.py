from dbus_next.aio import MessageBus
from dbus_next.service import ServiceInterface, method
import asyncio

class DbusInterface(ServiceInterface):
    def __init__(self):
        super().__init__('com.screendiary.bridge')

    @method()
    def updateActiveWindow(self, title: "s", caption: "s"):
        print(f'Updated window: {title}, {caption}')

async def main():
    bus = await MessageBus().connect()
    interface = DbusInterface()
    bus.export('/com/screendiary/bridge', interface)
    await bus.request_name('com.screendiary.bridge')

    await bus.wait_for_disconnect()

asyncio.get_event_loop().run_until_complete(main())