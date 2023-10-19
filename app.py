from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import openpyxl
from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
from handlers.scheduler_handler import send_email

# app = Flask(__name__)
app = Flask(__name__, template_folder='templates')
app.secret_key = 'mysecretkey1234567890'


# Database configuration
DB_NAME = 'details.db'

def create_tables():
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
                premium_schedule TEXT,     
                benefit_durations TEXT,    
                inflation_benefit_option TEXT  
                )''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        email_address = request.form['email_address']
        sex = request.form['sex']
        age = request.form['age']
        date_of_birth = request.form['date_of_birth']
        address = request.form['address']
        state = request.form['state']
        risk_class = request.form['risk_class']
        face_amount = request.form['face_amount']
        death_benefit_option = request.form['death_benefit_option']
        premium_mode = request.form['premium_mode']
        premium_schedule = request.form['premium_schedule']
        section = request.form['section']
        

        if section == 'ltc_rider':
            # Handle fields for LTC Rider section
            ltc_amount = request.form['ltc_amount']
            maximum_monthly_benefit = request.form['maximum_monthly_benefit']
            rate = request.form['rate']
            term = request.form['term']
            benefit_durations = None
            inflation_benefit_option = None  # Set to None for LTC Rider

        elif section == 'linked_benefit_ltc':
            # Handle fields for Linked Benefit LTC section
            premium_schedule = request.form['premium_schedule']
            benefit_durations = request.form['benefit_durations']
            inflation_benefit_option = request.form['inflation_benefit_option']

        else:
            flash('Invalid section selected')
            return redirect(url_for('index'))

       # Save form data to the database

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''INSERT INTO details (
                    first_name, middle_name, last_name, phone_number,
                    email_address, sex, age, date_of_birth, address,
                    state, risk_class, face_amount, death_benefit_option, premium_mode, section, ltc_amount, maximum_monthly_benefit,
                    rate, term, premium_schedule, benefit_durations, inflation_benefit_option
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (first_name, middle_name, last_name, phone_number,
                email_address, sex, age, date_of_birth, address,
                state, risk_class, face_amount, death_benefit_option, premium_mode, section, ltc_amount, maximum_monthly_benefit,
                rate, term, premium_schedule, benefit_durations, inflation_benefit_option))
        conn.commit()
        conn.close()
    
        return redirect(url_for('export'))

    return render_template('index.html')

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
          'State', 'Risk Class', 'Face amount', 'Death Benefit Option', 'Premium Mode', 'Section', 'LTC Amount', 'Maximum Monthly Benefit',
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
          'State', 'Risk Class', 'Face amount', 'Death Benefit Option', 'Premium Mode', 'Section', 'LTC Amount', 'Maximum Monthly Benefit',
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


@app.route('/schedule',methods = ["GET","POST"])
def schedule():
    if request.method == 'GET':
        return render_template('scheduler.html')
    if request.method == 'POST':
        data = request.json
        print(data)
        send_email(data)

        return jsonify({'result': data})

if __name__ == '__main__':
    create_tables()
    app.run(debug=False,port=8001)
