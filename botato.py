import config
from commanding import parse_phrase
import logging
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

        command = content.split(" ")[0]
        if command == result.intent and result.intent in functions:
            # await cls.sendMessage(type, group, qq, str(result))
            
            # Call functions
            await functions[result.intent](cls, result, { "type": type, "qq": qq, "group": group, "msgid": msgid, "content": content})
