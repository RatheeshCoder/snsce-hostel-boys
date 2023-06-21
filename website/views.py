from flask import Flask, render_template, request
from flask import Blueprint
import smtplib
import time
import threading
import easygui
import requests

views = Blueprint('views', __name__)



# Define the list of recipients
recipients = ['ratheeshraju2003@gmail.com', 'ratheeshraju01@gmail.com', 'ratheeshadis@gmail.com']
current_recipient_index = 0

@views.route('/', methods=['GET', 'POST'])
def send_email():
    if request.method == 'POST':
        try:
            date = request.form['date']
            name = request.form['name']
            college_id = request.form['college_id']
            department = request.form['department']
            year = request.form['year']
            block_name = request.form['block']
            room_no = request.form['room_no']
            problem = request.form['problem']
            media_link = request.form['media']

            # Send the form details to the Google Spreadsheet
            submit_form_to_spreadsheet(request.form)

            body = """
            Hello Hostel Management,

            This is a Complaint request from {name}.

            Department: {department}
            Year: {year}
            College ID: {college_id}
            Block Name: {block_name}
            Room Number: {room_no}


            Problem Description:
            I am experiencing issues with the hostel, including {problem}.

            Please take immediate action to address these concerns. I appreciate your prompt attention to this matter.

            Please take the necessary action.


            Media:  {media_link} 

            Regards,
            Maintenance Team
            """.format(name=name, department=department, year=year, college_id=college_id, block_name=block_name,
            room_no=room_no, date=date, problem=problem, media_link=media_link)

            send_mail_thread = threading.Thread(target=send_mail, args=(body,))
            send_mail_thread.start()

            return render_template('index.html')

        except Exception as e:
            print(f"An error occurred while processing the form data: {str(e)}")
            return render_template('index.html')

    return render_template('index.html')

def send_mail(body):
    global current_recipient_index
    if current_recipient_index >= len(recipients):
        return

    recipient = recipients[current_recipient_index]
    current_recipient_index += 1

    # Create the email message
    subject = "Urgent: Complaint Regarding Hostel Facilities and Services"
    message = f"Subject: {subject}\n\n{body}"

    # Configure the SMTP server
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'ratheeshraju2003@gmail.com'
    sender_password = 'lndzbnurfdzklcdu'

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, message)
            show_notification()
            time.sleep(10)  # Wait for 10 seconds

            # Ask user for feedback
            feedback = ask_feedback()

            if feedback == 'YES':
                print("Problem solved! Terminating the program.")
                return
            elif feedback == 'NO':
                send_mail(body)  # Send the email to the next recipient

    except Exception as e:
        print(f"An error occurred while sending the email: {str(e)}")

def show_notification():
    try:
        easygui.msgbox('An email has been sent to the recipient.', 'Email Sent')
    except Exception as e:
        print(f"An error occurred while showing the notification: {str(e)}")

def ask_feedback():
    choices = ['YES', 'NO']
    try:
        feedback = easygui.buttonbox('Did the recipient solve the problem you have said?', choices=choices)
        return feedback
    except Exception as e:
        print(f"An error occurred while asking for feedback: {str(e)}")
        return 'NO'

def submit_form_to_spreadsheet(form_data):
    try:
        url = "https://script.google.com/macros/s/AKfycbyhgJ_uhIIHyfUo5LMLC7U48xF7B11O77ek1EO3vHT5hwCa4HNQ0QgBzhIirN0QNIxM/exec"
        response = requests.post(url, data=form_data)
        if response.status_code == 200:
            print("Form submitted to the Google Spreadsheet successfully")
        else:
            print("Error occurred while submitting the form to the Google Spreadsheet")
    except Exception as e:
        print(f"An error occurred while submitting the form to the Google Spreadsheet: {str(e)}")

# if __name__ == '__main__':
#     views.run()
