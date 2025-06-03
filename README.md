ANDROID PROJECT GENERATOR - FILE STRUCTURE

project_root/
├── main.py                          # FastAPI entry point
├── requirements.txt                 # Python dependencies
├── generator/
│   ├── __init__.py                 # Package initialization
│   ├── builder.py                  # Main project generation logic
│   ├── utils.py                    # Utility functions
│   └── templates/                  # Jinja2 templates directory
│       ├── build_gradle.j2         # Root build.gradle template
│       ├── build_gradle_kts.j2     # Root build.gradle.kts template
│       ├── settings_gradle.j2      # settings.gradle template
│       ├── settings_gradle_kts.j2  # settings.gradle.kts template
│       ├── libs_versions_toml.j2   # libs.versions.toml template
│       ├── app_build_gradle.j2     # App build.gradle template
│       ├── app_build_gradle_kts.j2 # App build.gradle.kts template
│       ├── android_manifest.j2     # AndroidManifest.xml template
│       ├── main_activity_kotlin.j2 # MainActivity.kt template
│       ├── main_activity_java.j2   # MainActivity.java template
│       ├── strings_xml.j2          # strings.xml template
│       ├── colors_xml.j2           # colors.xml template
│       ├── themes_xml.j2           # themes.xml template
│       ├── network_config_xml.j2   # network_security_config.xml template
│       ├── compose_theme.j2        # Compose theme files template
│       ├── activity_main_xml.j2    # activity_main.xml template
│       └── gradle_properties.j2    # gradle.properties template
└── output/                         # Temporary output directory (auto-created)

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