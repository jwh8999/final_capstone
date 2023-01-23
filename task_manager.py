# Username = 'admin'
# Password = 'adm1n'

# =====importing libraries===========

# hashlib is needed for encrypting passwords
import hashlib
# datetime is needed to get the current date
from datetime import datetime
# ast is needed to convert the strings into lists
import ast
# fileinput is needed to edit specific lines in files
import fileinput

# ====Defining functions====

def login(f, current_user, current_password):
    '''
    Checks that a given username and password match in the 'user.csv' file.

    :param f: The file that contains the list of usernames and passwords.
    :param current_user: The user's entry for username.
    :param current_password: The user's entry for password.
    :return: True if the username and password match in the file, False if not.
    '''
    # Firstly the user's entered password is hashed so that the hash can be compared to the hash in the file
    current_password_hash = hashlib.sha256(current_password.encode()).hexdigest()
    # A for loop will loop through each line in the file
    for line in f:
        # If the line matches a user's username and the hash of the password then the function returns True. i.e. the login is successful
        # .strip() is needed because new line characters can mean the string won't match
        if line.strip('\n') == f"{current_user}, {current_password_hash}":
            return True
    return False

def user_exists(username):
    '''
    Checks that a user exists in the 'user.csv' file.
    :param username: The username that will be checked against the file.
    :return: True if the username exists in the file, false if not.
    '''
    # File is opened in read only mode
    with open('user.csv', 'r', encoding='utf-8') as f:
        # Each line in the file is looped through
        for line in f:
            # Each line is split into a list to make it easier to read.
            line_list = line.split(",")
            # Since the first item in the list will be the username this if clause checks if the current line contains the name that the user entered
            if line_list[0] == username:
                # If the user exists it returns True
                return True
        # If it is not present then it returns False
        return False

def registration():
    '''
    Registers a new user in the 'user.csv' file.
    Takes inputs for the new username and password and storing it in the file.
    '''
    print("\nRegistration of a new user: ")
    # Infinite loop will continually prompt the user if their input is invalid.
    while True:
        # Prompt for new user's username
        new_username = input("New username: ")
        # The user_exists() function checks that the user does not already exist.
        if user_exists(new_username):
            # If it does they are informed.
            print("\033[91mThis username already exists. Please try again.\033[00m")
        # Otherwise the loop is broken
        else:
            break
    # An infinite loop so that the user is continually prompted if the passwords don't match
    while True:
        new_pass = input("\nPassword: ")
        new_pass_confirm = input("\nPlease confirm the password: ")
        # Checks that both entries of the password match
        if new_pass == new_pass_confirm:
            # The file is opened in append mode.
            with open('user.csv', 'a', encoding='utf-8') as f:
                # The new user's username and the hash of the chosen password is written to the file.
                f.write(f"{new_username}, {hashlib.sha256(new_pass.encode()).hexdigest()}\n")
            # If successful a message is printed and the loop is broken
            print(f"User '{new_username}' added successfully.")
            break
        # If the passwords don't match the user is informed
        else:
            print("\033[91mPasswords do not match! Please try again.\033[00m")

def statistics():
    '''
    Prints the contents of both 'task_overview.txt' and 'user_overview.txt'.
    If they don't exist the user is informed.
    '''
    # A try, except block is used to handle to case where the file is not found.
    while True:
        try:
            # The file is read from and the contents are stored in the variable 'contents' which is printed.
            with open('task_overview.txt', 'r', encoding='utf-8') as f:
                contents = f.read()
            print(contents)
        # If the file is not found reports are generated and the loop restarts.
        except FileNotFoundError:
            if_success = generate_reports()
            # If reports could not be generated the loop breaks.
            if if_success == False:
                break
            continue
        input("Press enter to continue...\n")
        # The same process is used to read the other file.
        try:
            with open('user_overview.txt', 'r', encoding='utf-8') as f:
                contents = f.read()
            print(contents)
            break
        except FileNotFoundError:
            if_success = generate_reports()
            if if_success == False:
                break
            continue
            
