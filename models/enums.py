from enum import Enum

class UIToolkit(str, Enum):
    compose = "jetpack-compose"
    xml = "xml-views"

class NetworkingLib(str, Enum):
    retrofit = "retrofit"
    ktor = "ktor"
    none = "none"

class SerializationLib(str, Enum):
    gson = "gson"
    moshi = "moshi"
    kotlinx = "kotlinx-serialization"
    none = "none"

class DILib(str, Enum):
    hilt = "hilt"
    koin = "koin"
    none = "none"

class LocalStorage(str, Enum):
    datastore = "datastore"
    shared_pref = "shared-preferences"
    none = "none"

class UITheme(str, Enum):
    material = "material"
    material3 = "material3"
    material3_expressive = "material3-expressive"

class Language(str, Enum):
    kotlin = "kotlin"
    java = "java"

class JavaVersion(str, Enum):
    v11 = "11"
    v17 = "17"
    v21 = "21"

class BuildFormat(str, Enum):
    gradle = "gradle"
    kts = "kts"

class FontName(str, Enum):
    roboto = "roboto"
    poppins = "poppins"
    inter = "inter"
    open_sans = "open sans"
    lato = "lato"

class Navigation(str, Enum):
    compose = "compose-navigation"
    fragment = "jetpack-navigation"

class Permission(str, Enum):
    camera = "camera"
    internet = "internet"
    storage = "storage"
    location = "location"
    microphone = "microphone"
    contacts = "contacts"
    sms = "sms"
    phone = "phone"