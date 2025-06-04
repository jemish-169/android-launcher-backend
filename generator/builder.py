import glob
import os
import shutil
import tempfile
import zipfile
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from .utils import ProjectUtils
from .template.compose_templates import ComposeTemplates
from .template.xml_templates import XmlTemplates
from .template.gradle_templates import GradleTemplates
from .template.common_templates import CommonTemplates

class AndroidProjectBuilder:
    """Main builder class for generating Android projects"""
    
    def __init__(self, config: dict):
        self.config = config
        self.project_config = config['project']
        self.app_config = config['configuration']
        self.utils = ProjectUtils()

        typography = self.app_config.get('typography', {})
        font_name = typography.get('fontName', '')
        self.font_family = font_name
        
        # Setup Jinja2 environment
        template_dir = Path(__file__).parent / 'templates'
        template_dir.mkdir(exist_ok=True)
        self.jinja_env = Environment(loader=FileSystemLoader(str(template_dir)))
        
        # Initialize template handlers
        self.compose_templates = ComposeTemplates(self.config)
        self.xml_templates = XmlTemplates(self.config)
        self.gradle_templates = GradleTemplates(self.config)
        self.common_templates = CommonTemplates(self.config)
        
        # Create templates directory and files if they don't exist
        self._create_default_templates()
    
    def _create_default_templates(self):
        """Create default templates if they don't exist"""
        templates_dir = Path(__file__).parent / 'templates'
        templates_dir.mkdir(exist_ok=True)
        
        # Get all template files from different handlers
        template_files = {}
        template_files.update(self.gradle_templates.get_templates())
        template_files.update(self.xml_templates.get_templates())
        template_files.update(self.compose_templates.get_templates())
        template_files.update(self.common_templates.get_templates())
        
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
            
            self._copy_font_files(project_dir)

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
            'gradle/wrapper',
            'app/src/main/res/font'
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
    

    def _copy_font_files(self, project_dir : str):
        """
        Actually copies font .ttf files from selected font family directory 
        to app/src/main/res/font.
        """
        if not self.font_family:
            return

        font_source_path = f"fontfamilies/{self.font_family}"
        font_dest_path = f"{project_dir}/app/src/main/res/font"

        try:
            # Check if source directory exists
            if not os.path.exists(font_source_path):
                return

            # Create destination directory
            os.makedirs(font_dest_path, exist_ok=True)

            # Find and copy all .ttf files
            ttf_files = glob.glob(os.path.join(font_source_path, "*.ttf"))

            if not ttf_files:
                return

            for ttf_file in ttf_files:
                filename = os.path.basename(ttf_file)
                dest_file = os.path.join(font_dest_path, filename)
                shutil.copy2(ttf_file, dest_file)


        except Exception as e:
            print(f"Error copying fonts: {str(e)}")

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
        
        # Generate Theme.kt
        if self.app_config['language'] == 'kotlin':
            # Load and render Theme.kt
            theme_template = self.jinja_env.get_template('compose_theme.j2')
            self.utils.write_file(theme_dir / 'Theme.kt', theme_template.render(config=self.config))
            
            # Load and render Color.kt
            color_template = self.jinja_env.get_template('compose_color.j2')
            self.utils.write_file(theme_dir / 'Color.kt', color_template.render(config=self.config))
            
            # Load and render Type.kt
            type_template = self.jinja_env.get_template('compose_typography.j2')
            self.utils.write_file(theme_dir / 'Type.kt', type_template.render(config=self.config))