import sqlite3


class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
    

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT 'id' FROM 'users' WHERE user_id = ?", (user_id,))
        return bool(len(result.fetchall()))
    

    def get_user_id(self, user_id):
        """Получаем id юзера в базе по ego user_id в телеграме"""
        result = self.cursor.execute("SELECT 'id' FROM 'users' WHERE user_id = ?", (user_id,)) 
        return result.fetchone()[0]
    

    def get_all_user_id_by_team_id(self):
        """Получаем user_id по team_id"""
        result = self.cursor.execute("SELECT user_id FROM 'users'") 
        return result.fetchall()


    def get_user_id_by_team_id(self, team_id):
        """Получаем user_id по team_id"""
        result = self.cursor.execute("SELECT user_id FROM 'users' WHERE team_id = ?", (team_id,)) 
        return result.fetchall()

    def get_user_admin_by_user_id(self, user_id):
        """Получаем admin юзера в базе по ego user_id в телеграме"""
        result = self.cursor.execute("SELECT 'admin' FROM 'users' WHERE user_id = ?", (user_id,)) 
        return result.fetchone()[0]
    
    def add_admin_by_name(self, user_name, user_lastname):
        """Создаем пдмина из пользователя по имени и фамилии"""
        self.cursor.execute('''UPDATE users SET admin = ? WHERE (user_name = ? and user_lastname = ?)''', (1, user_name, user_lastname))
        return self.conn.commit()
    
    def get_user_by_user_id(self, user_id):
        """Получаем id юзера в базе по ego user_id в телеграме"""
        result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) 
        return result.fetchone()
    

    def add_user(self, user_id, user_name, user_lastname, team_id):
        """Добавляем юзера в БД"""
        self.cursor.execute("INSERT INTO 'users' ('user_id', 'user_name', 'user_lastname', 'team_id') VALUES (?, ?, ?, ?)", (user_id, user_name, user_lastname, team_id)) 
        return self.conn.commit()
    

    def add_team(self, team_id):
        """Добавляем команду в БД"""
        self.cursor.execute("INSERT INTO 'teams' ('team_id') VALUES (?)", (team_id,)) 
        return self.conn.commit()
    

    def get_team_id(self, team_name):
        """находим команду в БД"""
        result = self.cursor.execute("SELECT * FROM 'teams' WHERE team_name = ?", (team_name,)) 
        return result.fetchone()[1]
    
    def add_team_action(self, team_id, name, a):
        # добавление team_action
        self.cursor.execute("INSERT INTO 'team_action' ('team_id', 'name_of_action', 'info_about_action') VALUES (?, ?, ?)", (team_id, name, a,)) 
        return self.conn.commit()
    
    def get_team_action(self, team_id):
        result = self.cursor.execute("SELECT * FROM 'team_action' WHERE team_id = ?", (team_id,))
        return result.fetchall()
    

    def add_trainings(self, id, date, time, tp, coast):
        # Создание тренировки 
        self.cursor.execute("INSERT INTO 'trainings' ('id', 'training_day', 'training_time', 'training_type', 'training_price', 'training_id') VALUES (?, ?, ?, ?, ?, ?)", (id, date, time, tp, coast, id)) 
        return self.conn.commit()
    
    def get_trainings(self, date):
        result = self.cursor.execute("SELECT * FROM trainings WHERE training_day >= ?", (date,))
        return result.fetchall()
    
    def get_count_of_trainings(self):
        result = self.cursor.execute("SELECT count(*) FROM trainings")
        return result.fetchone()
        
    def mark_on_trainings(self, user_id, training_id):
        """Добавляем запись на тренировку в БД"""
        self.cursor.execute("INSERT INTO 'sign_up' ('training_id', 'user_id') VALUES (?, ?)", (training_id, user_id,)) 
        return self.conn.commit()
    
    def exist_mark_on_trainings(self, user_id, training_id):
        """Провеяем, есть ли пользователь в записи на треню в БД"""
        result = self.cursor.execute("SELECT * FROM 'sign_up' WHERE user_id = ? and training_id = ?", (user_id, training_id,))
        return result.fetchone()

    def check_mark_on_trainings(self, training_id):
        result = self.cursor.execute("SELECT user_id FROM 'sign_up' WHERE training_id = ?", (training_id,))
        return result.fetchall()

    def close(self):
        """Закрытие соединения c БД"""
        self.conn.close()