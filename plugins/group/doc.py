# fileName : plugins/group/doc.py
# copyright ©️ 2021 nabilanavab

# LOGGING INFO: DEBUG
import logging
logger=logging.getLogger(__name__)
logging.basicConfig(
                   level=logging.DEBUG,
                   format="%(levelname)s:%(name)s:%(message)s" # %(asctime)s:
                   )

import os
import fitz
import shutil
import asyncio
import convertapi
from pdf import myID
from PIL import Image
from time import sleep
from pdf import PROCESS
from pyrogram import filters
from configs.dm import Config
from pdf import PDF, invite_link
from plugins.thumbName import (
                              thumbName,
                              formatThumb
                              )
from configs.group import groupConfig
from pyrogram import Client as ILovePDF
from plugins.footer import footer, header
from plugins.fileSize import get_size_format as gSF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from configs.images import WELCOME_PIC, BANNED_PIC, BIG_FILE, PDF_THUMBNAIL

if Config.CONVERT_API is not None:
    convertapi.api_secret = Config.CONVERT_API

if Config.MAX_FILE_SIZE:
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE"))
    MAX_FILE_SIZE_IN_kiB = MAX_FILE_SIZE * (10 **6 )
else:
    MAX_FILE_SIZE = False

#--------------->
#--------> FILES TO PDF [SUPPORTED CODECS]
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
    ".dotx", ".log", ".mpp", ".mpt",
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

forceSubMsg ="""مرحبا [{}](tg://user?id={}) 🤚🏻..!!
يجب عليك إنضمام الى هذه القناة لكي تستطيع استخدام البوت اشترك في هذه القناة  :
👇👇👇👇👇👇
 @i2pdfbotchannel
وبعدها ارجع للبوت واضغط هذا الامر /start او من ازار اضغط تحديث
لمتابعة كافة تحديثات البوت

You must join a channel in order to use the bot. Subscribe to this channel: 
👇👇👇👇
 @i2pdfbotchannel
Then go back to the bot and press this command / start, or from the buttons, press update
To follow all bot updates`
"""


foolRefresh = "انظم اولا join frist"

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
UPDATE_CHANNEL = Config.UPDATE_CHANNEL

ONLY_GROUP_ADMIN = groupConfig.ONLY_GROUP_ADMIN

#--------------->
#--------> REPLY TO group DOCUMENTS/FILES/IMAGES
#------------------->

@ILovePDF.on_message(
                    filters.group &
                    ~filters.edited &
                    filters.incoming &
                    filters.command(
                          ["analyse", "check",
                             "nabilanavab"]
                                   )
                    )
