import requests

from utils.logger import logger
from utils.yamlutils import YamlUtil
from config.config import Environment


class RequestUtils:
    def get(self, url, param):
        url = YamlUtil().read_environment_info(Environment)["ip"] + url
        headers = YamlUtil().read_environment_info()["headers"]
        response = requests.get(url=url, headers=headers, params=param).json()
        logger.info(f"接口的请求地址为： url = {url}")
        logger.info(f"请求响应结果为： {response}")
        return response

    def post(self, url, json, **kwargs):
        url = YamlUtil().read_environment_info(Environment)["ip"] + url
        headers = YamlUtil().read_environment_info()["headers"]
        response = requests.post(url=url, headers=headers, json=json, **kwargs).json()
        logger.info(f"请求的接口地址为： {url}")
        logger.info(f"请求响应结果为： {response}")
        return response


if __name__ == "__main__":
    RequestUtils().get("/get", param="")
    RequestUtils().post("/post", {"data": "data"})
