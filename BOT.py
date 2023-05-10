from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN_API, start_text
from yt_dlp import YoutubeDL
import os.path
from moviepy.editor import *

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)
COUNTER_DIR = 0
cwd = os.getcwd() # сохраняем текущую директорию

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(text=start_text)


@dp.message_handler()
async def send_video(message: types.Message):
    global COUNTER_DIR
    os.mkdir(str(COUNTER_DIR)) # Создаем новую директорию
    new_path = os.path.abspath(str(COUNTER_DIR))  # сохраняем путь новой директории
    os.chdir(str(COUNTER_DIR)) # Выполняем код в новой директории
    COUNTER_DIR += 1

    with YoutubeDL() as ydl:
        os.system(f'yt-dlp {message.text}')
        file_name = os.listdir(new_path)[0] # заходим в директорию и берем путь к файлу
        full_path = os.path.join(new_path, file_name)
        new_file = os.path.join('new_video.mp4') # путь к новому файлу
        video = VideoFileClip(full_path)  # достаём аудиодорожку
        audio = video.audio
        audio.write_audiofile('audio.wav')
        recovered_video = video.resize(width=video.w, height=video.h)  # Восстанавливаем поврежденный файл
        recovered_video.write_videofile('video_to_send.mp4')
        await bot.send_video(chat_id=message.from_user.id,
                             video=open('video_to_send.mp4', 'rb'))

        os.chdir(cwd) # возвращаемся в предыдущую директорию


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
