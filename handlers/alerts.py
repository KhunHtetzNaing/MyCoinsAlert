import re
from aiogram import types
from coin_manager import coin_manager
from database import Database
from price_checker import price_checker
from keyboards import keyboards
from config import config


class AlertHandlers:
    def __init__(self, db: Database):
        self.db = db

    async def cmd_alert(self, user_id: int, message: types.Message):
        """Handler for /alert command"""
        try:
            # Parse command
            pattern = r"\/alert\s*([\w\s]+?)\s*([<>])\s*(\d*\.?\d+)"
            match = re.match(pattern, message.text)
            if match:
                coin = match.group(1).strip()
                operator = match.group(2)
                price = float(match.group(3))
            else:
                raise ValueError(
                    "❌ Invalid format. Use:\n"
                    "/alert BTC > 100000\n"
                    "/alert ETH < 2000"
                )

            is_greater_than = operator == ">"

            # Check alerts limit
            if self.db.get_alerts_count(user_id) >= config.MAX_ALERTS_PER_USER:
                raise ValueError(f"❌ Maximum {config.MAX_ALERTS_PER_USER} alerts allowed")

            coin_id = coin_manager.get_coin_id(coin)
            # Validate coin
            if not coin_id:
                raise ValueError(f"❌ Invalid coin: {coin}")

            # Get current price
            current_price = await price_checker.get_price(coin_id)
            if not current_price:
                raise ValueError("❌ Error fetching price. Please try again.")

            # Add alert
            if self.db.add_alert(user_id, coin_id, price, is_greater_than):
                await message.answer(
                    f"✅ Alert set: {coin_manager.get_coin_name(coin_id)} "
                    f"{'>' if is_greater_than else '<'} "
                    f"{price_checker.format_price(price)}\n"
                    f"Current price: {price_checker.format_price(current_price)}",
                    reply_markup=keyboards.main_keyboard()
                )
            else:
                raise ValueError("❌ This alert already exists")
        except ValueError as e:
            await message.answer(str(e))
        except Exception as e:
            print(e)
            await message.answer("❌ Error occurred. Please try again.")

    async def cmd_remove(self, user_id: int, message: types.Message):
        """Handler for /remove command"""
        try:
            coin = " ".join(message.text.split()[1:])
            if not coin:
                raise ValueError()
            if coin.isdigit():
                index = int(coin) - 1
                success, coin_id = self.db.remove_alert_by_index(user_id, index)
                if success:
                    await message.answer(
                        f"✅ Alert for {coin_manager.get_coin_name(coin_id)} removed",
                        reply_markup=keyboards.main_keyboard()
                    )
                else:
                    await message.answer(f"❌ Invalid alert number: {coin}")
            else:
                coin_id = coin_manager.get_coin_id(coin)
                if coin_id:
                    if self.db.remove_alert_by_coin(user_id, coin_id):
                        await message.answer(
                            f"✅ Alerts for {coin_manager.get_coin_name(coin_id)} are removed",
                            reply_markup=keyboards.main_keyboard()
                        )
                    else:
                        await message.answer(
                            f"❌No active alerts for {coin}",
                            reply_markup=keyboards.main_keyboard()
                        )
                else:
                    await message.answer(f"❌ Invalid coin: {coin}")
        except (ValueError, IndexError):
            await message.answer("❌ Invalid format\n\n"
                                 "To remove alert by number:\n"
                                 "/remove 1\n\n"
                                 "To remove all alerts for a coin:\n"
                                 "/remove BTC"
                                 )
        except Exception:
            await message.answer("❌ Error occurred. Please try again.")

    async def cmd_removeall(self, user_id: int, message: types.Message):
        """Remove all alerts for a user"""
        try:
            # First check if user has any alerts
            user_alerts = self.db.get_user_alerts(user_id)
            if not user_alerts:
                await message.answer(
                    "📝 You don't have any active alerts.",
                    reply_markup=keyboards.set_alert_keyboard()
                )
                return

            # Try to remove all alerts
            if self.db.remove_alert_by_user(user_id):
                await message.answer(
                    f"✅ Successfully removed {len(user_alerts)} alerts.",
                    reply_markup=keyboards.main_keyboard()
                )
            else:
                await message.answer(
                    "❌ Failed to remove alerts. Please try again.",
                    reply_markup=keyboards.main_keyboard()
                )

        except Exception as e:
            await message.answer(
                "❌ Something went wrong. Please try again later.",
                reply_markup=keyboards.main_keyboard()
            )

    async def show_alerts(self, user_id: int, message: types.Message):
        """Show user's active alerts"""
        alerts = self.db.get_user_alerts(user_id)

        if not alerts:
            await message.answer(
                "No active alerts.\nUse /alert to set one!",
                reply_markup=keyboards.set_alert_keyboard()
            )
            return

        try:
            # Get current prices
            coin_ids = list(set(alert[1] for alert in alerts))
            prices = await price_checker.get_prices(coin_ids)

            # Format alerts
            alert_text = "📊 Your Alerts:\n\n"
            for i, (_, coin_id, target, is_greater, created_at) in enumerate(alerts, 1):
                current_price = prices.get(coin_id)
                if current_price:
                    alert_text += (
                        f"{i}. {coin_manager.get_coin_name(coin_id)} "
                        f"{'>' if is_greater else '<'} "
                        f"{price_checker.format_price(target)}\n"
                        f"Current: {price_checker.format_price(current_price)}\n\n"
                    )

            alert_text += "Remove alert: /remove <number>\n"
            alert_text += "Remove alerts: /remove <coin>"
            await message.answer(alert_text, reply_markup=keyboards.main_keyboard())
        except Exception as e:
            await message.answer("❌ Error fetching current prices")
