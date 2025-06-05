from typing import Dict
from models.config_model import ProjectConfig
from models.enums import DILib, Language, UIToolkit

class CommonTemplates:
    """Template handler for common files like MainActivity, gradle.properties, etc."""

    def __init__(self, config: ProjectConfig):
        self.config = config
        self.project_pascal_case = self.config.configuration.projectName.replace(' ', '')

    def get_templates(self) -> Dict[str, str]:
        """Return all common templates"""
        templates = {
            'gradle_properties.j2': self._get_gradle_properties_template(),
        }

        language = self.config.configuration.language
        ui_toolkit = self.config.configuration.uiToolkit

        if language == Language.kotlin:
            templates['main_activity_kotlin.j2'] = self._get_main_activity_kotlin_template()
        elif language == Language.java and ui_toolkit == UIToolkit.xml:
            templates['main_activity_java.j2'] = self._get_main_activity_java_template()

        return templates

    def _get_main_activity_kotlin_template(self) -> str:
        is_compose = self.config.configuration.uiToolkit == UIToolkit.compose
        use_hilt = self.config.configuration.dependencyInjection == DILib.hilt

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
import ''' + f"{self.config.project.package}.ui.theme.{self.project_pascal_case}Theme" if is_compose else 'import androidx.appcompat.app.AppCompatActivity'}

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
        use_hilt = self.config.configuration.dependencyInjection == DILib.hilt

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
        view_binding_enabled = self.config.configuration.viewBinding
        return f'''# Project-wide Gradle settings.
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
android.nonTransitiveRClass=true
{'android.enableViewBinding=true' if view_binding_enabled else ''}
'''