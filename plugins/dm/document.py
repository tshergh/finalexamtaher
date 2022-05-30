# fileName : plugins/dm/document.py
# copyright ©️ 2021 nabilanavab

import os
import fitz
import shutil
import asyncio
import convertapi
from pdf import PDF
from PIL import Image
from time import sleep
from pdf import invite_link
from pyrogram import filters
from Configs.dm import Config
from pyrogram import Client as ILovePDF
from plugins.fileSize import get_size_format as gSF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#--------------->
#--------> convertAPI instance
#------------------->

if Config.CONVERT_API is not None:
    convertapi.api_secret = Config.CONVERT_API

#--------------->
#--------> MAXIMUM FILE SIZE (IF IN config var.)
#------------------->

if Config.MAX_FILE_SIZE:
    MAX_FILE_SIZE=int(os.getenv("MAX_FILE_SIZE"))
    MAX_FILE_SIZE_IN_kiB=MAX_FILE_SIZE * (10 **6 )
else:
    MAX_FILE_SIZE=False


PDF_THUMBNAIL=Config.PDF_THUMBNAIL

#--------------->
#--------> FILES TO PDF SUPPORTED CODECS
#------------------->

suprtedFile = [
    ".jpg", ".jpeg", ".png"
]                                       # Img to pdf file support

suprtedPdfFile = [
    ".epub", ".xps", ".oxps",
    ".cbz", ".fb2"
]                                      # files to pdf (zero limits)

suprtedPdfFile2 = [
    ".csv", ".doc", ".docx", ".dot",
    ".dotx", ".log", ".html", ".mpt",
    ".odt", ".pot", ".potx", ".pps",
    ".ppsx", ".ppt", ".pptx", ".pub",
    ".rtf", ".txt", ".vdx", ".vsd",
    ".vsdx", ".vst", ".vstx", ".wpd",
    ".wps", ".wri", ".xls", ".xlsb",
    ".xlsx", ".xlt", ".xltx", ".xml"
]                                       # file to pdf (ConvertAPI limit)

#--------------->
#--------> LOCAL VARIABLES
#------------------->


UCantUse = "لا يمكنك استخدام هذا الروبوت لبعض الأسباب "


pdfReplyMsg = """`ماذا تريد أن أفعل بهذا الملف.؟ \n What shall i wanted to do with this file.?`
File name(اسم الملف) : `{}`
File Size(حجم الملف) : `{}`"""


bigFileUnSupport = """Due to Overload(بسبب التحميل الزائد), Owner limits(حدد المطور) {}MB for pdf files(لكل ملفات) 🙇
`please Send me a file less than(لي ملف حجمه أقل من ) {}MB ` 🙃"""


imageAdded = """`تمت إضافة {} صفحة / إلى ملف pdf ..`🤓
/generate  اضغط لإنشاء ملف PDF 🤞"""


errorEditMsg = """حدث خطأ ما ..😐 Something went wrong..😐
error: `{}`
Dev&eng: @ta_ja199 👨‍💻"""


feedbackMsg = "[🌟Rate:تقييم🌟](https://telegramic.org/bot/i2pdfbot/)"

forceSubMsg = """مرحبا [{}](tg://user?id={}) 🤚🏻..!!
يجب عليك انضمام الى قناة لكي تستطيع استخدام البوت اشترك في هذه القناة  :👉👉 @i2pdfbotchannel
وبعدها ارجع للبوت واضغط هذا الامر /start او من ازار اضغط تحديث
لمتابعة كافة تحديثات البوت

You must join a channel in order to use the bot. Subscribe to this channel: 👉👉 @i2pdfbotchannel
Then go back to the bot and press this command / start, or from the buttons, press update
To follow all bot updates`
"""


button=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "😉webbot(موقع)😉",
                    url="https://electrical-engineer-cc40b.web.app/"
                )
            ]
       ]
    )

#--------------->
#--------> PDF REPLY BUTTON
#------------------->

