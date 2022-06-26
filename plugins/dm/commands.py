# fileName : plugins/dm/commands.py
# copyright ©️ 2021 nabilanavab

# LOGGING INFO: DEBUG
import logging
logger=logging.getLogger(__name__)
logging.basicConfig(
                   level=logging.DEBUG,
                   format="%(levelname)s:%(name)s:%(message)s" # %(asctime)s:
                   )

import os
import shutil
from pdf import PDF
from pdf import PROCESS
from asyncio import sleep
from pyrogram import filters
from configs.dm import Config
from configs.images import FEEDBACK
from pyrogram import Client as ILovePDF


feedbackMsg=f"[feedback|اكتب تعليقًا 📋]({FEEDBACK})"

userHELP="""[رسائل أوامر المستخدم]:\n
/start, /ping: للتحقق مما إذا كان Bot على قيد الحياة\n
/help, /command: على هذه الرسالة\n
/generate: إنشاء PDF بالصور الحالية\n
/delete: يحذف الصورة الحالية لقائمة انتظار pdf\n
/txt2pdf: لإنشاء ملفات pdf من رسالة نصية\n
/feedback: لكتابة شيء عن i2PDFbot
[USER COMMAND MESSAGES]:\n
/start, /ping: to check whether Bot alive\n
/help, /command: for this message\n
/generate: generate PDF with current images\n
/delete: deletes the current image to pdf queue\n
/txt2pdf: to create pdf files from text message\n
/feedback: to Write something about i2PDFbot"""

adminHelp="""\n\n[رسائل أوامر المشرف]:\n
/server: للحصول على البوت الحالي ، حالة الخادم\n
/ban `id/usrnm`: لحظر مستخدم\n
/unban `id/usrnm`:لفك حظر مستخدم محظور\n
/deleteUser `id/usrnm`: حذف المستخدم من قاعدة البيانات\n
/forward `id/usrnm`: ردت على إعادة توجيه الرسالة إلى المستخدم\n
/forward c `id/usrnm`: رد على إعادة توجيه الرسالة كنسخة \n
/users: الحصول على قائمة مستخدمي البوت الحاليين\n
/broadcast: رد بث الرسالة لجميع المستخدمين\n
/broadcast f: رد على إعادة توجيه الرسالة إلى مستخدمي الروبوت"""

footer="""\n\nDev: [i2PDFbot](https://t.me/i2pdfbotchannel)\n
Bot: @i2pdfbot
[Support Channel قناة الدعم](https://t.me/i2pdfbotchannel)"""


# ❌ CANCELS CURRENT PDF TO IMAGES WORK ❌
@ILovePDF.on_message(
                    (filters.private | filters.group) &
                    filters.command(["cancel"]) &
                    filters.incoming
                    )
async def cancelP2I(bot, message):
    try:
        PROCESS.remove(message.from_user.id)
        await message.delete()          # delete /cancel if process canceled
    except Exception:
        try:
            await message.reply_chat_action(
                                           "typing"
                                           )
            await message.reply_text(
                                    '🤔', quote = True
                                    )
        except Exception:
            pass

# ❌ DELETS CURRENT IMAGES TO PDF QUEUE (/delete) ❌
@ILovePDF.on_message(
                    (filters.private | filters.group) &
                    filters.command(["delete"]) &
                    filters.incoming
                    )
async def _cancelI2P(bot, message):
    try:
        await message.reply_chat_action(
                                       "typing"
                                       )
        del PDF[message.chat.id]
        await message.reply_text(
                                "`تم حذف قائمة الانتظار بنجاح ..Queue deleted Successfully..`🤧",
                                quote = True
                                )
        shutil.rmtree(f"{message.chat.id}")
    except Exception:
        await message.reply_text(
                                "`لم يتم تأسيس قائمة انتظار ..No Queue founded..`😲",
                                quote = True
                                )

# ❌ GET USER ID (/id) ❌
@ILovePDF.on_message(
                    (filters.private | filters.group) &
                    filters.command(["id"]) &
                    filters.incoming
                    )
async def userId(bot, message):
    try:
        if message.chat.id == message.from_user.id:
            await message.reply_text(
                                    f"**اسمك(Your Name)** : {message.from_user.mention}\n"
                                    f"**معرف(Id)** : `{message.chat.id}`",
                                    quote = True
                                    )
        else:
            await message.reply_text(
                                    f"**عنوان المحادثة(Chat Title)**    : `{message.chat.title}`\n"
                                    f"**يوزر نيم (User Name)** : `{message.from_user.mention}`\n"
                                    f"**جات ادي(Chat ID)**        : `{message.chat.id}`\n"
                                    f"**يوزر ادي(User ID)**        : `{message.from_user.id}`",
                                    quote = True
                                    )
    except Exception as e:
        logger.exception(
                        "/ID:CAUSES %(e)s ERROR",
                        exc_info=True
                        )


# ❌ GET FEEDBACK MESSAGE ❌
@ILovePDF.on_message(
                    (filters.private | filters.group) &
                    filters.command(["feedback"]) &
                    filters.incoming
                    )
async def feedback(bot, message):
    try:
        await message.reply_text(
                                feedbackMsg,
                                disable_web_page_preview = True
                                )
    except Exception as e:
        logger.exception(
                        "/FEEDBACK:CAUSES %(e)s ERROR",
                        exc_info = True
                        )

# ❌ DELETS CURRENT IMAGES TO PDF QUEUE (/delete) ❌
@ILovePDF.on_message(
                    (filters.private | filters.group) &
                    filters.command(["help", "commands"]) &
                    filters.incoming)
async def _help(bot, message):
    try:
        await message.reply_chat_action(
                                       "typing"
                                       )
        helpMsg = await message.reply(
                                     "⚙️ يعالج Processing..",
                                     quote = True
                                     )
        await sleep(2)
        HELP = userHELP
        await helpMsg.edit(
                          HELP
                          )
        if message.from_user.id in Config.ADMINS:
            await sleep(4)
            HELP = userHELP + adminHelp
            await helpMsg.edit(
                              HELP
                              )
        await sleep(2)
        HELP += footer
        await helpMsg.edit(
                          HELP,
                          disable_web_page_preview = True)
    except Exception as e:
        logger.exception(
                        "/HELP:CAUSES %(e)s ERROR خطا",
                        exc_info=True
                        )

#                                                                                  Telegram: @nabilanavab
