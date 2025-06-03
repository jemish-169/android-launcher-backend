import os
import tempfile
import shutil
import zipfile
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from .utils import ProjectUtils

class AndroidProjectBuilder:
    """Main builder class for generating Android projects"""
    
    def __init__(self, config: dict):
        self.config = config
        self.project_config = config['project']
        self.app_config = config['configuration']
        self.utils = ProjectUtils()
        
        # Setup Jinja2 environment
        template_dir = Path(__file__).parent / 'templates'
        template_dir.mkdir(exist_ok=True)
        self.jinja_env = Environment(loader=FileSystemLoader(str(template_dir)))
        
        # Create templates directory and files if they don't exist
        self._create_default_templates()
    
    def _create_default_templates(self):
        """Create default templates if they don't exist"""
        templates_dir = Path(__file__).parent / 'templates'
        templates_dir.mkdir(exist_ok=True)
        
        # Create template files with basic content
        template_files = {
            'build_gradle.j2': self._get_build_gradle_template(),
            'build_gradle_kts.j2': self._get_build_gradle_kts_template(),
            'settings_gradle.j2': self._get_settings_gradle_template(),
            'settings_gradle_kts.j2': self._get_settings_gradle_kts_template(),
            'libs_versions_toml.j2': self._get_libs_versions_toml_template(),
            'app_build_gradle.j2': self._get_app_build_gradle_template(),
            'app_build_gradle_kts.j2': self._get_app_build_gradle_kts_template(),
            'android_manifest.j2': self._get_android_manifest_template(),
            'main_activity_kotlin.j2': self._get_main_activity_kotlin_template(),
            'main_activity_java.j2': self._get_main_activity_java_template(),
            'strings_xml.j2': self._get_strings_xml_template(),
            'colors_xml.j2': self._get_colors_xml_template(),
            'themes_xml.j2': self._get_themes_xml_template(),
            'network_config_xml.j2': self._get_network_config_xml_template(),
            'compose_theme.j2': self._get_compose_theme_template(),
            'activity_main_xml.j2': self._get_activity_main_xml_template(),
            'gradle_properties.j2': self._get_gradle_properties_template(),
        }
        
        for filename, content in template_files.items():
            template_path = templates_dir / filename
            if not template_path.exists():
                with open(template_path, 'w', encoding='utf-8') as f:
                    f.write(content)
    
    def build(self) -> str:
        """Build the Android project and return ZIP file path"""
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir) / self.utils.sanitize_project_name(self.project_config['name'])
            
            # Create project structure
            self._create_project_structure(project_dir)
            
            # Generate files
            self._generate_root_files(project_dir)
            self._generate_app_files(project_dir)
            
            # Create ZIP file
            zip_path = tempfile.mktemp(suffix='.zip')
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(project_dir):
                    for file in files:
                        file_path = Path(root) / file
                        archive_name = file_path.relative_to(project_dir.parent)
                        zipf.write(file_path, archive_name)
            
            return zip_path
    
    def _create_project_structure(self, project_dir: Path):
        """Create the basic Android project directory structure"""
        package_path = self.utils.package_to_path(self.project_config['package'])
        language_dir = 'kotlin' if self.app_config['language'] == 'kotlin' else 'java'
        
        directories = [
            'app/src/main',
            f'app/src/main/{language_dir}/{package_path}',
            'app/src/main/res/layout',
            'app/src/main/res/values',
            'app/src/main/res/values-night',
            'app/src/main/res/drawable',
            'app/src/main/res/mipmap-hdpi',
            'app/src/main/res/mipmap-mdpi',
            'app/src/main/res/mipmap-xhdpi',
            'app/src/main/res/mipmap-xxhdpi',
            'app/src/main/res/mipmap-xxxhdpi',
            'app/src/main/res/xml',
            'gradle/wrapper'
        ]
        
        # Add internationalization directories
        if self.app_config.get('internationalization', {}).get('enabled'):
            for lang in self.app_config['internationalization'].get('languages', []):
                if lang != 'en':
                    directories.append(f'app/src/main/res/values-{lang}')
        
        # Add compose theme directory if using Jetpack Compose
        if self.app_config.get('uiToolkit') == 'jetpack-compose':
            directories.append(f'app/src/main/{language_dir}/{package_path}/ui/theme')
        
        self.utils.create_directories(project_dir, directories)
    
    def _generate_root_files(self, project_dir: Path):
        """Generate root-level project files"""
        build_format = self.app_config.get('buildFormat', 'gradle')
        
        # Generate build.gradle or build.gradle.kts
        if build_format == 'kts':
            template = self.jinja_env.get_template('build_gradle_kts.j2')
            self.utils.write_file(project_dir / 'build.gradle.kts', template.render(config=self.config))
            
            template = self.jinja_env.get_template('settings_gradle_kts.j2')
            self.utils.write_file(project_dir / 'settings.gradle.kts', template.render(config=self.config))
        else:
            template = self.jinja_env.get_template('build_gradle.j2')
            self.utils.write_file(project_dir / 'build.gradle', template.render(config=self.config))
            
            template = self.jinja_env.get_template('settings_gradle.j2')
            self.utils.write_file(project_dir / 'settings.gradle', template.render(config=self.config))
        
        # Generate libs.versions.toml if enabled
        if self.app_config.get('useLibsVersionsToml', False):
            template = self.jinja_env.get_template('libs_versions_toml.j2')
            self.utils.write_file(project_dir / 'gradle/libs.versions.toml', template.render(config=self.config))
        
        # Generate gradle.properties
        template = self.jinja_env.get_template('gradle_properties.j2')
        self.utils.write_file(project_dir / 'gradle.properties', template.render(config=self.config))
    
    def _generate_app_files(self, project_dir: Path):
        """Generate app-level files"""
        app_dir = project_dir / 'app'
        build_format = self.app_config.get('buildFormat', 'gradle')
        
        # Generate app build.gradle
        if build_format == 'kts':
            template = self.jinja_env.get_template('app_build_gradle_kts.j2')
            self.utils.write_file(app_dir / 'build.gradle.kts', template.render(config=self.config))
        else:
            template = self.jinja_env.get_template('app_build_gradle.j2')
            self.utils.write_file(app_dir / 'build.gradle', template.render(config=self.config))
        
        # Generate AndroidManifest.xml
        permissions = self.utils.get_permission_manifest_entries(self.app_config.get('permissions', []))
        template = self.jinja_env.get_template('android_manifest.j2')
        manifest_context = {
            'config': self.config,
            'permissions': permissions,
            'use_network_config': self.app_config.get('httpNetworking', False)
        }
        self.utils.write_file(app_dir / 'src/main/AndroidManifest.xml', template.render(**manifest_context))
        
        # Generate MainActivity
        package_path = self.utils.package_to_path(self.project_config['package'])
        language_dir = 'kotlin' if self.app_config['language'] == 'kotlin' else 'java'
        
        if self.app_config['language'] == 'kotlin':
            template = self.jinja_env.get_template('main_activity_kotlin.j2')
            self.utils.write_file(
                app_dir / f'src/main/{language_dir}/{package_path}/MainActivity.kt',
                template.render(config=self.config)
            )
        else:
            template = self.jinja_env.get_template('main_activity_java.j2')
            self.utils.write_file(
                app_dir / f'src/main/{language_dir}/{package_path}/MainActivity.java',
                template.render(config=self.config)
            )
        
        # Generate resources
        self._generate_resources(app_dir)
        
        # Generate Compose theme if using Jetpack Compose
        if self.app_config.get('uiToolkit') == 'jetpack-compose':
            self._generate_compose_theme(app_dir, package_path, language_dir)
    
    def _generate_resources(self, app_dir: Path):
        """Generate resource files"""
        res_dir = app_dir / 'src/main/res'
        
        # Generate strings.xml
        template = self.jinja_env.get_template('strings_xml.j2')
        self.utils.write_file(res_dir / 'values/strings.xml', template.render(config=self.config))
        
        # Generate internationalization strings
        if self.app_config.get('internationalization', {}).get('enabled'):
            for lang in self.app_config['internationalization'].get('languages', []):
                if lang != 'en':
                    self.utils.write_file(
                        res_dir / f'values-{lang}/strings.xml',
                        template.render(config=self.config, language=lang)
                    )
        
        # Generate colors.xml
        template = self.jinja_env.get_template('colors_xml.j2')
        self.utils.write_file(res_dir / 'values/colors.xml', template.render(config=self.config))
        
        # Generate themes.xml
        template = self.jinja_env.get_template('themes_xml.j2')
        self.utils.write_file(res_dir / 'values/themes.xml', template.render(config=self.config))
        
        if self.app_config.get('themes', {}).get('lightDark', False):
            self.utils.write_file(res_dir / 'values-night/themes.xml', template.render(config=self.config, is_dark=True))
        
        # Generate network_security_config.xml if HTTP networking is enabled
        if self.app_config.get('httpNetworking', False):
            template = self.jinja_env.get_template('network_config_xml.j2')
            self.utils.write_file(res_dir / 'xml/network_security_config.xml', template.render(config=self.config))
        
        # Generate activity_main.xml if using XML views
        if self.app_config.get('uiToolkit') != 'jetpack-compose':
            template = self.jinja_env.get_template('activity_main_xml.j2')
            self.utils.write_file(res_dir / 'layout/activity_main.xml', template.render(config=self.config))
    
    def _generate_compose_theme(self, app_dir: Path, package_path: str, language_dir: str):
        """Generate Jetpack Compose theme files"""
        theme_dir = app_dir / f'src/main/{language_dir}/{package_path}/ui/theme'
        
        template = self.jinja_env.get_template('compose_theme.j2')
        
        # Generate Theme.kt
        if self.app_config['language'] == 'kotlin':
            self.utils.write_file(theme_dir / 'Theme.kt', template.render(config=self.config, file_type='theme'))
            self.utils.write_file(theme_dir / 'Color.kt', template.render(config=self.config, file_type='color'))
            self.utils.write_file(theme_dir / 'Type.kt', template.render(config=self.config, file_type='type'))
    
    # Template content methods
    def _get_build_gradle_template(self):
        return '''plugins {
    id 'com.android.application' version '8.2.0' apply false
    id 'org.jetbrains.kotlin.android' version '1.9.0' apply false
{% if config.configuration.dependencyInjection == 'hilt' %}
    id 'com.google.dagger.hilt.android' version '2.48' apply false
{% endif %}
}'''

    def _get_build_gradle_kts_template(self):
        return '''plugins {
    id("com.android.application") version "8.2.0" apply false
    id("org.jetbrains.kotlin.android") version "1.9.0" apply false
{% if config.configuration.dependencyInjection == 'hilt' %}
    id("com.google.dagger.hilt.android") version "2.48" apply false
{% endif %}
}'''

    def _get_settings_gradle_template(self):
        return '''pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "{{ config.project.name }}"
include ':app'
'''

    def _get_settings_gradle_kts_template(self):
        return '''pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "{{ config.project.name }}"
include(":app")
'''

    def _get_libs_versions_toml_template(self):
        return '''[versions]
agp = "8.2.0"
kotlin = "1.9.0"
coreKtx = "1.12.0"
lifecycleRuntimeKtx = "2.7.0"
activityCompose = "1.8.2"
composeBom = "2023.10.01"
{% if config.configuration.dependencyInjection == 'hilt' %}
hilt = "2.48"
{% endif %}
{% if config.configuration.networking == 'retrofit' %}
retrofit = "2.9.0"
{% elif config.configuration.networking == 'ktor' %}
ktor = "2.3.7"
{% endif %}

[libraries]
androidx-core-ktx = { group = "androidx.core", name = "core-ktx", version.ref = "coreKtx" }
androidx-lifecycle-runtime-ktx = { group = "androidx.lifecycle", name = "lifecycle-runtime-ktx", version.ref = "lifecycleRuntimeKtx" }
{% if config.configuration.uiToolkit == 'jetpack-compose' %}
androidx-activity-compose = { group = "androidx.activity", name = "activity-compose", version.ref = "activityCompose" }
androidx-compose-bom = { group = "androidx.compose", name = "compose-bom", version.ref = "composeBom" }
androidx-ui = { group = "androidx.compose.ui", name = "ui" }
androidx-ui-graphics = { group = "androidx.compose.ui", name = "ui-graphics" }
androidx-ui-tooling = { group = "androidx.compose.ui", name = "ui-tooling" }
androidx-ui-tooling-preview = { group = "androidx.compose.ui", name = "ui-tooling-preview" }
androidx-ui-test-manifest = { group = "androidx.compose.ui", name = "ui-test-manifest" }
androidx-material3 = { group = "androidx.compose.material3", name = "material3" }
{% endif %}

[plugins]
androidApplication = { id = "com.android.application", version.ref = "agp" }
jetbrainsKotlinAndroid = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
{% if config.configuration.dependencyInjection == 'hilt' %}
hiltAndroid = { id = "com.google.dagger.hilt.android", version.ref = "hilt" }
{% endif %}
'''

    def _get_app_build_gradle_template(self):
        return '''plugins {
    id 'com.android.application'
{% if config.configuration.language == 'kotlin' %}
    id 'org.jetbrains.kotlin.android'
{% endif %}
{% if config.configuration.dependencyInjection == 'hilt' %}
    id 'com.google.dagger.hilt.android'
    id 'kotlin-kapt'
{% endif %}
{% if config.configuration.serialization == 'kotlinx.serialization' %}
    id 'org.jetbrains.kotlin.plugin.serialization'
{% endif %}
}

android {
    namespace '{{ config.project.package }}'
    compileSdk {{ config.project.compileSdk }}

    defaultConfig {
        applicationId "{{ config.project.package }}"
        minSdk {{ config.project.minSdk }}
        targetSdk {{ config.project.targetSdk }}
        versionCode 1
        versionName "1.0"

        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
{% if config.configuration.uiToolkit == 'jetpack-compose' %}
        vectorDrawables {
            useSupportLibrary true
        }
{% endif %}
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_{{ config.configuration.javaVersion }}
        targetCompatibility JavaVersion.VERSION_{{ config.configuration.javaVersion }}
    }
{% if config.configuration.language == 'kotlin' %}
    kotlinOptions {
        jvmTarget = '{{ config.configuration.javaVersion }}'
    }
{% endif %}
{% if config.configuration.uiToolkit == 'jetpack-compose' %}
    buildFeatures {
        compose true
    }
    composeOptions {
        kotlinCompilerExtensionVersion '1.5.4'
    }
    packaging {
        resources {
            excludes += '/META-INF/{AL2.0,LGPL2.1}'
        }
    }
{% endif %}
{% if config.configuration.viewBinding %}
    buildFeatures {
        viewBinding true
    }
{% endif %}
}

dependencies {
    implementation 'androidx.core:core-ktx:1.12.0'
    implementation 'androidx.lifecycle:lifecycle-runtime-ktx:2.7.0'
    
{% if config.configuration.uiToolkit == 'jetpack-compose' %}
    implementation 'androidx.activity:activity-compose:1.8.2'
    implementation platform('androidx.compose:compose-bom:2023.10.01')
    implementation 'androidx.compose.ui:ui'
    implementation 'androidx.compose.ui:ui-graphics'
    implementation 'androidx.compose.ui:ui-tooling-preview'
{% if config.configuration.uiTheme == 'material3' %}
    implementation 'androidx.compose.material3:material3'
{% else %}
    implementation 'androidx.compose.material:material'
{% endif %}
{% else %}
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
{% endif %}

{% if config.configuration.networking == 'retrofit' %}
    implementation 'com.squareup.retrofit2:retrofit:2.9.0'
{% if config.configuration.serialization == 'gson' %}
    implementation 'com.squareup.retrofit2:converter-gson:2.9.0'
    implementation 'com.google.code.gson:gson:2.10.1'
{% elif config.configuration.serialization == 'moshi' %}
    implementation 'com.squareup.retrofit2:converter-moshi:2.9.0'
    implementation 'com.squareup.moshi:moshi-kotlin:1.14.0'
{% endif %}
{% elif config.configuration.networking == 'ktor' %}
    implementation 'io.ktor:ktor-client-android:2.3.7'
    implementation 'io.ktor:ktor-client-core:2.3.7'
{% if config.configuration.serialization == 'kotlinx.serialization' %}
    implementation 'io.ktor:ktor-serialization-kotlinx-json:2.3.7'
    implementation 'org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.0'
{% endif %}
{% endif %}

{% if config.configuration.dependencyInjection == 'hilt' %}
    implementation 'com.google.dagger:hilt-android:2.48'
    kapt 'com.google.dagger:hilt-compiler:2.48'
{% elif config.configuration.dependencyInjection == 'koin' %}
    implementation 'io.insert-koin:koin-android:3.5.0'
{% endif %}

{% if config.configuration.localStorage == 'datastore' %}
    implementation 'androidx.datastore:datastore-preferences:1.0.0'
{% endif %}

{% if config.configuration.enableRoom %}
    implementation 'androidx.room:room-runtime:2.6.1'
    implementation 'androidx.room:room-ktx:2.6.1'
{% if config.configuration.language == 'kotlin' %}
    kapt 'androidx.room:room-compiler:2.6.1'
{% else %}
    annotationProcessor 'androidx.room:room-compiler:2.6.1'
{% endif %}
{% endif %}

{% if config.configuration.navigation == 'compose-navigation' %}
    implementation 'androidx.navigation:navigation-compose:2.7.6'
{% elif config.configuration.navigation == 'jetpack-navigation' %}
    implementation 'androidx.navigation:navigation-fragment-ktx:2.7.6'
    implementation 'androidx.navigation:navigation-ui-ktx:2.7.6'
{% endif %}

    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
{% if config.configuration.uiToolkit == 'jetpack-compose' %}
    androidTestImplementation platform('androidx.compose:compose-bom:2023.10.01')
    androidTestImplementation 'androidx.compose.ui:ui-test-junit4'
    debugImplementation 'androidx.compose.ui:ui-tooling'
    debugImplementation 'androidx.compose.ui:ui-test-manifest'
{% endif %}
}
'''

    def _get_app_build_gradle_kts_template(self):
        return '''plugins {
    id("com.android.application")
{% if config.configuration.language == 'kotlin' %}
    id("org.jetbrains.kotlin.android")
{% endif %}
{% if config.configuration.dependencyInjection == 'hilt' %}
    id("com.google.dagger.hilt.android")
    id("kotlin-kapt")
{% endif %}
{% if config.configuration.serialization == 'kotlinx.serialization' %}
    id("org.jetbrains.kotlin.plugin.serialization")
{% endif %}
}

android {
    namespace = "{{ config.project.package }}"
    compileSdk = {{ config.project.compileSdk }}

    defaultConfig {
        applicationId = "{{ config.project.package }}"
        minSdk = {{ config.project.minSdk }}
        targetSdk = {{ config.project.targetSdk }}
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
{% if config.configuration.uiToolkit == 'jetpack-compose' %}
        vectorDrawables {
            useSupportLibrary = true
        }
{% endif %}
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_{{ config.configuration.javaVersion }}
        targetCompatibility = JavaVersion.VERSION_{{ config.configuration.javaVersion }}
    }
{% if config.configuration.language == 'kotlin' %}
    kotlinOptions {
        jvmTarget = "{{ config.configuration.javaVersion }}"
    }
{% endif %}
{% if config.configuration.uiToolkit == 'jetpack-compose' %}
    buildFeatures {
        compose = true
    }
    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.4"
    }
    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
{% endif %}
{% if config.configuration.viewBinding %}
    buildFeatures {
        viewBinding = true
    }
{% endif %}
}

dependencies {
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.7.0")
    
{% if config.configuration.uiToolkit == 'jetpack-compose' %}
    implementation("androidx.activity:activity-compose:1.8.2")
    implementation(platform("androidx.compose:compose-bom:2023.10.01"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
{% if config.configuration.uiTheme == 'material3' %}
    implementation("androidx.compose.material3:material3")
{% else %}
    implementation("androidx.compose.material:material")
{% endif %}
{% else %}
    implementation("androidx.appcompat:appcompat:1.6.1")
    implementation("com.google.android.material:material:1.11.0")
    implementation("androidx.constraintlayout:constraintlayout:2.1.4")
{% endif %}

{% if config.configuration.networking == 'retrofit' %}
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
{% if config.configuration.serialization == 'gson' %}
    implementation("com.squareup.retrofit2:converter-gson:2.9.0")
    implementation("com.google.code.gson:gson:2.10.1")
{% elif config.configuration.serialization == 'moshi' %}
    implementation("com.squareup.retrofit2:converter-moshi:2.9.0")
    implementation("com.squareup.moshi:moshi-kotlin:1.14.0")
{% endif %}
{% elif config.configuration.networking == 'ktor' %}
    implementation("io.ktor:ktor-client-android:2.3.7")
    implementation("io.ktor:ktor-client-core:2.3.7")
{% if config.configuration.serialization == 'kotlinx.serialization' %}
    implementation("io.ktor:ktor-serialization-kotlinx-json:2.3.7")
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.0")
{% endif %}
{% endif %}

{% if config.configuration.dependencyInjection == 'hilt' %}
    implementation("com.google.dagger:hilt-android:2.48")
    kapt("com.google.dagger:hilt-compiler:2.48")
{% elif config.configuration.dependencyInjection == 'koin' %}
    implementation("io.insert-koin:koin-android:3.5.0")
{% endif %}

{% if config.configuration.localStorage == 'datastore' %}
    implementation("androidx.datastore:datastore-preferences:1.0.0")
{% endif %}

{% if config.configuration.enableRoom %}
    implementation("androidx.room:room-runtime:2.6.1")
    implementation("androidx.room:room-ktx:2.6.1")
{% if config.configuration.language == 'kotlin' %}
    kapt("androidx.room:room-compiler:2.6.1")
{% else %}
    annotationProcessor("androidx.room:room-compiler:2.6.1")
{% endif %}
{% endif %}

{% if config.configuration.navigation == 'compose-navigation' %}
    implementation("androidx.navigation:navigation-compose:2.7.6")
{% elif config.configuration.navigation == 'jetpack-navigation' %}
    implementation("androidx.navigation:navigation-fragment-ktx:2.7.6")
    implementation("androidx.navigation:navigation-ui-ktx:2.7.6")
{% endif %}

    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
{% if config.configuration.uiToolkit == 'jetpack-compose' %}
    androidTestImplementation(platform("androidx.compose:compose-bom:2023.10.01"))
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")
    debugImplementation("androidx.compose.ui:ui-tooling")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
{% endif %}
}
'''

    def _get_android_manifest_template(self):
        return '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

