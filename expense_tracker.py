import sqlite3
import os
import sys
from datetime import datetime

# ── Optional dependencies ─────────────────────────────────────────────────────
try:
    import matplotlib.pyplot as plt # type: ignore
    import matplotlib # type: ignore
    matplotlib.use("TkAgg") if sys.platform != "darwin" else matplotlib.use("MacOSX")
except Exception:
    plt = None

try:
    import pandas as pd # type: ignore
except ImportError:
    pd = None

try:
    from tabulate import tabulate # type: ignore
except ImportError:
    def tabulate(data, headers=(), tablefmt="grid"):
        rows = [list(map(str, row)) for row in data]
        header = list(map(str, headers)) if headers else []
        all_rows = [header] + rows if header else rows
        if not all_rows:
            return ""
        widths = [max(len(str(cell)) for cell in col) for col in zip(*all_rows)]
        sep = " | "
        div = "-+-".join("-" * w for w in widths)
        def fmt(row):
            return sep.join(str(c).ljust(w) for c, w in zip(row, widths))
        lines = []
        if header:
            lines += [fmt(header), div]
        lines += [fmt(r) for r in rows]
        return "\n".join(lines)

# ── Constants ─────────────────────────────────────────────────────────────────
DB_FILE = "expense_tracker.db"
CURRENT_USER = None          # Stores logged-in username
DEFAULT_CATEGORIES = ["Food", "Transport", "Utilities",
                       "Entertainment", "Healthcare", "Shopping", "Others"]


# ── Password input helper (plain input, works on all platforms) ───────────────
def get_password(prompt="Enter password: ") -> str:
    """Plain input for passwords — works on Windows CMD, VS Code, Git Bash, etc."""
    return input(prompt).strip()


# ── Database setup ────────────────────────────────────────────────────────────
def init_database():
    """Create tables if they do not already exist."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.executescript("""
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS users (
            user_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            username   TEXT    UNIQUE NOT NULL,
            password   TEXT    NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS categories (
            category_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id       INTEGER NOT NULL,
            category_name TEXT    NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            UNIQUE(user_id, category_name)
        );

        CREATE TABLE IF NOT EXISTS expenses (
            expense_id  INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            amount      REAL    NOT NULL,
            description TEXT    DEFAULT '',
            date        DATE    NOT NULL,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id)     REFERENCES users(user_id),
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        );
    """)

    conn.commit()
    conn.close()


# ── Helper utilities ──────────────────────────────────────────────────────────
def get_user_id(username: str):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def add_default_categories(user_id: int):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    for cat in DEFAULT_CATEGORIES:
        try:
            cur.execute(
                "INSERT INTO categories (user_id, category_name) VALUES (?, ?)",
                (user_id, cat)
            )
        except sqlite3.IntegrityError:
            pass
    conn.commit()
    conn.close()


def get_categories(user_id: int):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        "SELECT category_id, category_name FROM categories WHERE user_id = ? ORDER BY category_name",
        (user_id,)
    )
    cats = cur.fetchall()
    conn.close()
    return cats


def divider(title=""):
    print("\n" + "=" * 50)
    if title:
        print(title)
        print("=" * 50)


# ── Authentication ─────────────────────────────────────────────────────────────
def register_user() -> bool:
    global CURRENT_USER
    divider("📝 USER REGISTRATION")

    username = input("Enter username: ").strip()
    if not username:
        print("❌ Username cannot be empty!")
        return False

    password = get_password("Enter password (min 4 chars): ")
    if len(password) < 4:
        print("❌ Password must be at least 4 characters!")
        return False

    confirm = get_password("Confirm password: ")
    if password != confirm:
        print("❌ Passwords do not match!")
        return False

    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        print("❌ Username already exists! Please choose another.")
        return False

    uid = get_user_id(username)
    add_default_categories(uid)
    print(f"✅ Account created for '{username}'! Default categories added.")
    return True


def login_user() -> bool:
    global CURRENT_USER
    divider("🔐 USER LOGIN")

    username = input("Enter username: ").strip()
    password = get_password("Enter password: ")

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        "SELECT user_id FROM users WHERE username = ? AND password = ?",
        (username, password)
    )
    row = cur.fetchone()
    conn.close()

    if row:
        CURRENT_USER = username
        print(f"✅ Welcome back, {username}! 👋")
        return True
    else:
        print("❌ Invalid username or password!")
        return False


# ── Feature 1 – Record expense ────────────────────────────────────────────────
def record_expense():
    divider("💸 RECORD NEW EXPENSE")

    user_id = get_user_id(CURRENT_USER)
    categories = get_categories(user_id)

    if not categories:
        print("❌ No categories found!")
        return

    print("\n📂 Available Categories:")
    for idx, (_, name) in enumerate(categories, 1):
        print(f"   {idx}. {name}")

    try:
        choice = int(input("\nSelect category number: "))
        if not (1 <= choice <= len(categories)):
            print("❌ Invalid choice!")
            return
        cat_id = categories[choice - 1][0]
        cat_name = categories[choice - 1][1]

        amount = float(input("Enter amount (₹): "))
        if amount <= 0:
            print("❌ Amount must be positive!")
            return

        description = input("Enter description (optional, press Enter to skip): ").strip()

        date_str = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")
        else:
            datetime.strptime(date_str, "%Y-%m-%d")   # Validates format

        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO expenses (user_id, category_id, amount, description, date) VALUES (?, ?, ?, ?, ?)",
            (user_id, cat_id, amount, description, date_str)
        )
        conn.commit()
        conn.close()

        print(f"✅ Expense of ₹{amount:.2f} recorded under '{cat_name}' on {date_str}!")

    except ValueError as e:
        print(f"❌ Invalid input! ({e})")


# ── Feature 2 – View all expenses ────────────────────────────────────────────
def view_all_expenses():
    divider("📊 ALL EXPENSES")

    user_id = get_user_id(CURRENT_USER)
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        SELECT e.expense_id, c.category_name, e.amount, e.description, e.date
        FROM expenses e
        JOIN categories c ON e.category_id = c.category_id
        WHERE e.user_id = ?
        ORDER BY e.date DESC
    """, (user_id,))
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("❌ No expenses recorded yet!")
        return

    headers = ["ID", "Category", "Amount (₹)", "Description", "Date"]
    print("\n" + tabulate(rows, headers=headers, tablefmt="grid"))
    print(f"\n💰 Total: ₹{sum(r[2] for r in rows):.2f}")


