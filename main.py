import json
import os
from datetime import datetime

# File untuk menyimpan data tugas
DATA_FILE = "tasks.json"


def load_tasks():
    """Memuat data tugas dari file JSON"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []


def save_tasks(tasks):
    """Menyimpan data tugas ke file JSON"""
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(tasks, file, ensure_ascii=False, indent=2)


def display_tasks(tasks):
    """Menampilkan semua data tugas"""
    if not tasks:
        print("\n❌ Tidak ada tugas yang tersimpan.\n")
        return
    
    print("\n" + "=" * 100)
    print(f"{'No':<5} {'Mata Pelajaran':<20} {'Nama Tugas':<25} {'Pemberi Tugas':<20} {'Tanggal':<12} {'Deadline':<12}")
    print("=" * 100)
    
    for i, task in enumerate(tasks, 1):
        print(f"{i:<5} {task['mata_pelajaran']:<20} {task['nama_tugas']:<25} {task['pemberi_tugas']:<20} {task['tanggal']:<12} {task['deadline']:<12}")
    
    print("=" * 100 + "\n")


def add_task(tasks):
    """Menambah tugas baru"""
    print("\n--- Tambah Tugas Baru ---")
    
    mata_pelajaran = input("Masukkan mata pelajaran: ").strip()
    if not mata_pelajaran:
        print("❌ Mata pelajaran tidak boleh kosong!\n")
        return
    
    nama_tugas = input("Masukkan nama tugas: ").strip()
    if not nama_tugas:
        print("❌ Nama tugas tidak boleh kosong!\n")
        return
    
    pemberi_tugas = input("Masukkan nama pemberi tugas: ").strip()
    if not pemberi_tugas:
        print("❌ Nama pemberi tugas tidak boleh kosong!\n")
        return
    
    tanggal = input("Masukkan tanggal tugas (dd-mm-yyyy) [otomatis hari ini]: ").strip()
    if not tanggal:
        tanggal = datetime.now().strftime("%d-%m-%Y")
    else:
        # Validasi format tanggal
        try:
            datetime.strptime(tanggal, "%d-%m-%Y")
        except ValueError:
            print("❌ Format tanggal tidak valid! Gunakan format dd-mm-yyyy\n")
            return
    
    deadline = input("Masukkan deadline (dd-mm-yyyy): ").strip()
    if not deadline:
        print("❌ Deadline tidak boleh kosong!\n")
        return
    else:
        # Validasi format deadline
        try:
            datetime.strptime(deadline, "%d-%m-%Y")
        except ValueError:
            print("❌ Format deadline tidak valid! Gunakan format dd-mm-yyyy\n")
            return
    
    task = {
        "mata_pelajaran": mata_pelajaran,
        "nama_tugas": nama_tugas,
        "pemberi_tugas": pemberi_tugas,
        "tanggal": tanggal,
        "deadline": deadline
    }
    
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Tugas '{nama_tugas}' berhasil ditambahkan!\n")


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