def new_task():
    '''
    Takes inputs nesessary for creating a new task and stores as a new line 'tasks.csv' file
    '''
    # Inputs are collected for each piece of information needed to create the task.
    # While True so that the user is continually prompted if their input is invalid.
    while True:
        task_assigned_person = input("Please enter the username of the person the task should be assigned to: ")
        # Checks the user exists so a task can be assigned to them.
        if user_exists(task_assigned_person):
            break
        else:
            # Otherwise they are told to try again.
            print("\033[91mThis user doesn't exist. Please try again.\033[00m")
    task_name = input("Please enter a short title for the task: ")
    task_description = input("Please enter a more detailed description of the task: ")
    # Continually prompt the user if the entry is invalid.
    while True:
        task_due_date = input("Please enter the due date of the task: (dd/mm/yyyy) ")
        # Tries formatting the date according to dd/mm/yyyy
        try:
            datetime.strptime(task_due_date, "%d/%m/%Y")
            # If sucessful the while loop is broken
            break
        # If the date could not be formatted they are told to try again.
        except ValueError:
            print("\033[91mPlease ensure the date was formatted as: dd/mm/yyyy\033[00m")
    # The current date is retrieved.
    today = datetime.now()
    # It is formatted according to dd/mm/yyyy and stored as 'today'.
    today = today.strftime('%d/%m/%Y')
    # The information is stored as a list in the required format.
    new_line_list = [task_assigned_person, task_name, task_description, task_due_date, today, "Incomplete"]
    # The file is opened and the task is written to a new line in the file as a string
    with open('tasks.csv', 'a', encoding='utf-8') as f:
        f.write(str(new_line_list) + "\n")
        print("\nTask added successfully!")

def view_all_tasks():
    '''
    Prints all the tasks in the 'tasks.csv' file.
    '''
    # A try except block is used to process the error that occurs if the file does not exist.
    try:
        # Count is needed to keep track of which line the for loop is on in the file and thus the task number.
        count = 0
        # The tasks file is opened
        with open('tasks.csv', 'r', encoding='utf-8') as f:
            # A for loop goes through each line in the file
            for line in f:
                # Whitespace is removed from the beginning and end of the line which would make the line harder to read.
                line = line.strip()
                # If the line is not empty
                if line:
                    # To calculate the current task number
                    count += 1
                    # ast is used to convert the current line (which is stored as a string) into a list
                    line_list = ast.literal_eval(line)
                # If the line is empty the for loop will continue to the next line.
                else:
                    continue
                # The elements in the list are printed in an easy-to-read format
                print(f'''———————————————————————————————————
    / Task {count}:    {line_list[1]}
    / Assigned to:     {line_list[0]}
    / Date assigned:   {line_list[4]}
    / Due date:        {line_list[3]}
    / Task status:     {line_list[5]}
    ''')
        # If the file was empty and count was not incremented.
        if count == 0:
            print("No tasks found!")
        # This final bar is printed after the tasks are printed to make it look nicer when printed.
        else:
            print("———————————————————————————————————")
    # If the file does not exist the user is informed.
    except FileNotFoundError:
        print("\033[91mTask file not found!\033[00m Please check the tasks.csv file is in the correct location or add a task from the "
              "menu")

