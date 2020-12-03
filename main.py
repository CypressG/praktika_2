import sqlite3 
import tkinter as tk
import gui as g
import screeninfo
import database

roles = ["Student","Teacher","Admin"]

user = [
    ("Testas","Testuotojas",roles[0],"t.estuotojas","password","PI19A"),("Testutis","Testutijautojas",roles[2],"testutis1","password","PI14A")
]
false_user = [
    ("Vardenis","Pavardenis","User","DOES NOT EXIST","NONE")
]

lectures = [
    (None,"Istorija","Klaseje","318A"),
    (None,"Lietuviu","Klaseje","201B"),
]

lectures_id = [
    (1),(2)
]

marks = [
    (None,"Testutis1",1,10)
]

new = database.Database("database")


#new.edit_group("Testutis1x","PI19A")

#new.add_mark(marks[0])

#new.edit_mark(3,1)

#new.delete_mark(1)

#new.assign_lectures("Testutis1",2)

#new.add_lectures(lectures[0])

#new.delete_lectures(lectures_id[0])

#new.edit_lectures(lectures[1],1)

#new.register_user(user[0])

#print(new.delete_user(false_user[0]))

#print(new.delete_user(user[0]))


def main():
    root = tk.Tk()
    root.geometry("600x600")
    app = g.Application(master=root)
    app.mainloop()

main()

