import json
import os
from datetime import datetime, timedelta
from enum import Enum

# File untuk menyimpan data tugas
DATA_FILE = "tasks.json"

# Konstanta untuk warna terminal (ANSI codes)
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'

# Status tugas
class TaskStatus(Enum):
    DONE = "selesai"
    PENDING = "pending"


def load_tasks():
    """Memuat data tugas dari file JSON"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as file:
                tasks = json.load(file)
                # Tambahkan field status jika belum ada untuk kompatibilitas
                for task in tasks:
                    if 'status' not in task:
                        task['status'] = TaskStatus.PENDING.value
                return tasks
        except json.JSONDecodeError:
            return []
    return []


def save_tasks(tasks):
    """Menyimpan data tugas ke file JSON"""
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(tasks, file, ensure_ascii=False, indent=2)


def get_days_until_deadline(deadline_str):
    """Menghitung jumlah hari hingga deadline"""
    try:
        deadline = datetime.strptime(deadline_str, "%d-%m-%Y")
        today = datetime.now()
        days = (deadline - today).days
        return days
    except ValueError:
        return float('inf')


def get_status_icon(status):
    """Mendapatkan icon berdasarkan status tugas"""
    if status == TaskStatus.DONE.value:
        return "✅"
    else:
        return "📝"


def get_deadline_color(days_left):
    """Mendapatkan warna berdasarkan jarak deadline"""
    if days_left < 0:
        return Colors.RED  # Sudah lewat
    elif days_left == 0:
        return Colors.BG_RED + Colors.WHITE  # Hari ini
    elif days_left <= 3:
        return Colors.YELLOW  # Sangat dekat
    elif days_left <= 7:
        return Colors.CYAN  # Dekat
    else:
        return Colors.GREEN  # Masih lama


def check_reminders(tasks):
    """Mengecek dan menampilkan pengingat untuk deadline yang akan datang"""
    reminders = []
    
    for i, task in enumerate(tasks):
        days_left = get_days_until_deadline(task['deadline'])
        
        if days_left < 0:
            reminders.append({
                'index': i,
                'nama_tugas': task['nama_tugas'],
                'deadline': task['deadline'],
                'days_left': days_left,
                'tipe': '⚠️ LEWAT'
            })
        elif days_left == 0:
            reminders.append({
                'index': i,
                'nama_tugas': task['nama_tugas'],
                'deadline': task['deadline'],
                'days_left': days_left,
                'tipe': '🔴 HARI INI'
            })
        elif days_left <= 3:
            reminders.append({
                'index': i,
                'nama_tugas': task['nama_tugas'],
                'deadline': task['deadline'],
                'days_left': days_left,
                'tipe': '🟠 3 HARI LAGI'
            })
        elif days_left <= 7:
            reminders.append({
                'index': i,
                'nama_tugas': task['nama_tugas'],
                'deadline': task['deadline'],
                'days_left': days_left,
                'tipe': '🟡 DALAM SEMINGGU'
            })
    
    return reminders


def display_reminders(tasks):
    """Menampilkan pengingat deadline"""
    reminders = check_reminders(tasks)
    
    if not reminders:
        print(f"{Colors.GREEN}✅ Tidak ada deadline yang mendesak.{Colors.RESET}\n")
        return
    
    print(f"\n{Colors.BOLD}{Colors.RED}{'='*80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.RED}⏰ PENGINGAT DEADLINE YANG MENDESAK{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.RED}{'='*80}{Colors.RESET}\n")
    
    for reminder in reminders:
        print(f"{reminder['tipe']} {Colors.BOLD}{reminder['nama_tugas']}{Colors.RESET}")
        print(f"   📅 Deadline: {reminder['deadline']} ({reminder['days_left']} hari)")
        print()


def display_tasks(tasks, show_reminders=True):
    """Menampilkan semua data tugas dalam format tabel yang rapi"""
    if not tasks:
        print(f"\n{Colors.YELLOW}❌ Tidak ada tugas yang tersimpan.{Colors.RESET}\n")
        return
    
    if show_reminders:
        display_reminders(tasks)
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*130}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'No':<4} {'Status':<8} {'Mata Pelajaran':<18} {'Nama Tugas':<28} {'Pemberi Tugas':<16} {'Tanggal':<12} {'Deadline':<12} {'Hari ke Deadline':<17}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*130}{Colors.RESET}")
    
    for i, task in enumerate(tasks, 1):
        status_icon = get_status_icon(task.get('status', TaskStatus.PENDING.value))
        days_left = get_days_until_deadline(task['deadline'])
        
        # Tentukan warna deadline
        color = get_deadline_color(days_left)
        
        # Format hari ke deadline
        if days_left < 0:
            days_text = f"{color}LEWAT {abs(days_left)} hari{Colors.RESET}"
        elif days_left == 0:
            days_text = f"{color}HARI INI{Colors.RESET}"
        else:
            days_text = f"{color}{days_left} hari lagi{Colors.RESET}"
        
        print(f"{i:<4} {status_icon:<8} {task['mata_pelajaran']:<18} {task['nama_tugas']:<28} {task['pemberi_tugas']:<16} {task['tanggal']:<12} {task['deadline']:<12} {days_text:<17}")
    
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*130}{Colors.RESET}\n")


def add_task(tasks):
    """Menambah tugas baru"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}--- Tambah Tugas Baru ---{Colors.RESET}")
    
    mata_pelajaran = input(f"{Colors.CYAN}Masukkan mata pelajaran: {Colors.RESET}").strip()
    if not mata_pelajaran:
        print(f"{Colors.RED}❌ Mata pelajaran tidak boleh kosong!{Colors.RESET}\n")
        return
    
    nama_tugas = input(f"{Colors.CYAN}Masukkan nama tugas: {Colors.RESET}").strip()
    if not nama_tugas:
        print(f"{Colors.RED}❌ Nama tugas tidak boleh kosong!{Colors.RESET}\n")
        return
    
    pemberi_tugas = input(f"{Colors.CYAN}Masukkan nama pemberi tugas: {Colors.RESET}").strip()
    if not pemberi_tugas:
        print(f"{Colors.RED}❌ Nama pemberi tugas tidak boleh kosong!{Colors.RESET}\n")
        return
    
    tanggal = input(f"{Colors.CYAN}Masukkan tanggal tugas (dd-mm-yyyy) [otomatis hari ini]: {Colors.RESET}").strip()
    if not tanggal:
        tanggal = datetime.now().strftime("%d-%m-%Y")
    else:
        # Validasi format tanggal
        try:
            datetime.strptime(tanggal, "%d-%m-%Y")
        except ValueError:
            print(f"{Colors.RED}❌ Format tanggal tidak valid! Gunakan format dd-mm-yyyy{Colors.RESET}\n")
            return
    
    deadline = input(f"{Colors.CYAN}Masukkan deadline (dd-mm-yyyy): {Colors.RESET}").strip()
    if not deadline:
        print(f"{Colors.RED}❌ Deadline tidak boleh kosong!{Colors.RESET}\n")
        return
    else:
        # Validasi format deadline
        try:
            datetime.strptime(deadline, "%d-%m-%Y")
        except ValueError:
            print(f"{Colors.RED}❌ Format deadline tidak valid! Gunakan format dd-mm-yyyy{Colors.RESET}\n")
            return
    
    task = {
        "mata_pelajaran": mata_pelajaran,
        "nama_tugas": nama_tugas,
        "pemberi_tugas": pemberi_tugas,
        "tanggal": tanggal,
        "deadline": deadline,
        "status": TaskStatus.PENDING.value
    }
    
    tasks.append(task)
    save_tasks(tasks)
    print(f"{Colors.GREEN}✅ Tugas '{nama_tugas}' berhasil ditambahkan!{Colors.RESET}\n")