def view_current_users_tasks(current_user):
    '''
    Prints the tasks, associated with the current user that is logged in, from the 'tasks.csv' file.
    :param current_user: The username of the current user
    :return: Returns task_dict which is a dictionary containing all the tasks owned by the current user. Or False if there are no tasks.
    '''
    # Count is needed to keep track of the number of each task.
    count = 0
    # This dictionary will be used to store the task number as a key which has a value of the full information about the task
    task_dict = {}
    # The file is opened in read only mode.
    try:
        with open('tasks.csv', 'r', encoding='utf-8') as f:
            # Each line in the file is looped through.
            for line in f:
                # Whitespace is removed to make the line easier to process.
                line = line.strip()
                # If the line is not empty.
                if line:
                    # Count is incremented to keep track of the current task
                    count += 1
                    # The line is converted to a list using ast.
                    line_list = ast.literal_eval(line)
                # If the line is blank the loop goes on to the next line.
                else:
                    continue
                # The task is only printed if the current username matches the username in the task
                if line_list[0] == current_user:
                    # The current line (converted to a list) is added to a dictionary with the key of the current task number
                    task_dict[str(count)] = line_list
                    # Each task belonging to the user is printed.
                    print(f'''———————————————————————————————————
    / Task {count}:    {line_list[1]}
    / Assigned to:     {line_list[0]}*
    / Date assigned:   {line_list[4]}
    / Due date:        {line_list[3]}*
    / Task status:     {line_list[5]}*
    ''')
        # This makes the display of the tasks look nicer at the end.
        print("———————————————————————————————————")
    except FileNotFoundError:
        print("\033[91mTask file not found!\033[00m Please check the tasks.csv file is in the correct location or add a task from the "
              "menu")
        return False
    # If the user has no tasks associated with them.
    if len(task_dict) == 0:
        input("You have no tasks to view. Press enter to return to main menu...")
        # False is returned to make it easier to return to main menu.
        return False
    # task_dict is returned because it is needed for editing tasks in the edit_task() function.
    return task_dict

def edit_task(tasks_dict, which_task):
    '''
    Edits elements in a task. Including: to whom the task is assigned, the due date, and to mark the task complete.
    :param tasks_dict: The tasks_dict dictionary, generated by the view_current_users_tasks() function,
    is needed so the user's current tasks can be read.
    :param which_task: The which_task paramater contains the task number that the user wishes to edit.
    '''
    # Infinite loop to continually prompt the user after they've made their edit
    while True:
        # They are shown a menu containing information about their selected task and a menu containing the changes they can make
        vm_menu_selection = input(f'''
/ Task {which_task}:    {tasks_dict[which_task][1]}
/ Assigned to:     {tasks_dict[which_task][0]}*
/ Date assigned:   {tasks_dict[which_task][4]}
/ Due date:        {tasks_dict[which_task][3]}*
/ Task status:     {tasks_dict[which_task][5]}*

Please select from the following menu: (only items marked '*' may be edited)
/ m - Mark task complete
/ e - Edit the task owner
/ t - Edit the due date of the task
/ x - Return to main menu
        
> ''')
        # If they select 'x' return ends the running of the function.
        if vm_menu_selection == 'x':
            return
        # For marking the task complete.
        elif vm_menu_selection == 'm':
            # The entry in the task is updated to 'Complete'
            tasks_dict[which_task][5] = 'Complete'
            # The line in the tasks file is edited using the edit_line() function.
            edit_line('tasks.csv', which_task, tasks_dict[which_task])
            print("\nTask successfully marked as complete.\n")
        # For editing the task owner.
        elif vm_menu_selection == 'e':
            # Infinite loop to continually prompt the user if the user they selected does not exist.
            while True:
                new_owner = input("Enter the name of the new owner of this task: ")
                # user_exists() function checks their input is valid.
                if user_exists(new_owner):
                    # The task owner is updated according to the user's selection.
                    tasks_dict[which_task][0] = new_owner
                    # This is then written to the tasks file using the edit_line() function
                    edit_line("tasks.csv", which_task, tasks_dict[which_task])
                    print("Task owner updated sucessfully")
                    break
                else:
                    print("\033[91mUser doesn't exist. Please try again.\033[00m")
        # For editing the due date.
        elif vm_menu_selection == 't':
            # Infinite loop continually prompts the user if their entry was invalid.
            while True:
                new_due_date = input("\nPlease enter the new due date of the task: (dd/mm/yyyy) ")
                # try, except block handles the error that occurs if the user did not format the date correctly
                try:
                    # datetime.strptime() returns a ValueError if the date is not formatted correctly.
                    datetime.strptime(new_due_date, "%d/%m/%Y")
                    # The loop only breaks if an error does not occur.
                    break
                except ValueError:
                    print("\033[91mPlease ensure the date was formatted as: dd/mm/yyyy\033[00m")
            # The due date is updated in the dictionary.
            tasks_dict[which_task][3] = new_due_date
            # This is then written to the file using the edit_line() function
            edit_line('tasks.csv', which_task, tasks_dict[which_task])
            input("\nDate successfully updated! Press enter to continue...\n")
        # If the user makes an invalid selection they are informed and the loop repeats.
        else:
            print("\033[91mYou have made a wrong choice! Please try again.\033[00m")

