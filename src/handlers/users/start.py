from aiogram import Router, types
from aiogram.filters import CommandStart
from keyboards import reply
from utils.db.models import User

router = Router()

@router.message(CommandStart())
async def register_user(message: types.Message):
    await User.get_or_create(
        telegram_id=message.from_user.id,
        id=message.from_user.id,
        defaults={"username": message.from_user.username}
    )
    print("User registered:", message.from_user.id)
    await message.answer("Ushbu bot orqali siz UDKni topishingiz mumkin.", reply_markup=reply.find_udk)
