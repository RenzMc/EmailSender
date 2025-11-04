import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from config import get_gmail_config, set_gmail_config, get_messages, add_message, clear_messages, delete_message
from utils import validate_email, clear_screen

console = Console()

def show_ascii_art():
    """Menampilkan ASCII art keren"""
    ascii_art = """

╭━━━╮╱╱╱╱╱╱╭╮╭━━━╮╱╱╱╱╱╱╱╭╮
┃╭━━╯╱╱╱╱╱╱┃┃┃╭━╮┃╱╱╱╱╱╱╱┃┃
┃╰━━┳╮╭┳━━┳┫┃┃╰━━┳━━┳━╮╭━╯┣━━┳━╮
┃╭━━┫╰╯┃╭╮┣┫┃╰━━╮┃┃━┫╭╮┫╭╮┃┃━┫╭╯
┃╰━━┫┃┃┃╭╮┃┃╰┫╰━╯┃┃━┫┃┃┃╰╯┃┃━┫┃
╰━━━┻┻┻┻╯╰┻┻━┻━━━┻━━┻╯╰┻━━┻━━┻╯
    """
    console.print(ascii_art, style="bold blue")

def show_main_menu():
    """Menampilkan menu utama"""
    clear_screen()
    show_ascii_art()
    
    table = Table(title="Menu Utama", show_header=True, header_style="bold magenta")
    table.add_column("No", style="cyan", width=5)
    table.add_column("Menu", style="green")
    table.add_column("Deskripsi", style="yellow")
    
    table.add_row("1", "Run Tools", "Mulai mengirim email promosi")
    table.add_row("2", "Setting Tools", "Konfigurasi akun dan pesan")
    table.add_row("3", "Exit", "Keluar dari aplikasi")
    
    console.print(table)
    console.print("[italic dim]Gunakan Ctrl+C untuk keluar kapan saja[/italic dim]")

def show_settings_menu():
    """Menampilkan menu pengaturan"""
    clear_screen()
    show_ascii_art()
    
    # Menampilkan konfigurasi saat ini
    gmail_config = get_gmail_config()
    messages = get_messages()
    
    console.print("[bold blue]Konfigurasi Saat Ini[/bold blue]")
    
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Item", style="magenta")
    table.add_column("Value", style="green")
    
    table.add_row("Email Pengirim", gmail_config["email"] or "Belum diatur")
    table.add_row("App Password", "********" if gmail_config["app_password"] else "Belum diatur")
    table.add_row("Jumlah Pesan", str(len(messages)))
    
    console.print(table)
    
    # Menu pengaturan
    console.print("\n[bold cyan]Pengaturan:[/bold cyan]")
    console.print("1. Atur Akun Gmail")
    console.print("2. Kelola Pesan")
    console.print("3. Kembali ke Menu Utama")
    
    return Prompt.ask("Pilih menu", choices=["1", "2", "3"])

def gmail_settings():
    """Menu pengaturan akun Gmail"""
    clear_screen()
    show_ascii_art()
    
    console.print(Panel("Pengaturan Akun Gmail", style="bold blue"))
    
    current_config = get_gmail_config()
    if current_config["email"]:
        console.print(f"Email saat ini: [green]{current_config['email']}[/green]")
    
    email = Prompt.ask("Masukkan email Gmail")
    if not validate_email(email):
        console.print("[red]Format email tidak valid![/red]")
        return
    
    app_password = Prompt.ask("Masukkan App Password Gmail", password=True)
    
    set_gmail_config(email, app_password)
    console.print("[green]Konfigurasi Gmail berhasil disimpan![/green]")

def message_settings():
    """Menu pengaturan pesan"""
    while True:
        clear_screen()
        show_ascii_art()
        
        console.print("[bold blue]Pengaturan Pesan[/bold blue]")
        
        messages = get_messages()
        
        if messages:
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("No", style="magenta", width=3)
            table.add_column("Subject", style="green")
            table.add_column("Preview", style="yellow")
            
            for i, msg in enumerate(messages):
                preview = msg["body"][:50] + "..." if len(msg["body"]) > 50 else msg["body"]
                table.add_row(str(i+1), msg["subject"], preview)
            
            console.print(table)
        else:
            console.print("[yellow]Belum ada pesan yang disimpan.[/yellow]")
        
        console.print("\n[bold cyan]Opsi:[/bold cyan]")
        console.print("1. Tambah Pesan")
        console.print("2. Hapus Pesan")
        console.print("3. Hapus Semua Pesan")
        console.print("4. Kembali ke Menu Pengaturan")
        
        choice = Prompt.ask("Pilih opsi", choices=["1", "2", "3", "4"])
        
        if choice == "1":
            add_new_message()
        elif choice == "2":
            delete_specific_message(messages)
        elif choice == "3":
            clear_all_messages()
        elif choice == "4":
            break

def add_new_message():
    """Menambahkan pesan baru"""
    console.print("\n[bold blue]Tambah Pesan Baru:[/bold blue]")
    subject = Prompt.ask("Subject")
    body = Prompt.ask("Body")
    
    add_message(subject, body)
    console.print("[green]Pesan berhasil ditambahkan![/green]")
    Prompt.ask("Tekan Enter untuk melanjutkan")

def delete_specific_message(messages):
    """Menghapus pesan tertentu"""
    if not messages:
        console.print("[yellow]Tidak ada pesan untuk dihapus.[/yellow]")
        Prompt.ask("Tekan Enter untuk melanjutkan")
        return
    
    try:
        index = IntPrompt.ask("Masukkan nomor pesan yang akan dihapus") - 1
        if 0 <= index < len(messages):
            if delete_message(index):
                console.print("[green]Pesan berhasil dihapus![/green]")
            else:
                console.print("[red]Gagal menghapus pesan![/red]")
        else:
            console.print("[red]Nomor pesan tidak valid![/red]")
    except ValueError:
        console.print("[red]Masukkan angka yang valid![/red]")
    
    Prompt.ask("Tekan Enter untuk melanjutkan")

def clear_all_messages():
    """Menghapus semua pesan"""
    confirm = Prompt.ask("Yakin ingin menghapus semua pesan? (y/N)", default="N")
    if confirm.lower() == "y":
        clear_messages()
        console.print("[green]Semua pesan berhasil dihapus![/green]")
    else:
        console.print("[yellow]Penghapusan dibatalkan.[/yellow]")
    
    Prompt.ask("Tekan Enter untuk melanjutkan")