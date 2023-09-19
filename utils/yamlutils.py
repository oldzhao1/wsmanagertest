import os

import pytest
import yaml

from utils.logger import logger


class YamlUtil:

    # 读取yaml文件
    def read_data_yaml(self, path):
        with open(path, "r", encoding="utf-8") as f:
            value = yaml.load(f, yaml.FullLoader)
            return value

    # 清除yaml文件
    def clear_pydata_yaml(self, path):
        with open(path, "w", encoding='utf-8') as f:
            yaml.dump(f)

    # 读取测试用例数据
    def read_testdata(self, path):
        """

        :param path: 需要执行的yaml文件地址
        :return: 返回yaml文件内的数据
        """
        testdata = {}
        # for root, dirs, files in os.walk(path):
        #     for file in files:
        #         if file.endswith(".yaml"):
        # with open(os.path.join(root, file), "r", encoding="utf-8") as f:
        with open(path, "r", encoding="utf-8") as f:
            contents = yaml.load(f, Loader=yaml.FullLoader)
            if isinstance(contents, list):
                for case in contents:
                    name = case.pop("name")
                    testdata[name] = case
            elif isinstance(contents, dict):
                name = contents.pop("name")
                testdata[name] = contents["cases"]

        logger.info(f"获取到的testdata数据为： {testdata}")
        return testdata

    # 准备测试数据
    def get_testdata(self, path):
        """

        :param path: 需要执行的yaml文件地址
        :return: 格式化后要运行的用例数据
        """
        testdata = YamlUtil().read_testdata(path)
        testcases = []
        for k, v in testdata.items():
            for ca, casedata in v.items():
                if isinstance(casedata, dict):
                    testcases.append(casedata)
                elif isinstance(casedata, list):
                    for data in casedata:
                        print(data)
                        testcases.append(data)
        logger.info(f"最终执行测试的数据为： {testcases}")
        return testcases

    def read_environment_info(self, environment="test"):
        # 获取环境配置
        '''
        :param test,uat,prod对应测试，验收，线上环境,不传参默认test环境
        :returns 返回ip与headers信息
        '''
        domain = ""
        headers = ""
        # 读取环境配置的yaml文件
        env_info = YamlUtil().read_data_yaml("./config/environment.yaml")
        # 判断环境标识
        if environment == "test":
            request_info = env_info["test_environment"]
            domain = request_info["domain"]
            headers = request_info["headers"]
            logger.info(f"test环境的配置获取成功，domain的值为： {domain},headers的值为: {headers}")
            return {"ip": request_info["domain"], "headers": request_info["headers"]}
        elif environment == "uat":
            request_info = env_info["uat_environment"]
            domain = request_info["domain"]
            headers = request_info["headers"]
            logger.info(f"uat环境的配置获取成功，domain的值为： {domain},headers的值为: {headers}")
            return {"ip": request_info["domain"], "headers": request_info["headers"]}
        else:
            request_info = env_info["prod_environment"]
            return {"ip": request_info["domain"], "herders": request_info["headers"]}


if __name__ == '__main__':
    cc = YamlUtil().get_testdata("../case/channels.yml")
    print(cc)
