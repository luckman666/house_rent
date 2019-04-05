import os
# application配置参数
settings = dict(
    static_path = os.path.join(os.path.dirname(__file__),"static"),
    cookie_secret ="BeGGLS1zQ1qMhXYs/vQcZCQ5FD42U0/1mjDh3uJCT08=",
    template_path = os.path.join(os.path.dirname(__file__),"template"),
    xsrf_cookies=False,
    debug=True
)

 # 数据库配置参数
mysql_options = dict(
     host="192.1",
     database="i",
     user="root",
     password="root"
 )

 #redis数据库配置
redis_options = dict(
    host="192.168",
    port=6379
)

 # 日志配置参数
log_path = os.path.join(os.path.dirname(__file__),"logs/tornado.log")
log_level = "debug"
 # 密码加密秘钥
passwd_hash_key = "anm7OwNqQr+Wb5aeS3Z2tZ6k2AZjn0gvvasaU8qbje0="

SESSION_EXPIRES_SECONDS=8600  #session过期时间

