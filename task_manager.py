# importing libraries
import time, datetime

class Task:
    def __init__(self, username, title, description, due_date, assigned_date, status):
        self.username = username
        self.title = title
        self.description = description
        self.assigned_date = assigned_date
        self.due_date = due_date
        self.status = status
    
    def __str__(self):
        status = f'Task is Incomplete - Task due date: {self.due_date}' if self.status == 'No' else 'Task is Completed'
        output = f'''
        Assigned To: {self.username} on {self.assigned_date}
        Task Title: {self.title}
        ----------
        Description: {self.description}
        ---------
        {status}'''
        return output

# Login Section
def login_user():
    # Prompt for Username and Password
    print('\nLOGIN WITH USERNAME & PASSWORD\n----------')
    input_username = input('Enter Username:\n> ')
    input_password = input('Enter Password:\n> ')
    
    # Open and read user.txt in read mode
    with open('user.txt', 'r') as user:
        users = user.readlines()
        for u in users:
            user = u.split(',')
            username = user[0].strip().lower()
            password = user[1].strip().lower()
            if input_username.strip().lower() == username and input_password.strip().lower() == password:
                print('Successfully Logged In!')
                
                # Store username and password values in a dictionary for later use
                authenticated_user = {'username': username, 'password': password}
                return authenticated_user
            
    # Handle in valid credentials input
    print('Incorrect Credential! Please Try Again...\n')
    return login_user()
authenticated_user = login_user()

# Register Section
def register_user():
    # Prompt for Username and Password
    print('\nREGISTER A USER WITH USERNAME & PASSWORD\n----------')
    input_username = input('Enter Username:\n> ')
    input_password = input('Enter Password:\n> ')

    # Validate Input
    if input_username and input_password:
        print('registering...')
        time.sleep(1.5) # Simulate database read & write time
        
        # Open and read user.txt in append mode
        with open('user.txt', 'a') as append_user:
            for username in authenticated_user.keys():
                if username.lower() != input_username.lower():
                    new_user = f'\n{input_username}, {input_password}'
                    append_user.write(new_user)
                    print('User Successfully Registered!\nEnter any key to continue...')
                    input()
                    return
                else:
                    print('Username Already Exists! Please Try again...')
                    return register_user()
    else:
        print('Make sure "username" and "password" fields are filled out! Please Try Again...')
        return register_user()

# Fetch All Registered Users
def authenticated_users():
    authenticated_users = {}

    with open('user.txt', 'r') as read_users:
        users = read_users.readlines()
        
        # Update Auth User Dictionary
        for u in users:
            user = u.split(',')
            username = user[0].strip()
            password = user[1].strip('\n')
            authenticated_users.update({username.lower(): password.lower().strip()})

    # Return Dictionary of Authenticated Users
    return authenticated_users

# View Tasks Sections
def fetch_tasks(op):
    my_tasks = []
    all_tasks = []

    # Read Tasks from tasks.txt
    with open('tasks.txt', 'r') as read_tasks:
        tasks = read_tasks.readlines()
        for t in tasks:
            task_items = t.split(', ')
            # Create a task objects
            _task = Task(
                username=task_items[0],
                title=task_items[1],
                description=task_items[2],
                assigned_date=task_items[3],
                due_date=task_items[4],
                status=task_items[5])
            # Append Task object
            all_tasks.append(_task)

            # Check Task Assignee and Append if its a match with logged in username
            if _task.username == authenticated_user.get('username'):
                my_tasks.append(_task)

    # Test operation param
    if op == 'all':
        # Return all task objects
        return all_tasks
    elif op == 'mine':
        # Return only logged in user's task objects
        return my_tasks
    else:
        return None

# Add Task Section
def add_task():
    # Inverse Stop Flag - Exits Func.
    stop_flag = True

    # Prompt for New Task Fields
    print('\nADD A NEW TASK\n----------')
    input_username = input('Enter Username:\n> ')
    input_title = input('Enter the Task Title:\n> ')
    input_description = input('Enter the Task Description:\n> ')

    print('Task Due Date:')
    input_due_year = input('Enter the year for due date\n> ')
    input_due_month = input('Enter the month for due date\n> ')
    input_due_day = input('Enter the day for due date:\n> ')

    # Build due date format
    due_date = f'{input_due_year}-{input_due_month}-{input_due_day}'

    # Fetch Auth Users
    auth_users = authenticated_users()
    
    # Validate Inputs - Check that Assigned Username exists
    for username in auth_users.keys():
        print(username, input_username)
        if input_username == username:
            stop_flag = False
            break
    
    if stop_flag == False:
        # Create a new Task object
        _task = Task(
            username=input_username,
            title=input_title,
            description=input_description,
            due_date=due_date,
            assigned_date=datetime.datetime.now().date(),
            status='No')
        
        try:
            # Write Task object to tasks.txt
            with open('tasks.txt', 'a') as append_task:
                append_task.write(f'\n{_task.username}, {_task.title}, {_task.description}, {_task.assigned_date}, {_task.due_date}, {_task.status}')
            print('Successfully Added Task!')
            print(_task)
        except Exception as e:
            print(f'Something went wrong - {e}')
    else:
        print(f'No User with the Username: {input_username}')
        print('Enter any key to continue...')
        input()

# Statistics Section
def fetch_statistics():
    # Determine total user count
    auth_users = authenticated_users()
    total_users = len(auth_users)
    # Determine total task count
    all_tasks = fetch_tasks('all')
    total_tasks = len(all_tasks)

    # Return a dictionary of total users & tasks
    view_dict = {'total-users': total_users, 'total-tasks': total_tasks}
    return view_dict

# Special Menu Section
while True and authenticated_user.get('username') == 'admin':
    # Present the menu to the user and 
    # make sure that the user input is converted to lower case.
    special_menu = input('''Select one of the following options:
r - register a user
a - add task
va - view all tasks
vm - view my tasks
stats - display app statistics
e - exit
: ''').lower()

    if special_menu == 'r':
        register_user()
    elif special_menu == 'a':
        add_task()
    elif special_menu == 'va':
        tasks = fetch_tasks('all')
        for task_obj in tasks:
            print(task_obj)
        print('\nEnter any key to continue')
        input()
    elif special_menu == 'vm':
        tasks = fetch_tasks('mine')
        for task_obj in tasks:
            print(task_obj)
        print('\nEnter any key to continue')
        input()
    elif special_menu == 'stats':
        view_dict = fetch_statistics()
        print('\nAPPLICATION STATISTICS:\n---------')
        for key, value in view_dict.items():
            print(key, value, end='\n')
        print('\nEnter any key to continue')
        input()
    elif special_menu == 'e':
        print('Goodbye <3')
        exit()
    else:
        print("You have made entered an invalid input. Please try again")
        continue

# Standard Menu Section
else:
    while True:
        # Present the menu to the user and 
        # make sure that the user input is converted to lower case.
        standard_menu = input('''Select one of the following options:
    a - add task
    va - view all tasks
    vm - view my tasks
    e - exit
    : ''').lower()
        
        if standard_menu == 'a': # ADD TASK
            add_task()
        elif standard_menu == 'va':
            tasks = fetch_tasks('all')
            for task_obj in tasks:
                print(task_obj)
            print('\nEnter any key to continue')
            input()
        elif standard_menu == 'vm':
            tasks = fetch_tasks('mine')
            for task_obj in tasks:
                print(task_obj)
            print('\nEnter any key to continue')
            input()
        elif standard_menu == 'e':
            print('Goodbye <3')
            exit()
        else:
            print("You have made entered an invalid input. Please try again")
            continue
# EOF - Branden v Staden