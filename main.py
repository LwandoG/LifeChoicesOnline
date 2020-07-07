import getpass
import user
import datetime


# This is the local sign in function. It is used to print the appropriate message based on the result of the sign in
# function from the user module.
def sign_in(user_name):
    if user.sign_in(user_name):
        print("Signed in successfully. Enjoy your day.")
    else:
        print("Already signed in. Signout first.")


# This is the local sign out function. It is used to print the appropriate message based on the result of the sign out
# function from the user module.
def sign_out(user_name):
    if user.signout(user_name):
        print("Successfully signed out.")
    else:
        second_option = input("Not signed in.\n1. Sign in?\n2. Exit?\n")  # Can't sign out if not signed in.
        if second_option == '1':
            sign_in(user_name)
        else:
            exit(0)


option = input('Please select an option below: \n1.Login.\n2.Register.\n')
if option == '1':
    username = input('Please enter your username: ')
    password = input('Enter password: ')
    if user.authenticate(username, password):  # username and password authentication
        print('Welcome ', user.get_name(username))
        print('Please choose an option below:')
        log = input('1. Sign-in.\n2. Signout.\n')
        if log == '1':
            sign_in(username)

        elif log == '2':
            sign_out(username)
        else:
            print('Incorrect selection.')  # Error handling

    else:
        print('Incorrect username and password combination.')
elif option == '2':
    print('Welcome to the registration page.')
    full_name = input('Please enter your full name: ')
    username = input('Please enter your username: ')
    while username in user.get_usernames():  # this is to make sure no two users share the same username.
        username = input('Username already taken. Please enter your username: ')
    password = input('Enter password: ')
    role = input('Are you a visitor, student or an employee? ')
    while role not in ['visitor', 'student', 'employee']:  # to ensure the user doesn't select random roles.
        role = input('Incorrect input. Are you a visitor, student or an employee? ')
    new_user = user.User(full_name, username, password, role)  # creating a new user object.
    new_user.register()  # registering the new user
    second_option = input("Welcome to LifeChoices.\n1. Sign in?\n2. Exit?\n")
    if second_option == '1':
        sign_in(username)
    else:
        exit(0)

elif option == 'a':
    print('Welcome to the admin page.')
    username = input('Please input your admin username: ')
    password = input('Please input your admin password: ')
    if user.authenticate(username, password):
        if user.admin(username):  # ensuring the user is an actual admin.
            # admin privileges, each option is self explanatory.
            selection = input('Please choose an option:\n1. Sign in.\n2. Sign out.\n3. Add new user.\n4. Remove user\n'
                              '5. Upgrade user to admin.\n6. Downgrade admin to normal user\n7. Show people who have '
                              'signed in today.\n8. Show people who have signed out today.\n9. Show people who are '
                              'inside.\n')
            if selection == '1':
                sign_in(username)
            elif selection == '2':
                user.sign_out(username)
            elif selection == '3':
                full_name = input('Please enter the full name: ')
                username = input('Please enter the username: ')
                while username in user.get_usernames():
                    username = input('Username already taken. Please enter another username: ')
                password = input('Enter password: ')
                role = input('Is this user a visitor, student, employee or an admin? ')
                while role not in ['visitor', 'student', 'employee', 'admin']:
                    role = input('Incorrect input. Is the user a visitor, student, employee or an admin? ')
                new_user = user.User(full_name, username, password, role)
                new_user.register()
                print("Successfully registered new user.")
            elif selection == '4':
                expelled_user = input("Enter the username of the user to be removed: ")
                if expelled_user in user.get_usernames():
                    user.remove_user(expelled_user)
                else:
                    print("Username does not exist.")
            elif selection == '5':
                new_admin = input("Enter username to be upgraded: ")
                if new_admin in user.get_usernames():
                    user.upgrade(new_admin)
                    print("Successfully upgraded ", user.get_name(new_admin))
                else:
                    print("Username not in database.")
            elif selection == '6':
                downgrade = input("Enter username to be downgraded: ")
                new_role = input("Enter new role: ")
                while new_role not in ['visitor', 'student', 'employee']:
                    role = input('Incorrect input. Is the user a visitor, student or an employee? ')
                user.downgrade(downgrade, new_role)
                print("Successfully downgraded ", user.get_name(downgrade))
            elif selection == '7':
                result_list = user.show_sign_ins()
                print("List of people who signed in today:")
                for each in result_list:
                    print(user.get_name(each[0]))   # extracting the names from the list of tuples returned
            elif selection == '8':
                result_list = user.show_sign_outs()
                print("List of people who signed out today:")
                for each in result_list:
                    print(user.get_name(each[0]))   # extracting the names from the list of tuples returned
            elif selection == '9':
                result_list = user.inside()
                print("List of people who are inside:")
                for each in result_list:
                    print(user.get_name(each[0]))  # extracting the names from the list of tuples returned
            else:
                print("Invalid selection.")
        else:
            print('You do not have admin rights.')
    else:
        print('Invalid credentials.')
else:
    print('Invalid input.')
