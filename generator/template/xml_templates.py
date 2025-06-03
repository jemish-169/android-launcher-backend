class XmlTemplates:
    """Template handler for XML related templates (resources, manifests, layouts)"""
    
    def __init__(self, config: dict):
        self.config = config
        self.project_config = config['project']
        self.app_config = config['configuration']
    
    def get_templates(self) -> dict:
        """Return all XML-related templates"""
        return {
            'android_manifest.j2': self._get_android_manifest_template(),
            'strings_xml.j2': self._get_strings_xml_template(),
            'colors_xml.j2': self._get_colors_xml_template(),
            'themes_xml.j2': self._get_themes_xml_template(),
            'network_config_xml.j2': self._get_network_config_xml_template(),
            'activity_main_xml.j2': self._get_activity_main_xml_template()
        }
    
    def _get_android_manifest_template(self):
        """Generate AndroidManifest.xml template"""
        return '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

{% for permission in permissions %}
    <uses-permission android:name="{{ permission }}" />
{% endfor %}

{% if config.configuration.networking in ['retrofit', 'ktor'] %}
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
{% endif %}

{% if config.project.targetSdk >= 33 %}
    <!-- Android 13+ notification permission -->
    {% if 'notifications' in config.configuration.permissions %}
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
    {% endif %}
{% endif %}

    <application
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{{ config.project.name.replace(' ', '').replace('-', '').replace('_', '') }}"
{% if use_network_config %}
        android:networkSecurityConfig="@xml/network_security_config"
{% endif %}
{% if config.configuration.dependencyInjection == 'hilt' %}
        android:name=".{{ config.project.name.replace(' ', '').replace('-', '').replace('_', '') }}Application"
{% endif %}
{% if config.project.targetSdk >= 31 %}
        android:exported="false"
{% endif %}
        tools:targetApi="{{ config.project.targetSdk }}">
        
        <activity
            android:name=".MainActivity"
            android:exported="true"
{% if config.configuration.uiToolkit == 'jetpack-compose' %}
            android:theme="@style/Theme.{{ config.project.name.replace(' ', '').replace('-', '').replace('_', '') }}"
            android:windowSoftInputMode="adjustResize">
{% else %}
            android:theme="@style/Theme.{{ config.project.name.replace(' ', '').replace('-', '').replace('_', '') }}">
{% endif %}
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>'''
    
    def _get_strings_xml_template(self):
        """Generate strings.xml template"""
        return '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{{ config.project.name }}</string>
    
    <!-- Common strings -->
    <string name="hello_world">Hello World!</string>
    <string name="welcome">Welcome to {{ config.project.name }}</string>
    
    <!-- Navigation strings -->
{% if config.configuration.navigation in ['compose-navigation', 'navigation-component'] %}
    <string name="navigation_home">Home</string>
    <string name="navigation_profile">Profile</string>
    <string name="navigation_settings">Settings</string>
{% endif %}
    
    <!-- Error messages -->
    <string name="error_generic">Something went wrong. Please try again.</string>
    <string name="error_network">Network error. Please check your connection.</string>
    <string name="error_loading">Loading failed. Please retry.</string>
    
    <!-- Permission messages -->
{% if 'camera' in config.configuration.permissions %}
    <string name="permission_camera_rationale">Camera permission is needed to take photos</string>
{% endif %}
{% if 'location' in config.configuration.permissions %}
    <string name="permission_location_rationale">Location permission is needed for location-based features</string>
{% endif %}
{% if 'storage' in config.configuration.permissions %}
    <string name="permission_storage_rationale">Storage permission is needed to save files</string>
{% endif %}
    
    <!-- Action strings -->
    <string name="action_ok">OK</string>
    <string name="action_cancel">Cancel</string>
    <string name="action_retry">Retry</string>
    <string name="action_settings">Settings</string>
    
{% if language is defined %}
    <!-- Localized strings for {{ language }} -->
{% endif %}
</resources>'''
    
    def _get_colors_xml_template(self):
        """Generate colors.xml template"""
        return '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <!-- Base colors -->
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
    <color name="transparent">#00000000</color>
    
    <!-- Material Design 3 Theme colors -->
    <color name="primary">{{ config.configuration.themeColors.primary }}</color>
    <color name="on_primary">#FFFFFF</color>
    <color name="primary_container">#E1C4FF</color>
    <color name="on_primary_container">#21005D</color>
    
    <color name="secondary">{{ config.configuration.themeColors.secondary }}</color>
    <color name="on_secondary">#FFFFFF</color>
    <color name="secondary_container">#CCE8DD</color>
    <color name="on_secondary_container">#002019</color>
    
    <color name="tertiary">{{ config.configuration.themeColors.tertiary }}</color>
    <color name="on_tertiary">#FFFFFF</color>
    <color name="tertiary_container">#FFDDB1</color>
    <color name="on_tertiary_container">#2A1700</color>
    
    <!-- Surface colors -->
    <color name="surface">#FFFBFE</color>
    <color name="on_surface">#1C1B1F</color>
    <color name="surface_variant">#E7E0EC</color>
    <color name="on_surface_variant">#49454F</color>
    
    <!-- Background colors -->
    <color name="background">#FFFBFE</color>
    <color name="on_background">#1C1B1F</color>
    
    <!-- Error colors -->
    <color name="error">#B3261E</color>
    <color name="on_error">#FFFFFF</color>
    <color name="error_container">#F9DEDC</color>
    <color name="on_error_container">#410E0B</color>
    
    <!-- Outline colors -->
    <color name="outline">#79747E</color>
    <color name="outline_variant">#CAC4D0</color>
    
    <!-- Additional utility colors -->
    <color name="scrim">#000000</color>
    <color name="inverse_surface">#313033</color>
    <color name="inverse_on_surface">#F4EFF4</color>
    <color name="inverse_primary">#D0BCFF</color>
    
    <!-- Legacy Material colors for compatibility -->
    <color name="colorPrimary">{{ config.configuration.themeColors.primary }}</color>
    <color name="colorPrimaryDark">#3700B3</color>
    <color name="colorAccent">{{ config.configuration.themeColors.secondary }}</color>
    
    <!-- Status bar and system colors -->
    <color name="status_bar_color">@color/primary</color>
    <color name="navigation_bar_color">@color/surface</color>
