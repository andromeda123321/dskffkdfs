import time
import threading

HEARTS = ["💖", "💗", "💙", "💚", "💛", "💜", "🧡", "🤍", "🤎", "❤️"]

# Храним id уже обработанных сообщений, чтобы не дублировать анимацию

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
    # Инициализация state для хранения id сообщений
    if state is not None and 'handled_ids' not in state:
        state['handled_ids'] = set()
    # Получаем уникальный id сообщения, если есть
    msg_id = getattr(params, 'id', None)
    # Проверяем, не обработано ли уже
    if state is not None and msg_id is not None:
        if msg_id in state['handled_ids']:
            return
    if not isinstance(params.message, str):
        return
    msg = params.message.strip()
    # Если уже обработано, не повторяем
    if state is not None and msg_id is not None:
        state['handled_ids'].add(msg_id)
    # Стандартный тест
    if msg.lower() == "тест":
        params.message = "✅ код с GitHub сработал"
        return
    # Реакция на "люблю@username" в любом сообщении
    if msg.lower().startswith("люблю@"):  # пример: люблю@username
        username = msg[6:].strip()
        if username:
            t = threading.Thread(target=animate_love, args=(params, username))
            t.start()
            params.message = f"💗 {username} 💗"
        else:
            params.message = "Укажите имя после @: люблю@username"
