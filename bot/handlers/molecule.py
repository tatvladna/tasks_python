# Хэндлер — асинхронная функция, которая получает от диспетчера/роутера
# очередной апдейт и обрабатывает его.



from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from chembl_webresource_client.new_client import new_client
from custom_states import MyStates
# from keyboard.keyboard import Keyboard
from keyboards import main_download
from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section, as_key_value, HashTag
)
from aiogram.types import CallbackQuery
from CGRtools import SDFWrite, smiles
from io import StringIO, BytesIO
from aiogram.types import input_file  # специальная библиотека дял записи локальных файлов
from aiogram.types import InputFile


from rdkit import Chem
from rdkit.Chem.Draw import IPythonConsole
from rdkit.Chem.Draw import rdMolDraw2D
from rdkit.Chem import Draw
IPythonConsole.ipython_useSVG=True


from keyboards import some_options
from keyboards import another_set

from chembl_webresource_client.utils import utils
import json
from chembl_webresource_client.utils import utils
import json



# Диспетчер — объект, занимающийся получением апдейтов от
# Telegram с последующим выбором хэндлера для обработки принятого апдейта.
# Роутер — аналогично диспетчеру, но отвечает за подмножество множества хэндлеров.
# Можно сказать, что диспетчер — это корневой роутер.
router = Router()

# реакция на команду "/start"
# Command('start') - фильтр
# Фильтр — выражение, которое обычно возвращает True или False и влияет на то,
# будет вызван хэндлер или нет.
@router.message(Command('start'))
async def start(message: Message):
    # keyboard = [
    #     [KeyboardButton(text='By name'),
    #      KeyboardButton(text='By CHEMBL ID')]
    # ]
    # kb = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    await message.answer('Choose search type', reply_markup=main_download.Keyboard().start)

# ============  ID  ==============

