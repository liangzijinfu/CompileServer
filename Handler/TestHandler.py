# -*- coding: UTF-8 -*-
import tornado.web


class TestHandler(tornado.web.RequestHandler):
    def post(self):
        #result = json.dumps({"msg" : "success", "status" : 200})
        self.write("SUCCESS")