import os
import logging
from typing import Dict, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from googletrans import Translator, LANGUAGES

# ==================== CONFIGURATION ====================

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from environment variable
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("BOT_TOKEN not found in environment variables!")
    raise ValueError("No BOT_TOKEN found in environment variables!")

# Initialize translator
translator = Translator()

# User session storage
user_languages: Dict[int, str] = {}

# ==================== LANGUAGE DATA ====================

# 69 Most Common Languages
LANGUAGE_CODES = {
    "af": "Afrikaans",
    "sq": "Albanian",
    "am": "Amharic",
    "ar": "Arabic",
    "hy": "Armenian",
    "az": "Azerbaijani",
    "eu": "Basque",
    "be": "Belarusian",
    "bn": "Bengali",
    "bs": "Bosnian",
    "bg": "Bulgarian",
    "ca": "Catalan",
    "ceb": "Cebuano",
    "ny": "Chichewa",
    "zh-cn": "Chinese (Simplified)",
    "zh-tw": "Chinese (Traditional)",
    "co": "Corsican",
    "hr": "Croatian",
    "cs": "Czech",
    "da": "Danish",
    "nl": "Dutch",
    "en": "English",
    "eo": "Esperanto",
    "et": "Estonian",
    "tl": "Filipino",
    "fi": "Finnish",
    "fr": "French",
    "fy": "Frisian",
    "gl": "Galician",
    "ka": "Georgian",
    "de": "German",
    "el": "Greek",
    "gu": "Gujarati",
    "ht": "Haitian Creole",
    "ha": "Hausa",
    "haw": "Hawaiian",
    "iw": "Hebrew",
    "hi": "Hindi",
    "hmn": "Hmong",
    "hu": "Hungarian",
    "is": "Icelandic",
    "ig": "Igbo",
    "id": "Indonesian",
    "ga": "Irish",
    "it": "Italian",
    "ja": "Japanese",
    "jw": "Javanese",
    "kn": "Kannada",
    "kk": "Kazakh",
    "km": "Khmer",
    "rw": "Kinyarwanda",
    "ko": "Korean",
    "ku": "Kurdish",
    "ky": "Kyrgyz",
    "lo": "Lao",
    "la": "Latin",
    "lv": "Latvian",
    "lt": "Lithuanian",
    "lb": "Luxembourgish",
    "mk": "Macedonian",
    "mg": "Malagasy",
    "ms": "Malay",
    "ml": "Malayalam",
    "mt": "Maltese",
    "mi": "Maori",
    "mr": "Marathi",
    "mn": "Mongolian",
    "my": "Myanmar (Burmese)",
    "ne": "Nepali",
    "no": "Norwegian",
    "or": "Odia (Oriya)",
    "ps": "Pashto",
    "fa": "Persian",
    "pl": "Polish",
    "pt": "Portuguese",
    "pa": "Punjabi",
    "ro": "Romanian",
    "ru": "Russian",
    "sm": "Samoan",
    "gd": "Scots Gaelic",
    "sr": "Serbian",
    "st": "Sesotho",
    "sn": "Shona",
    "sd": "Sindhi",
    "si": "Sinhala",
    "sk": "Slovak",
    "sl": "Slovenian",
    "so": "Somali",
    "es": "Spanish",
    "su": "Sundanese",
    "sw": "Swahili",
    "sv": "Swedish",
    "tg": "Tajik",
    "ta": "Tamil",
    "tt": "Tatar",
    "te": "Telugu",
    "th": "Thai",
    "tr": "Turkish",
    "tk": "Turkmen",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "ug": "Uyghur",
    "uz": "Uzbek",
    "vi": "Vietnamese",
    "cy": "Welsh",
    "xh": "Xhosa",
    "yi": "Yiddish",
    "yo": "Yoruba",
    "zu": "Zulu"
}

# Quick access languages
QUICK_LANGUAGES = [
    ("🇬🇧 English", "en"),
    ("🇪🇸 Spanish", "es"),
    ("🇫🇷 French", "fr"),
    ("🇩🇪 German", "de"),
    ("🇨🇳 Chinese", "zh-cn"),
    ("🇯🇵 Japanese", "ja"),
    ("🇰🇷 Korean", "ko"),
    ("🇷🇺 Russian", "ru"),
    ("🇮🇳 Hindi", "hi"),
    ("🇦🇪 Arabic", "ar"),
    ("🇵🇹 Portuguese", "pt"),
    ("🇮🇹 Italian", "it"),
]

# ==================== HELPER FUNCTIONS ====================

def get_language_name(code: str) -> str:
    """Get language name from code with fallback."""
    return LANGUAGE_CODES.get(code, LANGUAGES.get(code, code))

def get_user_language(user_id: int) -> str:
    """Get user's preferred language or default to English."""
    return user_languages.get(user_id, "en")

