import allure
from jsonpath import jsonpath

from utils.logger import logger
from utils.patamterset import ParamterSetting
from utils.requestutils import RequestUtils


class SendRequest:
    def send_request(self, case):
        """

        :param case: 通过@pytest.mark.parametrize获取到的用例数据
        :return:
        """
        case_name = case["case_name"]
        url = case["path"]
        data = case["data"]
        method = case["method"]
        expected = case["expected"]
        extract_key = case["extract_key"]
        with allure.step(f"执行测试用例 {case_name}"):
            # 设置测试用例标题和描述信息
            allure.dynamic.title(case_name)
            allure.dynamic.description(f"请求 URL: {url}\n请求方法: {method}\n预期结果: {expected}")
        if method.lower() == "get":
            logger.info(f"------开始运行{case_name}测试用例------")
            res = RequestUtils().get(url=url, param=data)
        elif method.lower() == "post":
            logger.info(f"------开始运行{case_name}测试用例------")
            if ParamterSetting().data_is_replace(data):
                data = ParamterSetting().parameter_setting(data)
                logger.info(f"替换后的入参data为： {data}")
            data = data
            res = RequestUtils().post(url=url, json=data)
            logger.info(f"需要提取的参数值为： {extract_key}")
            if extract_key:
                extract_value = ParamterSetting().extract_value(res, extract_key)
                ParamterSetting().parameter_setting(extract_value, "save")
                logger.info(f"提取后的参数值为： {extract_value}")
        else:
            logger.info(f"请查看请求方式是否正确，请求方式为： {method}")
        # 使用jsonpath对每个接口的响应结果与与其结果断言
        SendRequest().assert_jsonpath(res, expected)
        logger.info(f"接口请求方式为： {method}，测试执行数据为： {case},请求的入参data为： {data},预期结果为： {expected}")
        logger.info(f"------运行结束{case_name}测试用例------")

    def assert_jsonpath(self, actual, expected):
        '''

        :param actual: 接口的响应response
        :param expected: yaml文件中需要通过jsonpath获取的字段值
        :return: 返回在response中提取实际字段值
        '''
        for k, v in expected.items():
            actual_value = jsonpath(actual, v)
            assert actual_value, f"Error: {v} is not found in response content."  # 判断是否找到目标值
            assert str(actual_value[0]) == str(k), f"Error: {v} is not equal to {k} in response content."  # 判断是否相等
            logger.info(f"断言的实际结果为： {actual_value[0]},期望结果为： {k}")
        return actual_value
