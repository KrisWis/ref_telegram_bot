from InstanceBot import bot
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from database import db

async def start(msg: types.Message):
    bot_name = await bot.get_me()
    user_id = msg.from_user.id
    username = msg.from_user.username
    start_message = msg.text[7:]

    if not db.user_exists(user_id):
        if len(start_message) > 0:
            if start_message.isdigit():

                db.add_user(user_id, ref_id=start_message)

                await bot.send_message(
                    chat_id=start_message,
                    text=f'У Вас новый реферал @{username}!'
                )

        else:
            db.add_user(user_id)

    user_balance = db.get_balance(user_id)

    await msg.answer(f"Приветствую тебя! \nТвоя реферальная ссылка - t.me/{bot_name.username}?start={user_id} \
                    \nТвой баланс: {user_balance} \nДля пополнения баланса - /balance")


async def balance(msg: types.Message):
    user_id = msg.from_user.id
    username = msg.from_user.username
    amount = 10

    db.change_balance(user_id, amount)

    await msg.answer(f"Твой баланс пополнен на {amount} монет!")

    user_referrer = db.get_referrer(user_id)[0]
    while user_referrer and amount > 2:
        amount = amount / 2
        db.change_balance(user_referrer, amount)

        await bot.send_message(user_referrer, f"Твой реферал @{username} получил на баланс {amount * 2} монет, поэтому твой баланс пополнен на {amount} монет!")
        user_referrer = db.get_referrer(user_referrer)[0]


def hand_add(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"], state="*")
    dp.register_message_handler(balance, commands=["balance"], state="*")