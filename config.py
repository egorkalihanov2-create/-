import os

# --- Обязательные переменные окружения (задаются в Railway → Variables) ---
BOT_TOKEN = os.environ["BOT_TOKEN"]              # токен от @BotFather
CHANNEL_ID = os.environ["CHANNEL_ID"]             # например: "@my_channel" или -1001234567890
CHANNEL_URL = os.environ.get("CHANNEL_URL", "https://t.me/my_channel")  # ссылка для кнопки "Подписаться"

# --- Материалы, которые бот выдаёт после проверки подписки ---
# id -> настройки материала: кнопка, fallback-текст/ссылка, id поста или файл
GUIDE_MATERIAL_KEYS = [
    "tgk_guide",
    "tgk_career",
    "awards_calendar",
    "designer_resources",
    "week_3d",
    "zine_week",
    "typography_week",
    "book_week",
]

ANTICRISIS_KEY = "anticrisis"

MATERIALS = {
    "tgk_guide": {
        "button_text": "гид по тгк",
        "content": "Гид по тгк: https://t.me/novaya_nasmotrennost/5671",
        "message_id": 5671,
    },
    "tgk_career": {
        "button_text": "тгк + карьера",
        "content": "ТГК + карьера: https://t.me/novaya_nasmotrennost/4226",
        "message_id": 4226,
    },
    "awards_calendar": {
        "button_text": "календарь премий",
        "content": "Календарь премий: https://t.me/novaya_nasmotrennost/6285",
        "message_id": 6285,
    },
    "designer_resources": {
        "button_text": "ресурсы для дизайнеров",
        "content": "Ресурсы для дизайнеров: https://t.me/novaya_nasmotrennost/5642",
        "message_id": 5642,
    },
    "week_3d": {
        "button_text": "неделя 3D",
        "content": "Неделя 3D: https://t.me/novaya_nasmotrennost/5392",
        "message_id": 5392,
    },
    "zine_week": {
        "button_text": "неделя зинов",
        "content": "Неделя зинов: https://t.me/novaya_nasmotrennost/4291",
        "message_id": 4291,
    },
    "typography_week": {
        "button_text": "неделя типографики",
        "content": "Неделя типографики: https://t.me/novaya_nasmotrennost/4472",
        "message_id": 4472,
    },
    "book_week": {
        "button_text": "неделя книги",
        "content": "Неделя книги: https://t.me/novaya_nasmotrennost/4936",
        "message_id": 4936,
    },
    "anticrisis": {
        "button_text": "антикризис",
        "content": "Антикризис: https://t.me/novaya_nasmotrennost/6562",
        "message_id": 6562,
        "file_path": "assets/nn_presentation.pdf",
    },
}
