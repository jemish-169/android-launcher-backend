from typing import Dict

class CommonTemplates:
    """Template handler for common files like MainActivity, gradle.properties, etc."""

    def __init__(self, config: dict):
        self.config = config
        self.project_config = config['project']
        self.app_config = config['configuration']
        self.project_pascal_case = self.project_config['name'].replace(' ', '')
        self.font_family = self.app_config.get('fontFamily', '').lower()

    def get_templates(self) -> Dict[str, str]:
        """Return all common templates"""
        templates = {
            'gradle_properties.j2': self._get_gradle_properties_template(),
        }

        language = self.app_config.get('language')
        ui_toolkit = self.app_config.get('uiToolkit')

        if language == 'kotlin':
            templates['main_activity_kotlin.j2'] = self._get_main_activity_kotlin_template()
        elif language == 'java' and ui_toolkit == 'xml':
            templates['main_activity_java.j2'] = self._get_main_activity_java_template()

        return templates

    def _get_main_activity_kotlin_template(self) -> str:
        is_compose = self.app_config.get('uiToolkit') == 'jetpack-compose'
        use_hilt = self.app_config.get('dependencyInjection') == 'hilt'

        return f'''package {{{{ config.project.package }}}}

{f"import dagger.hilt.android.AndroidEntryPoint\n" if use_hilt else ''}import android.os.Bundle
{'''import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.tooling.preview.Preview
import ''' + f"{self.project_config['package']}.ui.theme.{self.project_pascal_case}Theme" if is_compose else 'import androidx.appcompat.app.AppCompatActivity'}

{f"@AndroidEntryPoint\n" if use_hilt else ''}{'''class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            ''' + f"{self.project_pascal_case}Theme" + ''' {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    Greeting()
                }
            }
        }
    }
}

@Composable
fun Greeting(modifier: Modifier = Modifier) {
    Text(
        text = stringResource(id = R.string.hello_android),
        modifier = modifier
    )
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    ''' + f"{self.project_pascal_case}Theme" + ''' {
        Greeting()
    }
}''' if is_compose else '''class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }
}'''}
'''

    def _get_main_activity_java_template(self) -> str:
        use_hilt = self.app_config.get('dependencyInjection') == 'hilt'

        return '''package {{ config.project.package }};

''' + ("import dagger.hilt.android.AndroidEntryPoint;\n" if use_hilt else '') + '''
import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;

''' + ("@AndroidEntryPoint\n" if use_hilt else '') + '''
public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }
}
'''

    def _get_gradle_properties_template(self) -> str:
        view_binding_enabled = self.app_config.get('viewBinding', False)
        return f'''# Project-wide Gradle settings.
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
android.nonTransitiveRClass=true
{'android.enableViewBinding=true' if view_binding_enabled else ''}
'''

    def get_font_copy_instructions(self) -> str:
        """
        Returns shell instructions as string to copy required font .ttf files
        from selected font family directory to app/src/main/res/font.
        """
        if not self.font_family:
            return "# No font family specified in configuration."

        font_source_path = f"fontfamilies/{self.font_family}"
        return f'''
# Create font destination directory
mkdir -p app/src/main/res/font

# Copy .ttf files from selected font family
cp "{font_source_path}"/*.ttf app/src/main/res/font/
echo "Copied fonts from {font_source_path}"
'''