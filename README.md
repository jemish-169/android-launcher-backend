1. Install Python 3.10 or higher
2. Install dependencies:
   pip install -r requirements.txt
3. Run the development server:
   uvicorn main:app --reload --host 0.0.0.0 --port 8000

API USAGE:

POST /generate
- Upload JSON configuration file as multipart/form-data
- Returns ZIP file containing complete Android Studio project
- Content-Type: multipart/form-data
- Response: application/zip

GET /health
- Health check endpoint
- Returns: {"status": "healthy", "message": "Android Project Generator is running"}

The generator creates a fully functional Android Studio project that can be imported and built immediately.
