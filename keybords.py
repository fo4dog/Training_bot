from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


# клава регистрации
def get_keyboard_registr():
    buttons = [
        [types.InlineKeyboardButton(text="Ronin", callback_data="reg_Ronin")],
        [types.InlineKeyboardButton(text="Темп-1", callback_data="reg_Tемп-1")],
        [types.InlineKeyboardButton(text="Темп", callback_data="reg_Темп")],
        [types.InlineKeyboardButton(text="Престиж", callback_data="reg_Престиж")],
        [types.InlineKeyboardButton(text="RedHeads", callback_data="reg_RedHeads")],
        [types.InlineKeyboardButton(text="Reserve", callback_data="reg_Reserve")],
        [types.InlineKeyboardButton(text="Без команды", callback_data="reg_Без команды")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard



# клава main
def get_keyboard_main(admin):
    buttons = [
        [types.InlineKeyboardButton(text="Команды", callback_data="choice_team")],
        [types.InlineKeyboardButton(text="Тренировки", callback_data="trainings")]
    ]
    if admin:
        buttons.append([types.InlineKeyboardButton(text="Админка", callback_data="admin")])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

# -------------------
# клава для выбора команд 
def get_keyboard_teams():
    buttons = [
        [types.InlineKeyboardButton(text="Ronin", callback_data="team_Ronin")],
        [types.InlineKeyboardButton(text="Темп-1", callback_data="team_Темп-1")],
        [types.InlineKeyboardButton(text="Темп", callback_data="team_Темп")],
        [types.InlineKeyboardButton(text="Престиж", callback_data="team_Престиж")],
        [types.InlineKeyboardButton(text="RedHeads", callback_data="team_RedHeads")],
        [types.InlineKeyboardButton(text="Reserve", callback_data="team_Reserve")],
        [types.InlineKeyboardButton(text="Назад", callback_data="menu")]
    ]
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
# --------------------


def get_keyboard_trainings_menu():
    buttons = [
        [types.InlineKeyboardButton(text="Записаться на тренировку", callback_data="training_mark")],
        [types.InlineKeyboardButton(text="Кто будет на тренировке?", callback_data="training_cheak")],
        [types.InlineKeyboardButton(text="Назад", callback_data="menu")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
# ------------------

# авто подгрузка клавы команды
def get_team_keyboard(action, team):
    buttons = []
    buttons.append([types.InlineKeyboardButton(text="Статистика", callback_data=f"statistika_{team}")])
    buttons.append([types.InlineKeyboardButton(text="Видео", callback_data=f"video_{team}")])
    for row in action:
        if "Статистика" not in row[2] and "Видео" not in row[2]:
            buttons.append([types.InlineKeyboardButton(text=row[2], url=row[3])])
    buttons.append([types.InlineKeyboardButton(text="Назад", callback_data="choice_team")])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


# авто подгрузка статы
def get_statistika_keyboard(action, team):
    buttons = []
    for row in action:
        if "Статистика" in row[2]:
            buttons.append([types.InlineKeyboardButton(text=row[2], url=row[3])])
    buttons.append([types.InlineKeyboardButton(text="Назад", callback_data=f"team_{team}")])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


# авто подгрузка тренировок 
def get_keyboard_timetable(trainings):
    buttons = []
    for row in trainings:
        buttons.append([types.InlineKeyboardButton(text=f"{row[1]} в {row[2]}, цена {row[4]}, тип тренировки {row[3]}", callback_data=f"mark_{row[5]}")])
    buttons.append([types.InlineKeyboardButton(text="Назад", callback_data="trainings")])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard                 

#   авто подгрузка тренрировок для просмотра кто будет на трене 
def get_keyboard_check_who_in(trainings):
    buttons = []
    for row in trainings:
        buttons.append([types.InlineKeyboardButton(text=f"{row[1]} в {row[2]}, цена {row[4]}, тип тренировки {row[3]}", callback_data=f"check_{row[5]}")])
    buttons.append([types.InlineKeyboardButton(text="Назад", callback_data="trainings")])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard        

def admin_menu_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text="Создать тренировку", callback_data="admin_create_training")],
        [types.InlineKeyboardButton(text="Добавить раздел команде", callback_data="admin_create_team_action")],
        [types.InlineKeyboardButton(text="Сделать оповещение команде", callback_data="admin_create_team_notify")],
        [types.InlineKeyboardButton(text="Сделать пользователя админом", callback_data="admin_create_admin")],
        [types.InlineKeyboardButton(text="Назад", callback_data="menu")]
    ]
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard