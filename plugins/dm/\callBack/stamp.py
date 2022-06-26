# fileName : plugins/dm/callBack/stamp.py
# copyright ©️ 2021 nabilanavab

# LOGGING INFO: DEBUG
import logging
logger=logging.getLogger(__name__)
logging.basicConfig(
                   level=logging.DEBUG,
                   format="%(levelname)s:%(name)s:%(message)s" # %(asctime)s:
                   )

import os
import time
import fitz
import shutil
from time import sleep
from pdf import PROCESS
from pyrogram import filters
from plugins.thumbName import (
                              thumbName,
                              formatThumb
                              )
from plugins.checkPdf import checkPdf
from pyrogram import Client as ILovePDF
from configs.images import PDF_THUMBNAIL
from plugins.footer import footer, header
from plugins.fileSize import get_size_format as gSF
from plugins.progress import progress, uploadProgress
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#--------------->
#--------> LOCAL VARIABLES
#------------------->

cancel = InlineKeyboardMarkup(
                             [[InlineKeyboardButton("💤 CANCEL 💤",
                                     callback_data = "cancelP2I")]]
                             )

"""
____VARIABLES____

stmp = Stamp CB

STAMP ANNOTATIONS: [pymuPdf/fituz](annot)
0 : STAMP_Approved
1 : STAMP_AsIs
2 : STAMP_Confidential
3 : STAMP_Departmental
4 : STAMP_Experimental
5 : STAMP_Expired
6 : STAMP_Final
7 : STAMP_ForComment
8 : STAMP_ForPublicRelease
9 : STAMP_NotApproved
10: STAMP_NotForPublicRelease
11: STAMP_Sold
12: STAMP_TopSecret
13: STAMP_Draft


COLOR: [RGB]
r = red, g = green, b = blue
"""

#--------------->
#--------> PDF COMPRESSION
#------------------->

# pdfMessage to stamp --> "stamp"(stampselect)
stamp = filters.create(lambda _, __, query: query.data=="stamp")
Kstamp = filters.create(lambda _, __, query: query.data.startswith("Kstamp"))

# stampSelect to color --> "stmp"(stampcolor)
stmp = filters.create(lambda _, __, query: query.data.startswith("stmp"))
Kstmp = filters.create(lambda _, __, query: query.data.startswith("Kstmp"))

# color --> stamping process
colors = ["color", "Kcolor"]
color = filters.create(lambda _, __, query: query.data.startswith(tuple(colors)))

# stamp selet message(with unknown pdf page number)
@ILovePDF.on_callback_query(stamp)
async def _stamp(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        await callbackQuery.answer()
        await callbackQuery.edit_message_text(
            "__أضف ختم » حدد الختم:         \nمجموع الصفحات: غير معروف _ 😐\n__Add Stamp » Select Stamp:         \nTotal pages: unknown__ 😐",
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("ليس للنشر العام 🤧", callback_data="stmp|10")
                    ],[
                        InlineKeyboardButton("للنشر العام 🥱", callback_data="stmp|8")
                    ],[
                        InlineKeyboardButton("سري 🤫", callback_data="stmp|2"),
                        InlineKeyboardButton("إداري 🤝", callback_data="stmp|3")
                    ],[
                        InlineKeyboardButton("التجريبية 🔬", callback_data="stmp|4"),
                        InlineKeyboardButton("منتهية الصلاحية 🐀",callback_data="stmp|5")
                    ],[
                        InlineKeyboardButton("نهائي 🔧", callback_data="stmp|6"),
                        InlineKeyboardButton("للتعليق 🗯️",callback_data="stmp|7")
                    ],[
                        InlineKeyboardButton("غير معتمد 😒",callback_data="stmp|9"),
                        InlineKeyboardButton("تمت الموافقة 🥳", callback_data="stmp|0")
                    ],[
                        InlineKeyboardButton("تباع ✊",callback_data="stmp|11"),
                        InlineKeyboardButton("سري للغاية 😷", callback_data="stmp|12"),
                    ],[
                        InlineKeyboardButton("مسودة 👀",callback_data="stmp|13"),
                        InlineKeyboardButton("آيس 🤏", callback_data="stmp|1")
                    ],[
                        InlineKeyboardButton("« عودة «", callback_data="BTPM")
                    ]
                ]
            )
        )
    except Exception: pass

