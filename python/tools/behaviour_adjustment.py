from python.helpers import files, memory
from python.helpers.tool import Tool, Response
from atulya import Atulya
from python.helpers.log import LogItem


class UpdateBehaviour(Tool):

    async def execute(self, adjustments="", **kwargs):

        # stringify adjustments if needed
        if not isinstance(adjustments, str):
            adjustments = str(adjustments)

        await update_behaviour(self.atulya, self.log, adjustments)
        return Response(
            message=self.atulya.read_prompt("behaviour.updated.md"), break_loop=False
        )

    # async def before_execution(self, **kwargs):
    #     pass

    # async def after_execution(self, response, **kwargs):
    #     pass


async def update_behaviour(atulya: Atulya, log_item: LogItem, adjustments: str):

    # get system message and current ruleset
    system = atulya.read_prompt("behaviour.merge.sys.md")
    current_rules = read_rules(atulya)

    # log query streamed by LLM
    async def log_callback(content):
        log_item.stream(ruleset=content)

    msg = atulya.read_prompt(
        "behaviour.merge.msg.md", current_rules=current_rules, adjustments=adjustments
    )

    # call util llm to find solutions in history
    adjustments_merge = await atulya.call_utility_model(
        system=system,
        message=msg,
        callback=log_callback,
    )

    # update rules file
    rules_file = get_custom_rules_file(atulya)
    files.write_file(rules_file, adjustments_merge)
    log_item.update(result="Behaviour updated")


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