</resources>'''
    
    def _get_themes_xml_template(self):
        """Generate themes.xml template"""
        return '''<?xml version="1.0" encoding="utf-8"?>
<resources xmlns:tools="http://schemas.android.com/tools">
{% if config.configuration.uiTheme == 'material3' %}
    <!-- Material 3 Base Theme -->
    <style name="Base.Theme.{{ config.project.name.replace(' ', '').replace('-', '').replace('_', '') }}" parent="Theme.Material3.DayNight.NoActionBar">
        <!-- Material 3 color attributes -->
        <item name="colorPrimary">@color/primary</item>
        <item name="colorOnPrimary">@color/on_primary</item>
        <item name="colorPrimaryContainer">@color/primary_container</item>
        <item name="colorOnPrimaryContainer">@color/on_primary_container</item>
        
        <item name="colorSecondary">@color/secondary</item>
        <item name="colorOnSecondary">@color/on_secondary</item>
        <item name="colorSecondaryContainer">@color/secondary_container</item>
        <item name="colorOnSecondaryContainer">@color/on_secondary_container</item>
        
        <item name="colorTertiary">@color/tertiary</item>
        <item name="colorOnTertiary">@color/on_tertiary</item>
        <item name="colorTertiaryContainer">@color/tertiary_container</item>
        <item name="colorOnTertiaryContainer">@color/on_tertiary_container</item>
        
        <item name="colorError">@color/error</item>
        <item name="colorOnError">@color/on_error</item>
        <item name="colorErrorContainer">@color/error_container</item>
        <item name="colorOnErrorContainer">@color/on_error_container</item>
        
        <item name="colorSurface">@color/surface</item>
        <item name="colorOnSurface">@color/on_surface</item>
        <item name="colorSurfaceVariant">@color/surface_variant</item>
        <item name="colorOnSurfaceVariant">@color/on_surface_variant</item>
        
        <item name="android:colorBackground">@color/background</item>
        <item name="colorOnBackground">@color/on_background</item>
        
        <item name="colorOutline">@color/outline</item>
        <item name="colorOutlineVariant">@color/outline_variant</item>
        
        <!-- Status bar and navigation bar -->
        <item name="android:statusBarColor">@color/status_bar_color</item>
        <item name="android:navigationBarColor">@color/navigation_bar_color</item>
        <item name="android:windowLightStatusBar">true</item>
        <item name="android:windowLightNavigationBar" tools:targetApi="27">true</item>
    </style>
{% else %}
    <!-- Legacy Material Design Theme -->
    <style name="Base.Theme.{{ config.project.name.replace(' ', '').replace('-', '').replace('_', '') }}" parent="Theme.MaterialComponents.DayNight.NoActionBar">
        <item name="colorPrimary">@color/primary</item>
        <item name="colorPrimaryVariant">#3700B3</item>
        <item name="colorOnPrimary">@color/on_primary</item>
        
        <item name="colorSecondary">@color/secondary</item>
        <item name="colorSecondaryVariant">#018786</item>
        <item name="colorOnSecondary">@color/on_secondary</item>
        
        <item name="android:colorBackground">@color/background</item>
        <item name="colorOnBackground">@color/on_background</item>
        
        <item name="colorSurface">@color/surface</item>
        <item name="colorOnSurface">@color/on_surface</item>
        
        <item name="colorError">@color/error</item>
        <item name="colorOnError">@color/on_error</item>
        
        <!-- Status bar -->
        <item name="android:statusBarColor">@color/status_bar_color</item>
    </style>
{% endif %}

    <!-- Main App Theme -->
    <style name="Theme.{{ config.project.name.replace(' ', '').replace('-', '').replace('_', '') }}" parent="Base.Theme.{{ config.project.name.replace(' ', '').replace('-', '').replace('_', '') }}">
    </style>

