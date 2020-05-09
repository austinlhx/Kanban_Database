import mysql.connector
import json
from tkinter import *
from functools import partial
import tkinter as tk
from tkinter import ttk
import PIL
import sqlite3


with open('company.json') as f:
    company = json.load(f)

with open('tasks.json') as t:
    tasks = json.load(t)

with open('status.json')as s:
    status = json.load(s)

with open('users.json') as u:
    user = json.load(u)

entrance = False
#print(company)

class InvalidCompanyDataError(Exception):
    def __init__(self, d):
        self.d = d
    def __str__(self):
        return f"InvalidCompanyDataError: keys must be 'id' and 'name': {self.d}"

class InvalidTaskDataError(Exception):
    def __init__(self, d):
        self.d = d
    def __str__(self):
        return f"InvalidCompanyDataError: keys must be 'assigneeId' and 'clientCompanyId' and 'description' and 'dueDate' and 'task_id' and 'startDate' and 'statusId': {self.d}"

class InvalidUserDataError(Exception):
    def __init__(self, d):
        self.d = d
    def __str__(self):
        return f"InvalidCompanyDataError: keys must be 'id' and 'name': {self.d}"

class InvalidStatusDataError(Exception):
    def __init__(self, d):
        self.d = d
    def __str__(self):
        return f"InvalidCompanyDataError: keys must be 'id' and 'firstName' and 'lastName': {self.d}"

class Company():
    def __init__(self, data):
        self.__add_details(data)

    def __add_details(self, d):
        if (id_val := d.get("id")) and (name_val := d.get("name")):
            self._id = id_val
            self._name = name_val
        else:
            raise InvalidCompanyDataError(d)


class Task(Company): #assigneeId, clientCompanyId, description, dueDate, task_id, startDate, statusId
    def __init__(self, data):
        self.__add_task(data)

    
    def __add_task(self, d):
        assigneeId = d.get("assigneeId")
        clientCompanyId = d.get("clientCompanyId")
        description = d.get("description")
        dueDate = d.get("dueDate")
        task_id = d.get ("id")
        startDate = d.get("startDate")
        statusId = d.get("statusId")
        if (assigneeId and clientCompanyId and description and dueDate and task_id and startDate and statusId):
            self._assigneeId = assigneeId
            self._clientCompanyId = clientCompanyId
            self._description = description
            self._dueDate = dueDate
            self._task_id = task_id
            self._startDate = startDate
            self._statusId = statusId
        else:
            raise InvalidTaskDataError(d)

class Users(Company):
    def __init__(self, data):
        self.__add_status(data)
    
    def __add_status(self, d):
        if (id_val := d.get("id")) and (firstName_val := d.get("firstName") and (lastName_val := d.get("lastName"))):
            self._id = id_val
            self._firstName = firstName_val
            self._lastName = lastName_val
        else:
            raise InvalidUserDataError(d)

class Status(Task):
    def __init__(self, data):
        self.__add_status(data)
    
    def __add_status(self, d):
        if (id_val := d.get("id")) and (name_val := d.get("name")):
            self._id = id_val
            self._name = name_val
        else:
            raise InvalidStatusDataError(d)
        

def createCompany(data):
    try:
        companies = []
        for item in data:
            companies.append(Company(item))
        for i in range(4):
            print(companies[i]._id, companies[i]._name)
    except InvalidCompanyDataError as e:
        print(e)

def createTask(data):
    try:
        task = []
        for item in data:
            task.append(Task(item))
        for i in range(4):
            print(task[i]._task_id)
    except InvalidTaskDataError as e:
        print(e)

    

def createStatus(data):
    try:
        statuss = []
        for item in data:
            statuss.append(Status(item))
        for i in range(4):
            print(statuss[i]._id)
    except InvalidStatusDataError as e:
        print(e)