{% for permission in permissions %}
    <uses-permission android:name="{{ permission }}" />
{% endfor %}

    <application
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{{ config.project.name.replace(' ', '') }}"
{% if use_network_config %}
        android:networkSecurityConfig="@xml/network_security_config"
{% endif %}
{% if config.configuration.dependencyInjection == 'hilt' %}
        android:name=".{{ config.project.name.replace(' ', '') }}Application"
{% endif %}
        tools:targetApi="31">
        <activity
            android:name=".MainActivity"
            android:exported="true"
{% if config.configuration.uiToolkit == 'jetpack-compose' %}
            android:theme="@style/Theme.{{ config.project.name.replace(' ', '') }}">
{% else %}
            android:theme="@style/Theme.{{ config.project.name.replace(' ', '') }}">
{% endif %}
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>'''

    def _get_main_activity_kotlin_template(self):
        return '''package {{ config.project.package }}

{% if config.configuration.dependencyInjection == 'hilt' %}
import dagger.hilt.android.AndroidEntryPoint
{% endif %}
import android.os.Bundle
{% if config.configuration.uiToolkit == 'jetpack-compose' %}
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import {{ config.project.package }}.ui.theme.{{ config.project.name.replace(' ', '') }}Theme
{% else %}
import androidx.appcompat.app.AppCompatActivity
{% endif %}

