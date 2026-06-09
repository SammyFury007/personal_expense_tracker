# 🧪 Quick Testing Guide - Personal Expense Tracker

## How to Test the Application Before Submission

---

## SETUP & INSTALLATION

### 1. Install Dependencies

```bash
# Navigate to your project folder
cd Personal-Expense-Tracker

# Install required packages
pip install -r requirements.txt
```

Expected output:
```
Successfully installed matplotlib-3.7.1 pandas-2.0.3 tabulate-0.9.0
```

---

## RUNNING THE APPLICATION

### Start the Application

```bash
python expense_tracker.py
```

You should see:
```
==================================================
💰 PERSONAL EXPENSE TRACKER 💰
==================================================

🔐 AUTHENTICATION
1. Login
2. Register
3. Exit

Select an option:
```

---

## TEST SCENARIO 1: User Registration & Login

### Test Registration

1. Select option `2` (Register)
2. Enter username: `testuser`
3. Enter password: `password123`
4. Confirm password: `password123`
5. Expected: "✅ User registered successfully!"

### Test Login

1. Select option `1` (Login)
2. Enter username: `testuser`
3. Enter password: `password123`
4. Expected: "✅ Welcome back, testuser!"

---

## TEST SCENARIO 2: Record Expenses

### First Expense - Food

1. Select option `1` (Record New Expense)
2. Select category: `1` (Food)
3. Enter amount: `500`
4. Enter description: `Lunch at restaurant`
5. Press Enter for today's date
6. Expected: "✅ Expense recorded successfully! (₹500)"

### Second Expense - Transport

1. Select option `1` (Record New Expense)
2. Select category: `2` (Transport)
3. Enter amount: `150`
4. Enter description: `Taxi to office`
5. Press Enter for today's date
6. Expected: "✅ Expense recorded successfully! (₹150)"

### Third Expense - Entertainment

1. Select option `1` (Record New Expense)
2. Select category: `4` (Entertainment)
3. Enter amount: `800`
4. Enter description: `Movie tickets and popcorn`
5. Press Enter for today's date
6. Expected: "✅ Expense recorded successfully! (₹800)"

### Fourth Expense - Different Date

1. Select option `1` (Record New Expense)
2. Select category: `1` (Food)
3. Enter amount: `300`
4. Enter description: `Dinner`
5. Enter date: `2024-06-08`
6. Expected: "✅ Expense recorded successfully! (₹300)"

---

## TEST SCENARIO 3: View All Expenses

1. Select option `2` (View All Expenses)
2. Expected output should show:
   - A table with all 4 expenses
   - Columns: ID, Category, Amount (₹), Description, Date
   - Total: ₹1750

Sample output:
```
==================================================
📊 ALL EXPENSES
==================================================

  ID  Category         Amount (₹)  Description                     Date
----  ---------------  -----------  --------------------------------  ----------
   1  Food             500          Lunch at restaurant             2024-06-09
   2  Transport        150          Taxi to office                  2024-06-09
   3  Entertainment    800          Movie tickets and popcorn       2024-06-09
   4  Food             300          Dinner                          2024-06-08

💰 Total: ₹1750.00
```

---

## TEST SCENARIO 4: Monthly Summary

1. Select option `3` (Monthly Spending Summary)
2. Enter month: `2024-06`
3. Expected output should show:
   - Month: 2024-06
   - Total Expenses: ₹1750
   - Category breakdown with percentages
   
Example:
```
📅 Month: 2024-06
💰 Total Expenses: ₹1750.00

Category          Amount (₹)      Percentage
-----------  ----------------  -----------
Food                800           45.7%
Entertainment       800           45.7%
Transport           150            8.6%
```

---

## TEST SCENARIO 5: Search by Date Range

1. Select option `4` (Search by Date Range)
2. Enter start date: `2024-06-08`
3. Enter end date: `2024-06-09`
4. Expected: Display all 4 expenses with total ₹1750

---

## TEST SCENARIO 6: Search by Category

1. Select option `5` (Search by Category)
2. Select category: `1` (Food)
3. Expected: Display 2 expenses (500 + 300 = ₹800)
4. Message: "💰 Total: ₹800.00"

---

## TEST SCENARIO 7: Budget Tracking

1. Select option `6` (Budget Tracking)
2. Enter month: `2024-06`
3. Enter budget limit: `2000`
4. Expected output:
   - Budget Limit: ₹2000.00
   - Total Spent: ₹1750.00
   - Spent: 87.5%
   - Remaining: ₹250.00
   - ✅ (Not overspent)

### Test Overspending Alert

1. Select option `6` (Budget Tracking)
2. Enter month: `2024-06`
3. Enter budget limit: `1500`
4. Expected:
   - ⚠️ OVERSPENT by: ₹250.00
   - Progress bar showing 116.7%

