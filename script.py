import time
import threading
import re

# Цветные сердечки для мигания
HEARTS = ["💖", "💗", "💙", "💚", "💛", "💜", "🧡", "🤍", "🤎", "❤️"]

def animate_love(params, username):
    # 1. Постепенно уменьшаем сообщение до точки
    original = params.message
    for i in range(len(original), 0, -1):
        params.message = original[:i]
        time.sleep(0.07)
    params.message = "."
    time.sleep(0.2)

    # 2. Появляется основание сердечка
    base = "  💗💗💗  "
    params.message = f".\n{base}"
    time.sleep(0.3)

    # 3. Появляется username чуть выше основания
    params.message = f".\n{base}\n   @{username}"
    time.sleep(0.4)

    # 4. Достраивается полное сердечко
    heart_shape = [
        "  💖💖💖  ",
        " 💖💖💖💖💖 ",
        "💖💖💖💖💖💖💖",
        " 💖💖💖💖💖 ",
        "  💖💖💖  ",
        "   💖💖   ",
        "    💖    "
    ]
    for i in range(1, len(heart_shape)+1):
        params.message = f".\n{base}\n   @{username}\n" + "\n".join(heart_shape[:i])
        time.sleep(0.2)

    # 5. Мигает разными цветами
    for _ in range(6):
        for h in HEARTS:
            colored_heart = [
                f"  {h}{h}{h}  ",
                f" {h}{h}{h}{h}{h} ",
                f"{h}{h}{h}{h}{h}{h}{h}",
                f" {h}{h}{h}{h}{h} ",
                f"  {h}{h}{h}  ",
                f"   {h}{h}   ",
                f"    {h}    "
            ]
            params.message = f".\n{base}\n   @{username}\n" + "\n".join(colored_heart)
            time.sleep(0.13)

    # Финальное красивое сообщение
    params.message = f"{''.join(HEARTS)}\n💗 ЛЮБЛЮ @{username} 💗\n{''.join(HEARTS)}"

def on_send_message_hook(account, params, state=None):
    if not isinstance(params.message, str):
        return
    msg = params.message.strip()
    # Универсальный паттерн для поиска команды
    match = re.match(r"люблю\\s*@([\\w_]+)", msg, re.IGNORECASE)
    if match:
        username = match.group(1)
        t = threading.Thread(target=animate_love, args=(params, username))
        t.start()
        params.message = f"💗 @{username} 💗"
        return
    # Стандартный тест
    if msg.lower() == "тест":
        params.message = "✅ код с GitHub сработал"
        return