def delete_task(tasks):
    """Menghapus tugas"""
    if not tasks:
        print("\n❌ Tidak ada tugas yang tersimpan.\n")
        return
    
    display_tasks(tasks)
    
    try:
        no = int(input("Masukkan nomor tugas yang ingin dihapus: "))
        if 1 <= no <= len(tasks):
            deleted_task = tasks.pop(no - 1)
            save_tasks(tasks)
            print(f"✅ Tugas '{deleted_task['nama_tugas']}' berhasil dihapus!\n")
        else:
            print("❌ Nomor tugas tidak valid!\n")
    except ValueError:
        print("❌ Input harus berupa angka!\n")


def search_task(tasks):
    """Mencari tugas berdasarkan nama atau mata pelajaran"""
    if not tasks:
        print("\n❌ Tidak ada tugas yang tersimpan.\n")
        return
    
    keyword = input("\nMasukkan kata kunci pencarian (nama tugas atau mata pelajaran): ").strip().lower()
    
    results = [task for task in tasks if keyword in task['nama_tugas'].lower() or keyword in task['mata_pelajaran'].lower()]
    
    if results:
        print("\n" + "=" * 100)
        print(f"{'No':<5} {'Mata Pelajaran':<20} {'Nama Tugas':<25} {'Pemberi Tugas':<20} {'Tanggal':<12} {'Deadline':<12}")
        print("=" * 100)
        
        for i, task in enumerate(results, 1):
            print(f"{i:<5} {task['mata_pelajaran']:<20} {task['nama_tugas']:<25} {task['pemberi_tugas']:<20} {task['tanggal']:<12} {task['deadline']:<12}")
        
        print("=" * 100 + "\n")
    else:
        print(f"❌ Tidak ada tugas yang sesuai dengan kata kunci '{keyword}'.\n")


