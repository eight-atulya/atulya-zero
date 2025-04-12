from python.helpers.extension import Extension
from atulya import Atulya, LoopData

DATA_NAME_ITER_NO = "iteration_no"

class IterationNo(Extension):
    async def execute(self, loop_data: LoopData = LoopData(), **kwargs):
        # total iteration number
        no = self.atulya.get_data(DATA_NAME_ITER_NO) or 0
        self.atulya.set_data(DATA_NAME_ITER_NO, no + 1)


def get_iter_no(atulya: Atulya) -> int:
    return atulya.get_data(DATA_NAME_ITER_NO) or 0