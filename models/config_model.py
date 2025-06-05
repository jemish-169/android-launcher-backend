from pydantic import BaseModel
from typing import List, Optional
from models.enums import *

class ProjectInfo(BaseModel):
    name: str
    package: str
    minSdk: int
    targetSdk: int
    compileSdk: int

class I18nConfig(BaseModel):
    enabled: bool
    languages: List[str]

class ThemeColors(BaseModel):
    primary: str
    secondary: str
    tertiary: str

class Configuration(BaseModel):
    projectName: str
    projectId: str
    uiToolkit: UIToolkit
    networking: NetworkingLib
    serialization: SerializationLib
    dependencyInjection: DILib
    localStorage: LocalStorage
    enableRoom: bool
    uiTheme: UITheme
    permissions: List[Permission]
    internationalization: I18nConfig
    lightDark: bool
    httpNetworking: bool
    viewBinding: bool
    language: Language
    javaVersion: JavaVersion
    buildFormat: BuildFormat
    themeColors: ThemeColors
    fontName: FontName
    navigation: Navigation
    useLibsVersionsToml: bool

class ProjectConfig(BaseModel):
    project: ProjectInfo
    configuration: Configuration
    generated_at: Optional[str] = None
    generator_version: Optional[str] = None