def sort_by_deadline(tasks):
    """Menampilkan tugas yang diurutkan berdasarkan deadline"""
    if not tasks:
        print("\n❌ Tidak ada tugas yang tersimpan.\n")
        return
    
    sorted_tasks = sorted(tasks, key=lambda x: datetime.strptime(x['deadline'], "%d-%m-%Y"))
    
    print("\n" + "=" * 100)
    print("Tugas yang diurutkan berdasarkan DEADLINE (dari yang paling dekat):")
    print("=" * 100)
    print(f"{'No':<5} {'Mata Pelajaran':<20} {'Nama Tugas':<25} {'Pemberi Tugas':<20} {'Tanggal':<12} {'Deadline':<12}")
    print("=" * 100)
    
    for i, task in enumerate(sorted_tasks, 1):
        print(f"{i:<5} {task['mata_pelajaran']:<20} {task['nama_tugas']:<25} {task['pemberi_tugas']:<20} {task['tanggal']:<12} {task['deadline']:<12}")
    
    print("=" * 100 + "\n")


def main():
    """Menu utama aplikasi"""
    while True:
        print("\n" + "="*50)
        print("      APLIKASI TO-DO LIST TUGAS SEKOLAH")
        print("="*50)
        print("1. Tampilkan semua tugas")
        print("2. Tambah tugas baru")
        print("3. Hapus tugas")
        print("4. Cari tugas")
        print("5. Urutkan berdasarkan deadline")
        print("6. Keluar")
        print("="*50)
        
        pilihan = input("Pilih menu (1-6): ").strip()
        
        tasks = load_tasks()
        
        if pilihan == "1":
            display_tasks(tasks)
        elif pilihan == "2":
            add_task(tasks)
        elif pilihan == "3":
            delete_task(tasks)
        elif pilihan == "4":
            search_task(tasks)
        elif pilihan == "5":
            sort_by_deadline(tasks)
        elif pilihan == "6":
            print("\n👋 Terima kasih telah menggunakan aplikasi To-Do List. Sampai jumpa!\n")
            break
        else:
            print("\n❌ Pilihan tidak valid. Silakan pilih menu 1-6.\n")


if __name__ == "__main__":
    main()
