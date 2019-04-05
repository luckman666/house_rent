import logging
import uuid
import json
from config import SESSION_EXPIRES_SECONDS

class Session(object):

    def __init__(self, request_handler_obj):
    # def __init__(self):
        # 先判断用户是否已经有session_id,将请求者的request_handler导入进类中并实例化
        self.__request_handler = request_handler_obj
        # 取get_secure_cookie
        self.session_id = request_handler_obj.get_secure_cookie("session_id")
        # 如果不存在session_id,生成session_id
        if not self.session_id:
            # 设置session_id的值
            self.session_id = uuid.uuid4().hex
            # 将session的data值设置为空字典
            self.data = {}
            # 将其添加到coke中
            request_handler_obj.set_secure_cookie("session_id", self.session_id)

        # 如果存在session_id, 去redis中取出data
        else:
            try:
                json_data = request_handler_obj.redis.get("sess_%s" % self.session_id)
            except Exception as e:
                logging.error(e)
                raise e
            if not json_data:
                self.data = {}
            else:
                # 将从redis数据库中取出的数据进行json序列化，data还在内存中,loads把字符串转换成字典
                self.data = json.loads(json_data)

    def save(self):
        # 将内存中的session的data反序列化json，字典变成字符串
        json_data = json.dumps(self.data)
        # print(json_data)
        try:
            # 将其存储进redis
            self.__request_handler.redis.setex("sess_%s" % self.session_id,SESSION_EXPIRES_SECONDS, json_data)
        except Exception as e:
            logging.error(e)
            raise e
    # 清除session
    def clear(self):
        try:
            # delete,redis中的session
            self.__request_handler.redis.delete("sess_%s" % self.session_id)
        except Exception as e:
            logging.error(e)
        #     清除session_id
        self.__request_handler.clear_cookie("session_id")

# if __name__=="__main__":
#     class cmdb_test(object):
#         get_secure_cookie=""
#
#     t = cmdb_test()
#     session = Session(t)
#     session.save()






