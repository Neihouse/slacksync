#!/bin/bash

# Create the directory structure
mkdir -p packages/{slacklist,slackboard,slackcalendar,shared}
mkdir -p {tests,docs,scripts}

# Create initial files in the root directory
touch README.md LICENSE CODE_OF_CONDUCT.md CONTRIBUTING.md ISSUE_TEMPLATE.md PULL_REQUEST_TEMPLATE.md requirements.txt

# Optionally, create pyproject.toml if using Poetry
touch pyproject.toml

# Create initial files in each package
for package in slacklist slackboard slackcalendar; do
  touch packages/$package/{__init__.py,app.py,commands.py,views.py,utils.py}
done

# Create shared components
touch packages/shared/{auth.py,data.py,errors.py,config.py}

# Create initial files in tests, docs, and scripts directories
touch tests/.gitkeep docs/.gitkeep scripts/.gitkeep

echo "Directory structure and initial files created successfully."