def Login(userList, taskList):
    global nameEL
    global pwordEL # More globals :D
    global rootA
    
 
    rootA = Tk()
    rootA.title('Login')
 
    instruction = Label(rootA, text='Please Login\n') 
    instruction.grid(sticky=E)
 
    nameL = Label(rootA, text='Username: ')

    nameL.grid(row=1, sticky=W)

 
    nameEL = Entry(rootA) 

    nameEL.grid(row=1, column=1)

 
    loginB = Button(rootA, text='Login', command=lambda : CheckLogin(user, tasks, company, status)) 
    loginB.grid(columnspan=2, sticky=W)
    

    rootA.mainloop()



def CheckLogin(data, items, comp, stat):
    global treeview

    for i in range(len(data)):
        if nameEL.get() == data[i]['id']: 
            userLog = data[i]['firstName']
            userId = data[i]['id']
            r = Tk()
            r.title(':D')
            r.geometry('150x50')
            rlbl = Label(r, text='\n[+] Logged In')
            rlbl.pack()
            r.mainloop()
            entrance = True
            break

    else:

        r = Tk()
        r.title('D:')
        r.geometry('150x50')
        rlbl = Label(r, text='\n[!] Invalid Login')
        rlbl.pack()
        r.mainloop()   

    if entrance == True:
        r = Tk()
        r.geometry('200x200')
        z = 0
        for names in data:
            var = StringVar()
            myString = 'v' + str(z)
            c = Checkbutton(r, text = names['firstName'], variable=var)
            c.select()
            c.pack()
            z = z + 1


        userText = "Hello, " + userLog
        root = Tk()
        root.geometry('1500x500')
        treeview = ttk.Treeview(root)
        treeview.pack()
        treeview["columns"] = ('one', 'two', 'three', 'four')
        treeview.column("#0", width=80, minwidth=50, stretch=tk.NO)
        treeview.column("one", width=80, minwidth=50, stretch=tk.NO)
        treeview.column("two", width=80, minwidth=50)
        treeview.column("three", width=80, minwidth=50, stretch=tk.NO)

        treeview.heading("#0",text=userText,anchor=tk.W)
        treeview.heading("one", text="Column Name",anchor=tk.W)
        treeview.heading("two", text="Column Type",anchor=tk.W)
        treeview.heading("three", text="Description",anchor=tk.W)
        
        treeview.pack(side=tk.TOP, fill=tk.X)

       # treeview.insert('','0','item1',text='hello')
        #treeview.insert('item1','end', '0',text ='A')
        #treeview.insert('item1','end', '1',text ='B')
        count = 0
        for i in range(len(items)):
            
            clientCompany = items[i]['clientCompanyId']
            description = items[i]['description']
            dueDate = items[i]['dueDate']
            meta = items[i]['id']
            startDate = items[i]['startDate']
            assigneeId = items[i]['assigneeId']
            statusId = items[i]['statusId']

            for x in range(len(comp)):
                if (clientCompany == comp[x]['id']):
                     companyName = comp[x]['name']

            for j in range(len(data)):
                if (assigneeId == data[j]['id']):
                    first = data[j]['firstName']
                    last = data[j]['lastName']
                    fullName = first + ' ' + last

            for y in range(len(stat)):
                if (statusId == stat[y]['id']):
                     statusName = stat[y]['name']

            hierarchy = 'item' + str(i)
            treeview.insert("", i, hierarchy, text = fullName)
            treeview.insert(hierarchy, 'end', count, values=('client_company_id', '0', companyName))
            treeview.insert(hierarchy, 'end', count+1, values=('description', '0', description))
            treeview.insert(hierarchy, 'end', count+2, values=('dueDate', '0', dueDate))
            treeview.insert(hierarchy, 'end', count+3, values=('meta', '0', meta))
            treeview.insert(hierarchy, 'end', count+4, values=('startDate', '0', startDate))
            treeview.insert(hierarchy, 'end', count+5, values=('statusId', '0', statusName))
            count = count + 6
        r.mainloop()
def main():
    createCompany(company)
    createTask(tasks)
    createStatus(status)
    try:
        users = []
        for item in user:
            users.append(Users(item))
        
    except InvalidUserDataError as e:
        print(e)

    Login(users, tasks)


main()
