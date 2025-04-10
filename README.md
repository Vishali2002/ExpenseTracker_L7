# Expense Tracker Application

## Overview

The Expense Tracker is a web application built using Flask and MySQL that allows users to manage their expenses, set budgets, and view reports. Users can add expenses, categorize them, and track their spending against predefined budgets.

## Features

- **User Management**: Add and manage users.
- **Category Management**: Create and manage expense categories.
- **Expense Tracking**: Add expenses with associated categories and view all expenses.
- **Budget Management**: Set budgets for different categories and receive alerts when spending exceeds the budget.
- **Reporting**: Generate reports to view total spending.

## Technologies Used

- **Flask**: A lightweight WSGI web application framework for Python.
- **MySQL**: A relational database management system to store user and expense data.
- **PyMySQL**: A MySQL client library for Python.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set Up a Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:

   ```bash
   pip install flask pymysql
   ```

4. **Set Up the Database**:

   - Create a MySQL database named `expense_tracker`.
   - Run the following SQL commands to create the necessary tables:

   ```sql
   CREATE TABLE IF NOT EXISTS users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(50) NOT NULL,
       email VARCHAR(100) NOT NULL
   );

   CREATE TABLE IF NOT EXISTS categories (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(50) NOT NULL
   );

   CREATE TABLE IF NOT EXISTS expenses (
       id INT AUTO_INCREMENT PRIMARY KEY,
       user_id INT,
       category_id INT,
       amount DECIMAL(10, 2),
       date DATE,
       FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE,
       FOREIGN KEY (category_id) REFERENCES categories(id) ON UPDATE CASCADE ON DELETE CASCADE
   );

   CREATE TABLE IF NOT EXISTS budgets (
       id INT AUTO_INCREMENT PRIMARY KEY,
       user_id INT,
       category_id INT,
       month INT,
       year INT,
       amount DECIMAL(10, 2),
       FOREIGN KEY (user_id) REFERENCES users(id),
       FOREIGN KEY (category_id) REFERENCES categories(id)
   );
   ```

## Usage

1. **Run the Application**:

   ```bash
   python app.py
   ```

2. **Access the Application**:

   Open your web browser and navigate to `http://127.0.0.1:5000`.

3. **Commands**:

   - **Add User**: `add user`
   - **Add Category**: `add category`
   - **Add Expense**: `add expense`
   - **View Expenses**: `view expenses`
   - **Exit**: `exit`

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.

