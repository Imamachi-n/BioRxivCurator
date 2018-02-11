from slackclient import SlackClient


def send_slack_message(slack_token, channel, message):
    sc = SlackClient(
        "xoxp-45537981091-45586754727-313391649221-c77891d9c524e75b7fa0fa8cdf588cb8")
    sc.api_call(
        "chat.postMessage",
        channel="@imamachi",
        text="Hello from Python! :tada:"
    )
