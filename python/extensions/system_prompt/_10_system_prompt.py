from datetime import datetime, timezone
from python.helpers.extension import Extension
from atulya import Atulya, LoopData
from python.helpers.localization import Localization


class SystemPrompt(Extension):

    async def execute(self, system_prompt: list[str]=[], loop_data: LoopData = LoopData(), **kwargs):
        # append main system prompt and tools
        main = get_main_prompt(self.atulya)
        tools = get_tools_prompt(self.atulya)
        system_prompt.append(main)
        system_prompt.append(tools)


def get_main_prompt(atulya: Atulya):
    return atulya.read_prompt("atulya.system.main.md")


def get_tools_prompt(atulya: Atulya):
    prompt = atulya.read_prompt("atulya.system.tools.md")
    if atulya.config.chat_model.vision:
        prompt += '\n' + atulya.read_prompt("atulya.system.tools_vision.md")
    return prompt