# ── Feature 3 – Monthly summary ───────────────────────────────────────────────
def monthly_summary():
    divider("📈 MONTHLY SPENDING SUMMARY")

    user_id = get_user_id(CURRENT_USER)
    month_input = input("Enter month (YYYY-MM) or press Enter for current month: ").strip()

    if not month_input:
        month_input = datetime.now().strftime("%Y-%m")
    else:
        try:
            datetime.strptime(month_input + "-01", "%Y-%m-%d")
        except ValueError:
            print("❌ Invalid format! Use YYYY-MM (e.g. 2026-06)")
            return

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
        SELECT SUM(amount) FROM expenses
        WHERE user_id = ? AND strftime('%Y-%m', date) = ?
    """, (user_id, month_input))
    total = cur.fetchone()[0] or 0

    cur.execute("""
        SELECT c.category_name, SUM(e.amount)
        FROM expenses e
        JOIN categories c ON e.category_id = c.category_id
        WHERE e.user_id = ? AND strftime('%Y-%m', e.date) = ?
        GROUP BY c.category_name
        ORDER BY SUM(e.amount) DESC
    """, (user_id, month_input))
    summary = cur.fetchall()
    conn.close()

    if not summary:
        print(f"❌ No expenses found for {month_input}!")
        return

    print(f"\n📅 Month      : {month_input}")
    print(f"💰 Total      : ₹{total:.2f}\n")

    data = [[cat, f"₹{amt:.2f}", f"{amt/total*100:.1f}%"] for cat, amt in summary]
    print(tabulate(data, headers=["Category", "Amount (₹)", "% Share"], tablefmt="grid"))


# ── Feature 4 – Search by date range ─────────────────────────────────────────
def search_by_date_range():
    divider("🔍 SEARCH BY DATE RANGE")

    user_id = get_user_id(CURRENT_USER)

    try:
        start = input("Enter start date (YYYY-MM-DD): ").strip()
        end   = input("Enter end date   (YYYY-MM-DD): ").strip()
        datetime.strptime(start, "%Y-%m-%d")
        datetime.strptime(end,   "%Y-%m-%d")
    except ValueError:
        print("❌ Invalid date format! Use YYYY-MM-DD")
        return

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        SELECT e.expense_id, c.category_name, e.amount, e.description, e.date
        FROM expenses e
        JOIN categories c ON e.category_id = c.category_id
        WHERE e.user_id = ? AND e.date BETWEEN ? AND ?
        ORDER BY e.date DESC
    """, (user_id, start, end))
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print(f"❌ No expenses found between {start} and {end}!")
        return

    headers = ["ID", "Category", "Amount (₹)", "Description", "Date"]
    print("\n" + tabulate(rows, headers=headers, tablefmt="grid"))
    print(f"\n💰 Total: ₹{sum(r[2] for r in rows):.2f}")


