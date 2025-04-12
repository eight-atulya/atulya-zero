from collections import OrderedDict
from typing import Any
import uuid
from atulya import Atulya, AtulyaConfig, AtulyaContext
from python.helpers import files, history
import json
from initialize import initialize

from python.helpers.log import Log, LogItem

CHATS_FOLDER = "tmp/chats"
LOG_SIZE = 1000
CHAT_FILE_NAME = "chat.json"


def get_chat_folder_path(ctxid: str):
    return files.get_abs_path(CHATS_FOLDER, ctxid)

def save_tmp_chat(context: AtulyaContext):
    path = _get_chat_file_path(context.id)
    files.make_dirs(path)
    data = _serialize_context(context)
    js = _safe_json_serialize(data, ensure_ascii=False)
    files.write_file(path, js)


def load_tmp_chats():
    _convert_v080_chats()
    folders = files.list_files("tmp/chats/", "*")
    json_files = []
    for folder in folders:
        json_files.append(_get_chat_file_path(folder))

    ctxids = []
    for file in json_files:
        try:
            js = files.read_file(file)
            data = json.loads(js)
            ctx = _deserialize_context(data)
            ctxids.append(ctx.id)
        except Exception as e:
            print(f"Error loading chat {file}: {e}")
    return ctxids


def _get_chat_file_path(ctxid: str):
    return files.get_abs_path(CHATS_FOLDER, ctxid, CHAT_FILE_NAME)


def _convert_v080_chats():
    json_files = files.list_files("tmp/chats", "*.json")
    for file in json_files:
        path = files.get_abs_path(CHATS_FOLDER, file)
        name = file.rstrip(".json")
        fold = files.get_abs_path(CHATS_FOLDER, name)
        new = _get_chat_file_path(name)
        files.move_file(path, new)


def load_json_chats(jsons: list[str]):
    ctxids = []
    for js in jsons:
        data = json.loads(js)
        if "id" in data:
            del data["id"]  # remove id to get new
        ctx = _deserialize_context(data)
        ctxids.append(ctx.id)
    return ctxids


def export_json_chat(context: AtulyaContext):
    data = _serialize_context(context)
    js = _safe_json_serialize(data, ensure_ascii=False)
    return js


def remove_chat(ctxid):
    files.delete_dir(get_chat_folder_path(ctxid))



def _serialize_context(context: AtulyaContext):
    # serialize atulyas
    atulyas = []
    atulya = context.atulya0
    while atulya:
        atulyas.append(_serialize_atulya(atulya))
        atulya = atulya.data.get(Atulya.DATA_NAME_SUBORDINATE, None)

    return {
        "id": context.id,
        "name": context.name,
        "atulyas": atulyas,
        "streaming_atulya": (
            context.streaming_atulya.number if context.streaming_atulya else 0
        ),
        "log": _serialize_log(context.log),
    }


def _serialize_atulya(atulya: Atulya):
    data = {k: v for k, v in atulya.data.items() if not k.startswith("_")}

    history = atulya.history.serialize()

    return {
        "number": atulya.number,
        "data": data,
        "history": history,
    }


def _serialize_log(log: Log):
    return {
        "guid": log.guid,
        "logs": [
            item.output() for item in log.logs[-LOG_SIZE:]
        ],  # serialize LogItem objects
        "progress": log.progress,
        "progress_no": log.progress_no,
    }


def _deserialize_context(data):
    config = initialize()
    log = _deserialize_log(data.get("log", None))

    context = AtulyaContext(
        config=config,
        id=data.get("id", None),  # get new id
        name=data.get("name", None),
        log=log,
        paused=False,
        # atulya0=atulya0,
        # streaming_atulya=straming_atulya,
    )

    atulyas = data.get("atulyas", [])
    atulya0 = _deserialize_atulyas(atulyas, config, context)
    streaming_atulya = atulya0
    while streaming_atulya.number != data.get("streaming_atulya", 0):
        streaming_atulya = streaming_atulya.data.get(Atulya.DATA_NAME_SUBORDINATE, None)

    context.atulya0 = atulya0
    context.streaming_atulya = streaming_atulya

    return context


def _deserialize_atulyas(
    atulyas: list[dict[str, Any]], config: AtulyaConfig, context: AtulyaContext
) -> Atulya:
    prev: Atulya | None = None
    zero: Atulya | None = None

    for ag in atulyas:
        current = Atulya(
            number=ag["number"],
            config=config,
            context=context,
        )
        current.data = ag.get("data", {})
        current.history = history.deserialize_history(
            ag.get("history", ""), atulya=current
        )
        if not zero:
            zero = current

        if prev:
            prev.set_data(Atulya.DATA_NAME_SUBORDINATE, current)
            current.set_data(Atulya.DATA_NAME_SUPERIOR, prev)
        prev = current

    return zero or Atulya(0, config, context)


# def _deserialize_history(history: list[dict[str, Any]]):
#     result = []
#     for hist in history:
#         content = hist.get("content", "")
#         msg = (
#             HumanMessage(content=content)
#             if hist.get("type") == "human"
#             else AIMessage(content=content)
#         )
#         result.append(msg)
#     return result


def _deserialize_log(data: dict[str, Any]) -> "Log":
    log = Log()
    log.guid = data.get("guid", str(uuid.uuid4()))
    log.set_initial_progress()

    # Deserialize the list of LogItem objects
    i = 0
    for item_data in data.get("logs", []):
        log.logs.append(
            LogItem(
                log=log,  # restore the log reference
                no=i,  # item_data["no"],
                type=item_data["type"],
                heading=item_data.get("heading", ""),
                content=item_data.get("content", ""),
                kvps=OrderedDict(item_data["kvps"]) if item_data["kvps"] else None,
                temp=item_data.get("temp", False),
            )
        )
        log.updates.append(i)
        i += 1

    return log


def _safe_json_serialize(obj, **kwargs):
    def serializer(o):
        if isinstance(o, dict):
            return {k: v for k, v in o.items() if is_json_serializable(v)}
        elif isinstance(o, (list, tuple)):
            return [item for item in o if is_json_serializable(item)]
        elif is_json_serializable(o):
            return o
        else:
            return None  # Skip this property

    def is_json_serializable(item):
        try:
            json.dumps(item)
            return True
        except (TypeError, OverflowError):
            return False

    return json.dumps(obj, default=serializer, **kwargs)
