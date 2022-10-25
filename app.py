#app.py
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('2LS1fqsRyUJDr2x3TnJU7yrouDVTlzbdH0Bz6XeB4e31TbOGTQDlcGzaE9jns5XgBoO/dsW2qYvCZNm3x6HtxZpUt8gEKs/QoCTzvOQgAc4AngEmDZsEj9LtHsyp4e0xi7xto3PZGb0Kv3UEmNJwZAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2982e49821d08320e6f83b22658e3211')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '很抱歉，你說什麼'

    if msg == 'hi':
        r = 'hi'
    elif msg == '你吃飯了嗎':
        r = '還沒'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()