# ==================== COMMAND HANDLERS ====================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    user = update.effective_user
    welcome_message = (
        f"🌍 *Welcome {user.first_name}!*\n\n"
        f"I'm a powerful language translator bot supporting *69 languages*! 🌟\n\n"
        f"📌 *How to use:*\n"
        f"• Send any text and I'll auto-detect the language\n"
        f"• I'll translate it to your target language (default: English)\n"
        f"• Use /setlang to change your target language\n"
        f"• Use /langs to see all 69 supported languages\n\n"
        f"✨ *Commands:*\n"
        f"/start - Show this message\n"
        f"/help - Get detailed help\n"
        f"/langs - List all supported languages\n"
        f"/setlang - Change target language\n"
        f"/about - About this bot\n\n"
        f"🚀 *Just send me any text to translate!*"
    )
    await update.message.reply_text(welcome_message, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    help_text = (
        f"🤔 *How to use me:*\n\n"
        f"1️⃣ Send any text message\n"
        f"2️⃣ I'll detect the source language automatically\n"
        f"3️⃣ I'll translate it to your target language\n\n"
        f"⚙️ *Customize:*\n"
        f"• /setlang - Choose your target language\n"
        f"• /langs - See all 69 supported languages\n\n"
        f"📝 *Example:*\n"
        f"Send: 'Bonjour tout le monde'\n"
        f"Result: 'Hello everyone' (if target is English)\n\n"
        f"💡 *Tip:* Use /setlang to translate to your native language!"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /about command."""
    about_text = (
        f"🤖 *About This Bot*\n\n"
        f"• Name: Language69 Translator Bot\n"
        f"• Version: 2.0.0\n"
        f"• Languages: 69\n"
        f"• Technology: Python + Telegram Bot API\n"
        f"• Hosting: Railway\n\n"
        f"👨‍💻 *Features:*\n"
        f"• Auto language detection\n"
        f"• 69 language support\n"
        f"• User-specific preferences\n"
        f"• Inline keyboard interface\n"
        f"• Fast & accurate translations\n\n"
        f"📊 *Stats:*\n"
        f"• Supported Languages: {len(LANGUAGE_CODES)}\n"
        f"• Active Users: {len(user_languages)}\n"
    )
    await update.message.reply_text(about_text, parse_mode="Markdown")

async def setlang_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /setlang command with inline keyboard."""
    keyboard = []
    row = []
    for i, (label, code) in enumerate(QUICK_LANGUAGES):
        row.append(InlineKeyboardButton(label, callback_data=f"setlang_{code}"))
        if len(row) == 3 or i == len(QUICK_LANGUAGES) - 1:
            keyboard.append(row)
            row = []
    
    keyboard.append([InlineKeyboardButton("📋 See All 69 Languages", callback_data="show_all_langs")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    current_lang = get_user_language(update.effective_user.id)
    current_name = get_language_name(current_lang)
    
    await update.message.reply_text(
        f"🎯 *Choose your target language*\n\n"
        f"Current target: *{current_name}*\n"
        f"Select from the options below or click 'See All' for the complete list.",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def langs_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /langs command - show all languages."""
    lang_list = []
    for code, name in sorted(LANGUAGE_CODES.items()):
        lang_list.append(f"`{code}` - {name}")
    
    chunks = [lang_list[i:i+25] for i in range(0, len(lang_list), 25)]
    
    text = f"🌐 *Supported Languages ({len(LANGUAGE_CODES)} total)*\n\n"
    text += "\n".join(chunks[0])
    text += f"\n\n📌 *Page 1/{len(chunks)}*"
    
    if len(chunks) > 1:
        keyboard = [[InlineKeyboardButton("➡️ Next Page", callback_data=f"lang_page_2")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)
    else:
        await update.message.reply_text(text, parse_mode="Markdown")

# ==================== CALLBACK HANDLERS ====================

async def set_language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle language selection callback."""
    query = update.callback_query
    await query.answer()
    
    lang_code = query.data.replace("setlang_", "")
    lang_name = get_language_name(lang_code)
    user_id = query.from_user.id
    
    user_languages[user_id] = lang_code
    logger.info(f"User {user_id} set language to {lang_code}")
    
    await query.edit_message_text(
        f"✅ *Language Updated!*\n\n"
        f"Target language: *{lang_name}*\n"
        f"Language code: `{lang_code}`\n\n"
        f"Now send me any text and I'll translate it to {lang_name}! 🚀",
        parse_mode="Markdown"
    )

async def show_all_languages_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle 'Show All Languages' callback."""
    query = update.callback_query
    await query.answer()
    
    lang_list = []
    for code, name in sorted(LANGUAGE_CODES.items()):
        lang_list.append(f"`{code}` - {name}")
    
    chunks = [lang_list[i:i+30] for i in range(0, len(lang_list), 30)]
    
    text = f"🌐 *All 69 Languages*\n\n"
    text += "\n".join(chunks[0])
    text += f"\n\n📌 *Page 1/{len(chunks)}*"
    
    if len(chunks) > 1:
        keyboard = [[InlineKeyboardButton("➡️ Next Page", callback_data=f"all_lang_page_2")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=reply_markup)
    else:
        await query.edit_message_text(text, parse_mode="Markdown")

async def paginate_languages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle language pagination."""
    query = update.callback_query
    await query.answer()
    
    page = int(query.data.split("_")[-1])
    source = query.data.replace(f"_page_{page}", "")
    
    lang_list = []
    for code, name in sorted(LANGUAGE_CODES.items()):
        lang_list.append(f"`{code}` - {name}")
    
    items_per_page = 25 if source == "lang" else 30
    total_pages = (len(lang_list) + items_per_page - 1) // items_per_page
    
    start_idx = (page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, len(lang_list))
    
    if source == "lang":
        title = "🌐 *Supported Languages*"
    else:
        title = "🌐 *All 69 Languages*"
    
    text = f"{title}\n\n"
    text += "\n".join(lang_list[start_idx:end_idx])
    text += f"\n\n📌 *Page {page}/{total_pages}*"
    
    keyboard = []
    nav_row = []
    
    if page > 1:
        nav_row.append(InlineKeyboardButton("⬅️ Previous", callback_data=f"{source}_page_{page-1}"))
    if page < total_pages:
        nav_row.append(InlineKeyboardButton("➡️ Next", callback_data=f"{source}_page_{page+1}"))
    
    if nav_row:
        keyboard.append(nav_row)
    
    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=reply_markup)

# ==================== MESSAGE HANDLER ====================

async def handle_translation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages and translate them."""
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    if not text:
        await update.message.reply_text("❌ Please send some text to translate.")
        return
    
    target_lang = get_user_language(user_id)
    target_name = get_language_name(target_lang)
    
    await update.message.chat.send_action(action="typing")
    
    try:
        detection = translator.detect(text)
        source_lang = detection.lang
        source_name = get_language_name(source_lang)
        
        translation = translator.translate(text, dest=target_lang)
        translated_text = translation.text
        
        response = (
            f"🔍 *Detected:* {source_name}\n"
            f"🎯 *Target:* {target_name}\n"
            f"📝 *Translation:*\n\n"
            f"{translated_text}"
        )
        
        if source_lang == target_lang:
            response += f"\n\nℹ️ *Note:* Source and target languages are the same. Use /setlang to change target."
        
        await update.message.reply_text(response, parse_mode="Markdown")
        
    except Exception as e:
        logger.error(f"Translation error for user {user_id}: {e}")
        error_message = (
            f"❌ *Translation Failed*\n\n"
            f"I couldn't translate that text. Please try:\n"
            f"• Sending shorter text\n"
            f"• Checking if the text is valid\n"
            f"• Using /setlang to select a different target language"
        )
        await update.message.reply_text(error_message, parse_mode="Markdown")

async def handle_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle unknown commands."""
    await update.message.reply_text(
        "❌ *Unknown Command*\n\n"
        "Use /start to see available commands.\n"
        "Send any text to translate it!",
        parse_mode="Markdown"
    )

# ==================== ERROR HANDLER ====================

async def error_handler(update: Optional[Update], context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors gracefully."""
    logger.error(f"Update {update} caused error: {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "⚠️ *Oops! Something went wrong.*\n\n"
            "Please try again later. If the problem persists, contact the bot developer.",
            parse_mode="Markdown"
        )

# ==================== MAIN ====================

def main() -> None:
    """Start the bot application."""
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Command handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("about", about_command))
        application.add_handler(CommandHandler("setlang", setlang_command))
        application.add_handler(CommandHandler("langs", langs_command))
        
        # Callback handlers
        application.add_handler(CallbackQueryHandler(set_language_callback, pattern="^setlang_"))
        application.add_handler(CallbackQueryHandler(show_all_languages_callback, pattern="^show_all_langs$"))
        application.add_handler(CallbackQueryHandler(paginate_languages, pattern="^lang_page_"))
        application.add_handler(CallbackQueryHandler(paginate_languages, pattern="^all_lang_page_"))
        
        # Message handlers
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_translation))
        application.add_handler(MessageHandler(filters.COMMAND, handle_unknown))
        
        # Error handler
        application.add_error_handler(error_handler)
        
        logger.info("🚀 Language69 Translator Bot is starting...")
        logger.info(f"📊 Supported Languages: {len(LANGUAGE_CODES)}")
        logger.info(f"🤖 Bot Username: @language69translator_bot")
        
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

if __name__ == "__main__":
    main()
