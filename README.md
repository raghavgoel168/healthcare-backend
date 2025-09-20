# 🚀 Django Healthcare Backend Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/raghavgoel168/healthcare-backend.git
   cd healthcare-backend
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate         # Windows
   ```

3. Install Dependencies
   ```bash
   pip install -r requirements.txt
   ```


4. Configure Environment Variables
- Create a .env file in the project root with the following placeholders:
   ```bash
   DB_NAME=your_db_name
   DB_USER=your_db_username
   DB_PASSWORD=YOUR_PASSWORD_HERE    # Replace with your PostgreSQL password
   DB_HOST=localhost
   DB_PORT=5432
   SECRET_KEY=your_django_secret_key
   ```

5. Apply Migrations
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Run the Server
   ```bash
   python manage.py runserver
   ```


--------------------------------------
✅ Setup Complete!
- Server running at http://127.0.0.1:8000/
- Use Postman to test the APIs. Remember to replace .env placeholders with your credentials.
--------------------------------------
