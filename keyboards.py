from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class Keyboards:
    def __init__(self):
        self.set_alert_btn = InlineKeyboardButton(text="➕ Set Alert", callback_data="set_alert")
        self.my_alerts_btn = InlineKeyboardButton(text="📋 My Alerts", callback_data="view_alerts")
        self.help_btn = InlineKeyboardButton(text="ℹ️ Help", callback_data="help")

    def main_keyboard(self) -> InlineKeyboardMarkup:
        """Main menu keyboard"""
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                self.set_alert_btn,
                self.my_alerts_btn
            ],
            [
                self.help_btn
            ]
        ])

    def help_keyboard(self) -> InlineKeyboardMarkup:
        """Main menu keyboard"""
        return InlineKeyboardMarkup(inline_keyboard=[
                [self.help_btn],
        ])

    def set_alert_keyboard(self) -> InlineKeyboardMarkup:
        """Main menu keyboard"""
        return InlineKeyboardMarkup(inline_keyboard=[
                [self.set_alert_btn, self.help_btn],
        ])

    @staticmethod
    def after_alert_keyboard() -> InlineKeyboardMarkup:
        """Keyboard shown after setting an alert"""
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📋 View My Alerts", callback_data="view_alerts")],
            [InlineKeyboardButton(text="➕ Set Another Alert", callback_data="set_alert")]
        ])

    @staticmethod
    def confirm_remove_keyboard(alert_id: int) -> InlineKeyboardMarkup:
        """Confirmation keyboard for alert removal"""
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Yes", callback_data=f"confirm_remove_{alert_id}"),
                InlineKeyboardButton(text="❌ No", callback_data="cancel_remove")
            ]
        ])

keyboards = Keyboards()