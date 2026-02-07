# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os
import requests

# --- 配置信息 (从环境变量读取) ---
GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD").replace(" ", "")
RECIPIENT_EMAIL = os.environ.get("RECIPIENT_EMAIL")

# Clawdbot Gateway 信息（用于发送 WhatsApp）
CLAWDBOT_GATEWAY_URL = os.environ.get("CLAWDBOT_GATEWAY_URL")
CLAWDBOT_GATEWAY_TOKEN = os.environ.get("CLAWDBOT_GATEWAY_TOKEN")
CLAWDBOT_MESSAGE_TARGET = os.environ.get("CLAWDBOT_MESSAGE_TARGET")

# --- 天气获取 (Web Fetch 模拟) ---
# 在 GitHub Actions 中，我们无法直接调用 Clawdbot 的 web_fetch 工具。
# 因此，我们必须使用一个外部 API 或直接使用 requests 获取雅虎天气数据。
# 鉴于你不需要 API Key，我将编写一个简单的 requests 模拟来获取数据。

def get_weather_report():
    """使用 requests 库模拟获取并分析雅虎天气数据，生成报告。"""
    try:
        # 实际代码会非常复杂，需要进行HTML解析。为简化和演示，
        # 我们使用一个简单的公共 API (如 wttr.in) 或依赖AI分析。
        
        # 简单方案：使用 wttr.in 获取纯文本天气（更适合云端脚本）
        url = "https://wttr.in/Tokyo?format=%C+%t+%w+%m" # 格式：天气 + 温度 + 风速 + 月相
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        raw_data = response.text.strip()
        # 示例输出: Partly cloudy +10°C Wind: 10km/h
        
        # 这里需要AI分析逻辑，但在GitHub Actions中，我们无法直接进行AI分析。
        # 因此，脚本只能格式化纯文本输出。
        
        report_lines = [
            f"📌 **天气：** {raw_data.split(' ')[0]}",
            f"🔥 **气温：** {raw_data.split(' ')[1]}",
            f"💨 **风速：** {raw_data.split(' ')[2]}",
            "👔 **穿衣建议：** 无法在云端脚本中生成智能建议，请参考气温自行判断。",
            "💧 **降水预警：** 请手动查询降水概率。",
        ]
        
        return "\n".join(report_lines)

    except Exception as e:
        return f"【天气获取失败】无法从 wttr.in 获取信息: {e}"

# --- 邮件发送 (与之前相同) ---
def send_email(subject, body):
    """通过 Gmail 发送邮件。"""
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        return "邮件发送失败: 缺少 GMAIL_USER 或 GMAIL_APP_PASSWORD"
        
    try:
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = GMAIL_USER
        msg['To'] = RECIPIENT_EMAIL

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, RECIPIENT_EMAIL, msg.as_string())
        server.close()
        return "邮件发送成功。"
    except Exception as e:
        return f"邮件发送失败: {e}"

# --- WhatsApp 发送 (通过 Gateway) ---
def send_whatsapp(message):
    """通过 Clawdbot Gateway 发送 WhatsApp 消息。"""
    if not CLAWDBOT_GATEWAY_URL or not CLAWDBOT_GATEWAY_TOKEN:
        return "WhatsApp 发送失败: 缺少 Clawdbot Gateway 配置。"
        
    headers = {
        "Authorization": f"Bearer {CLAWDBOT_GATEWAY_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "action": "send",
        "target": CLAWDBOT_MESSAGE_TARGET,
        "message": message
    }
    
    try:
        # 注意: 这里的 URL 需要是 Clawdbot Gateway 的外部访问 URL
        response = requests.post(f"{CLAWDBOT_GATEWAY_URL}/api/message", headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        return f"WhatsApp 发送成功: {response.json().get('result', {}).get('messageId', 'N/A')}"
    except Exception as e:
        return f"WhatsApp 发送失败: {e}"

# --- 主函数 ---
def main():
    weather_report_text = get_weather_report()
    timestamp = datetime.now().strftime("%Y年%m月%d日")

    # 1. 构造邮件和 WhatsApp 内容
    email_subject = f"🦞 小龙虾为您播报：{timestamp} 东京天气预报 (云端)"
    
    # 邮件内容（纯文本）
    email_body = f"老王，这是您定制的每日天气报告 (云端版本)。\n\n{weather_report_text}\n\n[此邮件由 GitHub Actions 自动发送]"
    
    # WhatsApp 内容（美化）
    whatsapp_message = f"🌟 *🦞 小龙虾为您播报：{timestamp} 东京天气预报* 🌟\n\n老王，这是您今天的定制天气报告！\n\n{weather_report_text}"


    # 2. 发送邮件
    email_result = send_email(email_subject, email_body)
    print(f"邮件状态：{email_result}")
    
    # 3. 发送 WhatsApp 消息
    whatsapp_result = send_whatsapp(whatsapp_message)
    print(f"WhatsApp 状态：{whatsapp_result}")

if __name__ == "__main__":
    # 检查所有必需的环境变量是否设置
    required_vars = ["GMAIL_USER", "GMAIL_APP_PASSWORD", "RECIPIENT_EMAIL", "CLAWDBOT_GATEWAY_URL", "CLAWDBOT_GATEWAY_TOKEN", "CLAWDBOT_MESSAGE_TARGET"]
    if all(os.environ.get(var) for var in required_vars):
        main()
    else:
        print("错误：缺少一个或多个必需的环境变量。请在 GitHub Secrets 中配置。")
        for var in required_vars:
            if not os.environ.get(var):
                print(f" - 缺少变量: {var}")