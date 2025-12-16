# PERSONAL BUDGET MANAGER 

A simple command-line tool that helps users track income, expenses, and view summaries of their spending.

## Project Overview

As a college student preparing to move to Boston for a summer internship, I wanted a practical way to track my own finances. Managing rent, groceries, and daily expenses can be overwhelming—and many students face the same challenge.

The **Personal Budget Manager** allows users to log transactions into a CSV file, categorize income and expenses, and view summaries or monthly statistics. It is lightweight, offline, and ideal for students or anyone who wants a simple budgeting tool without using large apps. 

## Features

### Must-have (MVP)

- Record a transaction with amount, category, and date
- Save all transactions to a CSV file
- View all recorded transactions
- View spending grouped by category, e.g., rent, food, transportation
- View a summary: total income, total expenses, and current balance
- View monthly statistics (income, expenses, balance per month)
- Evaluate monthly spending (good/caution/overspending)

### Should-have (not implemented yet)
- Edit an existing transaction
- Export summary to a CSV file

## Installation

```bash
# clone the repository
git clone <your_repo_url>
cd personal-budget-manager

# create virtual environment
python3 -m venv .venv

# activate environment
source .venv/bin/activate

# no external dependencies required (Python standard library only)
python main.py
```

## Usage

1. Run `python main.py` from the project root (with virtual environment activated).
2. Choose from the menu options:
- Add a transaction
- View all transactions
- View spending by category
- View summary
- View monthly statistics
- Evaluate monthly spending
- Quit 

3. Follow all instructions displayed in the terminal. 

## Credits
 
- Tu Duong
- AI tools: ChatGPT, Claude

