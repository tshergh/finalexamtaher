# fileName : plugins/dm/url.py
# copyright ©️ 2021 nabilanavab

# LOGGING INFO: DEBUG
import logging
logger=logging.getLogger(__name__)
logging.basicConfig(
                   level=logging.DEBUG,
                   format="%(levelname)s:%(name)s:%(message)s" # %(asctime)s:
                   )

import os
from pdf import PROCESS
from asyncio import sleep
from pyrogram import filters
from configs.dm import Config
from plugins.thumbName import (
                              thumbName,
                              formatThumb
                              )
from pyrogram import Client as ILovePDF
from plugins.footer import header, footer
from plugins.fileSize import get_size_format as gSF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

reply_markup = InlineKeyboardMarkup(
                     [[
                             InlineKeyboardButton("🧭 Get PDF File حصول على ملف 🧭",
                                             callback_data = "getFile")
                     ]]
               )


if Config.MAX_FILE_SIZE:
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE"))
    MAX_FILE_SIZE_IN_kiB = MAX_FILE_SIZE * (10 **6 )
else:
    MAX_FILE_SIZE = False


# url Example مثال : https://t.me/channel/message
#              https://t.me/i2pdfbotchannel/9
links = ["https://telegram.dog/", "https://t.me/", "https://telegram.me/"]

async def getPDF(current, t, message, total=0, typ="DOWNLOADED"):
    if t != 0:
        total = t
    if typ == "DOWNLOADED":
        edit = "📥 تنزيل(DOWNLOADED): {:.2f}% 📥"
    else:
        edit = "📤 تحميل(UPLOADED): {:.2f}% 📤"
    percentage = current * 100 / total
    await message.edit_reply_markup(
          InlineKeyboardMarkup(
                              [[
                                  InlineKeyboardButton(
                                                    edit.format(percentage),
                                                    callback_data="nabilanavab")
                              ]]
          ))

@ILovePDF.on_message(
                    filters.private &
                    ~filters.edited &
                    filters.incoming &
                    filters.text
                    )
