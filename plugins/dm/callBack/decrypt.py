# fileName : plugins/dm/callBack/encrypt.py
# copyright ©️ 2021 nabilanavab

import os
import time
import fitz
import shutil
from pdf import PROCESS
from pyromod import listen
from pyrogram import filters
from Configs.dm import Config
from plugins.progress import progress
from plugins.checkPdf import checkPdf
from pyrogram.types import ForceReply
from pyrogram import Client as ILovePDF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#--------------->
#--------> LOCAL VARIABLES
#------------------->

encryptedFileCaption = "Page Number(عدد الصفحات) : {}\nkey(مفتاح) 🔐 : ||{}||"

pdfInfoMsg = """`ماذا تريد أن أفعل بهذا الملف.؟ \n What shall i wanted to do with this file.?`

File name(اسم الملف) : `{}`
File Size(حجم الملف) : `{}`"""

PDF_THUMBNAIL = Config.PDF_THUMBNAIL

#--------------->
#--------> PDF ENCRYPTION
#------------------->

encrypts = ["encrypt", "Kencrypt|"]
encrypt = filters.create(lambda _, __, query: query.data.startswith(tuple(encrypts)))

@ILovePDF.on_callback_query(encrypt)
async def _encrypt(bot, callbackQuery):
    try:
        # CHECKS IF BOT DOING ANY WORK
        if callbackQuery.message.chat.id in PROCESS:
            await callbackQuery.answer(
                "جاري العمل Work in progress .. ⏳",
            )
            return
        # CALLBACK DATA
        data = callbackQuery.data
        # IF PDF PAGE MORE THAN 5000 (PROCESS CANCEL)
        if data[0] == "K":
            _, number_of_pages = callbackQuery.data.split("|")
            if int(number_of_pages) >= 5000:
                await bot.answer_callback_query(
                    callbackQuery.id,
                    text="`Please send a pdf file less than 5000 pages\nالرجاء إرسال ملف pdf أقل من 5000 صفحة` 🙄",
                    show_alert=True,
                    cache_time=0
                )
                return
        # ADDED TO PROCESS
        PROCESS.append(callbackQuery.message.chat.id)
        # PYROMOD (PASSWORD REQUEST)
        password=await bot.ask(
            chat_id=callbackQuery.message.chat.id,
            reply_to_message_id = callbackQuery.message.message_id,
            text="__PDF Encryption »\nNow, please enter the password :__\n\n/exit __to cancel__\n__فك تشفير PDF »\nالآن ، الرجاء إدخال كلمة المرور :__\n\n/exit __للإلغاء__",
            filters=filters.text,
            reply_markup=ForceReply(True)
        )
        # CANCEL DECRYPTION PROCESS IF MESSAGE == /exit
        if password.text == "/exit":
            await password.reply(
                "`ألغيت العملية process canceled ..`😏"
            )
            PROCESS.remove(callbackQuery.message.chat.id)
            return
        # DOWNLOAD MESSAGE
        downloadMessage=await callbackQuery.message.reply_text(
            "`قم بتنزيل ملف pdf Downloading your 📕..` ⏳", quote=True
        )
        file_id=callbackQuery.message.reply_to_message.document.file_id
        input_file=f"{callbackQuery.message.message_id}/pdf.pdf"
        output_pdf=f"{callbackQuery.message.message_id}/Encrypted.pdf"
        fileSize=callbackQuery.message.reply_to_message.document.file_size
        fileNm=callbackQuery.message.reply_to_message.document.file_name
        fileNm, fileExt=os.path.splitext(fileNm)        # seperates name & extension
        # STARTED DOWNLOADING
        c_time=time.time()
        downloadLoc=await bot.download_media(
            message=file_id,
            file_name=input_file,
            progress=progress,
            progress_args=(
                fileSize,
                downloadMessage,
                c_time
            )
        )
        # CHECKS PDF DOWNLOAD OR NOT
        if downloadLoc is None:
            PROCESS.remove(callbackQuery.message.chat.id)
            return
        await downloadMessage.edit(
            "`بدأ فك التشفير.. 🔐\nit might take some time..💤\nقد يستغرق الأمر بعض الوقت ..`",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🚫Cancelإلغاء",
                            callback_data="closeme"
                        )
                    ]
                ]
            )
        )
        if data[0] != "K":
            checked = await checkPdf(input_file, callbackQuery)
            if not(checked == "pass"):
                await downloadMessage.delete()
                return
        # ENCRYPTION USING STRONG ALGORITHM (fitz/pymuPdf)
        with fitz.open(input_file) as encrptPdf:
            number_of_pages=encrptPdf.pageCount
            if int(number_of_pages) <= 5000:
                encrptPdf.save(
                    output_pdf,
                    encryption=fitz.PDF_ENCRYPT_AES_256,
                    owner_pw="nabil",
                    user_pw=f"{password.text}",
                    permissions=int(
                        fitz.PDF_PERM_ACCESSIBILITY |
                        fitz.PDF_PERM_PRINT |
                        fitz.PDF_PERM_COPY |
                        fitz.PDF_PERM_ANNOTATE
                    )
                )
            else:
                downloadMessage.edit(
                    "__Encryption Error:\nplease send me a file less than 5000 pages__ 🥱\n__ خطأ في التشفير: \ n من فضلك أرسل لي ملفًا أقل من 5000 صفحة__ 🥱"
                )
                PROCESS.remove(callbackQuery.message.chat.id)
                shutil.rmtree(f"{callbackQuery.message.message_id}")
                return
        if callbackQuery.message.chat.id not in PROCESS:
            shutil.rmtree(f'{callbackQuery.message.message_id}')
            return
        await downloadMessage.edit(
            "`بدأ التحميل (Started Uploading)..`🏋️"
        )
        await bot.send_chat_action(
            callbackQuery.message.chat.id, "upload_document"
        )
        # SEND ENCRYPTED PDF (AS REPLY)
        await callbackQuery.message.reply_document(
            file_name=f"{fileNm}.pdf",
            document=open(output_pdf, "rb"),
            thumb=PDF_THUMBNAIL,
            caption=encryptedFileCaption.format(
                number_of_pages, password.text
            ),
            quote=True
        )
        await downloadMessage.delete()
        shutil.rmtree(f"{callbackQuery.message.message_id}")
        PROCESS.remove(callbackQuery.message.chat.id)
    except Exception as e:
        try:
            print("Encrypt: ",e)
            PROCESS.remove(callbackQuery.message.chat.id)
            shutil.rmtree(f"{callbackQuery.message.message_id}")
        except Exception:
            pass

#                                                                                  Telegram: @nabilanavab
