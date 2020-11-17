#!/usr/bin/env python3.6
import sys, os, json, time, traceback
import tornado.ioloop
import tornado.web
from tornado import gen, websocket
from tornado.concurrent import Future
import asyncio

import topic_source

class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        file_data = ""
        with open("./html/index.html", 'r') as fp:
            file_data = fp.read()
        self.write(file_data)

class WSScript(tornado.web.RequestHandler):
    async def get(self):
        file_data = ""
        with open("./html/ws_script.js", 'r') as fp:
            file_data = fp.read()
        self.write(file_data)

class EchoWebSocket(websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")

class FavIcon(tornado.web.RequestHandler):
    def get(self):
        file_data = ""
        with open("./favicon.ico", 'r') as fp:
            file_data = fp.read()
        self.write(file_data)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/ws", EchoWebSocket),
        (r"/wsscript", WSScript),
        # (r"/favicon.ico", FavIcon),
    ])

def main():
    PORT = 8888
    app = make_app()
    app.listen(PORT)
    main_loop = tornado.ioloop.IOLoop().current()
    print("Starting server on port {}".format(PORT))
    # tornado.ioloop.IOLoop.add_callback(cb)
    # tornado.ioloop.PeriodicCallback(lambda: cb(), 4999).start()
    # tornado.ioloop.IOLoop.current().run_sync(topic_source.generateEvent)
    tornado.ioloop.IOLoop.current().run_sync(topic_source.redisReceive)
    
    # tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()