{% if config.configuration.themes.lightDark or is_dark is defined and is_dark %}
    <!-- Dark Theme (values-night) -->
    <style name="Base.Theme.{{ config.project.name.replace(' ', '').replace('-', '').replace('_', '') }}" parent="Theme.Material3.DayNight.NoActionBar">
        <!-- Dark theme colors -->
        <item name="colorPrimary">#D0BCFF</item>
        <item name="colorOnPrimary">#381E72</item>
        <item name="colorPrimaryContainer">#4F378B</item>
        <item name="colorOnPrimaryContainer">#E1C4FF</item>
        
        <item name="colorSecondary">#B1CCC2</item>
        <item name="colorOnSecondary">#1C352D</item>
        <item name="colorSecondaryContainer">#334B43</item>
        <item name="colorOnSecondaryContainer">#CCE8DD</item>
        
        <item name="colorTertiary">#DCC196</item>
        <item name="colorOnTertiary">#3E2D16</item>
        <item name="colorTertiaryContainer">#56442A</item>
        <item name="colorOnTertiaryContainer">#FFDDB1</item>
        
        <item name="android:colorBackground">#1C1B1F</item>
        <item name="colorOnBackground">#E6E1E5</item>
        
        <item name="colorSurface">#1C1B1F</item>
        <item name="colorOnSurface">#E6E1E5</item>
        <item name="colorSurfaceVariant">#49454F</item>
        <item name="colorOnSurfaceVariant">#CAC4D0</item>
        
        <item name="colorError">#F2B8B5</item>
        <item name="colorOnError">#601410</item>
        <item name="colorErrorContainer">#8C1D18</item>
        <item name="colorOnErrorContainer">#F9DEDC</item>
        
        <!-- Dark theme status bar -->
        <item name="android:statusBarColor">#1C1B1F</item>
        <item name="android:navigationBarColor">#1C1B1F</item>
        <item name="android:windowLightStatusBar">false</item>
        <item name="android:windowLightNavigationBar" tools:targetApi="27">false</item>
    </style>
{% endif %}

    <!-- Splash Screen Theme (for Android 12+) -->
{% if config.project.targetSdk >= 31 %}
    <style name="Theme.{{ config.project.name.replace(' ', '').replace('-', '').replace('_', '') }}.Splash" parent="Theme.SplashScreen">
        <item name="windowSplashScreenBackground">@color/primary</item>
        <item name="windowSplashScreenAnimatedIcon">@mipmap/ic_launcher</item>
        <item name="windowSplashScreenAnimationDuration">1000</item>
        <item name="postSplashScreenTheme">@style/Theme.{{ config.project.name.replace(' ', '').replace('-', '').replace('_', '') }}</item>
    </style>
{% endif %}
</resources>'''
    
    def _get_network_config_xml_template(self):
        """Generate network_security_config.xml template"""
        return '''<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <!-- Development configuration -->
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">localhost</domain>
        <domain includeSubdomains="true">10.0.2.2</domain>
        <domain includeSubdomains="true">127.0.0.1</domain>
    </domain-config>
    
    <!-- Production configuration -->
    <domain-config cleartextTrafficPermitted="false">
        <domain includeSubdomains="true">api.{{ config.project.package.split('.')[1] }}.com</domain>
    </domain-config>
    
    <!-- Certificate pinning for enhanced security -->
    <domain-config>
        <domain includeSubdomains="true">secure-api.{{ config.project.package.split('.')[1] }}.com</domain>
        <pin-set expiration="2025-12-31">
            <!-- Add your certificate pins here -->
            <pin digest="SHA-256">7HIpactkIAq2Y49orFOOQKurWxmmSFZhBCoQYcRhJ3Y=</pin>
        </pin-set>
    </domain-config>
    
    <!-- Debug overrides (will be ignored in release builds) -->
    <debug-overrides>
        <trust-anchors>
            <certificates src="user"/>
            <certificates src="system"/>
        </trust-anchors>
    </debug-overrides>
