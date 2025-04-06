from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, ReplyKeyboardRemove, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.config import bot

import app.keyboards as kb
import urllib.parse

from assets.info import FILEPATH, FILE_CAPTION

from filters.chat_subscriber import IsSubscriber
import crm.api as crm

router = Router()
print("Bot has successfully started!")

class User(StatesGroup):
    name = State()
    age = State()
    activity = State()
    average_income = State()
    goal = State()


@router.message(CommandStart(), IsSubscriber(bot))
async def start(message: Message, state: FSMContext):
    existing_user = await crm.get_lead_by_tg_id(str(message.from_user.id))
    if existing_user:
        await message.answer("Вы не можете пройти анкету еще раз! Вместо этого, просим вас следить за новостями в нашем телеграм канале :)",
                             reply_markup=kb.existing_lead)
    else:
        await state.set_state(User.name)
        await message.answer("Привет! Как тебя зовут? (Давай начнем с простого!)", reply_markup=ReplyKeyboardRemove())

@router.message(User.name)
async def reg_two(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(User.age)
    await message.answer("Сколько тебе полных лет? Или сколько бы ты хотел, чтобы было? 🙂")

@router.message(User.age)
async def reg_three(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(User.activity)
    await message.answer(f'''Ты сейчас учишься, работаешь или совмещаешь все сразу?
(Выбери один вариант)
1) Учусь
2) Работаю
3) И то, и другое
4) Свободный художник жизни 🎨''', reply_markup=kb.user_activity)


@router.callback_query(User.activity)
async def reg_activity(callback: CallbackQuery, state: FSMContext):
    activity_mapping = {
        "activity_1": "Учусь",
        "activity_2": "Работаю",
        "activity_3": "И то, и другое",
        "activity_4": "Свободный художник жизни"
    }

    activity = activity_mapping.get(callback.data, "Не указано")
    await state.update_data(activity=activity)
    await state.set_state(User.average_income)
    await callback.message.answer(f'''Ваш доход - секретное оружие!
Мы знаем, что разговоры о деньгах - это не всегда весело, но давайте подойдем к этому с юмором! 😉

Какой у вас уровень дохода?
(Не переживайте, ваше богатство останеться в секрете, а ответы только для статистики)

1. 💸 Я как волшебник - каждый месяц "фокус" с деньгами, но обычно их хватает только на пару пицц.
2. 🏠 Средний размер счастья - хватает на комфорт и кафе с друзьями, но в Париж еще не сгонял.
3. 💼 Высокий уровень мастерства - ипотека оплачена, отпуск на Мальдивах - в следующем месяце.
4. 🏖 Я - богат как Крез - у меня есть всё, что нужно, и даже то, что я ещё не знаю, что мне нужно!
5. 🤫 Секрет, не буду раскрывать - я ценю свою приватность, так что не говорите никому!''', reply_markup=kb.income)


@router.callback_query(User.average_income)
async def reg_income(callback: CallbackQuery, state: FSMContext):
    income_mapping = {
        "income_1": "Я как волшебник",
        "income_2": "Средний размер счастья",
        "income_3": "Высокий уровень мастерства",
        "income_4": "Я - богат как Крез",
        "income_5": "Секрет, не буду раскрывать"
    }

    income = income_mapping.get(callback.data, "Не указано")
    await state.update_data(average_income=income)
    await state.set_state(User.goal)
    await callback.message.answer(f'''Зачем ты вообще сюда пришел? Что хочешь найти в нашем канале?
(Выбери один вариант)
1. Хочу стать гуру нейросетей
2. Интересуюсь новыми технологиями
3. Искать крутые проекты для вдохновения
4. Просто люблю общаться с умными людьми
5. Случайно забрел, но теперь мне тут нравиться 😅''', reply_markup=kb.goal)


@router.callback_query(User.goal)
async def reg_complete(callback: CallbackQuery, state: FSMContext):
    goal_mapping = {
        "goal_1": "Хочу стать гуру нейросетей",
        "goal_2": "Интересуюсь новыми технологиями",
        "goal_3": "Искать крутые проекты для вдохновления",
        "goal_4": "Просто люблю общаться с умными людьми",
        "goal_5": "Случайно забрел, но теперь мне тут нравиться"
    }

    goal = goal_mapping.get(callback.data, "Не указано")
    await state.update_data(goal=goal)

    data = await state.get_data()
    data["tg_id"] = str(callback.message.chat.id)

    await crm.add_lead(data)

    await callback.message.answer("Благодарим за заполнение анкеты! После завершения, вы получите PDF-гайд...")
    await callback.message.answer_document(document=FSInputFile(FILEPATH), caption=FILE_CAPTION)

    await state.clear()

@router.message(F.text == "Проверить подписку", IsSubscriber(bot))
async def retry_reg(message:Message, state: FSMContext):
    await start(message, state)