{% if config.configuration.dependencyInjection == 'hilt' %}
@AndroidEntryPoint
{% endif %}
{% if config.configuration.uiToolkit == 'jetpack-compose' %}
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            {{ config.project.name.replace(' ', '') }}Theme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    Greeting("Android")
                }
            }
        }
    }
}

@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(
        text = "Hello $name!",
        modifier = modifier
    )
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    {{ config.project.name.replace(' ', '') }}Theme {
        Greeting("Android")
    }
}
{% else %}
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }
}
{% endif %}
'''

    def _get_main_activity_java_template(self):
        return '''package {{ config.project.package }};

{% if config.configuration.dependencyInjection == 'hilt' %}
import dagger.hilt.android.AndroidEntryPoint;
{% endif %}
import android.os.Bundle;
{% if config.configuration.uiToolkit == 'jetpack-compose' %}
import androidx.activity.ComponentActivity;
import androidx.activity.compose.ComponentActivityKt;
import androidx.compose.foundation.layout.BoxKt;
import androidx.compose.material3.MaterialTheme;
import androidx.compose.material3.SurfaceKt;
import androidx.compose.material3.TextKt;
import androidx.compose.runtime.Composable;
import androidx.compose.ui.Modifier;
import androidx.compose.ui.tooling.preview.Preview;
{% else %}
import androidx.appcompat.app.AppCompatActivity;
{% endif %}

