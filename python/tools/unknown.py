from python.helpers.tool import Tool, Response
from python.extensions.system_prompt._10_system_prompt import (
    get_tools_prompt,
)


class Unknown(Tool):
    async def execute(self, **kwargs):
        tools = get_tools_prompt(self.atulya)
        return Response(
            message=self.atulya.read_prompt(
                "fw.tool_not_found.md", tool_name=self.name, tools_prompt=tools
            ),
            break_loop=False,
        )
