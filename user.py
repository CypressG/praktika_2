import database



class Student:
    def __init__(self, first_name, last_name, role, class_name,username,password):
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.class_name = class_name
        self.username = username
        self.password = password
    def edit_user(self,db):
        pass
    def show_marks(self,db):
        answer = db.show_marks(self.username)
        return answer


class Teacher(Student): 
    def __init__(self, first_name, last_name, role, class_name,username,password):
        super().__init__(first_name, last_name, role, class_name,username,password)
    def add_mark(self,mark,db):
        return db.add_mark(mark)
    def update_mark(self,mark,db):
        return db.update_mark(mark)
    def delete_mark(self):
        pass
    def get_lectures(self,db):
        return db.get_lectures()
    def get_teacher_lectures(self,db):
        return db.get_teacher_lectures(self.username)
    def get_group_name_from_lecture(self,group,db):
        return db.get_group_name_from_lecture(group)
    def get_users_by_group(self,group,db):
        return db.get_users_by_group(group)
    def get_marks_by_lecture(self,lecture,db):
        return db.get_marks_by_lecture(lecture)
class Admin(Teacher):
    def __init__(self, first_name, last_name, role, class_name,username,password):
        super().__init__(first_name, last_name, role, class_name,username,password)
    def add_lecture(self,lecture,db):
        return db.add_lectures(lecture)
    def delete_lecture(self,lecture,db):
        return db.delete_lecture(lecture)
    def add_group(self,group,db):
        return db.add_group(group)
    def delete_group(self,group,db):
        return db.delete_group(group)
    def register_user(self,user,db):
        return db.register_user(user)
    def delete_user(self,user,db):
        return db.delete_user(user)
    def get_users(self,db):
        return db.get_users()
    def get_roles(self,db):
        return db.get_roles()       
    def get_groups(self,db):
        return db.get_groups()
    def get_teachers(self,db):
        return db.get_teachers()
    def assign_lecture(self,lecture,db):
        return db.assign_lecture(lecture)
    def assign_group_lectures(self,group,db):
        return db.assign_group_lecture(group)