from flask import Blueprint, render_template, jsonify,request,url_for

admin_login_bp = Blueprint('admin_login_bp',__name__, template_folder='templates')

@admin_login_bp.route('/admin_login',methods = ['GET','POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('admin_login.html')
    else:
        data = request.json
        if data['password'] == "1234":
            redirect_url = url_for('admin_data_bp.admin_data')
            return jsonify({"message": "Password Accepted", "redirect": redirect_url})
        else:
            return jsonify({"message":"Password not correct, PLease enter again"})
