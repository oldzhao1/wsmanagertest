from jsonpath import jsonpath

from utils.logger import logger


class Assert:
    def assert_response(self, assert_list: list, api_response: dict):
        mid_assert_list = []
        for i in assert_list:
            print(i)
            print(type(i))
            if "$" in i:
                print(i)
                # 获取$的索引
                index = i.find("$")
                # 切片出表达式
                json_path = i[index:len(i) - 1]
                # 把表达式转换为值
                value = jsonpath(api_response, json_path)
                if not value:
                    print("表达式提取失败，请检查")
                    return False
                value = value[0]
                # 用值把表达式替换掉
                i = i.replace(json_path, value)
            mid_assert_list.append(i)
        logger.info(f"获取到断言结果值为：{mid_assert_list}")
        print(f"断言列表：{mid_assert_list}")
        for i in mid_assert_list:
            assert_result = eval(i)
            print(assert_result)
            print(f"断言表达式：{i},断言结果{assert_result}")




if __name__ == "__main__":
    Assert().assert_response(assert_list=["'12' in '123'", "'123' == '$.b'", "'55'=='$.c.d'"],
                             api_response={'a': 'sss', 'b': "123", 'c': {'d': "55", 'f': "99"}})
