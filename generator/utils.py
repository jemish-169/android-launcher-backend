import os
import re
from pathlib import Path
from typing import List

class ProjectUtils:
    """Utility functions for Android project generation"""
    
    @staticmethod
    def sanitize_project_name(name: str) -> str:
        """Sanitize project name for use as folder name"""
        return re.sub(r'[^\w\-_.]', '', name)
    
    @staticmethod
    def package_to_path(package: str) -> str:
        """Convert package name to folder path"""
        return package.replace('.', '/')
    
    @staticmethod
    def create_directories(base_path: Path, directories: List[str]):
        """Create multiple directories"""
        for directory in directories:
            dir_path = base_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def write_file(file_path: Path, content: str):
        """Write content to file"""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    @staticmethod
    def get_permission_manifest_entries(permissions: List[str]) -> List[str]:
        """Convert permission names to Android manifest entries"""
        permission_map = {
            'camera': 'android.permission.CAMERA',
            'internet': 'android.permission.INTERNET',
            'storage': 'android.permission.WRITE_EXTERNAL_STORAGE',
            'location': 'android.permission.ACCESS_FINE_LOCATION',
            'microphone': 'android.permission.RECORD_AUDIO',
            'contacts': 'android.permission.READ_CONTACTS',
            'sms': 'android.permission.SEND_SMS',
            'phone': 'android.permission.CALL_PHONE'
        }
        return [permission_map.get(perm.lower(), f'android.permission.{perm.upper()}') for perm in permissions]
