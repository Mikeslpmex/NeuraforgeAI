#!/usr/bin/env python3
"""
Bot Pizza - Ejemplo de bot gratuito
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot_blueprint import BotPizza

if __name__ == "__main__":
    bot = BotPizza("pizza_demo")
    
    print("🍕 BOT PIZZA - Asistente de pedidos")
    print("Comandos: menu, pedir, estado")
    
    while True:
        cmd = input("\n> ").strip().lower()
        
        if cmd == "menu":
            print(bot.ejecutar("menu"))
        
        elif cmd.startswith("pedir"):
            pizza = input("Qué pizza? (margarita/pepperoni/hawaiana): ")
            direccion = input("Dirección de entrega: ")
            print(bot.ejecutar("pedir", pizza=pizza, direccion=direccion))
        
        elif cmd == "exit":
            break
