import sqlite3

# constants
ADD_TASK = 1
DISPLAY_TASK_LIST = 2
DISPLAY_COMPLETED_LIST = 3
MARK_COMPLETED = 4
DELETE_TASK = 5
CLEAR_COMPLETED_LIST = 6
EXIT = 7
MENU_SIZE = 7
ERROR_RETURN = -1


# functions
def display_menu():
    options = {
        ADD_TASK: "Enter a new task(s).",
        DISPLAY_TASK_LIST: "Display task list.",
        DISPLAY_COMPLETED_LIST: "Display completed task list.",
        MARK_COMPLETED: "Mark a task as completed.",
        DELETE_TASK: "Delete a task from the task list.",
        CLEAR_COMPLETED_LIST: "Clear completed task list.",
        EXIT: "Exit app.",
    }
    for key, value in options.items():
        print(f"{key}. {value}")


def get_num(prompt):
    try: 
        user_input = int(input(prompt))
        return user_input
    except ValueError:
        return ERROR_RETURN


def add_task(task_list, cursor, conn):
    num_of_tasks = get_num("Enter the number of tasks you want to add: ")
    if num_of_tasks <= 0:
        return ERROR_RETURN
    for i in range(0, num_of_tasks):
        task = input(f"Enter task #{i+1}: ")
        task_list.append(task)
        cursor.execute("INSERT INTO task_list (task_number, task_desc) VALUES (?, ?)", (i + 1, task))
        conn.commit()
    return len(task_list)


def display_task_list(list):
    for i in range(len(list)):
        print(f"{i+1}. {list[i]}")


def mark_completed(task_list, completed_list, cursor, conn):
    print("Task List.")
    display_task_list(task_list)

    if len(task_list) < 1:
        return ERROR_RETURN

    completed_task_i = get_num("Enter a task # to mark completed: ")

    if completed_task_i > 0 and completed_task_i <= len(task_list):
        completed_task = task_list[completed_task_i - 1]
        completed_list.append(completed_task)
        cursor.execute("INSERT INTO completed_task_list (task_number, task_desc) VALUES (?, ?)",
                       (len(completed_list), completed_task))
        cursor.execute("DELETE FROM task_list WHERE task_desc = ?", (completed_task,))
        conn.commit()
        task_list.remove(completed_task)
    else:
        return ERROR_RETURN


def delete_task(task_list, cursor, conn):
    print("Task List.")
    display_task_list(task_list)

    if len(task_list) < 1:
        return ERROR_RETURN
    
    delete_task_i = get_num("Enter a task # to delete from task list: ")
    print("\n")

    if delete_task_i > 0 and delete_task_i <= len(task_list):
        deleted_task = task_list[delete_task_i - 1]
        cursor.execute("DELETE FROM task_list WHERE task_desc = ?", (deleted_task,))
        conn.commit()
        task_list.remove(deleted_task)
    else:
        return ERROR_RETURN


# main function
def main():
    task_list = []
    completed_task_list = []
    taking_input = True

    conn = sqlite3.connect("tasklist.db")
    cursor = conn.cursor()

    cursor.execute(""" CREATE TABLE IF NOT EXISTS task_list (
                   task_number INT,
                   task_desc TEXT
                    )""")
    
    cursor.execute(""" CREATE TABLE IF NOT EXISTS completed_task_list (
                   task_number INT,
                   task_desc TEXT
                    )""")

    cursor.execute("SELECT task_desc FROM task_list")
    task_list = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT task_desc FROM completed_task_list")
    completed_task_list = [row[0] for row in cursor.fetchall()]

    conn.commit()


    while(taking_input):
        display_menu()

        menu_choice = get_num("Select an option: ")
        print("\n")

        if menu_choice == ERROR_RETURN or menu_choice <= 0 or menu_choice > MENU_SIZE :
            print("Error. Enter a valid number.")

        if menu_choice == ADD_TASK:
            num_tasks = add_task(task_list, cursor, conn)
            if num_tasks == ERROR_RETURN:
                print("Error. Enter a valid number.")
            else:
                print(f"Added {num_tasks} task(s) to task list.")
        
        if menu_choice == DISPLAY_TASK_LIST:
            print("Task List:")
            display_task_list(task_list)
        
        if menu_choice == DISPLAY_COMPLETED_LIST:
            print("Completed Task List:")
            display_task_list(completed_task_list)
        
        if menu_choice == MARK_COMPLETED:
            mark_completed_return = mark_completed(task_list, completed_task_list, cursor, conn)
            if mark_completed_return == ERROR_RETURN:
                print("Error. Enter a valid number.")
        
        if menu_choice == DELETE_TASK:
            delete_task_return = delete_task(task_list, cursor, conn)
            if delete_task_return == ERROR_RETURN:
                print("Error. Enter a valid number.")

        if menu_choice == CLEAR_COMPLETED_LIST:
            completed_task_list.clear()
            cursor.execute("DELETE FROM completed_task_list")
            conn.commit()
            print("Clearing completed list.")
        
        if menu_choice == EXIT:
            print("Exiting...")
            conn.close()
            taking_input = False
            break
        print("\n")


if __name__ == "__main__":
    main()