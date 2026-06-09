# 🚀 GitHub Setup Guide - Personal Expense Tracker

## Step-by-Step Instructions to Push Your Project to GitHub

---

## STEP 1: Create GitHub Account (If you don't have one)

1. Go to https://github.com
2. Click "Sign up"
3. Enter email, create password, and username
4. Verify your email
5. Complete setup

---

## STEP 2: Create a New Repository on GitHub

1. **Login to GitHub** with your credentials
2. **Click the "+" icon** (top-right corner)
3. **Select "New repository"**
4. **Fill in the details:**
   - Repository name: `Personal-Expense-Tracker`
   - Description: `A Python application to track personal expenses with SQLite database and data visualization`
   - Choose **Public** (required for submission)
   - ✅ Check "Add a README file" (Optional - we have our own)
   - ✅ Check "Add .gitignore" (Optional - we have our own)
   - Click **Create repository**

5. **Copy the repository URL** (you'll need this in next steps)
   Example: `https://github.com/YOUR_USERNAME/Personal-Expense-Tracker.git`

---

## STEP 3: Install Git on Your Computer

### On Windows:
1. Download from https://git-scm.com/download/win
2. Run installer with default options
3. Restart your computer

### On macOS:
```bash
brew install git
```

### On Linux:
```bash
sudo apt-get install git
```

---

## STEP 4: Configure Git Locally

Open terminal/command prompt and run:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Replace with your actual name and email (use the same email as GitHub account).

---

## STEP 5: Prepare Your Project Files

Create a folder for your project:

```bash
mkdir Personal-Expense-Tracker
cd Personal-Expense-Tracker
```

Copy these 4 files into this folder:
1. `expense_tracker.py` (main application)
2. `requirements.txt` (dependencies)
3. `README.md` (documentation)
4. `.gitignore` (git configuration)

---

## STEP 6: Initialize Git Repository Locally

In your project folder, run:

```bash
git init
```

This creates a hidden `.git` folder.

---

## STEP 7: Add Files to Git

```bash
git add .
```

This stages all files for commit.

**Verify what's being added:**
```bash
git status
```

You should see all 4 files listed in green.

---

## STEP 8: Create First Commit

```bash
git commit -m "Initial commit: Complete Personal Expense Tracker application"
```

The message describes what you're committing.

---

## STEP 9: Connect to GitHub Repository

```bash
git remote add origin https://github.com/YOUR_USERNAME/Personal-Expense-Tracker.git
```

Replace `YOUR_USERNAME` with your actual GitHub username.

**Verify connection:**
```bash
git remote -v
```

---

## STEP 10: Push to GitHub

```bash
git branch -M main
git push -u origin main
```

This uploads your code to GitHub. You may be asked for GitHub credentials.

---

## STEP 11: Verify on GitHub

1. Go to https://github.com/YOUR_USERNAME/Personal-Expense-Tracker
2. Check if all files are visible:
   - ✅ expense_tracker.py
   - ✅ requirements.txt
   - ✅ README.md
   - ✅ .gitignore

---

## STEP 12: Making Updates (If needed)

If you need to update your code later:

```bash
# Make changes to files
git add .
git commit -m "Description of changes made"
git push origin main
```

---

## Complete Commands Cheat Sheet

```bash
# One-time setup
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# For each new project
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/USERNAME/REPO.git
git branch -M main
git push -u origin main

# For future updates
git add .
git commit -m "Update message"
git push origin main

# Check status
git status
git log
```

---

## Troubleshooting

### Error: "fatal: not a git repository"
**Solution:** Make sure you're in the project folder and ran `git init`

### Error: "Authentication failed"
**Solution:** 
- For HTTPS: Use GitHub Personal Access Token instead of password
  - Go to GitHub → Settings → Developer settings → Personal access tokens
  - Generate new token and use it as password
- For SSH: Set up SSH keys (more advanced)

### Error: "Repository already exists"
**Solution:** Delete the `.git` folder and start over
```bash
rm -rf .git
git init
```

### Files not showing on GitHub
**Solution:**
1. Check `git status` shows your files
2. Verify `.gitignore` isn't excluding them
3. Run `git push origin main` again

---

## Final Checklist Before Submission

- [ ] Repository created on GitHub
- [ ] Repository is PUBLIC
- [ ] All 4 files pushed to GitHub
- [ ] README.md is visible and readable
- [ ] expense_tracker.py is present
- [ ] requirements.txt is present
- [ ] Application runs locally without errors
- [ ] Repository link is ready for submission
- [ ] Last commit message is descriptive

---

## Repository Link Format for Submission

When submitting, provide link in this format:
```
https://github.com/YOUR_USERNAME/Personal-Expense-Tracker
```

Example:
```
https://github.com/john_doe/Personal-Expense-Tracker
```

---

## Additional GitHub Features to Use

### Star your own repo (optional)
Click the Star ⭐ button to bookmark it

### Add topics
On repository page → About section → Add topics:
- python
- expense-tracker
- sqlite
- data-visualization

### Create a release (optional)
- Go to Releases → Create new release
- Tag: v1.0
- Title: Personal Expense Tracker v1.0
- Add release notes

---

## Quick Start Command Sequence

If you want to do everything in order without explanations:

```bash
# Configure Git (one time only)
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Create and setup project folder
mkdir Personal-Expense-Tracker
cd Personal-Expense-Tracker

# Copy the 4 files here: expense_tracker.py, requirements.txt, README.md, .gitignore

# Initialize and push
git init
git add .
git commit -m "Initial commit: Personal Expense Tracker"
git remote add origin https://github.com/YOUR_USERNAME/Personal-Expense-Tracker.git
git branch -M main
git push -u origin main

# View on GitHub
# Visit: https://github.com/YOUR_USERNAME/Personal-Expense-Tracker
```

---

## Need Help?

- GitHub Help: https://docs.github.com
- Git Documentation: https://git-scm.com/doc
- Stack Overflow: https://stackoverflow.com (search for your error)

---

**You're all set! Your project is now on GitHub and ready for submission! 🎉**