@router.message(F.text=='By ID')
async def by_id(message: Message, state: FSMContext):
    await message.answer('Type CHEMBL ID of molecule',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(MyStates.wait_chembl_id)


@router.message(StateFilter(MyStates.wait_chembl_id))
async def by_id(message: Message, state: FSMContext):
    id = message.text
    molecule = new_client.molecule
    result = molecule.filter(molecule_chembl_id=f'CHEMBL{id}').only(['molecule_chembl_id', 'molecule_structures', 'pref_name', 'molecule_properties'])
    if result:
        content = as_list(
            as_marked_section(
                Bold("Brief Information:"),
                f"CHEMBL ID: {result[0]['molecule_chembl_id']}",
                f"Smiles: {result[0]['molecule_structures']['canonical_smiles']}",
                f"InChi: {result[0]['molecule_structures']['standard_inchi_key']}",
                f"Title: {result[0]['pref_name']}",
                f"Full molformula: {result[0]['molecule_properties']['full_molformula']}",
                f"Full mwt: {result[0]['molecule_properties']['full_mwt']}",
                marker="💞 ",
            ),

            HashTag("#information"),
            sep="\n\n",
        )
        await message.answer(**content.as_kwargs(), reply_markup=main_download.InlineKeyboard().start)
        # все, что хранится в result[0], сохраняем в State
        await state.update_data(molecule=result[0])  # обновляет словарь данных внутри объекта State
    else:
        await message.answer('Sorry. No results')



# ============ title =======================

@router.message(F.text=='By title')
async def by_title(message: Message, state: FSMContext):
    await message.answer('Type CHEMBL title of molecule',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(MyStates.wait_chembl_title)


@router.message(StateFilter(MyStates.wait_chembl_title))
async def by_title(message: Message, state: FSMContext):
    # print('!!!')
    # title = message.text
    molecule = new_client.molecule
    result = molecule.filter(pref_name__iexact=message.text).only(['molecule_chembl_id', 'molecule_structures', 'pref_name', 'molecule_properties'])
    if result:
        content = as_list(
            as_marked_section(
                Bold("Brief Information:"),
                f"CHEMBL ID: {result[0]['molecule_chembl_id']}",
                f"Smiles: {result[0]['molecule_structures']['canonical_smiles']}",
                f"InChi: {result[0]['molecule_structures']['standard_inchi_key']}",
                f"Title: {result[0]['pref_name']}",
                f"Full molformula: {result[0]['molecule_properties']['full_molformula']}",
                f"Full mwt: {result[0]['molecule_properties']['full_mwt']}",
                marker="🍓 ",
            ),

            HashTag("#information"),
            sep="\n\n",
        )
        await message.answer(**content.as_kwargs(), reply_markup=main_download.InlineKeyboard().start)
        # все, что хранится в result[0], сохраняем в State
        await state.update_data(molecule=result[0])  # обновляет словарь данных внутри объекта State
    else:
        await message.answer('Sorry. No results')

# ================   InChi   ==================

@router.message(F.text=='By InChi')
async def by_inchi(message: Message, state: FSMContext):
    await message.answer('Type CHEMBL InChi of molecule',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(MyStates.wait_chembl_inchi)


@router.message(StateFilter(MyStates.wait_chembl_inchi))
async def by_inchi(message: Message, state: FSMContext):
    # print('!!!')
    # title = message.text
    molecule = new_client.molecule
    result = molecule.filter(molecule_structures__standard_inchi_key=message.text).only(['molecule_chembl_id', 'molecule_structures', 'pref_name', 'molecule_properties'])
    if result:
        content = as_list(

            as_marked_section(
                Bold("Brief Information:"),
                f"CHEMBL ID: {result[0]['molecule_chembl_id']}",
                f"Smiles: {result[0]['molecule_structures']['canonical_smiles']}",
                f"InChi: {result[0]['molecule_structures']['standard_inchi_key']}",
                f"Title: {result[0]['pref_name']}",
                f"Full molformula: {result[0]['molecule_properties']['full_molformula']}",
                f"Full mwt: {result[0]['molecule_properties']['full_mwt']}",
                marker="🍩 ",
            ),

            HashTag("#information"),
            sep="\n\n",
        )
        await message.answer(**content.as_kwargs(), reply_markup=main_download.InlineKeyboard().start)
        # все, что хранится в result[0], сохраняем в State
        await state.update_data(molecule=result[0])  # обновляет словарь данных внутри объекта State
        # await state.clear()
    else:
        await message.answer('Sorry. No results')


# =========================

@router.callback_query(F.data=='download')
async def download(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Select the format in which you want to save the information',reply_markup=main_download.AdvencedInformation().start)
    await callback.answer()


    # await callback.message.edit_text()
    # await state.set_state(MyStates.wait_download)
    # await callback.answer(reply_markup=keyboard.AdvencedInformation().start)
    # await state.set_state(MyStates.wait_download)
    # await message.answer(reply_markup=keyboard.AdvencedInformation().start)
    # await state.set_state(MyStates.wait_download)
    # await callback.answer(reply_markup=keyboard.AdvencedInformation().start)
    # await state, reply_markup = keyboard.AdvencedInformation().start


# @router.message(StateFilter(MyStates.wait_download))
# async def download(message: Message, state: FSMContext):
#     await message.answer(reply_markup=keyboard.AdvencedInformation().start)
#     await state.clear()


@router.callback_query(F.data == "sdf")
async def sdf(callback: CallbackQuery, state: FSMContext):
    molecule = await state.get_data()
    print(molecule)
    file = StringIO()
    with SDFWrite(file) as f:
        f.write(smiles(molecule['molecule']['molecule_structures']['canonical_smiles']))
        file.seek(0)

    await callback.message.answer_document(input_file.BufferedInputFile(BytesIO(file.read().encode("utf-8")).getbuffer(),
                                                                        filename=f"{molecule['molecule']['molecule_chembl_id']}.sdf"))

    await callback.message.delete()
    await state.set_state({})
    await callback.answer()


@router.callback_query(F.data == "txt")
async def sdf(callback: CallbackQuery, state: FSMContext):
    molecule = await state.get_data()
    print(molecule)
    file = StringIO(f"Brief Information:\n"
                f"CHEMBL ID: {molecule['molecule']['molecule_chembl_id']}\n"
                f"Smiles: {molecule['molecule']['molecule_structures']['canonical_smiles']}\n"
                f"InChi: {molecule['molecule']['molecule_structures']['standard_inchi_key']}\n"
                f"Title: {molecule['molecule']['pref_name']}\n"
                f"Full molformula: {molecule['molecule']['molecule_properties']['full_molformula']}\n"
                f"Full mwt: {molecule['molecule']['molecule_properties']['full_mwt']}\n")


    await callback.message.answer_document(input_file.BufferedInputFile(BytesIO(file.read().encode("utf-8")).getbuffer(),
                                                                        filename=f"{molecule['molecule']['molecule_chembl_id']}.txt"))

    await callback.message.delete()
    await state.set_state({})
    await callback.answer()





# не работает
@router.callback_query(F.data == "png")
async def sdf(callback: CallbackQuery, state: FSMContext):
    molecule = await state.get_data()
    # print(molecule)
    # file = StringIO()
    formula = Chem.MolFromSmiles(molecule['molecule']['molecule_structures']['canonical_smiles'])
    d = rdMolDraw2D.MolDraw2DCairo(300, 300)
    d.DrawMolecule(formula)
    d.FinishDrawing()
    png = d.GetDrawingText()
    open('formula.png', 'wb+').write(png)

    await callback.send_photo(photo=InputFile("formula.png"))

    await callback.message.delete()
    await state.set_state({})
    await callback.answer()



@router.callback_query(F.data=='options')
async def options(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Select another options',reply_markup=some_options.create_button())
    await callback.answer()


@router.callback_query(F.data=='extract')
async def extract(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Select another options',reply_markup=another_set.create_button())
    await callback.answer()



@router.callback_query(F.data=='standardize')
async def standardize(callback: CallbackQuery, state: FSMContext):

    molecule = await state.get_data()
    smiles = molecule['molecule']['molecule_structures']['canonical_smiles']
    mol = utils.smiles2ctab(smiles)
    # Преобразуйте JSON строку в словарь
    st = json.loads(utils.standardize(mol))

    result = []
    for k, v in st[0].items():
        result.append("{}: {}".format(k, v))
    res = "; ".join(result)
    res

    file = StringIO(res)

    await callback.message.answer_document(
        input_file.BufferedInputFile(BytesIO(file.read().encode("utf-8")).getbuffer(),
                                     filename=f"{molecule['molecule']['molecule_chembl_id']}.txt"))
    await callback.answer()



@router.callback_query(F.data=='descriptor')
async def standardize(callback: CallbackQuery, state: FSMContext):
    molecule = await state.get_data()
    smiles = molecule['molecule']['molecule_structures']['canonical_smiles']
    answer = utils.smiles2ctab(smiles)
    descs = json.loads(utils.chemblDescriptors(answer))[0]
    result = []
    for k, v in descs.items():
        result.append("{}: {}".format(k, v))
    res = "; ".join(result)
    res

    file = StringIO(res)

    await callback.message.answer_document(
        input_file.BufferedInputFile(BytesIO(file.read().encode("utf-8")).getbuffer(),
                                     filename=f"{molecule['molecule']['molecule_chembl_id']}.txt"))
    await callback.answer()




@router.callback_query(F.data=='similar')
async def standardize(callback: CallbackQuery, state: FSMContext):

    molecule = await state.get_data()
    smiles = molecule['molecule']['molecule_structures']['canonical_smiles']
    similarity = new_client.similarity
    res = similarity.filter(smiles=smiles, similarity=70).only(
        ['molecule_chembl_id', 'similarity'])

    result = []
    for k, v in res[0].items():
        result.append("{}: {}".format(k, v))
    res = "; ".join(result)
    res

    file = StringIO(res )

    await callback.message.answer_document(
        input_file.BufferedInputFile(BytesIO(file.read().encode("utf-8")).getbuffer(),
                                     filename=f"{molecule['molecule']['molecule_chembl_id']}.txt"))
    await callback.answer()




@router.callback_query(F.data=='extract')
async def options(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('What set of molecules do you want to extract?',reply_markup=another_set.create_button())
    await callback.answer()



@router.callback_query(F.data=='weight')
async def options(callback: CallbackQuery, state: FSMContext):
    molecule = new_client.molecule
    light_molecules = molecule.filter(molecule_properties__mw_freebase__lte=300).only(['molecule_chembl_id', 'pref_name'])

    # def f(d):
    #     return '\n'.join('{}: {}'.format(k, v) for k, v in d.items())
    #
    # txt = '\n\n'.join(map(f, light_molecules))

    file = StringIO( f'Количество молекул, у которых МВ меньше 300: {len(light_molecules)}')

    await callback.message.answer_document(
        input_file.BufferedInputFile(BytesIO(file.read().encode("utf-8")).getbuffer(),
                                     filename=f"light_molecules.txt"))
    await callback.answer()