{% if config.configuration.dependencyInjection == 'hilt' %}
@AndroidEntryPoint
{% endif %}
{% if config.configuration.uiToolkit == 'jetpack-compose' %}
public class MainActivity extends ComponentActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        ComponentActivityKt.setContent(this, ComposableSingletons$MainActivityKt.INSTANCE.getLambda-1$app_debug(), null);
    }
}
{% else %}
public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }
}
{% endif %}
'''

    def _get_strings_xml_template(self):
        return '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{{ config.project.name }}</string>
{% if language is defined %}
    <!-- Localized strings for {{ language }} -->
{% endif %}
</resources>'''

    def _get_colors_xml_template(self):
        return '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
    
    <!-- Theme colors -->
    <color name="primary">{{ config.configuration.themeColors.primary }}</color>
    <color name="secondary">{{ config.configuration.themeColors.secondary }}</color>
    <color name="tertiary">{{ config.configuration.themeColors.tertiary }}</color>
    
    <!-- Additional colors -->
    <color name="primary_variant">#3700B3</color>
    <color name="secondary_variant">#018786</color>
    <color name="background">#FFFFFF</color>
    <color name="surface">#FFFFFF</color>
    <color name="error">#B00020</color>
    <color name="on_primary">#FFFFFF</color>
    <color name="on_secondary">#000000</color>
    <color name="on_background">#000000</color>
    <color name="on_surface">#000000</color>
    <color name="on_error">#FFFFFF</color>
