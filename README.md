# =========================================
# Django Healthcare Backend Setup Script
# =========================================

echo "--------------------------------------"
echo "🚀 Django Healthcare Backend Setup"
echo "--------------------------------------"

# 1. Clone the repository
read -p "Enter your GitHub repo URL: " REPO_URL
read -p "Enter local folder name for the repo: " REPO_NAME

git clone "$REPO_URL" "$REPO_NAME" || { echo "Failed to clone repo"; exit 1; }
cd "$REPO_NAME" || { echo "Folder not found"; exit 1; }

# 2. Create a virtual environment
python3 -m venv venv || { echo "Failed to create virtual environment"; exit 1; }

# 3. Activate the virtual environment
source venv/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }

# 4. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt || { echo "Failed to install dependencies"; exit 1; }

# 5. Create .env file
echo "Creating .env file..."
cat <<EOL > .env
DB_NAME=your_db_name
DB_USER=your_db_username
DB_PASSWORD=YOUR_PASSWORD_HERE   # Replace with your PostgreSQL password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your_django_secret_key
EOL
echo ".env file created. ⚠️ Replace placeholders with your own credentials."

# 6. Apply Django migrations
python manage.py makemigrations
python manage.py migrate

# 7. Run the server
echo "Starting Django development server..."
python manage.py runserver

echo "--------------------------------------"
echo "✅ Setup Complete!"
echo "Server running at http://127.0.0.1:8000/"
echo "Use Postman to test the APIs. Remember to replace .env placeholders with your credentials."
echo "--------------------------------------"
