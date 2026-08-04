# Flask API

A modular, production-ready Flask application template.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy the environment file and configure variables:
   ```bash
   cp .env.example .env
   ```
5. Apply database migrations:
   ```bash
   flask db upgrade
   ```
6. Run the application:
   ```bash
   python run.py
   ```

## Database Migrations

To generate a new migration after modifying models:
```bash
flask db migrate -m "Description of changes"
flask db upgrade
```
