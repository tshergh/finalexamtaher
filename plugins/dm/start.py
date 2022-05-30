# fileName : plugins/dm/start.py
# copyright ©️ 2021 nabilanavab




from pdf import invite_link
from pyrogram import filters
from Configs.dm import Config
from pyrogram import Client as ILovePDF
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineKeyboardMarkup





#--------------->
#--------> LOCAL VARIABLES
#------------------->

welcomeMsg = """مرحبا 𝓗𝓲 [{}](tg://user?id={})..!!🌝💛
سيساعدك هذا البوت على القيام بأشياء كثيرة باستخدام ملفات pdf  📗
𝕋𝕙𝕚𝕤 𝕓𝕠𝕥 𝕨𝕚𝕝𝕝 𝕙𝕖𝕝𝕡 𝕪𝕠𝕦 𝕕𝕠 𝕒 𝕝𝕠𝕥 𝕠𝕗 𝕥𝕙𝕚𝕟𝕘𝕤 𝕨𝕚𝕥𝕙 𝕡𝕕𝕗 𝕗𝕚𝕝𝕖𝕤 
بعض الميزات الرئيسية هي:
◍ `تحويل الصور إلى PDF`
◍ `تحويل الملفات إلى pdf`
◍ `للمزيد من معلومات اضغط : استكشاف البوت`
Some of the main features are:
◍ `Convert images to PDF`
◍ `Convert files to pdf`
◍ `For more information, click: Explore Bot`


 𝔇𝔢𝔳&𝔢𝔫𝔤: @ta_ja199 🧑🏻‍💻
 
[feedback|اكتب تعليقًا 📋 ](https://t.me/engineering_electrical9/719?comment=1)"""


UCantUse = "لا يمكنك استخدام هذا الروبوت لبعض الأسباب 🛑"


forceSubMsg = """مرحبا [{}](tg://user?id={}) 🤚🏻..!!
يجب عليك انضمام الى قناة لكي تستطيع استخدام البوت اشترك في هذه القناة  :👉👉 @i2pdfbotchannel
وبعدها ارجع للبوت واضغط هذا الامر /start او من ازار اضغط تحديث
لمتابعة كافة تحديثات البوت

You must join a channel in order to use the bot. Subscribe to this channel: 👉👉 @i2pdfbotchannel
Then go back to the bot and press this command / start, or from the buttons, press update
To follow all bot updates`
"""
foolRefresh = "يجيب عليك إشتراك أولا في قناة بعدها إضغط تحديث 😁 \n You must first subscribe to a channel, then click Refresh😁"

aboutDev = """🤖𝑨𝑩𝑶𝑼𝑻 𝑩𝑶𝑻 (حول البوت)
Name(أسم): pdf pro | تعديل على pdf
Username(معرف): @i2pdfbot
Version(إلإصدار): 2.5
Channel Bot: @i2pdfbotchannel 


👤 Developer(المطور)
Name(أسم ): 𝗧𝗔𝗛𝗘𝗥 𝗔𝗟𝗡𝗢𝗢𝗥𝗜
Username(معرف): @ta_ja199 
Instagram(انستا)🎛:[Click here | إضغط  هنا](https://www.instagram.com/ta_9_ja/)
Website(موقع)🌐:موسوعة المهندس الكهربائي
Bot Extracte zip&rar(بوت استخراج zip&rar)🌐:unzipunrarprobot
"""


