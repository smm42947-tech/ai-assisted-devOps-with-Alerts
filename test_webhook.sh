#!/bin/bash

WEBHOOK="https://hooks.slack.com/services/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"

echo "Testing Slack webhook..."
echo "Webhook: $WEBHOOK"

curl -X POST -H 'Content-type: application/json' \
  --data '{
    "text": "🚀 *AIOps System Connected!*",
    "blocks": [
      {
        "type": "header",
        "text": {
          "type": "plain_text",
          "text": "🎯 AIOps Alert System",
          "emoji": true
        }
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "✅ *Connection Test Successful!*\nYour AIOps system is now connected to Slack."
        }
      },
      {
        "type": "context",
        "elements": [
          {
            "type": "mrkdwn",
            "text": "Time: $(date '+%Y-%m-%d %H:%M:%S') | Status: Active"
          }
        ]
      }
    ]
  }' \
  "$WEBHOOK"

echo ""
echo "✅ Test message sent! Check your #aiops-alerts channel."
