import time
import threading

HEARTS = ["💖", "💗", "💙", "💚", "💛", "💜", "🧡", "🤍", "🤎", "❤️"]

def animate_love(params, username):
    frames = [
        f"{h} {username} {h}" for h in HEARTS
    ]
    frames.append("".join(HEARTS) + f"\n💗 {username} 💗\n" + "".join(HEARTS))
    for frame in frames:
        params.message = frame
        time.sleep(0.5)
    params.message = f"{''.join(HEARTS)}\n💗 ЛЮБЛЮ {username} 💗\n{''.join(HEARTS)}"

def on_send_message_hook(account, params, state=None):
    if not isinstance(params.message, str):
        return
    msg = params.message.strip()
    if msg.lower() == "тест":
        params.message = "✅ код с GitHub сработал"
        return
    if msg.lower().startswith("люблю@"):  # пример: люблю@username
        username = msg[6:].strip()
        if username:
            t = threading.Thread(target=animate_love, args=(params, username))
            t.start()
            params.message = f"💗 {username} 💗"
        else:
            params.message = "Укажите имя после @: люблю@username"
