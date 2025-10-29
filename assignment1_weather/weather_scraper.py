"""
作业①: 中国气象网天气预报爬虫
功能: 爬取指定城市的7日天气预报并保存到数据库
"""

import requests
from bs4 import BeautifulSoup
import sqlite3
import json
from datetime import datetime


class WeatherScraper:
    def __init__(self, db_path='weather_data.db'):
        """初始化天气爬虫"""
        self.db_path = db_path
        self.base_url = 'http://www.weather.com.cn'
        self.init_database()
    
    def init_database(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_forecast (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city_name TEXT NOT NULL,
                city_code TEXT NOT NULL,
                date TEXT NOT NULL,
                weather TEXT,
                temperature_high TEXT,
                temperature_low TEXT,
                wind_direction TEXT,
                wind_level TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(city_code, date)
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"数据库初始化完成: {self.db_path}")
    
    def get_weather_data(self, city_code, city_name):
        """
        获取指定城市的7日天气预报
        
        参数:
            city_code: 城市代码，如 '101010100' (北京)
            city_name: 城市名称
        """
        url = f"{self.base_url}/weather/{city_code}.shtml"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                weather_list = self.parse_weather_data(soup, city_code, city_name)
                
                if weather_list:
                    self.save_to_database(weather_list)
                    print(f"成功爬取 {city_name} 的天气数据，共 {len(weather_list)} 天")
                    return weather_list
                else:
                    print(f"未能解析 {city_name} 的天气数据")
                    return []
            else:
                print(f"请求失败，状态码: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"爬取 {city_name} 天气数据时出错: {str(e)}")
            return []
    
    def parse_weather_data(self, soup, city_code, city_name):
        """解析HTML页面中的天气数据"""
        weather_list = []
        
        try:
            # 查找7日天气预报容器
            weather_7d = soup.find('ul', class_='t clearfix')
            
            if weather_7d:
                days = weather_7d.find_all('li')
                
                for day in days[:7]:  # 只取前7天
                    try:
                        # 日期
                        date_elem = day.find('h1')
                        date = date_elem.text.strip() if date_elem else ''
                        
                        # 天气状况
                        weather_elem = day.find('p', class_='wea')
                        weather = weather_elem.text.strip() if weather_elem else ''
                        
                        # 温度
                        temp_elem = day.find('p', class_='tem')
                        if temp_elem:
                            temp_high = temp_elem.find('span')
                            temp_low = temp_elem.find('i')
                            temperature_high = temp_high.text.strip() if temp_high else ''
                            temperature_low = temp_low.text.strip() if temp_low else ''
                        else:
                            temperature_high = ''
                            temperature_low = ''
                        
                        # 风向和风力
                        wind_elem = day.find('p', class_='win')
                        if wind_elem:
                            wind_em = wind_elem.find('em')
                            wind_direction = wind_em.find('span')['title'] if wind_em and wind_em.find('span') else ''
                            wind_level = wind_elem.find('i').text.strip() if wind_elem.find('i') else ''
                        else:
                            wind_direction = ''
                            wind_level = ''
                        
                        weather_info = {
                            'city_name': city_name,
                            'city_code': city_code,
                            'date': date,
                            'weather': weather,
                            'temperature_high': temperature_high,
                            'temperature_low': temperature_low,
                            'wind_direction': wind_direction,
                            'wind_level': wind_level
                        }
                        
                        weather_list.append(weather_info)
                        
                    except Exception as e:
                        print(f"解析单日天气数据时出错: {str(e)}")
                        continue
                        
        except Exception as e:
            print(f"解析天气数据时出错: {str(e)}")
        
        return weather_list
    
    def save_to_database(self, weather_list):
        """将天气数据保存到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for weather in weather_list:
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO weather_forecast 
                    (city_name, city_code, date, weather, temperature_high, 
                     temperature_low, wind_direction, wind_level)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    weather['city_name'],
                    weather['city_code'],
                    weather['date'],
                    weather['weather'],
                    weather['temperature_high'],
                    weather['temperature_low'],
                    weather['wind_direction'],
                    weather['wind_level']
                ))
            except Exception as e:
                print(f"保存数据时出错: {str(e)}")
        
        conn.commit()
        conn.close()
    
    def query_weather(self, city_name=None):
        """查询数据库中的天气数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if city_name:
            cursor.execute('''
                SELECT city_name, date, weather, temperature_high, 
                       temperature_low, wind_direction, wind_level
                FROM weather_forecast
                WHERE city_name = ?
                ORDER BY id
            ''', (city_name,))
        else:
            cursor.execute('''
                SELECT city_name, date, weather, temperature_high, 
                       temperature_low, wind_direction, wind_level
                FROM weather_forecast
                ORDER BY city_name, id
            ''')
        
        results = cursor.fetchall()
        conn.close()
        
        return results


def main():
    """主函数"""
    # 初始化爬虫
    scraper = WeatherScraper()
    
    # 城市代码字典 (城市名: 城市代码)
    cities = {
        '北京': '101010100',
        '上海': '101020100',
        '广州': '101280101',
        '深圳': '101280601',
        '成都': '101270101',
        '杭州': '101210101',
        '武汉': '101200101',
        '西安': '101110101'
    }
    
    print("=" * 50)
    print("开始爬取城市天气数据...")
    print("=" * 50)
    
    # 爬取各城市天气数据
    for city_name, city_code in cities.items():
        print(f"\n正在爬取 {city_name} 的天气数据...")
        scraper.get_weather_data(city_code, city_name)
    
    print("\n" + "=" * 50)
    print("天气数据爬取完成！")
    print("=" * 50)
    
    # 查询并显示结果
    print("\n数据库中的天气数据:")
    print("-" * 50)
    
    for city_name in cities.keys():
        print(f"\n{city_name} - 7日天气预报:")
        results = scraper.query_weather(city_name)
        for row in results:
            print(f"  {row[1]}: {row[2]}, {row[3]}/{row[4]}, {row[5]} {row[6]}")


if __name__ == '__main__':
    main()
