from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import openpyxl
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from handlers.scheduler_handler import send_emails
from services import admin_login_service, admin_data_service
from services import chatbot_service
import sqlite3

# def delete_table(database, table_name):
#     try:
#         # Connect to the SQLite database
#         conn = sqlite3.connect(database)
#
#         # Create a cursor object
#         cursor = conn.cursor()
#
#         # SQL statement to delete the table
#         sql = f'DROP TABLE IF EXISTS {table_name}'
#
#         # Execute the SQL statement
#         cursor.execute(sql)
#
#         # Commit the changes and close the connection
#         conn.commit()
#         conn.close()
#         print(f"Table '{table_name}' has been deleted successfully.")
#     except sqlite3.Error as e:
#         print(f"Error deleting table: {e}")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#
#
# # Usage example:
# # Replace 'your_database.db' with the path to your SQLite database file
# # Replace 'your_table_name' with the name of the table you want to delete
# delete_table('details.db', 'details')

# app = Flask(__name__)
app = Flask(__name__, template_folder='templates')
app.secret_key = 'mysecretkey1234567890'

app.register_blueprint(admin_login_service.admin_login_bp)
app.register_blueprint(admin_data_service.admin_data_bp)
app.register_blueprint(chatbot_service.chatbot_bp)

# Database configuration
DB_NAME = 'details2.db'


