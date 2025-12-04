#!/usr/bin/env python3
import os
import requests
import json
from datetime import datetime

# Your Slack webhook
WEBHOOK = "https://hooks.slack.com/services/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"

def send_slack_alert():
    """Send a test alert to Slack"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    payload = {
        "username": "AIOps Test Bot",
        "icon_emoji": ":robot_face:",
        "channel": "#aiops-alerts",
        "text": f"🔄 Cron Test at {timestamp}",
        "attachments": [
            {
                "color": "#36a64f",
                "title": "✅ AIOps Cron Job Working!",
                "text": "This alert proves your cron job is running successfully.",
                "fields": [
                    {
                        "title": "Time",
                        "value": timestamp,
                        "short": True
                    },
                    {
                        "title": "Status",
                        "value": "Active",
                        "short": True
                    },
                    {
                        "title": "Message",
                        "value": "Your automated AIOps system is running!",
                        "short": False
                    }
                ],
                "footer": "AIOps Demo System",
                "ts": datetime.now().timestamp()
            }
        ]
    }
    
    try:
        print(f"Sending test alert to Slack...")
        response = requests.post(
            WEBHOOK,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 200:
            print(f"✅ Success! Alert sent to Slack at {timestamp}")
            return True
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 AIOps Cron Test Script")
    print("=" * 50)
    success = send_slack_alert()
    if success:
        print("✅ Test completed successfully!")
        print("📤 Check your #aiops-alerts channel in Slack!")
    else:
        print("❌ Test failed. Check errors above.")
