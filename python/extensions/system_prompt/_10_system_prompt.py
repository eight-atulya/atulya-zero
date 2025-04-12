from datetime import datetime
from python.helpers.extension import Extension
from atulya import Atulya, LoopData


class SystemPrompt(Extension):

    async def execute(self, system_prompt: list[str]=[], loop_data: LoopData = LoopData(), **kwargs):
        # append main system prompt and tools
        main = get_main_prompt(self.atulya)
        tools = get_tools_prompt(self.atulya)
        system_prompt.append(main)
        system_prompt.append(tools)


def get_main_prompt(atulya: Atulya):
    return get_prompt("atulya.system.main.md", atulya)


def get_tools_prompt(atulya: Atulya):
    prompt = get_prompt("atulya.system.tools.md", atulya)
    if atulya.config.chat_model.vision:
        prompt += '\n' + get_prompt("atulya.system.tools_vision.md", atulya)
    return prompt


def get_prompt(file: str, atulya: Atulya):
    # variables for system prompts
    # TODO: move variables to the end of chain
    # variables in system prompt would break prompt caching, better to add them to the last message in conversation
    vars = {
        "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "atulya_name": atulya.atulya_name,
    }
    return atulya.read_prompt(file, **vars)