---

## TEST SCENARIO 8: Generate Charts

1. Select option `7` (Generate Charts)
2. Enter month: `2024-06`
3. Expected: A window with 4 charts should appear:
   - Pie chart (expense distribution)
   - Bar chart (amount by category)
   - Line chart (daily trend)
   - Statistics panel

4. Close the chart window to continue

---

## TEST SCENARIO 9: Export Report

1. Select option `8` (Export Report)
2. Expected:
   - New folder "reports" created
   - CSV file generated: `expense_report_YYYYMMDD_HHMMSS.csv`
   - Message showing: Total records: 4, Total amount: ₹1750.00
   - File location: `reports/expense_report_*.csv`

### Verify CSV File

1. Open the generated CSV file
2. Should contain columns: Date, Category, Amount (₹), Description
3. Should have 4 data rows

---

## TEST SCENARIO 10: Logout & Relogin

1. Select option `9` (Logout)
2. Expected: "✅ Logged out successfully!"
3. Back at authentication menu
4. Login again with `testuser` / `password123`
5. All previous expenses should still be there

---

## ERROR HANDLING TESTS

### Test Invalid Input - Amount

1. Select option `1` (Record Expense)
2. Select category: `1`
3. Enter amount: `abc`
4. Expected: "❌ Invalid input!"

### Test Invalid Input - Date Format

1. Select option `1` (Record Expense)
2. Select category: `1`
3. Enter amount: `500`
4. Enter date: `06-09-2024` (wrong format)
5. Expected: "❌ Invalid date format! Use YYYY-MM-DD"

### Test Invalid Login

1. At login screen, enter:
   - Username: `wronguser`
   - Password: `wrongpass`
2. Expected: "❌ Invalid username or password!"

---

## FINAL VERIFICATION CHECKLIST

- [ ] Application starts without errors
- [ ] User registration works
- [ ] User login works
- [ ] Can record expenses
- [ ] View all expenses shows correct data
- [ ] Monthly summary calculates correctly
- [ ] Search by date range works
- [ ] Search by category works
- [ ] Budget tracking shows correct percentages
- [ ] Charts display correctly (no errors)
- [ ] CSV export creates file successfully
- [ ] Logout works
- [ ] Can relogin and see saved data
- [ ] Database file created (expense_tracker.db)
- [ ] Error handling works for invalid inputs

---

## COMMON ISSUES & SOLUTIONS

### Issue: "ModuleNotFoundError: No module named 'matplotlib'"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Charts not displaying

**Solution:**
- Make sure matplotlib is installed
- If on Linux without display, this is expected (just a limitation)
- Application should still work for all other features

### Issue: "Database is locked" error

**Solution:**
- Close the application completely
- Wait 2-3 seconds
- Restart application

### Issue: Permission denied on Linux

**Solution:**
```bash
chmod +x expense_tracker.py
python expense_tracker.py
```

---

## TESTING TIPS

1. **Test with multiple users:** Register 2-3 different users and verify data isolation

2. **Test date handling:** Try various date formats to ensure error handling works

3. **Test with large numbers:** Record very large amounts to verify precision

4. **Test edge cases:**
   - Empty descriptions (should be optional)
   - Duplicate expenses
   - Expenses on same day

5. **Test menu navigation:** Try invalid options to see error handling

---

## PERFORMANCE EXPECTATIONS

- Application should start in <2 seconds
- Charts should generate in <3 seconds
- Database queries should be instant
- CSV export should be instant

---

## BEFORE SUBMITTING - FINAL CHECKS

1. ✅ Run the application completely start to finish
2. ✅ Test all 10 menu options
3. ✅ Test error handling
4. ✅ Verify all files are in GitHub repository
5. ✅ Verify repository is PUBLIC
6. ✅ Check README.md displays correctly on GitHub
7. ✅ Get the GitHub repository URL ready for submission

---

**Once all tests pass, you're ready to submit! 🎉**

---

## Example Test Session Output

```
python expense_tracker.py

==================================================
💰 PERSONAL EXPENSE TRACKER 💰
==================================================

🔐 AUTHENTICATION
1. Login
2. Register
3. Exit

Select an option: 2

==================================================
📝 USER REGISTRATION
==================================================
Enter username: testuser
Enter password: ****
Confirm password: ****
✅ User registered successfully!

🔐 AUTHENTICATION
1. Login
2. Register
3. Exit

Select an option: 1

==================================================
🔐 USER LOGIN
==================================================
Enter username: testuser
Enter password: ****
✅ Welcome back, testuser!

==================================================
📊 MAIN MENU (Logged in as: testuser)
==================================================
1. Record New Expense
2. View All Expenses
... [and so on]
```

---

**Congratulations! Your Expense Tracker is ready for submission! 🚀**
