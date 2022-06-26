# fileName : plugins/dm/start.py
# copyright ©️ 2021 nabilanavab

# LOGGING INFO: DEBUG
import logging
logger=logging.getLogger(__name__)
logging.basicConfig(
                   level=logging.DEBUG,
                   format="%(levelname)s:%(name)s:%(message)s" # %(asctime)s:
                   )

from pdf import invite_link
from pyrogram import filters
from configs.dm import Config
from plugins.footer import header
from plugins.dm.photo import images
from configs.images import FEEDBACK
from pyrogram import Client as ILovePDF
from plugins.dm.document import documents
from pyrogram.types import InputMediaPhoto
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineKeyboardMarkup
from configs.db import isMONGOexist, LOG_CHANNEL
from configs.images import WELCOME_PIC, BANNED_PIC

if isMONGOexist:
    from database import db

#------------------->
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
◍ `For more information, click: Explore Bot`"""
UCantUse = "لا يمكنك استخدام هذا الروبوت لبعض الأسباب 🛑"


forceSubMsg = """مرحبا [{}](tg://user?id={}) 🤚🏻..!!
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
Bot Extracte zip&rar(بوت استخراج zip&rar)🌐:@unzipunrarprobot
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

helpMessage = """هلو Hey  [{}](tg://user?id={}).!
بعض الميزات الرئيسية هي:

- صور إلى PDF:
     الصور إلى PDF ، ملفات [JPEG ، png ، JPG] إلى PDF ، إعادة تسمية PDF في وقت الإنشاء ، إعادة التسمية حسب الاسم

- معالجة ملفات PDF:
     PDF إلى صور ، PDF إلى JPEG ، جلب البيانات الوصفية ، دمج ملفات PDF متعددة ، تقسيم ملفات PDF إلى أجزاء ، PDF إلى (رسائل ، نص ، html ، json) ، صفحات Zip / Rar PDF ، تشفير / فك تشفير PDF ، إضافة طوابع ، OCR PDF ، A4 المادة الأساسية ، وتحويل النص إلى PDF ، والحصول على معاينة PDF ، وجلب البيانات من القنوات والمجموعات المحمية

- تحويل برامج الترميز المختلفة إلى PDF
     ~ .epub ، .fb2 ، .cbz ، إلخ [بلا حدود]
     ~ 45 من برامج الترميز الأخرى باستخدام convertAPI [linmited]

⚠️ تحذير ⚠️
◍ هذا الروبوت مجاني تمامًا للاستخدام. لذا ، من فضلك لا ترسل بريد مزعج هنا. البريد العشوائي ممنوع منعا باتا ويؤدي إلى حظر دائم
Some of the main features are:

- Images to PDF:
    Images to PDF, [JPEG, png, JPG] files to PDF, Rename PDF at the Time Of Creation, Rename By Name

- PDF Manipulation:
    PDF to Images, PDF to JPEG, Fetch metaData, Merge Multiple PDF's, Split PDF's to parts, PDF to (messages, text, html, json), Zip / Rar PDF pages, Encrypt/Decrypt PDF, Add Stamps, OCR PDF, A4 Fotmatter, text to PDF, Get PDF Preview, Fetch Data From Protected Channels & Groups

- Convert Different Codecs to PDF
    ~ .epub, .fb2, .cbz, etc [with no limits]
    ~ 45 Other Codecs by Using convertAPI [linmited]

⚠️ WARNING ⚠️
◍ This Bot is Completely Free to Use. So, please dont spam here. Spamming is strictly prohibited and leads to permanent ban.🚶
"""


LOG_TEXT = "#مستخدم_جديد @ta_ja199/I2PDFbot\nID: {}\nعرض البروفايل(View Profile): {}"
LOG_TEXT_C = "#مستخدم_جات @ta_ja199/I2PDFbot\nID: {}\nعنوان المجموعة(Group Title): {}\nعدد مستخدمين(Total Users): {}\nUserNsme: {}"

button = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("📌 SET THUMB ضبط الإبهام  📌",
                                 callback_data="getThumb"),
        ],[
            InlineKeyboardButton("⚠️ HELP AND RULES تعليمات وقواعد⚠️",
                                     callback_data="help")
        ],[
            InlineKeyboardButton("📨 About |حول 📨",
            callback_data = "strtDevEdt")
        ],[
            InlineKeyboardButton("🤖 CHANNEL قناة 🤖",
                  url="https://telegram.dog/i2pdfbotchannel"),
            InlineKeyboardButton("📝 FEEDBACK اكتب تعليقاً 📝",
                                        url=f"{FEEDBACK}")
        ],[
            InlineKeyboardButton("➕ ADD TO GROUP أضف للمجموعة➕",
                                  callback_data="underDev")
        ],[
            InlineKeyboardButton("🚶 CLOSE أغلق 🚶",
                                    callback_data="close")
        ]]
    )

