from slackclient import SlackClient


def send_slack_message(slack_token, channel, message):
    sc = SlackClient(slack_token)
    sc.api_call(
        "chat.postMessage",
        channel=channel,
        text=message
    )
