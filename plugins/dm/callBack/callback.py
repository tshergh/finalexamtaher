# fileName : plugins/dm/callBack/callback.py
# copyright ©️ 2021 nabilanavab

# LOGGING INFO: DEBUG
import logging
logger=logging.getLogger(__name__)
logging.basicConfig(
                   level=logging.DEBUG,
                   format="%(levelname)s:%(name)s:%(message)s" # %(asctime)s:
                   )

from pdf import PROCESS
from pyrogram import filters
from plugins.footer import header
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

#--------------->
#--------> PDF TO IMAGES (CB/BUTTON)
#------------------->

BTPM = filters.create(lambda _, __, query: query.data == "BTPM")
toImage = filters.create(lambda _, __, query: query.data == "toImage")
KBTPM = filters.create(lambda _, __, query: query.data.startswith("KBTPM|"))
KtoImage = filters.create(lambda _, __, query: query.data.startswith("KtoImage|"))

I = filters.create(lambda _, __, query: query.data == "I")
D = filters.create(lambda _, __, query: query.data == "D")
KI = filters.create(lambda _, __, query: query.data.startswith("KI|"))
KD = filters.create(lambda _, __, query: query.data.startswith("KD|"))

zIp = filters.create(lambda _, __, query: query.data == "zip")
KzIp = filters.create(lambda _, __, query: query.data.startswith("Kzip|"))

tAr = filters.create(lambda _, __, query: query.data == "tar")
KtAr = filters.create(lambda _, __, query: query.data.startswith("Ktar|"))

rotate = filters.create(lambda _, __, query: query.data == "rotate")
Krotate = filters.create(lambda _, __, query: query.data.startswith("Krotate|"))

toText = filters.create(lambda _, __, query: query.data == "toText")
KtoText = filters.create(lambda _, __, query: query.data.startswith("KtoText|"))

error = filters.create(lambda _, __, query: query.data == "error")
closeme = filters.create(lambda _, __, query: query.data == "closeme")
closeALL = filters.create(lambda _, __, query: query.data == "closeALL")
underDev = filters.create(lambda _, __, query: query.data == "underDev")
canceled = filters.create(lambda _, __, query: query.data == "canceled")
completed = filters.create(lambda _, __, query: query.data == "completed")
cancelP2I = filters.create(lambda _, __, query: query.data == "cancelP2I")
notEncrypted = filters.create(lambda _, __, query: query.data == "notEncrypted")


