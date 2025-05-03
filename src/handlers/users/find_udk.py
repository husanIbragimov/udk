import os
from datetime import date

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from data.config import ADMINS, MEDIA_PATH
from keyboards import builders
from keyboards import reply
from utils.db.models import Order, Payment
from utils.services import download_file, send_to_admins, get_udk, user_is_member
from utils.states import UDK

router = Router()


@router.message(F.text == "🔍 UDK ni aniqlash")
async def question_state(message: Message, state: FSMContext, bot: Bot):
    await user_is_member(message, bot)
    await state.clear()
    await message.answer("Savolni kiriting...")
    await state.set_state(UDK.question)


@router.message(UDK.question)
async def save_question(message: Message, state: FSMContext):
    await message.answer("Iltimos to'lov qiling va rasmini shu yerga yuklang.", reply_markup=reply.rmk)
    order = await Order.create(
        user_id=message.from_user.id,
        question=message.text,
    )
    await state.update_data(order_id=order.id, question=message.text)
    await state.set_state(UDK.check_image)


@router.message(UDK.check_image)
async def check_image(message: Message, state: FSMContext, bot: Bot):
    print(message.json())
    if message.text:
        await message.answer("Iltimos checkni rasm yoki file qilib yuklang.")
        return

    save_path = f"{MEDIA_PATH}/{message.from_user.id}-{date.today()}.jpg"
    await download_file(message, bot, save_path)

    data = await state.get_data()
    order_id = data.get("order_id")

    await Payment.create(
        order_id=order_id,
        check_image=save_path,
        is_paid=False,
    )
    await state.update_data(check_image=save_path)
    checking = await builders.inline_kb(
        ["✅ Tasdiqlash", "❌ Rad etish"],
        [f"confirm_{order_id}_{message.from_user.id}", f"reject_{order_id}_{message.from_user.id}"],
    )
    await send_to_admins(message, state, bot, save_path, checking)
    await message.answer("Tasdiqlash biroz vaqt olishi mumkin, iltimos kuting...")



@router.callback_query(F.data.startswith("confirm_"))
async def confirm_udk(call: CallbackQuery, bot: Bot):
    print(call.json())
    order_id, user_id = call.data.split("_")[1:]
    order = await Order.filter(id=order_id).first()
    if not order:
        return

    old_text = call.message.caption
    await call.message.edit_caption(
        caption=f"{old_text}\n\n⏳ Kutilmoqda..."
    )

    res = get_udk(topic=order.question)

    await bot.send_message(
        chat_id=user_id,
        text=f"{res}",
        reply_markup=reply.find_udk
    )

    await call.message.edit_caption(
        caption=f"{old_text}\n\nJavob: {res}"
    )


@router.callback_query(F.data.startswith("reject_"))
async def reject_udk(call: CallbackQuery, bot: Bot):
    order_id, user_id = call.data.split("_")[1:]
    await bot.send_message(
        chat_id=user_id,
        text="Siz to'lov qilmagansiz, iltimos to'lov qiling va qaytadan urinib ko'ring.",
        reply_markup=reply.find_udk
    )
    await call.message.delete()
