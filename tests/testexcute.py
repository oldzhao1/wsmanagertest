import allure
import pytest

from utils.sendrequest import SendRequest
from utils.yamlutils import YamlUtil


class Test:

    @allure.feature("导购活码")
    @pytest.mark.parametrize("case", YamlUtil().get_testdata("./case/guide.yml"))
    def test_guide_drainage(self, case):
        SendRequest().send_request(case)

    @allure.feature("渠道管理")
    @pytest.mark.parametrize("case", YamlUtil().get_testdata("./case/channels.yml"))
    def test_channel(self, case):
        SendRequest().send_request(case)
