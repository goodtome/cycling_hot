#!/usr/bin/env python3
"""
自动同步 FastAPI 到 Apifox 的脚本
需要先配置 Apifox 的 API Token 和项目 ID
"""

import requests
import json
import time
import os
from datetime import datetime

class ApifoxSync:
    def __init__(self, apifox_token, project_id, api_url="http://127.0.0.1:8000/openapi.json"):
        self.apifox_token = apifox_token
        self.project_id = project_id
        self.api_url = api_url
        self.headers = {
            "Authorization": f"Bearer {apifox_token}",
            "Content-Type": "application/json"
        }
    
    def get_openapi_spec(self):
        """获取 FastAPI 的 OpenAPI 规范"""
        try:
            print(f"正在获取 OpenAPI 规范: {self.api_url}")
            response = requests.get(self.api_url)
            response.raise_for_status()
            spec = response.json()
            print(f"✅ 成功获取 OpenAPI 规范，包含 {len(spec.get('paths', {}))} 个接口")
            return spec
        except requests.RequestException as e:
            print(f"❌ 获取 OpenAPI 规范失败: {e}")
            return None
    
    def sync_to_apifox(self):
        """同步到 Apifox"""
        openapi_spec = self.get_openapi_spec()
        if not openapi_spec:
            return False
        
        # Apifox 导入 API 的接口
        import_url = f"https://api.apifox.cn/api/v1/projects/{self.project_id}/import-data"
        print(f"正在同步到 Apifox: {import_url}")
        
        payload = {
            "importFormat": "openapi3",
            "data": json.dumps(openapi_spec),
            "options": {
                "mergeType": "smart",  # 智能合并
                "conflictMode": "overwrite"  # 冲突时覆盖
            }
        }
        
        try:
            print("发送同步请求...")
            response = requests.post(import_url, headers=self.headers, json=payload)
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code != 200:
                print(f"响应内容: {response.text}")
            
            response.raise_for_status()
            result = response.json()
            
            if result.get("success"):
                print(f"✅ 同步成功！时间: {datetime.now()}")
                print(f"   导入接口数: {result.get('data', {}).get('importCount', 0)}")
                return True
            else:
                print(f"❌ 同步失败: {result.get('message', '未知错误')}")
                return False
                
        except requests.RequestException as e:
            print(f"❌ 同步请求失败: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"错误响应: {e.response.text}")
            return False

def main():
    # 配置信息 - 直接在这里修改
    APIFOX_TOKEN = "APS-5RpKuoKovVdPTuNTPXu2WYMjMUe4fRv5"  # 你的实际 Token
    PROJECT_ID = "6705360"  # 你的实际项目 ID
    
    # 也可以从环境变量读取（如果设置了的话）
    if os.getenv("APIFOX_TOKEN"):
        APIFOX_TOKEN = os.getenv("APIFOX_TOKEN")
    if os.getenv("APIFOX_PROJECT_ID"):
        PROJECT_ID = os.getenv("APIFOX_PROJECT_ID")
    
    if APIFOX_TOKEN == "your_apifox_token_here":
        print("⚠️  请先配置 Apifox Token 和项目 ID")
        print("   方法1: 设置环境变量 APIFOX_TOKEN 和 APIFOX_PROJECT_ID")
        print("   方法2: 直接修改脚本中的配置")
        return
    
    syncer = ApifoxSync(APIFOX_TOKEN, PROJECT_ID)
    
    print("🔄 开始同步 FastAPI 到 Apifox...")
    print(f"   项目ID: {PROJECT_ID}")
    print(f"   API地址: {syncer.api_url}")
    success = syncer.sync_to_apifox()
    
    if success:
        print("🎉 同步完成！")
    else:
        print("💥 同步失败，请检查配置和网络连接")

if __name__ == "__main__":
    main() 