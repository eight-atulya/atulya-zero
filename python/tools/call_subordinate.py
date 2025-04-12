from atulya import Atulya, UserMessage
from python.helpers.tool import Tool, Response


class Delegation(Tool):

    async def execute(self, message="", reset="", **kwargs):
        # create subordinate atulya using the data object on this atulya and set superior atulya to his data object
        if (
            self.atulya.get_data(Atulya.DATA_NAME_SUBORDINATE) is None
            or str(reset).lower().strip() == "true"
        ):
            sub = Atulya(
                self.atulya.number + 1, self.atulya.config, self.atulya.context
            )
            sub.set_data(Atulya.DATA_NAME_SUPERIOR, self.atulya)
            self.atulya.set_data(Atulya.DATA_NAME_SUBORDINATE, sub)

        # add user message to subordinate atulya
        subordinate: Atulya = self.atulya.get_data(Atulya.DATA_NAME_SUBORDINATE)
        subordinate.hist_add_user_message(UserMessage(message=message, attachments=[]))
        # run subordinate monologue
        result = await subordinate.monologue()
        # result
        return Response(message=result, break_loop=False)