UPDATE_CHANNEL = Config.UPDATE_CHANNEL

#--------------->
#--------> /start (START MESSAGE)
#------------------->

@ILovePDF.on_message(
                    ~filters.edited &
                    filters.incoming &
                    filters.command(
                                   ["start", "ping"]
                    ))
async def start(bot, message):
    try:
        global invite_link
        await message.reply_chat_action(
                                       "typing"
                                       )
        # CHECK IF USER IN DATABASE
        if isMONGOexist:
            if message.chat.type in ['group', 'supergroup']:
                if not await db.is_chat_exist(message.chat.id):
                    await db.add_chat(
                                     message.chat.id,
                                     message.chat.title
                                     )
                    if LOG_CHANNEL:
                        try:
                            total = await bot.get_chat_members_count(
                                                                message.chat.id
                                                                )
                            await bot.send_message(
                                              chat_id = LOG_CHANNEL,
                                                  text = LOG_TEXT_C.format(
                                                                          message.chat.id,
                                                                          message.chat.title,
                                                                          total,
                                                                          message.chat.username if message.chat.username else "❌"
                                                                          ),
                                                   reply_markup = InlineKeyboardMarkup(
                                                          [[InlineKeyboardButton("« B@N «",
                                                                 callback_data = f"banC|{message.chat.id}")]]
                                                   ))
                        except Exception: pass
                try:
                    return await message.reply(
                                   f"أهلاً.! Hi There.! 🖐️\n"
                                   f"أنا جديد هنا(Im new here) {message.chat.title}\n\n"
                                   f"دعني أقدم نفسي(Let me Introduce myself).. \n"
                                   f"اسمي هو i2pdf ، ويمكنني مساعدتك في القيام بالكثير (My Name is iLovePDF, and i can help you to do many )"
                                   f"التلاعب بملفاتTelegram PDF Manipulations with @Telegram PDF files\n\n"
                                   f"Thanks @ta_ja199 for this Awesome Bot 😅", quote=True,
                                   reply_markup = InlineKeyboardMarkup(
                                                                     [[InlineKeyboardButton("🤠 BOT OWNER مطور البوت 🤠",
                                                                          url = "Telegram.dog/ta_ja199"),
                                                                       InlineKeyboardButton("🛡️ UPDATE CHANNEL قناة التحديثات🛡️",
                                                                          url = "Telegram.dog/i2pdfbotchannel")],
                                                                      [InlineKeyboardButton("🌟 تقييم البوت Rate bot 🌟",
                                                                          url = "https://telegramic.org/bot/i2pdfbot/")]]
                                  ))
                except Exception: pass
            if message.chat.type == "private":
                if not await db.is_user_exist(message.from_user.id):
                    await db.add_user(
                                     message.from_user.id,
                                     message.from_user.first_name
                                     )
                    if LOG_CHANNEL:
                        try:
                            await bot.send_message(
                                              chat_id = LOG_CHANNEL,
                                              text = LOG_TEXT.format(
                                                                    message.from_user.id,
                                                                    message.from_user.mention
                                                                    ),
                                              reply_markup = InlineKeyboardMarkup(
                                                          [[InlineKeyboardButton("« B@N «",
                                                          callback_data=f"banU|{message.from_user.id}")]]
                                              ))
                        except Exception: pass
        # CHECK USER IN CHANNEL (IF UPDATE_CHANNEL ADDED)
        if UPDATE_CHANNEL:
            try:
                userStatus = await bot.get_chat_member(
                                                      str(UPDATE_CHANNEL),
                                                      message.from_user.id
                                                      )
                # IF USER BANNED FROM CHANNEL
                if userStatus.status == 'banned':
                     await message.reply_photo(
                                              photo = BANNED_PIC,
                                              caption = "لا يمكنك استخدام هذا الروبوت لبعض الأسباب\nFor Some Reason You Can't Use This Bot"
                                                        "\nاتصل بمالك البوت 🤐\nContact Bot Owner 🤐",
                                              reply_markup = InlineKeyboardMarkup(
                                                    [[InlineKeyboardButton("المالك Owner 🎊",
                                                      url="https://t.me/ta_ja199")]]
                                              ))
                     return
            except Exception as e:
                if invite_link == None:
                    invite_link = await bot.create_chat_invite_link(
                                                                   int(UPDATE_CHANNEL)
                                                                   )
                await message.reply_photo(
                                         photo = WELCOME_PIC,
                                         caption = forceSubMsg.format(
                                                                     message.from_user.first_name,
                                                                     message.from_user.id
                                                                     ),
                                                    reply_markup=InlineKeyboardMarkup(
                                                        [
                                                            [
                                                                InlineKeyboardButton("🌟(JOIN CHANNEL) أنظم في القناة🌟", url=invite_link.invite_link)
                                                            ],[
                                                                InlineKeyboardButton("تحديث | Refresh ♻️", callback_data="refresh")
                                                            ]]
                                                    ))
                if message.chat.type not in ['group', 'supergroup']:
                    await message.delete()
                return
        # IF NO FORCE SUBSCRIPTION
        if message.chat.type == "private":
            await message.reply_photo(
                                     photo = WELCOME_PIC,
                                     caption = welcomeMsg.format(
                                                                message.from_user.first_name,
                                                                message.from_user.id
                                     ),
                                     reply_markup = button
                                     )
            await message.delete()
        else:
            await message.reply(
                               "هذه رسالة ترحيبTHIS IS A WELCOME MESSAGE 😂\n\n"
                               "/help FOR HELP MESSAGEلرسالة المساعدة 🤧",
                               quote = True,
                               reply_markup = InlineKeyboardMarkup(
                                   [[
                                       InlineKeyboardButton("🌟Rate bot تقييم البوت 🌟",
                                              url="https://telegramic.org/bot/i2pdfbot/"),
                                       InlineKeyboardButton("🔍 ABOUT BOT حول البوت 🔎",
                                                     url="https://telegram.dog/i2pdfbot")
                                   ],[
                                       InlineKeyboardButton("📌 SET THUMB اختر الابهام 📌",
                                                                   callback_data="getThumb")
                                   ]]
                               ))
    except Exception as e:
        logger.exception(
                        "PHOTO:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

#--------------->
#--------> START CALLBACKS
#------------------->

refreshDoc = filters.create(lambda _, __, query: query.data == "refreshDoc")
refreshImg = filters.create(lambda _, __, query: query.data == "refreshImg")
strtDevEdt = filters.create(lambda _, __, query: query.data == "strtDevEdt")
exploreBot = filters.create(lambda _, __, query: query.data == "exploreBot")
translatorBot= filters.create(lambda _, __, query: query.data == "translatorBot")
refresh = filters.create(lambda _, __, query: query.data == "refresh")
close = filters.create(lambda _, __, query: query.data == "close")
back = filters.create(lambda _, __, query: query.data == "back")
hlp = filters.create(lambda _, __, query: query.data == "help")
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

@ILovePDF.on_callback_query(hlp)
async def _hlp(bot, callbackQuery):
    try:
        if (callbackQuery.message.chat.type != "private") and (
            callbackQuery.from_user.id != callbackQuery.message.reply_to_message.from_user.id):
                return callbackQuery.answer("الرسالة ليست لك .. \nMessage Not For You.. 😏")
        
        await callbackQuery.answer()
        await callbackQuery.edit_message_caption(
              caption = helpMessage.format(
                        callbackQuery.from_user.first_name, callbackQuery.from_user.id
                        ),
                        reply_markup = InlineKeyboardMarkup(
                              [[InlineKeyboardButton("« BACK عودة «",
                                       callback_data = "back")]]
              ))
    except Exception as e:
        logger.exception(
                        "HLP:CAUSES %(e)s ERROR",
                        exc_info = True
                        )

@ILovePDF.on_callback_query(back)
async def _back(bot, callbackQuery):
    try:
        if (callbackQuery.message.chat.type != "private") and (
            callbackQuery.from_user.id != callbackQuery.message.reply_to_message.from_user.id):
                return await callbackQuery.answer("الرسالة ليست لك .. \nMessage Not For You.. 😏")
        
        await callbackQuery.answer()
        try:
            await callbackQuery.edit_message_media(InputMediaPhoto(WELCOME_PIC))
        except Exception: pass
        await callbackQuery.edit_message_caption(
              caption = welcomeMsg.format(
                        callbackQuery.from_user.first_name,
                        callbackQuery.message.chat.id
              ),
              reply_markup = button
              )
    except Exception as e:
        # error if back followed by help message
        logger.exception(
                        "BACK:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

@ILovePDF.on_callback_query(refresh | refreshDoc | refreshImg)
async def _refresh(bot, callbackQuery):
    try:
        if (callbackQuery.message.chat.type != "private") and (
            callbackQuery.from_user.id != callbackQuery.message.reply_to_message.from_user.id):
                return await callbackQuery.answer("الرسالة ليست لك .. \nMessage Not For You.. 😏")
        
        # CHECK USER IN CHANNEL (REFRESH CALLBACK)
        userStatus = await bot.get_chat_member(
                                              str(UPDATE_CHANNEL),
                                              callbackQuery.from_user.id
                                              )
        await callbackQuery.answer()
        # IF USER NOT MEMBER (ERROR FROM TG, EXECUTE EXCEPTION)
        if callbackQuery.data == "refresh":
            return await callbackQuery.edit_message_caption(
                          caption = welcomeMsg.format(
                                      callbackQuery.from_user.first_name,
                                      callbackQuery.from_user.id
                                      ),
                                      reply_markup = button
                         )
        if callbackQuery.data == "refreshDoc":
            messageId = callbackQuery.message.reply_to_message
            await callbackQuery.message.delete()
            return await documents(
                            bot, messageId
                            )
        if callbackQuery.data == "refreshImg":
            messageId = callbackQuery.message.reply_to_message
            await callbackQuery.message.delete()
            return await images(
                               bot, messageId
                               )
    except Exception as e:
        try:
            # IF NOT USER ALERT MESSAGE (AFTER CALLBACK)
            await bot.answer_callback_query(
                                           callbackQuery.id,
                                           text = foolRefresh,
                                           show_alert = True,
                                           cache_time = 0
                                           )
        except Exception:
            pass

@ILovePDF.on_callback_query(close)
async def _close(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        await callbackQuery.message.delete()
    except Exception as e:
        logger.exception(
                        "CLOSE:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

#                                                                                  Telegram: @nabilanavab
