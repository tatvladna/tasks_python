
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from chembl_webresource_client.new_client import new_client
from custom_states import MyStates

from keyboards import some_options
from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section, as_key_value, HashTag
)
from aiogram.types import CallbackQuery
from handlers import molecule


router = Router()

@router.callback_query(F.data=='operation')
async def download(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Select the format in which you want to save the information',reply_markup=keyboard_some_operation.create_inline_kb(2, 'but_1', 'but_3', 'but_7').start)
    await callback.answer()
