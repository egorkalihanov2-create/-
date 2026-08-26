import os

# --- Обязательные переменные окружения (задаются в Railway → Variables) ---
BOT_TOKEN = os.environ["BOT_TOKEN"]              # токен от @BotFather
CHANNEL_ID = os.environ["CHANNEL_ID"]             # например: "@my_channel" или -1001234567890
CHANNEL_URL = os.environ.get("CHANNEL_URL", "https://t.me/my_channel")  # ссылка для кнопки "Подписаться"

# --- Материалы, которые бот выдаёт после проверки подписки ---
# id -> (текст кнопки в меню, текст/ссылка, которые получит пользователь)
MATERIALS = {
    "awards_calendar": {
        "button_text": "календарь премий",
        "content": "Календарь премий: https://t.me/c/3657884848/433",
    },
    "tgk_guide": {
        "button_text": "гид по тгк",
        "content": "Гид по тгк: https://t.me/c/3657884848/435",
    },
    "designer_resources": {
        "button_text": "ресурсы для дизайнеров",
        "content": "Ресурсы для дизайнеров: https://t.me/c/3657884848/436",
    },
    "hh_hse": {
        "button_text": "HH x HSE",
        "content": "HH x HSE: https://t.me/c/3657884848/439",
    },
    "week_3d": {
        "button_text": "неделя 3д",
        "content": "Неделя 3д: https://t.me/c/3657884848/443",
    },
    "zine_week": {
        "button_text": "неделя зинов",
        "content": "Неделя зинов: https://t.me/c/3657884848/444",
    },
    "typography_week": {
        "button_text": "неделя типографики",
        "content": "Неделя типографики: https://t.me/c/3657884848/445",
    },
    "archive_week": {
        "button_text": "неделя архивов",
        "content": "Неделя архивов: https://t.me/c/3657884848/446",
    },
    "nn_presentation": {
        "button_text": "НН преза PDF",
        "content": "НН преза",
        "file_path": "assets/nn_presentation.pdf",
    },
}