# Stamp select message (with known pdf page number)
@ILovePDF.on_callback_query(Kstamp)
async def _Kstamp(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        await callbackQuery.answer()
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            f"__أضف ختم » حدد الختم:          \nعدد الصفحات: {number_of_pages}__ 🌟",
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("ليس للنشر العام 🤧", callback_data=f"Kstmp|{number_of_pages}|10")
                    ],[
                        InlineKeyboardButton("للنشر العام 🥱", callback_data=f"Kstmp|{number_of_pages}|8")
                    ],[
                        InlineKeyboardButton("سري 🤫", callback_data=f"Kstmp|{number_of_pages}|2"),
                        InlineKeyboardButton("إداري 🤝", callback_data=f"Kstmp|{number_of_pages}|3")
                    ],[
                        InlineKeyboardButton("التجريبية 🔬", callback_data=f"Kstmp|{number_of_pages}|4"),
                        InlineKeyboardButton("منتهية الصلاحية 🐀",callback_data=f"Kstmp|{number_of_pages}|5")
                    ],[
                        InlineKeyboardButton("نهائي 🔧", callback_data=f"Kstmp|{number_of_pages}|6"),
                        InlineKeyboardButton("للتعليق 🗯️",callback_data=f"Kstmp|{number_of_pages}|7")
                    ],[
                        InlineKeyboardButton("غير معتمد 😒",callback_data=f"Kstmp|{number_of_pages}|9"),
                        InlineKeyboardButton("تمت الموافقة 🥳", callback_data=f"Kstmp|{number_of_pages}|0")
                    ],[
                        InlineKeyboardButton("تباع ✊",callback_data=f"Kstmp|{number_of_pages}|11"),
                        InlineKeyboardButton("سري للغاية 😷", callback_data=f"Kstmp|{number_of_pages}|12"),
                    ],[
                        InlineKeyboardButton("مسودة 👀",callback_data=f"Kstmp|{number_of_pages}|13"),
                        InlineKeyboardButton("آيس 🤏", callback_data=f"Kstmp|{number_of_pages}|1")
                    ],[
                        InlineKeyboardButton("« عودة «", callback_data=f"KBTPM|{number_of_pages}")
                    ]
                ]
            )
        )
    except Exception: pass

# Stamp color message (with unknown pdf page number)
@ILovePDF.on_callback_query(stmp)
async def _stmp(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        await callbackQuery.answer()
        _, annot = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            "__أضف التوقيع » حدد اللون:         \nمجموع الصفحات: غير معروف _ 😐",
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("أحمر ❤️", callback_data=f"color|{annot}|r"),
                        InlineKeyboardButton("أزرق 💙", callback_data=f"color|{annot}|b")
                    ],[
                        InlineKeyboardButton("أخضر 💚", callback_data=f"color|{annot}|g"),
                        InlineKeyboardButton("أصفر 💛", callback_data=f"color|{annot}|c1")
                    ],[
                        InlineKeyboardButton("وردي 💜", callback_data=f"color|{annot}|c2"),
                        InlineKeyboardButton("درجة لون 💚", callback_data=f"color|{annot}|c3")
                    ],[
                        InlineKeyboardButton("أبيض 🤍", callback_data=f"color|{annot}|c4"),
                        InlineKeyboardButton("أسود 🖤", callback_data=f"color|{annot}|c5")
                    ],[
                        InlineKeyboardButton("« عودة «", callback_data=f"stamp")
                    ]
                ]
            )
        )
    except Exception: pass

# Stamp color message (with known pdf page number)
@ILovePDF.on_callback_query(Kstmp)
async def _Kstmp(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        await callbackQuery.answer()
        _, number_of_pages, annot = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            f"__أضف التوقيع » حدد اللون:           \nعدد الصفحات: {number_of_pages}__ 🌟",
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("أحمر ❤️", callback_data=f"Kcolor|{annot}|r"),
                        InlineKeyboardButton("أزرق 💙", callback_data=f"Kcolor|{annot}|b")
                    ],[
                        InlineKeyboardButton("أخضر 💚", callback_data=f"Kcolor|{annot}|g"),
                        InlineKeyboardButton("أصفر 💛", callback_data=f"Kcolor|{annot}|c1")
                    ],[
                        InlineKeyboardButton("وردي 💜", callback_data=f"Kcolor|{annot}|c2"),
                        InlineKeyboardButton("درجة اللون 💚", callback_data=f"Kcolor|{annot}|c3")
                    ],[
                        InlineKeyboardButton("أبيض 🤍", callback_data=f"Kcolor|{annot}|c4"),
                        InlineKeyboardButton("أسود 🖤", callback_data=f"Kcolor|{annot}|c5")
                    ],[
                        InlineKeyboardButton("« عودة «", callback_data=f"Kstamp|{number_of_pages}")
                    ]
                ]
            )
        )
    except Exception:
        pass

