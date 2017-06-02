from BaseHTTPServer import BaseHTTPRequestHandler
import json
import bpbot
#route messages to the bot
class MessageRouter(BaseHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers.getheader('content-length'))
        post_body = self.rfile.read(content_len)
        data = json.loads(post_body)

        bpbot.bot.receive_message(data['text'])
