# 💰 Personal Expense Tracker

## Project Overview

The **Personal Expense Tracker** is a command-line application designed to help individuals understand and manage their spending habits. It provides a comprehensive solution for recording, analyzing, and visualizing personal expenses with an intuitive menu-driven interface.

**Problem Statement:** Individuals often struggle to understand where their money goes each month.

**Solution:** This application tracks all expenses, categorizes them, and provides detailed insights through summaries, reports, and visual charts.

---

## 🎯 Features

### Core Features Implemented

✅ **User Authentication**
- Secure user registration and login
- Password-protected accounts
- Multiple user support

✅ **Record Expenses**
- Add new expenses with amount, category, description, and date
- Auto-populate with current date
- Validate input data
- Support for past or future date entry

✅ **Expense Categories**
- 7 default categories: Food, Transport, Utilities, Entertainment, Healthcare, Shopping, Others
- Pre-populated for new users
- Easy category selection during expense recording

✅ **Monthly Spending Summary**
- View total spending for any month
- Category-wise breakdown
- Percentage distribution
- Year-Month selection format

✅ **Budget Tracking**
- Set monthly budget limits
- Track spending against budget
- Visual progress bar
- Overspend alerts

✅ **Search by Date Range**
- Filter expenses between two dates
- View all matching transactions
- Calculate total for date range

✅ **Search by Category**
- Filter expenses by spending category
- View all expenses in selected category
- Category-wise totals

✅ **Export Reports**
- Export all expenses to CSV format
- Timestamped filenames for easy organization
- Summary statistics in report

✅ **Generate Charts & Visualizations**
- Pie chart: Expense distribution by category
- Bar chart: Spending amount by category
- Line chart: Daily spending trend
- Summary statistics panel
- All in one comprehensive view

---

## 📊 Database Schema

### Users Table
```
users
├── user_id (INTEGER, PRIMARY KEY, AUTO-INCREMENT)
├── username (TEXT, UNIQUE, NOT NULL)
├── password (TEXT, NOT NULL)
└── created_at (TIMESTAMP)
```

### Categories Table
```
categories
├── category_id (INTEGER, PRIMARY KEY, AUTO-INCREMENT)
├── user_id (INTEGER, FOREIGN KEY)
├── category_name (TEXT, NOT NULL)
└── UNIQUE(user_id, category_name)
```

### Expenses Table
```
expenses
├── expense_id (INTEGER, PRIMARY KEY, AUTO-INCREMENT)
├── user_id (INTEGER, FOREIGN KEY)
├── category_id (INTEGER, FOREIGN KEY)
├── amount (REAL, NOT NULL)
├── description (TEXT)
├── date (DATE, NOT NULL)
└── created_at (TIMESTAMP)
```

---

## 🛠️ Technologies Used

- **Language:** Python 3.7+
- **Database:** SQLite3
- **UI:** Command-line menu-driven interface
- **Visualization:** Matplotlib, Pandas
- **Additional Libraries:** Tabulate (for formatted tables)

---

## 📋 Setup & Execution Instructions

### Prerequisites
- Python 3.7 or higher installed
- pip (Python package manager)

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Personal-Expense-Tracker.git
   cd Personal-Expense-Tracker
   ```

2. **Create Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
python expense_tracker.py
```

### First Time Setup

1. **Register a new account**
   - Enter unique username
   - Create a secure password (minimum 4 characters)
   - Confirm password
   - Default expense categories will be automatically created

2. **Login**
   - Use registered credentials to login
   - Access main menu after successful login

---

## 📖 User Guide

### Main Menu Options

#### 1. **Record New Expense**
   - Select expense category from available options
   - Enter amount in rupees (₹)
   - Add optional description
   - Specify date (defaults to today)
   - Expense is saved to database

#### 2. **View All Expenses**
   - Displays all recorded expenses
   - Shows ID, Category, Amount, Description, and Date
   - Displays total spending across all expenses

#### 3. **Monthly Spending Summary**
   - Enter month in YYYY-MM format (e.g., 2024-06)
   - View total spending for that month
   - See category-wise breakdown
   - View percentage distribution

