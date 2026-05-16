def on_send_message_hook(account, params, state=None):
    if isinstance(params.message, str) and params.message.strip().lower() == "тест":
        params.message = "✅ код с GitHub сработал"