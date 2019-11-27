import asyncio
import OpenVisus as ov


class VisusLab(ov.Dataflow):
    def __init__(self):
        ov.IdxModule.attach()
        ov.NodesModule.attach()
        super().__init__()
        self.task = None

    async def _run(self):
        while True:
            # print('step...')
            self.dispatchPublishedMessages()
            await asyncio.sleep(1)
            # time.sleep(1.0) # / 60)

    def start(self):
        if self.task is None:
            self.task = asyncio.create_task(self._run())
        else:
            print('VisusLab already running')

    def cancel(self):
        if self.task is not None:
            self.task.cancel()
            self.task = None

