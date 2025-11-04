#!/usr/bin/env python3

import signal
import sys
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from menu import show_main_menu, show_settings_menu, gmail_settings, message_settings
from config import get_gmail_config, get_messages
from utils import send_email, validate_email, format_time
import time

console = Console()

def signal_handler(sig, frame):
    """Menangani interupsi Ctrl+C"""
    console.print("\n\n[yellow]Terima kasih telah menggunakan EmailSender![/yellow]")
    console.print("[cyan]Sampai jumpa lagi![/cyan]")
    sys.exit(0)

def run_email_sender():
    """Fungsi utama untuk mengirim email"""
    clear_screen()
    
    # Memeriksa konfigurasi
    gmail_config = get_gmail_config()
    messages = get_messages()
    
    if not gmail_config["email"] or not gmail_config["app_password"]:
        console.print("[red]Konfigurasi Gmail belum lengkap![/red]")
        console.print("Silakan atur akun Gmail di menu Setting Tools.")
        return
    
    if not messages:
        console.print("[red]Belum ada pesan yang disimpan![/red]")
        console.print("Silakan tambahkan pesan di menu Setting Tools.")
        return
    
    console.print("[bold blue]Run Email Sender[/bold blue]")
    
    # Meminta jumlah pengiriman
    try:
        send_count = IntPrompt.ask("Jumlah pengiriman (per pesan)", default=1)
        if send_count <= 0:
            console.print("[red]Jumlah pengiriman harus lebih dari 0![/red]")
            return
    except Exception:
        console.print("[red]Masukkan angka yang valid![/red]")
        return
    
    # Meminta email tujuan
    target_emails_input = Prompt.ask("Email tujuan (pisahkan dengan koma jika lebih dari satu)")
    target_emails = [email.strip() for email in target_emails_input.split(",") if email.strip()]
    
    if not target_emails:
        console.print("[red]Minimal harus ada satu email tujuan![/red]")
        return
    
    # Validasi email tujuan
    invalid_emails = [email for email in target_emails if not validate_email(email)]
    if invalid_emails:
        console.print(f"[red]Email tidak valid: {', '.join(invalid_emails)}[/red]")
        return
    
    console.print(f"\n[green]Siap mengirim {len(messages)} pesan ke {len(target_emails)} email sebanyak {send_count} kali per pesan[/green]")
    console.print("[yellow]Total pengiriman: {}[/yellow]".format(len(messages) * len(target_emails) * send_count))
    
    confirm = Prompt.ask("Lanjutkan pengiriman? (y/N)", default="N")
    if confirm.lower() != "y":
        console.print("[yellow]Pengiriman dibatalkan.[/yellow]")
        return
    
    # Proses pengiriman
    start_time = time.time()
    sent_count = 0
    failed_count = 0
    
    try:
        with console.status("[bold green]Mengirim email...", spinner="clock") as status:
            for msg in messages:
                subject = msg["subject"]
                body = msg["body"]
                
                for _ in range(send_count):
                    for email in target_emails:
                        status.update(f"[bold green]Mengirim: {subject} ke {email}...")
                        
                        success, message = send_email(email, subject, body)
                        
                        if success:
                            sent_count += 1
                            console.print(f"[green]✓[/green] {subject} -> {email}")
                        else:
                            failed_count += 1
                            console.print(f"[red]✗[/red] {subject} -> {email} ({message})")
                        
                        # Jeda kecil untuk menghindari rate limit
                        time.sleep(1)
        
        # Menampilkan hasil
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        console.print("[bold]" + f"""
[yellow]Statistik Pengiriman:[/yellow]
[green]Berhasil:[/green] {sent_count}
[red]Gagal:[/red] {failed_count}
[blue]Waktu:[/blue] {format_time(elapsed_time)}
        """ + "[/bold]")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Pengiriman dihentikan oleh pengguna.[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Terjadi kesalahan: {str(e)}[/red]")

def clear_screen():
    """Membersihkan layar terminal"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """Fungsi utama aplikasi"""
    # Mengatur penangan sinyal untuk Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    while True:
        try:
            show_main_menu()
            choice = Prompt.ask("\nPilih menu", choices=["1", "2", "3"])
            
            if choice == "1":
                run_email_sender()
                Prompt.ask("Tekan Enter untuk kembali ke menu utama")
            elif choice == "2":
                while True:
                    setting_choice = show_settings_menu()
                    if setting_choice == "1":
                        gmail_settings()
                        Prompt.ask("Tekan Enter untuk kembali ke menu pengaturan")
                    elif setting_choice == "2":
                        message_settings()
                    elif setting_choice == "3":
                        break
            elif choice == "3":
                console.print("\n[yellow]Terima kasih telah menggunakan EmailSender![/yellow]")
                console.print("[cyan]Sampai jumpa lagi![/cyan]")
                break
        except KeyboardInterrupt:
            signal_handler(None, None)
        except Exception as e:
            console.print(f"\n[red]Terjadi kesalahan: {str(e)}[/red]")
            Prompt.ask("Tekan Enter untuk melanjutkan")

if __name__ == "__main__":
    main()