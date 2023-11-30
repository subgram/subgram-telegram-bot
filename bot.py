from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application, 
    CommandHandler, CallbackQueryHandler, 
    ContextTypes, filters,
)

from config import settings

from subgram import Subgram

subgram = Subgram(settings.SUBGRAM_TOKEN)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(
        "This bot will demonstrate how easy it is to add a subscription paywall to your Telegram bot.",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Open paid functionallity", callback_data="show_paywall")
        ]]),
    )


async def show_paywall(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    checkout_page = await subgram.create_checkout_page(
        product_id=settings.SUBGRAM_PRODUCT_ID,
        user_id=update.effective_user.id,
        name=update.effective_user.name,
        language_code=update.effective_user.language_code,
    )
    return await update.effective_user.send_message(
        "You can subscribe to this bot by clicking this button:",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Subscribe", url=checkout_page.checkout_url)
        ]]),
    )


async def show_paid_functionallity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await subgram.has_access(
        user_id=update.effective_user.id,
        product_id=settings.SUBGRAM_PRODUCT_ID,
    ):
        return await update.message.reply_html(
            "You have access to paid functionallity!",
        )
    return await show_paywall(update, context)

    


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(settings.TELEGRAM_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    application.add_handler(CallbackQueryHandler(show_paywall, "show_paywall"))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()