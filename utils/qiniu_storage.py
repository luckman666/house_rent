
import qiniu.config
import logging

from qiniu import Auth, put_data, etag, urlsafe_base64_encode

access_key = 'pwZa'
secret_key = 'cPKxl'

def storage(file_data):
    try:
        q = Auth(access_key, secret_key)

        bucket_name = 'house'




        token = q.upload_token(bucket_name)

        ret, info = put_data(token, None, file_data)
    except Exception as e:
        logging.error(e)
        raise e
    if 200 == info.status_code:
        return ret["key"]
    else:
        raise Exception("上传失败")


if __name__ == "__main__":
    file_name = input("input file name")
    with open(file_name, "rb") as file:
        file_data = file.read()
        storage(file_data)
