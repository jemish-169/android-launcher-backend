class ComposeTemplates:
    """Template handler for Jetpack Compose related templates"""
    
    def __init__(self, config: dict):
        self.config = config
        self.project_config = config['project']
        self.app_config = config['configuration']
    
    def get_templates(self) -> dict:
        """Return all Compose-related templates"""
        return {
            'compose_theme.j2': self._get_compose_theme_template(),
        }
    
    def _get_compose_theme_template(self):
        """Generate Jetpack Compose theme template with conditional content based on file_type"""
        return '''{% if file_type == 'theme' %}
package {{ config.project.package }}.ui.theme

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
{% elif file_type == 'color' %}
package {{ config.project.package }}.ui.theme

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
{% elif file_type == 'type' %}
package {{ config.project.package }}.ui.theme

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
{% endif %}'''