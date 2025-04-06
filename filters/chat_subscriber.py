from aiogram import types
from aiogram.filters import BaseFilter
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram import Bot
from assets.info import CHANNEL_TAG, CHANNEL_URL

class IsSubscriber(BaseFilter):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def __call__(self, message: types.Message, bot) -> bool:
        try:
            sub = await self.bot.get_chat_member(chat_id=CHANNEL_TAG, user_id=message.from_user.id)

            if sub.status in ["member", "creator", "administrator"]:
                return True
            else:
                markup_inline = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
                    [InlineKeyboardButton(text="Подпишись!", url=CHANNEL_URL)]
                ])

                markup_reply = ReplyKeyboardMarkup(keyboard=[
                    [KeyboardButton(text="Проверить подписку")]
                ], resize_keyboard=True)

                await message.answer("Для доступа подпишись на канал и повтори попытку!", reply_markup=markup_inline)
                await message.answer("После подписки, выберите пункт меню 'Проверить подписку' чтобы попробовать еще раз!", reply_markup=markup_reply)
                return False

        except Exception as e:
            await message.answer("Ошибка проверки подписки, попробуйте позже.")
            return False