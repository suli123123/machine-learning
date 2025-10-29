"""
作业③: 中国大学排名爬虫
功能: 爬取上海排名2021年中国大学主榜数据并存储到数据库
数据源: https://www.shanghairanking.cn/rankings/bcur/2021
"""

import requests
import json
import sqlite3
from datetime import datetime


class UniversityRankingScraper:
    def __init__(self, db_path='university_data.db'):
        """初始化大学排名爬虫"""
        self.db_path = db_path
        # 上海排名API（通过F12调试发现的数据接口）
        self.api_url = 'https://www.shanghairanking.cn/api/pub/v1/bcur/2021'
        self.init_database()
    
    def init_database(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS university_ranking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rank_number TEXT,
                university_name TEXT NOT NULL,
                province TEXT,
                university_type TEXT,
                total_score REAL,
                ranking_year INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(university_name, ranking_year)
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"数据库初始化完成: {self.db_path}")
    
    def fetch_ranking_data(self):
        """
        从上海排名网站获取大学排名数据
        通过F12调试发现的API接口
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://www.shanghairanking.cn/rankings/bcur/2021',
                'Accept': 'application/json, text/plain, */*'
            }
            
            response = requests.get(self.api_url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"请求失败，状态码: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"获取排名数据时出错: {str(e)}")
            return None
    
    def parse_ranking_data(self, data):
        """
        解析排名数据
        
        数据结构分析（通过F12调试获得）:
        - univNameCn: 大学中文名称
        - ranking: 排名
        - province: 省份
        - univCategory: 院校类型
        - score: 总分
        """
        university_list = []
        
        try:
            if data and 'data' in data:
                universities = data['data']
                
                for univ in universities:
                    university_info = {
                        'rank_number': str(univ.get('ranking', '')),
                        'university_name': univ.get('univNameCn', ''),
                        'province': univ.get('province', ''),
                        'university_type': univ.get('univCategory', ''),
                        'total_score': float(univ.get('score', 0)) if univ.get('score') else 0,
                        'ranking_year': 2021
                    }
                    
                    university_list.append(university_info)
                
                print(f"成功解析 {len(university_list)} 所大学的排名数据")
                
        except Exception as e:
            print(f"解析排名数据时出错: {str(e)}")
        
        return university_list
    
    def save_to_database(self, university_list):
        """将大学排名数据保存到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        saved_count = 0
        for univ in university_list:
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO university_ranking 
                    (rank_number, university_name, province, university_type, 
                     total_score, ranking_year)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    univ['rank_number'],
                    univ['university_name'],
                    univ['province'],
                    univ['university_type'],
                    univ['total_score'],
                    univ['ranking_year']
                ))
                saved_count += 1
            except Exception as e:
                print(f"保存大学 {univ.get('university_name', 'unknown')} 数据时出错: {str(e)}")
        
        conn.commit()
        conn.close()
        print(f"成功保存 {saved_count} 所大学的数据到数据库")
    
    def scrape_rankings(self):
        """爬取大学排名数据"""
        print("正在获取大学排名数据...")
        data = self.fetch_ranking_data()
        
        if data:
            universities = self.parse_ranking_data(data)
            if universities:
                self.save_to_database(universities)
                return universities
            else:
                print("未能解析到有效数据")
                return []
        else:
            print("获取数据失败")
            return []
    
    def query_rankings(self, limit=None, province=None):
        """查询数据库中的排名数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if province:
            if limit:
                cursor.execute('''
                    SELECT rank_number, university_name, province, university_type, total_score
                    FROM university_ranking
                    WHERE province = ?
                    ORDER BY CAST(rank_number AS INTEGER)
                    LIMIT ?
                ''', (province, limit))
            else:
                cursor.execute('''
                    SELECT rank_number, university_name, province, university_type, total_score
                    FROM university_ranking
                    WHERE province = ?
                    ORDER BY CAST(rank_number AS INTEGER)
                ''', (province,))
        else:
            if limit:
                cursor.execute('''
                    SELECT rank_number, university_name, province, university_type, total_score
                    FROM university_ranking
                    ORDER BY CAST(rank_number AS INTEGER)
                    LIMIT ?
                ''', (limit,))
            else:
                cursor.execute('''
                    SELECT rank_number, university_name, province, university_type, total_score
                    FROM university_ranking
                    ORDER BY CAST(rank_number AS INTEGER)
                ''')
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def get_statistics(self):
        """获取统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM university_ranking')
        total_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT province) FROM university_ranking')
        province_count = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT province, COUNT(*) as count
            FROM university_ranking
            GROUP BY province
            ORDER BY count DESC
            LIMIT 10
        ''')
        top_provinces = cursor.fetchall()
        
        conn.close()
        
        return {
            'total': total_count,
            'province_count': province_count,
            'top_provinces': top_provinces
        }


def main():
    """主函数"""
    # 初始化爬虫
    scraper = UniversityRankingScraper()
    
    print("=" * 70)
    print("开始爬取中国大学2021排名数据...")
    print("=" * 70)
    
    # 爬取排名数据
    universities = scraper.scrape_rankings()
    
    print("\n" + "=" * 70)
    print(f"大学排名数据爬取完成！共爬取 {len(universities)} 所大学")
    print("=" * 70)
    
    if universities:
        # 显示统计信息
        stats = scraper.get_statistics()
        print("\n数据统计:")
        print(f"  总大学数: {stats['total']}")
        print(f"  省份数: {stats['province_count']}")
        
        print("\n  大学数量最多的10个省份:")
        for province, count in stats['top_provinces']:
            print(f"    {province}: {count}所")
        
        # 显示前20名大学
        print("\n前20名大学:")
        print("-" * 70)
        top20 = scraper.query_rankings(limit=20)
        for univ in top20:
            rank, name, province, utype, score = univ
            print(f"  {rank:>3}. {name:25} {province:8} {utype:10} {score:.1f}")
        
        # 显示北京的大学
        print("\n北京的大学排名:")
        print("-" * 70)
        beijing_univs = scraper.query_rankings(province='北京', limit=15)
        for univ in beijing_univs:
            rank, name, province, utype, score = univ
            print(f"  {rank:>3}. {name:25} {utype:10} {score:.1f}")


if __name__ == '__main__':
    main()
