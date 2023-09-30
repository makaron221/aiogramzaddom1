import asyncio
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, CommandStart, Filter
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from dbinit import conn
from aiogram.enums import ParseMode

TOKEN = "6385333718:AAGKKVQ13u2XmEWTqe4NOreFm4DNcPOhvBI"
form_router = Router()

class Form(StatesGroup):
    name = State()
    surname = State()
    phone_num = State()


@form_router.message(CommandStart())
async def command_start(message:Message, state:FSMContext):
    await state.set_state(Form.name)
    await message.answer(f"добрий день {hbold(message.from_user.first_name)}, введіть своє ім'я")

@form_router.message(Form.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.surname)
    await message.answer("введіть своє прізвище")

@form_router.message(Form.surname)
async def get_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await state.set_state(Form.phone_num)
    await message.answer("введіть свій номер телефону")

@form_router.message(Form.phone_num)
async def get_phnum(message: Message, state: FSMContext):
    if "+" not in message.text:
        await message.answer("ви не ввели код країни, спробуйте ще раз")
    else:
        data = await state.update_data(phone_num=message.text)
        await state.clear()
        conn.execute("INSERT INTO pdata VALUES(?, ?, ?)", [data.get(i) for i in data])
        await message.answer("done")

    

@form_router.message(Command("show"))
async def command_start(message:Message, state:FSMContext):
    await message.answer(str(conn.execute("SELECT * FROM pdata").fetchall())[1:-1])


async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(form_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())