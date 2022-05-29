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
import numpy as np
import sqlite3

app = Flask(__name__)

# Create main page
@app.route('/')
def main():
    return render_template('main.html')

# Submit Page
@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    # user's first time at submit page, show form
    if request.method == 'GET':
        return render_template('submit.html')

# If user submitted form
    else:
        insert_message(request)
        try: 
            #pass the filled in parameters
            return render_template('submit.html', thanks=True)
        #if there is an error
        except: 
            return render_template('submit.html', error=True)



def get_message_db():
    #if db exists, return it
    try:
        return g.message_db 
    #create db
    except: 
        # connect to that database, ensuring that the connection is an attribute of g
        g.message_db = sqlite3.connect("messages_db.sqlite")

        # SQL command to create three columns
        cmd = \
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER, 
            message TEXT NOT NULL,
            handle TEXT NOT NULL)
        """
        cursor = g.message_db.cursor()
        cursor.execute(cmd)
        return g.message_db


def insert_message(request):

    # store user's submitted message
    message = request.form['message']
    # store user's submitted name
    handle = request.form['handle']

    # open the connection
    conn = get_message_db()
    cursor = conn.cursor()

    #count rows and assign unique id
    cursor.execute("select count(*) from messages")
    rows = cursor.fetchone()[0]
    message_id = 1 + rows

    # create a sqlite command that inserts the user's message and handle 
    # into the database
    cmd = \
    f"""
    INSERT INTO messages (id, message, handle) 
    VALUES ('{message_id}', '{message}', '{handle}')
    """

    cursor.execute(cmd)
    # ensure row insertion has been saved
    conn.commit()
    #close the connection
    conn.close()

    return message, handle




def random_messages(n):

    # open the connection
    conn = get_message_db()

    # initialize cursor
    cursor = conn.cursor()

    #get n random messages
    cmd = \
    f"""
    SELECT * FROM messages ORDER BY RANDOM() LIMIT {n}
    """

    cursor.execute(cmd)

    # store in list 
    message_list = cursor.fetchall()
    #close the connection
    conn.close()

    return message_list


# view page
@app.route('/view/')
def view(): 
    # get 3 random messages to view
    return render_template('view.html', messages=random_messages(3))