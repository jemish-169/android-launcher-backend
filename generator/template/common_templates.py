class CommonTemplates:
    """Template handler for common files like MainActivity, gradle.properties, etc."""
    
    def __init__(self, config: dict):
        self.config = config
        self.project_config = config['project']
        self.app_config = config['configuration']
    
    def get_templates(self) -> dict:
        """Return all common templates"""
        return {
            'main_activity_kotlin.j2': self._get_main_activity_kotlin_template(),
            'main_activity_java.j2': self._get_main_activity_java_template(),
            'gradle_properties.j2': self._get_gradle_properties_template(),
        }
    
    def _get_main_activity_kotlin_template(self):
        """Generate MainActivity.kt template"""
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
        """Generate MainActivity.java template"""
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
    
    def _get_gradle_properties_template(self):
        """Generate gradle.properties template"""
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