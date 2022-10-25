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

    if '給我貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='1', 
            sticker_id='1'
        )

        line_bot_api.reply_message(
        event.reply_token,
        sticker_message)

        return

    if msg in ['hi', 'Hi']:
        r = '嗨'
    elif msg == '你吃飯了嗎':
        r = '還沒'
    elif msg == '你是誰':
        r = '我是機器人'
    elif '訂位' in msg:
        r = '您想訂位，是嗎?'


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()