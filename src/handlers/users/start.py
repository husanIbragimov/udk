from aiogram import Bot, F
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.types.chat_member_owner import ChatMemberStatus

from data.config import CHANNEL_ID
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
    await message.answer("Ushbu bot orqali siz UDKni aniqlashingiz mumkin ('🔍 UDK ni aniqlash' tugmasini bosing)", reply_markup=reply.find_udk)

@router.callback_query(F.data.startswith("check_subscription"))
async def check_subscription(call: CallbackQuery, bot: Bot):
    for channel in CHANNEL_ID:
        chat_member = await bot.get_chat_member(
            chat_id=channel,
            user_id=call.from_user.id
        )
        print("chat_member", chat_member, call.from_user.id)
        if chat_member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR, ChatMemberStatus.MEMBER]:
            await call.message.answer(
                "Ushbu bot orqali siz UDKni aniqlashingiz mumkin ('🔍 UDK ni aniqlash' tugmasini bosing)",
                reply_markup=reply.find_udk
            )
