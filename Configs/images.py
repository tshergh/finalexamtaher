# fileName: configs/images.py
# copyright ©️ 2021 nabilanavab

import os


# ❌ FEEDBACK LINK ❌ [EDITABLE]
FEEDBACK = "https://t.me/i2pdfbotchannel/9?comment=13"


# ❌ DEFAULT THUMBNAIL ❌ [EDITABLE]
# NB: Thumbnails can’t be reused and can be only uploaded as a new file.
# from Configs.images import PDF_THUMBNAIL
PDF_THUMBNAIL = "./images/i2pdfbot.jpg"
# PDF_THUMBNAIL="https://te.legra.ph/i2pdfbot-06-26"


# ❌ WELCOME IMAGE ❌ [EDITABLE]
# from Configs.images import WELCOME_PIC
# WELCOME_IMAGE="./images/start.jpeg"
WELCOME_PIC = "https://te.legra.ph/i2pdfbot-06-26"


# ❌ BANNED IMAGE ❌ [EDITABLE]
# from Configs.images import BANNED_PIC
# BANNED_MESSAGE="./images/banned.jpeg"
BANNED_PIC = "https://te.legra.ph/i2pdfbot-06-26"


# ❌ BIG FILE ❌ [EDITABLE]
# from Configs.images import BIG_FILE
#  = "./images/bigFile.jpeg"
BIG_FILE = "https://te.legra.ph/i2pdfbot-06-26"


# ❌ Load UsersId with custom thumbnail ❌
CUSTOM_THUMBNAIL_U, CUSTOM_THUMBNAIL_C = [], []


# file name [if needed]
DEFAULT_NAME = os.environ.get("DEFAULT_NAME", False)


#                                                             @nabilanavab