</network-security-config>'''
    
    def _get_activity_main_xml_template(self):
        """Generate activity_main.xml template"""
        return '''<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="?attr/colorSurface"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/hello_world"
        android:textAppearance="?attr/textAppearanceHeadlineMedium"
        android:textColor="?attr/colorOnSurface"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <TextView
        android:id="@+id/welcomeText"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_marginStart="16dp"
        android:layout_marginTop="32dp"
        android:layout_marginEnd="16dp"
        android:gravity="center"
        android:text="@string/welcome"
        android:textAppearance="?attr/textAppearanceBodyLarge"
        android:textColor="?attr/colorOnSurfaceVariant"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/textView" />

</androidx.constraintlayout.widget.ConstraintLayout>'''
    
    @staticmethod
    def get_permission_manifest_entries(permissions: list, target_sdk: int = 34) -> list:
        """Convert permission names to Android manifest entries with proper Android version compatibility"""
        permission_map = {
            # Basic permissions
            'internet': 'android.permission.INTERNET',
            'network_state': 'android.permission.ACCESS_NETWORK_STATE',
            
            # Camera permissions
            'camera': 'android.permission.CAMERA',
            
            # Storage permissions (version dependent)
            'storage': 'android.permission.WRITE_EXTERNAL_STORAGE' if target_sdk < 30 else None,
            'read_storage': 'android.permission.READ_EXTERNAL_STORAGE' if target_sdk < 33 else None,
            'manage_storage': 'android.permission.MANAGE_EXTERNAL_STORAGE',  # Special permission for file managers
            
            # Android 13+ granular media permissions
            'read_media_images': 'android.permission.READ_MEDIA_IMAGES',  # API 33+
            'read_media_video': 'android.permission.READ_MEDIA_VIDEO',    # API 33+
            'read_media_audio': 'android.permission.READ_MEDIA_AUDIO',    # API 33+
            
            # Location permissions
            'location_fine': 'android.permission.ACCESS_FINE_LOCATION',
            'location_coarse': 'android.permission.ACCESS_COARSE_LOCATION',
            'location_background': 'android.permission.ACCESS_BACKGROUND_LOCATION',  # API 29+
            
            # Audio permissions
            'microphone': 'android.permission.RECORD_AUDIO',
            
            # Contacts permissions
            'read_contacts': 'android.permission.READ_CONTACTS',
            'write_contacts': 'android.permission.WRITE_CONTACTS',
            
            # Phone permissions
            'call_phone': 'android.permission.CALL_PHONE',
            'read_phone_state': 'android.permission.READ_PHONE_STATE',
            'read_phone_numbers': 'android.permission.READ_PHONE_NUMBERS',  # API 26+
            
            # SMS permissions
            'send_sms': 'android.permission.SEND_SMS',
            'receive_sms': 'android.permission.RECEIVE_SMS',
            'read_sms': 'android.permission.READ_SMS',
            
            # Calendar permissions
            'read_calendar': 'android.permission.READ_CALENDAR',
            'write_calendar': 'android.permission.WRITE_CALENDAR',
            
            # Notification permissions (Android 13+)
            'notifications': 'android.permission.POST_NOTIFICATIONS' if target_sdk >= 33 else None,
            
            # Bluetooth permissions
            'bluetooth': 'android.permission.BLUETOOTH',
            'bluetooth_admin': 'android.permission.BLUETOOTH_ADMIN',
            'bluetooth_connect': 'android.permission.BLUETOOTH_CONNECT',  # API 31+
            'bluetooth_scan': 'android.permission.BLUETOOTH_SCAN',        # API 31+
            'bluetooth_advertise': 'android.permission.BLUETOOTH_ADVERTISE',  # API 31+
            
            # WiFi permissions
            'wifi_state': 'android.permission.ACCESS_WIFI_STATE',
            'change_wifi_state': 'android.permission.CHANGE_WIFI_STATE',
            
            # Biometric permissions
            'fingerprint': 'android.permission.USE_FINGERPRINT',
            'biometric': 'android.permission.USE_BIOMETRIC',  # API 28+
            
            # Foreground service permissions (Android 14+)
            'foreground_service': 'android.permission.FOREGROUND_SERVICE',
            'foreground_service_camera': 'android.permission.FOREGROUND_SERVICE_CAMERA',  # API 34+
            'foreground_service_microphone': 'android.permission.FOREGROUND_SERVICE_MICROPHONE',  # API 34+
            'foreground_service_location': 'android.permission.FOREGROUND_SERVICE_LOCATION',  # API 34+
            
            # System permissions
            'wake_lock': 'android.permission.WAKE_LOCK',
            'vibrate': 'android.permission.VIBRATE',
            'system_alert_window': 'android.permission.SYSTEM_ALERT_WINDOW',
            
            # Installation permissions
            'install_packages': 'android.permission.INSTALL_PACKAGES',
            'request_install_packages': 'android.permission.REQUEST_INSTALL_PACKAGES',  # API 26+
        }
        
        result = []
        for perm in permissions:
            perm_lower = perm.lower().replace('-', '_').replace(' ', '_')
            
            if perm_lower in permission_map:
                mapped_perm = permission_map[perm_lower]
                if mapped_perm:  # Skip None values (version incompatible permissions)
                    result.append(mapped_perm)
            else:
                # Fallback: try to construct Android permission string
                result.append(f'android.permission.{perm.upper().replace("-", "_").replace(" ", "_")}')
        
        # Remove duplicates while preserving order
        seen = set()
        unique_result = []
        for perm in result:
            if perm not in seen:
                seen.add(perm)
                unique_result.append(perm)
        
        return unique_result