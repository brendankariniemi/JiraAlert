# JiraAlert

JiraAlert is a short Python script that allows you to receive text message notifications for the latest issues created in your Jira projects. 
It utilizes the Jira REST API to fetch issue data and the Twilio API to send SMS messages. 
This is extremely useful for staying updated on project developments when away from computer.

## Usage
1. Clone this repository to your local machine
2. Install the required Python packages: pip install twilio requests
3. Create a jira personal access token.
4. Set up your Twilio account and obtain your Twilio API credentials (Account SID and Auth Token).
5. Create a config.ini file in the project directory with your Twilio/Jira credentials and other configuration settings.
6. Run the script every so often with cron or launchd.

Example config.ini: 

[Twilio]  
account_sid = <your_account_sid>  
auth_token = <your_auth_token>  
twilio_phone_number = <your_twilio_phone_number>  
recipient_phone_number = <recipient_phone_number>  
  
[Jira]  
url = <your_jira_url>  
auth_token = <your_jira_token>  
jql_query = <your_query, Ex: created >= -30m ORDER BY created DESC>
