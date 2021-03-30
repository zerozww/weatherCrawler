import dao
import requests
import demjson
import pandas as pd



# 以下代码来自博客
def get_data(city_name, city_id):
    # 构造2018~2020全年的月份列表
    months = []
    for year in (2018, 2019, 2020):
        for month in range(12):
            months.append("%d%02d" % (year, month + 1))
    # 从2345天气网的历史天气中获取数据
    todo_urls = ["http://tianqi.2345.com/t/wea_history/js/" + month + "/" + str(city_id) + "_" + month + ".js" for month in
                 months]

    datas = []
    for url in todo_urls:
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception()
        # 去除javascript前后的字符串，得到一个js格式的JSON
        data = r.text.lstrip("var weather_str=").rstrip(";")
        datas.append(data)

    # 解析所有月份的数据
    all_datas = []
    for data in datas:
        tqInfos = demjson.decode(data)["tqInfo"]
        all_datas.extend([x for x in tqInfos if len(x) > 0])
    # 将城市名称添加入dataframe中
    data_city = pd.DataFrame(all_datas)
    data_city['city'] = city_name
    return data_city



citys = dao.get_city_id()
all_data = pd.DataFrame()
for indexs in citys.index:
    # 解决中文乱码
    city_name = citys.loc[indexs]['name'].encode('latin-1').decode('gbk')
    city_id = citys.loc[indexs]['id']
    city_data = get_data(city_name,city_id)
    all_data = all_data.append(city_data)

all_data.to_csv('nanyang.csv')



