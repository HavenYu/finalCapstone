# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass
  
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Create a function to read the user file
def open_user():

    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

    # Convert to a dictionary
    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password

    return username_password

# Call the function and read in user data
username_password = open_user()

# Create a function to read the task file
def open_task():

    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []
    for t_str in task_data:
        curr_t = {}

        # Split by semicolon and manually add each component
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False

        task_list.append(curr_t)

    return task_list

# Call the function to read in task data
task_list = open_task()

# Create a function to write the task file
def write_task(task_list):
    with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))

# Create a function to let the user to register new user
def reg_user():

    # Read the user data
    username_password = open_user()

    while True:
        # - Request input of a new username
        new_username = input("New Username: ")

        if new_username in username_password.keys():
            print("Username has already registered. Please enter another username.")
            continue
        else:
            pass

        # - Request input of a new password
        new_password = input("New Password: ")

        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # - If they are the same, add them to the user.txt file,
            print("New user added")
        

            username_password[new_username] = new_password
            
            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))
                break

        # - Otherwise you present a relevant message.
        else:
            print("Passwords do no match")
            continue

# Create a function to let the user to add new task
def add_task():

    # Read the user data
    username_password = open_user()

    while True:

        # Request input from user
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")


        # Then get the current date.
        curr_date = date.today()
        ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

        task_list.append(new_task)
        write_task(task_list)
        print("Task successfully added.")
        break

# Create a function to let the user to view all tasks
def view_all():

    # Read the task data
    task_list_va = open_task()

    # Display all tasks
    for t in task_list_va:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)

# Create a function to let the user to view his/her task and edit or mark as completed
def view_mine():

    # Read the tasks and user data    
    task_list = open_task()
    user_list = [i['username'] for i in task_list]

    # Check if the current user has any tasks
    if curr_user not in user_list:
        print("You have no tasks currently.")
        return
    
    else:
        for t in task_list:

            # Read the tasks of the current user
            if t['username'] == curr_user:
                task_id = task_list.index(t)
                disp_str = f"\nTask ID: \t {task_id}\n"
                disp_str += f"Task: \t\t {t['title']}\n"
                disp_str += f"Assigned to: \t {t['username']}\n"
                disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Task Description: \n {t['description']}\n"
                print(disp_str)
        
    while True:

        try:
            
            # Ask the user to select the action needed
            vm_select = int(input("Please enter the Task ID to select a task, or enter -1 to return to main menu: "))

            # Return to menu
            if vm_select == -1:
                break
            
            # Check if the selected task is completed or not
            elif task_list[vm_select]['completed'] == True:
                print("The selected task is already completed and cannot be edited. Please try again.")
                continue

            elif vm_select == task_id:
                vm_select_2 = input("Select one of the following options below:\n1 - Mark the task as complete\n2 - Edit the task\n: ")
                
                # Mark task as completed
                if vm_select_2 == "1":
                    task_list[task_id]['completed'] = True
                    write_task(task_list)
                    print("Task marked completed")
                    break               

                # Edit task
                elif vm_select_2 == "2":
                    vm_select_3 = input("Select one of the following options below:\n1 - Edit the person assigned\n2 - Edit the due date\n: ")
 
                    # Edit person in charge
                    if vm_select_3 == "1":
                        edit_user = input("Please enter the username of the new person in charged: ")
                        if edit_user not in username_password.keys():
                            print("This username is not exist. Please try again.")
                            continue
                        else:
                            task_list[task_id]['username'] = edit_user
                            write_task(task_list)
                            print("Person in charged edited")
                            break               

                    # Edit due date
                    elif vm_select_3 == "2":
                        try:
                            edit_date = input("Please enter the new due date (YYYY-MM-DD): ")
                            edit_date_2 = datetime.strptime(edit_date, DATETIME_STRING_FORMAT)
                            task_list[task_id]['due_date'] = edit_date_2
                            write_task(task_list)
                            print("Due date edited")
                            break

                        # Check the date format
                        except ValueError:
                            print("Invalid datetime format. Please use the format specified")

                    else:
                        print("The input is invalid, please try again.")
                        continue

                else:
                    print("The input is invalid, please try again.")
                    continue

            else:
                print("The input is invalid, please try again.")
                continue

        except ValueError:
            print("The input is invalid, please try again.")
            continue

