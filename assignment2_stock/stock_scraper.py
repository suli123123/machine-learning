"""
作业②: 股票数据爬虫
功能: 使用requests和json解析方法定向爬取股票相关信息并存储到数据库
数据源: 东方财富网
"""

import requests
import json
import sqlite3
from datetime import datetime


class StockScraper:
    def __init__(self, db_path='stock_data.db'):
        """初始化股票爬虫"""
        self.db_path = db_path
        # 东方财富网沪深京A股列表API
        self.api_url = 'http://82.push2.eastmoney.com/api/qt/clist/get'
        self.init_database()
    
    def init_database(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stock_code TEXT NOT NULL UNIQUE,
                stock_name TEXT NOT NULL,
                latest_price REAL,
                price_change REAL,
                price_change_percent REAL,
                volume REAL,
                turnover REAL,
                amplitude REAL,
                highest REAL,
                lowest REAL,
                open_price REAL,
                close_price REAL,
                market_cap REAL,
                pe_ratio REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"数据库初始化完成: {self.db_path}")
    
    def fetch_stock_list(self, page=1, page_size=100):
        """
        从东方财富网获取股票列表数据
        
        参数:
            page: 页码
            page_size: 每页数量
        """
        params = {
            'pn': page,
            'pz': page_size,
            'po': '1',
            'np': '1',
            'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
            'fltt': '2',
            'invt': '2',
            'fid': 'f3',
            'fs': 'm:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23',  # 沪深京A股
            'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25',
            '_': int(datetime.now().timestamp() * 1000)
        }
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'http://quote.eastmoney.com/'
            }
            
            response = requests.get(self.api_url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"请求失败，状态码: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"获取股票数据时出错: {str(e)}")
            return None
    
    def parse_stock_data(self, data):
        """
        解析股票数据
        
        字段说明:
        f12: 股票代码
        f14: 股票名称
        f2: 最新价
        f3: 涨跌幅
        f4: 涨跌额
        f5: 成交量(手)
        f6: 成交额
        f7: 振幅
        f15: 最高
        f16: 最低
        f17: 今开
        f18: 昨收
        f20: 总市值
        f9: 市盈率(动态)
        """
        stock_list = []
        
        try:
            if data and 'data' in data and data['data'] and 'diff' in data['data']:
                stocks = data['data']['diff']
                
                for stock in stocks:
                    stock_info = {
                        'stock_code': stock.get('f12', ''),
                        'stock_name': stock.get('f14', ''),
                        'latest_price': stock.get('f2', 0) if stock.get('f2') != '-' else 0,
                        'price_change': stock.get('f4', 0) if stock.get('f4') != '-' else 0,
                        'price_change_percent': stock.get('f3', 0) if stock.get('f3') != '-' else 0,
                        'volume': stock.get('f5', 0) if stock.get('f5') != '-' else 0,
                        'turnover': stock.get('f6', 0) if stock.get('f6') != '-' else 0,
                        'amplitude': stock.get('f7', 0) if stock.get('f7') != '-' else 0,
                        'highest': stock.get('f15', 0) if stock.get('f15') != '-' else 0,
                        'lowest': stock.get('f16', 0) if stock.get('f16') != '-' else 0,
                        'open_price': stock.get('f17', 0) if stock.get('f17') != '-' else 0,
                        'close_price': stock.get('f18', 0) if stock.get('f18') != '-' else 0,
                        'market_cap': stock.get('f20', 0) if stock.get('f20') != '-' else 0,
                        'pe_ratio': stock.get('f9', 0) if stock.get('f9') != '-' else 0
                    }
                    
                    stock_list.append(stock_info)
                
                print(f"成功解析 {len(stock_list)} 条股票数据")
                
        except Exception as e:
            print(f"解析股票数据时出错: {str(e)}")
        
        return stock_list
    
    def save_to_database(self, stock_list):
        """将股票数据保存到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        saved_count = 0
        for stock in stock_list:
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO stock_info 
                    (stock_code, stock_name, latest_price, price_change, 
                     price_change_percent, volume, turnover, amplitude,
                     highest, lowest, open_price, close_price, market_cap, pe_ratio,
                     updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ''', (
                    stock['stock_code'],
                    stock['stock_name'],
                    stock['latest_price'],
                    stock['price_change'],
                    stock['price_change_percent'],
                    stock['volume'],
                    stock['turnover'],
                    stock['amplitude'],
                    stock['highest'],
                    stock['lowest'],
                    stock['open_price'],
                    stock['close_price'],
                    stock['market_cap'],
                    stock['pe_ratio']
                ))
                saved_count += 1
            except Exception as e:
                print(f"保存股票 {stock.get('stock_code', 'unknown')} 数据时出错: {str(e)}")
        
        conn.commit()
        conn.close()
        print(f"成功保存 {saved_count} 条股票数据到数据库")
    
    def scrape_stocks(self, max_pages=5):
        """爬取股票数据"""
        all_stocks = []
        
        for page in range(1, max_pages + 1):
            print(f"\n正在爬取第 {page} 页数据...")
            data = self.fetch_stock_list(page=page, page_size=100)
            
            if data:
                stocks = self.parse_stock_data(data)
                if stocks:
                    all_stocks.extend(stocks)
                    self.save_to_database(stocks)
                else:
                    print(f"第 {page} 页没有数据")
                    break
            else:
                print(f"第 {page} 页获取失败")
                break
        
        return all_stocks
    
    def query_stocks(self, limit=20, order_by='price_change_percent', ascending=False):
        """查询数据库中的股票数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Whitelist of allowed column names to prevent SQL injection
        allowed_columns = {
            'price_change_percent', 'latest_price', 'volume', 'turnover',
            'market_cap', 'price_change', 'stock_code', 'stock_name'
        }
        
        if order_by not in allowed_columns:
            order_by = 'price_change_percent'
        
        order = 'ASC' if ascending else 'DESC'
        
        cursor.execute(f'''
            SELECT stock_code, stock_name, latest_price, price_change, 
                   price_change_percent, volume, turnover
            FROM stock_info
            ORDER BY {order_by} {order}
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def get_statistics(self):
        """获取数据库统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM stock_info')
        total_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT AVG(price_change_percent) FROM stock_info')
        avg_change = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM stock_info WHERE price_change_percent > 0')
        up_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM stock_info WHERE price_change_percent < 0')
        down_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total': total_count,
            'avg_change': avg_change or 0,
            'up_count': up_count,
            'down_count': down_count
        }


def main():
    """主函数"""
    # 初始化爬虫
    scraper = StockScraper()
    
    print("=" * 60)
    print("开始爬取股票数据...")
    print("=" * 60)
    
    # 爬取股票数据（前5页，约500条）
    stocks = scraper.scrape_stocks(max_pages=5)
    
    print("\n" + "=" * 60)
    print(f"股票数据爬取完成！共爬取 {len(stocks)} 条数据")
    print("=" * 60)
    
    # 显示统计信息
    stats = scraper.get_statistics()
    print("\n数据统计:")
    print(f"  总股票数: {stats['total']}")
    print(f"  平均涨跌幅: {stats['avg_change']:.2f}%")
    print(f"  上涨股票数: {stats['up_count']}")
    print(f"  下跌股票数: {stats['down_count']}")
    
    # 显示涨幅前10的股票
    print("\n涨幅前10的股票:")
    print("-" * 60)
    top_gainers = scraper.query_stocks(limit=10, order_by='price_change_percent', ascending=False)
    for stock in top_gainers:
        print(f"  {stock[0]} {stock[1]}: ¥{stock[2]:.2f} ({stock[4]:+.2f}%)")
    
    # 显示跌幅前10的股票
    print("\n跌幅前10的股票:")
    print("-" * 60)
    top_losers = scraper.query_stocks(limit=10, order_by='price_change_percent', ascending=True)
    for stock in top_losers:
        print(f"  {stock[0]} {stock[1]}: ¥{stock[2]:.2f} ({stock[4]:+.2f}%)")


if __name__ == '__main__':
    main()
