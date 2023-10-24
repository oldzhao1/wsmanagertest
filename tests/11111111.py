from utils.yamlutils import YamlUtil

data = YamlUtil().read_data_yaml("../case/comparear.yml")
print(data)
for v in data.values():
    print(v)
