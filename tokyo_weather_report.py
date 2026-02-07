# -*- coding: utf-8 -*-
# Clawdbot 编码修复：强制使用 UTF-8
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# --- 配置信息 (请注意保护您的密码) ---
GMAIL_USER = "wangyining0926@gmail.com"
GMAIL_APP_PASSWORD = "faqx ufvl ptlv dfia"
RECIPIENT_EMAIL = "wangyining0926@gmail.com"

def send_email(subject, body):
    """通过 Gmail 发送邮件。"""
    try:
        msg = MIMEText(body, 'plain', 'utf-8') # 确保使用 UTF-8 编码
        msg['Subject'] = subject
        msg['From'] = GMAIL_USER
        msg['To'] = RECIPIENT_EMAIL

        # 使用 SSL 连接到 Gmail 的 SMTP 服务器
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD.replace(" ", "")) # 移除空格
        server.sendmail(GMAIL_USER, RECIPIENT_EMAIL, msg.as_string())
        server.close()
        return "邮件发送成功。"
    except Exception as e:
        return f"邮件发送失败: {e}"

def main(weather_report_text):
    """接受天气报告文本，并发送邮件。"""
    timestamp = datetime.now().strftime("%Y年%m月%d日")
    
    # 构造邮件内容
    email_subject = f"🦞 小龙虾为您播报：{timestamp} 东京天气预报"
    email_body = f"老王，这是您定制的每日天气报告。\n\n{weather_report_text}\n\n[此邮件由 Clawdbot 自动发送]"

    # 发送邮件
    email_result = send_email(email_subject, email_body)
    
    # 打印结果到日志
    print(f"任务状态：{email_result}")

if __name__ == "__main__":
    import sys
    # 从命令行参数读取天气报告
    if len(sys.argv) > 1:
        report = sys.argv[1]
    else:
        report = "【错误】未收到天气报告文本。"
    main(report)
