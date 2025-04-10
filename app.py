from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql

app = Flask(__name__)
app.secret_key = 'key'  # Needed for flash messages

# Database configuration
db_config = {
    'user': 'root',
    'password': 'add your own',
    'host': '127.0.0.1',
    'database': 'expense_tracker'
}


def connect_to_mysql():
    return pymysql.connect(**db_config)


def create_tables(connection):
    with connection.cursor() as cursor:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            category_id INT,
            amount DECIMAL(10, 2),
            date DATE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON UPDATE CASCADE ON DELETE CASCADE
        );
        """)
        cursor.execute("""
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
        """)
    connection.commit()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

        conn = connect_to_mysql()
        try:
            with conn.cursor() as cursor:
                cursor.execute('INSERT INTO users (username, email) VALUES (%s, %s)', (username, email))
            conn.commit()
            flash("User added successfully!")
        except Exception as e:
            flash(f"Error: {e}")
        finally:
            conn.close()
        return redirect(url_for('index'))

    return render_template('add_user.html')


@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        user_id = request.form['user_id']
        category_id = request.form['category_id']
        amount = request.form['amount']
        date = request.form['date']
        month = int(date.split('-')[1])
        year = int(date.split('-')[0])

        conn = connect_to_mysql()
        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT id FROM users WHERE id = %s', (user_id,))
                if cursor.fetchone() is None:
                    flash("User does not exist.")
                    return redirect(url_for('add_expense'))

                cursor.execute('SELECT id FROM categories WHERE id = %s', (category_id,))
                if cursor.fetchone() is None:
                    flash("Category does not exist.")
                    return redirect(url_for('add_expense'))

                cursor.execute('INSERT INTO expenses (user_id, category_id, amount, date) VALUES (%s, %s, %s, %s)',
                               (user_id, category_id, amount, date))
            conn.commit()
            check_budget(conn, user_id, category_id, month, year)
            flash("Expense added successfully!")
        except Exception as e:
            flash(f"Error: {e}")
        finally:
            conn.close()
        return redirect(url_for('index'))

    return render_template('add_expense.html')


def check_budget(connection, user_id, category_id, month, year):
    with connection.cursor() as cursor:
        cursor.execute('SELECT amount FROM budgets WHERE user_id = %s AND category_id = %s AND month = %s AND year = %s',
                       (user_id, category_id, month, year))
        budget = cursor.fetchone()
        if budget:
            cursor.execute(
                'SELECT SUM(amount) FROM expenses WHERE user_id = %s AND category_id = %s AND MONTH(date) = %s AND YEAR(date) = %s',
                (user_id, category_id, month, year))
            total_spent = cursor.fetchone()[0] or 0

            if total_spent > budget[0]:
                flash("Alert: Budget exceeded!")
            elif total_spent > 0.9 * budget[0]:
                flash("Alert: Only 10% of your budget is left!")


@app.route('/view_expenses')
def view_expenses():
    conn = connect_to_mysql()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute('SELECT * FROM expenses')
            expenses = cursor.fetchall()
    finally:
        conn.close()
    return render_template('view_expenses.html', expenses=expenses)


@app.route('/set_budget', methods=['GET', 'POST'])
def set_budget_route():
    if request.method == 'POST':
        user_id = request.form['user_id']
        category_id = request.form['category_id']
        month = request.form['month']
        year = request.form['year']
        amount = request.form['amount']

        conn = connect_to_mysql()
        try:
            with conn.cursor() as cursor:
                cursor.execute('INSERT INTO budgets (user_id, category_id, month, year, amount) VALUES (%s, %s, %s, %s, %s)',
                               (user_id, category_id, month, year, amount))
            conn.commit()
            flash("Budget set successfully!")
        except Exception as e:
            flash(f"Error: {e}")
        finally:
            conn.close()
        return redirect(url_for('index'))

    return render_template('set_budget.html')


@app.route('/generate_report', methods=['GET', 'POST'])
def generate_report_route():
    if request.method == 'POST':
        user_id = request.form['user_id']
        month = request.form['month']
        year = request.form['year']

        conn = connect_to_mysql()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(
                    'SELECT c.name, SUM(e.amount) as total_spent FROM expenses e JOIN categories c ON e.category_id = c.id WHERE '
                    'e.user_id = %s AND MONTH(e.date) = %s AND YEAR(e.date) = %s GROUP BY c.name',
                    (user_id, month, year))
                report = cursor.fetchall()
        finally:
            conn.close()
        return render_template('report.html', report=report)

    return render_template('generate_report.html')


if __name__ == "__main__":
    conn = connect_to_mysql()
    create_tables(conn)
    conn.close()
    app.run(debug=True)
