class XmlTemplates:
    """Template handler for XML related templates (resources, manifests, layouts)"""
    
    def __init__(self, config: dict):
        self.config = config
        self.project_config = config['project']
        self.app_config = config['configuration']
    
    @staticmethod
    def get_permission_manifest_entries(permissions: list) -> dict:
        """Convert permission names to Android manifest entries with version compatibility"""
        permission_entries = {
            'permissions': [],
            'uses_features': []
        }
        
        permission_map = {
            'camera': {
                'permissions': ['android.permission.CAMERA'],
                'features': ['android.hardware.camera', 'android.hardware.camera.autofocus']
            },
            'internet': {
                'permissions': ['android.permission.INTERNET', 'android.permission.ACCESS_NETWORK_STATE'],
                'features': []
            },
            'storage': {
                'permissions': [
                    'android.permission.READ_EXTERNAL_STORAGE',
                    'android.permission.WRITE_EXTERNAL_STORAGE',
                    'android.permission.READ_MEDIA_IMAGES',
                    'android.permission.READ_MEDIA_VIDEO',
                    'android.permission.READ_MEDIA_AUDIO'
                ],
                'features': []
            },
            'location': {
                'permissions': [
                    'android.permission.ACCESS_FINE_LOCATION',
                    'android.permission.ACCESS_COARSE_LOCATION',
                    'android.permission.ACCESS_BACKGROUND_LOCATION'
                ],
                'features': ['android.hardware.location', 'android.hardware.location.gps']
            },
            'microphone': {
                'permissions': ['android.permission.RECORD_AUDIO'],
                'features': ['android.hardware.microphone']
            },
            'contacts': {
                'permissions': ['android.permission.READ_CONTACTS', 'android.permission.WRITE_CONTACTS'],
                'features': []
            },
            'sms': {
                'permissions': ['android.permission.SEND_SMS', 'android.permission.READ_SMS', 'android.permission.RECEIVE_SMS'],
                'features': ['android.hardware.telephony']
            },
            'phone': {
                'permissions': ['android.permission.CALL_PHONE', 'android.permission.READ_PHONE_STATE'],
                'features': ['android.hardware.telephony']
            }
        }
        
        all_permissions = set()
        all_features = set()
        
        for perm in permissions:
            perm_lower = perm.lower()
            if perm_lower in permission_map:
                all_permissions.update(permission_map[perm_lower]['permissions'])
                all_features.update(permission_map[perm_lower]['features'])
            else:
                all_permissions.add(f'android.permission.{perm.upper()}')
        
        permission_entries['permissions'] = list(all_permissions)
        permission_entries['uses_features'] = list(all_features)
        
        return permission_entries
    
    def get_templates(self) -> dict:
        """Return all XML-related templates"""
        return {
            'android_manifest.j2': self._get_android_manifest_template(),
            'strings_xml.j2': self._get_strings_xml_template(),
            'colors_xml.j2': self._get_colors_xml_template(),
            'themes_xml.j2': self._get_themes_xml_template(),
            'network_config_xml.j2': self._get_network_config_xml_template(),
            'activity_main_xml.j2': self._get_activity_main_xml_template(),
            'data_extraction_rules_xml.j2': self._get_data_extraction_rules_template(),
            'backup_rules_xml.j2': self._get_backup_rules_template(),
        }
    
    def _get_android_manifest_template(self):
        """Generate AndroidManifest.xml template"""
        return '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

{% for permission in permissions %}
    <uses-permission android:name="{{ permission }}"{% if permission == 'android.permission.WRITE_EXTERNAL_STORAGE' %} 
        android:maxSdkVersion="28"{% endif %}{% if permission == 'android.permission.ACCESS_BACKGROUND_LOCATION' %} 
        tools:targetApi="29"{% endif %} />
{% endfor %}

