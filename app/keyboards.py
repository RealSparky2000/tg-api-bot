from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from assets.info import CHANNEL_URL

user_activity = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="1", callback_data="activity_1"), InlineKeyboardButton(text="2", callback_data="activity_2")],
    [InlineKeyboardButton(text="3", callback_data="activity_3"), InlineKeyboardButton(text="4", callback_data="activity_4")]
])

income = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="1", callback_data="income_1"), InlineKeyboardButton(text="2", callback_data="income_2")],
    [InlineKeyboardButton(text="3", callback_data="income_3"), InlineKeyboardButton(text="4", callback_data="income_4")],
    [InlineKeyboardButton(text="5", callback_data="income_5")]
])

goal = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="1", callback_data="goal_1"), InlineKeyboardButton(text="2", callback_data="goal_2")],
    [InlineKeyboardButton(text="3", callback_data="goal_3"), InlineKeyboardButton(text="4", callback_data="goal_4")],
    [InlineKeyboardButton(text="5", callback_data="goal_5")]
])

existing_lead = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Перейти в телеграм канал", url=CHANNEL_URL)]
])
