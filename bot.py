from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, Update
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
            InlineKeyboardButton("Open paid functionallity", callback_data="show_paid_functionallity")
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
            InlineKeyboardButton("Subscribe", web_app=WebAppInfo(url=checkout_page.checkout_url))
        ]]),
    )


async def show_paid_functionallity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await subgram.has_access(
        user_id=update.effective_user.id,
        product_id=settings.SUBGRAM_PRODUCT_ID,
    ):
        return await update.effective_user.send_message(
            "You paid for the service and this is your paid content:\n\nI love you!",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("💸 Show paywall anyway 💸", callback_data="show_paywall")
            ]]),
        )
    
    return await show_paywall(update, context)



def main() -> None:
    application = Application.builder().token(settings.TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", show_paid_functionallity, filters.Regex("subgram_paid")))
    application.add_handler(CommandHandler("start", start))

    application.add_handler(CallbackQueryHandler(show_paid_functionallity, "show_paid_functionallity"))
    application.add_handler(CallbackQueryHandler(show_paywall, "show_paywall"))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()