{% for feature in uses_features %}
    <uses-feature android:name="{{ feature }}" android:required="false" />
{% endfor %}

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
        tools:targetApi="{{ config.project.targetSdk }}">
        
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:theme="@style/Theme.{{ config.project.name.replace(' ', '').replace('-', '').replace('_', '') }}"
            tools:ignore="AppLinkUrlError">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        
{% if config.configuration.networking == 'retrofit' or config.configuration.networking == 'ktor' %}
        <provider
            android:name="androidx.core.content.FileProvider"
            android:authorities="${applicationId}.fileprovider"
            android:exported="false"
            android:grantUriPermissions="true">
            <meta-data
                android:name="android.support.FILE_PROVIDER_PATHS"
                android:resource="@xml/file_paths" />
        </provider>
{% endif %}
    </application>

</manifest>'''
    
    def _get_strings_xml_template(self):
        """Generate strings.xml template"""
        return '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{{ config.project.name }}</string>
    <string name="hello_world">Hello World!</string>
    <string name="welcome_message">Welcome to {{ config.project.name }}</string>
    
{% if config.configuration.networking != 'None' %}
    <string name="network_error">Network connection error</string>
    <string name="loading">Loading...</string>
{% endif %}

{% if 'camera' in config.configuration.permissions %}
    <string name="camera_permission_required">Camera permission is required</string>
{% endif %}

{% if 'location' in config.configuration.permissions %}
    <string name="location_permission_required">Location permission is required</string>
{% endif %}

{% if 'storage' in config.configuration.permissions %}
    <string name="storage_permission_required">Storage permission is required</string>
{% endif %}

{% if 'microphone' in config.configuration.permissions %}
    <string name="microphone_permission_required">Microphone permission is required</string>
{% endif %}

{% if language is defined and language != 'en' %}
    <!-- Localized strings for {{ language }} -->
{% endif %}
</resources>'''
    
    def _get_colors_xml_template(self):
        """Generate colors.xml template"""
        return '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
    
    <color name="primary">{{ config.configuration.themeColors.primary }}</color>
    <color name="secondary">{{ config.configuration.themeColors.secondary }}</color>
    <color name="tertiary">{{ config.configuration.themeColors.tertiary }}</color>
    
{% if config.configuration.uiTheme == 'material3' %}
    <color name="primary_container">#EADDFF</color>
    <color name="on_primary_container">#21005D</color>
    <color name="secondary_container">#E8DEF8</color>
    <color name="on_secondary_container">#1D192B</color>
    <color name="tertiary_container">#FFD8E4</color>
    <color name="on_tertiary_container">#31111D</color>
    <color name="surface">#FFFBFE</color>
    <color name="on_surface">#1C1B1F</color>
    <color name="surface_variant">#E7E0EC</color>
    <color name="on_surface_variant">#49454F</color>
    <color name="outline">#79747E</color>
    <color name="outline_variant">#CAC4D0</color>
{% else %}
    <color name="primary_variant">#3700B3</color>
    <color name="secondary_variant">#018786</color>
    <color name="surface">#FFFFFF</color>
    <color name="on_surface">#000000</color>
{% endif %}
    
    <color name="background">#FFFBFE</color>
    <color name="on_background">#1C1B1F</color>
    <color name="error">#B3261E</color>
    <color name="on_error">#FFFFFF</color>
    <color name="error_container">#F9DEDC</color>
    <color name="on_error_container">#410E0B</color>
    <color name="on_primary">#FFFFFF</color>
    <color name="on_secondary">#FFFFFF</color>
    <color name="on_tertiary">#FFFFFF</color>
</resources>'''
    
    def _get_themes_xml_template(self):
        """Generate themes.xml template"""
        theme_name = self.project_config['name'].replace(' ', '').replace('-', '').replace('_', '')
        
        return f'''<?xml version="1.0" encoding="utf-8"?>
