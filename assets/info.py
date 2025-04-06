# Важно для работы, не удалять!
import os

# Для работы проверки на подписку, нужно оставить тэг на канал, и ссылку к нему
CHANNEL_TAG = "@neuroquiztest" # Вставить тэг через @
CHANNEL_URL = "https://t.me/neuroquiztest" # Ссылка на ваш телеграм канал

# Путь к файлу, который будет отправляться пользователю по окончанию анкеты
# Файл размещать в папке assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILEPATH = os.path.join(BASE_DIR, "info.txt") # Вместо "info.txt" вставить название и расширение вашего файла, например "bonus.pdf"
FILE_CAPTION = "Ваш бонус" # Текст в сообщении под файлом, оставить None если ничего не нужно