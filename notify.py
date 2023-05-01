import mysql.connector
from twilio.rest import Client

# Set up Twilio client with your account SID and auth token
account_sid = ""
auth_token = ""
client = Client(account_sid, auth_token)

# Connect to MySQL database
mydb = mysql.connector.connect(
  host="localhost",
  user='root',
  password="#",
  database="login"
)

# Define function to send notifications
def send_notification(sensor):
    if sensor == 'Temperature':
        message = "Your greenhouse temperature is out of range. Take action!"
    elif sensor == 'Humidity':
        message = "Your greenhouse humidity is out of range. Take action!"
    elif sensor == 'Light':
        message = "Your greenhouse light level is too low. Take action!"
    elif sensor == 'CO2':
        message = "Your greenhouse CO2 level is too high. Take action!"
    else:
        message = "Unknown trigger"
    # Set up Twilio message with your Twilio phone number and the recipient's phone number
    twilio_number = "#"  # Replace with your Twilio phone number
    recipient_number = "#"  # Replace with the recipient's phone number
    twilio_message = client.messages.create(
        body=message,
        from_=twilio_number,
        to=recipient_number
    )
    # Print message SID for reference
    print("Twilio message sent with SID:", twilio_message.sid)

# Retrieve latest sensor data from MySQL database
cursor = mydb.cursor()
cursor.execute("SELECT temperature, humidity, light, co2 FROM sensor_status ORDER BY id DESC LIMIT 1")
result = cursor.fetchone()
temperature = result[0]
humidity = result[1]
light = result[2]
co2 = result[3]

# Check if any triggers have been exceeded and send notifications if necessary
if temperature < 27 or temperature > 32:
    send_notification('Temperature')
elif humidity < 60 or humidity > 80:
    send_notification('Humidity')
elif light < 500:
    send_notification('Light')
elif co2 > 1000:
    send_notification('CO2')
