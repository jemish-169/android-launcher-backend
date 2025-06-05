from models.config_model import ProjectConfig

class ComposeTemplates:
    """Template handler for Jetpack Compose related templates"""

    def __init__(self, config: ProjectConfig):
        self.config = config
        self.project_pascal_case = self.config.project.name.replace(' ', '')

    def get_templates(self) -> dict:
        """Return all Compose-related templates"""
        return {
            'compose_theme.j2': self._get_compose_theme_template(),
            'compose_color.j2': self._get_color_scheme_template(),
            'compose_typography.j2': self._get_typography_template(),
        }

    def _get_compose_theme_template(self) -> str:
        """Generate the main Theme.kt template"""
        return '''package {{ config.project.package }}.ui.theme

import android.app.Activity
import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat

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
            WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = !darkTheme
        }
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
'''

    def _get_color_scheme_template(self) -> str:
        """Generate the Color.kt template"""
        return '''package {{ config.project.package }}.ui.theme

import androidx.compose.material3.lightColorScheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.ui.graphics.Color

// Custom theme colors
val Primary = Color({{ config.configuration.themeColors.primary.replace('#', '0xFF') if config.configuration.themeColors.primary else '0xFF6200EE' }})
val Secondary = Color({{ config.configuration.themeColors.secondary.replace('#', '0xFF') if config.configuration.themeColors.secondary else '0xFF03DAC6' }})
val Tertiary = Color({{ config.configuration.themeColors.tertiary.replace('#', '0xFF') if config.configuration.themeColors.tertiary else '0xFFBB86FC' }})

// Light theme colors
val LightBackground = Color(0xFFFFFBFE)
val LightSurface = Color(0xFFFFFBFE)
val LightOnPrimary = Color(0xFFFFFFFF)
val LightOnSecondary = Color(0xFFFFFFFF)
val LightOnTertiary = Color(0xFFFFFFFF)
val LightOnBackground = Color(0xFF1C1B1F)
val LightOnSurface = Color(0xFF1C1B1F)

// Dark theme colors
val DarkPrimary = Color(0xFFD0BCFF)
val DarkSecondary = Color(0xFFCCC2DC)
val DarkTertiary = Color(0xFFEFB8C8)
val DarkBackground = Color(0xFF1C1B1F)
val DarkSurface = Color(0xFF1C1B1F)
val DarkOnPrimary = Color(0xFF1C1B1F)
val DarkOnSecondary = Color(0xFF1C1B1F)
val DarkOnTertiary = Color(0xFF1C1B1F)
val DarkOnBackground = Color(0xFFE6E1E5)
val DarkOnSurface = Color(0xFFE6E1E5)

val LightColorScheme = lightColorScheme(
    primary = Primary,
    secondary = Secondary,
    tertiary = Tertiary,
    background = LightBackground,
    surface = LightSurface,
    onPrimary = LightOnPrimary,
    onSecondary = LightOnSecondary,
    onTertiary = LightOnTertiary,
    onBackground = LightOnBackground,
    onSurface = LightOnSurface,
)

val DarkColorScheme = darkColorScheme(
    primary = DarkPrimary,
    secondary = DarkSecondary,
    tertiary = DarkTertiary,
    background = DarkBackground,
    surface = DarkSurface,
    onPrimary = DarkOnPrimary,
    onSecondary = DarkOnSecondary,
    onTertiary = DarkOnTertiary,
    onBackground = DarkOnBackground,
    onSurface = DarkOnSurface,
)
'''

    def _get_typography_template(self) -> str:
        """Generate the Type.kt template"""
        return '''package {{ config.project.package }}.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp
import {{ config.project.package }}.R

// Custom font family
val {{ config.configuration.fontName.title() }}FontFamily = FontFamily(
    Font(R.font.{{ config.configuration.fontName.lower() }}_light, FontWeight.Light),
    Font(R.font.{{ config.configuration.fontName.lower() }}_regular, FontWeight.Normal),
    Font(R.font.{{ config.configuration.fontName.lower() }}_medium, FontWeight.Medium),
    Font(R.font.{{ config.configuration.fontName.lower() }}_bold, FontWeight.Bold),
    Font(R.font.{{ config.configuration.fontName.lower() }}_semibold, FontWeight.SemiBold)
)

// Set of Material typography styles
val Typography = Typography(
    displayLarge = TextStyle(
        fontFamily = {{ config.configuration.fontName.title() }}FontFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 57.sp,
        lineHeight = 64.sp,
        letterSpacing = (-0.25).sp,
    ),
    displayMedium = TextStyle(
        fontFamily = {{ config.configuration.fontName.title() }}FontFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 45.sp,
        lineHeight = 52.sp,
        letterSpacing = 0.sp,
    ),
    displaySmall = TextStyle(
        fontFamily = {{ config.configuration.fontName.title() }}FontFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 36.sp,
        lineHeight = 44.sp,
        letterSpacing = 0.sp,
    ),
    headlineLarge = TextStyle(
        fontFamily = {{ config.configuration.fontName.title() }}FontFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 32.sp,
        lineHeight = 40.sp,
        letterSpacing = 0.sp,
    ),
    headlineMedium = TextStyle(
        fontFamily = {{ config.configuration.fontName.title() }}FontFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 28.sp,
        lineHeight = 36.sp,
        letterSpacing = 0.sp,
    ),
    headlineSmall = TextStyle(
        fontFamily = {{ config.configuration.fontName.title() }}FontFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 24.sp,
        lineHeight = 32.sp,
        letterSpacing = 0.sp,
    ),
    titleLarge = TextStyle(
        fontFamily = {{ config.configuration.fontName.title() }}FontFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 22.sp,
        lineHeight = 28.sp,
        letterSpacing = 0.sp,
    ),
    titleMedium = TextStyle(
        fontFamily = {{ config.configuration.fontName.title() }}FontFamily,
        fontWeight = FontWeight.Medium,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.15.sp,
    ),
    titleSmall = TextStyle(
        fontFamily = {{ config.configuration.fontName.title() }}FontFamily,
        fontWeight = FontWeight.Medium,
        fontSize = 14.sp,
        lineHeight = 20.sp,
        letterSpacing = 0.1.sp,
    ),
    bodyLarge = TextStyle(
        fontFamily = {{ config.configuration.fontName.title() }}FontFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.5.sp,
    ),
    bodyMedium = TextStyle(
        fontFamily = {{ config.configuration.fontName.title() }}FontFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 14.sp,
        lineHeight = 20.sp,
        letterSpacing = 0.25.sp,
    ),
    bodySmall = TextStyle(
        fontFamily = {{ config.configuration.fontName.title() }}FontFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 12.sp,
        lineHeight = 16.sp,
        letterSpacing = 0.4.sp,
    ),
    labelLarge = TextStyle(
        fontFamily = {{ config.configuration.fontName.title() }}FontFamily,
        fontWeight = FontWeight.Medium,
        fontSize = 14.sp,
        lineHeight = 20.sp,
        letterSpacing = 0.1.sp,
    ),
    labelMedium = TextStyle(
        fontFamily = {{ config.configuration.fontName.title() }}FontFamily,
        fontWeight = FontWeight.Medium,
        fontSize = 12.sp,
        lineHeight = 16.sp,
        letterSpacing = 0.5.sp,
    ),
    labelSmall = TextStyle(
        fontFamily = {{ config.configuration.fontName.title() }}FontFamily,
        fontWeight = FontWeight.Medium,
        fontSize = 11.sp,
        lineHeight = 16.sp,
        letterSpacing = 0.5.sp,
    ),
)
'''