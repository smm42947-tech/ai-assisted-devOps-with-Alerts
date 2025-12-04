<img width="873" height="582" alt="image" src="https://github.com/user-attachments/assets/3f68e249-08d7-4689-9c11-01e3d3255af2" />


# 🏗️ Architecture

<img width="672" height="261" alt="image" src="https://github.com/user-attachments/assets/4cacc958-c406-42e5-a657-e4f4a247b1cd" />


# 📁 Project Structure

<img width="719" height="318" alt="image" src="https://github.com/user-attachments/assets/30f53f01-1486-40b3-90f8-89417acc2b4f" />

# 🛠️ Installation

### Prerequisites

Python 3.8+

Slack workspace with admin access

Linux/Unix environment (tested on Ubuntu)

### Step 1: Clone Repository

git clone <your-repo-url>

cd ai-assisted-devops/day-6

### Step 2: Set Up Python Environment

python3 -m venv venv

source venv/bin/activate

pip install requests

### Step 3: Configure Slack Integration

Go to Slack API Apps

Create new app → "From scratch"

Name: "AIOps Alert Bot"

Enable Incoming Webhooks

Add webhook to #aiops-alerts channel

Copy webhook URL (format: https://hooks.slack.com/services/TXXXXX/BXXXXX/XXXXX)

### Step 4: Set Environment Variable

export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/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"

For persistence, add to ~/.bashrc:

echo 'export SLACK_WEBHOOK_URL="your_webhook_url"' >> ~/.bashrc

source ~/.bashrc

## 🚀 Quick Start

Run Once (Manual Testing)

cd ~/ai-assisted-devops/day-6

source venv/bin/activate

export SLACK_WEBHOOK_URL="your_webhook_url"

python3 aiops_slack_final.py

## Test Slack Connection

./test_webhook.sh

## OR

python3 aiops_test_simple.py

## Launch Full System

chmod +x start_aiops.sh

./start_aiops.sh

## ⚙️ Configuration

### Cron Jobs Setup

To enable automated monitoring every 10 minutes:

### Add to crontab

crontab -e

### Add this line:

*/10 * * * * cd /home/azureuser/ai-assisted-devops/day-6 && SLACK_WEBHOOK_URL="your_webhook_url" /usr/bin/python3 aiops_slack_final.py >> /home/azureuser/aiops_cron.log 2>&1

### Customize Analysis

Edit aiops_slack_final.py to modify:

Error thresholds

Alert severity levels

Pattern detection rules

Slack message formatting

## 🎯 Features in Detail

<img width="834" height="268" alt="image" src="https://github.com/user-attachments/assets/a6999358-c134-4d5c-a2fb-a7a1021e6181" />


<img width="677" height="486" alt="image" src="https://github.com/user-attachments/assets/7f2a263c-38b4-48f4-b214-26d7ae6bada6" />


## 🎭 Demo Presentation

## Quick Demo Steps:

### Test Connection

python3 aiops_test_simple.py

### Run Analysis

python3 aiops_slack_final.py

### Check Results

cat aiops_results.json

### Check Slack #aiops-alerts channel

### Add Test Errors

echo "$(date) ERROR: Demo test error" >> system_logs.txt

echo "$(date) CRITICAL: Demo critical error" >> system_logs.txt

python3 aiops_slack_final.py

<img width="682" height="428" alt="image" src="https://github.com/user-attachments/assets/5e4390c6-4ac8-441b-ad65-8b484f3654e6" />


<img width="654" height="430" alt="image" src="https://github.com/user-attachments/assets/e8e2c1aa-3d0a-40cd-8342-2e95b8bf9ad1" />
