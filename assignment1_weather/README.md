# 作业①：中国气象网天气预报爬虫

## 功能描述
爬取中国气象网（http://www.weather.com.cn）指定城市的7日天气预报，并保存到SQLite数据库中。

## 技术要点
- 使用 `requests` 库发送HTTP请求
- 使用 `BeautifulSoup` 解析HTML页面
- 使用 `sqlite3` 存储数据

## 数据库结构
```sql
CREATE TABLE weather_forecast (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_name TEXT NOT NULL,           -- 城市名称
    city_code TEXT NOT NULL,           -- 城市代码
    date TEXT NOT NULL,                -- 日期
    weather TEXT,                      -- 天气状况
    temperature_high TEXT,             -- 最高温度
    temperature_low TEXT,              -- 最低温度
    wind_direction TEXT,               -- 风向
    wind_level TEXT,                   -- 风力等级
    created_at TIMESTAMP,              -- 创建时间
    UNIQUE(city_code, date)
)
```

## 使用方法

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行爬虫
```bash
cd assignment1_weather
python weather_scraper.py
```

### 3. 查看结果
程序运行后会：
1. 自动创建 `weather_data.db` 数据库
2. 爬取北京、上海、广州、深圳、成都、杭州、武汉、西安共8个城市的天气数据
3. 将数据保存到数据库
4. 在终端输出爬取结果

## 支持的城市
默认支持以下城市（可在代码中修改）：
- 北京 (101010100)
- 上海 (101020100)
- 广州 (101280101)
- 深圳 (101280601)
- 成都 (101270101)
- 杭州 (101210101)
- 武汉 (101200101)
- 西安 (101110101)

## 输出示例
```
==================================================
开始爬取城市天气数据...
==================================================

正在爬取 北京 的天气数据...
成功爬取 北京 的天气数据，共 7 天

正在爬取 上海 的天气数据...
成功爬取 上海 的天气数据，共 7 天

...

北京 - 7日天气预报:
  今天: 晴, 18℃/8℃, 北风 3-4级
  明天: 多云, 20℃/10℃, 南风 <3级
  ...
```

## 注意事项
1. 城市代码可在中国气象网查询获取
2. 爬取时请遵守网站robots.txt规则
3. 建议设置合理的请求间隔，避免对服务器造成压力
4. 数据仅供学习研究使用
