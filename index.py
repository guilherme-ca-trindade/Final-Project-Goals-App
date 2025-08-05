import json
import os
import questionary

msg= 'Welcome to your Goals app! =) ' \
'\nHere you can create, list, mark and delete your goals!'
goals=[]

def load_goals():
    global goals
    try:
        with open("goals.json","r",encoding="utf-8") as f:
            goals=json.load(f)
    except Exception:
        goals=[]

def save_goals():
    with open("goals.json","w",encoding="utf-8") as f:
        json.dump(goals, f, ensure_ascii=False, indent=2)

def create_goals():
    global msg
    goal= questionary.text('Type the goal you want to create: ').ask()
    if not goal:
        msg = "The goal can't be empty"
        return
    goals.append({"value":goal, "checkend":False})
    msg = "Goal created with success!"

def list_goals():
    global msg
    if not goals:
        msg = "Doesn't exist goals currently"
        return
    choices = [questionary.Choice(g['value'], checked=g['checkend'])
               for g in goals]
    answers = questionary.checkbox(
        "Use the arrows to change the goal, spacebar to mark or unmark the goal, and the Enter to finalize this process",
        choices=choices
    ).ask()
    for g in goals:
        g['checkend'] = False
    if not answers:
        msg = "No goal selected"
        return
    for a in answers:
        for g in goals:
            if g['value'] == a:
                g['checkend'] = True
    msg = "Goal(s) selected as finished!"

def finished_goals():
    global msg
    if not goals:
        msg = "Doesn't exist goals currently"
        return
    finished = [g for g in goals if g['checkend']]
    if not finished:
        msg = "Doesn't exist finished goals at moment! =("
        return
    questionary.select(
        f"Finished goals: {len(finished)}", 
        choices=[g['value'] for g in finished]
    ).ask()

def open_goals():
    global msg
    if not goals:
        msg = "Doesn't exist goals currently"
        return
    open = [g for g in goals if not g['checkend']]
    if not open:
        msg = "Doesn't exist open goals at moment =("
        return
    questionary.select(
        f"Open Goals: {len(open)}",
        choices=[g['value'] for g in open]
    ).ask()

def delete_goals():
    global msg, goals
    if not goals:
        msg = "Doesn't exist goals currently"
        return
    choices = [g['value'] for g in goals]
    delete_item= questionary.checkbox(
        "Select the goal that you want to delete: ",
        choices=choices
    ).ask()
    if not delete_item:
        msg = "No goals selected to delete"
        return
    goals = [g for g in goals if g['value'] not in delete_item]
    msg = "Goal(s) deleted with success! "

def show_msg():
    os.system('clear')
    global msg
    if msg:
        print(msg)
        print('')
        msg = ''

def main():
    load_goals()
    while True:
        show_msg()
        save_goals()
        option = questionary.select(
            "Menu > ",
            choices = [
                "Create goal",
                "List goals",
                "Finished goals",
                "Open goals",
                "Delete goal",
                "Exit the program"
            ]
        ).ask()
        print(f"Selected option: {option}")  # Debug print
        if option == "Create goal":
            create_goals()
        elif option == "List goals":
            list_goals()
        elif option == "Finished goals":
            finished_goals()
        elif option == "Open goals":
            open_goals()
        elif option == "Delete goal":
            delete_goals()
        elif option == "Exit the program":
            print("See you soon! " \
            "\nThank you! Merci! Obrigado! ")
            break

if __name__ == "__main__":
    main()


