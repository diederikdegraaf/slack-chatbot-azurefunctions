import os
import re
import logging

from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

from flask import Flask, request

logging.basicConfig(level=logging.INFO)

slack_token = os.environ["SLACK_TOKEN"]
slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]

app = App(token=slack_token,signing_secret=slack_signing_secret,process_before_response=True)

greeting_messages = re.compile(
    r"\bhello\b|"
    r"\bhi\b|"
    r"\bgreetings\b|"
    r"\bhey\b"
    ,re.IGNORECASE)

@app.middleware
def log_request(logger, body, next):
    logger.info(body)
    return next()

@app.event("app_mention")
def event_test(body, say, logger):
    logger.info(body)

    try:
        channel_type = body["event"]["channel_type"]
    except KeyError:
        channel_type = ""

    if "cinq connect" in body["event"]["text"].lower() and channel_type != "im" and body["event"]["user"] == "UGN0UGXJA":
        say_cinq_connect_intro(say)
        say_cinq_connect_info(say)


@app.message("robot")
def add_reaction(body, client, context, logger):
    logger.info(body)
    message_ts = body["event"]["ts"]
    client.reactions_add(
        channel=context.channel_id, 
        timestamp=message_ts, 
        name="robot_face")

@app.message(greeting_messages)
def message_hello(message, say):
    say(
        text=f"Hey there <@{message['user']}>!")

@app.message("cinq connect")
def reply_cinq_connect(body, say):
    if body["event"]["channel_type"] == "im":
        say_cinq_connect_info(say)

@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


def say_cinq_connect_intro(say):
    raw_msg = """
        _Hi <!channel>! My name is didoubot, and I am created by Diederik de Graaf,
        from the CINQ DevOps unit. On 24 November, there will be a workshop
        on how to create me! Or at least, something like me. And we're going
        to use something called 'Azure Functions'.

        Below you will find some info on the CINQ Connect. If you want to see the info again,
        you can send me a direct message and say "cinq connect"._
        """

    raw_msg.strip('\n')
    parsed_msg = re.sub("\s+" , " ", raw_msg)
    say(parsed_msg)

def say_cinq_connect_info(say):
    raw_msg = """
In the upcoming _CINQ Connect_ you will learn about Function-as-a-Service (FaaS). After the presentation there will be a hands-on where we will create a Slack chatbot, using Azure Functions and Python.

CINQ Connect will take place on Thursday 24 November 2022, 19.30 @ CINQ HQ. Try to arrive a bit before, so we can start on time. The workshop will take about 2-3 hours, but feel free to leave early.

Some coding experience is recommended, but there will be plenty of helpful CINQers otherwise! You are of course also welcome to join the CINQ Connect but not do the workshop.

To prepare for the workshop, you will need a few things:

• <https://www.python.org/downloads/|Python 3>
• An Azure account from CINQ ICT. Submit the <https://docs.google.com/forms/d/e/1FAIpQLScTFtZhoLBDiuvbtLsG1H3oPACB9fTkxyuNopXtXgBko6M5xA/viewform|Google Form> to request one.
• <https://code.visualstudio.com/|Visual Studio Code> + extensions (we need this to deploy to Azure Functions, but IntelliJ is also supported)
\t• <https://marketplace.visualstudio.com/items?itemName=ms-python.python|Python>
\t• <https://marketplace.visualstudio.com/items?itemName=ms-vscode.azure-account|Azure Account>
\t• <https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azureresourcegroups|Azure Resources>
\t• <https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions|Azure Functions>
• <https://github.com/Azure/azure-functions-core-tools|Azure Functions Core Tools>
• <https://ngrok.com|Ngrok> (You will need an account)
        """

    say(raw_msg)