class GradleTemplates:
    """Handler for Gradle-related templates"""
    
    def __init__(self, config: dict):
        self.config = config
    
    def get_templates(self):
        """Return all Gradle template files"""
        return {
            'build_gradle.j2': self._get_build_gradle_template(),
            'build_gradle_kts.j2': self._get_build_gradle_kts_template(),
            'settings_gradle.j2': self._get_settings_gradle_template(),
            'settings_gradle_kts.j2': self._get_settings_gradle_kts_template(),
            'libs_versions_toml.j2': self._get_libs_versions_toml_template(),
            'app_build_gradle.j2': self._get_app_build_gradle_template(),
            'app_build_gradle_kts.j2': self._get_app_build_gradle_kts_template(),
            'gradle_properties.j2': self._get_gradle_properties_template(),
        }
    
    def _get_build_gradle_template(self):
        return '''
plugins {
    id 'com.android.application' version '8.2.0' apply false
    id 'org.jetbrains.kotlin.android' version '1.9.0' apply false
{% if config.configuration.dependencyInjection == 'hilt' %}
    id 'com.google.dagger.hilt.android' version '2.48' apply false
{% endif %}
}
'''.strip()

    def _get_build_gradle_kts_template(self):
        return '''
plugins {
    id("com.android.application") version "8.2.0" apply false
    id("org.jetbrains.kotlin.android") version "1.9.0" apply false
{% if config.configuration.dependencyInjection == 'hilt' %}
    id("com.google.dagger.hilt.android") version "2.48" apply false
{% endif %}
}
'''.strip()

    def _get_settings_gradle_template(self):
        return '''
pluginManagement {
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
'''.strip()

    def _get_settings_gradle_kts_template(self):
        return '''
pluginManagement {
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
'''.strip()

    def _get_libs_versions_toml_template(self):
        return '''
[versions]
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
'''.strip()

    def _get_app_build_gradle_template(self):
        return '''
plugins {
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
'''.strip()

    def _get_app_build_gradle_kts_template(self):
        return '''
plugins {
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
    {% endif %}
}
'''.strip()

    def _get_gradle_properties_template(self):
        return '''
# Project-wide Gradle settings.
# IDE (e.g. Android Studio) users:
# Gradle settings configured through the IDE *will override*
# any settings specified in this file.
# For more details on how to configure your build environment visit
# http://www.gradle.org/docs/current/userguide/build_environment.html
# Specifies the JVM arguments used for the daemon process.
# The setting is particularly useful for tweaking memory settings.
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
# When configured, Gradle will run in incubating parallel mode.
# This option should only be used with decoupled projects. For more details, visit
# https://developer.android.com/r/tools/gradle-multi-project-decoupled-projects
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
'''.strip()