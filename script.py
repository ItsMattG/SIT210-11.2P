# Importing libraries.
import RPi.GPIO as GPIO
import time
import datetime
import picamera
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from gpiozero import LED

# Initiating camera.
camera = picamera.PiCamera() 

# Setting up BCM GPIO numbering.
GPIO.setmode(GPIO.BCM) 

# Setting GPIO 4 as input.
GPIO.setup(4, GPIO.IN) 

# Setting LED to GPIO 17.
led = LED(17) 

# Comma space.
comma_space = ', '

# Function for sending image through email.
def Send_Email(image):
    
    # Email details.
    sender_details = 'testtesttesttestrasppi@gmail.com'
    gmail_password = 'TestTestTestPi.1'
    recipient = ['gleesonmatt96@gmail.com']

    # Creating the message.
    message = MIMEMultipart()
    message['Subject'] = 'Motion Detected!'
    message['To'] = comma_space.join(recipient)
    message['From'] = sender_details

    # List of attachments.
    folder = [image]

    # Add the attachments to the message.
    for image in folder:
        try:
            with open(image, 'rb') as f:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(f.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'folder', filename=os.path.basename(image))
            message.attach(msg)
        except:
            print("Unable to open error: ", sys.exc_info()[0])
            raise

    composed = message.as_string()

    # Send the email.
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as r:
            r.ehlo()
            r.starttls()
            r.ehlo()
            r.login(sender_details, gmail_password)
            r.sendmail(sender_details, recipient, composed)
            r.close()
        print("Email sent!")
    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise


# Ensures LED is off before motion is detected.
led.off()

# Loop for detecting motion then sending email
# then waits for motion again.
while True:
    time_stamp = time.time()
    sent_time = datetime.datetime.fromtimestamp(time_stamp).strftime('%d-%m-%Y %H:%M:%S')
    if GPIO.input(4):
        print("Motion Detected at {}".format(sent_time))
        led.on()
        camera.capture('image_{}.jpg'.format(sent_time))
        image = ('image_{}.jpg'.format(sent_time))
        Send_Email(image)
        led.off()
        time.sleep(2) 
