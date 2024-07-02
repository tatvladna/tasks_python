from aiogram.fsm.state import StatesGroup, State

# можно разбить на разные файлы

class MyStates(StatesGroup):
    wait_chembl_id = State()  #  oжидание id
    wait_chembl_title = State()  # ожидание названия
    wait_chembl_inchi = State() # ожидание INCHI

    #================
    wait_download = State()
    wait_download_text = State()
    wait_download_sdf = State()
    wait_download_smi = State()
    wait_download_csv = State()
    wait_download_png = State()

    # =========
    wait_stand = State()
    wait_descriptors = State()