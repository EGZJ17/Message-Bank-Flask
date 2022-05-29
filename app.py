'''
At the command line, run 

conda activate PIC16B
export FLASK_ENV=development
flask run

# Sources

This set of lecture notes is based in part on previous materials developed by [Erin George](https://www.math.ucla.edu/~egeo/) (UCLA Mathematics) and the tutorial [here](https://stackabuse.com/deploying-a-flask-application-to-heroku/). 
'''
from flask import Flask, g, render_template, request
from flask import redirect, url_for, abort
import sqlite3

app = Flask(__name__)


# specify that the below function will be called when '/' is appended to the webpage's URL
@app.route('/')
def main():
    return render_template('main.html')


def get_message_db():
    try:
        return g.message_db # return the database if it already exists

    except: # otherwise, initialize the database

        # create the messages_db.sqlite database
        g.message_db = sqlite3.connect("messages_db.sqlite")

        # use a sqlite command to create a table called "messages" with three columns
        cmd = \
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            handle TEXT NOT NULL)
        """

        # create a cursor object referencing the database and execute the command
        cursor = g.message_db.cursor()
        cursor.execute(cmd)

        return g.message_db


def insert_message():

    # use request object to get the user's input for 'message',
    # the name attribute corresponding to the textarea element
    # that holds the user's message
    message = request.form['message']

    # use request object to get the user's input for 'handle',
    # the name attribute corresponding to the input element
    # that holds the user's handle
    handle = request.form['handle']

    # open a connection to the database with the previously defined function
    conn = get_message_db()

    # create a sqlite command that inserts the user's message and handle 
    # into the database
    cmd = \
    f"""
    INSERT INTO messages (message, handle) 
    VALUES ('{message}', '{handle}')
    """

    # create a cursor object referencing the database and execute the command
    cursor = conn.cursor()
    cursor.execute(cmd)

    # use commit() to save the changes to the database, and close the connection
    conn.commit()
    conn.close()

    return message, handle


# specify that the below function will be called when '/submit/' is appended to the 
# webpage's URL; also specify that this function will make use of POST and GET methods
@app.route('/submit/', methods=['POST', 'GET'])
def submit():

    # render the page if the user only accesses the webpage without submitting a form
    if request.method == 'GET':
        return render_template('submit.html')

    # otherwise, the user submitted the form
    else:
        try: # call insert_message() and save its return values
            message, handle = insert_message()

            # render the page with various defined variables that can be used by Jinja
            # to manipulate the webpage
            return render_template('submit.html', Thanks=True, message=message, handle=handle)

        except: # if an error occurred, render the webpage while specifying the error
            return render_template('submit.html', error=True)



def random_messages(n):

    # connect to the database with the previously defined function
    conn = get_message_db()

    # create a sqlite command that randomly selects n many entries from the 
    # messages table, n being specified by the function call
    cmd = \
    f"""
    SELECT * FROM messages ORDER BY RANDOM() LIMIT {n}
    """

    # create a cursor object referencing the database and execute the command
    cursor = conn.cursor()
    cursor.execute(cmd)

    # fetchall() the selections, assign it to result, and close the connection
    result = cursor.fetchall()
    conn.close()

    return result


# specify that the below function will be called when '/view/' is appended to the 
# webpage's URL
@app.route('/view/')
def view(): 
    # render the page with a messages variable that holds the result of a call to
    # random_messages() with argument 5
    return render_template('view.html', messages=random_messages(5))