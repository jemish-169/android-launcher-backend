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
            'activity_main_xml.j2': self._get_activity_main_xml_template(),
        }
    
    def _get_android_manifest_template(self):
        """Generate AndroidManifest.xml template"""
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
    
    def _get_strings_xml_template(self):
        """Generate strings.xml template"""
        return '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{{ config.project.name }}</string>
{% if language is defined %}
    <!-- Localized strings for {{ language }} -->
{% endif %}
</resources>'''
    
    def _get_colors_xml_template(self):
        """Generate colors.xml template"""
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
        """Generate themes.xml template"""
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
        """Generate network_security_config.xml template"""
        return '''<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">localhost</domain>
        <domain includeSubdomains="true">10.0.2.2</domain>
    </domain-config>
</network-security-config>'''
    
    def _get_activity_main_xml_template(self):
        """Generate activity_main.xml template"""
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