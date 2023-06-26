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

def load_data():
    global users, tasks

    users = {}
    tasks = []

    # Load user data from user.txt
    with open('user.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split(';')
            users[username] = password

    # Load task data from tasks.txt
    with open('tasks.txt', 'r') as file:
        for line in file:
            task_data = line.strip().split(';')
            tasks.append(task_data)


def save_data():
    # Save user data to user.txt
    with open('user.txt', 'w') as file:
        for username, password in users.items():
            file.write(f"{username};{password}\n")

    # Save task data to tasks.txt
    with open('tasks.txt', 'w') as file:
        for task in tasks:
            file.write(';'.join(task) + '\n')


def print_main_menu():
    print("\nPlease select one of the following options:")
    print("r - register user")
    print("a - add task")
    print("va - view all tasks")
    print("vm - view my tasks")
    print("gr - generate reports")
    print("ds - display statistics")
    print("e - exit")


def reg_user(): 
    # When the user selects 'r' to register a user
    username = input("Enter a new username: ")

    if username in users:
        print("Username already exists. Please try again with a different username.")
        # Making sure that usernames aren't duplicated when adding a new user
        return

    password = input("Enter a password: ")
    confirm_password = input("Confirm password: ")

    if password != confirm_password:
        print("Passwords do not match. User registration failed.")
        return

    users[username] = password
    print("User registration successful.")


def add_task(): 
    # When a user selects 'a' to add a new task
    username = input("Enter the username of the person the task is assigned to: ")
    title = input("Enter the title of the task: ")
    description = input("Enter a description of the task: ")
    due_date = input("Enter the due date (YYYY-MM-DD) of the task: ")
    completed = "No"

    task_data = [username, title, description, due_date, completed]
    tasks.append(task_data)

    print("Task added successfully.")


def view_all(): 
    # When users type 'va' to view all the tasks listed in 'tasks.txt'
    print("\nAll Tasks:")
    for index, task in enumerate(tasks, start=1):
        print(f"\nTask {index}:")
        print(f"Assigned to: {task[0]}")
        print(f"Title: {task[1]}")
        print(f"Description: {task[2]}")
        print(f"Due Date: {task[3]}")
        print(f"Completed: {task[4]}")

    if not tasks:
        print("No tasks found.")


def view_mine(): 
    # When users type 'vm' to view all the tasks that have been assigned to them
    username = input("Enter your username: ")

    user_tasks = [task for task in tasks if task[0] == username]

    if not user_tasks:
        print("No tasks assigned to you.")
        return

    print("\nYour Tasks:")
    for i, task in enumerate(user_tasks):
        print(f"\nTask {i + 1}:")
        print(f"Assigned to: {task[0]}")
        print(f"Description: {task[1]}")
        print(f"Due Date: {task[3]}")
        print(f"Completed: {task[4]}")

    task_number = input("Enter the task number to select a specific task (or -1 to return to the main menu): ")

    if task_number == "-1":
        return

    try:
        task_index = int(task_number) - 1
        selected_task = user_tasks[task_index]
    except (ValueError, IndexError):
        print("Invalid task number.")
        return

    print("\nSelected Task:")
    print(f"Assigned to: {selected_task[0]}")
    print(f"Description: {selected_task[1]}")
    print(f"Due Date: {selected_task[3]}")
    print(f"Completed: {selected_task[4]}")

    action = input("Choose an action for the task (1: Mark as Complete, 2: Edit Task): ")

    if action == "1":
        if selected_task[4] == "Yes":
            print("This task is already marked as complete.")
        else:
            selected_task[4] = "Yes"
            print("Task marked as complete.")
    elif action == "2":
        if selected_task[4] == "Yes":
            print("This task cannot be edited as it is already marked as complete.")
        else:
            edit_option = input("Choose an option to edit (1: Username, 2: Due Date): ")

            if edit_option == "1":
                new_username = input("Enter the new username: ")
                selected_task[0] = new_username
                print("Task username updated.")
            elif edit_option == "2":
                new_due_date = input("Enter the new due date (YYYY-MM-DD): ")
                selected_task[3] = new_due_date
                print("Task due date updated.")
            else:
                print("Invalid edit option.")
    else:
        print("Invalid action.")

    save_data()


def generate_reports():
    # Added option to generate reports
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task[4] == "Yes")
    uncompleted_tasks = sum(1 for task in tasks if task[4] == "No")
    overdue_tasks = sum(1 for task in tasks if task[4] == "No" and task[3] < today_date())

    incomplete_percentage = (uncompleted_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    overdue_percentage = (overdue_tasks / uncompleted_tasks) * 100 if uncompleted_tasks > 0 else 0

    with open('task_overview.txt', 'w') as file:
        file.write(f"Total tasks: {total_tasks}\n")
        file.write(f"Completed tasks: {completed_tasks}\n")
        file.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
        file.write(f"Overdue tasks: {overdue_tasks}\n")
        file.write(f"Incomplete percentage: {incomplete_percentage}%\n")
        file.write(f"Overdue percentage: {overdue_percentage}%\n")

    user_stats = {}

    for task in tasks:
        username = task[0]

        if username not in user_stats:
            user_stats[username] = {
                'total_tasks': 0,
                'completed_tasks': 0,
                'incomplete_tasks': 0,
                'overdue_tasks': 0
            }

        user_stats[username]['total_tasks'] += 1

        if task[4] == "Yes":
            user_stats[username]['completed_tasks'] += 1
        else:
            user_stats[username]['incomplete_tasks'] += 1

            if task[3] < today_date():
                user_stats[username]['overdue_tasks'] += 1

    with open('user_overview.txt', 'w') as file:
        file.write(f"Total users: {len(users)}\n")
        file.write(f"Total tasks: {total_tasks}\n")

        for username, stats in user_stats.items():
            total_user_tasks = stats['total_tasks']
            completed_user_tasks = stats['completed_tasks']
            incomplete_user_tasks = stats['incomplete_tasks']
            overdue_user_tasks = stats['overdue_tasks']

            percentage_assigned = (total_user_tasks / total_tasks) * 100 if total_tasks > 0 else 0
            percentage_completed = (completed_user_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0
            percentage_incomplete = (incomplete_user_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0
            percentage_overdue = (overdue_user_tasks / incomplete_user_tasks) * 100 if incomplete_user_tasks > 0 else 0

            file.write(f"\nUsername: {username}\n")
            file.write(f"Total tasks assigned: {total_user_tasks}\n")
            file.write(f"Percentage of tasks assigned: {percentage_assigned}%\n")
            file.write(f"Percentage of tasks completed: {percentage_completed}%\n")
            file.write(f"Percentage of tasks incomplete: {percentage_incomplete}%\n")
            file.write(f"Percentage of tasks overdue: {percentage_overdue}%\n")


def display_statistics():
    with open('task_overview.txt', 'r') as file:
        task_data = file.read()
        print("\nTask Overview:")
        print(task_data)

    with open('user_overview.txt', 'r') as file:
        user_data = file.read()
        print("\nUser Overview:")
        print(user_data)


def today_date():
    # Returns the current date in the format YYYY-MM-DD
    from datetime import date
    return str(date.today())


def main():
    load_data()

    while True:
        print_main_menu()
        option = input("Enter your option: ")

        if option == "r":
            reg_user()
        elif option == "a":
            add_task()
        elif option == "va":
            view_all()
        elif option == "vm":
            view_mine()
        elif option == "gr":
            generate_reports()
            print("Reports generated successfully.")
        elif option == "ds":
            display_statistics()
        elif option == "e":
            save_data()
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == '__main__':
    main()