# Create a function to let the user to generate reports
def generate_reports():

    # Read tasks and user data
    tasks_list_gr = open_task()
    username_password = open_user()

    # Create a list of user with tasks
    user_list_gr = [i['username'] for i in tasks_list_gr]
    task_users_list_gr = []
    for i in user_list_gr:
        if i not in task_users_list_gr:
              task_users_list_gr.append(i)

    # Work out the data needed for task overview
    num_task = len(tasks_list_gr)
    num_task_c = len([i for i in tasks_list_gr if i['completed'] is True])
    num_task_ic = len([i for i in tasks_list_gr if i['completed'] is False])
    num_task_od = len([i for i in tasks_list_gr if i['due_date'] < datetime.today() and i['completed'] is False])
    per_task_ic = round((num_task_ic / num_task) * 100)
    per_task_od = round((num_task_od / num_task) * 100)

    # Generate the task overview
    task_ov = f"""------------------------------------------------
Task Overview:
Total number of tasks:             {num_task}
Total number of completed task:    {num_task_c}
Total number of incompleted task:  {num_task_ic}
Total number of overdue task:      {num_task_od}
Percentage of incompleted task:    {per_task_ic}%
Percentage of overdue task:        {per_task_od}%
------------------------------------------------
"""
    
    # Work out the needed data and generate the user overview
    num_user = len(username_password)
    num_task1 = 0
    num_task_c1 = 0
    num_task_ic1 = 0
    num_task_od1 = 0

    user_ov = f"""------------------------------------------------
User Overview:
Total number of users registered:  {num_user}
Total number of tasks:             {num_task}
------------------------------------------------
"""

    for i in task_users_list_gr:
        num_task1 = len([j for j in tasks_list_gr if j['username'] in i])
        num_task_c1 = len([j for j in tasks_list_gr if j['username'] in i and j['completed'] is True])
        num_task_ic1 = len([j for j in tasks_list_gr if j['username'] in i and j['completed'] is False])
        num_task_od1 = len([j for j in tasks_list_gr if j['username'] in i and j['completed'] is False and j['due_date'] < datetime.today()])
        user_ov += f"""Username:                           {i}
Total number of tasks assigned:     {num_task1}
Percentage of task in total tasks:  {round((num_task1 / num_task) * 100)}%
Percentage of completed tasks:      {round((num_task_c1 / num_task1) * 100)}%
Percentage of incompleted tasks:    {round((num_task_ic1 / num_task1) * 100)}%
Percentage of overdue tasks:        {round((num_task_od1 / num_task1) * 100)}%
------------------------------------------------
"""

    # Check are there any users without tasks
    for i in username_password.keys():
        if i not in user_ov:
            user_ov += f"""Username:                           {i}
Total number of tasks assigned:     {0}
Percentage of task in total tasks:  {0}%
Percentage of completed tasks:      {0}%
Percentage of incompleted tasks:    {0}%
Percentage of overdue tasks:        {0}%
------------------------------------------------
"""

    # Write the reports in text files
    with open("task_overview.txt", "w") as w_t_ov:
        w_t_ov.write(task_ov)

    with open("user_overview.txt", "w") as w_u_ov:
        w_u_ov.write(user_ov)

    print("Reports generated")

# Create a function to let the admin user to display statistics about number of users and tasks
def display_statistics():

    generate_reports()

    # Read the data from the text files
    with open("task_overview.txt", "r") as t_ov:
        tasks = t_ov.read()

    with open("user_overview.txt", "r") as u_ov:
        users = u_ov.read()

    # Display the report
    print(tasks)
    print(users)

#====Login Section====
'''This code allow a user to login.
'''

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    
    # Show menu for admin user
    if curr_user == 'admin': 
        menu = input('''\nSelect one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    gr - generate reports (Only available for admin)
    ds - display statistics (Only available for admin)
    e - Exit
    : ''').lower()

    # Show menu for non admin user
    else:
        menu = input('''\nSelect one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    e - Exit
    : ''').lower()

    if menu == 'r':
        reg_user()
        continue

    elif menu == 'a':
        add_task()
        continue

    elif menu == 'va':
        view_all()
        continue
            
    elif menu == 'vm':
        view_mine()
        continue

    elif menu == 'gr' and curr_user == 'admin':
        generate_reports()
        continue
 
    elif menu == 'ds' and curr_user == 'admin':
        display_statistics()
        continue

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
        continue