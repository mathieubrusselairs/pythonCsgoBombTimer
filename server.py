from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import time
import json
import threading

class MyServer(HTTPServer):
    def __init__(self, server_address, token, RequestHandler):
        self.auth_token = token

        super(MyServer, self).__init__(server_address, RequestHandler)

        # You can store states over multiple requests in the server 
        self.round_phase = None
        self.bomb_status = None


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode('utf-8')

        self.parse_payload(json.loads(body))

        self.send_header('Content-type', 'text/html')
        self.send_response(200)
        # self.dev_outputstatus(json.loads(body))
        self.end_headers()


    def is_payload_authentic(self, payload):
        if 'auth' in payload and 'token' in payload['auth']:
            return payload['auth']['token'] == self.server.auth_token
        else:
            return False

    # def dev_outputstatus(self, payload):
        # print(payload)
        # with open('out.json', 'w') as f:
        #     json.dump(payload, f)

    def parse_payload(self, payload):
		# Ignore unauthenticated payloads
        if not self.is_payload_authentic(payload):
            return None

        round_phase = self.get_round_phase(payload)

        if round_phase != self.server.round_phase:
            self.server.round_phase = round_phase
            print('New round phase: %s' % round_phase)

        bomb_status = self.get_bomb_status(payload)

        if bomb_status != self.server.bomb_status:
            self.server.bomb_status = bomb_status
            print('New bomb_status: %s' % bomb_status)

    def get_round_phase(self, payload):
        if 'round' in payload and 'phase' in payload['round']:
            return payload['round']['phase']
        else:
            return None

    def get_bomb_status(self, payload):
        if 'round' in payload and 'bomb' in payload['round']:
            return payload['round']['bomb']
        else:
            return None


    def log_message(self, format, *args):
        """
        Prevents requests from printing into the console
        """
        return




