# === COMANDO DE VALIDACIÓN OFICIAL ===

def register_admin_handlers(bot, admin_id):
    @bot.message_handler(commands=['validar'])
    def validate_payment(message):
        # 1. Seguridad: Solo el ID 8362361029 puede ejecutar esto
        if str(message.from_user.id) != str(admin_id):
            bot.reply_to(message, "❌ No tienes permisos de Tesorería.")
            return

        try:
            # Uso: /validar ID_USUARIO CANTIDAD
            parts = message.text.split()
            if len(parts) < 3:
                bot.reply_to(message, "⚠️ Uso correcto: `/validar 12345678 100`", parse_mode='Markdown')
                return

            target_user_id = parts[1]
            amount = int(parts[2])

            # 2. Actualizar Firebase (Colección 'usuarios')
            user_ref = db.collection('usuarios').document(str(target_user_id))
            
            # Incremento atómico para evitar errores de saldo
            user_ref.update({
                'fc_balance': firestore.Increment(amount),
                'ultimo_pago': firestore.SERVER_TIMESTAMP,
                'nivel': 'premium' if amount >= 100 else 'gratis'
            })

            # 3. Notificar al usuario (Felicidad del cliente)
            mensaje_usuario = f"""
✅ *¡DEPÓSITO VALIDADO!*
Se han acreditado `{amount} FC` a tu cuenta.
Gracias por financiar el reciclaje de hardware para la Forgecoin® Bitcoin's AI.
            """
            bot.send_message(target_user_id, mensaje_usuario, parse_mode='Markdown')
            
            # 4. Confirmar al Admin
            bot.reply_to(message, f"💰 Éxito: {amount} FC cargados al ID {target_user_id}")

        except Exception as e:
            bot.reply_to(message, f"❌ Error en base de datos: {str(e)}")
