import config
from commanding import parse_phrase
import logging
import messages
from functions import commands, functions, regexes
from QQLightBot import ApiProtocol,MsgDict
logger = logging.getLogger('QQLightBot')

class BotatoHandler(ApiProtocol):
    @classmethod
    async def onConnect(cls):
        logger.info('Connected to server successfully.')

    @classmethod
    async def message(cls, type=0, qq='', group='', msgid='', content=''):
        if not content.startswith(config.prefix):
            return

        if type in config.disabled_type:
            return
        if int(qq) in config.shield_qq:
            return
        if type == 2 or type == 3:
            if not int(group) in config.enabled_groups:
                return
        
        content = content[len(config.prefix):]
        result = parse_phrase(content, commands, regexes)

        if result.intent != result.items[0]:
            await cls.sendMessage(type, group, qq, messages.COMMAND_ERROR.format(result.intent))
            return
        else:
            # Call functions
            functions[result.intent](cls, result, { "type": type, "qq": qq, "group": group, "msgid": msgid, "content": content})