exploreBotEdit = """بعض الميزات الرئيسية هي:
◍ `تحويل الصور إلى PDF`
◍ `تحويل ملفات PDF إلى صور`
◍ `تحويل الملفات إلى pdf`
◍ `قم بأرسال ملف pdf  لتعديل عليه`
تعديل على ملف pdf :
◍ `تحويله  الى نص` 
◍ `ضغط ملف pdf `
◍ `تقسيم ملف pdf `
◍` دمج ملفات pdf`
◍` استخراج صورة من pdf`  
◍ `ختم على  pdf `
◍` إعادة تسمية ملف pdf
◍` استدارة ملف pdf
◍ `تشفير وفك تشفير  عن ملف pdf `
◍ `تنسيق ملف  pdf `
◍ `ارسل ملف وورد لتحويلة الى docx to pdf `
◍ `ارسل ملف بوربيونت لتحويلة الى pptx to pdf `
◍ `ارسل ملف الاكسيل لتحويلة الى  xlsx, xlt, xltx, xml to pdf`
◍ `قص دمج تدوير صغط ختم تحويل الى صور وغيرها فقط ب pdf `
◍ `ضغط ملفات pdf الى ملف مضغوط  zip`
◍ `تحويل ملف html الى pdf`
◍ `تحويل الرابط URL web الى pdf`
◍ `تحويل النص الى pdf`

مطور البوت: @ta_ja199
قناة البوت channel Bot :@i2pdfbotchannel

Some of the main features are:
◍ `Convert Images to PDF`
◍ `Convert PDFs to Images`
◍ `Convert files to pdf`
◍ `Send a pdf file to edit`
Modify the pdf file:
◍ `convert it to text`
◍ `zip pdf file`
◍ `split pdf file`
◍` Merge pdf files`
◍` Extract image from pdf`
◍ `Stamp on pdf`
◍` Rename pdf file
◍` Rotate pdf file
◍ `Encrypt and decrypt pdf file `
◍ `pdf file format`
◍ `Send a word document to convert it to docx to pdf `
◍ `Send a PowerPoint file to convert it to pptx to pdf `
◍ `Send the excel file to convert it to xlsx, xlt, xltx, xml to pdf`
◍ `Cut, Merge, Rotate, Stamp, Stamp, Convert to Images, etc. only with PDF `
◍ `Compress pdf files to a zip file`
◍ `Convert html file to pdf`
◍ `Convert web URL to pdf`
◍ `Convert text to pdf`

Bot Developer: @ta_ja199
Bot channel: @i2pdfbotchannel

[feedback|اكتب تعليقًا📋](https://t.me/engineering_electrical9/719?comment=1)"""

translatorBot2Edit = """
ترجمة pdf translator  :
لترجمة  pdf  أولا  أرسل  ملف pdf الى البوت هنا  
سوف تظهر  لك ازار إضغط  على :
 ✏️ totext الى نص✏️
وبعدها اختار:
html 🌐
✏️ totext الى نص✏️>>html 🌐
وبعدها افتح ملف واضغط  ترجمة وثم مشاركة  وبعدها  طباعة 
اذا لم تفهم جيدا تابع الشرح أدناه 👇


[feedback|اكتب تعليقًا📋](https://t.me/engineering_electrical9/719?comment=1)"""
#--------------->
#--------> config vars
#------------------->

UPDATE_CHANNEL=Config.UPDATE_CHANNEL
BANNED_USERS=Config.BANNED_USERS
ADMIN_ONLY=Config.ADMIN_ONLY
ADMINS=Config.ADMINS

#--------------->
#--------> /start (START MESSAGE)
#------------------->


@ILovePDF.on_message(filters.private & ~filters.edited & filters.command(["start"]))
async def start(bot, message):
        global invite_link
        await bot.send_chat_action(
            message.chat.id, "typing"
        )
        # CHECK IF USER BANNED, ADMIN ONLY..
        if (message.chat.id in BANNED_USERS) or (
            (ADMIN_ONLY) and (message.chat.id not in ADMINS)
        ):
            await bot.send_message(
                message.chat.id, UCantUse
            )
            return
        # CHECK USER IN CHANNEL (IF UPDATE_CHANNEL ADDED)
        if UPDATE_CHANNEL:
            try:
                await bot.get_chat_member(
                    str(UPDATE_CHANNEL), message.chat.id
                )
            except Exception:
                if invite_link == None:
                    invite_link = await bot.create_chat_invite_link(
                        int(UPDATE_CHANNEL)
                    )
                await bot.send_message(
                    message.chat.id,
                    forceSubMsg.format(
                        message.from_user.first_name, message.chat.id
                    ),
                    reply_markup = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "🌟(JOIN CHANNEL) أنظم في القناة🌟",
                                    url = invite_link.invite_link
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    "تحديث |Refresh ♻️",
                                    callback_data = "refresh"
                                )
                            ]
                        ]
                    )
                )
                await bot.delete_messages(
                    chat_id = message.chat.id,
                    message_ids = message.message_id
                )
                return
        
        await bot.send_message(
            message.chat.id,
            welcomeMsg.format(
                message.from_user.first_name,
                message.chat.id
            ),
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "📨 About |حول 📨",
                            callback_data = "strtDevEdt"
                        ),
                        InlineKeyboardButton(
                            "📮Explore|استكشف📮",
                            callback_data = "exploreBot"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "📕ترجمة pdf | translator📙",
                            callback_data = "translatorBot"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🚫 أغلق | CLOSE  🚫",
                            callback_data = "close"
                        )
                    ]
                ]
            )
        )
        # DELETES /start MESSAGE
        await bot.delete_messages(
            chat_id = message.chat.id,
            message_ids = message.message_id
        )


#--------------->
#--------> START CALLBACKS
#------------------->


