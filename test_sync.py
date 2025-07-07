#!/usr/bin/env python3
"""
简化的同步测试脚本
"""

import requests
import json

def test_openapi():
    """测试获取 OpenAPI 文档"""
    try:
        response = requests.get("http://127.0.0.1:8000/openapi.json")
        if response.status_code == 200:
            spec = response.json()
            print(f"✅ OpenAPI 文档获取成功，包含 {len(spec.get('paths', {}))} 个接口")
            return True
        else:
            print(f"❌ OpenAPI 文档获取失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False

def test_apifox_connection():
    """测试 Apifox 连接"""
    token = "APS-5RpKuoKovVdPTuNTPXu2WYMjMUe4fRv5"
    project_id = "6705360"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 测试获取项目信息
    try:
        url = f"https://api.apifox.cn/api/v1/projects/{project_id}"
        response = requests.get(url, headers=headers)
        print(f"Apifox 连接测试状态码: {response.status_code}")
        if response.status_code == 200:
            print("✅ Apifox 连接成功")
            return True
        else:
            print(f"❌ Apifox 连接失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Apifox 连接异常: {e}")
        return False

if __name__ == "__main__":
    print("🧪 开始测试同步功能...")
    
    print("\n1. 测试 FastAPI 服务...")
    if test_openapi():
        print("✅ FastAPI 服务正常")
    else:
        print("❌ FastAPI 服务异常")
    
    print("\n2. 测试 Apifox 连接...")
    if test_apifox_connection():
        print("✅ Apifox 连接正常")
    else:
        print("❌ Apifox 连接异常")
    
    print("\n测试完成！") 