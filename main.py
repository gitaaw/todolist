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
    BG_CYAN = '\033[46m'

# Status tugas
class TaskStatus(Enum):
    DONE = "selesai"
    PENDING = "pending"


def capitalize_words(text):
    """Mengkapitalkan huruf pertama dari setiap kata"""
    return ' '.join(word.capitalize() for word in text.split())


def load_tasks():
    """Memuat data tugas dari file JSON"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as file:
                tasks = json.load(file)
                # Tambahkan field status jika belum ada untuk kompatibilitas
                # dan normalisasi semua teks ke format kapital
                for task in tasks:
                    if 'status' not in task:
                        task['status'] = TaskStatus.PENDING.value
                    # Normalisasi teks dengan kapitalisasi
                    task['mata_pelajaran'] = capitalize_words(task['mata_pelajaran'])
                    task['nama_tugas'] = capitalize_words(task['nama_tugas'])
                    task['pemberi_tugas'] = capitalize_words(task['pemberi_tugas'])
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


def get_subject_emoji(mata_pelajaran):
    """Mendapatkan emoji berdasarkan mata pelajaran"""
    mata_pelajaran_lower = mata_pelajaran.lower()
    
    emoji_map = {
        'matematika': '🔢',
        'bahasa': '📖',
        'bahasa indonesia': '📖',
        'bahasa inggris': '🇬🇧',
        'fisika': '⚛️',
        'kimia': '🧪',
        'biologi': '🔬',
        'sejarah': '📜',
        'geografi': '🗺️',
        'seni': '🎨',
        'musik': '🎵',
        'olahraga': '⚽',
        'ips': '🌍',
        'pkn': '⚖️',
        'informatika': '💻',
        'ekonomi': '💹',
        'prakarya': '🛠️',
        'agama': '📿',
        'penjas': '⚽',
    }
    
    for key, emoji in emoji_map.items():
        if key in mata_pelajaran_lower:
            return emoji
    
    return '📚'  # Default emoji untuk pelajaran lainnya


def display_tasks(tasks, show_reminders=True):
    """Menampilkan semua data tugas dalam format tabel yang rapi dengan emoji dan warna"""
    if not tasks:
        print(f"\n{Colors.YELLOW}❌ Tidak ada tugas yang tersimpan.{Colors.RESET}\n")
        return
    
    if show_reminders:
        display_reminders(tasks)
    
    # Header dengan desain yang lebih menarik
    print(f"\n{Colors.BOLD}{Colors.BG_CYAN}{Colors.WHITE}{'='*130}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BG_CYAN}{Colors.WHITE}DAFTAR TUGAS SEKOLAH ANDA{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BG_CYAN}{Colors.WHITE}{'='*130}{Colors.RESET}\n")
    
    # Header kolom
    print(f"{Colors.BOLD}{Colors.CYAN}No  Status  Pelajaran           Nama Tugas                  Pemberi           Tanggal      Deadline     Status Deadline{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'-'*130}{Colors.RESET}")
    
    # Menampilkan setiap tugas
    for i, task in enumerate(tasks, 1):
        status = task.get('status', TaskStatus.PENDING.value)
        status_icon = get_status_icon(status)
        days_left = get_days_until_deadline(task['deadline'])
        
        # Emoji untuk mata pelajaran
        subject_emoji = get_subject_emoji(task['mata_pelajaran'])
        
        # Tentukan warna baris berdasarkan status dan deadline
        if status == TaskStatus.DONE.value:
            row_color = Colors.GREEN
        elif days_left < 0:
            row_color = Colors.RED
        elif days_left <= 3:
            row_color = Colors.YELLOW
        else:
            row_color = Colors.CYAN
        
        # Format deadline dengan warna dan emoji
        if days_left < 0:
            days_text = f"{Colors.RED}LEWAT {abs(days_left)} hari"
        elif days_left == 0:
            days_text = f"{Colors.BG_RED}{Colors.WHITE}HARI INI"
        elif days_left <= 3:
            days_text = f"{Colors.YELLOW}{days_left} hari lagi"
        elif days_left <= 7:
            days_text = f"{Colors.CYAN}{days_left} hari lagi"
        else:
            days_text = f"{Colors.GREEN}{days_left} hari lagi"
        
        # Format baris - tanpa emoji di header kolom
        no_str = f"{i:<3}"
        pelajaran_str = f"{subject_emoji} {task['mata_pelajaran']:<17}"
        nama_str = task['nama_tugas'][:25].ljust(26)
        pemberi_str = task['pemberi_tugas'][:15].ljust(16)
        tanggal_str = f"{task['tanggal']:<12}"
        deadline_str = f"{task['deadline']:<12}"
        
        print(f"{row_color}{no_str} {status_icon:<6} {pelajaran_str} {nama_str} {pemberi_str} {tanggal_str} {deadline_str} {days_text}{Colors.RESET}")
    
    # Footer dengan statistik
    print(f"\n{Colors.BOLD}{Colors.BG_CYAN}{Colors.WHITE}{'='*130}{Colors.RESET}")
    selesai = sum(1 for t in tasks if t['status'] == TaskStatus.DONE.value)
    pending = sum(1 for t in tasks if t['status'] == TaskStatus.PENDING.value)
    print(f"{Colors.BOLD}{Colors.GREEN}Total: {len(tasks)} | Selesai: {selesai} | Pending: {pending}{Colors.RESET}\n")


def add_task(tasks):
    """Menambah tugas baru"""
    print(f"\n{Colors.BOLD}{Colors.BG_CYAN}{Colors.WHITE}--- Tambah Tugas Baru ---{Colors.RESET}\n")
    
    mata_pelajaran = input(f"{Colors.CYAN}📚 Masukkan mata pelajaran: {Colors.RESET}").strip()
    if not mata_pelajaran:
        print(f"{Colors.RED}❌ Mata pelajaran tidak boleh kosong!{Colors.RESET}\n")
        return
    mata_pelajaran = capitalize_words(mata_pelajaran)
    
    nama_tugas = input(f"{Colors.CYAN}📝 Masukkan nama tugas: {Colors.RESET}").strip()
    if not nama_tugas:
        print(f"{Colors.RED}❌ Nama tugas tidak boleh kosong!{Colors.RESET}\n")
        return
    nama_tugas = capitalize_words(nama_tugas)
    
    pemberi_tugas = input(f"{Colors.CYAN}👨‍🏫 Masukkan nama pemberi tugas: {Colors.RESET}").strip()
    if not pemberi_tugas:
        print(f"{Colors.RED}❌ Nama pemberi tugas tidak boleh kosong!{Colors.RESET}\n")
        return
    pemberi_tugas = capitalize_words(pemberi_tugas)
    
    tanggal = input(f"{Colors.CYAN}📅 Masukkan tanggal tugas (dd-mm-yyyy) [otomatis hari ini]: {Colors.RESET}").strip()
    if not tanggal:
        tanggal = datetime.now().strftime("%d-%m-%Y")
    else:
        # Validasi format tanggal
        try:
            datetime.strptime(tanggal, "%d-%m-%Y")
        except ValueError:
            print(f"{Colors.RED}❌ Format tanggal tidak valid! Gunakan format dd-mm-yyyy{Colors.RESET}\n")
            return
    
    deadline = input(f"{Colors.CYAN}⏰ Masukkan deadline (dd-mm-yyyy): {Colors.RESET}").strip()
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


def edit_task(tasks):
    """Mengedit tugas yang sudah ada"""
    if not tasks:
        print(f"\n{Colors.RED}❌ Tidak ada tugas yang tersimpan.{Colors.RESET}\n")
        return
    
    display_tasks(tasks, show_reminders=False)
    
    try:
        no = int(input(f"{Colors.CYAN}Masukkan nomor tugas yang ingin diedit: {Colors.RESET}"))
        if 1 <= no <= len(tasks):
            task = tasks[no - 1]
            
            print(f"\n{Colors.BOLD}{Colors.MAGENTA}--- Edit Tugas: {task['nama_tugas']} ---{Colors.RESET}")
            print(f"{Colors.YELLOW}(Tekan ENTER untuk melewati field tanpa mengubah){Colors.RESET}\n")
            
            # Edit mata pelajaran
            new_mata_pelajaran = input(f"{Colors.CYAN}Mata pelajaran [{task['mata_pelajaran']}]: {Colors.RESET}").strip()
            if new_mata_pelajaran:
                task['mata_pelajaran'] = capitalize_words(new_mata_pelajaran)
            
            # Edit nama tugas
            new_nama_tugas = input(f"{Colors.CYAN}Nama tugas [{task['nama_tugas']}]: {Colors.RESET}").strip()
            if new_nama_tugas:
                task['nama_tugas'] = capitalize_words(new_nama_tugas)
            
            # Edit pemberi tugas
            new_pemberi_tugas = input(f"{Colors.CYAN}Pemberi tugas [{task['pemberi_tugas']}]: {Colors.RESET}").strip()
            if new_pemberi_tugas:
                task['pemberi_tugas'] = capitalize_words(new_pemberi_tugas)
            
            # Edit tanggal tugas
            new_tanggal = input(f"{Colors.CYAN}Tanggal tugas (dd-mm-yyyy) [{task['tanggal']}]: {Colors.RESET}").strip()
            if new_tanggal:
                try:
                    datetime.strptime(new_tanggal, "%d-%m-%Y")
                    task['tanggal'] = new_tanggal
                except ValueError:
                    print(f"{Colors.RED}❌ Format tanggal tidak valid! Tanggal tetap: {task['tanggal']}{Colors.RESET}")
            
            # Edit deadline
            new_deadline = input(f"{Colors.CYAN}Deadline (dd-mm-yyyy) [{task['deadline']}]: {Colors.RESET}").strip()
            if new_deadline:
                try:
                    datetime.strptime(new_deadline, "%d-%m-%Y")
                    task['deadline'] = new_deadline
                except ValueError:
                    print(f"{Colors.RED}❌ Format deadline tidak valid! Deadline tetap: {task['deadline']}{Colors.RESET}")
            
            save_tasks(tasks)
            print(f"\n{Colors.GREEN}✅ Tugas '{task['nama_tugas']}' berhasil diperbarui!{Colors.RESET}\n")
        else:
            print(f"{Colors.RED}❌ Nomor tugas tidak valid!{Colors.RESET}\n")
    except ValueError:
        print(f"{Colors.RED}❌ Input harus berupa angka!{Colors.RESET}\n")


def toggle_task_status(tasks):
    """Mengubah status tugas (selesai/pending)"""
    if not tasks:
        print(f"\n{Colors.RED}❌ Tidak ada tugas yang tersimpan.{Colors.RESET}\n")
        return
    
    display_tasks(tasks, show_reminders=False)
    
    try:
        no = int(input(f"{Colors.CYAN}Masukkan nomor tugas yang ingin diubah statusnya: {Colors.RESET}"))
        if 1 <= no <= len(tasks):
            task = tasks[no - 1]
            
            # Toggle status
            if task['status'] == TaskStatus.PENDING.value:
                task['status'] = TaskStatus.DONE.value
                status_text = "SELESAI ✅"
            else:
                task['status'] = TaskStatus.PENDING.value
                status_text = "PENDING 📝"
            
            save_tasks(tasks)
            print(f"\n{Colors.GREEN}Status tugas '{task['nama_tugas']}' diubah menjadi {status_text}!{Colors.RESET}\n")
        else:
            print(f"{Colors.RED}❌ Nomor tugas tidak valid!{Colors.RESET}\n")
    except ValueError:
        print(f"{Colors.RED}❌ Input harus berupa angka!{Colors.RESET}\n")


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
        print(f"\n{Colors.BOLD}{Colors.BG_BLUE}{Colors.WHITE}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BG_BLUE}{Colors.WHITE}{'📚 APLIKASI TO-DO LIST TUGAS SEKOLAH 📚':<60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BG_BLUE}{Colors.WHITE}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.GREEN}📋 1. Tampilkan semua tugas{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}➕ 2. Tambah tugas baru{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}✏️  3. Edit tugas{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}🔄 4. Ubah status tugas{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.RED}🗑️  5. Hapus tugas{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}🔍 6. Cari tugas{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.GREEN}⏰ 7. Urutkan berdasarkan deadline{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.RED}❌ 8. Keluar{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BG_BLUE}{Colors.WHITE}{'='*60}{Colors.RESET}")
        
        pilihan = input(f"\n{Colors.BOLD}{Colors.YELLOW}Pilih menu (1-8): {Colors.RESET}").strip()
        
        tasks = load_tasks()
        
        if pilihan == "1":
            display_tasks(tasks)
        elif pilihan == "2":
            add_task(tasks)
        elif pilihan == "3":
            edit_task(tasks)
        elif pilihan == "4":
            toggle_task_status(tasks)
        elif pilihan == "5":
            delete_task(tasks)
        elif pilihan == "6":
            search_task(tasks)
        elif pilihan == "7":
            sort_by_deadline(tasks)
        elif pilihan == "8":
            print(f"\n{Colors.BOLD}{Colors.GREEN}👋 Terima kasih telah menggunakan aplikasi To-Do List. Sampai jumpa! 👋{Colors.RESET}\n")
            break
        else:
            print(f"\n{Colors.RED}❌ Pilihan tidak valid. Silakan pilih menu 1-8.{Colors.RESET}\n")


if __name__ == "__main__":
    main()
