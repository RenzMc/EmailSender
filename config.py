import json
import os

# File konfigurasi
CONFIG_FILE = "config.json"

# Struktur default konfigurasi
DEFAULT_CONFIG = {
    "gmail": {
        "email": "",
        "app_password": ""
    },
    "messages": [
        {
            "subject": "Promosi Menarik!",
            "body": "Halo, kami memiliki penawaran menarik untuk Anda."
        }
    ]
}

def load_config():
    """Memuat konfigurasi dari file JSON"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()

def save_config(config):
    """Menyimpan konfigurasi ke file JSON"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def get_gmail_config():
    """Mendapatkan konfigurasi Gmail"""
    config = load_config()
    return config.get("gmail", {"email": "", "app_password": ""})

def set_gmail_config(email, app_password):
    """Menyimpan konfigurasi Gmail"""
    config = load_config()
    config["gmail"] = {
        "email": email,
        "app_password": app_password
    }
    save_config(config)

def get_messages():
    """Mendapatkan daftar pesan"""
    config = load_config()
    return config.get("messages", [])

def add_message(subject, body):
    """Menambahkan pesan baru"""
    config = load_config()
    if "messages" not in config:
        config["messages"] = []
    
    config["messages"].append({
        "subject": subject,
        "body": body
    })
    save_config(config)

def clear_messages():
    """Menghapus semua pesan"""
    config = load_config()
    config["messages"] = []
    save_config(config)

def delete_message(index):
    """Menghapus pesan berdasarkan index"""
    config = load_config()
    if 0 <= index < len(config.get("messages", [])):
        config["messages"].pop(index)
        save_config(config)
        return True
    return False