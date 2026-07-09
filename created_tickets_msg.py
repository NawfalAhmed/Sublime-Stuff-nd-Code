# JIRA
import re
from string import Template
import textwrap
import requests
import pyperclip


USERNAME = "--DUMMY--"
JIRA_DOMAIN = "--DUMMY--"
JIRA_ACCESS_TOKEN = "--DUMMY--"
TICKET_PREFIX="DUMMY-"

PR_TITLE = Template(textwrap.dedent("[$TICKET_KEY]($TICKET_LINK): $TICKET_TITLE").strip())

def format_ticket_key(ticket_key: str):
	stripped = ticket_key.strip()
	return stripped if stripped.startswith(TICKET_PREFIX) else TICKET_PREFIX + stripped

def get_ticket_title(ticket_key: str):
	"""Get the title of the ticket"""

	# Create the basic authentication header
	auth = (USERNAME, JIRA_ACCESS_TOKEN)

	response = requests.get(
		f"{JIRA_DOMAIN}/rest/api/latest/issue/{ticket_key}", auth=auth
	)

	if response.status_code == 200:
		# Extract the ticket title from the response JSON
		ticket_data = response.json()
		ticket_title = ticket_data["fields"]["summary"].strip()
		return PR_TITLE.substitute(
			TICKET_KEY=ticket_key, TICKET_TITLE=ticket_title, TICKET_LINK=f"{JIRA_DOMAIN}/browse/{ticket_key}"
		)

	else:
		raise Exception(
			f"Failed to fetch ticket details for {ticket_key}. Status code: {response.status_code}"
		)

ticket_keys = input("Enter ticket numbers separated by comma: ").split(',')
titles = [get_ticket_title(format_ticket_key(ticket_key)) for ticket_key in ticket_keys]

plural = "s" if len(titles) > 1 else ""
message= "\n".join([f"Created Ticket{plural}:", *titles])

print("Copied:")
print(message)
pyperclip.copy(message + "\n\nCC: @")
