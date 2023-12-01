from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import openpyxl
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from handlers.scheduler_handler import send_emails
from services import admin_login_service, admin_data_service
from services import chatbot_service
import sqlite3
import requests
from datetime import datetime

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
TABLE_NAME = 'details3'


def create_tables():
    print("lets create")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
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
		            premium_schedule_ltc TEXT,                    
                    benefit_durations TEXT,    
                    inflation_benefit_option TEXT,
                    consultant TEXT,  
                    location TEXT,    
                    time TEXT,
                    enter_date TEXT
                    )''')

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
        'premium_schedule': '',
        'section': '',
        'ltc_amount': '',
        'maximum_monthly_benefit': '',
        'rate': '',
        'term': '',
        'premium_schedule_ltc': '',
        'benefit_durations': '',
        'inflation_benefit_option': '',
        'consultant': '',
        'location': '',
        'date': '',
        'time': '',
        'date_time': '',
        'enter_date':''
    }
    inserted_data = {}

    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        data = request.json
        print("data", data)
        # for key, value in data.items():
        #     if value != '':
        #         form_data[key] = value

        for key1, key2 in zip(form_data, data):
            form_data[key1] = data[key2]

        print("form_data", form_data)

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(f'''
        INSERT INTO {TABLE_NAME} (
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
    c.execute(f'SELECT * FROM {TABLE_NAME} WHERE id = ?', (inserted_id,))
    column_names = [description[0] for description in c.description]
    inserted_record = c.fetchone()
    print(inserted_id)
    if inserted_record:
        inserted_data = dict(zip(column_names, inserted_record))
    conn.close()

    print(inserted_record)
    return jsonify({'result':'well done'})


@app.route('/download', methods=['GET'])
def download():
    id = session['latest_id']
    print(id)
    # Retrieve all details from the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(f'SELECT * FROM {TABLE_NAME} WHERE ID = ?', (id,))
    rows = c.fetchall()
    conn.close()
    print(rows)

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

# @app.route('/download', methods=['GET','POST'])
# def download():
#     if request.method == 'GET':
#         return "well"
#     if request.method == 'POST':
#         id = session['latest_id']
#         print(id)
#         # Retrieve all details from the database
#         conn = sqlite3.connect(DB_NAME)
#         c = conn.cursor()
#         c.execute(f'SELECT * FROM {TABLE_NAME} WHERE ID = ?', (id,))
#         rows = c.fetchall()
#         conn.close()
#         print(rows)
#
#         # Create a new Excel workbook
#         workbook = openpyxl.Workbook()
#         sheet = workbook.active
#
#         # Write header row
#         header = ['ID', 'First Name', 'Middle Name', 'Last Name', 'Phone Number',
#                   'Email Address', 'Sex', 'Age', 'Date of Birth', 'Address',
#                   'State', 'Risk Class', 'Face amount', 'Death Benefit Option', 'Premium Mode', 'Section', 'LTC Amount',
#                   'Maximum Monthly Benefit',
#                   'Rate', 'Term', 'Premium Schedule', 'Benefit Durations', 'Inflation Benefit Option']
#         sheet.append(header)
#
#         # Write data rows
#         for row in rows:
#             sheet.append(row)
#
#         # Save the workbook
#         excel_file = 'details.xlsx'
#         workbook.save(excel_file)
#
#         # Send the file as a response for download
#         return send_file(excel_file, as_attachment=True)


@app.route('/schedule', methods=["GET", "POST"])
def schedule():
    if request.method == 'GET':
        return render_template('scheduler.html')
    if request.method == 'POST':

        data = request.json

        if 'id' in data:
            id = data['id']
        else:
            id = session['latest_id']
        print("schedule data", data)
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        try:
            c.execute((
                          f'''UPDATE {TABLE_NAME} SET consultant="{data['professional']}", location="{data['location']}", time="{data['time']}" WHERE id = {id} ;'''))
            conn.commit()

            send_emails(data)
        except Exception as e:
            print(e)
        data2 = {'result':'posrt'}
        return jsonify(data2)


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
    if request.method == "GET":
        item_id = request.args.get('id')
        print("inside get", item_id)
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        c.execute(f"SELECT * FROM {TABLE_NAME} WHERE id=?", (item_id,))
        result = c.fetchone()
        c.execute(f"PRAGMA table_info({TABLE_NAME})")

        # Fetch the results
        columns = c.fetchall()

        # Extract and print the column names
        column_names = [column[1] for column in columns]
        print("result", result)
        print("col", columns)

        result_dict = {}

        # Iterate through the keys and values
        for key, value in zip(column_names, result):
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

        return render_template("details.html", data=result_dict)
    else:
        print("inside post")
        item_id = request.args.get('id')

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        c.execute(f"SELECT * FROM {TABLE_NAME} WHERE id=?", (item_id,))
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


@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    form_data_section_1 = {
        'first_name': '',
        'last_name': '',
        'age': '',
        'phone_number': '',
        'sex': '',
        'email_address': '',

        'date_of_birth': '',
        'address': '',
        'state': '',
        'risk_class': '',
        'face_amount': '',
        'death_benefit_option': '',
        'premium_mode': '',
        'premium_schedule': '',
        'section': '',
        'ltc_amount': '',
        'maximum_monthly_benefit': '',
        'rate': '',
        'term': '',
        'meeting': '',
        'consultant': 'None',
        'location': 'None',
        'time': 'None'
    }
    form_data_section_2 = {
        'first_name': '',
        'last_name': '',
        'age': '',
        'phone_number': '',
        'sex': '',
        'email_address': '',
        'date_of_birth': '',
        'address': '',
        'state': '',
        'risk_class': '',
        'face_amount': '',
        'death_benefit_option': '',
        'premium_mode': '',
        'premium_schedule': '',
        'section': '',
        'premium_schedule_ltc': '',
        'benefit_durations': '',
        'inflation_benefit_option': '',
        'meeting': '',
        'consultant': 'None',
        'location': 'None',
        'time': 'None'
    }
    form_data_section_3 = {
        'first_name': '',
        'last_name': '',
        'age': '',
        'phone_number': '',
        'sex': '',
        'email_address': '',
        'date_of_birth': '',
        'address': '',
        'state': '',
        'risk_class': '',
        'face_amount': '',
        'death_benefit_option': '',
        'premium_mode': '',
        'premium_schedule': '',
        'section': '',
        'meeting': '',
        'consultant': 'None',
        'location': 'None',
        'time': 'None'
    }

    if request.method == 'GET':
        return render_template('chatbot.html')
    else:
        try:
            data = request.json
            print("inside data")
            print(data)
            ################# DATA changing based on options ####################

            # if data['q4'] == 1:
            #     data['q4'] = 'Male'
            # else:
            #     data['q4'] = 'Female'
            #
            form_data = {}
            data['q4'] = 'Male' if data['q4'] == '1' else 'Female'

            data['q9'] = 'Preferred Plus Non Tobacco' if data['q6'] == '1' else \
                'Preferred Non Tobacco' if data['q6'] == '2' else \
                    ' Standard Plus Non Tobacco' if data['q6'] == '3' else \
                        'Standard Non Tobacco' if data['q6'] == '4' else \
                            'Preferred Tobacco' if data['q6'] == '5' else \
                                'Standard Tobacco'

            data['q11'] = 'Level' if data['q11'] == '1' else \
                'Increasing'
            data['q12'] = 'Monthly' if data['q12'] == '1' else \
                'Annual'
            data['q13'] = 'Maximum' if data['q13'] == '1' else \
                'Target'
            data['q14'] = 'LTC Rider' if data['q14'] == '1' else \
                'Linked Benefit-LTC' if data['q14'] == '2' else \
                'skip'

            conn = sqlite3.connect('details2.db')
            c = conn.cursor()
            if data['q14'] == 'LTC Rider':
                form_data = form_data_section_1
                data['q16'] = "2%" if data['q16'] == '1' else \
                    "3%" if data['q16'] == '2' else \
                        "4%"
                data['q17'] = "Preferred Tobacco" if data['q17'] == '1' else \
                    "Tobacco" if data['q17'] == '2' else \
                        "Preferred Non Tobacco" if data['q17'] == '3' else \
                            "Tobacco"
                data['q18'] = "10-Year" if data['q18'] == '1' else \
                    "15-Year" if data['q18'] == '2' else \
                        "20-year" if data['q18'] == '3' else \
                            "30-Year" if data['q18'] == '4' else \
                                "Permanent"
                if 'q23' in data:
                    form_data['subject'] = data['q23']
                else:
                    form_data['subject'] = ''

                for i, j in zip(form_data, data):
                    form_data[i] = data[j]

                try:
                    c.execute(f'''
                            INSERT INTO {TABLE_NAME} (
                                first_name, last_name, phone_number,
                                email_address, sex, age, date_of_birth, address,
                                state, risk_class, face_amount, death_benefit_option, premium_mode,
                                 premium_schedule,
                                section, ltc_amount, maximum_monthly_benefit,
                                rate, term,consultant,location,time
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,  ?, ?, ?, ?, ?, ?,?,?,?,?)''',
                              (
                                  form_data['first_name'], form_data['last_name'],
                                  form_data['phone_number'],
                                  form_data['email_address'], form_data['sex'], form_data['age'],
                                  form_data['date_of_birth'],
                                  form_data['address'],
                                  form_data['state'], form_data['risk_class'], form_data['face_amount'],
                                  form_data['death_benefit_option'], form_data['premium_mode'],
                                  form_data['premium_schedule'],
                                  form_data['section'], form_data['ltc_amount'], form_data['maximum_monthly_benefit'],
                                  form_data['rate'], form_data['term'],
                                  form_data['consultant'], form_data['location'], form_data['time']
                              )
                              )
                except Exception as e:
                    print(e)
                print("executed")
                try:
                    conn.commit()
                except Exception as e:
                    print(e, "commit error")
                print("-------------------------------> ")
                inserted_id = c.lastrowid
                conn.close()
                if data['q19'] == 'yes':
                    data1 = {'professional': form_data['consultant'],
                             'location': form_data['location'],
                             'time': form_data['time'],
                             'id': inserted_id,
                             'email': form_data['email_address'],
                             'name': form_data['first_name'],
                             'subject': form_data['subject']}
                    target_url = 'http://127.0.0.1:8001/schedule'
                    headers = {'Content-Type': 'application/json'}
                    response = requests.post(target_url, json=data1, headers=headers)
                print("entered into database")
                return jsonify({'message': 'Data written to SQLite database'})
            elif data['q14'] == 'Linked Benefit-LTC':
                form_data = form_data_section_2
                data['q15'] = "Single" if data['q15'] == '1' else \
                    "5-pay" if data['q15'] == '2' else \
                        "10-pay" if data['q15'] == '3' else \
                            "Pay-to-AFS"
                data['q16'] = "2 years" if data['q16'] == '1' else \
                    "3 years" if data['q16'] == '2' else \
                        "4 years" if data['q16'] == '3' else \
                            "5 years" if data['q16'] == '4' else \
                                "6 years" if data['q16'] == '5' else \
                                    "7 years"
                data['q17'] = "None" if data['q17'] == '1' else \
                    "3% Simple" if data['q17'] == '2' else \
                        "3% Compound" if data['q17'] == '3' else \
                            "5% Compound"
                if 'q22' in data:
                    form_data['subject'] =data['q22']
                else:
                    form_data['subject'] = ''

                for i, j in zip(form_data, data):
                    form_data[i] = data[j]

                try:
                    c.execute(f'''
                            INSERT INTO {TABLE_NAME} (
                                first_name, last_name, phone_number,
                                email_address, sex, age, date_of_birth, address,
                                state, risk_class, face_amount, death_benefit_option, premium_mode,
                                 premium_schedule,
                                section, premium_schedule_ltc, benefit_durations,
                                inflation_benefit_option,consultant,location,time
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,  ?, ?, ?, ?, ?, ?,?,?,?,?)''',
                              (
                                  form_data['first_name'], form_data['last_name'],
                                  form_data['phone_number'],
                                  form_data['email_address'], form_data['sex'], form_data['age'],
                                  form_data['date_of_birth'],
                                  form_data['address'],
                                  form_data['state'], form_data['risk_class'], form_data['face_amount'],
                                  form_data['death_benefit_option'], form_data['premium_mode'],
                                  form_data['premium_schedule'],
                                  form_data['section'], form_data['premium_schedule_ltc'],
                                  form_data['benefit_durations'],
                                  form_data['inflation_benefit_option'],
                                  form_data['consultant'], form_data['location'], form_data['time']
                              )
                              )
                except Exception as e:
                    print(e)
                print("executed")
                try:
                    conn.commit()
                except Exception as e:
                    print(e, "commit error")
                print("-------------------------------> ")
                inserted_id = c.lastrowid
                conn.close()
                if data['q18'] == 'yes':
                    data1 = {'professional': form_data['consultant'],
                             'location': form_data['location'],
                             'time': form_data['time'],
                             'id': inserted_id,
                             'email': form_data['email_address'],
                             'name': form_data['first_name'],
                             'subject': form_data['subject']}
                    target_url = 'http://127.0.0.1:8001/schedule'

                    headers = {'Content-Type': 'application/json'}

                    response = requests.post(target_url, json=data1, headers=headers)
                    print(response)
                print("entered into database")

                return jsonify({'message': 'Data written to SQLite database'})
            else:
                print("inside q14 else")
                form_data = form_data_section_3

                for i, j in zip(form_data, data):
                    form_data[i] = data[j]
                print(form_data)
                try:
                    c.execute(f'''
                            INSERT INTO {TABLE_NAME} (
                                first_name, last_name, phone_number,
                                email_address, sex, age, date_of_birth, address,
                                state, risk_class, face_amount, death_benefit_option, premium_mode,
                                 premium_schedule,
                                section,
                                consultant,location,time
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,  ?, ?, ?,?,?,?,?)''',
                              (
                                  form_data['first_name'], form_data['last_name'],
                                  form_data['phone_number'],
                                  form_data['email_address'], form_data['sex'], form_data['age'],
                                  form_data['date_of_birth'],
                                  form_data['address'],
                                  form_data['state'], form_data['risk_class'], form_data['face_amount'],
                                  form_data['death_benefit_option'], form_data['premium_mode'],
                                  form_data['premium_schedule'],
                                  form_data['section'],
                                  form_data['consultant'], form_data['location'], form_data['time']
                              )
                              )
                except Exception as e:
                    print(e)
                print("executed")
                try:
                    conn.commit()
                except Exception as e:
                    print(e, "commit error")
                print("-------------------------------> ")
                inserted_id = c.lastrowid
                conn.close()
                if 'q18' in data:
                    form_data['subject'] =data['q18']
                else:
                    form_data['subject'] = ''
                if data['q15'] == 'yes':
                    data1 = {'professional': form_data['consultant'],
                             'location': form_data['location'],
                             'time': form_data['time'],
                             'id': inserted_id,
                             'email': form_data['email_address'],
                             'name': form_data['first_name'],
                             'subject': form_data['subject']}
                    target_url = 'http://127.0.0.1:8001/schedule'

                    headers = {'Content-Type': 'application/json'}

                    response = requests.post(target_url, json=data1, headers=headers)
                    print(response)
                print("entered into database")
                return jsonify({'message': 'Data written to SQLite database'})
        except Exception as e:
            print()
            # Handle the exception, e.g., log the error or return an error response
            return jsonify({'error': str(e)})


if __name__ == '__main__':
    create_tables()
    app.run(debug=False, port=8001)
