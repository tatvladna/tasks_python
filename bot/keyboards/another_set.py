from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def create_button():

    button_1 = InlineKeyboardButton(
        text='Set with molecular weight less than 300',
        callback_data='weight'
    )
    button_2 = InlineKeyboardButton(
        text="Molecules according to Lipinski's rule",
        callback_data='lipinski'
    )

    button_3 = InlineKeyboardButton(
        text='Approved drugs',
        callback_data='approved'
    )


    # Создаем объект инлайн-клавиатуры
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_1],
                         [button_2],
                         [button_3]]
    )
    return keyboard