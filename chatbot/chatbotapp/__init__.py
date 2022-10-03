from flask import Flask
import slack_sdk
from slackeventsapi import SlackEventAdapter
import os

slack_token = os.environ["SLACK_TOKEN"]
slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(slack_signing_secret, '/slack/events', app)
client = slack_sdk.WebClient(token=slack_token)

@app.route("/slack/events")
def slack_events():
    return ('', 200)

@slack_event_adapter.on('message')
def message(payload):
    print(payload)
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    timestamp = event.get('ts')
 
    if text == "hi":
        client.chat_postMessage(channel=channel_id,text="Hello")

    if "robot" in text:
        client.reactions_add(channel=channel_id, name='robot_face', timestamp=timestamp)


if __name__ == "__main__":
    app.run()