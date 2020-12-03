import sqlite3 
import os

class Database:
    def __init__(self, *args):
        if os.path.isfile(f'{args[0]}.db'):
            self.connect = sqlite3.connect(f'{args[0]}.db')
        else:
            open(f"{args[0]}.db",'w').close()
            self.connect = sqlite3.connect(f'{args[0]}.db')
            c = self.connect.cursor()

            c.execute(''' CREATE TABLE Groups(
            group_name TEXT PRIMARY KEY,
            description TEXT
            )''')

            c.execute('''CREATE TABLE Users(
            first_name TEXT,
            last_name TEXT,
            role TEXT,
            username TEXT PRIMARY KEY,
            password TEXT,
            FK_group TEXT,
            FOREIGN KEY (FK_group) REFERENCES Groups(group_name) ON DELETE CASCADE
            )''')

            c.execute(''' CREATE TABLE Lectures(
                lectureID INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                type TEXT,
                class TEXT
            )''')

            c.execute('''CREATE TABLE Lectured_By(
                FK_lectures INTEGER,
                FK_user TEXT,
                FOREIGN KEY(FK_user) REFERENCES Users(username) ON DELETE CASCADE,
                FOREIGN KEY(FK_lectures) REFERENCES Lectures(lectureID)
                ON DELETE CASCADE,
                PRIMARY KEY (FK_lectures,FK_user)
                )''')

            c.execute(''' CREATE TABLE Marks(
                markID INTEGER PRIMARY KEY AUTOINCREMENT,
                FK_user TEXT,
                FK_lectures INTEGER,
                mark INTEGER,
                FOREIGN KEY(FK_user) REFERENCES Users(username) ON DELETE CASCADE,
                FOREIGN KEY(FK_lectures) REFERENCES Lectures(lectureID) ON DELETE CASCADE
            )''')
            c.execute('''CREATE TABLE GroupLectures(
                    FK_lectures INTEGER,
                    FK_group TEXT,
                    FOREIGN KEY (FK_group) REFERENCES Groups(group_name) ON DELETE CASCADE,
                    FOREIGN KEY (FK_lectures) REFERENCES Lectures(lectureID) ON DELETE CASCADE
                    PRIMARY KEY (FK_lectures,FK_group)
                )''')
            self.connect.commit()

    def register_user(self,user):
        c = self.connect.cursor()
        try:
            c.execute(''' INSERT INTO Users VALUES (?,?,?,?,?,?)''',user)
            self.connect.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def login_user(self,user):
        if self.check_user_details(user[3],user[4]) == True:
            self.logged_in = user
            return True
        else:
            return False

    def check_user_details(self,username,password):
        c = self.connect.cursor()
        c.execute(''' SELECT * FROM Users WHERE username = ? AND password = ?''',(username,password))
        answer = c.fetchone()
        if answer == None:
            return False
        return answer
    

    def delete_user(self,user):
        c = self.connect.cursor()
        c.execute('''SELECT * FROM Users WHERE username=(?)''',(user,))
        if c.fetchone()== None:
            return False
        else:
            c.execute('''DELETE FROM Users WHERE username=(?)''',(user,))
            self.connect.commit()
            return True

    def edit_user(self,user):
        c = self.connect.cursor()
        c.execute(''' UPDATE Users 
        SET first_name = ?, last_name = ?, role = ?, password = ?
        WHERE username = ?
        ''',(user[0],user[1],user[2],user[4],user[3]))
        self.connect.commit()

    def show_marks(self,user):
        c = self.connect.cursor()
        c.execute('''
        SELECT * FROM Marks 
        INNER JOIN Lectures ON Lectures.lectureID = FK_lectures 
        WHERE FK_user = (?);
        ''',(user,))
        answer = c.fetchall()
        return answer

    def edit_mark(self,new_mark, markID):
        c = self.connect.cursor()
        c.execute(''' UPDATE Marks
        SET mark = ? WHERE markID = ?
        ''',(new_mark,markID))
        self.connect.commit()
        return True

    def add_mark(self,mark):
        c = self.connect.cursor()
        c.execute('''
        INSERT INTO Marks VALUES(?,?,?,?)
        ''',(mark))
        self.connect.commit()
        return True

    def delete_mark(self,markID):
        c = self.connect.cursor()
        c.execute('''SELECT * FROM Marks WHERE markID = ?''',(markID,))
        if c.fetchone() == None:
            return False
        c.execute('''
        DELETE FROM Marks WHERE markID = ?
        ''',(markID,))
        self.connect.commit()
        return True


    def add_lectures(self,lectures):
        c = self.connect.cursor()
        #print(lectures)

        c.execute(''' 
        INSERT INTO Lectures VALUES(?,?,?,?)
        ''',lectures)
        self.connect.commit()

    def edit_lectures(self,lecture,lectureID):
        c = self.connect.cursor()
        c.execute('''
        UPDATE Lectures SET name = ?, type = ?, class = ? WHERE lectureID = ?
        ''',(lecture[1],lecture[2],lecture[3],lectureID))
        self.connect.commit()
        pass

    def delete_lecture(self,lecture):
        c = self.connect.cursor()
        c.execute(''' SELECT * FROM Lectures WHERE lectureID = ?
        ''',(lecture[0],))
        if c.fetchone() == None:
            return False
        c.execute(''' DELETE FROM Lectures WHERE lectureID=? ''',(lecture[0],))
        self.connect.commit()
        return True

    def assign_lecture(self, lecture):
        c = self.connect.cursor()
        try:
            c.execute('''INSERT INTO Lectured_By VALUES (?,?)''',(lecture))
            self.connect.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        

    def edit_group(self,username,group):
        c = self.connect.cursor()
        c.execute('''SELECT * FROM Users WHERE username = ?''',(username,))
        if c.fetchone() == None:
            return False
        c.execute('''UPDATE Users SET class = ?  WHERE username = ?''',(group,username,))
        self.connect.commit()
        return True

    def get_roles(self):
        c = self.connect.cursor()
        c.execute('''
        SELECT DISTINCT role FROM Users
        ''')
        answer = c.fetchall()
        if len(answer) > 0:
            return answer
        return False
    
    def add_group(self,group):
        c = self.connect.cursor()
        c.execute('''SELECT * FROM Groups WHERE group_name=?''',(group[0],))
        tmp = c.fetchall()
        if len(tmp)==0:
            c.execute('''
            INSERT INTO Groups VALUES(?,?)
            ''',group)
            self.connect.commit()
            return True
        else:
            return False

    def get_groups(self):
        c = self.connect.cursor()
        c.execute('''
        SELECT DISTINCT group_name FROM Groups
        ''')
        answer = c.fetchall()
        if len(answer)>0:
            return answer
        return False

    def get_lectures(self):
        c = self.connect.cursor()
        c.execute('''
        SELECT lectureID, name FROM Lectures
        ''')
        answer = c.fetchall()
        
        if len(answer) > 0:
            return answer
        return False
    
    def get_users(self):
        c = self.connect.cursor()
        c.execute(''' 
        SELECT username FROM Users
        ''')
        answer = c.fetchall()
        if len(answer) > 0:
            return answer
        return False


    def get_teachers(self):
        c = self.connect.cursor()
        c.execute('''
        SELECT username FROM Users WHERE role="Teacher" OR role="Admin"
        ''')
        answer = c.fetchall()
        if len(answer) > 0:
            return answer
        return False
    def delete_group(self,group):
        c = self.connect.cursor()
        c.execute('''SELECT * FROM Groups WHERE group_name =?''',(group,))
        answer = c.fetchall()
        if len(answer) > 0:
            c.execute('''
            DELETE FROM Groups WHERE group_name =?
            ''',(group,))
            return True
        else:
            return False
    
    def get_teacher_lectures(self,teacher):
        c = self.connect.cursor()
        print(teacher)
        c.execute('''
        SELECT lectureID, name FROM Lectures WHERE lectureID IN (SELECT FK_lectures FROM Lectured_By WHERE FK_user = ?)
        ''',(teacher,))
        answer = c.fetchall()
        print(answer)
        return answer
    
    def assign_group_lecture(self,group):
        c = self.connect.cursor()
        try:
            c.execute('''
            INSERT INTO GroupLectures VALUES(?,?)
            ''',(group))
            self.connect.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_group_name_from_lecture(self,group):
        c = self.connect.cursor()
        print(group)
        c.execute('''
        SELECT FK_group FROM GroupLectures WHERE FK_lectures = ?
        ''',(group,))
        answer = c.fetchall()
        return answer
    def get_users_by_group(self,group):
        c = self.connect.cursor()
        c.execute('''
        SELECT username FROM Users WHERE FK_group = ?
        ''',(group,)) 
    
        answer = c.fetchall()
        return answer
    
    def get_marks_by_lecture(self,lecture):
        c = self.connect.cursor()
        c.execute(
            '''
            SELECT FK_user, mark,markID FROM Marks WHERE FK_lectures = ?
            ''',(lecture,))
        answer = c.fetchall()
        return answer

    def update_mark(self,mark):
        c = self.connect.cursor()
        c.execute('''UPDATE Marks SET mark = ? WHERE markID = ?
        ''',(mark[0],mark[1]))
        self.connect.commit()