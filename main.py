from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import openpyxl

app = Flask(__name__)

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
                risk_class TEXT
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

        # Save form data to the database
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''INSERT INTO details (
                        first_name, middle_name, last_name, phone_number,
                        email_address, sex, age, date_of_birth, address,
                        state, risk_class
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (first_name, middle_name, last_name, phone_number,
                   email_address, sex, age, date_of_birth, address,
                   state, risk_class))
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
              'State', 'Risk Class']
    sheet.append(header)

    # Write data rows
    for row in rows:
        sheet.append(row)

    # Save the workbook
    excel_file = 'details.xlsx'
    workbook.save(excel_file)

    return redirect(url_for('index'))

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
