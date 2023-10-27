import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(sender, receiver, subject, body, password, smtp_server, smtp_port):
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender, password)
        text = message.as_string()
        server.sendmail(sender, receiver, text)
        server.quit()
        return 'Email sent!'
    except Exception as e:
        return f'Error sending email: {str(e)}'

def send_emails(user_details):
    user_email = user_details['email']
    admin_email = 'saipjaligama@gmail.com'

    sender_email = 'saijaligama@hotmail.com'
    sender_password = 'Jungle@123'

    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587

    # date = user_details['date']
    time = user_details['time']
    # day = user_details['day']
    professional = user_details['professional']
    user_name = user_details['name']

    subject = f'Scheduled Zoom Meeting for {user_name}'

    user_body = f'Your Zoom meeting has been scheduled with {professional} on {time}.'
    admin_body = f'A Zoom meeting has been scheduled with {professional} on {time}.'

    result1 = send_email(sender_email, user_email, subject, user_body, sender_password, smtp_server, smtp_port)
    result2 = send_email(sender_email, admin_email, subject, admin_body, sender_password, smtp_server, smtp_port)

    if result1 == 'Email sent!' and result2 == 'Email sent!':
        return 'Email sent!'
    else:
        return 'Error sending email'

# def send_email(sender, receiver, subject, body, password, smtp_server, smtp_port):
#     message = MIMEMultipart()
#     message['From'] = sender
#     message['To'] = receiver
#     message['Subject'] = subject
#     message.attach(MIMEText(body, 'plain'))
#
#     server = smtplib.SMTP(smtp_server, smtp_port)
#     server.starttls()
#     server.login(sender, password)
#     text = message.as_string()
#     server.sendmail(sender, receiver, text)
#     server.quit()
#
#     print('Email sent!')




# Example user details
# user_details = {
#     'name': 'John Doe',
#     'email': 'jaliprabhu123@gmail.com',
#     'date': 'Dec 1, 2022',
#     'time': '10:00 AM',
#     'day': 'Thursday',
#     'professional': 'Jane Smith'
# }

# send_emails(user_details)

# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
#
#
# def send_email(data):
#     receiver_email = data['email']
#     receiver_email2 = 'jaliprabhu123@gmail.com'
#     sender_email = 'saijaligama@hotmail.com'
#     # receiver_email = 'saipjaligama@gmail.com'
#     subject = data['subject']
#     message = 'Your meeting is scheduled for {} with Mahesh at location {}'
#     password = 'Jungle@123'
#     smtp_server = 'smtp-mail.outlook.com'  # Replace with your SMTP server
#     smtp_port = 587  # Replace with the appropriate port
#     try:
#         # Create the email message
#         email_message = MIMEMultipart()
#         email_message['From'] = sender_email
#         email_message['To'] = receiver_email
#         email_message['Subject'] = subject
#
#         email_message.attach(MIMEText(message, 'plain'))
#
#         # Establish a connection to the SMTP server
#         server = smtplib.SMTP(smtp_server, smtp_port)
#         server.starttls()
#
#         # Log in to your email account
#         server.login(sender_email, password)
#
#         # Send the email
#         server.sendmail(sender_email, receiver_email, email_message.as_string())
#
#         # Close the SMTP server connection
#         server.quit()
#
#         print("Email sent successfully!")
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#
#
#     try:
#         # Create the email message
#         email_message = MIMEMultipart()
#         email_message['From'] = sender_email
#         email_message['To'] = receiver_email2
#         email_message['Subject'] = subject
#
#         email_message.attach(MIMEText(message, 'plain'))
#
#         # Establish a connection to the SMTP server
#         server = smtplib.SMTP(smtp_server, smtp_port)
#         server.starttls()
#
#         # Log in to your email account
#         server.login(sender_email, password)
#
#         # Send the email
#         server.sendmail(sender_email, receiver_email2, email_message.as_string())
#
#         # Close the SMTP server connection
#         server.quit()
#
#         print("Email sent successfully!")
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#
# # Example usage:
#
#
# # send_email(sender_email, receiver_email, subject, message, password, smtp_server, smtp_port)