def generate_reports():
    '''
    Generates the files 'user_overview.txt' and 'tasks_overview.txt' from the 'user.csv' and 'tasks.csv' files.
    These contain statistics about the tasks and users.
    '''
    # Variables are initialised for counting the numbers of tasks.
    total_tasks_num = 0
    total_tasks_complete_num = 0
    total_tasks_overdue = 0
    # Dictionaries are initialised
    # These will contain the username as a key. The value will be the number of tasks associated with their username.
    user_task_total = {}
    user_complete_total = {}
    user_overdue_total = {}
    
    # A try except block is used to process the error that occurs if the tasks file is not found.
    try:
        # The tasks file is opened in read only mode.
        with open("tasks.csv", 'r') as f:
            # Each line in the file is looped through.
            for line in f:
                # Whitespace is removed to make the line easier to read.
                line = line.strip()
                # If the line is not empty.
                if line:
                    # The number of total tasks is incremented.
                    total_tasks_num += 1
                    # The line is converted to a list using ast.
                    line_list = ast.literal_eval(line)
                    # If the task is marked 'Complete'
                    if line_list[5] == "Complete":
                        # The number of complete tasks is incremented.
                        total_tasks_complete_num += 1
                    # The date in the current task is formatted to make a comparison with today's date easier.
                    new_due_date = datetime.strptime(line_list[3], "%d/%m/%Y")
                    # today is equal to today's date.
                    today = datetime.now()
                    # .setdefault() is used to add the current username as a key in the dictionary of overdue tasks
                    # This prevents error occuring when writing to the files if the user does not have any overdue tasks
                    # i.e if the key was not present in the dictionary.
                    user_overdue_total.setdefault(line_list[0], 0)
                    # If the due date has elapsed and the task is incomplete.
                    if today > new_due_date and line_list[5] == "Incomplete":
                        # The number of overdue tasks is incremented.
                        total_tasks_overdue += 1
                        # The value is retrieved from the dictionary (with the key of the current username).
                        value = user_overdue_total.get(line_list[0], 0)
                        # The value is incremented by one. This means 1 is added to the number of tasks they have overdue.
                        value += 1
                        # The value is updated in the dictionary.
                        user_overdue_total[line_list[0]] = value
                    # The value is similarly incremented for the user task total dictionary.
                    value = user_task_total.get(line_list[0], 0)
                    value += 1
                    user_task_total[line_list[0]] = value
                    # The total tasks a user have is similarly updated with the current username to prevent errors when writing to the file.
                    user_complete_total.setdefault(line_list[0], 0)
                    # If the task is marked complete.
                    if line_list[5] == 'Complete':
                        # The value for the username is incremented in the dictionary by one.
                        value = user_complete_total.get(line_list[0], 0)
                        value += 1
                        user_complete_total[line_list[0]] = value
                        
        # The information that has been calculated is written to the task_overview.txt file as required.
        with open(f'task_overview.txt', 'w', encoding='utf-8') as f:
            f.write(f'''Task overview report as of {today.strftime("%d/%m/%Y")}:
Total tasks: {total_tasks_num}
Total tasks complete: {total_tasks_complete_num} ({round(total_tasks_complete_num / total_tasks_num * 100)}%)
Total tasks incomplete: {total_tasks_num - total_tasks_complete_num} ({round((total_tasks_num - total_tasks_complete_num) / total_tasks_num * 100)}%)
Total tasks overdue {total_tasks_overdue} ({round(total_tasks_overdue / total_tasks_num * 100)}%)
''')
        # Variables are initialised for storing information about the number of tasks assigned to users.
        user_total_num = 0
        user_total_tasks_assigned = 0
        # The user.csv file is opend and the number of users is counted
        with open("user.csv", 'r', encoding='utf-8') as f:
            for line in f:
                # The line only counts if it is not empty. i.e there is a user associated with that line.
                if line.strip():
                    user_total_num += 1

        # The user_overview.txt file is written containing the required information.
        with open(f'user_overview.txt', 'w', encoding='utf-8') as f:
            f.write(f'''User overview report as of {today.strftime("%d/%m/%Y")}
Total users: {user_total_num}
Total tasks: {total_tasks_num}\n''')
        with open(f'user_overview.txt', 'a', encoding='utf-8') as f:
            for key, value in user_task_total.items():
                f.write(f'''
'{key}' has {value} tasks assigned ({round(value / total_tasks_num * 100)}% of total tasks)
> {key} has completed {round(user_complete_total[key] / user_task_total[key] * 100)}% of their assigned tasks
> {key} has yet to complete {round((user_task_total[key] - user_complete_total[key]) / user_task_total[key] * 100)}% of their assigned tasks
> {key} has {round(user_overdue_total[key] / user_task_total[key] * 100)}% of their tasks overdue.
''')
        return True
    
    # An error is printed if the tasks file does not exist.
    except FileNotFoundError:
        input('''
Reports could not be generated as the 'tasks.csv' file could not be found.
        
Try to:
Add a task from the main menu
Ensure the 'tasks.csv' file is in the correct location
     
Press enter to return to the main menu...''')
        # return ends the function.
        return False

