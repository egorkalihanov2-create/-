import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

from config import (
    ANTICRISIS_KEY,
    BOT_TOKEN,
    CHANNEL_ID,
    CHANNEL_URL,
    GUIDE_MATERIAL_KEYS,
    MATERIALS,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

WELCOME_TEXT = (
    "привет! 👀\n\n"
    "это бот от @novaya_nasmotrennost – здесь будем делиться полезными "
    "для дизайнеров и недизайнеров материалами\n\n"
    "в наличии ↓"
)
MENU_SWITCH_TEXT = "\u2060"


def build_main_menu() -> InlineKeyboardMarkup:
    """Первый шаг: выбор раздела."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="гайд по тгк", callback_data="menu:guide"),
                InlineKeyboardButton(text="антикризис", callback_data=f"get:{ANTICRISIS_KEY}"),
            ]
        ]
    )


def build_guide_menu() -> InlineKeyboardMarkup:
    """Второй шаг: материалы гайда по тгк."""
    buttons = [
        InlineKeyboardButton(
            text=MATERIALS[key]["button_text"],
            callback_data=f"get:{key}",
        )
        for key in GUIDE_MATERIAL_KEYS
    ]
    rows = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
    rows.append([InlineKeyboardButton(text="назад", callback_data="menu:main")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def build_reply_menu() -> ReplyKeyboardMarkup:
    """Обычная клавиатура с разделами под полем ввода."""
    rows = [[KeyboardButton(text="гайд по тгк"), KeyboardButton(text="антикризис")]]
    return ReplyKeyboardMarkup(
        keyboard=rows,
        resize_keyboard=True,
        input_field_placeholder="выбери материал",
    )


def build_guide_reply_menu() -> ReplyKeyboardMarkup:
    """Обычная клавиатура второго шага под полем ввода."""
    buttons = [KeyboardButton(text=MATERIALS[key]["button_text"]) for key in GUIDE_MATERIAL_KEYS]
    rows = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
    rows.append([KeyboardButton(text="назад")])
    return ReplyKeyboardMarkup(
        keyboard=rows,
        resize_keyboard=True,
        input_field_placeholder="выбери материал",
    )


def build_subscribe_keyboard(material_key: str) -> InlineKeyboardMarkup:
    """Клавиатура: ссылка на канал + кнопка повторной проверки."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="подписаться на канал", url=CHANNEL_URL)],
            [InlineKeyboardButton(text="я подписался", callback_data=f"get:{material_key}")],
        ]
    )


async def is_subscribed(user_id: int) -> bool:
    """Проверяет, состоит ли пользователь в канале CHANNEL_ID."""
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ("member", "administrator", "creator")
    except Exception as e:
        # Частая причина ошибки — бот не добавлен админом в канал
        logger.error(f"Ошибка проверки подписки для user_id={user_id}: {e}")
        return False


def get_material_key_by_button_text(button_text: str) -> str | None:
    for key in GUIDE_MATERIAL_KEYS:
        if MATERIALS[key]["button_text"] == button_text:
            return key
    return None


async def send_material(
    message: Message,
    material: dict,
    reply_markup: ReplyKeyboardMarkup | None = None,
):
    reply_markup = reply_markup or build_reply_menu()
    forwarded = False

    if message_id := material.get("message_id"):
        from_chat_id = material.get("from_chat_id", CHANNEL_ID)
        try:
            await bot.forward_message(
                chat_id=message.chat.id,
                from_chat_id=from_chat_id,
                message_id=message_id,
            )
            forwarded = True
        except Exception as e:
            logger.error(
                f"Ошибка пересылки message_id={message_id} из {from_chat_id}: {e}"
            )

    if file_path := material.get("file_path"):
        await message.answer_document(
            FSInputFile(file_path),
            caption=material.get("file_caption"),
            reply_markup=reply_markup,
        )
    else:
        text = "выбирай дальше ↓" if forwarded else material["content"]
        await message.answer(text, reply_markup=reply_markup)


async def delete_button_press(message: Message):
    try:
        await message.delete()
    except Exception as e:
        logger.info(f"Не удалось удалить служебное сообщение с кнопки: {e}")


async def switch_reply_menu(message: Message, reply_markup: ReplyKeyboardMarkup):
    await delete_button_press(message)
    try:
        menu_message = await message.answer(MENU_SWITCH_TEXT, reply_markup=reply_markup)
        await menu_message.delete()
    except Exception as e:
        logger.error(f"Не удалось тихо переключить нижнюю клавиатуру: {e}")


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(WELCOME_TEXT, reply_markup=build_main_menu())


@dp.callback_query(F.data == "menu:main")
async def handle_main_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(WELCOME_TEXT, reply_markup=build_main_menu())


@dp.callback_query(F.data == "menu:guide")
async def handle_guide_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("гайд по тгк ↓", reply_markup=build_guide_menu())


@dp.callback_query(F.data.startswith("get:"))
async def handle_material_request(callback: CallbackQuery):
    material_key = callback.data.split(":", 1)[1]
    material = MATERIALS.get(material_key)

    if not material:
        await callback.answer("Материал не найден.", show_alert=True)
        return

    subscribed = await is_subscribed(callback.from_user.id)

    if subscribed:
        await callback.answer()  # закрыть "часики" на кнопке
        await send_material(callback.message, material)
    else:
        await callback.answer("Нужно подписаться на канал 🙂", show_alert=True)
        await callback.message.answer(
            "Похоже, ты ещё не подписан(а) на канал.\n"
            "Подпишись и нажми «я подписался» — материал придёт сразу после проверки.",
            reply_markup=build_subscribe_keyboard(material_key),
        )


@dp.message(F.text.in_(["гайд по тгк", "антикризис"]))
async def handle_reply_menu(message: Message):
    if message.text == "гайд по тгк":
        await switch_reply_menu(message, build_guide_reply_menu())
        return

    await delete_button_press(message)
    material_key = ANTICRISIS_KEY
    material = MATERIALS[material_key]

    subscribed = await is_subscribed(message.from_user.id)

    if subscribed:
        await send_material(message, material)
    else:
        await message.answer(
            "Похоже, ты ещё не подписан(а) на канал.\n"
            "Подпишись и нажми «я подписался» — материал придёт сразу после проверки.",
            reply_markup=build_subscribe_keyboard(material_key),
        )


@dp.message(F.text == "назад")
async def handle_reply_back(message: Message):
    await switch_reply_menu(message, build_reply_menu())


@dp.message(F.text.in_([MATERIALS[key]["button_text"] for key in GUIDE_MATERIAL_KEYS]))
async def handle_guide_reply_material(message: Message):
    await delete_button_press(message)
    material_key = get_material_key_by_button_text(message.text)
    if material_key is None:
        await message.answer("Материал не найден.", reply_markup=build_guide_reply_menu())
        return

    material = MATERIALS[material_key]
    subscribed = await is_subscribed(message.from_user.id)

    if subscribed:
        await send_material(message, material, reply_markup=build_guide_reply_menu())
    else:
        await message.answer(
            "Похоже, ты ещё не подписан(а) на канал.\n"
            "Подпишись и нажми «я подписался» — материал придёт сразу после проверки.",
            reply_markup=build_subscribe_keyboard(material_key),
        )


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
