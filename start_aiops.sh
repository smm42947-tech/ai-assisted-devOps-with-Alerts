#!/bin/bash

# AIOps System Launcher
echo "========================================"
echo "🤖 AIOps System - Devops Workspace"
echo "========================================"

# Set your webhook URL
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/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"

echo "🔗 Webhook: T0A1CHV57KP/B0A19MB564B/..."
echo "📊 Log file: $1"
echo "📤 Channel: #aiops-alerts"
echo ""

# Run the analyzer
if [ -f "$1" ]; then
    python3 aiops_slack_final.py "$1"
elif [ -f "system_logs.txt" ]; then
    echo "ℹ️  Using default log file: system_logs.txt"
    python3 aiops_slack_final.py
else
    echo "❌ No log file specified and system_logs.txt not found"
    echo "Usage: $0 [logfile]"
    exit 1
fi

echo ""
echo "✅ Done! Check Slack for alerts."