<resources xmlns:tools="http://schemas.android.com/tools">
{{% if config.configuration.uiTheme == 'material3' %}}
    <style name="Base.Theme.{theme_name}" parent="Theme.Material3.DayNight.NoActionBar">
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
        <item name="colorOutline">@color/outline</item>
        <item name="colorOutlineVariant">@color/outline_variant</item>
        <item name="android:colorBackground">@color/background</item>
        <item name="colorOnBackground">@color/on_background</item>
    </style>
{{% elif config.configuration.uiTheme == 'material3-expressive' %}}
    <style name="Base.Theme.{theme_name}" parent="Theme.Material3.DynamicColors.DayNight.NoActionBar">
        <item name="colorPrimary">@color/primary</item>
        <item name="colorSecondary">@color/secondary</item>
        <item name="colorTertiary">@color/tertiary</item>
    </style>
{{% else %}}
    <style name="Base.Theme.{theme_name}" parent="Theme.MaterialComponents.DayNight.NoActionBar">
        <item name="colorPrimary">@color/primary</item>
        <item name="colorPrimaryVariant">@color/primary_variant</item>
        <item name="colorSecondary">@color/secondary</item>
        <item name="colorSecondaryVariant">@color/secondary_variant</item>
        <item name="android:colorBackground">@color/background</item>
        <item name="colorSurface">@color/surface</item>
        <item name="colorError">@color/error</item>
        <item name="colorOnPrimary">@color/on_primary</item>
        <item name="colorOnSecondary">@color/on_secondary</item>
        <item name="colorOnBackground">@color/on_background</item>
        <item name="colorOnSurface">@color/on_surface</item>
        <item name="colorOnError">@color/on_error</item>
    </style>
{{% endif %}}

    <style name="Theme.{theme_name}" parent="Base.Theme.{theme_name}" />
    
{{% if config.configuration.uiToolkit != 'jetpack-compose' %}}
    <style name="Theme.{theme_name}.AppBarOverlay" parent="ThemeOverlay.AppCompat.Dark.ActionBar" />
    <style name="Theme.{theme_name}.PopupOverlay" parent="ThemeOverlay.AppCompat.Light" />
{{% endif %}}

{{% if is_dark is defined and is_dark %}}
    <style name="Base.Theme.{theme_name}" parent="Theme.Material3.DayNight.NoActionBar">
        <item name="android:colorBackground">#121212</item>
        <item name="colorSurface">#1E1E1E</item>
        <item name="colorOnSurface">#E1E1E1</item>
        <item name="colorOnBackground">#E1E1E1</item>
        <item name="colorPrimary">@color/primary</item>
        <item name="colorSecondary">@color/secondary</item>
        <item name="colorTertiary">@color/tertiary</item>
    </style>
{{% endif %}}
</resources>'''
    
    def _get_network_config_xml_template(self):
        """Generate network_security_config.xml template"""
        return '''<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">localhost</domain>
        <domain includeSubdomains="true">10.0.2.2</domain>
        <domain includeSubdomains="true">127.0.0.1</domain>
    </domain-config>
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors>
            <certificates src="system"/>
        </trust-anchors>
    </base-config>
</network-security-config>'''
    
    def _get_activity_main_xml_template(self):
        """Generate activity_main.xml template"""
        return '''<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout 
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/hello_world"
        android:textAppearance="?attr/textAppearanceHeadlineMedium"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>'''
    
    def _get_data_extraction_rules_template(self):
        """Generate data_extraction_rules.xml template"""
        return '''<?xml version="1.0" encoding="utf-8"?>
<data-extraction-rules>
    <cloud-backup>
        <include domain="file" path="."/>
        <exclude domain="file" path="no_backup/"/>
    </cloud-backup>
    <device-transfer>
        <include domain="file" path="."/>
        <exclude domain="file" path="no_backup/"/>
    </device-transfer>
</data-extraction-rules>'''
    
    def _get_backup_rules_template(self):
        """Generate backup_rules.xml template"""
        return '''<?xml version="1.0" encoding="utf-8"?>
<full-backup-content>
    <exclude domain="file" path="no_backup"/>
    <exclude domain="database" path="temp.db"/>
</full-backup-content>'''