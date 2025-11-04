import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from config import get_gmail_config

def send_email(to_email, subject, body):
    """
    Mengirim email menggunakan SMTP Gmail
    """
    # Mendapatkan konfigurasi Gmail
    gmail_config = get_gmail_config()
    sender_email = gmail_config["email"]
    app_password = gmail_config["app_password"]
    
    # Membuat objek pesan
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    
    # Menambahkan body ke pesan
    message.attach(MIMEText(body, "plain"))
    
    try:
        # Membuat koneksi SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Mengaktifkan enkripsi TLS
        server.login(sender_email, app_password)
        
        # Mengirim email
        text = message.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
        
        return True, "Email berhasil dikirim"
    except Exception as e:
        return False, str(e)

def validate_email(email):
    """
    Validasi sederhana untuk format email
    """
    return "@" in email and "." in email and len(email) > 5

def format_time(seconds):
    """
    Memformat waktu dalam format yang mudah dibaca
    """
    if seconds < 60:
        return f"{seconds:.1f} detik"
    elif seconds < 3600:
        return f"{seconds/60:.1f} menit"
    else:
        return f"{seconds/3600:.1f} jam"

def clear_screen():
    """
    Membersihkan layar terminal
    """
    import os
    os.system('cls' if os.name == 'nt' else 'clear')