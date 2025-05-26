import csv
import os
print("File disimpan di folder:", os.getcwd())

def simpan_ke_csv(nama_file="data_peserta1.csv"):
    with open(nama_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nama', 'Email', 'Instansi', 'No_Telepon', 'Hadir'])  # header
        for p in dataPeserta:
            writer.writerow([p.nama, p.email, p.instansi, p.no_telepon, p.hadir])

def muat_dari_csv(nama_file="data_peserta1.csv"):
    try:
        with open(nama_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                peserta = Peserta(
                    nama=row['Nama'],
                    email=row['Email'],
                    instansi=row['Instansi'],
                    no_telepon=int(row['No_Telepon']),
                    hadir=(row['Hadir'].lower() == 'true')
                )
                dataPeserta.append(peserta)
    except FileNotFoundError:
        pass  # File belum ada, tidak apa-apa

MAX_PESERTA = 100

class Peserta:
    def __init__(self, nama='', email='', instansi='', no_telepon=0, hadir=False):
        self.nama = str(nama)  # Ubah ke string
        self.email = email
        self.instansi = instansi
        self.no_telepon = int(no_telepon)  # Ubah ke integer
        self.hadir = hadir

nama_kegiatan = ""
tanggal_kegiatan = ""
penyelenggara = ""
dataPeserta = []

def tambah_peserta(nama, email, instansi, no_telepon, hadir):
    if len(dataPeserta) >= MAX_PESERTA:
        return "Data peserta sudah penuh."
    
    for peserta in dataPeserta:
        if peserta.email == email:
            return "❗ Email sudah digunakan oleh peserta lain."
        if peserta.no_telepon == int(no_telepon):
            return "❗ Nomor telepon sudah digunakan oleh peserta lain."

    peserta = Peserta(nama, email, instansi, int(no_telepon), hadir)
    dataPeserta.append(peserta)
    simpan_ke_csv()
    return "Peserta berhasil ditambahkan."

def edit_peserta(nama_target, nama_baru, email_baru, instansi_baru, no_telepon_baru, hadir_baru):
    for peserta in dataPeserta:
        if peserta.nama == nama_target:
            for p in dataPeserta:
                if p.nama != nama_target:
                    if p.email == email_baru:
                        return "❗ Email sudah digunakan oleh peserta lain."
                    if p.no_telepon == int(no_telepon_baru):
                        return "❗ Nomor telepon sudah digunakan oleh peserta lain."

            peserta.nama = nama_baru
            peserta.email = email_baru
            peserta.instansi = instansi_baru
            peserta.no_telepon = int(no_telepon_baru)
            peserta.hadir = hadir_baru
            simpan_ke_csv()
            return "Peserta berhasil diubah."
    return "Peserta dengan nama tersebut tidak ditemukan."

def hapus_peserta_sequential(nama_target):
    for i in range(len(dataPeserta)):
        if dataPeserta[i].nama == nama_target:
            del dataPeserta[i]
            return "Peserta berhasil dihapus."
    return "Peserta dengan nama tersebut tidak ditemukan."
    simpan_ke_csv()

def sort_peserta(mode='asc'): #Ubah bentuknya menjadi kolom yang langsung bisa dipilih
    n = len(dataPeserta)
    if mode == 'asc':
        for i in range(n - 1):
            min_idx = i
            for j in range(i + 1, n):
                if dataPeserta[j].nama < dataPeserta[min_idx].nama:
                    min_idx = j
            dataPeserta[i], dataPeserta[min_idx] = dataPeserta[min_idx], dataPeserta[i]
    elif mode == 'desc':
        for i in range(1, n):
            key = dataPeserta[i]
            j = i - 1
            while j >= 0 and dataPeserta[j].nama < key.nama:
                dataPeserta[j + 1] = dataPeserta[j]
                j -= 1
            dataPeserta[j + 1] = key
    else:
        return "Mode tidak valid. Gunakan 'asc' atau 'desc'."
    
def reset_data():
    confirm = messagebox.askyesno("Konfirmasi Reset", "Yakin ingin menghapus semua data peserta?")
    if confirm:
        dataPeserta.clear()
        simpan_ke_csv()  # Ini akan menulis ulang file hanya dengan header
        refresh_list()
        messagebox.showinfo("Reset Berhasil", "Semua data peserta telah dihapus.")
        
def cari_peserta_sequential(keyword):
    hasil = []
    keyword = keyword.lower()
    for peserta in dataPeserta:
        if keyword in peserta.nama.lower():
            hasil.append(peserta)
    return hasil


# BUAT GUI TAMPILAN SEMACAM LOGIN WELCOME
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
    
def refresh_list():
    listbox.delete(*listbox.get_children())
    keyword = search_var.get().lower()
    hasil_pencarian = cari_peserta_sequential(keyword)
    count = 0
    for idx, p in enumerate(hasil_pencarian):
        status_hadir = "Hadir" if p.hadir else "Tidak Hadir"
        listbox.insert("", "end", values=(idx+1, p.nama, p.email, p.instansi, p.no_telepon, status_hadir))
        count += 1
    jumlah_label.config(text=f"👥 Jumlah Peserta: {count} orang")

def form_peserta(is_edit=False, peserta=None, idx_edit=None):
    top = tk.Toplevel(root)
    top.title("Form Peserta")
    top.geometry("400x450")
    top.config(bg="#FDFCE8")
    top.grab_set()

    lbl_title = tk.Label(top, text="Form Peserta", font=("Segoe UI", 14, 'bold'), bg="#FDFCE8")
    lbl_title.pack(pady=10)

    frame_form = tk.Frame(top, bg="#FDFCE8")
    frame_form.pack(padx=20, pady=5, fill='both')

    labels = ['Nama', 'Email', 'Instansi', 'No Telepon']
    entries = {}

    for i, lbl in enumerate(labels):
        l = tk.Label(frame_form, text=lbl, bg="#FDFCE8", anchor='w')
        l.grid(row=i, column=0, sticky='w', pady=5)
        e = tk.Entry(frame_form, width=30)
        e.grid(row=i, column=1, pady=5)
        entries[lbl] = e

    hadir_var = tk.BooleanVar(value=True)  

    if is_edit and peserta:
        entries['Nama'].insert(0, peserta.nama)
        entries['Email'].insert(0, peserta.email)
        entries['Instansi'].insert(0, peserta.instansi)
        entries['No Telepon'].insert(0, peserta.no_telepon)
        hadir_var.set(peserta.hadir)

    def submit():
        values = [entries[f].get().strip() for f in labels]
        hadir = hadir_var.get()
        if all(values):
            no_telepon = values[3]
            if not no_telepon.isdigit():
                messagebox.showwarning("Input Salah", "Nomor Telepon harus berupa angka saja.")
                return

            if not all(c.isalpha() or c.isspace() for c in values[0]) or values[0].strip() == "":
                messagebox.showwarning("Input Salah", "Nama hanya boleh berisi huruf dan spasi.")
                return

            if is_edit:
                hasil = edit_peserta(peserta.nama, *values, hadir)
            else:
                hasil = tambah_peserta(*values, hadir)

            if "berhasil" in hasil.lower():
                messagebox.showinfo("Sukses", hasil)
                refresh_list()
                top.destroy()
            else:
                messagebox.showwarning("Peringatan", hasil)
        else:
            messagebox.showwarning("Input Salah", "Semua data wajib diisi.")

    btn_text = "Ubah" if is_edit else "Tambah"
    btn_submit = ttk.Button(top, text=btn_text, command=submit)

    btn_submit.pack(pady=15)

def tambah_gui():
    form_peserta()
    
def edit_gui():
    selected = listbox.selection()
    if selected:
        idx = int(listbox.item(selected)['values'][0]) - 1
        p = dataPeserta[idx]
        form_peserta(is_edit=True, peserta=p, idx_edit=idx)
    else:
        messagebox.showwarning("Pilih Data", "Pilih peserta yang ingin diedit.")

def hapus_gui():
    selected = listbox.selection()
    if selected:
        idx = int(listbox.item(selected)['values'][0]) - 1
        p = dataPeserta[idx]
        confirm = messagebox.askyesno("Konfirmasi", f"Yakin hapus peserta '{p.nama}'?")
        if confirm:
            hapus_peserta_sequential(p.nama)
            refresh_list()
            messagebox.showinfo("Sukses", "Peserta berhasil dihapus.")
    else:
        messagebox.showwarning("Pilih Data", "Pilih peserta yang ingin dihapus.")

def urutkan_gui():
    def apply_sort():
        mode = mode_var.get()
        if mode in ['asc', 'desc']:
            sort_peserta(mode)
            refresh_list()
            messagebox.showinfo("Info", f"Data diurutkan ({mode}).")
            top.destroy()
        else:
            messagebox.showwarning("Input Salah", "Pilih mode pengurutan yang valid.")

    top = tk.Toplevel(root)
    top.title("Urutkan Peserta")
    top.geometry("250x120")
    top.config(bg="#FDFCE8")
    top.grab_set()

    tk.Label(top, text="Pilih Mode Urutan", bg="#FDFCE8", font=("Segoe UI", 11)).pack(pady=10)
    mode_var = tk.StringVar()
    mode_combo = ttk.Combobox(top, textvariable=mode_var, state='readonly', values=["asc", "desc"])
    mode_combo.pack(pady=5)

    ttk.Button(top, text="Urutkan", command=apply_sort).pack(pady=10)

def halaman_masuk():
    login_win = tk.Tk()
    login_win.title("Masuk - Informasi Kegiatan")
    login_win.geometry("400x350")
    login_win.config(bg="#FDFCE8")

    tk.Label(login_win, text="📋 SIPEKA 📋", font=("Segoe UI", 16, 'bold'), bg="#FDFCE8").pack(pady=(15, 0))
    tk.Label(login_win, text="Sistem Pendataan Peserta Kegiatan", font=("Segoe UI", 12, 'bold'), bg="#FDFCE8", fg="#444").pack(pady=(0, 15))

    frame_form = tk.Frame(login_win, bg="#FDFCE8")
    frame_form.pack(pady=10)

    labels = ['Nama Kegiatan', 'Tanggal Kegiatan', 'Penyelenggara']
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(frame_form, text=label, bg="#FDFCE8").grid(row=i, column=0, pady=8, sticky='w')
        ent = tk.Entry(frame_form, width=30)
        ent.grid(row=i, column=1, pady=8)
        entries[label] = ent

    def submit():
        global nama_kegiatan, tanggal_kegiatan, penyelenggara
        values = [entries[lbl].get().strip() for lbl in labels]
        if all(values):
            nama_kegiatan, tanggal_kegiatan, penyelenggara = values
            login_win.destroy()
            buka_halaman_utama()
        else:
            messagebox.showwarning("Input Wajib", "Semua kolom harus diisi.")

    ttk.Button(login_win, text="Masuk", command=submit).pack(pady=20)

    login_win.mainloop()

def buka_halaman_utama():
    global root, listbox, search_var, jumlah_label
    root = tk.Tk()
    root.title("Pendataan Peserta Kegiatan")
    root.geometry("1000x600")
    root.config(bg="#FDFCE8")

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TButton", font=("Segoe UI", 11), padding=8, background="#391E10", foreground="white")
    style.map("TButton", background=[('active', '#1976D2')])
    style.configure("TLabel", font=("Segoe UI", 12))

    header_frame = tk.Frame(root, bg="#391E10", height=70)
    header_frame.pack(fill='x')
    header_label = tk.Label(header_frame, text="📋 SIPEKA", bg="#391E10", fg="white", font=('Segoe UI', 20, 'bold'))
    header_label.pack()
    subheader_label = tk.Label(header_frame, text="SISTEM PENDATAAN PESERTA KEGIATAN", bg="#391E10", fg="white", font=('Segoe UI', 12, 'bold'))
    subheader_label.pack()


    info_frame = tk.Frame(root, bg="#FDFCE8")
    info_frame.pack(pady=5)
    tk.Label(info_frame, text=f"📌 {nama_kegiatan} | 📅 {tanggal_kegiatan} | 🏢 {penyelenggara}", font=("Segoe UI", 12, 'italic'), bg="#FDFCE8", fg="#333").pack()

    main_frame = tk.Frame(root, bg="#FDFCE8")
    main_frame.pack(padx=10, pady=10, fill='both', expand=True)

    btn_frame = tk.Frame(main_frame, bg="#FDFCE8")
    btn_frame.pack(side='top', pady=10)

    buttons = [
        ("➕ Tambah Peserta", tambah_gui),
        ("✏ Edit Peserta", edit_gui),
        ("❌ Hapus Peserta", hapus_gui),
        ("⬆⬇ Urutkan Peserta", urutkan_gui),
        ("🔄 Reset Data", reset_data)

    ]

    for text, cmd in buttons:
        ttk.Button(btn_frame, text=text, command=cmd).pack(side='left', padx=6)

    search_frame = tk.Frame(main_frame, bg="#FDFCE8")
    search_frame.pack(pady=5)

    search_var = tk.StringVar()
    search_var.trace_add('write', lambda *args: refresh_list())

    tk.Label(search_frame, text="🔎 Cari Nama: ", font=("Segoe UI", 11), bg="#FDFCE8").pack(side='left')
    search_entry = tk.Entry(search_frame, textvariable=search_var, font=("Segoe UI", 11), width=30)
    search_entry.pack(side='left', padx=5)

    cols = ('No', 'Nama', 'Email', 'Instansi', 'No Telepon', 'Hadir')
    listbox = ttk.Treeview(main_frame, columns=cols, show='headings', height=15)
    for col in cols:
        listbox.heading(col, text=col)
        listbox.column(col, anchor='center')
    listbox.pack(pady=10, fill='both', expand=True)

    jumlah_label = tk.Label(main_frame, text="", font=("Segoe UI", 11, 'bold'), bg="#FDFCE8", fg="#391E10")
    jumlah_label.pack()

    muat_dari_csv()
    refresh_list()
    root.mainloop()
    
if __name__ == "__main__":
    halaman_masuk()
