from aiogram import Bot, F
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards import reply
from utils.db.models import User
from utils.services import user_is_member

router = Router()

@router.message(CommandStart())
async def register_user(message: Message, bot: Bot):
    await User.get_or_create(
        telegram_id=message.from_user.id,
        id=message.from_user.id,
        defaults={"username": message.from_user.username}
    )
    await user_is_member(message, bot)
    await message.answer("Ushbu bot orqali siz UDKni aniqlashingiz mumkin.", reply_markup=reply.find_udk)

@router.callback_query(F.data.startswith("check_subscription"))
async def check_subscription(call: CallbackQuery, bot: Bot):
    print("check_subscription")
    await call.message.delete()
    if await user_is_member(call.message, bot) is True:
        await call.message.answer("Ushbu bot orqali siz UDKni topishingiz mumkin.", reply_markup=reply.find_udk)

