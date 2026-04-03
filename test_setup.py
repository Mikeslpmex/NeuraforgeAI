#!/usr/bin/env python3
"""Script de prueba de configuración"""

import sys
import os

def test_setup():
    """Verifica que todo esté configurado correctamente"""
    
    print("=" * 60)
    print("🔍 VERIFICACIÓN DE CONFIGURACIÓN NEURAFORGEAI")
    print("=" * 60)
    
    # 1. Verificar estructura de carpetas
    required_dirs = [
        "neuraforge/core",
        "neuraforge/payments", 
        "neuraforge/suite/bots",
        "neuraforge/ui",
        "neuraforge/logs",
        "neuraforge/data"
    ]
    
    print("\n📁 Verificando estructura de carpetas...")
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path} - FALTA")
    
    # 2. Verificar archivos principales
    required_files = [
        "neuraforge/main.py",
        "neuraforge/requirements.txt",
        "neuraforge/.env"
    ]
    
    print("\n📄 Verificando archivos principales...")
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - FALTA")
    
    # 3. Verificar dependencias instaladas
    print("\n📦 Verificando dependencias instaladas...")
    try:
        import fastapi
        print("✅ fastapi")
    except ImportError:
        print("❌ fastapi - NO INSTALADO")
    
    try:
        import uvicorn
        print("✅ uvicorn")
    except ImportError:
        print("❌ uvicorn - NO INSTALADO")
    
    try:
        import requests
        print("✅ requests")
    except ImportError:
        print("❌ requests - NO INSTALADO")
    
    print("\n" + "=" * 60)
    print("✅ VERIFICACIÓN COMPLETADA")
    print("=" * 60)

if __name__ == "__main__":
    test_setup()