strtDevEdt = filters.create(lambda _, __, query: query.data == "strtDevEdt")
exploreBot = filters.create(lambda _, __, query: query.data == "exploreBot")
translatorBot= filters.create(lambda _, __, query: query.data == "translatorBot")
refresh = filters.create(lambda _, __, query: query.data == "refresh")
close = filters.create(lambda _, __, query: query.data == "close")
back = filters.create(lambda _, __, query: query.data == "back")



@ILovePDF.on_callback_query(strtDevEdt)
async def _strtDevEdt(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            aboutDev,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Website(موقع)🌐",
                            url = "https://electrical-engineer-cc40b.web.app/"
                        ),
                        InlineKeyboardButton(
                            "الصفحة الرئيسية home 🏠  ",
                            callback_data = "back"
                        )
                    ],
                          [
                        InlineKeyboardButton(
                            "🌟 Rate : تقييم 🌟",
                            url ="https://telegramic.org/bot/i2pdfbot/"
                        )
                    ],                  
                        [
                        InlineKeyboardButton(
                            "🚫 أغلق | CLOSE  🚫",
                            callback_data = "close"
                        )
                    ]
                ]
            )
        )
        return
    except Exception as e:
        print(e)


@ILovePDF.on_callback_query(exploreBot)
async def _exploreBot(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            exploreBotEdit,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "الصفحة الرئيسية home 🏠  ",
                            callback_data = "back"
                        )
                    ],
                          [
                        InlineKeyboardButton(
                            "🌟 Rate : تقييم 🌟",
                            url ="https://t.me/tlgrmcbot?start=i2pdfbot"
                        )
                    ],                  
                        [
                        InlineKeyboardButton(
                            "🚫 أغلق | CLOSE  🚫",
                            callback_data = "close"
                        )
                    ]
                ]
            )
        )
        return
    except Exception as e:
        print(e)
@ILovePDF.on_callback_query(translatorBot)
async def _translatorBot(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            translatorBot2Edit,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "الصفحة الرئيسية home 🏠  ",
                            callback_data = "back"
                        )
                    ],
                          [
                        InlineKeyboardButton(
                            "شرح كيفية  ترجمة pdf 🎥",
                            url ="https://youtu.be/96n_OlK3PCk"
                        )
                    ],                  
                        [
                        InlineKeyboardButton(
                            "🚫 أغلق | CLOSE  🚫",
                            callback_data = "close"
                        )
                    ]
                ]
            )
        )
        return
    except Exception as e:
        print(e)

@ILovePDF.on_callback_query(back)
async def _back(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            welcomeMsg.format(
                callbackQuery.from_user.first_name,
                callbackQuery.message.chat.id
            ),
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "📨About |حول📨",
                            callback_data = "strtDevEdt"
                        ),
                        InlineKeyboardButton(
                            "📮Explore|استكشف📮",
                            callback_data = "exploreBot"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "📕ترجمة pdf | translator📙",
                            callback_data = "translatorBot"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🚫 أغلق | CLOSE  🚫",
                            callback_data = "close"
                        )
                    ]
                ]
            )
        )
        return
    except Exception as e:
        print(e)


@ILovePDF.on_callback_query(refresh)
async def _refresh(bot, callbackQuery):
    try:
        # CHECK USER IN CHANNEL (REFRESH CALLBACK)
        await bot.get_chat_member(
            str(UPDATE_CHANNEL),
            callbackQuery.message.chat.id
        )
        # IF USER NOT MEMBER (ERROR FROM TG, EXECUTE EXCEPTION)
        await callbackQuery.edit_message_text(
            welcomeMsg.format(
                callbackQuery.from_user.first_name,
                callbackQuery.message.chat.id
            ),
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "📨About |حول📨",
                            callback_data = "strtDevEdt"
                        ),
                        InlineKeyboardButton(
                            "📮Explore|استكشف📮",
                            callback_data = "exploreBot"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "📕ترجمة pdf | translator📙",
                            callback_data = "translatorBot"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🚫 أغلق | CLOSE  🚫",
                            callback_data = "close"
                        )
                    ]
                ]
            )
        )
    except Exception:
        try:
            # IF NOT USER ALERT MESSAGE (AFTER CALLBACK)
            await bot.answer_callback_query(
                callbackQuery.id,
                text = foolRefresh,
                show_alert = True,
                cache_time = 0
            )
        except Exception as e:
            print(e)


@ILovePDF.on_callback_query(close)
async def _close(bot, callbackQuery):
    try:
        await bot.delete_messages(
            chat_id = callbackQuery.message.chat.id,
            message_ids = callbackQuery.message.message_id
        )
        return
    except Exception as e:
        print(e)


#                                                                                  Telegram: @nabilanavab
