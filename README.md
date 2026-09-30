# Office Expense and Attendance System

This project is a Django-based employee office management system.
It helps employees and managers track attendance, leave requests, swipe requests, and expenses.
Employees can view their information and submit requests, while managers can review records and approvals.
The project also includes authentication, profiles, quick information pages, and attendance photo support.
It uses SQLite for local development and stores uploaded media in the `media` folder.

## How to run

From the repository folder, create and activate a virtual environment, run `pip install -r requirements.txt`, then enter `Employee_attendance_system` and run `python manage.py migrate` followed by `python manage.py runserver`.
Open http://127.0.0.1:8000/ in your browser.
