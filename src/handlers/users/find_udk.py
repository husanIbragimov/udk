import os
from datetime import date

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types.input_file import FSInputFile

from data.config import ADMINS, MEDIA_PATH
from keyboards import builders
from keyboards import reply
from utils.db.models import Order, Payment
from utils.dwd_file import download_file
from utils.states import UDK

router = Router()


@router.message(F.text == "🔍 UDK ni aniqlash")
async def find_udk(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Iltimos to'lov qiling va rasmini shu yerga yuklang.", reply_markup=reply.rmk)
    order = await Order.create(
        user_id=message.from_user.id,
    )
    payment = await Payment.create(
        order_id=order.id,
    )
    await state.set_state(UDK.check_image)
    # await state.update_data(order_id=order.id, payment_id=payment.id)


@router.message(UDK.check_image)
async def check_image(message: Message, state: FSMContext, bot: Bot):
    print(message.json())
    save_path = f"{MEDIA_PATH}/{message.from_user.id}-{date.today()}.jpg"

    await download_file(message, bot, save_path)

    data = await state.get_data()
    pk = data.get("payment_id")
    order_id = data.get("order_id")

    await Payment.filter(id=pk).update(
        check_image=save_path,
        is_paid=False,
    )
    await state.update_data(check_image=save_path)
    checking = await builders.inline_kb(
        ["✅ Tasdiqlash", "❌ Rad etish"],
        [f"confirm_{order_id}_{message.from_user.id}", f"reject_{order_id}_{message.from_user.id}"],
    )
    if os.path.exists(save_path):
        for admin in ADMINS:
            await bot.send_photo(
                chat_id=admin,
                photo=FSInputFile(path=save_path),
                caption=f"Yangi UDK aniqlash so'rovi: {message.from_user.full_name}",
                reply_markup=checking
            )
    else:
        await message.answer("Rasmni yuklashda xatolik yuz berdi. Iltimos qaytadan urinib ko'ring.")
        await state.clear()
        return


@router.callback_query(F.data.startswith("confirm_"))
async def confirm_udk(call: CallbackQuery, bot: Bot):
    order_id, user_id = call.data.split("_")[1:]
    await bot.send_message(
        chat_id=user_id,
        text="Hay, sizning UDK raqamingiz: 1234567890",
        reply_markup=reply.find_udk
    )
    await call.message.delete()


@router.callback_query(F.data.startswith("reject_"))
async def reject_udk(call: CallbackQuery, bot: Bot):
    order_id, user_id = call.data.split("_")[1:]
    await bot.send_message(
        chat_id=user_id,
        text="Siz to'lov qilmagansiz, iltimos to'lov qiling va qaytadan urinib ko'ring.",
        reply_markup=reply.find_udk
    )
    await call.message.delete()
