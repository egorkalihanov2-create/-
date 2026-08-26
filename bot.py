import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import BOT_TOKEN, CHANNEL_ID, CHANNEL_URL, MATERIALS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def build_main_menu() -> InlineKeyboardMarkup:
    """Клавиатура с материалами (по 2 кнопки в ряд)."""
    buttons = [
        InlineKeyboardButton(text=item["button_text"], callback_data=f"get:{key}")
        for key, item in MATERIALS.items()
    ]
    rows = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def build_subscribe_keyboard(material_key: str) -> InlineKeyboardMarkup:
    """Клавиатура: ссылка на канал + кнопка 'Я подписался' для повторной проверки."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔔 Подписаться на канал", url=CHANNEL_URL)],
            [InlineKeyboardButton(text="✅ Я подписался", callback_data=f"get:{material_key}")],
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


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Выбери материал ниже 👇\n"
        "Чтобы получить его, нужно быть подписанным на наш канал.",
        reply_markup=build_main_menu(),
    )


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
        if file_path := material.get("file_path"):
            await callback.message.answer_document(
                FSInputFile(file_path),
                caption=material.get("content"),
            )
        else:
            await callback.message.answer(material["content"])
    else:
        await callback.answer("Нужно подписаться на канал 🙂", show_alert=True)
        await callback.message.answer(
            "Похоже, ты ещё не подписан(а) на канал.\n"
            "Подпишись и нажми «Я подписался» — материал придёт сразу после проверки.",
            reply_markup=build_subscribe_keyboard(material_key),
        )


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