#### 4. **Search by Date Range**
   - Enter start date (YYYY-MM-DD format)
   - Enter end date (YYYY-MM-DD format)
   - View all expenses within date range
   - See total for selected date range

#### 5. **Search by Category**
   - Select from available categories
   - View all expenses in selected category
   - See category total

#### 6. **Budget Tracking**
   - Enter month for budget tracking
   - Set budget limit in rupees
   - View current spending against budget
   - Visual progress bar shows percentage used
   - Alerts if overspent

#### 7. **Generate Charts**
   - Enter month for analysis
   - View 4 different visualizations:
     - Pie chart (percentage distribution)
     - Bar chart (amount by category)
     - Line chart (daily trend)
     - Summary statistics
   - Charts displayed in separate window

#### 8. **Export Report**
   - Exports all expenses to CSV file
   - Reports folder created automatically
   - Filename includes timestamp
   - Contains all expense details

#### 9. **Logout**
   - Securely logout from account
   - Return to authentication menu

#### 10. **Exit**
   - Safely close application

---

## 💡 Example Usage Workflow

```
1. Start application → python expense_tracker.py
2. Register new account
3. Login with credentials
4. Record first expense:
   - Category: Food
   - Amount: 500
   - Description: Lunch at restaurant
   - Date: 2024-06-09
5. Record more expenses
6. View monthly summary for June 2024
7. Search expenses between specific dates
8. Generate charts for visual analysis
9. Set budget limit and track spending
10. Export monthly report to CSV
11. Logout safely
```

---

## 🎓 Skills Demonstrated

✅ **Python Programming**
- Object-oriented design principles
- Control flow and data structures
- String manipulation and formatting
- File I/O operations

✅ **Database Management**
- SQLite3 database design
- CRUD operations (Create, Read, Update, Delete)
- Foreign key relationships
- Query optimization

✅ **Data Analysis**
- Aggregation and grouping
- Summary calculations
- Date range filtering
- Statistical analysis

✅ **Visualization**
- Matplotlib chart creation
- Pandas data manipulation
- Multi-plot layouts
- Statistical visualization

✅ **User Interface Design**
- Menu-driven navigation
- Input validation
- Error handling
- User feedback

---

## 📁 Project Structure

```
Personal-Expense-Tracker/
├── expense_tracker.py       # Main application file
├── requirements.txt         # Project dependencies
├── README.md               # This file
├── .gitignore              # Git ignore file
├── expense_tracker.db      # SQLite database (auto-created)
└── reports/                # CSV export folder (auto-created)
    └── expense_report_*.csv # Exported reports
```

---

## ⚙️ Configuration

### Default Categories
The following categories are automatically created for new users:
1. Food
2. Transport
3. Utilities
4. Entertainment
5. Healthcare
6. Shopping
7. Others

### Database Location
- `expense_tracker.db` is created in the same directory as the script

### Reports Location
- Exported CSV reports are saved in the `reports/` folder

---

## 🔒 Security Features

- Password-based authentication
- User-specific data isolation
- Foreign key constraints for data integrity
- Input validation for dates and amounts
- Secure password confirmation during registration

---

## 🚀 Future Enhancements

Potential features for future versions:
- Recurring expense automation
- Multi-currency support
- Expense budgeting by category
- Email report generation
- Mobile app version
- Cloud backup functionality
- Advanced filtering options
- Expense goals and targets
- Savings tracker

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'matplotlib'"
**Solution:** Run `pip install -r requirements.txt`

### Issue: "Database is locked"
**Solution:** Close other instances of the application

### Issue: "Invalid date format"
**Solution:** Use YYYY-MM-DD format (e.g., 2024-06-09)

### Issue: Charts not displaying
**Solution:** Ensure matplotlib is installed and display device is available

---

## 📝 Testing Checklist

- [x] User registration works correctly
- [x] User login validation
- [x] Expense recording with all fields
- [x] Default categories created
- [x] View all expenses
- [x] Monthly summary calculations
- [x] Date range filtering
- [x] Category filtering
- [x] Budget tracking and alerts
- [x] Chart generation
- [x] CSV export
- [x] Data persistence across sessions
- [x] Error handling for invalid inputs

---

## 📄 License

This project is open source and available under the MIT License.

---


