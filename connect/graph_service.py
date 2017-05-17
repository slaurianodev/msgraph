# Copyright (c) Microsoft. All rights reserved. Licensed under the MIT license.
# See LICENSE in the project root for license information.

import requests
import uuid
import json
from connect.data import get_email_text

# The base URL for the Microsoft Graph API.
graph_api_endpoint = 'https://graph.microsoft.com/v1.0{0}'

def call_sendMail_endpoint(access_token, alias, emailAddress):
	  # The resource URL for the sendMail action.
    send_mail_url = graph_api_endpoint.format('/me/microsoft.graph.sendMail')

	# Set request headers.
    headers = {
		      'User-Agent' : 'python_tutorial/1.0',
		      'Authorization' : 'Bearer {0}'.format(access_token),
		      'Accept' : 'application/json',
		      'Content-Type' : 'application/json'
    }

	# Use these headers to instrument calls. Makes it easier
	# to correlate requests and responses in case of problems
	# and is a recommended best practice.
    request_id = str(uuid.uuid4())
    instrumentation = {
		      'client-request-id' : request_id,
		      'return-client-request-id' : 'true'
}
    headers.update(instrumentation)

	# Create the email that is to be sent with API.
    email = {
		      'Message': {
                          'Subject': 'Welcome to Office 365 development with Python and the Office 365 Connect sample',
			                       'Body': {
				                                               'ContentType': 'HTML',
				                                               'Content': get_email_text(alias)
                                    },
			                       'ToRecipients': [
				                                               {
					                   'EmailAddress': {
						                 'Address': emailAddress
					}
				}
			]
		},
		      'SaveToSentItems': 'true'
	}

    response = requests.post(url = send_mail_url, headers = headers, data = json.dumps(email), verify=False, params = None)

	# Check if the response is 202 (success) or not (failure).
    if response.status_code == requests.codes.accepted:
        return response.status_code
    else:
        return "{0}: {1}".format(response.status_code, response.text)


def call_create_event_Calendar(access_token, guest_email):
    create_event_url = graph_api_endpoint.format('/me/calendar/events')

    # Set request headers.
    headers = {
		      'User-Agent' : 'python_tutorial/1.0',
		      'Authorization' : 'Bearer {0}'.format(access_token),
		      'Accept' : 'application/json',
		      'Content-Type' : 'application/json'
    }

    event = {
      "subject": "Let's go for lunch",
      "body": {
        "contentType": "HTML",
        "content": "Does late morning work for you?"
      },
      "start": {
        "dateTime": "2017-05-18T12:00:00",
        "timeZone": "Pacific Standard Time"
      },
      "end": {
          "dateTime": "2017-05-18T14:00:00",
          "timeZone": "Pacific Standard Time"
      },
      "location":{
          "displayName":"Harry's Bar"
      },
      "attendees": [
          {
            "emailAddress": {
                "address":guest_email,
                "name": "Sergio Lauriano"
            },
            "type": "required"
      }]
    }

    response = requests.post(url = create_event_url, headers = headers, data = json.dumps(event), verify=False, params = None)

	# Check if the response is 202 (success) or not (failure).
    if response.status_code == 201:
        return response.status_code
    else:
        return "{0}: {1}".format(response.status_code, response.text)


