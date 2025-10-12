#!/bin/bash

# GitHub Labels Setup Script
# Creates all necessary labels for auto-labeling and PR management

set -e

echo "🏷️  GitHub Labels Setup"
echo "======================="
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed."
    echo "   Install it from: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub CLI."
    echo "   Run: gh auth login"
    exit 1
fi

echo "✅ GitHub CLI is ready"
echo ""

# Function to create label if it doesn't exist
create_label() {
    local name="$1"
    local color="$2"
    local description="$3"

    if gh label list | grep -q "^$name"; then
        echo "⏭️  Label '$name' already exists"
    else
        gh label create "$name" --color "$color" --description "$description"
        echo "✅ Created label '$name'"
    fi
}

echo "Creating category labels..."
create_label "documentation" "0075ca" "Documentation changes"
create_label "ui" "d4c5f9" "UI/Frontend changes"
create_label "backend" "c2e0c6" "Backend/Logic changes"
create_label "config" "fef2c0" "Configuration changes"
create_label "devops" "0e8a16" "DevOps/Infrastructure"
create_label "testing" "e99695" "Test changes"
create_label "security" "d93f0b" "Security-related"
create_label "dependencies" "0366d6" "Dependency updates"

echo ""
echo "Creating size labels..."
create_label "size/xs" "ededed" "< 10 lines changed"
create_label "size/s" "d4c5f9" "< 100 lines changed"
create_label "size/m" "fbca04" "< 500 lines changed"
create_label "size/l" "ff9800" "< 1000 lines changed"
create_label "size/xl" "d93f0b" "> 1000 lines changed"

echo ""
echo "Creating workflow labels..."
create_label "automated" "006b75" "Automated PR/issue"
create_label "ci" "1d76db" "CI/CD related"
create_label "performance" "5319e7" "Performance improvements"

echo ""
echo "Creating priority labels..."
create_label "priority/high" "d93f0b" "High priority"
create_label "priority/medium" "fbca04" "Medium priority"
create_label "priority/low" "0e8a16" "Low priority"

echo ""
echo "Creating status labels..."
create_label "status/needs-review" "fbca04" "Needs review"
create_label "status/in-progress" "0052cc" "Work in progress"
create_label "status/blocked" "d93f0b" "Blocked by something"

echo ""
echo "✅ All labels created successfully!"
echo ""
echo "📋 Summary:"
gh label list | wc -l | xargs echo "   Total labels:"
echo ""
echo "🔗 View labels at:"
echo "   https://github.com/$(gh repo view --json nameWithOwner -q .nameWithOwner)/labels"
