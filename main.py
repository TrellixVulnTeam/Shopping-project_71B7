from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = 'development key'


@app.route('/')
def login():
    return render_template('scratch.html')


@app.route('/viewerform')
def viewerform():
    return render_template("viewerform.html")


@app.route('/viewerresults', methods=['GET', 'POST'])
def viewer():
    # defining variables
    user = request.form['user']
    if user == 'no_filter':
        user = None
    date_opened = request.form['date_opened']
    if date_opened == '':
        date_opened = None
    date_fulfilled = request.form['date_fulfilled']
    if date_fulfilled == '':
        date_fulfilled = None
    frequent_item = request.form['frequent_item']
    if frequent_item == 'no_filter':
        frequent_item = None
    # constructing sql call terms
    counter = 0
    if user is None:
        user_filter = ''
    else:
        user_filter = 'user = ' + "'" + user + "'" + ' AND '
        counter = counter + 1
    if date_opened is None:
        date_opened_filter = ''
    else:
        date_opened_filter = 'date_opened = ' + date_opened + ' AND '
        counter = counter + 1
    if date_fulfilled is None:
        date_fulfilled_filter = ''
    else:
        date_fulfilled_filter = 'date fulfilled = ' + date_fulfilled + ' AND '
        counter = counter + 1
    if frequent_item is None:
        frequent_item_filter = ''
    else:
        frequent_item_filter = 'frequent_item = ' + "'" + frequent_item + "'" + ' AND '
        counter = counter + 1

    # constructing where clause from sql call terms
    if counter == 0:
        where_clause = ''
    elif counter == 1:
        where_clause = ' WHERE ' + user_filter + date_opened_filter + date_fulfilled_filter + frequent_item_filter
        where_clause = where_clause.replace("AND", "")
    elif counter > 1:
        where_clause = ' WHERE ' + user_filter + date_opened_filter + date_fulfilled_filter + frequent_item_filter
        where_clause = where_clause[:-4]

    print(counter)
    print(where_clause)
    # putting together sql statement
    sql_statement = 'SELECT frequent_items.name as frequent_item, users.user, orders.date_opened, ' \
                    'orders.date_fulfilled FROM ((orders JOIN frequent_items ON orders.frequent_item_id = ' \
                    'frequent_items.id) JOIN ' \
                    'users ON orders.user_id = users.id)' + where_clause
    print(sql_statement)
    # connecting to database and executing sql statement
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute(sql_statement)
    rows = cur.fetchall()
    return render_template('viewerresults.html', rows=rows)


if __name__ == '__main__':
    app.run(debug=True)
