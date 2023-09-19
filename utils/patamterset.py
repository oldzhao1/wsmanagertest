from jsonpath import jsonpath

from utils.logger import logger


class ParamterSetting:
    access_value = {}

    def data_is_replace(self, data):
        '''
        :param data: case里面的请求参数data、接口关联需提取的extract_key
        :return: 返回是否需要被替换
        '''

        # 兼容data为空
        if data is None:
            return False
        # 迭代case里面的data
        for key, value in data.items():
            try:
                if "$" in value:
                    return True
                elif isinstance(value, list):
                    for v in value:
                        if "$" in v:
                            return True
            except TypeError:
                continue
        return False

    def parameter_setting(self, data: dict, type="get"):
        '''

        :param data:接口关联数据/或response存储字典里面
        :param type: sava： 把数据存储至参数池，get： 读取参数池数据并返回新数据
        :return:
        '''
        if type == "save":
            for key, value in data.items():
                # 把data里面的键值添加到access_value
                ParamterSetting().access_value[key] = value
                logger.info(f"参数提取完成后的参数池：{ParamterSetting.access_value}")
        if type == "get":
            for key, value in data.items():
                if "$" in value:
                    if not jsonpath(ParamterSetting().access_value, value):
                        logger.error(f"依赖参数存在问题，依赖的表达式{value},参数池{ParamterSetting.access_value}")
                        return {"错误信息": "未读取到参数"}
                    logger.info(f"读取前的参数池：{ParamterSetting.access_value}")
                    value = jsonpath(ParamterSetting().access_value, value)[0]
                    data[key] = value
                    print(f"参数化后的值为：{key} : {value}")
                if isinstance(value, list):
                    for v in value:
                        if "$" in v:
                            if not jsonpath(ParamterSetting().access_value, v):
                                logger.error(f"依赖参数存在问题，依赖的表达式{v},参数池{ParamterSetting.access_value}")
                                return {"错误信息": "未读取到参数"}
                            logger.info(f"读取前的参数池：{ParamterSetting.access_value}")
                            v = jsonpath(ParamterSetting().access_value, v)[0]
                            data[key] = [v]
                            print(f"参数化后的值为：{data}")
            return data

    def extract_value(self, reponse: dict, extract_key: dict):
        '''

        :param reponse: 从接口response中获取替换的值
        :param extract_key: 依赖的参数字典
        :return: 最终提取的值
        '''
        extract_value = {}
        for key, value in extract_key.items():
            try:
                extract_value[key] = jsonpath(reponse, value)[0]
            except TypeError:
                continue
        logger.info(f"通过json表达式获取的最终的值为：{extract_value}")
        return extract_value


if __name__ == "__main__":
    print(ParamterSetting().extract_value(reponse={"a": "sss", "b": 123, "c": {"d": 55, "f": 99}},
                                          extract_key={"b": "$.b", "d": "$.c.d"}))
    print(f"最终的参数池：{ParamterSetting.access_value}")