async def documents(bot, message):
    try:
        global invite_link, myID
        if not myID:
            myID = await bot.get_me()
        await message.reply_chat_action(
                                       "typing"
                                       )
        # CHECK USER IN CHANNEL (IF UPDATE_CHANNEL ADDED)
        if UPDATE_CHANNEL:
            try:
                userStatus = await bot.get_chat_member(
                                                      str(UPDATE_CHANNEL),
                                                      message.from_user.id
                                                      )
                # IF USER BANNED FROM CHANNEL
                if userStatus.status == 'banned':
                     return await message.reply_photo(
                                              photo = BANNED_PIC,
                                              caption = "لا يمكنك استخدام هذا الروبوت لبعض الأسباب\nFor Some Reason You Can't Use This Bot"
                                                        "\nاتصل بمالك البوت 🤐\nContact Bot Owner 🤐",
                                              reply_markup = InlineKeyboardMarkup(
                                                    [[InlineKeyboardButton("المالك Owner 🎊",
                                                      url="https://t.me/ta_ja199")]]
                                              ))
            except Exception:
                if invite_link == None:
                    invite_link = await bot.create_chat_invite_link(
                                                                   int(UPDATE_CHANNEL)
                                                                   )
                return await message.reply_photo(
                                    photo = WELCOME_PIC,
                                    caption = forceSubMsg.format(
                                            message.from_user.first_name, message.from_user.id
                                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🌟(JOIN CHANNEL) أنظم في القناة🌟", url=invite_link.invite_link)
                            ],[
                                InlineKeyboardButton("تحديث | Refresh ♻️", callback_data="refresh")
                            ]]
                    ))
        
        if message.from_user.id in PROCESS:
            return await message.reply_to_message.reply(
                                                       "العمل قيد التقدم ..WORK IN PROGRESS.. 🙇"
                                                       "\nأعد المحاولة لاحقًا ..Try Again Later.. 😉"
                                                       "\n\nالطلب من(Request from): {}".format(message.from_user.mention),
                                                       quote = True,
                                                       reply_markup = InlineKeyboardMarkup(
                                                             [[
                                                                 InlineKeyboardButton(
                                                                          "♻️ Try Again حاول مجددا♻️",
                                                                 callback_data = "newGrupDoc")
                                                             ]]
                                                       ))
        
        status = await bot.get_chat_member(
                                           message.chat.id,
                                           myID.id
                                           )
        if status.status not in ["administrator", "creator"]:
            return await message.reply(
                                      "بسبب بعض حدود تيليكرام ..Due to Some Telegram Limits.."
                                      "لا يمكنني العمل إلا كمسؤول I can only work as an admin\n\n"
                                      "__من فضلك قم بترقيتي كمسؤول Please promote me as admin__ ☺️",
                                      quote = True
                                      )
        
        if (not message.reply_to_message) or not(message.reply_to_message.document or message.reply_to_message.photo):
            return await message.reply(
                                      "الرجاء الرد على مستند أو صورة ..🤧\nPlease Reply to a Document or an Image..🤧",
                                      quote = True
                                      )
        
        if message.from_user.id in Config.ADMINS:
            pass
        else:
            isAdmin = await bot.get_chat_member(
                                         message.chat.id,
                                         message.from_user.id
                                         )
            if ONLY_GROUP_ADMIN and isAdmin.status not in ["administrator", "creator"]:
                return await message.reply(
                                          "يمكن فقط لمسؤولي المجموعة استخدام هذا الروبوت\nOnly Group Admins Can Use This Bot\n"
                                          "آخر تعال إلى رئيس بلدي Else Come to my Pm 😋", quote = True
                                          )
            elif isAdmin.status not in ["administrator", "creator"]:
                if message.from_user.id != message.reply_to_message.from_user.id:
                    return await message.reply(
                                              "الرجاء الرد على رسالتك .. 🙂\nPlease Reply to Your Message.. 🙂"
                                              )
        
        if message.reply_to_message.photo:
            imageReply = await message.reply_to_message.reply_text(
                                             "`تحميل صورتك .. Downloading your Image..` 📥",
                                             quote = True
                                             )
            if not isinstance(PDF.get(message.chat.id), list):
                PDF[message.chat.id] = []
            await message.reply_to_message.download(
                                     f"{message.chat.id}/{message.chat.id}.jpg"
                                     )
            img = Image.open(
                f"{message.chat.id}/{message.chat.id}.jpg"
            ).convert("RGB")
            PDF[message.chat.id].append(img)
            return await imageReply.edit(
                                 imageAdded.format(
                                                  len(PDF[message.chat.id])
                                                  )
                                 )
        
        isPdfOrImg = message.reply_to_message.document.file_name        # file name
        fileSize = message.reply_to_message.document.file_size          # file size
        fileNm, fileExt = os.path.splitext(isPdfOrImg) # seperate name & extension
        
        # REPLY TO LAGE FILES/DOCUMENTS
        if MAX_FILE_SIZE and fileSize >= int(MAX_FILE_SIZE_IN_kiB):
            await message.reply_to_message.reply_photo(
                                     photo = BIG_FILE,
                                     caption = bigFileUnSupport.format(
                                             MAX_FILE_SIZE, MAX_FILE_SIZE
                                     ),
                                     reply_markup = InlineKeyboardMarkup(
                                          [[
                                               InlineKeyboardButton("💎 channel bot 💎",
                                                     url = "https://t.me/i2pdfbotchannel")
                                           ]]
                                    ))
            return
        
        # IMAGE AS FILES (ADDS TO PDF FILE)
        elif fileExt.lower() in suprtedFile:
            try:
                imageDocReply = await message.reply_to_message.reply_text(
                                                        "`تنزيل صورتك Downloading your Image.. 📥`",
                                                        quote = True
                                                        )
                if not isinstance(PDF.get(message.chat.id), list):
                    PDF[message.chat.id] = []
                await message.reply_to_message.download(
                                      f"{message.chat.id}/{message.chat.id}.jpg"
                                      )
                img = Image.open(
                                f"{message.chat.id}/{message.chat.id}.jpg"
                                ).convert("RGB")
                PDF[message.chat.id].append(img)
                await imageDocReply.edit(
                                        imageAdded.format(
                                                         len(PDF[message.chat.id])
                                                         )
                                        )
            except Exception as e:
                await imageDocReply.edit(
                                        errorEditMsg.format(e)
                                        )
        
        # REPLY TO .PDF FILE EXTENSION
        elif fileExt.lower() == ".pdf":
            pdfMsgId = await message.reply_to_message.reply_text(
                                                                "⚙️ يتم المعالجة PROCESSING.",
                                                                quote = True
                                                                )
            await asyncio.sleep(0.5)
            await pdfMsgId.edit("⚙️يتم المعالجة PROCESSING..")
            await asyncio.sleep(0.5)
            await pdfMsgId.edit("⚙️ يتم المعالجة PROCESSING...")
            await asyncio.sleep(0.5)
            await pdfMsgId.edit(
                               text = pdfReplyMsg.format(
                                                        isPdfOrImg,
                                                        await gSF(fileSize)
                               ),
                               reply_markup = pdfReply
                               )
            await footer(message, message.reply_to_message)
        
        # FILES TO PDF (PYMUPDF/FITZ)
        elif fileExt.lower() in suprtedPdfFile:
            try:
                PROCESS.append(message.from_user.id)
                pdfMsgId = await message.reply_to_message.reply_text(
                                                   "`جارٍ تنزيل ملفك ..Downloading your file.. 📥`",
                                                   quote = True
                                                   )
                await message.reply_to_message.download(
                                      f"{message.message_id}/{isPdfOrImg}"
                                      )
                await pdfMsgId.edit(
                                   "`جاري العمل .. قد يستغرق بعض الوقت ..\nWork in Progress.. It might take some time.. 💛`"
                                   )
                Document = fitz.open(
                                    f"{message.message_id}/{isPdfOrImg}"
                                    )
                b = Document.convert_to_pdf()
                pdf = fitz.open("pdf", b)
                pdf.save(
                        f"{message.message_id}/{fileNm}.pdf",
                        garbage = 4,
                        deflate = True,
                        )
                pdf.close()
                
                # Getting thumbnail
                thumbnail, fileName = await thumbName(message, isPdfOrImg)
                if PDF_THUMBNAIL != thumbnail:
                    await bot.download_media(
                                            message = thumbnail,
                                            file_name = f"{message.message_id}/thumbnail.jpeg"
                                            )
                    thumbnail = await formatThumb(f"{message.message_id}/thumbnail.jpeg")
                
                await pdfMsgId.edit(
                                   "`بدأ التحميل ..Started Uploading..` 📤"
                                   )
                await message.reply_chat_action(
                                               "upload_document"
                                               )
                logFile = await message.reply_to_message.reply_document(
                                            file_name = f"{fileName}.pdf",
                                            document = open(f"{message.message_id}/{fileNm}.pdf", "rb"),
                                            thumb = thumbnail,
                                            caption = f"`Converted: {fileExt} to pdf`",
                                            quote = True
                                            )
                await pdfMsgId.delete(); PROCESS.remove(message.from_user.id)
                shutil.rmtree(f"{message.message_id}")
                await footer(message, logFile)
            except Exception as e:
                try:
                    await pdfMsgId.edit(
                                       errorEditMsg.format(e)
                                       )
                    shutil.rmtree(f"{message.message_id}")
                    PROCESS.remove(message.from_user.id)
                except Exception:
                    pass
        
        # FILES TO PDF (CONVERTAPI)
        elif fileExt.lower() in suprtedPdfFile2:
            if Config.CONVERT_API is None:
                pdfMsgId = await message.reply_text(
                                                   "`المالك نسيت إضافة ConvertAPI .. اتصل بالمالك 😒Owner Forgot to add ConvertAPI.. contact Owner 😒`",
                                                   quote = True
                                                   )
                return 
            else:
                try:
                    PROCESS.append(message.from_user.id)
                    pdfMsgId = await message.reply_to_message.reply_text(
                                                       "`جارٍ تنزيل ملفك ..Downloading your file.. 📥`",
                                                       quote = True
                                                       )
                    await message.reply_to_message.download(
                                          f"{message.message_id}/{isPdfOrImg}"
                                          )
                    await pdfMsgId.edit(
                                       "`جاري العمل .. قد يستغرق بعض الوقت ..\nWork in Progress.. It might take some time.. `💛"
                                       )
                    try:
                        convertapi.convert(
                                          "pdf",
                                              {
                                                  "File": f"{message.message_id}/{isPdfOrImg}"
                                              },
                                              from_format=fileExt[1:],
                                          ).save_files(
                                              f"{message.message_id}/{fileNm}.pdf"
                                          )
                    except Exception:
                        try:
                            shutil.rmtree(f"{message.message_id}")
                            await pdfMsgId.edit(
                                               "يصل حد ConvertAPI .. اتصل بالمالك ConvertAPI limit reaches.. contact Owner"
                                               )
                            PROCESS.remove(message.from_user.id)
                            return
                        except Exception: pass
                    
                    # Getting thumbnail
                    thumbnail, fileName = await thumbName(message, isPdfOrImg)
                    if PDF_THUMBNAIL != thumbnail:
                        await bot.download_media(
                                                message = thumbnail,
                                                file_name = f"{message.message_id}/thumbnail.jpeg"
                                                )
                        thumbnail = await formatThumb(f"{message.message_id}/thumbnail.jpeg")
                    await pdfMsgId.edit(
                                       "`بدأ التحميل ..Started Uploading..` 📤"
                                       )
                    await message.reply_chat_action(
                                                   "upload_document"
                                                   )
                    logFile = await message.reply_to_message.reply_document(
                                                file_name = f"{fileNm}.pdf",
                                                document = open(f"{message.message_id}/{fileNm}.pdf", "rb"),
                                                thumb = PDF_THUMBNAIL,
                                                caption = f"`Converted: {fileExt} to pdf`",
                                                quote = True
                                                )
                    await pdfMsgId.delete(); PROCESS.remove(message.from_user.id)
                    shutil.rmtree(f"{message.message_id}")
                    await footer(message, logFile)
                except Exception:
                    PROCESS.remove(message.from_user.id)
                    pass
        
        # UNSUPPORTED FILES
        else:
            try:
                await message.reply_to_message.reply_text(
                                        "`unsupported file..🙄`",
                                        quote = True
                                        )
            except Exception:
                pass
    except Exception as e:
        logger.exception(
                        "»»GROUP:DOC:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

newGrupDoc = filters.create(lambda _, __, query: query.data == "newGrupDoc")
refreshAnalyse = filters.create(lambda _, __, query: query.data == "refreshAnalyse")

@ILovePDF.on_callback_query(refreshAnalyse)
async def _refreshGrup(bot, callbackQuery):
    try:
        if callbackQuery.from_user.id != callbackQuery.message.reply_to_message.from_user.id:
            return await callbackQuery.answer("الرسالة ليست لك ..😏\nMessage Not For You.. 😏")
        
        # CHECK USER IN CHANNEL (REFRESH CALLBACK)
        userStatus = await bot.get_chat_member(
                                              str(UPDATE_CHANNEL),
                                              callbackQuery.from_user.id
                                              )
        await callbackQuery.answer()
        # IF USER NOT MEMBER (ERROR FROM TG, EXECUTE EXCEPTION)
        if callbackQuery.data == "refreshAnalyse":
            messageId = callbackQuery.message.reply_to_message
            await callbackQuery.message.delete()
            return await analyse(bot, messageId)
    except Exception as e:
        try:
            logger.exception(
                        "»»GROUP:DOCUMENTS:CAUSES %(e)s ERROR خطا",
                        exc_info=True
                        )
            # IF NOT USER ALERT MESSAGE (AFTER CALLBACK)
            await bot.answer_callback_query(
                                           callbackQuery.id,
                                           text = foolRefresh,
                                           show_alert = True,
                                           cache_time = 0
                                           )
        except Exception: pass

@ILovePDF.on_callback_query(newGrupDoc)
async def _asDoc(bot, callbackQuery):
    try:
        if callbackQuery.from_user.id in PROCESS:
            return await callbackQuery.answer(
                                             "العمل في التقدمWORK IN PROGRESS..🙇"
                                             )
        await callbackQuery.answer(
                                  "⚙️ المعالجة PROCESSING.."
                                  )
        if await header(bot, callbackQuery):
            return
        await callbackQuery.message.delete()
        await documents(
                       bot, callbackQuery.message.reply_to_message
                       )
    except Exception:
        logger.exception(
                        "»»GROUP:DOC:CAUSES %(e)s ERROR حطا",
                        exc_info=True
                        )

#                                                                                  Telegram: @nabilanavab
