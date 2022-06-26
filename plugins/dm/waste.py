# fileName : plugins/dm/waste.py
# copyright ©️ 2021 nabilanavab

# LOGGING INFO: DEBUG
import logging
logger=logging.getLogger(__name__)
logging.basicConfig(
                   level=logging.DEBUG,
                   format="%(levelname)s:%(name)s:%(message)s" # %(asctime)s:
                   )

from pyrogram import filters
from configs.dm import Config
from pyrogram import Client as ILovePDF


#--------------->
#--------> PDF REPLY BUTTON
#------------------->

@ILovePDF.on_message(
                    filters.private &
                    ~filters.edited &
                    filters.incoming &
                    ~filters.user(Config.ADMINS)
                    )
async def _spam(bot, message):
    try:
        await message.reply_chat_action(
                                       "typing"
                                       )
        await message.reply_text(
                                f"` كيف يمكنني  مساعدةno one gonna to help you` 😏",
                                quote = True
                                )
    except Exception as e:
        logger.exception(
                        "/SERVER:CAUSES %(e)s ERROR",
                        exc_info=True
                        )


#                                                     Telegram: @nabilanavab
