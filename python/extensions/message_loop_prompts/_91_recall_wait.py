from python.helpers.extension import Extension
from atulya import LoopData
from python.extensions.message_loop_prompts._50_recall_memories import DATA_NAME_TASK as DATA_NAME_TASK_MEMORIES
from python.extensions.message_loop_prompts._51_recall_solutions import DATA_NAME_TASK as DATA_NAME_TASK_SOLUTIONS


class RecallWait(Extension):
    async def execute(self, loop_data: LoopData = LoopData(), **kwargs):

            task = self.atulya.get_data(DATA_NAME_TASK_MEMORIES)
            if task and not task.done():
                # self.atulya.context.log.set_progress("Recalling memories...")
                await task

            task = self.atulya.get_data(DATA_NAME_TASK_SOLUTIONS)
            if task and not task.done():
                # self.atulya.context.log.set_progress("Recalling solutions...")
                await task

