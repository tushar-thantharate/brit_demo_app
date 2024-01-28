# Brit Demo App

This document provides instructions on setting up and running the Brint Demo App locally for development purposes.

## Prerequisites
Ensure that you have the following software installed on your machine:
- Python [3.10.12]
- Pip (Python package installer)
- Virtualenv

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-project.git
   cd brit_demo_app


2. Create a virtual environment:
   ```bash
    python -m venv brit_env
    source venv/bin/activate   # On Windows, use 'venv\Scripts\activate'

3. Install project dependencies:
    ```bash
    pip3 install -r requirements.txt

## Configuration (Provided with Code)
- Create configuration file (Other Environment- Staiging/Production):
  ```bash
  /brit_demo_app/brit/.env

- Update the .env file with your configuration settings:
  ```bash
  - Open the .env file in a text editor.
  - Add SECRET_KEY varaible name with a secure, random string.
  - Add DEBUG varaible name with True as value.
  - Configure other settings such as database credentials, API keys, etc., as needed.

## Database Setup
- Apply database migrations:
    ```bash
    python manage.py migrate

- Create a superuser (admin) for the Django admin interface:
    ```bash
    python manage.py createsuperuser

## Running the tests
- Run Unit tests:
    ```bash
    python manage.py test

## Running the Server
- Start the development server:
    ```bash
    python manage.py runserver

## Accessing the Application
- Open your web browser and navigate to http://localhost:8000.
- Access the Django admin interface at http://localhost:8000/admin using the superuser   credentials.

## Troubleshooting
If you encounter any issues during the setup, consider the following steps:
- Check the console for error messages and traceback.
- Ensure all dependencies are installed.
- Verify database settings in the .env file.
- Make sure the virtual environment is activated.