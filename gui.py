import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk as ttk
import database
import user

name_of_db = "database"

db = database.Database(name_of_db)

choices = ['Student','Teacher',"Admin"]

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.canvas_left = tk.Canvas(master,width=50)
        self.canvas_right = tk.Canvas(master,width=100)
        self.canvas_left.pack(side="left")
        self.canvas_right.pack(side="right")
        #Left Side of Main
        self.start_screen()
        self.logo()
        #Right Side of Main
        #--------------------
          

    def logo(self):
        render = ImageTk.PhotoImage(Image.open("viko.png"))
        self.logo_picture = tk.Label(image=render)
        self.logo_picture.image = render
        self.logo_picture.pack(expand="yes",fill="both",side="bottom") 


    def start_screen(self):
        self.delete_all_children(self.canvas_left)
        self.delete_all_children(self.canvas_right)
        self.logged_in = None
        self.login_button = tk.Button(self.canvas_left, text="Login", command=self.login,width=15,height=2)
       # self.register_button = tk.Button( self.canvas_left, text="Register",command=self.register,width=15,height=2,state="normal")
        self.login_button.pack(side="top")
        #self.register_button.pack(side="left")


    def delete_all_children(self,parent):
        for child in parent.winfo_children():
            child.destroy()
        

    def pack_everything(self,parent):
        for c in parent.children:
            parent.children[c].pack()


    def delete_parent(self,parent):
        parent.destroy()


    def if_false(self):
        self.incorrect = tk.Toplevel(self)
        error = tk.Label(self.incorrect,text="You've put something wrong. Please fix it and try again")
        turn_off = tk.Button(self.incorrect,text="Leave",command = self.incorrect.destroy)
        error.pack()
        turn_off.pack()

    def if_true(self):
        self.correct = tk.Toplevel(self)
        information = tk.Label(self.correct,text="Everything worked well!!")
        turn_off = tk.Button(self.correct,text="Close",command=self.correct.destroy)
        information.pack()
        turn_off.pack()

        
    def login(self):
        self.delete_all_children(self.canvas_left)
        self.login_input = tk.Entry(self.canvas_left,width=30,justify="center")
        self.password = tk.Entry(self.canvas_left, width=30,justify="center",show="*")
        label_a = tk.Label(self.canvas_left,text="User: ")
        label_b =tk.Label(self.canvas_left,text="Password: ")
        label_a.pack()
        self.login_input.pack(side='top')
        label_b.pack()
        self.password.pack(side='top')
        frame = tk.Frame(self.canvas_left)
        login_button = tk.Button(frame,text="Login",command=self.check_login)
        go_back = tk.Button(frame,text="Go Back",command=self.start_screen)
        login_button.pack(side="left")
        go_back.pack(side="left")
        frame.pack()


    def check_login(self):
        username = self.login_input.get().lower()
        password = self.password.get().lower()
        answer = db.check_user_details(username,password) 
        if answer == False:
            return self.if_false()
        else:
            if answer[2] == "Student":
                self.logged_in = user.Student(answer[0],answer[1],answer[2],answer[3],answer[4],answer[5])
            elif answer[2] == "Teacher":
                self.logged_in = user.Teacher(answer[0],answer[1],answer[2],answer[3],answer[4],answer[5])
            elif answer[2] == "Admin":
                self.logged_in = user.Admin(answer[0],answer[1],answer[2],answer[3],answer[4],answer[5])
            self.main_screen()
    

    def register(self):
        self.get_all_roles()
        roles = []
        for role in self.roles:
            roles.append(role[0])
        self.get_all_groups()
        groups = []
        for group in self.groups:
            groups.append(group[0])
        self.delete_all_children(self.canvas_right)
        register_first_name_label = tk.Label(self.canvas_right,text="First Name",justify="center")
        self.register_first_name_input = tk.Entry(self.canvas_right,width=30,justify="center")
        register_last_name_label = tk.Label(self.canvas_right,text="Last Name",justify="center")
        self.register_last_name_input = tk.Entry(self.canvas_right,width=30,justify="center")
        group_label_a = tk.Label(self.canvas_right,text="Choose Role: ")
        self.role = ttk.Combobox(self.canvas_right,values=roles)
        group_label_b = tk.Label(self.canvas_right,text="Choose Group: ")

        self.group = ttk.Combobox(self.canvas_right,values=groups)
        self.pack_everything(self.canvas_right)
        frame = tk.Frame(self.canvas_right)
        register_button = tk.Button(frame,text="Register", command=self.try_register)
        go_back = tk.Button(frame,text="Go Back",command=self.start_screen)
        frame.pack()
        register_button.pack(side="left")
        go_back.pack(side="left")
        pass
    
    
    def get_all_groups(self):
        self.groups = self.logged_in.get_groups(db)

    def try_register(self):
        answer = (self.register_first_name_input.get(),self.register_last_name_input.get(),self.role.get(),self.register_first_name_input.get().lower(),self.register_last_name_input.get().lower(),self.group.get().lower())
        if answer[0] and answer[1] and answer[2]:
            self.if_true()
            return self.logged_in.register_user(answer,db)
        self.if_false()


    def main_screen(self):
        self.delete_all_children(self.canvas_left)
        if self.logged_in.role == "Student":
            self.show_marks = tk.Button(self.canvas_left,text="Check Marks", width=15, command=self.show_marks)
        

        elif self.logged_in.role == "Admin":
            self.add_lecture = tk.Button(self.canvas_left,text="Add Lecture", width=15, command=self.add_lecture)
            self.delete_lecture = tk.Button(self.canvas_left,text="Delete Lecture",width=15,command=self.delete_lecture)
            self.add_user = tk.Button(self.canvas_left,text="Add User", width=15,command=self.register)
            self.delete_user = tk.Button(self.canvas_left, text="Delete User",width=15, command=self.delete_user)
            self.assign_lecture = tk.Button(self.canvas_left,text="Assign Teacher", width=15,command=self.assign_lecture)
            self.add_group = tk.Button(self.canvas_left,text="Add Group", width=15,command=self.add_group)
            self.delete_group = tk.Button(self.canvas_left,text="Delete Group", width=15, command=self.delete_group)
            self.assign_lectures_group = tk.Button(self.canvas_left,text="Assign Group to Lecture", command=self.assign_group_lectures)
        elif self.logged_in.role == "Teacher":
            self.add_mark = tk.Button(self.canvas_left,text="Add Mark", width=15,command=self.add_mark)
            self.edit_mark = tk.Button(self.canvas_left,text="Edit Mark", width=15,command=self.edit_user_mark)

        logout = tk.Button(self.canvas_left, text="Log Out", command=self.start_screen)
        self.pack_everything(self.canvas_left)


    def add_lecture(self):
        self.delete_all_children(self.canvas_right)
        name_label = tk.Label(self.canvas_right,text="Name: ")
        self.name = tk.Entry(self.canvas_right)
        description_label = tk.Label(self.canvas_right,text="Type: ")
        self.description = tk.Entry(self.canvas_right)
        class_room_label = tk.Label(self.canvas_right, text="Class Room: ")
        self.class_room = tk.Entry(self.canvas_right)
        button = tk.Button(self.canvas_right, command=self.submit_lecture,text="Submit")
        self.pack_everything(self.canvas_right)


    def submit_lecture(self):
        lecture = (None,self.name.get(),self.description.get(),self.class_room.get())
        #self.get_all_roles()
        if lecture[1] and lecture[2] and lecture[3]:
            self.logged_in.add_lecture(lecture,db)
            self.if_true()
        else:
            self.if_false()


    def choose_lecture(self):
        pass


    def change_state(self, parent):
        for children in parent.children:
            try:
                if children['state'] == tk.DISABLED:
                    children['state'] = tk.NORMAL
            except TypeError:
                pass


    def show_marks(self):
        self.delete_all_children(self.canvas_right)
        #tree = ttk.Treeview(self.canvas_right)
        #tree.column("1",width=20,anchor='se')
        #tree.column("2",width=20,anchor='se')
        #tree.heading("1", text="Mark")
        #tree.heading("1", text="Lecture")
        tree = ttk.Treeview(self.canvas_right)
        tree["columns"] = ("1","2") 
        tree['show'] = 'headings'
        tree.column("1",width=100)
        tree.column("2",width=100)
        tree.heading("1",text="Lectures")
        tree.heading("2",text="Mark")
        answers = self.logged_in.show_marks(db)
        for answer in answers:
            tree.insert("",'end',values=(answer[5],answer[3]))
        tree.pack(side="top")
       # print(answers.values())
       # for answer in answers:
        #    print(answer)
       #     tree.insert("",'end',values=(answer[5],answer[3]))


    def get_all_roles(self):
        self.roles = self.logged_in.get_roles(db)
        for role in self.roles:
            print(role)


    def assign_lecture(self):
        self.teachers = None
        self.lectures = None
        self.get_lectures()
        self.get_teachers()
        self.delete_all_children(self.canvas_right)
        group_label_b = tk.Label(self.canvas_right,text="Choose Teacher: ")
        self.add_lecture_user = ttk.Combobox(self.canvas_right,values=self.teachers)
        group_label_a = tk.Label(self.canvas_right,text="Choose Topic: ")
        self.which_lecture = ttk.Combobox(self.canvas_right,values=self.lectures)
        self.assing_lecture_button = tk.Button(self.canvas_right,text="Submit", command=self.assign_to)
        self.pack_everything(self.canvas_right)


    def assign_to(self):
        answer = (self.which_lecture.get()[0], self.add_lecture_user.get())
        if self.logged_in.assign_lecture(answer,db):
            self.if_true()
        else:self.if_false()
        

    def get_lectures(self):
        tmp = self.logged_in.get_lectures(db)
        self.lectures = [ lecture for lecture in tmp]
        

    def get_teachers(self):
        tmp = self.logged_in.get_teachers(db)
        self.teachers = [teacher for teacher in tmp]
        

    def get_group(self):
        tmp = self.logged_in.get_groups(db)
        self.groups = [group for group in tmp]
    

    def get_users(self):
        tmp = self.logged_in.get_users(db)
        self.users = [user for user in tmp]


    def get_teacher_lectures(self):
        tmp = self.logged_in.get_teacher_lectures(db)
        self.teacher_lectures = [lecture for lecture in tmp]


    def add_group(self):
        self.delete_all_children(self.canvas_right)
        group_label = tk.Label(self.canvas_right,text="Group Name: ")
        self.add_group_name = tk.Entry(self.canvas_right)
        group_label_b = tk.Label(self.canvas_right,text="Group Description: ")
        self.add_group_description = tk.Entry(self.canvas_right)
        self.add_group_submit = tk.Button(self.canvas_right,text="Add Group", command=self.adding_group)
        self.pack_everything(self.canvas_right)
    

    def adding_group(self):
        answer = (self.add_group_name.get().lower(),self.add_group_description.get())
        if self.logged_in.add_group(answer,db):
            self.if_true()
        else:
            self.if_false()
        

    def delete_group(self):
        self.get_group()
        self.delete_all_children(self.canvas_right)
        group_label = tk.Label(self.canvas_right,text="Which group would you like to delete: ")
        self.delete_group = ttk.Combobox(self.canvas_right, values=self.groups)
        self.delete_group_submit = tk.Button(self.canvas_right,text="Delete Group", command=self.trying_delete)
        self.pack_everything(self.canvas_right)
    
    
    def trying_delete(self):
        answer = (self.delete_group.get())
        #self.logged_in.delete_group(answer,db)
        if self.logged_in.delete_group(answer,db):
            self.if_true()
        else:
            self.if_false()
    

    def delete_user(self):
        self.get_users()
        self.delete_all_children(self.canvas_right)
        group_label_b = tk.Label(self.canvas_right,text="Which User you would like to delete: ")
        self.delete_user_combo = ttk.Combobox(self.canvas_right,values=self.users)
        self.delete_user_submit = tk.Button(self.canvas_right, command=self.trying_delete_user,text="Delete user")
        self.pack_everything(self.canvas_right)


    def trying_delete_user(self):
        answer = self.delete_user_combo.get()
        if self.logged_in.delete_user(answer,db):
            self.if_true()
        else:
            self.if_false()
    

    def delete_lecture(self):
        self.get_lectures()
        self.delete_all_children(self.canvas_right)
        group_label_b = tk.Label(self.canvas_right,text="Choose which lecture you would like to delete: ")
        self.delete_lecture_combo = ttk.Combobox(self.canvas_right, values=self.lectures)
        self.delete_lecture_submit = tk.Button(self.canvas_right,text="Delete Lecture", command=self.trying_delete_lecture)
        self.pack_everything(self.canvas_right)


    def trying_delete_lecture(self):
        answer = self.delete_lecture_combo.get()
        if self.logged_in.delete_lecture(answer,db): self.if_true()
        else: self.if_false()


    def add_mark(self):
        self.get_teacher_lectures()
        self.delete_all_children(self.canvas_right)
        label = tk.Label(self.canvas_right,text="Choose to which subject you would like to mark")
        self.teacher_lectures_combo = ttk.Combobox(self.canvas_right,values=self.teacher_lectures)
        self.teacher_lectures_button = tk.Button(self.canvas_right,text="Next",command=self.add_mark_group)
        self.pack_everything(self.canvas_right)
        

    def add_mark_group(self):
        self.trying_to_mark()
        self.delete_all_children(self.canvas_right)
        label = tk.Label(self.canvas_right,text="Choose a group You would like to evaluate")
        self.add_mark_group_combo = ttk.Combobox(self.canvas_right, values=self.groups_from_lecture)
        self.add_mark_group_button = tk.Button(self.canvas_right,command=self.add_mark_to, text="Next")
        self.pack_everything(self.canvas_right)


    def add_mark_to(self):
        answer = self.find_users()
        print(answer)
        self.delete_all_children(self.canvas_right)
        label = tk.Label(self.canvas_right,text="Who should get the mark?")
        self.add_mark_user = ttk.Combobox(self.canvas_right, values=answer)
        label_a = tk.Label(self.canvas_right,text="What mark should they get?")
        self.mark = tk.Entry(self.canvas_right)
        self.mark_submit = tk.Button(self.canvas_right,text="Submit Mark",command=self.adding_mark)
        self.pack_everything(self.canvas_right)
    

    def adding_mark(self):
        user = self.add_mark_user.get()
        mark = self.mark.get()
        answer = (None,user,self.save_lecture[0],mark)
        if self.logged_in.add_mark(answer,db):
            self.if_true()
        

    def trying_to_mark(self):
        self.save_lecture = self.teacher_lectures_combo.get()
        self.groups_from_lecture = self.logged_in.get_group_name_from_lecture(self.save_lecture[0],db)
    

    def find_users(self):
        group = self.add_mark_group_combo.get()
        print(f"{group} <- CIA")
        answer = self.logged_in.get_users_by_group(group,db)
        return answer


    def get_groups_by_lecture(self):
        pass


    def assign_group_lectures(self):
        self.get_group()
        self.get_lectures()
        self.delete_all_children(self.canvas_right)
        label = tk.Label(self.canvas_right, text="Which lecture you would like to assign?")
        self.assign_lectures = ttk.Combobox(self.canvas_right,values=self.lectures)
        label_b = tk.Label(self.canvas_right, text="Which group would you like to assign to? ")
        self.assign_lectures_group = ttk.Combobox(self.canvas_right,values=self.groups)
        self.assign_lectures_button = tk.Button(self.canvas_right, text="Add lecture", command=self.trying_assign_group_lectures)
        self.pack_everything(self.canvas_right)
        

    def trying_assign_group_lectures(self):
        group = self.assign_lectures_group.get()
        lectures = self.assign_lectures.get()
        answer = (lectures[0],group)
        if self.logged_in.assign_group_lectures(answer,db):
            self.if_true()
        else:self.if_false()


    def edit_user_mark(self):
        self.delete_all_children(self.canvas_right)
        label = tk.Label(self.canvas_right,text="Which Lecture mark You would like to edit?")
        self.get_lectures()
        self.assign_lectures = ttk.Combobox(self.canvas_right,values=self.lectures)
        button = tk.Button(self.canvas_right,text="Choose Lecture", command=self.edit_user_mark_group)
        self.pack_everything(self.canvas_right)


    def edit_user_mark_group(self):
        self.get_user_delf()
        self.delete_all_children(self.canvas_right)
        self.tree = ttk.Treeview(self.canvas_right)
        self.tree["columns"] = ("1","2","3") 
        self.tree['show'] = 'headings'
        self.tree.column("1",width=100)
        self.tree.column("2",width=100)
        self.tree.column("3",width=100)
        self.tree.heading("3",text="ID")
        self.tree.heading("1",text="Student")
        self.tree.heading("2",text="Mark")
        
        answers = self.marks_list
        for answer in answers:
            self.tree.insert("",'end',values=(answer[0],answer[1],answer[2]))

        self.edit_mark_entry = tk.Entry(self.canvas_right)
        submit = tk.Button(self.canvas_right,text="Edit A Mark",command=self.trying_to_edit_mark)
        self.pack_everything(self.canvas_right)        

    def get_user_delf(self):
        answer = self.assign_lectures.get()[0]
        self.marks_list = self.logged_in.get_marks_by_lecture(answer,db)
        
    def trying_to_edit_mark(self):
        answer = self.tree.selection()
        values = self.tree.item(answer)['values']
        mark = (self.edit_mark_entry.get(), values[2])
    
        if self.logged_in.update_mark(mark,db):
            self.if_true()

#        self.logged_in.edit_mark(mark,db)