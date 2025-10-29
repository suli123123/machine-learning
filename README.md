# Machine Learning - Web Scraping Assignments

本仓库包含三个Web爬虫作业，用于学习数据采集和数据库存储技术。

## 项目结构

```
machine-learning/
├── assignment1_weather/          # 作业①：天气预报爬虫
│   ├── weather_scraper.py       # 天气爬虫主程序
│   └── README.md                # 详细说明文档
├── assignment2_stock/            # 作业②：股票数据爬虫
│   ├── stock_scraper.py         # 股票爬虫主程序
│   └── README.md                # 详细说明文档
├── assignment3_university/       # 作业③：大学排名爬虫
│   ├── university_scraper.py    # 大学排名爬虫主程序
│   └── README.md                # 详细说明文档
└── requirements.txt              # Python依赖包
```

## 作业概览

### 作业①：中国气象网天气预报爬虫
- **目标**: 爬取中国气象网指定城市的7日天气预报
- **数据源**: http://www.weather.com.cn
- **技术**: requests + BeautifulSoup + SQLite
- **详细说明**: [assignment1_weather/README.md](assignment1_weather/README.md)

### 作业②：股票数据爬虫
- **目标**: 爬取股票相关信息并存储到数据库
- **数据源**: 东方财富网 (https://www.eastmoney.com/)
- **技术**: requests + JSON解析 + SQLite
- **详细说明**: [assignment2_stock/README.md](assignment2_stock/README.md)

### 作业③：中国大学排名爬虫
- **目标**: 爬取2021年中国大学主榜所有院校信息
- **数据源**: https://www.shanghairanking.cn/rankings/bcur/2021
- **技术**: requests + JSON解析 + SQLite + F12调试
- **详细说明**: [assignment3_university/README.md](assignment3_university/README.md)

## 快速开始

### 1. 环境准备

确保已安装 Python 3.7 或更高版本。

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行爬虫

#### 运行作业①（天气爬虫）
```bash
cd assignment1_weather
python weather_scraper.py
```

#### 运行作业②（股票爬虫）
```bash
cd assignment2_stock
python stock_scraper.py
```

#### 运行作业③（大学排名爬虫）
```bash
cd assignment3_university
python university_scraper.py
```

## 依赖包

- `requests>=2.25.0` - HTTP请求库
- `beautifulsoup4>=4.9.0` - HTML解析库

## 数据存储

所有爬虫都使用SQLite数据库存储数据：
- 作业①：`assignment1_weather/weather_data.db`
- 作业②：`assignment2_stock/stock_data.db`
- 作业③：`assignment3_university/university_data.db`

## 技术特点

1. **数据采集**
   - HTTP请求：使用requests库
   - 数据解析：支持HTML解析（BeautifulSoup）和JSON解析
   - 错误处理：完善的异常处理机制

2. **数据存储**
   - 使用SQLite轻量级数据库
   - 自动创建数据表
   - 支持数据去重和更新

3. **代码质量**
   - 面向对象设计
   - 清晰的代码结构
   - 详细的注释说明

4. **调试技巧**
   - 浏览器F12开发者工具
   - 网络请求分析
   - API接口逆向

## 注意事项

1. **遵守法律法规**：爬取数据时请遵守网站的robots.txt规则和使用条款
2. **合理请求频率**：建议设置合理的请求间隔，避免对服务器造成压力
3. **数据使用规范**：爬取的数据仅供学习研究使用
4. **网络环境**：某些网站可能需要特定的网络环境才能访问

## 学习收获

通过这三个作业，可以学习到：
- Web爬虫的基本原理和实现方法
- HTML和JSON数据的解析技术
- 数据库的设计和使用
- 浏览器开发者工具的使用
- API接口的分析和逆向
- Python面向对象编程

## 许可证

本项目仅用于学习和研究目的。

## 联系方式

如有问题或建议，欢迎提Issue。
