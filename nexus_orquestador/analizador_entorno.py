# En DirectorOrquesta.registrar_modulos_base

# ... (otros módulos) ...

"nexus_mente": ModuloInfo(
    nombre="nexus_mente",
    archivo="nexus_mente_agi.py",
    funcion_principal="establecer_estrategia",
    dependencias=["analizador_entorno"], # Depende del contexto de análisis
    parametros={}, # No necesita parámetros fijos
    tiempo_estimado=10,
    critico=True
),
            
# **ACTUALIZACIÓN CRÍTICA DE DEPENDENCIAS**
"generador_contenido": ModuloInfo(
    nombre="generador_contenido",
    archivo="modulo_contenido.py",
    funcion_principal="generar_contenido_automatico",
    dependencias=["analizador_entorno", "nexus_mente"], # Ahora depende de la estrategia
    parametros={}, # Quitamos los parámetros fijos
    tiempo_estimado=120,
    critico=True
),

"promotor_automatico": ModuloInfo(
    nombre="promotor_automatico", 
    archivo="promo_bot.py",
    funcion_principal="ejecutar_campana_promocional",
    dependencias=["motor_afiliados", "generador_contenido", "nexus_mente"], # Depende de la estrategia
    parametros={}, # Quitamos los parámetros fijos
    tiempo_estimado=60,
    critico=False
),

# ...