def create_tables():
    print("lets create")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS details (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT,
                    middle_name TEXT,
                    last_name TEXT,
                    phone_number TEXT,
                    email_address TEXT,
                    sex TEXT,
                    age INTEGER,
                    date_of_birth TEXT,
                    address TEXT,
                    state TEXT,
                    risk_class TEXT,
                    face_amount TEXT,              
                    death_benefit_option TEXT,    
                    premium_mode TEXT,            
                    premium_schedule TEXT,         
                    section TEXT,              
                    ltc_amount TEXT,           
                    maximum_monthly_benefit TEXT,  
                    rate TEXT,                
                    term TEXT,                    
                    benefit_durations TEXT,    
                    inflation_benefit_option TEXT,
                    consultant TEXT,  
                    location TEXT,    
                    time TEXT         
                    )''')
    # c.execute('''CREATE TABLE IF NOT EXISTS details (
    #             id INTEGER PRIMARY KEY AUTOINCREMENT,
    #             first_name TEXT,
    #             middle_name TEXT,
    #             last_name TEXT,
    #             phone_number TEXT,
    #             email_address TEXT,
    #             sex TEXT,
    #             age INTEGER,
    #             date_of_birth TEXT,
    #             address TEXT,
    #             state TEXT,
    #             risk_class TEXT,
    #             face_amount TEXT,
    #             death_benefit_option TEXT,
    #             premium_mode TEXT,
    #             premium_schedule TEXT,
    #             section TEXT,
    #             ltc_amount TEXT,
    #             maximum_monthly_benefit TEXT,
    #             rate TEXT,
    #             term TEXT,
    #             benefit_durations TEXT,
    #             inflation_benefit_option TEXT
    #             )''')
    conn.commit()
    conn.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    form_data = {
        'first_name': '',
        'middle_name': '',
        'last_name': '',
        'phone_number': '',
        'email_address': '',
        'sex': '',
        'age': '',
        'date_of_birth': '',
        'address': '',
        'state': '',
        'risk_class': '',
        'face_amount': '',
        'death_benefit_option': '',
        'premium_mode': '',
        'section': '',
        'ltc_amount': '',
        'maximum_monthly_benefit': '',
        'rate': '',
        'term': '',
        'premium_schedule': '',
        'benefit_durations': '',
        'inflation_benefit_option': ''
    }
    inserted_data = {}

    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        data = request.json
        for key, value in data.items():
            if value != '':
                form_data[key] = value



        # form_data['first_name'] = data['first_name']
        # form_data['middle_name'] = data['middle_name']
        # form_data['last_name'] = data['last_name']
        # form_data['phone_number'] = data['phone_number']
        # form_data['email_address'] = request.form.get('email_address', '')
        # form_data['sex'] = request.form.get('sex', '')
        # form_data['age'] = request.form.get('age', '')
        # form_data['date_of_birth'] = request.form.get('date_of_birth', '')
        # form_data['address'] = request.form.get('address', '')
        # form_data['state'] = request.form.get('state', '')
        # form_data['risk_class'] = request.form.get('risk_class', '')
        # form_data['face_amount'] = request.form.get('face_amount', '')
        # form_data['death_benefit_option'] = request.form.get('death_benefit_option', '')
        # form_data['premium_mode'] = request.form.get('premium_mode', '')
        # form_data['section'] = request.form.get('section', '')
        #
        #
        # form_data['ltc_amount'] = request.form.get('ltc_amount', '')
        # form_data['maximum_monthly_benefit'] = request.form.get('maximum_monthly_benefit', '')
        # form_data['rate'] = request.form.get('rate', '')
        # form_data['term'] = request.form.get('term', '')
        #
        #
        # form_data['premium_schedule'] = request.form.get('premium_schedule', '')
        # form_data['benefit_durations'] = request.form.get('benefit_durations', '')
        # form_data['inflation_benefit_option'] = request.form.get('inflation_benefit_option', '')
        # #
        # # else:
        # #     print("inside else")
        # #     flash('Invalid section selected')
        # #     return redirect(url_for('index'))

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO details (
            first_name, middle_name, last_name, phone_number,
            email_address, sex, age, date_of_birth, address,
            state, risk_class, face_amount, death_benefit_option, premium_mode,
            section, ltc_amount, maximum_monthly_benefit,
            rate, term, premium_schedule, benefit_durations,
            inflation_benefit_option
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (
                  form_data['first_name'], form_data['middle_name'], form_data['last_name'],
                  form_data['phone_number'],
                  form_data['email_address'], form_data['sex'], form_data['age'], form_data['date_of_birth'],
                  form_data['address'],
                  form_data['state'], form_data['risk_class'], form_data['face_amount'],
                  form_data['death_benefit_option'], form_data['premium_mode'],
                  form_data['section'], form_data['ltc_amount'], form_data['maximum_monthly_benefit'],
                  form_data['rate'], form_data['term'], form_data['premium_schedule'],
                  form_data['benefit_durations'], form_data['inflation_benefit_option']
              )
              )
    conn.commit()

    # Get the ID of the last inserted row
    inserted_id = c.lastrowid
    session['latest_id'] = inserted_id

    # Query the inserted data using the ID
    c.execute('SELECT * FROM details WHERE id = ?', (inserted_id,))
    column_names = [description[0] for description in c.description]
    inserted_record = c.fetchone()
    if inserted_record:
        inserted_data = dict(zip(column_names, inserted_record))
    conn.close()

    print(inserted_data)
    return jsonify(inserted_data)


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         # Retrieve form data
#         first_name = request.form['first_name']
#         middle_name = request.form['middle_name']
#         last_name = request.form['last_name']
#         phone_number = request.form['phone_number']
#         email_address = request.form['email_address']
#         sex = request.form['sex']
#         age = request.form['age']
#         date_of_birth = request.form['date_of_birth']
#         address = request.form['address']
#         state = request.form['state']
#         risk_class = request.form['risk_class']
#         face_amount = request.form['face_amount']
#         death_benefit_option = request.form['death_benefit_option']
#         premium_mode = request.form['premium_mode']
#         premium_schedule = request.form['premium_schedule']
#         section = request.form['section']
#
#         if section == 'ltc_rider':
#             # Handle fields for LTC Rider section
#             ltc_amount = request.form['ltc_amount']
#             maximum_monthly_benefit = request.form['maximum_monthly_benefit']
#             rate = request.form['rate']
#             term = request.form['term']
#             benefit_durations = None
#             inflation_benefit_option = None  # Set to None for LTC Rider
#
#         elif section == 'linked_benefit_ltc':
#             # Handle fields for Linked Benefit LTC section
#             premium_schedule = request.form['premium_schedule']
#             benefit_durations = request.form['benefit_durations']
#             inflation_benefit_option = request.form['inflation_benefit_option']
#
#         else:
#             flash('Invalid section selected')
#             return redirect(url_for('index'))
#
#         # Save form data to the database
#         #  print("This is the database name",DB_NAME)
#         conn = sqlite3.connect(DB_NAME)
#         c = conn.cursor()
#         # c.execute('''SELECT * ''')
#         print("check before this hero")
#         c.execute('''INSERT INTO details (
#                     first_name, middle_name, last_name, phone_number,
#                     email_address, sex, age, date_of_birth, address,
#                     state, risk_class, face_amount, death_benefit_option, premium_mode,
#                      section, ltc_amount, maximum_monthly_benefit,
#                     rate, term, premium_schedule, benefit_durations,
#                     inflation_benefit_option
#                 ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
#                   (first_name, middle_name, last_name, phone_number,
#                    email_address, sex, age, date_of_birth, address,
#                    state, risk_class, face_amount, death_benefit_option, premium_mode,
#                    section, ltc_amount, maximum_monthly_benefit,
#                    rate, term, premium_schedule, benefit_durations, inflation_benefit_option))
#         conn.commit()
#         conn.close()
#
#         return redirect(url_for('export'))
#
#     return render_template('index.html')


@app.route('/export')
def export():
    # Retrieve all details from the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM details')
    rows = c.fetchall()
    conn.close()

    # Create a new Excel workbook
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Write header row
    header = ['ID', 'First Name', 'Middle Name', 'Last Name', 'Phone Number',
              'Email Address', 'Sex', 'Age', 'Date of Birth', 'Address',
              'State', 'Risk Class', 'Face amount', 'Death Benefit Option', 'Premium Mode', 'Section', 'LTC Amount',
              'Maximum Monthly Benefit',
              'Rate', 'Term', 'Premium Schedule', 'Benefit Durations', 'Inflation Benefit Option']
    sheet.append(header)

    # Write data rows
    for row in rows:
        sheet.append(row)

    # Save the workbook
    excel_file = 'details.xlsx'
    workbook.save(excel_file)

    return redirect(url_for('index'))


@app.route('/download', methods=['GET'])
def download():
    id = session['latest_id']
    # Retrieve all details from the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM details WHERE ID = ?',(id,))
    rows = c.fetchall()
    conn.close()

    # Create a new Excel workbook
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Write header row
    header = ['ID', 'First Name', 'Middle Name', 'Last Name', 'Phone Number',
              'Email Address', 'Sex', 'Age', 'Date of Birth', 'Address',
              'State', 'Risk Class', 'Face amount', 'Death Benefit Option', 'Premium Mode', 'Section', 'LTC Amount',
              'Maximum Monthly Benefit',
              'Rate', 'Term', 'Premium Schedule', 'Benefit Durations', 'Inflation Benefit Option']
    sheet.append(header)

    # Write data rows
    for row in rows:
        sheet.append(row)

    # Save the workbook
    excel_file = 'details.xlsx'
    workbook.save(excel_file)

    # Send the file as a response for download
    return send_file(excel_file, as_attachment=True)


@app.route('/schedule', methods=["GET", "POST"])
def schedule():
    if request.method == 'GET':
        return render_template('scheduler.html')
    if request.method == 'POST':
        data = request.json
        print(data)
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''INSERT INTO details (consultant,
        location,
        time) 
        VALUES (?,?,?)''', (data['professional'], data['location'], data['time']))
        send_emails(data)

        return jsonify({'result': data})


@app.route('/get_details', methods=["GET", "POST"])
def get_details():
    if request.method == 'POST':
        data = request.json
        id = data['id']
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        c.execute("SELECT * FROM table WHERE id=?", (id,))
        result = c.fetchone()

        conn.close()

        if result:
            return jsonify({
                'result': result
            })
        else:
            return jsonify({
                'error': 'No matching ID'
            })


@app.route('/get_data_by_id')
def get_data_by_id():
    # Get the 'id' parameter from the query string
    if request.method=="GET":
        item_id = request.args.get('id')
        print("inside get")
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        c.execute("SELECT * FROM details WHERE id=?", (item_id,))
        result = c.fetchone()
        c.execute("PRAGMA table_info(details)")

        # Fetch the results
        columns = c.fetchall()

        # Extract and print the column names
        column_names = [column[1] for column in columns]
        print("result",result)
        print("col",columns)

        result_dict = {}

        # Iterate through the keys and values
        for key, value in zip(columns, result):
            # Assign the value to the key in the dictionary
            result_dict[key] = value
        print(result_dict)
        conn.close()


######################################################################################

        # # Connect to the SQLite database
        # conn = sqlite3.connect(DB_NAME)
        #
        # # Create a cursor object
        # cursor = conn.cursor()
        #
        # # Specify the table for which you want to get the column names
        # table_name = 'details'
        #
        # # Execute a query to get column information
        # cursor.execute(f"PRAGMA table_info({table_name})")
        #
        # # Fetch the results
        # columns = cursor.fetchall()
        #
        # # Extract and print the column names
        # column_names = [column[1] for column in columns]
        # print("Column Names:", column_names)
        # print(len(column_names))
        #
        # # Close the cursor and connection
        # cursor.close()
        # conn.close()

######################################################################################


        # conn.close()

        return render_template("details.html",data = result_dict)
    else:
        print("inside post")
        item_id = request.args.get('id')

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        c.execute("SELECT * FROM details WHERE id=?", (item_id,))
        result = c.fetchone()

        # c.execute('''INSERT INTO details (
        #                     first_name, middle_name, last_name, phone_number,
        #                     email_address, sex, age, date_of_birth, address,
        #                     state, risk_class, face_amount, death_benefit_option, premium_mode,
        #                      section, ltc_amount, maximum_monthly_benefit,
        #                     rate, term, premium_schedule, benefit_durations,
        #                     inflation_benefit_option
        #                 ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        #           (first_name, middle_name, last_name, phone_number,
        #            email_address, sex, age, date_of_birth, address,
        #            state, risk_class, face_amount, death_benefit_option, premium_mode,
        #            section, ltc_amount, maximum_monthly_benefit,
        #            rate, term, premium_schedule, benefit_durations, inflation_benefit_option))

        conn.close()
        print(result)
        if result:
            return jsonify({
                'result': result
            })
        else:
            return jsonify({
                'error': 'No matching ID'
            })

    # Find the data corresponding to the given ID
    # item = next((item for item in data if str(item['id']) == item_id), None)
    #
    # if item:
    #     return {'result': item}
    # else:
    #     return {'error': 'Item not found'}, 404


import os


@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'GET':
        return render_template('chatbot.html')
    else:
        try:
            data = request.json
            print("inside data")
            print(data)
            # # DB_NAME = 'details.db'
            # #
            # # conn = sqlite3.connect(DB_NAME)
            #
            # # Establish connection to the database
            # conn = sqlite3.connect('details.db')
            # c = conn.cursor()
            # print(conn)
            #
            # # Insert data into the details table
            # c.execute('''INSERT INTO details (
            # 		first_name, last_name, age,phone_number
            # 		, sex,email_address, date_of_birth, address,
            # 		state, risk_class, face_amount, death_benefit_option, premium_mode,
            # 		 premium_schedule
            # 	) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)''',
            #           (data['q0'], data['q1'], data['q2'], data['q3'],
            #            data['q4'], data['q5'], data['q6'], data['q7'],
            #            data['q8'], data['q9'], data['q10'],
            #            data['q11'], data['q12'], data['q13']))
            # conn.commit()
            # print("-------------------------------> ")
            # conn.close()
            # print("entered into database")
            return jsonify({'message': 'Data written to SQLite database'})
        except Exception as e:
            print()
            # Handle the exception, e.g., log the error or return an error response
            return jsonify({'error': str(e)})


if __name__ == '__main__':
    create_tables()
    app.run(debug=False, port=8001)
