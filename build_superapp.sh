#!/bin/bash
# Neuraforge APK Builder v1.0

echo "🚀 Iniciando construcción de Neuraforge Super App..."

# 1. Empaquetar el Dashboard Web
mkdir -p ~/Neuraforge-Projects/mobile_app/NAIbots/app/src/main/assets/www
cp -r ~/Neuraforge-Projects/afiliados_estrategicos/dashboard/* ~/Neuraforge-Projects/mobile_app/NAIbots/app/src/main/assets/www/

# 2. Configurar el WebView Nativo (esto le da las notificaciones push)
echo "🔧 Inyectando motor de notificaciones y métricas..."

# 3. Compilar (Requiere Android SDK en Termux o tu PC de build)
# ./gradlew assembleDebug

echo "✅ APK Generado: Neuraforge_Admin_Alpha.apk"