# Extract pgNo (with unknown pdf page number)
@ILovePDF.on_callback_query(I)
async def _I(bot, callbackQuery):
    try:
        if callbackQuery.message.chat.type != "private":
            return await callbackQuery.answer(
                                             "أرجوك حاول\nPlease Try in Bot Pm's 🤧"
                                             )
        await callbackQuery.answer()
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
            ))
    except Exception as e:
        logger.exception(
                        "CB/1:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

# Extract pgNo (with unknown pdf page number)
@ILovePDF.on_callback_query(D)
async def _D(bot, callbackQuery):
    try:
        if callbackQuery.message.chat.type != "private":
            return await callbackQuery.answer(
                                             " يوجد مشكلة  في البوتPlease Try in Bot Pm's 🤧"
                                             )
        await callbackQuery.answer()
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
      except Exception as e:
        logger.exception(
                        "CB/2:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

# Extract pgNo (with known pdf page number)
@ILovePDF.on_callback_query(KI)
async def _KI(bot, callbackQuery):
    try:
        if callbackQuery.message.chat.type != "private":
            return await callbackQuery.answer(
                                             "يوجد مشكلة  في البوتPlease Try in Bot Pm's 🤧"
                                             )
        await callbackQuery.answer()
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
                    ]]           
                    ))    
    except Exception as e:
        logger.exception(
                        "CB/3:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

# Extract pgNo (with known pdf page number)
@ILovePDF.on_callback_query(KD)
async def _KD(bot, callbackQuery):
    try:
        if callbackQuery.message.chat.type != "private":
            return await callbackQuery.answer(
                                             "يوجد مشكلة في بوت اعد محاولةPlease Try in Bot Pm's 🤧"
                                             )
        await callbackQuery.answer()
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
    except Exception as e:
        logger.exception(
                        "CB/4:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

# pdf to images (with unknown pdf page number)
@ILovePDF.on_callback_query(toImage)
async def _toImage(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        await callbackQuery.answer()
        await callbackQuery.edit_message_text(
                                             text = "__Send pdf Images as:__\n"
                                                    "__Total pages: unknown__ 😐",
                                             reply_markup = InlineKeyboardMarkup(
                                                 [[
                                                     InlineKeyboardButton("🖼 IMG صورة 🖼",
                                                                    callback_data="I"),
                                                     InlineKeyboardButton("📂 DOC ملف 📂",
                                                                    callback_data="D")
                                                 ],[
                                                     InlineKeyboardButton("🤐 ZIP مضغوط🤐",
                                                                  callback_data="zip"),
                                                     InlineKeyboardButton("🎯 TAR مضغوط🎯",
                                                                  callback_data="tar")
                                                 ],[
                                                     InlineKeyboardButton("« Back عودة «",
                                                                 callback_data="BTPM")
                                                 ]]
                                             ))
    except Exception as e:
        logger.exception(
                        "CB/5:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

# pdf to images (with known page Number)
@ILovePDF.on_callback_query(KtoImage)
async def _KtoImage(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        await callbackQuery.answer()
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
                                             text = f"__Send pdf Images as:__\n"
                                                    f"__Total pages: {number_of_pages}__ 😐",
                                             reply_markup = InlineKeyboardMarkup(
                                                 [[
                                                     InlineKeyboardButton("🖼 IMG صورة🖼️",
                                                     callback_data=f"KI|{number_of_pages}"),
                                                     InlineKeyboardButton("📂 DOC ملف📂",
                                                     callback_data=f"KD|{number_of_pages}")
                                                 ],[
                                                     InlineKeyboardButton("🤐 ZIP ملف🤐",
                                                     callback_data=f"Kzip|{number_of_pages}"),
                                                     InlineKeyboardButton("🎯 TAR ملف 🎯",
                                                     callback_data=f"Ktar|{number_of_pages}")
                                                 ],[
                                                     InlineKeyboardButton("« Back عودة «",
                                                     callback_data=f"KBTPM|{number_of_pages}")
                                                 ]]
                                             ))
    except Exception as e:
        logger.exception(
                        "CB/6:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

# back to pdf message (unknown page number)
@ILovePDF.on_callback_query(BTPM)
async def _BTPM(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        await callbackQuery.answer()
        fileName = callbackQuery.message.reply_to_message.document.file_name
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        
        await callbackQuery.edit_message_text(
                                              BTPMcb.format(
                                                           fileName,
                                                           await gSF(fileSize)
                                                           ),
                                              reply_markup=pdfReply
                                              )
    except Exception as e:
        logger.exception(
                        "CB/7:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

# Extract pgNo as Zip(with unknown pdf page number)
@ILovePDF.on_callback_query(tAr)
async def _tar(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        await callbackQuery.answer()
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
    except Exception as e:
        logger.exception(
                        "CB/8:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

# Extract pgNo as Zip(with known pdf page number)
@ILovePDF.on_callback_query(KtAr)
async def _Ktar(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        await callbackQuery.answer()
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
    except Exception as e:
        logger.exception(
                        "CB/9:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

# Extract pgNo as Zip(with unknown pdf page number)
@ILovePDF.on_callback_query(zIp)
async def _zip(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        await callbackQuery.answer()
        await callbackQuery.edit_message_text(
            "__Pdf - Img » مثل zip » الصفحات:           \nمجموع الصفحات: غير معروف _ 😐\n__Pdf - Img » as Doc » Pages:           \nTotal pages: unknown__ 😐",
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
    except Exception as e:
        logger.exception(
                        "CB/10:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

# Extract pgNo as Zip(with known pdf page number)
@ILovePDF.on_callback_query(KzIp)
async def _Kzip(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        await callbackQuery.answer()
        _, number_of_pages = callbackQuery.data.split("|")
        __Pdf - Img » مثل zip » الصفحات:           \nمجموع الصفحات: {number_of_pages}__ 🌟\n__Pdf - Img » as Doc » Pages:           \nTotal pages: {number_of_pages}__ 🌟",
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
     except Exception as e:
        logger.exception(
                        "CB/11:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

# back to pdf message (with known page Number)
@ILovePDF.on_callback_query(KBTPM)
async def _KBTPM(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        await callbackQuery.answer()
        fileName = callbackQuery.message.reply_to_message.document.file_name
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
                                             KBTPMcb.format(
                                                           fileName,
                                                           await gSF(fileSize),
                                                           number_of_pages
                                             ),
                                             reply_markup = InlineKeyboardMarkup(
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
                        InlineKeyboardButton("🚫 أغلق | CLOSE  🚫", callback_data="closeALL")
                    ]
                ]
            ))
        logger.exception(
                        "CB/12:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

# rotate PDF (unknown pg no)
@ILovePDF.on_callback_query(rotate)
async def _rotate(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        await callbackQuery.answer()
        await callbackQuery.edit_message_text(
                                             text ="__إجمالي الصفحات: غير معروف 😐 \nتدوير PDF في: __\n__Total Pages: Unknown 😐 \nRotate PDF in :__",
                                             reply_markup = InlineKeyboardMarkup(
                                                 [[
                                                     InlineKeyboardButton("90°",
                                                             callback_data="rot90"),
                                                     InlineKeyboardButton("180°",
                                                            callback_data="rot180")
                                                 ],[
                                                     InlineKeyboardButton("270°",
                                                            callback_data="rot270"),
                                                     InlineKeyboardButton("360°",
                                                            callback_data="rot360")
                                                 ],[
                                                     InlineKeyboardButton("« Back عودة «",
                                                              callback_data="BTPM")
                                                ]]
                                            ))
    except Exception as e:
        logger.exception(
                        "CB/13:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

# rotate PDF (only change in back button)
@ILovePDF.on_callback_query(Krotate)
async def _Krotate(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        await callbackQuery.answer()
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
                                             text = f"__اجمالي الصفحات Total Pages: {number_of_pages}__ 🌟\n"
                                                    f"__ تدوير ملف pdf في \nRotate PDF in:__",
                                             reply_markup = InlineKeyboardMarkup(
                                                 [[
                                                     InlineKeyboardButton("90°",
                                                            callback_data="rot90"),
                                                     InlineKeyboardButton("180°",
                                                           callback_data="rot180")
                                                 ],[
                                                     InlineKeyboardButton("270°",
                                                           callback_data="rot270"),
                                                     InlineKeyboardButton("360°",
                                                           callback_data="rot360")
                                                 ],[
                                                     InlineKeyboardButton("« Back عودة «",
                                                        callback_data=f"KBTPM|{number_of_pages}")
                                                 ]]
                                             ))
    except Exception as e:
        logger.exception(
                        "CB/14:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

# pdf to images (with unknown pdf page number)
@ILovePDF.on_callback_query(toText)
async def _toText(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        await callbackQuery.answer()
        await callbackQuery.edit_message_text(
                                             text = "__Pdf » Text__\n"
                                             "__Total Pages(عدد الصفحات): غير معروفunknown__ 😐\n"
                                             "__ الآن ، حدد التنسيق\nNow, Specify the format:__",
                                             reply_markup = InlineKeyboardMarkup(
                                                 [[
                                                     InlineKeyboardButton("Messages رسالة 📜",
                                                                       callback_data="M"),
                                                     InlineKeyboardButton("Txt file ملف نصي🧾",
                                                                       callback_data="T")
                                                 ],[
                                                     InlineKeyboardButton("Html نلف🌐",
                                                                       callback_data="H"),
                                                     InlineKeyboardButton("Json ملف🎀",
                                                                       callback_data="J")
                                                 ],[
                                                     InlineKeyboardButton("« Back عودة«",
                                                                    callback_data="BTPM")
                                                 ]]
                                             ))
    except Exception as e:
        logger.exception(
                        "CB/15:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

# pdf to images (with known page Number)
@ILovePDF.on_callback_query(KtoText)
async def _KtoText(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        await callbackQuery.answer()
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
                                             text = f"__Pdf » Text__\n"
                                                    f"__Total pages عدد صفحات: {number_of_pages}__ 🌟\n"
                                                    f"الآن ، حدد التنسيق\nNow, Specify the format:__",
                                             reply_markup = InlineKeyboardMarkup(
                                                 [[
                                                     InlineKeyboardButton("Messages رسالة📜",
                                                                     callback_data="KM"),
                                                     InlineKeyboardButton("Txt file ملف🧾",
                                                                     callback_data="KT")
                                                 ],[
                                                     InlineKeyboardButton("Html ملف🌐",
                                                                     callback_data="KH"),
                                                     InlineKeyboardButton("Json ملف🎀",
                                                                     callback_data="KJ")
                                                 ],[
                                                     InlineKeyboardButton("« Back عودة«",
                                                        callback_data=f"KBTPM|{number_of_pages}")
                                                 ]]
                                             ))
    except Exception as e:
        logger.exception(
                        "CB/16:CAUSES %(e)s ERRORخطا",
                        exc_info=True
                        )

@ILovePDF.on_callback_query(underDev)
async def _underDev(bot, callbackQuery):
    try:
        await callbackQuery.answer(
                                  "هذه الميزة قيد التطوير \nThis feature is Under Development ⛷️"
                                  )
    except Exception as e:
        logger.exception(
                        "CB/17:CAUSES %(e)s ERRORخطا ",
                        exc_info=True
                        )

# Error in Codec
@ILovePDF.on_callback_query(error)
async def _error(bot, callbackQuery):
    try:
        await callbackQuery.answer(
                                  "خطا في بوت. 😏"
                                  )
    except Exception as e:
        logger.exception(
                        "CB/18:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

# Download Cancel 
@ILovePDF.on_callback_query(closeme)
async def _closeme(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        try:
            await callbackQuery.message.delete()
        except Exception:
            pass
        await callbackQuery.answer(
                                  " العملية ملغاةProcess Canceled.. 😏"
                                  )
        PROCESS.remove(callbackQuery.message.chat.id)
    except Exception as e:
        logger.exception(
                        "CB/19:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

# File Not Encrypted callBack
@ILovePDF.on_callback_query(notEncrypted)
async def _notEncrypted(bot, callbackQuery):
    try:
        await callbackQuery.answer(
                                  "الملف غير مشفر\nFile Not Encrypted.. 👀"
                                  )
    except Exception as e:
        logger.exception(
                        "CB/20:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

# Close both Pdf Message + CB
@ILovePDF.on_callback_query(closeALL)
async def _closeALL(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        await callbackQuery.message.delete()
        if callbackQuery.message.chat.type == "private":
            await callbackQuery.message.reply_to_message.delete()
    except Exception as e:
        logger.exception(
                        "CB/21:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

# Cancel Pdf to Images, Images to Zip
@ILovePDF.on_callback_query(cancelP2I)
async def _cancelP2I(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        await callbackQuery.answer()
        await callbackQuery.message.edit_reply_markup(
             InlineKeyboardMarkup([[InlineKeyboardButton("💤 إلغاء CANCELLING.. 💤", callback_data = "nabilanavab")]])
        )
        PROCESS.remove(callbackQuery.from_user.id)
    except Exception as e:
        logger.exception(
                        "CB/22:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

@ILovePDF.on_callback_query(canceled)
async def _canceled(bot, callbackQuery):
    try:
        await callbackQuery.answer(
                                  "لا شيء رسمي حول هذا الموضوع.\nNothing Official About it.. 😅"
                                  )
    except Exception as e:
        logger.exception(
                        "CB/23:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

@ILovePDF.on_callback_query(completed)
async def _completed(bot, callbackQuery):
    try:
        await callbackQuery.answer(
                                  "🎉 اكتمل Completed.. 🏃"
                                  )
    except Exception as e:
        logger.exception(
                        "CB/24:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

#                                                                                             Telegram: @nabilanavab
