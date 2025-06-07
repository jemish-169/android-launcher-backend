from models.config_model import ProjectConfig
from models.enums import Language


class TestTemplates:
    """Template handler for test and androidTest packages"""

    def __init__(self, config: ProjectConfig):
        self.config = config

    def get_templates(self) -> dict:
        language = self.config.configuration.language
        
        if language == Language.kotlin:
            return {
                'unit_test_kt.j2': self._get_test_kotlin(),
                'example_instrumented_test_kt.j2': self._get_android_test_kotlin()
            }
        else :
            return {
                'unit_test_java.j2': self._get_test_java(),
                'example_instrumented_test_java.j2': self._get_android_test_java()
            }

    def _get_test_kotlin(self):
        return '''package {{ config.project.package }}

import org.junit.Assert.*
import org.junit.Test

class ExampleUnitTest {
    @Test
    fun addition_isCorrect() {
        assertEquals(4, 2 + 2)
    }
}'''

    def _get_android_test_kotlin(self):
        return '''package {{ config.project.package }}

import androidx.test.platform.app.InstrumentationRegistry
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Test
import org.junit.runner.RunWith
import org.junit.Assert.*

@RunWith(AndroidJUnit4::class)
class ExampleInstrumentedTest {

    @Test
    fun useAppContext() {
        val appContext = InstrumentationRegistry.getInstrumentation().targetContext
        assertEquals("{{ config.project.package }}", appContext.packageName)
    }
}'''

    def _get_test_java(self):
        return '''package {{ config.project.package }};

import org.junit.Test;
import static org.junit.Assert.*;

public class ExampleUnitTest {
    @Test
    public void addition_isCorrect() {
        assertEquals(4, 2 + 2);
    }
}'''

    def _get_android_test_java(self):
        return '''package {{ config.project.package }};

import android.content.Context;
import androidx.test.platform.app.InstrumentationRegistry;
import androidx.test.ext.junit.runners.AndroidJUnit4;
import org.junit.Test;
import org.junit.runner.RunWith;
import static org.junit.Assert.*;

@RunWith(AndroidJUnit4.class)
public class ExampleInstrumentedTest {

    @Test
    public void useAppContext() {
        Context appContext = InstrumentationRegistry.getInstrumentation().getTargetContext();
        assertEquals("{{ config.project.package }}", appContext.getPackageName());
    }
}'''