</resources>'''

    def _get_themes_xml_template(self):
        return '''<?xml version="1.0" encoding="utf-8"?>
<resources xmlns:tools="http://schemas.android.com/tools">
    <!-- Base application theme. -->
{% if config.configuration.uiTheme == 'material3' %}
    <style name="Base.Theme.{{ config.project.name.replace(' ', '') }}" parent="Theme.Material3.DayNight.NoActionBar">
{% else %}
    <style name="Base.Theme.{{ config.project.name.replace(' ', '') }}" parent="Theme.Material3.DayNight">
{% endif %}
        <!-- Customize your light theme here. -->
        <item name="colorPrimary">@color/primary</item>
        <item name="colorSecondary">@color/secondary</item>
        <item name="colorTertiary">@color/tertiary</item>
    </style>

    <style name="Theme.{{ config.project.name.replace(' ', '') }}" parent="Base.Theme.{{ config.project.name.replace(' ', '') }}" />
{% if is_dark is defined and is_dark %}
    
    <!-- Dark theme colors -->
    <style name="Base.Theme.{{ config.project.name.replace(' ', '') }}" parent="Theme.Material3.DayNight.NoActionBar">
        <item name="android:colorBackground">#121212</item>
        <item name="colorSurface">#121212</item>
        <item name="colorOnSurface">#FFFFFF</item>
    </style>
{% endif %}
</resources>'''

    def _get_network_config_xml_template(self):
        return '''<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">localhost</domain>
        <domain includeSubdomains="true">10.0.2.2</domain>
    </domain-config>
