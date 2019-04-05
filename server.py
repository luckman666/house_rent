import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
import os
import pymysql
import config
import redis

from handlers import Passport
from urls import urls
from tornado.options import options, define
from tornado.web import RequestHandler

define ("port", type=int, default = 8002, help="qidong duan kou")

class Application(tornado.web.Application):
    def __init__(self,*args, **kwargs):
        super(Application,self).__init__(*args, **kwargs)
        # config里面是字典，可以用这个**config.mysql_options方式将参数传进去
        conn = pymysql.Connect(**config.mysql_options)
        self.db = conn.cursor(cursor=pymysql.cursors.DictCursor)
        self.redis = redis.StrictRedis(**config.redis_options)

def main():
    options.log_file_prefix = config.log_path
    options.logging = config.log_level
    tornado.options.parse_command_line()
    app = Application(
        urls,
        **config.settings
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__=="__main__":
    main()