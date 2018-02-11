from slackclient import SlackClient
from logging_utils import logger
from time import sleep


def send_slack_message(slack_token, channel, message):
    """
    Simple wrapper for sending a Slack message.
    """
    sc = SlackClient(slack_token)
    response = sc.api_call(
        "chat.postMessage",
        channel=channel,
        text=message
    )

    # Check to see if the message sent successfully
    if response["ok"]:
        logger(__name__).info(
            "Message posted successfully: " + response["message"]["ts"])

    # If the message failed, check for rate limit headers in the response
    elif response["ok"] is False and response["headers"]["Retry-After"]:
        delay = int(response["headers"]["Retry-After"])
        logger(__name__).warning(
            "Rate limited. Retrying in " + str(delay) + " seconds")
        sleep(delay)
        response = sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=message
        )
