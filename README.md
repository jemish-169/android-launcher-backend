DEPLOYMENT INSTRUCTIONS:

1. Install Python 3.10 or higher
2. Install dependencies:
   pip install -r requirements.txt

3. Run the development server:
   uvicorn main:app --reload --host 0.0.0.0 --port 8000

4. For production deployment:
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

API USAGE:

POST /generate
- Upload JSON configuration file as multipart/form-data
- Returns ZIP file containing complete Android Studio project
- Content-Type: multipart/form-data
- Response: application/zip

GET /health
- Health check endpoint
- Returns: {"status": "healthy", "message": "Android Project Generator is running"}

FEATURES SUPPORTED:
✅ Jetpack Compose & XML Views
✅ Kotlin & Java language support
✅ Multiple build systems (Gradle, Gradle KTS)
✅ Dependency injection (Hilt, Koin)
✅ Networking libraries (Retrofit, Ktor)
✅ Serialization (Gson, Moshi, Kotlinx.serialization)
✅ Local storage (DataStore, SharedPreferences)
✅ Room database support
✅ Material Design themes (Material 2, Material 3)
✅ Custom theme colors and typography
✅ Internationalization support
✅ Light/Dark theme support
✅ Android permissions configuration
✅ HTTP networking with security config
✅ Navigation components
✅ ViewBinding support
✅ Version catalogs (libs.versions.toml)

The generator creates a fully functional Android Studio project that can be imported and built immediately.