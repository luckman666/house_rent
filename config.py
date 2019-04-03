import os
settings = dict(
    static_path = os.path.join(os.path.dirname(__file__),"static"),
    cookie_secret ="BeGGLS1zQ1qMhXYs/vQcZCQ5FD42U0/1mjDh3uJCT08=",
    template_path = os.path.join(os.path.dirname(__file__),"template"),
    xsrf_cookies=False,
    debug=True
)

mysql_options = dict(
     host="192.1",
     database="house",
     user="root",
     password="root"
 )

redis_options = dict(
    host="192.168",
    port=63
)

log_path = os.path.join(os.path.dirname(__file__),"logs/tornado.log")
log_level = "debug"
passwd_hash_key = "anm7OwNqQr+Wb5aeS3Z2tZ6k2AZjn0gvvasaU8qbje0="