# ── Feature 5 – Search by category ───────────────────────────────────────────
def search_by_category():
    divider("🔍 SEARCH BY CATEGORY")

    user_id = get_user_id(CURRENT_USER)
    categories = get_categories(user_id)

    if not categories:
        print("❌ No categories found!")
        return

    print("\n📂 Available Categories:")
    for idx, (_, name) in enumerate(categories, 1):
        print(f"   {idx}. {name}")

    try:
        choice = int(input("\nSelect category number: "))
        if not (1 <= choice <= len(categories)):
            print("❌ Invalid choice!")
            return
        cat_id, cat_name = categories[choice - 1]

        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("""
            SELECT e.expense_id, c.category_name, e.amount, e.description, e.date
            FROM expenses e
            JOIN categories c ON e.category_id = c.category_id
            WHERE e.user_id = ? AND e.category_id = ?
            ORDER BY e.date DESC
        """, (user_id, cat_id))
        rows = cur.fetchall()
        conn.close()

        if not rows:
            print(f"❌ No expenses found in '{cat_name}'!")
            return

        print(f"\n📂 Expenses in '{cat_name}':\n")
        print(tabulate(rows, headers=["ID", "Category", "Amount (₹)", "Description", "Date"], tablefmt="grid"))
        print(f"\n💰 Total for '{cat_name}': ₹{sum(r[2] for r in rows):.2f}")

    except ValueError:
        print("❌ Invalid input!")


# ── Feature 6 – Budget tracking ──────────────────────────────────────────────
def budget_tracking():
    divider("💼 BUDGET TRACKING")

    user_id = get_user_id(CURRENT_USER)

    month_input = input("Enter month (YYYY-MM) or press Enter for current month: ").strip()
    if not month_input:
        month_input = datetime.now().strftime("%Y-%m")
    else:
        try:
            datetime.strptime(month_input + "-01", "%Y-%m-%d")
        except ValueError:
            print("❌ Invalid format! Use YYYY-MM")
            return

    try:
        budget_limit = float(input("Enter your budget limit (₹): "))
        if budget_limit <= 0:
            print("❌ Budget must be positive!")
            return
    except ValueError:
        print("❌ Invalid amount!")
        return

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        SELECT SUM(amount) FROM expenses
        WHERE user_id = ? AND strftime('%Y-%m', date) = ?
    """, (user_id, month_input))
    total_spent = cur.fetchone()[0] or 0
    conn.close()

    remaining  = budget_limit - total_spent
    percentage = total_spent / budget_limit * 100

    print(f"\n📅 Month        : {month_input}")
    print(f"💰 Budget Limit : ₹{budget_limit:.2f}")
    print(f"💸 Total Spent  : ₹{total_spent:.2f}")
    print(f"📊 Used         : {percentage:.1f}%")

    if remaining >= 0:
        print(f"✅ Remaining    : ₹{remaining:.2f}")
    else:
        print(f"⚠️  OVERSPENT by : ₹{abs(remaining):.2f}")

    # Visual progress bar (caps bar fill at 100% width)
    filled = min(int(30 * percentage / 100), 30)
    bar    = "█" * filled + "░" * (30 - filled)
    print(f"\n[{bar}] {percentage:.1f}%\n")

    # Per-category breakdown
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        SELECT c.category_name, SUM(e.amount)
        FROM expenses e
        JOIN categories c ON e.category_id = c.category_id
        WHERE e.user_id = ? AND strftime('%Y-%m', e.date) = ?
        GROUP BY c.category_name
        ORDER BY SUM(e.amount) DESC
    """, (user_id, month_input))
    breakdown = cur.fetchall()
    conn.close()

    if breakdown:
        print("📂 Category Breakdown:")
        data = [[cat, f"₹{amt:.2f}", f"{amt/total_spent*100:.1f}%" if total_spent else "0%"]
                for cat, amt in breakdown]
        print(tabulate(data, headers=["Category", "Amount (₹)", "% of Spent"], tablefmt="simple"))