def edit_line(file, line_change_num, new_line):
    '''
    Edits a line in a specified file.
    :param file: The file containing the line to be edited.
    :param line_change_num: The line on the file which needs to be changed.
    :param new_line: The new line to write to the file.
    '''
    # Loops through each line in the file
    # inplace=True means the new content will be rewritten to the same file.
    for line in fileinput.input(file, inplace=True):
        # If the current line in the loop equals the line that needs to be edited.
        if fileinput.lineno() == int(line_change_num):
            # The current line is replaced with the new line.
            # In fileinput, print() is used to write to a file.
            # Whitespaced is stripped and the end of the line is \n to maintain a standard organisation in the file.
            print(str(new_line).strip(), end='\n')
        # Otherwise the same line is printed
        else:
            print(str(line).strip(), end='\n')

def menu_selection(current_user):
    '''
    Generates the user's selection from the main menu in the task manager.
    :param current_user: The current user who's logged in is needed to check if the user is the admin.
    The admin gets extra options in the main menu.
    :return: Returns the menu selection.
    '''
    # If the user is the admin they are given extra options to choose from
    if current_user == "admin":
        # .lower() is needed to make the user's choice non case sensitive
        menu_selection = input('''
Please select one of the following options below:

/ r - Registering a user
/ a - Adding a task
/ va - View all tasks
/ vm - View my task
/ s - Display statistics
/ gr - Generate reports
/ p - Change password
/ e - Exit

> ''').lower()
        
    else:
        menu_selection = input('''
Please select one of the following options below:

/ a - Adding a task
/ va - View all tasks
/ vm - View my task
/ p - Change password
/ e - Exit

> ''').lower()
    return menu_selection

# ====Logging in====

print("Welcome to the task manager. Please log in:")
# This infinite loop combined with a try, except block means that if the user.csv file is not found a new one is generated
# The new file will only contain the admin username and password.
while True:
    try:
        # Again an infinite loop means that the user is continually prompted in case of entering an invalid username or password
        while True:
            # The list of usernames and passwords is opened
            with open('user.csv', 'r', encoding='utf-8') as f:
                # The user is asked for their username and password
                current_user = input("User name: ")
                current_password = input("Password: ")
                # If the login() function returns True then the user is allowed to login and the loop breaks so the program can continue
                if login(f, current_user, current_password):
                    break
                else:
                    print("\033[91mInvalid username or password!\033[00m Please try again.")
        break
    except FileNotFoundError:
        with open('user.csv', 'w', encoding='utf-8') as f:
            f.write("admin, 8f8145e0f8d63c646e48f5a0377007c2193fce8c87399b5d9a59dec43b4cb45b\n")

