#!/usr/bin/env bash

# ----------------------------------------
# OSS-style™ GitHub repo setup script
# Project: raffle-portal
# Author: Sandro Regis a.k.a WarBro
# ----------------------------------------

set -e  # Fail on error

PROJECT_NAME="raffle-portal"
GITHUB_USER="srcsoftwareengineer"

echo "🔥 Initializing Git repository for '$PROJECT_NAME'..."

# Init repo and basic structure
git init
echo -e "venv/\n__pycache__/\n*.pyc\n.env\n.env.*\n*.sqlite3\ndb.sqlite3\n.DS_Store\n.idea/\n*.log" > .gitignore

echo "✅ .gitignore created"

# First commit
git add .
git commit -m "Initial commit for $PROJECT_NAME - StormSDK OSS-style™"

# GitHub repo creation via GH CLI
echo "🚀 Creating GitHub repository..."
gh repo create "$PROJECT_NAME" --public --source=. --remote=origin --push

echo "✅ Repository '$PROJECT_NAME' created and pushed to GitHub"

# Optional next steps
echo -e "\n🌱 Next steps:"
echo "1. Activate your virtualenv"
echo "2. Start your Django app: django-admin startproject core ."
echo "3. Push changes: git add . && git commit -m 'Start Django project' && git push"

echo -e "\n💥 Done! OSS-style™ repo is live!\n"

exit 0
