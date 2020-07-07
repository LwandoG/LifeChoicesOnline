from time import strftime

import mysql.connector
import datetime

my_database = mysql.connector.connect(host='localhost', user='root', password='1234', database='lifechoicesonline')
cursor = my_database.cursor(buffered=True)


# this function authenticates the entered credentials with those in the database.
def authenticate(username, password):
    cursor.execute("SELECT username FROM users WHERE username = %s AND password = %s", (username, password))
    result = cursor.fetchall()
    if len(result) > 0:
        return True
    else:
        return False


# This function returns all usernames in the database. It's used to check that a new username is not in database already
def get_usernames():
    cursor.execute("SELECT username FROM users;")
    usernames = cursor.fetchall()
    username_list = []
    for each in usernames:
        username_list.append(each[0])
    return username_list


def sign_in(username):
    # check if the user is not inside already
    cursor.execute("SELECT logid FROM logsTable WHERE username = %s AND signout IS NULL", (username, ))
    log_test = cursor.fetchall()
    if len(log_test) == 0:
        cursor.execute("INSERT INTO logsTable(username, signin, inside) VALUES(%s, %s, %s)", (username,
                                                                                              datetime.datetime.now(),
                                                                                              1))
        my_database.commit()
        return True
    else:
        return False


def signout(username):
    cursor.execute("SELECT MAX(logid) FROM logsTable WHERE username = %s AND signout IS NULL", (username, ))
    latest_raw = cursor.fetchall()
    latest_log = latest_raw[0][0]
    # check if user is signed in.
    if latest_log is None:
        return False
    else:
        cursor.execute("UPDATE logsTable SET signout = %s, inside = 0 WHERE logid = %s", (datetime.datetime.now(),
                                                                                          latest_log))
        my_database.commit()
        return True


# The following function returns the user's full name.
def get_name(username):
    cursor.execute('SELECT full_name FROM users WHERE username = %s', (username, ))
    return cursor.fetchall()[0][0]


# this function check if an entered username belongs to an admin
def admin(username):
    cursor.execute("SELECT role FROM users WHERE username = %s", (username, ))
    result = cursor.fetchall()
    role = result[0][0]
    if role == "admin":
        return True
    else:
        return False


def remove_user(username):
    cursor.execute("DELETE FROM logsTable WHERE username = %s", (username, ))
    my_database.commit()
    cursor.execute("DELETE FROM users WHERE username = %s", (username, ))
    my_database.commit()


def upgrade(username):
    cursor.execute("UPDATE users SET role = 'admin'")
    my_database.commit()


def downgrade(username, role):
    cursor.execute("UPDATE users SET role = %s WHERE username = %s", (role, username))
    my_database.commit()


# list of people who signed in today.
def show_sign_ins():
    date_string1 = datetime.date.today().strftime('%Y-%m-%d')
    cursor.execute('SELECT username FROM logsTable WHERE DATE(signin) = %s', (date_string1, ))
    result_list = cursor.fetchall()
    return result_list


# list of people who signed in today.
def show_sign_outs():
    date_string1 = datetime.date.today().strftime('%Y-%m-%d')
    cursor.execute('SELECT username FROM logsTable WHERE DATE(signout) = %s', (date_string1,))
    result_list = cursor.fetchall()
    return result_list


def inside():
    cursor.execute('SELECT username FROM logsTable WHERE inside = 1')
    result_list = cursor.fetchall()
    return result_list


# User class to make registration easy.
class User:
    def __init__(self, full_name, username, password, role):
        self.full_name = full_name
        self.username = username
        self.password = password
        self.role = role

    def register(self):
        cursor.execute('INSERT INTO users(full_name, username, password, role) VALUES (%s, %s, %s, %s)', (self.full_name,
                                                                                                          self.username,
                                                                                                          self.password,
                                                                                                          self.role))
        my_database.commit()
