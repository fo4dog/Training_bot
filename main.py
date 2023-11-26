import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder



from config_reader import config

from db import BotDB

import keybords

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
# Подключение к БД
BotDB = BotDB('database.db')
# Диспетчер
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Для завершения регистрации, выберите комаду или без команды", reply_markup=keybords.get_keyboard_registr())

# рег


@dp.callback_query(F.data.startswith('reg_'))
async def callbacks_num(callback: types.CallbackQuery):
    user_id = callback.from_user.id


    if BotDB.user_exists(user_id):
        await callback.message.answer(f"Ваш пользователь уже был зарегестрирован ранее")
        admin = BotDB.get_user_admin_by_user_id(user_id)
        await callback.message.answer(f"Меню", reply_markup=keybords.get_keyboard_main(admin))

    else:
        # Получение инфы о юзере
        user_name = callback.from_user.first_name
        user_lastname = callback.from_user.last_name
        team = callback.data.split("_")[1]
        team_id = BotDB.get_team_id(team)

        BotDB.add_user(user_id, user_name, user_lastname, team_id)
        await callback.message.answer(f"Пользователь {user_name} {user_lastname} зарегестрирован")
        admin = BotDB.get_user_admin_by_user_id(user_id)
        await callback.message.answer(f"Меню", reply_markup=keybords.get_keyboard_main(admin))

# колбэк главного меню
# ------------------------------------------
@dp.callback_query(F.data == 'menu')
async def main_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    admin = BotDB.get_user_admin_by_user_id(user_id)
    await callback.message.answer(f"Меню", reply_markup=keybords.get_keyboard_main(admin))

# колбэки главного меню
# ------------------------------------------

@dp.callback_query(F.data == "choice_team")
async def send_teams(callback: types.CallbackQuery):
    await callback.message.answer("Выберите команду", reply_markup=keybords.get_keyboard_teams())



# колбэки меню тренировок
# ------------------------------------------
@dp.callback_query(F.data == "trainings")
async def send_trainings(callback: types.CallbackQuery):
    await callback.message.answer("Выберите интересующий вас раздел тренировок", reply_markup=keybords.get_keyboard_trainings_menu())


# ------------------------------------------


# колбэки главного меню команд
# ------------------------------------------

@dp.callback_query(F.data.startswith('team_'))
async def team_menu(callback: types.CallbackQuery):
    team = callback.data.split("_")[1]
    team_id = BotDB.get_team_id(team)
    action = BotDB.get_team_action(team_id)
    await callback.message.answer(f"Меню команды {team}", reply_markup=keybords.get_team_keyboard(action, team))





# ------------------------------------------
# колбэки статистики и видео команд
# ------------------------------------------

@dp.callback_query(F.data.startswith('statistika_'))
async def stat_menu(callback: types.CallbackQuery):
    team = callback.data.split("_")[1]
    team_id = BotDB.get_team_id(team)
    action = BotDB.get_team_action(team_id)
    await callback.message.answer(f"Статистика команды {team}", reply_markup=keybords.get_statistika_keyboard(action, team))


@dp.callback_query(F.data.startswith('video_'))
async def stat_menu(callback: types.CallbackQuery):
    team = callback.data.split("_")[1]
    team_id = BotDB.get_team_id(team)
    action = BotDB.get_team_action(team_id)
    await callback.message.answer(f"Видео команды {team}", reply_markup=keybords.get_statistika_keyboard(action, team))




# ------------------------------------------
# колбэки просмотра меню отметки тренировок
# ------------------------------------------
@dp.callback_query(F.data == "training_mark")
async def train_menu(callback: types.CallbackQuery):
    forward_date = callback.message.date
    formatted_date = forward_date.strftime("%d.%m.%Y")
    trainings = BotDB.get_trainings(formatted_date)
    await callback.message.answer("Тренировки", reply_markup=keybords.get_keyboard_timetable(trainings))
# колбэки просмотра меню кто будет
# ------------------------------------------

