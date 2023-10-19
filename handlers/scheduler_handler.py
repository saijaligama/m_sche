import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(data):
    receiver_email = data['email']
    receiver_email2 = 'jaliprabhu123@gmail.com'
    sender_email = 'saijaligama@hotmail.com'
    # receiver_email = 'saipjaligama@gmail.com'
    subject = data['subject']
    message = 'Your meeting is scheduled for {} with Mahesh at location {}'
    password = 'Jungle@123'
    smtp_server = 'smtp-mail.outlook.com'  # Replace with your SMTP server
    smtp_port = 587  # Replace with the appropriate port
    try:
        # Create the email message
        email_message = MIMEMultipart()
        email_message['From'] = sender_email
        email_message['To'] = receiver_email
        email_message['Subject'] = subject

        email_message.attach(MIMEText(message, 'plain'))

        # Establish a connection to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Log in to your email account
        server.login(sender_email, password)

        # Send the email
        server.sendmail(sender_email, receiver_email, email_message.as_string())

        # Close the SMTP server connection
        server.quit()

        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


    try:
        # Create the email message
        email_message = MIMEMultipart()
        email_message['From'] = sender_email
        email_message['To'] = receiver_email2
        email_message['Subject'] = subject

        email_message.attach(MIMEText(message, 'plain'))

        # Establish a connection to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Log in to your email account
        server.login(sender_email, password)

        # Send the email
        server.sendmail(sender_email, receiver_email2, email_message.as_string())

        # Close the SMTP server connection
        server.quit()

        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage:


# send_email(sender_email, receiver_email, subject, message, password, smtp_server, smtp_port)
