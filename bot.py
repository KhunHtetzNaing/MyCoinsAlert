from logger import logging
import asyncio
from aiogram import Bot, Dispatcher, types, html
from aiogram.enums import ParseMode
from aiogram.filters import Command
from coin_manager import coin_manager
from config import config
from database import Database
from keyboards import keyboards
from handlers.alerts import AlertHandlers
from price_checker import price_checker

# Setup
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()
db = Database(config.DB_NAME)
alert_handlers = AlertHandlers(db)

# Command handlers
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Handle the /start command"""
    user_name = html.bold(message.from_user.full_name)
    welcome_message = (
        f"👋 Welcome {user_name} to Crypto Price Alert!\n\n"
        "📊 I will notify you when cryptocurrencies reach your target prices.\n\n"
        "Quick Start:\n"
        "• Set alerts with /alert command\n"
        "• View your alerts with /alerts\n"
        "• Get help anytime with /help\n\n"
        "🚀 Ready to start tracking crypto prices?"
    )
    await message.answer(
        welcome_message,
        reply_markup=keyboards.main_keyboard(),
        parse_mode=ParseMode.HTML,
    )


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "🔔 Crypto Price Alerts\n\n"
        "📝 Set Alert:\n"
        "/alert <coin> <operator> <price>\n"
        "Examples:\n"
        "/alert BTC > 50000\n"
        "/alert ETH < 2000\n\n"

        "📋 Manage Alerts:\n"
        "/alerts - View your alerts\n"
        "/remove <number> - Remove alert by number\n"
        "/remove <coin> - Remove alerts by coin\n"
        "/removeall - Clear all alerts\n"
        "Examples:\n"
        "/remove 1\n"
        "/remove BTC\n\n"

        "💡 Note:\n"
        "• Supports both full name and symbol (Bitcoin, BTC)\n"
        "• You can set multiple alerts for the same coin\n"
        "• One alert triggers once\n"
        "• Check numbers with /alerts\n"
        "• Remove alerts by coin or number.",
        reply_markup=keyboards.main_keyboard(),
    )


@dp.message(Command("alert"))
async def cmd_alert(message: types.Message):
    await alert_handlers.cmd_alert(message.from_user.id, message)


@dp.message(Command("alerts"))
async def cmd_alerts(message: types.Message):
    await alert_handlers.show_alerts(message.from_user.id, message)


@dp.message(Command("remove"))
async def cmd_remove(message: types.Message):
    await alert_handlers.cmd_remove(message.from_user.id, message)


@dp.message(Command("removeall"))
async def cmd_remove(message: types.Message):
    await alert_handlers.cmd_removeall(message.from_user.id, message)


@dp.message()
async def echo_handler(message: types.Message):
    await message.reply("Unknown commands 🤔", reply_markup=keyboards.help_keyboard())


# Callback query handlers
@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    if callback.data == "set_alert":
        await callback.message.answer(
            "📝 Set alert using:\n"
            "/alert BTC > 100000\n"
            "/alert ETH < 2000"
        )
    elif callback.data == "view_alerts":
        await alert_handlers.show_alerts(callback.from_user.id, callback.message)
    elif callback.data == "help":
        await cmd_help(callback.message)
        # await callback.message.answer(config.HELP_MESSAGE)
    await callback.answer()


async def check_alerts():
    """Background task to check alerts"""
    while True:
        try:
            alerts = db.get_all_alerts()
            if alerts:
                # Get unique coins
                coin_ids = list(set(alert[2] for alert in alerts))
                prices = await price_checker.get_prices(coin_ids)

                send_list = {}  # Initialize empty dictionary

                # Check each alert
                for alert_id, user_id, coin_id, target, is_greater in alerts:
                    current_price = prices.get(coin_id)
                    if current_price:
                        condition_met = (
                                (is_greater and current_price > target) or
                                (not is_greater and current_price < target)
                        )

                        if condition_met:
                            # Initialize list for user if not exists
                            if user_id not in send_list:
                                send_list[user_id] = []

                            # Add alert info to user's list
                            alert_info = (
                                f"• {coin_manager.get_coin_name(coin_id)}: "
                                f"{price_checker.format_price(current_price)}\n"
                                f"  Target: {'>' if is_greater else '<'} "
                                f"{price_checker.format_price(target)}"
                            )
                            send_list[user_id].append(alert_info)

                # Send consolidated messages to users
                for user_id, alerts_list in send_list.items():
                    try:
                        message = (
                                "🎯 Target(s) reached!\n\n" +
                                "\n\n".join(alerts_list)
                        )

                        await bot.send_message(
                            user_id,
                            message,
                            reply_markup=keyboards.main_keyboard()
                        )

                    except Exception as e:
                        logging.error(f"Error sending message to user {user_id}: {e}")

        except Exception as e:
            logging.error(f"Error in check_alerts: {e}")

        await asyncio.sleep(config.CHECK_INTERVAL)


async def main():
    # Start the alert checking loop
    asyncio.create_task(check_alerts())
    try:
        logging.info("Starting My Coins Alert bot...")
        # Start polling
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Bot stopped with error: {e}")
    finally:
        logging.info("Bot stopped")
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.error(f"Fatal error: {e}")