@dp.callback_query(F.data == "training_cheak")
async def send_trainings(callback: types.CallbackQuery):
    forward_date = callback.message.date
    formatted_date = forward_date.strftime("%d.%m.%Y")
    trainings = BotDB.get_trainings(formatted_date)
    await callback.message.answer("Тренировки", reply_markup=keybords.get_keyboard_check_who_in(trainings))
# колбэки отметки на тренировку
# ------------------------------------------

@dp.callback_query(F.data.startswith('mark_'))
async def mark_on_trainings(callback: types.CallbackQuery):
    training_id = callback.data.split("_")[1]
    user_id = callback.from_user.id
    if BotDB.exist_mark_on_trainings(user_id, training_id):
        await callback.message.answer(f"Ваш пользователь уже был зарегестрирован на тренировку")
        admin = BotDB.get_user_admin_by_user_id(user_id)
        await callback.message.answer(f"Меню", reply_markup=keybords.get_keyboard_main(admin))
    else:
        BotDB.mark_on_trainings(user_id, training_id)
        admin = BotDB.get_user_admin_by_user_id(user_id)
        await callback.message.answer("Вы записались на тренировку", reply_markup=keybords.get_keyboard_main(admin))


# колбэки просмотра кто будет на трене
# ------------------------------------------

@dp.callback_query(F.data.startswith('check_'))
async def check_mark_on_trainings(callback: types.CallbackQuery):
    training_id = callback.data.split("_")[1]
    users_id = BotDB.check_mark_on_trainings(training_id)
    message = ""
    await callback.message.answer("На тренировке будут:")
    for user_id in users_id:
        us_id = BotDB.get_user_by_user_id(user_id[0])
        message += f"{us_id[1]} {us_id[2]}\n"
    await callback.message.answer(message)
    user_id = callback.from_user.id
    admin = BotDB.get_user_admin_by_user_id(user_id)
    await callback.message.answer(f"Меню", reply_markup=keybords.get_keyboard_main(admin))
# Запуск процесса поллинга новых апдейтов