async def _url(bot, message):
    try:
        await message.reply_chat_action(
                                       "typing"
                                       )
        data = await message.reply(
                                  "__تم البدء في جلب البيانات.\nStarted Fetching Datas..__ 📥",
                                  quote = True
                                  )
        
        url = message.text
        # Get one or more messages from a chat by using message identifiers.
        # get_messages(chat_id, message_ids)
        if url.startswith(tuple(links)):
            part = url.split("/")
            message_ids = int(part[-1])
            try:
                chat_id = int(part[-2])
                chat_id = int("-100" + f"{chat_id}")
            except Exception:
                chat_id = part[-2]
            try:
                file = await bot.get_messages(
                                             chat_id = chat_id,
                                             message_ids = message_ids
                                             )
            except Exception as e:
                return await data.edit(
                                      "🐉هناك خطأ ما\nSOMETHING WENT WRONG 🐉\n\n"
                                      f"ERRORخطا: `{e}`\n\n"
                                      "في المجموعات ، يمكن للروبوتات فقط جلب المستندات التي يتم إرسالها بعد الانضمام إلى المجموعة \nIn Groups, Bots Can Only fetch documents Send After Joining Group =)",
                                      reply_markup = InlineKeyboardMarkup(
                                           [[
                                                 InlineKeyboardButton("🚫 Close اغلق🚫",
                                                         callback_data = "closeALL")
                                           ]]
                                      ))
            await sleep(1)
            isProtect = "🔒 Protected 🔒" if (
                                 (file.sender_chat and file.sender_chat.has_protected_content) or (
                                 file.chat and file.chat.has_protected_content)) else "👀 Public 👀"
            if file.chat.type == "channel":
                return await data.edit(
                                      f"[Open Chat فتح المحادثة]({url})\n\n"
                                      f"**ABOUT CHAT حول الجات↓**\n"
                                      f"Chat Type  نوع جات : {file.chat.type}\n"
                                      f"Chat Name اسم الجات : {file.sender_chat.title}\n"
                                      f"Chat Usr يوزر جات : @{file.sender_chat.username}\n"
                                      f"Chat ID    معرف جات : {file.sender_chat.id}\n"
                                      f"Date وقت: {file.date}\n\n"
                                      f"**ABOUT MEDIA حول وسائط↓**\n"
                                      f"Media    وسائط   : {file.media}\n"
                                      f"File Name اسم ملف : {file.document.file_name}\n"
                                      f"File Size  حجم ملف : {await gSF(file.document.file_size)}\n\n" + 
                                      f"File Type نوع ملف : {isProtect}",
                                      reply_markup = reply_markup if file.document.file_name[-4:] == ".pdf" else None,
                                      disable_web_page_preview = True
                                      )
            return await data.edit(
                                  f"[Open Chat فتح جات]({url})\n\n "
                                  f"**ABOUT CHAT حول جات↓**\n"
                                  f"Chat Type  نوع جات : {file.chat.type}\n"
                                  f"Chat Name اسم جات: {file.chat.title}\n"
                                  f"Chat Usr  يوزر جات  : @{file.chat.username}\n"
                                  f"Chat ID   معرف جات  : {file.chat.id}\n"
                                  f"Date الوقت: {file.date}\n\n"
                                  f"**ABOUT MEDIA حول وسائط ↓**\n"
                                  f"Media   الوسائط     : {file.media}\n"
                                  f"File Name أسم  ملف: {file.document.file_name}\n"
                                  f"File Size  حجم ملف: {await gSF(file.document.file_size)}\n\n"
                                  f"File Type نوع ملف: {isProtect}",
                                  reply_markup = reply_markup if file.document.file_name[-4:] == ".pdf" else None,
                                  disable_web_page_preview = True
                                  )
            
        return await data.edit(
                              "الرجاء إرسال عنوان Telegram PDF المباشر إلي\nPlease Send Me A Direct Telegram PDF Url"
                              )
    except Exception as e:
        return await data.edit("__تحقق من عنوان URL ، وليس ملف PDF\nCheck Url, Not a PDF File__ 🥲")
        logger.exception(
                        "URL:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

getFile = filters.create(lambda _, __, query: query.data == "getFile")

@ILovePDF.on_callback_query(getFile)
async def _getFile(bot, callbackQuery):
    try:
        # REPLY TO LAGE FILES/DOCUMENTS
        if MAX_FILE_SIZE and fileSize >= int(MAX_FILE_SIZE_IN_kiB):
            return await callbackQuery.answer("ملف كبير Big File.. 🏃")
        
        if callbackQuery.from_user.id in PROCESS:
            return await callbackQuery.answer(
                                             "جاري العمل Work in progress.. 🙇"
                                             )
        if callbackQuery.message.chat.type != "private":
            if await header(bot, callbackQuery):
                return
        PROCESS.append(callbackQuery.from_user.id)
        await callbackQuery.answer("انتظر .. دعني ..\nWait.. Let me.. 😜")
        url = callbackQuery.message.reply_to_message.text
        part = url.split("/")
        message_ids = int(part[-1])
        try:
            chat_id = int(part[-2])
            chat_id = int("-100" + f"{chat_id}")
        except Exception:
            chat_id = part[-2]
        # bot.get_messages
        file = await bot.get_messages(
                                     chat_id = chat_id,
                                     message_ids = message_ids
                                     )
        # if not a protected channel/group [just forward]
        if not (
               (file.sender_chat and file.sender_chat.has_protected_content) or (
               file.chat and file.chat.has_protected_content)):
            PROCESS.remove(callbackQuery.from_user.id)
            return await file.copy(
                                  chat_id = callbackQuery.message.chat.id,
                                  caption = file.caption
                                  )
        await callbackQuery.edit_message_reply_markup(
              InlineKeyboardMarkup(
                                  [[
                                      InlineKeyboardButton(
                                                          "📥 ..تنزيل DOWNLOADING.. 📥",
                                                          callback_data = "nabilanavab")
                                  ]]
              ))
        location = await bot.download_media(
                                           message = file.document.file_id,
                                           file_name = file.document.file_name,
                                           progress = getPDF,
                                           progress_args = (
                                                           callbackQuery.message, file.document.file_size,
                                                           )
                                           )
        await callbackQuery.edit_message_reply_markup(
              InlineKeyboardMarkup(
                                  [[
                                      InlineKeyboardButton(
                                                          "📤 ..تحميل UPLOADING..  📤",
                                                          callback_data = "nabilanavab")
                                  ]]
        ))
        logFile = await callbackQuery.message.reply_document(
                                              document = location,
                                              caption = file.caption,
                                              progress = getPDF,
                                              progress_args = (
                                                              callbackQuery.message, 0, 
                                                              "UPLOADED"
                                                              )
                                              )
        await callbackQuery.edit_message_reply_markup(
              InlineKeyboardMarkup(
                                  [[
                                      InlineKeyboardButton(
                                                          "😎 قناة البوت 😎",
                                                          url = "https://t.me/i2pdfbotchannel")
                                  ]]
        ))
        PROCESS.remove(callbackQuery.from_user.id)
        await footer(callbackQuery.message, logFile)
        os.remove(location)
    except Exception as e:
        PROCESS.remove(callbackQuery.from_user.id); os.remove(location)
        logger.exception(
                        "BAN_USER:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

#                                                                                                           Telegram: @nabilanavab
