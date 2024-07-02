from aiogram import types
# from aiogram.filters import Command
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class Keyboard:
    @property
    def start(self):
        keyboard = [
            [types.KeyboardButton(text='By title', callback_data="title"),
             types.KeyboardButton(text='By ID', callback_data='id'),
             types.KeyboardButton(text="By InChi", callback_data="inchi")]
        ]
        return types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

class InlineKeyboard:
    @property
    def start(self):

        inline_keyboard = [
            [types.InlineKeyboardButton(text='Some options', callback_data='options'),
             types.InlineKeyboardButton(text="Download", callback_data="download"),]
        ]
        return types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)




class AdvencedInformation:
    @property
    def start(self):

        inline_keyboard2 = [
            [types.InlineKeyboardButton(text='txt', callback_data="txt"),
             types.InlineKeyboardButton(text='sdf', callback_data='sdf'),
             types.InlineKeyboardButton(text="smi", callback_data="smi"),
             types.InlineKeyboardButton(text="csv", callback_data="csv"),
             types.InlineKeyboardButton(text="png", callback_data="png")]
        ]
        return types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard2)