</network-security-config>'''

    def _get_compose_theme_template(self):
        if self.config['configuration']['language'] == 'kotlin':
            if '{{ file_type }}' == 'theme':
                return '''package {{ config.project.package }}.ui.theme

import android.app.Activity
import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat

private val DarkColorScheme = darkColorScheme(
    primary = Purple80,
    secondary = PurpleGrey80,
    tertiary = Pink80
)

private val LightColorScheme = lightColorScheme(
    primary = Purple40,
    secondary = PurpleGrey40,
    tertiary = Pink40
)

@Composable
fun {{ config.project.name.replace(' ', '') }}Theme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }
        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }
    val view = LocalView.current
    if (!view.isInEditMode) {
        SideEffect {
            val window = (view.context as Activity).window
            window.statusBarColor = colorScheme.primary.toArgb()
            WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = darkTheme
        }
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
'''
            elif '{{ file_type }}' == 'color':
                return '''package {{ config.project.package }}.ui.theme

import androidx.compose.ui.graphics.Color

val Purple80 = Color(0xFFD0BCFF)
val PurpleGrey80 = Color(0xFFCCC2DC)
val Pink80 = Color(0xFFEFB8C8)

val Purple40 = Color(0xFF6650a4)
val PurpleGrey40 = Color(0xFF625b71)
val Pink40 = Color(0xFF7D5260)

// Custom theme colors
val Primary = Color({{ config.configuration.themeColors.primary | replace('#', '0xFF') }})
val Secondary = Color({{ config.configuration.themeColors.secondary | replace('#', '0xFF') }})
val Tertiary = Color({{ config.configuration.themeColors.tertiary | replace('#', '0xFF') }})
'''
            elif '{{ file_type }}' == 'type':
                return '''package {{ config.project.package }}.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
{% if config.configuration.typography.fontName != 'roboto' %}
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import {{ config.project.package }}.R
{% endif %}
import androidx.compose.ui.unit.sp

{% if config.configuration.typography.fontName != 'roboto' %}
val {{ config.configuration.typography.fontName.capitalize() }}FontFamily = FontFamily(
    Font(R.font.{{ config.configuration.typography.fontName.lower() }}_regular, FontWeight.Normal),
    Font(R.font.{{ config.configuration.typography.fontName.lower() }}_medium, FontWeight.Medium),
    Font(R.font.{{ config.configuration.typography.fontName.lower() }}_bold, FontWeight.Bold)
)
{% endif %}

val Typography = Typography(
    bodyLarge = TextStyle(
{% if config.configuration.typography.fontName != 'roboto' %}
        fontFamily = {{ config.configuration.typography.fontName.capitalize() }}FontFamily,
{% endif %}
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.5.sp
    )
)
'''
        return ''

    def _get_activity_main_xml_template(self):
        return '''<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>'''

    def _get_gradle_properties_template(self):
        return '''# Project-wide Gradle settings.
# IDE (e.g. Android Studio) users:
# Gradle settings configured through the IDE *will override*
# any settings specified in this file.
# For more details on how to configure your build environment visit
# http://www.gradle.org/docs/current/userguide/build_environment.html
# Specifies the JVM arguments used for the daemon process.
# The setting is particularly useful for tweaking memory settings.
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
# When configured, Gradle will run in incubating parallel mode.
# This option should only be used with decoupled projects. More details, visit
# http://www.gradle.org/docs/current/userguide/multi_project_builds.html#sec:decoupled_projects
# org.gradle.parallel=true
# AndroidX package structure to make it clearer which packages are bundled with the
# Android operating system, and which are packaged with your app's APK
# https://developer.android.com/topic/libraries/support-library/androidx-rn
android.useAndroidX=true
# Kotlin code style for this project: "official" or "obsolete":
kotlin.code.style=official
# Enables namespacing of each library's R class so that its R class includes only the
# resources declared in the library itself and none from the library's dependencies,
# thereby reducing the size of the R class for that library
android.nonTransitiveRClass=true
{% if config.configuration.viewBinding %}
android.enableViewBinding=true
{% endif %}
'''