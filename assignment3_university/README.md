# 作业③：中国大学排名爬虫

## 功能描述
爬取上海排名网站的中国大学2021主榜（https://www.shanghairanking.cn/rankings/bcur/2021）所有院校信息，并存储到数据库中。

## 技术要点
- 使用 `requests` 库发送HTTP请求
- 使用 `json` 模块解析API返回的JSON数据
- 使用 `sqlite3` 存储数据
- 通过浏览器F12调试模式分析API接口

## 数据库结构
```sql
CREATE TABLE university_ranking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rank_number TEXT,                  -- 排名
    university_name TEXT NOT NULL,     -- 大学名称
    province TEXT,                     -- 省份
    university_type TEXT,              -- 院校类型
    total_score REAL,                  -- 总分
    ranking_year INTEGER,              -- 排名年份
    created_at TIMESTAMP,              -- 创建时间
    UNIQUE(university_name, ranking_year)
)
```

## F12 调试分析过程

### 步骤1：打开浏览器开发者工具
1. 访问 https://www.shanghairanking.cn/rankings/bcur/2021
2. 按 F12 打开浏览器开发者工具
3. 切换到 "Network"（网络）标签

### 步骤2：分析网络请求
1. 刷新页面，观察Network标签中的请求
2. 筛选 "XHR" 或 "Fetch" 类型的请求
3. 找到包含排名数据的API请求

### 步骤3：定位数据API
通过分析发现真实的数据API：
```
https://www.shanghairanking.cn/api/pub/v1/bcur/2021
```

### 步骤4：分析API返回数据
点击API请求，查看 "Response" 标签，可以看到JSON格式的数据：
```json
{
  "data": [
    {
      "ranking": "1",
      "univNameCn": "清华大学",
      "province": "北京",
      "univCategory": "综合",
      "score": "1000.0"
    },
    ...
  ]
}
```

### 步骤5：分析数据字段
- `ranking`: 排名
- `univNameCn`: 大学中文名称
- `province`: 省份
- `univCategory`: 院校类型
- `score`: 总分

## 使用方法

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行爬虫
```bash
cd assignment3_university
python university_scraper.py
```

### 3. 查看结果
程序运行后会：
1. 自动创建 `university_data.db` 数据库
2. 爬取所有大学的排名数据
3. 将数据保存到数据库
4. 显示统计信息和排名结果

## 输出示例
```
======================================================================
开始爬取中国大学2021排名数据...
======================================================================
正在获取大学排名数据...
成功解析 600 所大学的排名数据
成功保存 600 所大学的数据到数据库

======================================================================
大学排名数据爬取完成！共爬取 600 所大学
======================================================================

数据统计:
  总大学数: 600
  省份数: 31

  大学数量最多的10个省份:
    江苏: 45所
    广东: 38所
    山东: 35所
    ...

前20名大学:
----------------------------------------------------------------------
    1. 清华大学                      北京     综合        1000.0
    2. 北京大学                      北京     综合        950.5
    3. 浙江大学                      浙江     综合        912.3
    ...
```

## F12调试技巧总结
1. **Network标签**: 用于监控所有网络请求
2. **XHR/Fetch筛选**: 快速定位AJAX请求
3. **Preview/Response**: 查看API返回的数据格式
4. **Headers**: 查看请求头信息，有助于模拟请求
5. **Timing**: 分析请求耗时
6. **保存为HAR**: 可以保存整个请求记录用于分析

## API 接口说明

### 请求方法
```
GET https://www.shanghairanking.cn/api/pub/v1/bcur/2021
```

### 请求头
```
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
Referer: https://www.shanghairanking.cn/rankings/bcur/2021
Accept: application/json, text/plain, */*
```

### 返回格式
JSON格式，包含所有大学的排名信息

## 注意事项
1. 请遵守网站的robots.txt规则和使用条款
2. 建议设置合理的请求间隔，避免对服务器造成压力
3. 数据仅供学习研究使用
4. 排名数据会随年份更新，URL中的年份参数需要相应调整