# admin menu
# -----------------
@dp.callback_query(F.data == "admin")
async def admin_menu_hendler(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    admin = BotDB.get_user_admin_by_user_id(user_id)
    if admin:
        await callback.message.answer(f"Админское Меню", reply_markup=keybords.admin_menu_keyboard())
    else:
        await callback.message.answer(f"Вы не администратор", reply_markup=keybords.get_keyboard_main(admin))
async def main():
    await dp.start_polling(bot)


# admin menu
# -----------------

# добавление тренировок
# -----------------
@dp.callback_query(F.data == "admin_create_training")
async def admin_create_training_hendler(callback: types.CallbackQuery):
    intro = '''<b>Чтобы добавить тренировку, нужно написать !new_training: и далее ввести информацию о тренировке</b>\nПример:\n'''
    ans = '!new_training: Дата, Время, Тип тренировки, Стоимость'
    prim = '!new_training: 21.11.2023, 19:00, игровая(или обычная), 400'
    await callback.message.answer(intro)
    await callback.message.answer(ans)
    await callback.message.answer(prim)

# -----------------
# отработчик добавления тренировки

@dp.message(F.text.startswith("!new_training:"))
async def cmd_new_training(message: types.Message):
    new_tr = message.text.split(',')
    user_id = message.from_user.id
    admin = BotDB.get_user_admin_by_user_id(user_id)
    if len(new_tr) == 4 and admin:
        date = new_tr[0].split(' ')[1]
        time = new_tr[1][1:]
        tp = new_tr[2][1:]
        coast = new_tr[3]
        id = BotDB.get_count_of_trainings()[0] + 1
        BotDB.add_trainings(id, date, time, tp, coast)
        await message.answer("Тренировка успешно добавлена в базу")  
    else:
        await message.answer("Данные введены не корректно или вы не админ")
    await message.answer(f"Меню", reply_markup=keybords.get_keyboard_main(admin))



# -----------------
# добавления иформации о команде
@dp.callback_query(F.data == "admin_create_team_action")
async def admin_create_team_action_hendler(callback: types.CallbackQuery):
    await callback.message.answer("<b>Чтобы добавить что-то в раздел команды, нужно:</b>")
    await callback.message.answer("Пример:")
    await callback.message.answer("!new_action: Название команды, название, ссылка")
    await callback.message.answer("!new_action: Ronin, Статистика Сезон 2022-2023, https://disk.yandex.ru/d/h2UE9y40UxXxKQ")


# -----------------
# отработчик добавления иформации о команде
@dp.message(F.text.startswith("!new_action:"))
async def cmd_new_action(message: types.Message):
    new_action = message.text.split(',')
    user_id = message.from_user.id
    admin = BotDB.get_user_admin_by_user_id(user_id)
    if len(new_action) == 3 and admin:
        team_name = new_action[0].split(' ')[1]
        name = new_action[1][1:]
        a = new_action[2][1:]
        team_id = BotDB.get_team_id(team_name)
        BotDB.add_team_action(team_id, name, a)
        await message.answer(f"Тренировка успешно добавлена в базу")  
    else:
        await message.answer("Данные введены не корректно или вы не админ")
    await message.answer(f"Меню", reply_markup=keybords.get_keyboard_main(admin))


# -----------------
# Рассылка
@dp.callback_query(F.data == "admin_create_team_notify")
async def admin_create_team_notify_hendler(callback: types.CallbackQuery):
    await callback.message.answer("<b>Чтобы сделать рассылку нужно:</b>")
    await callback.message.answer("Пример:")
    await callback.message.answer("!mailing: Название команды, Текст")
    await callback.message.answer("!mailing: Ronin(или all), отмечайтесь на тренировку")

# -----------------
# отработчик добавления иформации о команде
@dp.message(F.text.startswith("!mailing:"))
async def cmd_mailing(message: types.Message):
    new_action = message.text.split(',')
    user_id = message.from_user.id
    admin = BotDB.get_user_admin_by_user_id(user_id)
    if len(new_action) == 2 and admin:
        team_name = new_action[0].split(' ')[1]
        text = new_action[1][1:]
        if team_name != 'all':
            team_id = BotDB.get_team_id(team_name)
            users = BotDB.get_user_id_by_team_id(team_id)
        else:
            users = BotDB.get_all_user_id_by_team_id()

        for user in users:
            
            await bot.send_message(user[0], text)

        await message.answer(f"Рассылка выполнена")  
    else:
        await message.answer("Данные введены не корректно или вы не админ")
    await message.answer(f"Меню", reply_markup=keybords.get_keyboard_main(admin))

# -----------------
# Создание админа
@dp.callback_query(F.data == "admin_create_admin")
async def cmd_create_new_admin(callback: types.CallbackQuery):
    await callback.message.answer("<b>Чтобы создать админа:</b>")
    await callback.message.answer("Пример:")
    await callback.message.answer("!admin: Имя, Фамилия, Пароль админа")
    await callback.message.answer("!admin: Елизавета, Петрушина, блаблабла")

# -----------------
# отработчик создания админа
@dp.message(F.text.startswith("!admin:"))
async def cmd_mailing(message: types.Message):
    new_action = message.text.split(',')
    user_id = message.from_user.id
    admin = BotDB.get_user_admin_by_user_id(user_id)

    if len(new_action) == 3 and admin:
        user_name = new_action[0].split(' ')[1]
        user_last_name = new_action[1][1:]
        password = new_action[2][1:]
        if password == config.admin_password.get_secret_value():
            BotDB.add_admin_by_name(user_name, user_last_name)
            await message.answer(f"{user_name} {user_last_name} теперь админ")
        else:
            await message.answer(f"Неверный пароль!")
    else:
        await message.answer("Данные введены не корректно или вы не админ")
    await message.answer(f"Меню", reply_markup=keybords.get_keyboard_main(admin))




if __name__ == "__main__":
    asyncio.run(main())
