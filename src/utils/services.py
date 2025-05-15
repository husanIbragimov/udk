import os
from typing import Union

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile
from openai import OpenAI, ChatCompletion
from data.config import ADMINS, API_KEY, CHANNEL_ID
from keyboards import builders, reply


async def download_file(message, bot, save_path):
    if message.photo:
        file_id = message.photo[-1].file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        await bot.download_file(file_path, save_path)
    elif message.document:
        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        await bot.download_file(file_path, save_path)
    else:
        await message.reply(
            "Yuklashda xatolik, iltimos qaytadan yuklang!"
        )
        return
    return save_path


async def send_to_admins(message: Message, state: FSMContext, bot: Bot, save_path: str, checking):
    data = await state.get_data()
    if os.path.exists(save_path):
        for admin in ADMINS:
            await bot.send_photo(
                chat_id=admin,
                photo=FSInputFile(path=save_path),
                caption=f"Yangi UDK aniqlash so'rovi: {data.get('question')}\n\n",
                reply_markup=checking
            )
    else:
        await message.answer("Rasmni yuklashda xatolik yuz berdi. Iltimos qaytadan urinib ko'ring.")
        await state.clear()
        return


def get_udk(topic):
    client = OpenAI(api_key=API_KEY)
    completion: ChatCompletion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
            {
                "role": "user",
                "content": f"Dissertatsiya mavzusi: {topic}.Dissertatsiya mavzusi bo'yicha UDKni aniqlab ber.UDK ni dissertatsiya hujjatlarida rasmiy yozilishi kerak bo‘lgan shaklida tayyorlab ber(Agar Mavzu: dan keying so'z  boshqa savol bo'lsa unga bu dissertatsiya mavzusi emas degan javob qaytar.Boshqa mavzularni yozma va qo'shimcha takliflar berma, ya'ni javobda bu javobning AI tomonidan generatsiya qilinganligi bo'lmasin).(faqat UDK kodini va tarkibini yoz, boshqa hech narsa yozma)"
            }
        ],
    )
    return completion.choices[0].message.content


async def user_is_member(message: Message, bot: Bot):
    chat_member = await bot.get_chat_member(CHANNEL_ID[0], message.from_user.id)
    print(chat_member)
    chat_link = await bot.create_chat_invite_link(
        chat_id=CHANNEL_ID[0],
        name="Kanalga o'tish"
    )
    inline_btn = await builders.vertical_inline_kb(chat_link.invite_link)
    if chat_member.status == "left":
        await message.answer("Sizni tekshiryapmiz...", reply_markup=reply.rmk)
        await message.answer("Botdan foydalanish uchun kanalimizga obuna bo'lishingiz kerak.", reply_markup=inline_btn)
        return False
    else:
        return True