# ====Choosing from the menu====

print(f"\nWelcome {current_user}!")
# The infinite loop means that the user is prompted after a function is finished or they make an invalid selection
# This block of code calls the menu_selection function and if it matches one of the menu items the corresponding
# function is executed
while True:
    menu = menu_selection(current_user)
    # To add a new task.
    if menu == 'a':
        new_task()
    # These options can only be executed if the user is an admin
    # To register a new user.
    elif menu == "r" and current_user == "admin":
        registration()
    # To view statistics
    elif menu == "s" and current_user == "admin":
        statistics()
        # For some options where the user views lists of information an input() is taken to pause the program so the user has time to read the information
        input("\nPress enter to return to main menu...")
    # To view all tasks.
    elif menu == 'va':
        view_all_tasks()
        input("Press enter to return to main menu...")
    # To view current user's tasks.
    elif menu == 'vm':
        while True:
            tasks_dict = view_current_users_tasks(current_user)
            if tasks_dict == False:
                break
            # After the view_current_users_tasks() function has been run the user is presented with another menu
            # This menu allows them to choose a task to edit.
            which_task = input('''
Please choose from the menu below: 
/ enter a task number - to edit or mark it as complete (only items marked '*' may be edited)
/ x - Return to main menu

> ''').lower()
            if which_task == 'x':
                break
            # This will only run if their selected task belongs to them and exists.
            elif which_task in tasks_dict:
                # If the task is complete it cannot be edited.
                if tasks_dict[which_task][5] == "Complete":
                    input("\n\033[91mThis task is complete and cannot be edited. Press try again.\033[00m\n")
                    continue
                # Otherwise the edit_task() function is run.
                edit_task(tasks_dict, which_task)
                break
            else:
                print("\n\033[91mYou have made a wrong choice!\033[00m Please try again.")
                continue
    # To generate reports as admin.
    elif menu == 'gr' and current_user == "admin":
        if_success = generate_reports()
        if if_success == True:
            input("Reports generated sucessfully. Press enter to return to the main menu...")
    # To change the user's password.
    elif menu == 'p':
        # Count is needed to keep track of which line in the user's username and password is located.
        count = 0
        # The user.csv file is opened in read only mode.
        with open('user.csv', 'r', encoding='utf-8') as f:
            for line in f:
                # Each line is counted.
                count += 1
                # Whitespace is removed
                line = line.strip()
                # If the line is not empty.
                if line:
                    # The line is split into a list so it can be read easily.
                    line_list = line.split(',')
                    # If the current line contains the user's information the for loop and count stops.
                    if line_list[0] == current_user:
                        break
        # The user is asked to set a new password.
        while True:
            new_password = input("New password: ")
            new_password_2 = input("Confirm password: ")
            # If the confirmation matches the edit_line() function will update the user's password in user.csv.
            # count contains the line the username and password is on.
            if new_password == new_password_2:
                edit_line('user.csv', count, f"{current_user}, {hashlib.sha256(new_password.encode()).hexdigest()}")
                input("Password updated successfully! Press enter to return to main menu...")
                break
            # If the passwords didn't match then the user is prompted again.
            else:
                print("\nPasswords do not match. Please try again.\n")
    # If the user chooses to exit the SystemExit exception is raised which exits the program
    elif menu == 'e':
        print('Program exiting...')
        raise SystemExit
    # If the user doesn't make a valid selection they are informed and the loop repeats meaning they can choose again
    else:
        print("\033[91mYou have made a wrong choice!\033[00m Please try again.")
