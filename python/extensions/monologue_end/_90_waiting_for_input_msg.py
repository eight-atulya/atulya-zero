from python.helpers.extension import Extension
from atulya import LoopData

class WaitingForInputMsg(Extension):

    async def execute(self, loop_data: LoopData = LoopData(), **kwargs):
        # show temp info message
        if self.atulya.number == 0:
            self.atulya.context.log.set_initial_progress()

