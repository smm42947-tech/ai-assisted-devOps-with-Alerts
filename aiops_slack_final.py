#!/usr/bin/env python3
"""
aiops_slack_final.py - Complete AIOps with Slack alerts
Author: Azure User
Webhook: T0A1CHV57KP/B0A19MB564B/YgYISdl1FYO7pltYCOkJycKY
"""

import os
import json
import re
from datetime import datetime, timedelta
from collections import defaultdict
import requests
import sys

# ==================== SLACK INTEGRATION ====================
class SlackAIOps:
    def __init__(self):
        self.webhook = os.getenv("SLACK_WEBHOOK_URL")
        if not self.webhook:
            print("⚠️  SLACK_WEBHOOK_URL not set. Using your provided URL.")
            self.webhook = "https://hooks.slack.com/services/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"
        
        self.channel = "#aiops-alerts"
        self.username = "AIOps Bot 🤖"
    
    def send(self, message, severity="info", title=None, details=None):
        """Send message to Slack with rich formatting"""
        
        # Severity colors
        colors = {
            "info": "#36a64f",      # Green
            "success": "#2eb67d",   # Bright green
            "warning": "#ffcc00",   # Yellow
            "error": "#ff9900",     # Orange
            "critical": "#ff0000",  # Red
            "emergency": "#8b0000"  # Dark red
        }
        
        # Emojis
        emojis = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "🚨",
            "critical": "🔥",
            "emergency": "💀"
        }
        
        # Create payload
        payload = {
            "username": self.username,
            "icon_emoji": ":robot_face:",
            "channel": self.channel,
            "attachments": [
                {
                    "color": colors.get(severity, "#808080"),
                    "title": f"{emojis.get(severity, '📌')} {title if title else severity.upper()}",
                    "text": message,
                    "fields": [
                        {
                            "title": "Severity",
                            "value": severity.upper(),
                            "short": True
                        },
                        {
                            "title": "Time",
                            "value": datetime.now().strftime("%H:%M:%S"),
                            "short": True
                        },
                        {
                            "title": "Date",
                            "value": datetime.now().strftime("%Y-%m-%d"),
                            "short": True
                        }
                    ],
                    "footer": "AIOps System | Devops Workspace",
                    "ts": datetime.now().timestamp()
                }
            ]
        }
        
        # Add details if provided
        if details:
            details_text = ""
            for key, value in details.items():
                if isinstance(value, (dict, list)):
                    details_text += f"*{key}:*\n```{json.dumps(value, indent=2)[:500]}```\n"
                else:
                    details_text += f"*{key}:* {value}\n"
            
            payload["attachments"][0]["fields"].append({
                "title": "Details",
                "value": details_text,
                "short": False
            })
        
        # Send to Slack
        try:
            response = requests.post(
                self.webhook,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            if response.status_code == 200:
                print(f"✅ Slack: {severity.upper()} - {message[:50]}...")
                return True
            else:
                print(f"❌ Slack error {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Failed to send to Slack: {e}")
            return False
    
    def send_test(self):
        """Send test message"""
        return self.send(
            "AIOps system is online and monitoring logs.",
            "success",
            "🚀 AIOps System Started",
            {
                "Status": "Operational",
                "Webhook": "Configured",
                "Workspace": "Devops",
                "Channel": "#aiops-alerts"
            }
        )

# ==================== LOG ANALYZER ====================
class LogAnalyzer:
    def __init__(self, log_file="system_logs.txt"):
        self.log_file = log_file
        self.slack = SlackAIOps()
        self.results = {}
        
    def analyze(self):
        """Main analysis function"""
        print("\n" + "="*60)
        print("🔍 AIOPS LOG ANALYSIS WITH SLACK ALERTS")
        print("="*60)
        
        # Send startup message
        self.slack.send_test()
        
        # Read logs
        logs = self._read_logs()
        if not logs:
            self.slack.send(
                "No log file found or empty logs.",
                "warning",
                "📭 Log File Issue"
            )
            return self.results
        
        # Perform analysis
        self.results = self._analyze_logs(logs)
        
        # Generate alerts
        self._generate_alerts()
        
        # Send summary
        self._send_summary()
        
        return self.results
    
    def _read_logs(self):
        """Read log file"""
        try:
            with open(self.log_file, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"❌ File not found: {self.log_file}")
            return []
    
    def _analyze_logs(self, logs):
        """Analyze logs for patterns and errors"""
        analysis = {
            "total": len(logs),
            "errors": 0,
            "warnings": 0,
            "by_hour": defaultdict(int),
            "error_types": defaultdict(int),
            "critical_count": 0,
            "patterns": {},
            "top_errors": [],
            "timeline": []
        }
        
        # Define patterns to check
        patterns = {
            "error": r"error|failed|exception|err\s",
            "warning": r"warning|warn",
            "critical": r"panic|fatal|emergency|segmentation",
            "timeout": r"timeout|timed\s+out",
            "memory": r"out of memory|oom|memory\s+error",
            "connection": r"connection refused|failed to connect|connection timeout",
            "permission": r"permission denied|access denied|forbidden",
            "disk": r"disk full|no space|disk error"
        }
        
        for i, line in enumerate(logs, 1):
            line_lower = line.lower()
            
            # Check each pattern
            for pattern_name, pattern in patterns.items():
                if re.search(pattern, line_lower, re.IGNORECASE):
                    analysis["error_types"][pattern_name] += 1
                    
                    if pattern_name == "error":
                        analysis["errors"] += 1
                    elif pattern_name == "warning":
                        analysis["warnings"] += 1
                    elif pattern_name == "critical":
                        analysis["critical_count"] += 1
            
            # Track by hour (if timestamp exists)
            timestamp_match = re.search(r'(\d{2}):\d{2}:\d{2}', line)
            if timestamp_match:
                hour = timestamp_match.group(1)
                analysis["by_hour"][hour] += 1
            
            # Store every 100th log for timeline
            if i % 100 == 0:
                analysis["timeline"].append({
                    "line": i,
                    "sample": line[:100] + "..." if len(line) > 100 else line
                })
        
        # Calculate top errors
        analysis["top_errors"] = sorted(
            analysis["error_types"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        # Calculate error rate
        analysis["error_rate"] = (analysis["errors"] / analysis["total"] * 100) if analysis["total"] > 0 else 0
        
        return analysis
    
    def _generate_alerts(self):
        """Generate alerts based on analysis"""
        total = self.results["total"]
        errors = self.results["errors"]
        error_rate = self.results["error_rate"]
        
        # Alert 1: Error rate too high
        if error_rate > 20:
            self.slack.send(
                f"Error rate is {error_rate:.1f}% ({errors} errors in {total} logs)",
                "critical",
                "🚨 Critical Error Rate",
                {
                    "Error Rate": f"{error_rate:.1f}%",
                    "Threshold": "20%",
                    "Recommendation": "Check application immediately"
                }
            )
        elif error_rate > 10:
            self.slack.send(
                f"Error rate is {error_rate:.1f}% ({errors} errors)",
                "warning",
                "⚠️ High Error Rate"
            )
        
        # Alert 2: Critical errors found
        if self.results["critical_count"] > 0:
            self.slack.send(
                f"Found {self.results['critical_count']} critical errors",
                "emergency",
                "🔥 CRITICAL ERRORS FOUND",
                {
                    "Count": self.results["critical_count"],
                    "Action": "IMMEDIATE ATTENTION REQUIRED"
                }
            )
        
        # Alert 3: Specific error patterns
        for error_type, count in self.results["top_errors"][:3]:
            if count > 5:
                self.slack.send(
                    f"Pattern '{error_type}' found {count} times",
                    "error" if count > 10 else "warning",
                    f"🔍 Pattern Detected: {error_type}"
                )
        
        # Alert 4: Hourly pattern
        hourly = self.results["by_hour"]
        if hourly:
            peak_hour = max(hourly.items(), key=lambda x: x[1])
            if peak_hour[1] > (total / 24 * 3):  # 3x average
                self.slack.send(
                    f"Peak activity at {peak_hour[0]}:00 ({peak_hour[1]} logs)",
                    "info",
                    "📈 Peak Activity Detected"
                )
    
    def _send_summary(self):
        """Send analysis summary to Slack"""
        total = self.results["total"]
        errors = self.results["errors"]
        warnings = self.results["warnings"]
        critical = self.results["critical_count"]
        
        # Create summary message
        if errors == 0 and critical == 0:
            message = f"✅ All clear! {total} logs analyzed with no errors."
            severity = "success"
            title = "✅ System Status: Healthy"
        elif critical > 0:
            message = f"🚨 {critical} CRITICAL errors found! {errors} total errors in {total} logs."
            severity = "emergency"
            title = "🚨 SYSTEM CRITICAL"
        elif errors > 0:
            message = f"⚠️ Found {errors} errors and {warnings} warnings in {total} logs."
            severity = "warning"
            title = "⚠️ System Issues Detected"
        else:
            message = f"ℹ️ {total} logs analyzed with {warnings} warnings."
            severity = "info"
            title = "ℹ️ System Status"
        
        # Send summary
        self.slack.send(
            message,
            severity,
            title,
            {
                "Total Logs": total,
                "Errors": errors,
                "Warnings": warnings,
                "Critical Errors": critical,
                "Error Rate": f"{self.results.get('error_rate', 0):.1f}%",
                "Top Error Types": dict(self.results.get("top_errors", [])[:3]),
                "Peak Hour": max(self.results.get("by_hour", {}).items(), key=lambda x: x[1])[0] + ":00" if self.results.get("by_hour") else "N/A"
            }
        )
        
        # Print console summary
        print(f"\n📊 ANALYSIS SUMMARY:")
        print(f"   Total logs: {total}")
        print(f"   Errors: {errors}")
        print(f"   Warnings: {warnings}")
        print(f"   Critical: {critical}")
        print(f"   Error rate: {self.results.get('error_rate', 0):.1f}%")
        print(f"   Top error: {self.results.get('top_errors', [['None', 0]])[0][0]}")
        print("="*60)

# ==================== MAIN EXECUTION ====================
def main():
    """Main function"""
    
    # Get log file from command line or use default
    log_file = sys.argv[1] if len(sys.argv) > 1 else "system_logs.txt"
    
    print(f"Starting AIOps analysis on: {log_file}")
    print(f"Slack Webhook: T0A1CHV57KP/B0A19MB564B/...")
    print(f"Channel: #aiops-alerts")
    print(f"Workspace: Devops")
    
    # Create analyzer and run
    analyzer = LogAnalyzer(log_file)
    results = analyzer.analyze()
    
    # Save results to file
    with open("aiops_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Analysis complete! Results saved to aiops_results.json")
    print("📤 Check your Slack #aiops-alerts channel for notifications!")
    
    return results

if __name__ == "__main__":
    main()
