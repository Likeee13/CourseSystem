from flask import request
import sqlite3
import requests

#API_URL = "http://192.168.43.94:5000/execute"  # 统一API地址

API_URL = "http://10.129.60.119:5000/execute"
#API_URL = "http://localhost:5000/execute" 
def fetch_all(query, params=()):
    """执行查询语句并返回所有结果"""
    try:
        response = requests.post(
            API_URL,
            json={'query': query, 'params': params},
            timeout=100  # 添加超时设置[8](@ref)
        )
        response.raise_for_status()  # 自动处理HTTP错误状态码
        result = response.json()
        
        if result['status'] == 'error':
            raise RuntimeError(f"数据库错误: {result['message']}")
            
        return result['data']
    
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"API连接失败1: {str(e)}") from e

def execute_query(query, params=()):
    """执行非查询语句(INSERT/UPDATE/DELETE)"""
    try:
        response = requests.post(
            API_URL,
            json={'query': query, 'params': params},
            timeout=100
        )
        response.raise_for_status()
        result = response.json()
        
        if result['status'] == 'error':
            raise RuntimeError(f"执行错误: {result['message']}")
            
        return {"affected_rows": len(result['data'])}  # 返回影响行数
    
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"API连接失败2: {str(e)}") from e