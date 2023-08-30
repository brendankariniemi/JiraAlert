from datetime import datetime
import requests
from twilio.rest import Client
import configparser
import logging

HTTP_OK = 200

logging.basicConfig(filename='/var/log/JiraAlert.log', level=logging.INFO)


def send_sms(message):
    client = Client(twilio_account_sid, twilio_auth_token)

    twilio_message = client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=recipient_phone_number
    )

    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    logging.info(f"{timestamp} - Message sent. SID: {twilio_message.sid}")


def main():
    headers = {
        "Authorization": f"Bearer {jira_auth_token}"
    }

    try:
        response = requests.get(
            url=jira_url,
            params={"jql": jql_query},
            headers=headers
        )

        if response.status_code == HTTP_OK:
            issues = response.json().get("issues", [])

            if issues:
                message = "\n\n".join(issue["fields"]["summary"] for issue in issues)
                message = "\nNew Issues: \n\n" + message
                send_sms(message)
            else:
                logging.info(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - No issues found.")
        else:
            logging.error(
                f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Error: {response.status_code}, {response.text}")

    except Exception as e:
        logging.error(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - An error occurred: {str(e)}")


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')  # Load configuration from the file

    # Read Twilio info
    twilio_account_sid = config['Twilio']['account_sid']
    twilio_auth_token = config['Twilio']['auth_token']
    twilio_phone_number = config['Twilio']['twilio_phone_number']
    recipient_phone_number = config['Twilio']['recipient_phone_number']

    # Read Jira info
    jira_url = config['Jira']['url']
    jira_auth_token = config['Jira']['auth_token']
    jql_query = config['Jira']['jql_query']

    main()