pdfReply=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⭐️ معلومات|info ⭐️", callback_data="pdfInfo"),
                InlineKeyboardButton("🗳 معاينة | preview🗳", callback_data="preview")
            ],[
                InlineKeyboardButton("🖼 الى صور | toImage 🖼", callback_data="toImage"),
                InlineKeyboardButton("✏️ الى نص totext✏️", callback_data="toText")
            ],[
                InlineKeyboardButton("🔐 تشفير | ENCRYPT 🔐", callback_data="encrypt"),
                InlineKeyboardButton("🔒 فك تشفير | DECRYPT🔓",callback_data="decrypt")
            ],[
                InlineKeyboardButton("🗜 ضغط | COMPRESS 🗜", callback_data="compress"),
                InlineKeyboardButton("🤸 استدارة | ROTATE  🤸", callback_data="rotate")
            ],[
                InlineKeyboardButton("✂️ تقسيم | SPLIT  ✂️", callback_data="split"),
                InlineKeyboardButton("🧬 دمج | MERGE  🧬", callback_data="merge")
            ],[
                InlineKeyboardButton("™️ ختم STAMP ™️", callback_data="stamp"),
                InlineKeyboardButton("✏️ إعادة تسمية |RENAME ✏️", callback_data="rename")
            ],[
                InlineKeyboardButton("📝 مسح ضوئي | OCR 📝", callback_data="ocr"),
                InlineKeyboardButton("🥷A4 FORMAT|تنسيق🥷", callback_data="format")
            ],[
                InlineKeyboardButton("🤐 ZIP 🤐", callback_data="zip"),
                InlineKeyboardButton("🎯 TAR 🎯", callback_data="tar")
            ],[     
                InlineKeyboardButton("🚫 أغلق | CLOSE  🚫", callback_data="closeALL")
            ]
        ]
    )


#--------------->
#--------> Config var.
#------------------->

UPDATE_CHANNEL=Config.UPDATE_CHANNEL
BANNED_USERS=Config.BANNED_USERS
ADMIN_ONLY=Config.ADMIN_ONLY
ADMINS=Config.ADMINS

#--------------->
#--------> REPLY TO DOCUMENTS/FILES
#------------------->

