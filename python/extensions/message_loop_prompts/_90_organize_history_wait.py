from python.helpers.extension import Extension
from atulya import LoopData
from python.extensions.message_loop_end._10_organize_history import DATA_NAME_TASK
import asyncio


class OrganizeHistoryWait(Extension):
    async def execute(self, loop_data: LoopData = LoopData(), **kwargs):

        # sync action only required if the history is too large, otherwise leave it in background
        while self.atulya.history.is_over_limit():
            # get task
            task = self.atulya.get_data(DATA_NAME_TASK)

            # Check if the task is already done
            if task:
                if not task.done():
                    self.atulya.context.log.set_progress("Compressing history...")

                # Wait for the task to complete
                await task

                # Clear the coroutine data after it's done
                self.atulya.set_data(DATA_NAME_TASK, None)
            else:
                # no task running, start and wait
                self.atulya.context.log.set_progress("Compressing history...")
                await self.atulya.history.compress()