@ILovePDF.on_callback_query(color)
async def _color(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        
        chat_id = callbackQuery.message.chat.id
        message_id = callbackQuery.message.message_id
        
        # CHECK IF USER IN PROCESS
        if chat_id in PROCESS:
            await callbackQuery.answer(
                                      "جاري العمل Work in progress .. ⏳"
                                      )
            return
        _, annot, colr = callbackQuery.data.split("|")
        await callbackQuery.answer()
        # ↓ ADD TO PROCESS       ↓ CALLBACK DATA
        PROCESS.append(chat_id); data = callbackQuery.data
        # STARTED DOWNLOADING
        input_file = f"{message_id}/inPut.pdf"
        output_file = f"{message_id}/outPut.pdf"
        
        downloadMessage = await callbackQuery.message.reply_text(
                                                                "`قم بتنزيل ملف pdf Downloading your 📕...` 📥", 
                                                                quote = True
                                                                )
        file_id = callbackQuery.message.reply_to_message.document.file_id
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        fileNm = callbackQuery.message.reply_to_message.document.file_name
        # DOWNLOAD PROGRESS
        c_time = time.time()
        downloadLoc = await bot.download_media(
                                              message = file_id,
                                              file_name = input_file,
                                              progress = progress,
                                              progress_args = (
                                                              fileSize,
                                                              downloadMessage,
                                                              c_time
                                                              )
                                              )
        
        # COLOR CODE
        if colr=="r": color=(1, 0, 0)
        elif colr=="b": color=(0, 0, 1)
        elif colr=="g": color=(0, 1, 0)
        elif colr=="c1": color=(1, 1, 0)
        elif colr=="c2": color=(1, 0, 1)
        elif colr=="c3": color=(0, 1, 1)
        elif colr=="c4": color=(1, 1, 1)
        elif colr=="c5": color=(0, 0, 0)
        
        # CHECK DOWNLOAD COMPLETED OR CANCELED
        if downloadLoc is None:
            PROCESS.remove(chat_id)
            return
        #STAMPING STARTED
        await downloadMessage.edit(
                                  "`بدأ الختم ..` 💠"
                                  )
        if data.startswith("color"):
            checked = await checkPdf(input_file, callbackQuery)
            if not(checked == "pass"):
                await downloadMessage.delete()
                return
        r = fitz.Rect(72, 72, 440, 200)
        with fitz.open(input_file) as doc:
            page = doc.load_page(0)
            annot = page.add_stamp_annot(
                                        r,
                                        stamp = int(f"{annot}")
                                        )
            annot.set_colors(stroke = color)
            annot.set_opacity(0.5)
            annot.update()
            doc.save(output_file)
        # Getting thumbnail
        thumbnail, fileName = await thumbName(callbackQuery.message, fileNm)
        if PDF_THUMBNAIL != thumbnail:
            location = await bot.download_media(
                                    message = thumbnail,
                                    file_name = f"{callbackQuery.message.message_id}.jpeg"
                                    )
            thumbnail = await formatThumb(location)
        
        await downloadMessage.edit(
                                  "⚙️ `بدأ التحميل (Started Uploading)..` 📤",
                                  reply_markup = cancel
                                  )
        await callbackQuery.message.reply_chat_action(
                                                     "upload_document"
                                                     )
        c_time = time.time()
        await callbackQuery.message.reply_document(
                                                  file_name = fileName,
                                                  document = output_file,
                                                  thumb = thumbnail,
                                                  quote = True,
                                                  caption = " مختوم stamped pdf",
                                                  progress = uploadProgress,
                                                  progress_args = (
                                                                  downloadMessage,
                                                                  c_time
                                                                  )
                                                  )
        # DELETE DOWNLOAD MESSAGE
        await downloadMessage.delete()
        try:
            os.remove(location)
        except Exception: pass
        PROCESS.remove(chat_id)
        shutil.rmtree(f"{message_id}")
        await footer(callbackQuery.message, False)
    except Exception as e:
        logger.exception(
                        "CB/STAMP:CAUSES %(e)s ERROR",
                        exc_info=True
                        )
        try:
            PROCESS.remove(chat_id)
            shutil.rmtree(f"{message_id}")
            await downloadMessage.delete()
        except Exception:
            pass

#                                                                                             Telegram: @nabilanavab
