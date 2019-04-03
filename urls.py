
import os
from handlers.BaseHandler import StaticFileBaseHandler as StaticFileHandler
from handlers import Passport, VerifyCode, Profile, House, Orders
from handlers.cmdb_test import Cmdb
urls = [
    (r"/api/register", Passport.RegisterHandler),
    (r"/api/login", Passport.LoginHandler),
    (r"/api/logout", Passport.LogoutHandler),
    (r"/api/piccode", VerifyCode.PicCodeHandler),
    (r"/api/smscode", VerifyCode.SMSCodeHandler),
    (r'^/api/order/comment$', Orders.OrderCommentHandler),
    (r"/(.*)", StaticFileHandler,
     dict(path=os.path.join(os.path.dirname(__file__), "html"), default_filename="index.html"))
]