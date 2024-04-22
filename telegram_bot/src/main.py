from pyrogram import Client

api_hash = "8c86aa0ee784f88a2e2b2f5fbc084f0b"
api_id = "15519192"

with Client(name="my_account", api_hash=api_hash, api_id=api_id) as app:
    app.send_message("me", "Это я бот")