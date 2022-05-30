# fileName : plugins/dm/callBack/asImgOrDoc.py
# copyright ©️ 2021 nabilanavab




from pyrogram import filters
from pyrogram import Client as ILovePDF
from plugins.fileSize import get_size_format as gSF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup




#--------------->
#--------> LOCAL VARIABLES
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
                InlineKeyboardButton("🥷A4 FORMAT | تنسيق 🥷", callback_data="format")
            ],[
                InlineKeyboardButton("🤐 ZIP 🤐", callback_data="zip"),
                InlineKeyboardButton("🎯 TAR 🎯", callback_data="tar")
            ],[
                InlineKeyboardButton("🚫 أغلق | CLOSE  🚫", callback_data="closeALL")
            ]
        ]
    )

BTPMcb = """`ماذا تريد أن أفعل بهذا الملف.؟ \n What shall i wanted to do with this file.?`

File name(اسم الملف) : `{}`
File Size(حجم الملف) : `{}`"""

KBTPMcb = """`ماذا تريد أن أفعل بهذا الملف.؟ \n What shall i wanted to do with this file.?`

File name(اسم الملف) : `{}`
File Size(حجم الملف) : `{}`

`Number of Pages(عدد الصفحات): {}`📓
"""

"""
______VARIABLES______

I : as image
D : as document
K : pgNo known
A : Extract All
R : Extract Range
S : Extract Single page
BTPM : back to pdf message
KBTPM : back to pdf message (known pages)
______المتغيرات______

I: كصورة
D: كوثيقة
K: صغير معروف
A: استخراج الكل
R: استخراج المدى
S: استخراج صفحة واحدة
BTPM: العودة Back إلى رسالة pdf
KBTPM: العودة Back إلى رسالة pdf (الصفحات المعروفة)
"""

BTPM = filters.create(lambda _, __, query: query.data == "BTPM")
toImage = filters.create(lambda _, __, query: query.data == "toImage")
KBTPM = filters.create(lambda _, __, query: query.data.startswith("KBTPM|"))
KtoImage = filters.create(lambda _, __, query: query.data.startswith("KtoImage|"))

I = filters.create(lambda _, __, query: query.data == "I")
D = filters.create(lambda _, __, query: query.data == "D")
KI = filters.create(lambda _, __, query: query.data.startswith("KI|"))
KD = filters.create(lambda _, __, query: query.data.startswith("KD|"))


# Extract pgNo (with unknown pdf page number)
@ILovePDF.on_callback_query(I)
async def _I(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            "__Pdf - Img » مثل Img »الصفحات:           \nمجموع الصفحات: غير معروف _ 😐\n__Pdf - Img » as Img » Pages:           \nTotal pages: unknown__ 😐",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🙄 استخراج الكل  Extract All ",
                            callback_data="IA"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🙂ضمن النطاق With In Range  ",
                            callback_data="IR"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🌝صفحة واحدة Single Page",
                            callback_data="IS"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "« عودة Back «",
                            callback_data="toImage"
                        )
                    ]
                ]
            )
        )
    except Exception:
        pass


# Extract pgNo (with unknown pdf page number)
@ILovePDF.on_callback_query(D)
async def _D(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            "__Pdf - Img » مثل Doc » الصفحات:           \nمجموع الصفحات: غير معروف _ 😐\n__Pdf - Img » as Doc » Pages:           \nTotal pages: unknown__ 😐",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🙄 استخراج الكل  Extract All ",
                            callback_data="DA"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🙂ضمن النطاق With In Range  ",
                            callback_data="DR"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🌝صفحة واحدة Single Page",
                            callback_data="DS"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "« عودة Back «",
                            callback_data="toImage"
                        )
                    ]
                ]
            )
        )
    except Exception:
        pass


# Extract pgNo (with known pdf page number)
@ILovePDF.on_callback_query(KI)
async def _KI(bot, callbackQuery):
    try:
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            f"__Pdf - Img » مثل Img » الصفحات:           \nمجموع الصفحات: {number_of_pages}__ 🌟\n__Pdf - Img » as Img » Pages:           \nTotal pages: {number_of_pages}__ 🌟",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🙄 استخراج الكل  Extract All ",
                            callback_data=f"KIA|{number_of_pages}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🙂ضمن النطاق With In Range  ",
                            callback_data=f"KIR|{number_of_pages}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🌝صفحة واحدة Single Page",
                            callback_data=f"KIS|{number_of_pages}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "« عودة Back «",
                            callback_data=f"KtoImage|{number_of_pages}"
                        )
                    ]
                ]
            )
        )
    except Exception:
        pass


# Extract pgNo (with known pdf page number)
@ILovePDF.on_callback_query(KD)
async def _KD(bot, callbackQuery):
    try:
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            f"__Pdf - Img » مثل Doc » الصفحات:           \nمجموع الصفحات: {number_of_pages}__ 🌟\n__Pdf - Img » as Doc » Pages:           \nTotal pages: {number_of_pages}__ 🌟",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🙄 استخراج الكل  Extract All ",
                            callback_data=f"KDA|{number_of_pages}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🙂ضمن النطاق With In Range  ",
                            callback_data=f"KDR|{number_of_pages}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🌝صفحة واحدة Single Page",
                            callback_data=f"KDS|{number_of_pages}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "« عودة Back «",
                            callback_data=f"KtoImage|{number_of_pages}"
                        )
                    ]
                ]
            )
        )
    except Exception:
        pass

# pdf to images (with unknown pdf page number)
@ILovePDF.on_callback_query(toImage)
async def _toImage(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            "__ إرسال صور بتنسيق pdf:           \nمجموع الصفحات: غير معروف _ 😐\n__Send pdf Images as:           \nTotal pages: unknown__ 😐",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🖼صور  Images ",
                            callback_data="I"
                        ),
                        InlineKeyboardButton(
                            "📂مستندات Documents ",
                            callback_data="D"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "« عودة Back «",
                            callback_data="BTPM"
                        )
                    ]
                ]
            )
        )
    except Exception:
        pass


# pdf to images (with known page Number)
@ILovePDF.on_callback_query(KtoImage)
async def _KtoImage(bot, callbackQuery):
    try:
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            f"__ إرسال صور بتنسيق pdf:           \nمجموع الصفحات: {number_of_pages}__ 😐\n__Send pdf Images as:           \nTotal pages: {number_of_pages}__ 😐",
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🖼️ Images صور",
                            callback_data=f"KI|{number_of_pages}"
                        ),
                        InlineKeyboardButton(
                            "📂مستندات Documents ",
                            callback_data=f"KD|{number_of_pages}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "عودة Back «",
                            callback_data=f"KBTPM|{number_of_pages}"
                        )
                    ]
                ]
            )
        )
    except Exception:
        pass


# back to pdf message (unknown page number)
@ILovePDF.on_callback_query(BTPM)
async def _BTPM(bot, callbackQuery):
    try:
        fileName=callbackQuery.message.reply_to_message.document.file_name
        fileSize=callbackQuery.message.reply_to_message.document.file_size
        
        await callbackQuery.edit_message_text(
            BTPMcb.format(
                fileName, await gSF(fileSize)
            ),
            reply_markup = pdfReply
        )
    except Exception:
        pass


# back to pdf message (with known page Number)
@ILovePDF.on_callback_query(KBTPM)
async def _KBTPM(bot, callbackQuery):
    try:
        fileName = callbackQuery.message.reply_to_message.document.file_name
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            KBTPMcb.format(
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
    except Exception:
        pass

#                                                                                             Telegram: @nabilanavab
