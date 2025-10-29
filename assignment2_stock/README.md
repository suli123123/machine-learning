# 作业②：股票数据爬虫

## 功能描述
使用 `requests` 和 `json` 解析方法定向爬取股票相关信息，并存储到数据库中。
数据源：东方财富网（https://www.eastmoney.com/）

## 技术要点
- 使用 `requests` 库发送HTTP请求
- 使用 `json` 模块解析API返回的JSON数据
- 使用 `sqlite3` 存储数据
- 通过浏览器F12调试模式分析API接口

## 数据库结构
```sql
CREATE TABLE stock_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stock_code TEXT NOT NULL UNIQUE,      -- 股票代码
    stock_name TEXT NOT NULL,             -- 股票名称
    latest_price REAL,                    -- 最新价
    price_change REAL,                    -- 涨跌额
    price_change_percent REAL,            -- 涨跌幅(%)
    volume REAL,                          -- 成交量(手)
    turnover REAL,                        -- 成交额
    amplitude REAL,                       -- 振幅
    highest REAL,                         -- 最高价
    lowest REAL,                          -- 最低价
    open_price REAL,                      -- 开盘价
    close_price REAL,                     -- 昨收价
    market_cap REAL,                      -- 总市值
    pe_ratio REAL,                        -- 市盈率
    created_at TIMESTAMP,                 -- 创建时间
    updated_at TIMESTAMP                  -- 更新时间
)
```

## API 接口分析

### 东方财富网股票列表API
通过浏览器F12调试发现的API接口：
```
http://82.push2.eastmoney.com/api/qt/clist/get
```

### 关键参数说明
- `fs`: 市场筛选参数
  - `m:0+t:6,m:0+t:80` - 沪深A股
  - `m:1+t:2,m:1+t:23` - 沪深指数
- `fields`: 返回字段
  - `f12`: 股票代码
  - `f14`: 股票名称
  - `f2`: 最新价
  - `f3`: 涨跌幅
  - `f4`: 涨跌额
  - `f5`: 成交量
  - `f6`: 成交额
  - 等...

## 使用方法

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行爬虫
```bash
cd assignment2_stock
python stock_scraper.py
```

### 3. 查看结果
程序运行后会：
1. 自动创建 `stock_data.db` 数据库
2. 爬取约500条股票数据（5页）
3. 将数据保存到数据库
4. 显示数据统计信息
5. 显示涨跌幅前10的股票

## 输出示例
```
============================================================
开始爬取股票数据...
============================================================

正在爬取第 1 页数据...
成功解析 100 条股票数据
成功保存 100 条股票数据到数据库

...

============================================================
股票数据爬取完成！共爬取 500 条数据
============================================================

数据统计:
  总股票数: 500
  平均涨跌幅: 0.85%
  上涨股票数: 320
  下跌股票数: 180

涨幅前10的股票:
------------------------------------------------------------
  600123 示例股票A: ¥25.30 (+10.00%)
  ...
```

## 技巧说明
1. **F12调试**: 在Chrome浏览器中按F12，切换到Network标签，筛选XHR请求
2. **API分析**: 查找加载股票列表的URL，分析返回的JSON数据结构
3. **参数调整**: 根据需求调整API参数（如f1、f2等字段）获取不同数值
4. **参数优化**: 可以删减不需要的请求参数以简化请求

## 参考资料
- [Python爬虫实战：抓取东方财富网股票数据](https://zhuanlan.zhihu.com/p/50099084)

## 注意事项
1. 爬取时请遵守网站使用条款
2. 建议设置合理的请求间隔
3. 数据仅供学习研究使用，不构成投资建议
4. 股票市场有风险，投资需谨慎
