from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_button():

    button_1 = InlineKeyboardButton(
        text='Search for a similar molecule',
        callback_data='similar'
    )
    button_2 = InlineKeyboardButton(
        text='Standardize the molecule',
        callback_data='standardize'
    )
    button_3 = InlineKeyboardButton(
        text='Various molecular descriptors',
        callback_data='descriptor'
    )

    button_4 = InlineKeyboardButton(
        text='Extract another set of molecules',
        callback_data='extract'
    )

    # Создаем объект инлайн-клавиатуры
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_1],
                         [button_2],
                         [button_3],
                         [button_4]]
    )
    return keyboard