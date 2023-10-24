# pytest官方文档：https://learning-pytest.readthedocs.io/zh/latest/
# allure官方文档：https://docs.qameta.io/allure/

项目持续集成配置：
    Jenkins配置allure：
        下载https://github.com/allure-framework/allure2/releases安装包
        wget https://github.com/allure-framework/allure2/releases/download/2.16.1/allure-2.16.1.tgz
        tar -zxvf allure-2.16.1.tgz -C /usr/local/
        Jenkins下载allure插件，安装
        配置Jenkins全局allure路径，添加名称+allure安装路径（/bin/allure）
        Jenkins节点管理模块，节点中工具配置中配置allure的安装目录