# ── Feature 7 – Charts ────────────────────────────────────────────────────────
def generate_chart():
    divider("📊 GENERATE CHARTS")

    if plt is None:
        print("❌ matplotlib is not installed.")
        print("   Run:  pip install matplotlib")
        return

    user_id = get_user_id(CURRENT_USER)

    month_input = input("Enter month (YYYY-MM) or press Enter for current month: ").strip()
    if not month_input:
        month_input = datetime.now().strftime("%Y-%m")
    else:
        try:
            datetime.strptime(month_input + "-01", "%Y-%m-%d")
        except ValueError:
            print("❌ Invalid format! Use YYYY-MM")
            return

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        SELECT c.category_name, SUM(e.amount)
        FROM expenses e
        JOIN categories c ON e.category_id = c.category_id
        WHERE e.user_id = ? AND strftime('%Y-%m', e.date) = ?
        GROUP BY c.category_name
        ORDER BY SUM(e.amount) DESC
    """, (user_id, month_input))
    cat_data = cur.fetchall()

    cur.execute("""
        SELECT date, SUM(amount)
        FROM expenses
        WHERE user_id = ? AND strftime('%Y-%m', date) = ?
        GROUP BY date
        ORDER BY date
    """, (user_id, month_input))
    daily_data = cur.fetchall()
    conn.close()

    if not cat_data:
        print(f"❌ No expense data found for {month_input}!")
        return

    categories = [r[0] for r in cat_data]
    amounts    = [r[1] for r in cat_data]
    total      = sum(amounts)

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f"Expense Analysis — {month_input}", fontsize=15, fontweight="bold")

    # Pie chart
    colors = plt.cm.Set3.colors[:len(categories)]
    ax1.pie(amounts, labels=categories, autopct="%1.1f%%", colors=colors, startangle=90)
    ax1.set_title("Expense Distribution")

    # Bar chart
    bars = ax2.bar(categories, amounts, color=colors)
    ax2.set_title("Spending by Category")
    ax2.set_ylabel("Amount (₹)")
    ax2.tick_params(axis="x", rotation=30)
    for bar, amt in zip(bars, amounts):
        ax2.text(bar.get_x() + bar.get_width() / 2,
                 amt + total * 0.01,
                 f"₹{amt:.0f}", ha="center", va="bottom", fontsize=8)

    # Line chart – daily trend
    if daily_data:
        dates  = [r[0] for r in daily_data]
        damts  = [r[1] for r in daily_data]
        ax3.plot(dates, damts, marker="o", color="#E74C3C", linewidth=2, markersize=5)
        ax3.set_title("Daily Spending Trend")
        ax3.set_ylabel("Amount (₹)")
        ax3.tick_params(axis="x", rotation=30)
        ax3.grid(True, alpha=0.3)
        # Fill area under the curve
        ax3.fill_between(dates, damts, alpha=0.15, color="#E74C3C")
    else:
        ax3.text(0.5, 0.5, "No daily data", ha="center", va="center", transform=ax3.transAxes)
        ax3.set_title("Daily Spending Trend")

    # Summary statistics panel
    ax4.axis("off")
    max_cat = max(cat_data, key=lambda x: x[1])
    min_cat = min(cat_data, key=lambda x: x[1])
    summary = (
        f"📊  SUMMARY — {month_input}\n"
        f"{'─'*32}\n"
        f"  Total Spending   : ₹{total:.2f}\n"
        f"  No. of Categories: {len(categories)}\n"
        f"  Avg per Category : ₹{total/len(categories):.2f}\n\n"
        f"  🔴 Highest  : {max_cat[0]}\n"
        f"             ₹{max_cat[1]:.2f} ({max_cat[1]/total*100:.1f}%)\n\n"
        f"  🟢 Lowest   : {min_cat[0]}\n"
        f"             ₹{min_cat[1]:.2f} ({min_cat[1]/total*100:.1f}%)"
    )
    ax4.text(0.05, 0.95, summary, transform=ax4.transAxes,
             fontsize=10, verticalalignment="top", family="monospace",
             bbox=dict(boxstyle="round,pad=0.6", facecolor="#FEF9E7", alpha=0.8))

    plt.tight_layout()
    plt.show()
    print("✅ Charts generated successfully!")


# ── Feature 8 – Export CSV ────────────────────────────────────────────────────
def export_report():
    divider("💾 EXPORT REPORT TO CSV")

    user_id = get_user_id(CURRENT_USER)

    os.makedirs("reports", exist_ok=True)

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        SELECT e.date, c.category_name, e.amount, e.description
        FROM expenses e
        JOIN categories c ON e.category_id = c.category_id
        WHERE e.user_id = ?
        ORDER BY e.date DESC
    """, (user_id,))
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("❌ No expenses to export!")
        return

    filename = f"reports/expense_report_{CURRENT_USER}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    if pd is not None:
        df = pd.DataFrame(rows, columns=["Date", "Category", "Amount (₹)", "Description"])
        df.to_csv(filename, index=False, encoding="utf-8")
        total = df["Amount (₹)"].sum()
        count = len(df)
    else:
        import csv
        with open(filename, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Date", "Category", "Amount (₹)", "Description"])
            w.writerows(rows)
        total = sum(r[2] for r in rows)
        count = len(rows)

    print(f"✅ Report exported  : {filename}")
    print(f"   Total records   : {count}")
    print(f"   Total amount    : ₹{total:.2f}")


# ── Authentication loop ───────────────────────────────────────────────────────
def auth_loop():
    while True:
        print("\n🔐 AUTHENTICATION")
        print("1. Login")
        print("2. Register")
        print("3. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            if login_user():
                return True
        elif choice == "2":
            register_user()
        elif choice == "3":
            return False
        else:
            print("❌ Invalid choice! Enter 1, 2, or 3.")


# ── Main menu ─────────────────────────────────────────────────────────────────
def main_menu():
    global CURRENT_USER

    init_database()

    print("\n" + "=" * 50)
    print("  💰  PERSONAL EXPENSE TRACKER  💰")
    print("=" * 50)

    # Keep looping until a user is logged in or user chooses Exit
    while not CURRENT_USER:
        if not auth_loop():
            print("👋 Goodbye!")
            return

    # Inner app loop
    while True:
        print("\n" + "=" * 50)
        print(f"  📊  MAIN MENU  (👤 {CURRENT_USER})")
        print("=" * 50)
        print("  1. Record New Expense")
        print("  2. View All Expenses")
        print("  3. Monthly Spending Summary")
        print("  4. Search by Date Range")
        print("  5. Search by Category")
        print("  6. Budget Tracking")
        print("  7. Generate Charts")
        print("  8. Export Report (CSV)")
        print("  9. Logout")
        print(" 10. Exit")

        choice = input("\nSelect an option: ").strip()

        if   choice == "1":  record_expense()
        elif choice == "2":  view_all_expenses()
        elif choice == "3":  monthly_summary()
        elif choice == "4":  search_by_date_range()
        elif choice == "5":  search_by_category()
        elif choice == "6":  budget_tracking()
        elif choice == "7":  generate_chart()
        elif choice == "8":  export_report()
        elif choice == "9":
            print(f"✅ Logged out. Goodbye, {CURRENT_USER}!")
            CURRENT_USER = None
            # Go back to auth screen
            if not auth_loop():
                print("👋 Goodbye!")
                return
        elif choice == "10":
            print("👋 Thank you for using Personal Expense Tracker!")
            break
        else:
            print("❌ Invalid choice! Enter a number from 1 to 10.")


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main_menu()