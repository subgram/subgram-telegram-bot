import asyncio
from telegram import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    WebAppInfo, 
    Update, 
    Bot
)
from telegram.ext import (
    Application, 
    CommandHandler, 
    CallbackQueryHandler, 
    ContextTypes
)

from config import settings

from subgram import Subgram
from subgram.constants import EventType

subgram = Subgram(settings.SUBGRAM_TOKEN)


MANAGE_SUBSCRIPTION_CALLBACK_DATA = "manage_subscription"
MANAGE_SUBSCRIPTION_MARKUP = InlineKeyboardMarkup([[
    InlineKeyboardButton("💸 Manage Subscription 💸", callback_data=MANAGE_SUBSCRIPTION_CALLBACK_DATA)
]])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(
        "This bot will demonstrate how easy it is to add a subscription paywall to your Telegram bot.",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Open paid functionallity", callback_data="show_paid_functionallity")
        ]]),
    )


async def manage_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    checkout_page = await subgram.create_checkout_page(
        product_id=settings.SUBGRAM_PRODUCT_ID,
        user_id=update.effective_user.id,
        name=update.effective_user.name,
        language_code=update.effective_user.language_code,
    )

    return await update.effective_user.send_message(
        "⬇️ Click below to manage your subscription ⬇️",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Manage Subscription", web_app=WebAppInfo(url=checkout_page.checkout_url))
        ]]),
    )


async def show_paid_functionallity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # check if user has paid
    if await subgram.has_access(
        user_id=update.effective_user.id,
        product_id=settings.SUBGRAM_PRODUCT_ID,
    ):
        return await update.effective_user.send_message(
            "🎉 You paid for the service and this is your paid content:\n\n❤️❤️❤️ I love you! ❤️❤️❤️",
            reply_markup=MANAGE_SUBSCRIPTION_MARKUP,
        )
    
    return await manage_subscription(update, context)


async def handle_subgram_events():
    bot = Bot(settings.TELEGRAM_TOKEN)

    async for event in subgram.event_listener():
        if event.type == EventType.SUBSCRIPTION_STARTED:
            await bot.send_message(
                chat_id=event.object.customer.telegram_id,
                text=f"Thank you for subscribing! You have access until: {event.object.status.ending_at}.",
                reply_markup=MANAGE_SUBSCRIPTION_MARKUP,
            )

        if event.type == EventType.SUBSCRIPTION_RENEWED:
            await bot.send_message(
                chat_id=event.object.customer.telegram_id,
                text=f"You just renewed your subscription and have access until: {event.object.status.ending_at}.",
                reply_markup=MANAGE_SUBSCRIPTION_MARKUP,
            )

        if event.type == EventType.SUBSCRIPTION_CANCELLED:
            await bot.send_message(
                chat_id=event.object.customer.telegram_id,
                text=f"You just canceled subscription! You still have access until: {event.object.status.ending_at}.",
                reply_markup=MANAGE_SUBSCRIPTION_MARKUP,
            )

        if event.type == EventType.SUBSCRIPTION_UPGRADED:
            await bot.send_message(
                chat_id=event.object.customer.telegram_id,
                text=f"You upgraded your subscription and have access until: {event.object.status.ending_at}.",
                reply_markup=MANAGE_SUBSCRIPTION_MARKUP,
            )

        if event.type == EventType.SUBSCRIPTION_RENEW_FAILED:
            await bot.send_message(
                chat_id=event.object.customer.telegram_id,
                text=f"We failed to charge you. Please update your payment method.\nYou have access until: {event.object.status.ending_at}",
                reply_markup=MANAGE_SUBSCRIPTION_MARKUP,
            )


async def post_init(_: Application) -> None:
    asyncio.create_task(handle_subgram_events())


def main() -> None:
    application = (
        Application
        .builder()
        .post_init(post_init)
        .token(settings.TELEGRAM_TOKEN)
        .build()
    )

    application.add_handler(CommandHandler("start", start))

    application.add_handler(CallbackQueryHandler(show_paid_functionallity, "show_paid_functionallity"))
    application.add_handler(CallbackQueryHandler(manage_subscription, MANAGE_SUBSCRIPTION_CALLBACK_DATA))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()