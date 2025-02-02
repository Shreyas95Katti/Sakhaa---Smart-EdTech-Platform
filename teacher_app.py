from flask import Flask, request, redirect, render_template
from twilio.rest import Client
import frame_differentiation
import Virtual_WhiteBoard
import requests
import base64
import json


#Twilio API
ACCOUNT_SID = ''
AUTH_TOKEN = ''
WHATSAPP_FROM = ''
WHATSAPP_TO = ''   #Add your number here

#Zoom API
CLIENT_ID = ''
CLIENT_SECRET = ''
ACCOUNT_ID = ''


def meeting():
	def get_access_token(client_id, client_secret, account_id):
		url = "https://zoom.us/oauth/token"
    
		# Encode client_id:client_secret in Base64
		credentials = f"{client_id}:{client_secret}".encode("utf-8")
		encoded_credentials = base64.b64encode(credentials).decode("utf-8")

		headers = {
			"Authorization": f"Basic {encoded_credentials}",
			"Content-Type": "application/x-www-form-urlencoded"
		}

		payload = {
			"grant_type": "account_credentials",
			"account_id": account_id
		}

		response = requests.post(url, headers=headers, data=payload)

		if response.status_code == 200:
			return response.json().get("access_token")
		else:
			print("Error:", response.text)
			raise Exception("Failed to obtain access token")

	access_token = get_access_token(CLIENT_ID, CLIENT_SECRET, ACCOUNT_ID)

	def create_meeting(access_token):
		meeting_details = {
			"topic": "The title of your zoom meeting",
			"type": 2,
			"start_time": "2025-01-09T10:21:57",
			"duration": 45,
			"timezone": "Asia/Kolkata",
			"agenda": "test",
			"settings": {
				"host_video": True,
				"participant_video": True,
				"join_before_host": False,
				"mute_upon_entry": False,
				"watermark": True,
				"audio": "voip",
				"auto_recording": "cloud"
			}
		}
		headers = {
			"Authorization": f"Bearer {access_token}",
			"Content-Type": "application/json"
		}
		response = requests.post(
			'https://api.zoom.us/v2/users/me/meetings',
			headers=headers,
			data=json.dumps(meeting_details)
		)
		if response.status_code == 201:
			meeting_info = response.json()
			join_url = meeting_info.get("join_url")
			meeting_password = meeting_info.get("password")
			print(f"Meeting created successfully. Join URL: {join_url}, Password: {meeting_password}")
			return join_url
		else:
			raise Exception(f"Failed to create meeting: {response.text}")

	# run the create meeting function
	meetLink = create_meeting(access_token)

	def send_whatsapp_message(account_sid, auth_token, whatsapp_from, whatsapp_to, message_body):
		client = Client(account_sid, auth_token)
		message = client.messages.create(
			body=message_body,
			from_=whatsapp_from,
			to=whatsapp_to
		)
		print(f"Message sent: SID {message.sid}")

	message_body = f"You may join the class now using the given link - {meetLink}"
	send_whatsapp_message(ACCOUNT_SID, AUTH_TOKEN, WHATSAPP_FROM, WHATSAPP_TO, message_body)
	return meetLink

    

app = Flask(__name__)


@app.route('/submit_data', methods=['POST'])
def submit_data():
   
    print("Working")
    # Do something with the data here
    link = meeting()
    return redirect(link)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/button1')
def button1():
    # add functionality for button 1 here
    
    Virtual_WhiteBoard.board()
    return 'Button 1 clicked!'

@app.route('/button2')
def button2():
    # add functionality for button 2 here
    frame_differentiation.motion()
    return 'Button 2 clicked!'




if __name__ == '__main__':
    app.run(debug=True, port = 8080)
