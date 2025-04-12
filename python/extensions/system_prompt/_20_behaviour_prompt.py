from datetime import datetime
from python.helpers.extension import Extension
from atulya import Atulya, LoopData
from python.helpers import files, memory


class BehaviourPrompt(Extension):

    async def execute(self, system_prompt: list[str]=[], loop_data: LoopData = LoopData(), **kwargs):
        prompt = read_rules(self.atulya)
        system_prompt.insert(0, prompt) #.append(prompt)

def get_custom_rules_file(atulya: Atulya):
    return memory.get_memory_subdir_abs(atulya) + f"/behaviour.md"

def read_rules(atulya: Atulya):
    rules_file = get_custom_rules_file(atulya)
    if files.exists(rules_file):
        rules = files.read_file(rules_file)
        return atulya.read_prompt("atulya.system.behaviour.md", rules=rules)
    else:
        rules = atulya.read_prompt("atulya.system.behaviour_default.md")
        return atulya.read_prompt("atulya.system.behaviour.md", rules=rules)
  