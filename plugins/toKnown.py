# fileName : plugins/toKnown.py
# copyright ©️ 2021 nabilanavab

from pyrogram.types import Message
from plugins.fileSize import get_size_format as gSF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

pdfInfoMsg = """`ماذا تريد أن أفعل بهذا الملف.؟ \n What shall i wanted to do with this file.?`
File name(اسم الملف) : `{}`
File Size(حجم الملف) : `{}`"""


# convert unknown to known page number msgs
async def toKnown(callbackQuery, number_of_pages):
    try:
        fileName = callbackQuery.message.reply_to_message.document.file_name
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        
        await callbackQuery.edit_message_text(
            pdfInfoMsg.format(
                fileName, await gSF(fileSize), number_of_pages
            ),
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("⭐️ معلومات|info", callback_data=f"KpdfInfo|{number_of_pages}"),
                        InlineKeyboardButton("🗳 معاينة | preview🗳", callback_data="Kpreview")
                    ],[
                        InlineKeyboardButton("🖼 الى صور | toImage 🖼", callback_data=f"KtoImage|{number_of_pages}"),
                        InlineKeyboardButton("✏️ الى نص totext✏️", callback_data=f"KtoText|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("🔐 تشفير | ENCRYPT 🔐", callback_data=f"Kencrypt|{number_of_pages}"),
                        InlineKeyboardButton("🔓فك تشفير | DECRYPT🔓", callback_data=f"notEncrypted")
                    ],[
                        InlineKeyboardButton("🗜 ضغط | COMPRESS 🗜", callback_data=f"Kcompress"),
                        InlineKeyboardButton("🤸 إستدارة 🤸", callback_data=f"Krotate|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("✂️ تقسيم | SPLIT  ✂️", callback_data=f"Ksplit|{number_of_pages}"),
                        InlineKeyboardButton("🧬 دمج | MERGE  🧬", callback_data="merge")
                    ],[
                        InlineKeyboardButton("™️ ختم STAMP ™️", callback_data=f"Kstamp|{number_of_pages}"),
                        InlineKeyboardButton("✏️ إعادة تسمية |RENAME ✏️", callback_data="rename")
                    ],[
                        InlineKeyboardButton("📝 مسح ضوئي | OCR 📝", callback_data=f"Kocr|{number_of_pages}"),
                        InlineKeyboardButton("🥷A4 FORMAT | تنسيق 🥷", callback_data=f"Kformat|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("🤐 ZIP 🤐", callback_data=f"Kzip|{number_of_pages}"),
                        InlineKeyboardButton("🎯 TAR 🎯", callback_data=f"Ktar|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("🚫 أغلق | CLOSE  🚫", callback_data="closeALL")
                    ]
                ]
            )
        )
    except Exception as e:
        print(f"plugins/toKnown: {e}")

#                                                                                  Telegram: @nabilanavab