@ILovePDF.on_message(filters.private & filters.document & ~filters.edited)
async def documents(bot, message):
    try:
        global invite_link
        await message.reply_chat_action("typing")
        # CHECK USER IN CHANNEL (IF UPDATE_CHANNEL ADDED)
        if UPDATE_CHANNEL:
            try:
                await bot.get_chat_member(
                    str(UPDATE_CHANNEL), message.chat.id
                )
            except Exception:
                if invite_link == None:
                    invite_link=await bot.create_chat_invite_link(
                        int(UPDATE_CHANNEL)
                    )
                await bot.send_message(
                    message.chat.id,
                    forceSubMsg.format(
                        message.from_user.first_name, message.chat.id
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🌟(JOIN CHANNEL) أنظم في القناة🌟", url=invite_link.invite_link)
                            ],[
                                InlineKeyboardButton("تحديث | Refresh ♻️", callback_data="refresh")
                            ]
                        ]
                    )
                )
                return
        # CHECKS IF USER BANNED/ADMIN..
        if (message.chat.id in BANNED_USERS) or (
            (ADMIN_ONLY) and (message.chat.id not in ADMINS)
        ):
            await message.reply_text(
                UCantUse,
                reply_markup=button
            )
            return
        
        isPdfOrImg = message.document.file_name        # file name
        fileSize = message.document.file_size          # file size
        fileNm, fileExt = os.path.splitext(isPdfOrImg) # seperate name & extension
        
        # REPLY TO LAGE FILES/DOCUMENTS
        if MAX_FILE_SIZE and fileSize >= int(MAX_FILE_SIZE_IN_kiB):
            await message.reply_text(
                bigFileUnSupport.format(MAX_FILE_SIZE, MAX_FILE_SIZE), quote=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "💎webbot(موقع)💎",
                                url="https://electrical-engineer-cc40b.web.app/"
                            )
                        ]
                    ]
                )
            )
            return
        
        # IMAGE AS FILES (ADDS TO PDF FILE)
        elif fileExt.lower() in suprtedFile:
            try:
                imageDocReply = await message.reply_text(
                    "`تحميل صورتك (Downloading your Image) ..⏳`", quote=True
                )
                if not isinstance(PDF.get(message.chat.id), list):
                    PDF[message.chat.id]=[]
                await message.download(
                    f"{message.chat.id}/{message.chat.id}.jpg"
                )
                img = Image.open(
                    f"{message.chat.id}/{message.chat.id}.jpg"
                ).convert("RGB")
                PDF[message.chat.id].append(img)
                await imageDocReply.edit(
                    imageAdded.format(len(PDF[message.chat.id]))
                )
            except Exception as e:
                await imageDocReply.edit(
                    errorEditMsg.format(e)
                )
            
        # REPLY TO .PDF FILE EXTENSION
        elif fileExt.lower() == ".pdf":
            try:
                pdfMsgId = await message.reply_text(
                    "المعالجة (Processing)..⏳", quote=True
                )
                await asyncio.sleep(0.5)
                await pdfMsgId.edit(
                    text=pdfReplyMsg.format(
                        isPdfOrImg, await gSF(fileSize)
                    ),
                    reply_markup=pdfReply
                )
            except Exception:
                pass
        
        # FILES TO PDF (PYMUPDF/FITZ)
        elif fileExt.lower() in suprtedPdfFile:
            try:
                pdfMsgId = await message.reply_text(
                    "`تحميل ملفك (Downloading your file) ..⏳`", quote=True
                )
                await message.download(
                    f"{message.message_id}/{isPdfOrImg}"
                )
                await pdfMsgId.edit("`جاري العمل .. قد يستغرق بعض الوقت .. 💛\nWork in Progress.. It might take some time.. `")
                Document=fitz.open(
                    f"{message.message_id}/{isPdfOrImg}"
                )
                b=Document.convert_to_pdf()
                pdf=fitz.open("pdf", b)
                pdf.save(
                    f"{message.message_id}/{fileNm}.pdf",
                    garbage=4,
                    deflate=True,
                )
                pdf.close()
                await pdfMsgId.edit(
                    "`بدأ التحميل (Started Uploading)..`🏋️"
                )
                await bot.send_chat_action(
                    message.chat.id, "upload_document"
                )
                await message.reply_document(
                    file_name=f"{fileNm}.pdf",
                    document=open(f"{message.message_id}/{fileNm}.pdf", "rb"),
                    thumb=PDF_THUMBNAIL,
                    caption=f"` تم تحويل ملفك: {fileExt} إالى pdf` \n`Converted: {fileExt} to pdf`",
                    quote=True
                )
                await pdfMsgId.delete()
                shutil.rmtree(f"{message.message_id}")
                await asyncio.sleep(5)
                await bot.send_chat_action(
                    message.chat.id, "typing"
                )
                await bot.send_message(
                    message.chat.id, feedbackMsg,
                    disable_web_page_preview = True
                )
            except Exception as e:
                try:
                    shutil.rmtree(f"{message.message_id}")
                    await pdfMsgId.edit(
                        errorEditMsg.format(e)
                    )
                except Exception:
                    pass
        
        # FILES TO PDF (CONVERTAPI)
        elif fileExt.lower() in suprtedPdfFile2:
            if Config.CONVERT_API is None:
                pdfMsgId = await message.reply_text(
                    "`المالك نسيت إضافة ConvertAPI .. اتصل بالمالك 😒`",
                    quote=True
                )
                return
            else:
                try:
                    pdfMsgId = await message.reply_text(
                        "`تحميل ملفك (Downloading your file) ..⏳`", quote=True
                    )
                    await message.download(
                        f"{message.message_id}/{isPdfOrImg}"
                    )
                    await pdfMsgId.edit("`جاري العمل .. قد يستغرق بعض الوقت ..\nWork in Progress.. It might take some time.. `💛")
                    try:
                        convertapi.convert(
                            "pdf",
                            {
                                "File": f"{message.message_id}/{isPdfOrImg}"
                            },
                            from_format = fileExt[1:],
                        ).save_files(
                            f"{message.message_id}/{fileNm}.pdf"
                        )
                    except Exception:
                        try:
                            shutil.rmtree(f"{message.message_id}")
                            await pdfMsgId.edit(
                                "يصل حد ConvertAPI .. اتصل بالمالك"
                            )
                            return
                        except Exception:
                            pass
                    await bot.send_chat_action(
                        message.chat.id, "upload_document"
                    )
                    await message.reply_document(
                        file_name=f"{fileNm}.pdf",
                        document=open(f"{message.message_id}/{fileNm}.pdf", "rb"),
                        thumb=PDF_THUMBNAIL,
                        caption=f"` تم تحويل ملفك: {fileExt} إلى pdf` \n`Converted: {fileExt} to pdf`",
                        quote=True
                    )
                    await pdfMsgId.delete()
                    shutil.rmtree(f"{message.message_id}")
                    await asyncio.sleep(5)
                    await bot.send_chat_action(
                        message.chat.id, "typing"
                    )
                    await bot.send_message(
                        message.chat.id, feedbackMsg,
                        disable_web_page_preview=True
                    )
                except Exception:
                    pass
        
        # UNSUPPORTED FILES
        else:
            try:
                await message.reply_text(
                    "`ملف غير مدعوم (unsupported file)..🙄`", quote=True
                )
            except Exception:
                pass
    
    except Exception as e:
        print("plugins/dm/document : ", e)

#                                                                                  Telegram: @nabilanavab
