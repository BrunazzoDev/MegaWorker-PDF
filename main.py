import os
import sys
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import re
import subprocess
import tempfile
import shutil
from PyPDF2 import PdfReader, PdfWriter
import datetime
import json
import threading
import time
import queue


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_VERSION = "v1.2.5"
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
SUPPORTED_LANGUAGES = ["English", "Italian"]
CURRENT_LANGUAGE = "English"

TRANSLATIONS = {
    "English": {
        "app_ready": "Ready - {version}", "convert_tab": "Convert Images to PDF",
        "compress_tab": "Compress PDF", "settings_tab": "Settings",
        "converter_title": "Image to PDF Converter", "converter_desc": "Convert PNG and JPG files into a single PDF",
        "order_desc": "Images will be inserted in the order of the selected folders",
        "quality_select": "Select PDF quality:", "a4": "A4 format", "original": "Original quality",
        "select_folders": "Select folders", "conversion_history": "Conversion history",
        "compressor_title": "PDF Compressor", "compressor_desc": "Reduce the size of your PDF files",
        "compression_level": "Compression level:", "low": "Low", "medium": "Medium", "high": "High",
        "select_pdf": "Select PDF to compress", "compression_history": "Compression history",
        "select_theme": "Select theme:", "clear_history": "Clear all history",
        "history_path": "History file path:", "version": "Version:", "select_language": "Language:",
        "theme_changed": "Theme changed to: {theme}", "history_cleared": "History cleared.",
        "no_conversions": "No conversions recorded.", "no_compressions": "No compressions recorded.",
        "select_folders_title": "Folder selection", "select_folders_message": "Select folders containing PNG and JPG files to convert.\nThe folder selection order determines the PDF file order.",
        "select_folder": "Select folder {number} (Cancel to finish)", "no_folder": "No folders selected.",
        "no_images": "No PNG or JPG files found in the selected folders.",
        "no_images_selected": "Select at least one image before continuing.",
        "analyzing": "Analyzing files...",
        "compression_start": "Starting compression of {name}", "compression_window": "PDF compression",
        "compression_progress": "Compression in progress... {progress:.2f}% complete",
        "compression_file_progress": "Compressing {name}...", "compression_done": "Compression completed successfully.",
        "compression_result": "Compression completed. Size change: {ratio:.2f}% (from {input_size:.2f} KB to {output_size:.2f} KB)",
        "compression_in_progress": "PDF compression in progress...", "compression_of": "Compressing {name}...",
        "compression_error": "Error during compression.", "error": "Error", "success": "Success",
        "same_file": "The destination file must be different from the source PDF.",
        "preview_window": "Image preview", "preview_header": "Preview of collected images",
        "include": "Include", "cancel": "Cancel", "save_changes": "Save changes",
        "changes_saved": "Changes saved", "changes_saved_message": "The changes were saved successfully.",
        "confirmation_window": "Files to convert", "found_files": "Found {files} image files in {folders} folders",
        "selected_mode": "Selected mode: {mode}", "folder_number": "Folder {number}: {name}",
        "excluded": "{name} (excluded)", "view_images": "View images", "proceed": "Proceed",
        "save_pdf": "Save PDF", "operation_cancelled": "Operation cancelled.",
        "creating_pdf": "Creating PDF...", "creation_window": "PDF creation",
        "creation_progress": "Creating PDF...", "processing_image": "Processing image {current}/{total}...",
        "finalizing": "PDF created, finalizing...", "pdf_created": "PDF created successfully!\n{count} images converted to: {path}",
        "creation_error": "An error occurred while creating the PDF:\n{error}",
        "compression_info_title": "Compression information", "compression_info": "Compression information:\n\nLow: Light compression that preserves quality. Ideal for documents requiring high quality.\n\nMedium: Balance between quality and size. Suitable for most general uses.\n\nHigh: Maximum content-stream compression. The result depends on the PDF content.\n\nNote: Some PDFs may already be well compressed.",
        "confirm": "Confirm", "clear_history_question": "Are you sure you want to clear all history?",
        "language_changed": "Language changed to: {language}"
    },
    "Italian": {
        "app_ready": "Pronto - {version}", "convert_tab": "Converti immagini in PDF",
        "compress_tab": "Comprimi PDF", "settings_tab": "Impostazioni",
        "converter_title": "Convertitore immagini in PDF", "converter_desc": "Converti file PNG e JPG in un unico PDF",
        "order_desc": "Le immagini verranno inserite nell'ordine delle cartelle selezionate",
        "quality_select": "Seleziona la qualita del PDF:", "a4": "Formato A4", "original": "Qualita originale",
        "select_folders": "Seleziona cartelle", "conversion_history": "Cronologia conversioni",
        "compressor_title": "Compressore PDF", "compressor_desc": "Riduci la dimensione dei tuoi file PDF",
        "compression_level": "Livello di compressione:", "low": "Bassa", "medium": "Media", "high": "Alta",
        "select_pdf": "Seleziona PDF da comprimere", "compression_history": "Cronologia compressioni",
        "select_theme": "Seleziona tema:", "clear_history": "Cancella tutta la cronologia",
        "history_path": "Percorso file cronologia:", "version": "Versione:", "select_language": "Lingua:",
        "theme_changed": "Tema cambiato in: {theme}", "history_cleared": "Cronologia cancellata.",
        "no_conversions": "Nessuna conversione registrata.", "no_compressions": "Nessuna compressione registrata.",
        "select_folders_title": "Selezione cartelle", "select_folders_message": "Seleziona le cartelle contenenti file PNG e JPG da convertire.\nL'ordine di selezione determina l'ordine nel PDF.",
        "select_folder": "Seleziona cartella {number} (Annulla per terminare)", "no_folder": "Nessuna cartella selezionata.",
        "no_images": "Nessun file PNG o JPG trovato nelle cartelle selezionate.",
        "no_images_selected": "Seleziona almeno un'immagine prima di continuare.",
        "analyzing": "Analisi dei file in corso...",
        "compression_start": "Inizio compressione di {name}", "compression_window": "Compressione PDF",
        "compression_progress": "Compressione in corso... {progress:.2f}% completata",
        "compression_file_progress": "Compressione di {name}...", "compression_done": "Compressione completata con successo.",
        "compression_result": "Compressione completata. Riduzione: {ratio:.2f}% (da {input_size:.2f} KB a {output_size:.2f} KB)",
        "compression_in_progress": "Compressione PDF in corso...", "compression_of": "Compressione di {name}...",
        "compression_error": "Errore durante la compressione.", "error": "Errore", "success": "Successo",
        "same_file": "Il file di destinazione deve essere diverso dal PDF originale.",
        "preview_window": "Anteprima immagini", "preview_header": "Anteprima delle immagini raccolte",
        "include": "Includi", "cancel": "Annulla", "save_changes": "Salva modifiche",
        "changes_saved": "Modifiche salvate", "changes_saved_message": "Le modifiche sono state salvate con successo.",
        "confirmation_window": "File da convertire", "found_files": "Trovati {files} file immagine in {folders} cartelle",
        "selected_mode": "Modalita selezionata: {mode}", "folder_number": "Cartella {number}: {name}",
        "excluded": "{name} (escluso)", "view_images": "Visualizza immagini", "proceed": "Procedi",
        "save_pdf": "Salva PDF", "operation_cancelled": "Operazione annullata.",
        "creating_pdf": "Creazione PDF in corso...", "creation_window": "Creazione PDF",
        "creation_progress": "Creazione PDF in corso...", "processing_image": "Elaborazione immagine {current}/{total}...",
        "finalizing": "PDF creato, finalizzazione in corso...", "pdf_created": "PDF creato con successo!\n{count} immagini convertite in: {path}",
        "creation_error": "Si e verificato un errore durante la creazione del PDF:\n{error}",
        "compression_info_title": "Informazioni sulla compressione", "compression_info": "Informazioni sulla compressione:\n\nBassa: compressione leggera che mantiene la qualita. Ideale per documenti che richiedono alta qualita.\n\nMedia: equilibrio tra qualita e dimensioni. Adatta alla maggior parte degli usi.\n\nAlta: massima compressione dei contenuti. Il risultato dipende dal contenuto del PDF.\n\nNota: alcuni PDF potrebbero essere gia ben compressi.",
        "confirm": "Conferma", "clear_history_question": "Sei sicuro di voler cancellare tutta la cronologia?",
        "language_changed": "Lingua cambiata in: {language}"
    }
}

def load_settings():
    defaults = {"language": "English", "theme": "System"}
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as settings_file:
            saved = json.load(settings_file)
        if isinstance(saved, dict):
            defaults.update({key: value for key, value in saved.items() if key in defaults})
    except (OSError, json.JSONDecodeError):
        pass
    if defaults["language"] not in SUPPORTED_LANGUAGES:
        defaults["language"] = "English"
    if defaults["theme"] not in ["System", "Light", "Dark"]:
        defaults["theme"] = "System"
    return defaults

def save_settings(settings):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as settings_file:
            json.dump(settings, settings_file, indent=2)
    except OSError:
        pass

def translate(key, **values):
    return TRANSLATIONS[CURRENT_LANGUAGE][key].format(**values)

def auto_scroll(widget):
    """Esegue lo scorrimento automatico di un widget di testo."""
    def scroll():
        while True:
            # Scorri verso il basso
            time.sleep(1.8)
            for i in range(380):
                widget.yview_moveto(i / 380)
                time.sleep(0.05)  # Velocità di scorrimento
            time.sleep(1)  # Pausa in fondo

            # Scorri verso l'alto
            for i in range(380, -1, -1):
                widget.yview_moveto(i / 380)
                time.sleep(0.05)  # Velocità di scorrimento
            time.sleep(2)  # Pausa in cima

    # Avvia il thread per lo scorrimento
    thread = threading.Thread(target=scroll, daemon=True)
    thread.start()

# Impostazione tema di CustomTkinter
ctk.set_appearance_mode("System")  # "System", "Dark" o "Light"
ctk.set_default_color_theme("blue")  # "blue", "green" o "dark-blue"

# Configurazione del database e del file di log
DATABASE_DIR = os.path.join(BASE_DIR, "Database")
HISTORY_DIR = os.path.join(BASE_DIR, "History")
LOG_FILE = os.path.join(HISTORY_DIR, "pdf_history.json")
COMPRESS_LOG_FILE = os.path.join(HISTORY_DIR, "compress_history.json")

def ensure_directories():
    """Assicura che le directory necessarie esistano"""
    directories = {
        "database": DATABASE_DIR,
        "history": HISTORY_DIR
    }
    for name, directory in directories.items():
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except Exception as e:
                messagebox.showwarning(translate("error"), f"Unable to create the {name} directory:\n{str(e)}")
    return all(os.path.exists(dir) for dir in directories.values())

def ensure_database_directory():
    """Assicura che la directory del database esista"""
    return ensure_directories()

def load_history():
    """Carica la cronologia dal file JSON"""
    ensure_directories()  # Assicura che la directory History esista
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
        return history if isinstance(history, list) else []
    except Exception as e:
        messagebox.showwarning(translate("error"), f"Unable to load history:\n{str(e)}")
        return []

def save_history(history):
    """Salva la cronologia nel file JSON"""
    ensure_directories()  # Assicura che la directory History esista
    try:
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        messagebox.showwarning(translate("error"), f"Unable to save history:\n{str(e)}")

def add_history_entry(action, details):
    """Aggiunge una nuova voce alla cronologia"""
    history = load_history()
    entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "details": details
    }
    history.append(entry)
    save_history(history)
    return entry

def load_compress_history():
    """Carica la cronologia delle compressioni dal file JSON"""
    ensure_directories()  # Assicura che la directory History esista
    if not os.path.exists(COMPRESS_LOG_FILE):
        return []
    try:
        with open(COMPRESS_LOG_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
        return history if isinstance(history, list) else []
    except Exception as e:
        messagebox.showwarning(translate("error"), f"Unable to load compression history:\n{str(e)}")
        return []

def save_compress_history(history):
    """Salva la cronologia delle compressioni nel file JSON"""
    ensure_directories()  # Assicura che la directory History esista
    try:
        with open(COMPRESS_LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        messagebox.showwarning(translate("error"), f"Unable to save compression history:\n{str(e)}")

def add_compress_history_entry(action, details):
    """Aggiunge una nuova voce alla cronologia delle compressioni"""
    history = load_compress_history()
    entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "details": details
    }
    history.append(entry)
    save_compress_history(history)
    return entry

def natural_sort_key(s):
    """Funzione per ordinamento naturale delle stringhe con numeri"""
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', s)]

def select_folders():
    """Permette all'utente di selezionare cartelle da cui importare immagini"""
    messagebox.showinfo(translate("select_folders_title"), translate("select_folders_message"))
    folders = []
    while True:
        folder = filedialog.askdirectory(title=translate("select_folder", number=len(folders) + 1))
        if not folder:
            break
        folders.append(folder)
    if not folders:
        messagebox.showwarning(translate("error"), translate("no_folder"))
        return None
    return folders

def get_image_files(folders):
    """Raccoglie tutti i file PNG e JPG dalle cartelle selezionate, rispettando l'ordine delle cartelle"""
    all_image_files = []
    for folder in folders:
        folder_files = []
        for file in os.listdir(folder):
            lower_file = file.lower()
            if lower_file.endswith('.png') or lower_file.endswith('.jpg') or lower_file.endswith('.jpeg'):
                folder_files.append(os.path.join(folder, file))
        folder_files.sort(key=lambda x: natural_sort_key(os.path.basename(x)))
        all_image_files.extend(folder_files)
    if not all_image_files:
        messagebox.showwarning(translate("error"), translate("no_images"))
        return None
    return all_image_files

def compress_pdf(input_pdf, output_pdf, compression_level, progress_callback=None):
    """Comprime un PDF con diverse strategie a seconda del livello di compressione."""
    try:
        temp_dir = tempfile.mkdtemp(prefix="pdf_compress_")
        temp_pdf = os.path.join(temp_dir, "temp.pdf")
        shutil.copy2(input_pdf, temp_pdf)

        reader = PdfReader(temp_pdf)
        writer = PdfWriter()
        total_pages = len(reader.pages)
        if total_pages == 0:
            raise ValueError("The PDF contains no pages.")

        for i, page in enumerate(reader.pages):
            if compression_level in ("High", "Alta"):
                page.compress_content_streams()
            writer.add_page(page)

            # Aggiorna la percentuale nella barra di stato
            if progress_callback:
                progress = ((i + 1) / total_pages) * 100
                progress_callback(progress)

        with open(output_pdf, "wb") as output_stream:
            writer.write(output_stream)

        input_size = os.path.getsize(input_pdf)
        output_size = os.path.getsize(output_pdf)
        if input_size == 0:
            raise ValueError("The source PDF is empty.")
        compression_ratio = (1 - (output_size / input_size)) * 100
        return True, translate("compression_result", ratio=compression_ratio,
                      input_size=input_size / 1024, output_size=output_size / 1024)

    except Exception as e:
        return False, f"{translate('compression_error')} {str(e)}"
    finally:
        if 'temp_dir' in locals():
            shutil.rmtree(temp_dir, ignore_errors=True)

class AdvancedPDFApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MegaWorker PDF")
        self.geometry("710x600")
        self.minsize(710, 600)

        ensure_database_directory()
        self.settings = load_settings()
        self.language = self.settings["language"]
        global CURRENT_LANGUAGE
        CURRENT_LANGUAGE = self.language
        save_settings(self.settings)
        ctk.set_appearance_mode(self.settings["theme"])

        # Variabili
        self.quality_var = ctk.StringVar(value="A4")
        self.compression_var = ctk.StringVar(value="Medium")
        self.image_files = []
        self.folders = []
        self.history = load_history()
        self.worker_queue = queue.Queue()
        self.after(100, self.process_worker_events)

        # Frame principale con tabs
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)  # Ridotto padding

        # Creazione delle tab
        self.tab_names = {
            "convert": self.t("convert_tab"),
            "compress": self.t("compress_tab"),
            "settings": self.t("settings_tab")
        }
        self.tab_convert = self.tabview.add(self.tab_names["convert"])
        self.tab_compress = self.tabview.add(self.tab_names["compress"])
        self.tab_settings = self.tabview.add(self.tab_names["settings"])

        self.tabview.set(self.t("convert_tab"))

        # Configurazione delle tab
        self.setup_conversion_tab()
        self.setup_compression_tab()
        self.setup_settings_tab()

        # Barra di stato nella parte inferiore
        self.status_bar = ctk.CTkFrame(self, height=30)
        self.status_bar.pack(side="bottom", fill="x")
        self.status_label_bottom = ctk.CTkLabel(self.status_bar, text=self.t("app_ready", version=APP_VERSION), anchor="w")
        self.status_label_bottom.pack(side="left", padx=10)

        # Aggiunta di compress_status_label per evitare errori
        self.compress_status_label = ctk.CTkLabel(self.status_bar, text="", anchor="w")
        self.compress_status_label.pack(side="right", padx=10)

        # Aggiunta di status_label per evitare errori
        self.status_label = ctk.CTkLabel(self, text="", anchor="w")
        self.status_label.pack(side="top", fill="x", padx=10, pady=5)

        self.update_history_display()

    def t(self, key, **values):
        return TRANSLATIONS[self.language][key].format(**values)

    def process_worker_events(self):
        """Applica nel thread GUI i risultati prodotti dai worker."""
        try:
            while True:
                event, payload = self.worker_queue.get_nowait()
                if event == "compress_progress":
                    progress = payload
                    self.compress_status_label.configure(
                        text=self.t("compression_progress", progress=progress)
                    )
                elif event == "compress_done":
                    success, message, output_pdf = payload
                    self.progress_bar.stop()
                    self.progress_window.grab_release()
                    self.progress_window.destroy()
                    if success:
                        self.compress_status_label.configure(text=message)
                        self.status_label_bottom.configure(text=self.t("compression_done"))
                        details = f"File: {os.path.basename(output_pdf)} - {message}"
                        add_compress_history_entry("PDF compression", details)
                        self.update_history_display()
                        messagebox.showinfo(self.t("success"), message)
                    else:
                        self.compress_status_label.configure(text=self.t("compression_error"))
                        self.status_label_bottom.configure(text=self.t("compression_error"))
                        messagebox.showerror(self.t("error"), message)
                elif event == "conversion_progress":
                    progress, message = payload
                    self.progress_bar.set(progress)
                    self.status_label_bottom.configure(text=message)
                elif event == "conversion_done":
                    success, message, output_file, image_count, folder_names = payload
                    self.progress_window.grab_release()
                    self.progress_window.destroy()
                    if success:
                        details = f"File: {os.path.basename(output_file)} - {image_count} images from {folder_names}"
                        add_history_entry("PDF conversion", details)
                        self.history = load_history()
                        self.update_history_display()
                        messagebox.showinfo(self.t("success"), message)
                        self.status_label.configure(text=f"PDF created: {os.path.basename(output_file)}")
                        self.status_label_bottom.configure(text=self.t("success"))
                    else:
                        messagebox.showerror(self.t("error"), message)
                        self.status_label.configure(text=self.t("creation_error", error=""))
                        self.status_label_bottom.configure(text=self.t("error"))
        except queue.Empty:
            pass
        self.after(100, self.process_worker_events)

    def setup_conversion_tab(self):
        self.title_label = ctk.CTkLabel(self.tab_convert, text=self.t("converter_title"),
                                         font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=10)
        self.desc_label = ctk.CTkLabel(self.tab_convert, text=self.t("converter_desc"))
        self.desc_label.pack(pady=5)
        self.order_label = ctk.CTkLabel(self.tab_convert, text=self.t("order_desc"),
                                        font=ctk.CTkFont(size=12, slant="italic"))
        self.order_label.pack(pady=2)
        self.quality_frame = ctk.CTkFrame(self.tab_convert)
        self.quality_frame.pack(pady=15)
        self.quality_label = ctk.CTkLabel(self.quality_frame, text=self.t("quality_select"))
        self.quality_label.pack(side="left", padx=10, pady=10)
        self.a4_radio = ctk.CTkRadioButton(self.quality_frame, text=self.t("a4"),
                                           variable=self.quality_var, value="A4")
        self.a4_radio.pack(side="left", padx=10, pady=10)
        self.orig_radio = ctk.CTkRadioButton(self.quality_frame, text=self.t("original"),
                                             variable=self.quality_var, value="Originale")
        self.orig_radio.pack(side="left", padx=10, pady=10)
        self.start_button = ctk.CTkButton(self.tab_convert, text=self.t("select_folders"),
                                          command=self.start_selection, width=200, height=40)
        self.start_button.pack(pady=20)
        self.status_frame = ctk.CTkFrame(self.tab_convert)
        self.status_frame.pack_forget()  # Rimosso lo spazio vuoto per la linea di dialogo
        self.history_label = ctk.CTkLabel(self.tab_convert, text=self.t("conversion_history"),
                                          font=ctk.CTkFont(size=16, weight="bold"))
        self.history_label.pack(pady=(20, 5))
        self.convert_history = ctk.CTkTextbox(self.tab_convert, height=150)
        self.convert_history.pack(fill="x", padx=10, pady=5)
        self.convert_history.configure(state="disabled")

        # Avvia lo scorrimento automatico (TOGLIERE IL COMMENTO ALLA LINEA SOTTOSTANTE PER ATTIVARLO!!!!!!)
        # auto_scroll(self.convert_history)

    def setup_compression_tab(self):
        self.compression_title = ctk.CTkLabel(self.tab_compress, text=self.t("compressor_title"),
                                               font=ctk.CTkFont(size=24, weight="bold"))
        self.compression_title.pack(pady=10)
        self.compression_desc = ctk.CTkLabel(self.tab_compress, text=self.t("compressor_desc"))
        self.compression_desc.pack(pady=5)
        self.comp_frame = ctk.CTkFrame(self.tab_compress)
        self.comp_frame.pack(pady=15)
        self.comp_label = ctk.CTkLabel(self.comp_frame, text=self.t("compression_level"))
        self.comp_label.pack(side="left", padx=10, pady=10)
        self.low_radio = ctk.CTkRadioButton(self.comp_frame, text=self.t("low"),
                           variable=self.compression_var, value="Low")
        self.low_radio.pack(side="left", padx=10, pady=10)
        self.med_radio = ctk.CTkRadioButton(self.comp_frame, text=self.t("medium"),
                           variable=self.compression_var, value="Medium")
        self.med_radio.pack(side="left", padx=10, pady=10)
        self.high_radio = ctk.CTkRadioButton(self.comp_frame, text=self.t("high"),
                            variable=self.compression_var, value="High")
        self.high_radio.pack(side="left", padx=10, pady=10)
        self.info_button = ctk.CTkButton(self.tab_compress, text="?", width=30, height=30, 
                                         command=self.show_compression_info)
        self.info_button.pack(pady=5, padx=10, anchor="ne")

        self.select_pdf_button = ctk.CTkButton(self.tab_compress, text=self.t("select_pdf"),
                                               command=self.compress_pdf_workflow, width=200, height=40)
        self.select_pdf_button.pack(pady=20)
        self.compress_status_frame = ctk.CTkFrame(self.tab_compress)
        self.compress_status_frame.pack_forget()  # Rimosso lo spazio vuoto per la linea di dialogo
        self.history_label_compress = ctk.CTkLabel(self.tab_compress, text=self.t("compression_history"),
                                                   font=ctk.CTkFont(size=16, weight="bold"))
        self.history_label_compress.pack(pady=(20, 5))
        self.compress_history = ctk.CTkTextbox(self.tab_compress, height=150)
        self.compress_history.pack(fill="x", padx=10, pady=5)
        self.compress_history.configure(state="disabled")

        # Avvia lo scorrimento automatico (TOGLIERE IL COMMENTO ALLA LINEA SOTTOSTANTE PER ATTIVARLO!!!!!!)
        # auto_scroll(self.compress_history)

    def setup_settings_tab(self):
        theme_frame = ctk.CTkFrame(self.tab_settings)
        theme_frame.pack(pady=10, padx=10, fill="x")
        self.theme_label = ctk.CTkLabel(theme_frame, text=self.t("select_theme"))
        self.theme_label.pack(side="left", padx=10)
        self.theme_var = ctk.StringVar(value=self.settings["theme"])
        self.theme_option_menu = ctk.CTkOptionMenu(theme_frame, values=["System", "Light", "Dark"],
                                                   variable=self.theme_var, command=self.change_theme)
        self.theme_option_menu.pack(side="left", padx=10)

        history_frame = ctk.CTkFrame(self.tab_settings)
        history_frame.pack(pady=10, padx=10, fill="x")
        self.clear_all_button = ctk.CTkButton(history_frame, text=self.t("clear_history"),
                                              command=self.clear_all_history, fg_color="#c0392b")
        self.clear_all_button.pack(side="left", padx=10)

        path_frame = ctk.CTkFrame(self.tab_settings)
        path_frame.pack(pady=10, padx=10, fill="x")
        self.path_label = ctk.CTkLabel(path_frame, text=self.t("history_path"))
        self.path_label.pack(side="left", padx=10)
        self.path_value = ctk.CTkLabel(path_frame, text=LOG_FILE)
        self.path_value.pack(side="left", padx=10)

        version_frame = ctk.CTkFrame(self.tab_settings)
        version_frame.pack(pady=10, padx=10, fill="x")
        self.version_label = ctk.CTkLabel(version_frame, text=self.t("version"))
        self.version_label.pack(side="left", padx=10)
        self.version_value = ctk.CTkLabel(version_frame, text=APP_VERSION)
        self.version_value.pack(side="left", padx=10)

        language_frame = ctk.CTkFrame(self.tab_settings)
        language_frame.pack(pady=10, padx=10, fill="x")
        self.language_label = ctk.CTkLabel(language_frame, text=self.t("select_language"))
        self.language_label.pack(side="left", padx=10)
        self.language_var = ctk.StringVar(value=self.language)
        self.language_option_menu = ctk.CTkOptionMenu(
            language_frame, values=SUPPORTED_LANGUAGES,
            variable=self.language_var, command=self.change_language
        )
        self.language_option_menu.pack(side="left", padx=10)

    def change_theme(self, selected_theme):
        if selected_theme == "System":
            ctk.set_appearance_mode("System")
        elif selected_theme == "Light":
            ctk.set_appearance_mode("Light")
        elif selected_theme == "Dark":
            ctk.set_appearance_mode("Dark")
        self.settings["theme"] = selected_theme
        save_settings(self.settings)
        self.status_label_bottom.configure(text=self.t("theme_changed", theme=selected_theme))

    def change_language(self, selected_language):
        if selected_language not in SUPPORTED_LANGUAGES:
            return
        self.language = selected_language
        global CURRENT_LANGUAGE
        CURRENT_LANGUAGE = selected_language
        self.settings["language"] = selected_language
        save_settings(self.settings)
        self.apply_language()
        self.status_label_bottom.configure(text=self.t("language_changed", language=selected_language))

    def apply_language(self):
        new_tab_names = {
            "convert": self.t("convert_tab"),
            "compress": self.t("compress_tab"),
            "settings": self.t("settings_tab")
        }
        for key, widget in (("convert", self.tab_convert), ("compress", self.tab_compress), ("settings", self.tab_settings)):
            self.tabview.rename(self.tab_names[key], new_tab_names[key])
            self.tab_names[key] = new_tab_names[key]
        self.title_label.configure(text=self.t("converter_title"))
        self.desc_label.configure(text=self.t("converter_desc"))
        self.order_label.configure(text=self.t("order_desc"))
        self.quality_label.configure(text=self.t("quality_select"))
        self.a4_radio.configure(text=self.t("a4"))
        self.orig_radio.configure(text=self.t("original"))
        self.start_button.configure(text=self.t("select_folders"))
        self.history_label.configure(text=self.t("conversion_history"))
        self.compression_title.configure(text=self.t("compressor_title"))
        self.compression_desc.configure(text=self.t("compressor_desc"))
        self.comp_label.configure(text=self.t("compression_level"))
        self.low_radio.configure(text=self.t("low"))
        self.med_radio.configure(text=self.t("medium"))
        self.high_radio.configure(text=self.t("high"))
        self.select_pdf_button.configure(text=self.t("select_pdf"))
        self.history_label_compress.configure(text=self.t("compression_history"))
        self.theme_label.configure(text=self.t("select_theme"))
        self.clear_all_button.configure(text=self.t("clear_history"))
        self.path_label.configure(text=self.t("history_path"))
        self.version_label.configure(text=self.t("version"))
        self.language_label.configure(text=self.t("select_language"))
        self.update_history_display()

    def clear_all_history(self):
        if messagebox.askyesno(self.t("confirm"), self.t("clear_history_question")):
            save_history([])
            save_compress_history([])
            self.history = []
            self.update_history_display()
            self.status_label_bottom.configure(text=self.t("history_cleared"))

    def update_history_display(self):
        # Aggiorna cronologia conversioni
        self.convert_history.configure(state="normal")
        self.convert_history.delete("1.0", "end")
        conversion_entries = [entry for entry in self.history if entry.get("action") in ("PDF conversion", "Conversione PDF")]
        if conversion_entries:
            for entry in reversed(conversion_entries):
                timestamp = entry["timestamp"]
                details = entry["details"]
                self.convert_history.insert("end", f"📄 {timestamp} - {details}\n\n")
        else:
            self.convert_history.insert("end", self.t("no_conversions"))
        self.convert_history.configure(state="disabled")

        # Aggiorna cronologia compressioni
        compress_history = load_compress_history()
        self.compress_history.configure(state="normal")
        self.compress_history.delete("1.0", "end")
        if compress_history:
            for entry in reversed(compress_history):
                timestamp = entry["timestamp"]
                details = entry["details"]
                self.compress_history.insert("end", f"🔄 {timestamp} - {details}\n\n")
        else:
            self.compress_history.insert("end", self.t("no_compressions"))
        self.compress_history.configure(state="disabled")

    def compress_pdf_workflow(self):
        input_pdf = filedialog.askopenfilename(
            filetypes=[("PDF files", "*.pdf")],
            title=self.t("select_pdf")
        )
        if not input_pdf:
            return
        input_basename = os.path.basename(input_pdf)
        filename_without_ext = os.path.splitext(input_basename)[0]
        suggested_name = f"{filename_without_ext}_compressed.pdf"
        output_pdf = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title=self.t("save_pdf"),
            initialdir=DATABASE_DIR,
            initialfile=suggested_name
        )
        if not output_pdf:
            return
        if os.path.abspath(input_pdf) == os.path.abspath(output_pdf):
            messagebox.showerror(self.t("error"), self.t("same_file"))
            return
        self.status_label_bottom.configure(text=self.t("compression_start", name=os.path.basename(input_pdf)))
        self.progress_window = ctk.CTkToplevel(self)
        self.progress_window.title(self.t("compression_window"))
        self.progress_window.geometry("400x150")
        self.progress_window.transient(self)
        self.progress_window.grab_set()
        progress_frame = ctk.CTkFrame(self.progress_window)
        progress_frame.pack(fill="both", expand=True, padx=20, pady=20)
        progress_label = ctk.CTkLabel(progress_frame, text=self.t("compression_in_progress"),
                                      font=ctk.CTkFont(size=14))
        progress_label.pack(pady=10)
        self.progress_bar = ctk.CTkProgressBar(progress_frame, width=300, mode="indeterminate")
        self.progress_bar.pack(pady=10)
        self.progress_bar.start()
        self.compress_status_label.configure(text=self.t("compression_of", name=os.path.basename(input_pdf)))
        compression_level = self.compression_var.get()
        compress_thread = threading.Thread(
            target=self.compress_pdf_thread, 
            args=(input_pdf, output_pdf, compression_level)
        )
        compress_thread.daemon = True
        compress_thread.start()

    def compress_pdf_thread(self, input_pdf, output_pdf, compression_level):
        success, message = compress_pdf(
            input_pdf,
            output_pdf,
            compression_level,
            lambda progress: self.worker_queue.put(("compress_progress", progress))
        )
        self.worker_queue.put(("compress_done", (success, message, output_pdf)))

    def start_selection(self):
        self.folders = select_folders()
        if not self.folders:
            return
        self.status_label.configure(text=self.t("analyzing"))
        self.update()
        self.image_files = get_image_files(self.folders)
        if not self.image_files:
            return
        self.show_confirmation()

    def show_preview_window(self):
        """Mostra una finestra di anteprima per visualizzare ed eliminare immagini"""
        self.preview_window = ctk.CTkToplevel(self)
        self.preview_window.title(self.t("preview_window"))
        self.preview_window.geometry("900x700")  # Aumentata la dimensione della finestra
        self.preview_window.grab_set()

        preview_frame = ctk.CTkFrame(self.preview_window)
        preview_frame.pack(fill="both", expand=True, padx=20, pady=20)

        header_label = ctk.CTkLabel(preview_frame, text=self.t("preview_header"),
                                    font=ctk.CTkFont(size=18, weight="bold"))
        header_label.pack(pady=10)

        image_container = ctk.CTkScrollableFrame(preview_frame, height=500)  # Aumentata l'altezza del contenitore
        image_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.image_checkboxes = []
        for img_path in self.image_files:
            img_frame = ctk.CTkFrame(image_container)
            img_frame.pack(fill="x", padx=5, pady=10)  # Aumentato il padding per separare meglio le immagini

            # Carica l'immagine e ridimensionala per l'anteprima
            img = Image.open(img_path)
            img = img.resize((200, 200), Image.LANCZOS)  # Ridimensiona l'immagine per l'anteprima (dimensione aumentata)
            img_preview = ctk.CTkImage(light_image=img, size=(200, 200))

            img_label = ctk.CTkLabel(img_frame, image=img_preview, text="")
            img_label.pack(side="left", padx=15)  # Aumentato il padding laterale

            file_label = ctk.CTkLabel(img_frame, text=os.path.basename(img_path), anchor="w",
                                      font=ctk.CTkFont(size=14))  # Font leggermente più grande
            file_label.pack(side="left", padx=10)

            checkbox = ctk.CTkCheckBox(img_frame, text=self.t("include"), onvalue=True, offvalue=False)
            checkbox.select()  # Selezionato di default
            checkbox.pack(side="right", padx=10)

            self.image_checkboxes.append((img_path, checkbox))

        button_frame = ctk.CTkFrame(preview_frame)
        button_frame.pack(pady=20)

        cancel_button = ctk.CTkButton(button_frame, text=self.t("cancel"), command=self.preview_window.destroy,
                                      fg_color="#c0392b", hover_color="#e74c3c")
        cancel_button.pack(side="left", padx=10)

        save_button = ctk.CTkButton(button_frame, text=self.t("save_changes"), command=self.save_preview_changes)
        save_button.pack(side="left", padx=10)

    def save_preview_changes(self):
        """Salva le modifiche effettuate nella finestra di anteprima"""
        updated_files = []
        self.excluded_files = []  # Nuova lista per i file esclusi
        for img_path, checkbox in self.image_checkboxes:
            if checkbox.get():
                updated_files.append(img_path)
            else:
                self.excluded_files.append(img_path)  # Aggiungi i file non selezionati alla lista esclusi

        self.image_files = updated_files
        self.preview_window.destroy()
        self.confirm_window.destroy()
        self.show_confirmation()
        messagebox.showinfo(self.t("changes_saved"), self.t("changes_saved_message"))

    def show_confirmation(self):
        self.confirm_window = ctk.CTkToplevel(self)
        self.confirm_window.title(self.t("confirmation_window"))
        self.confirm_window.geometry("700x600")
        self.confirm_window.grab_set()

        conf_frame = ctk.CTkFrame(self.confirm_window)
        conf_frame.pack(fill="both", expand=True, padx=20, pady=20)

        header_label = ctk.CTkLabel(conf_frame, 
                                    text=self.t("found_files", files=len(self.image_files), folders=len(self.folders)),
                                    font=ctk.CTkFont(size=16, weight="bold"))
        header_label.pack(pady=10)

        quality_mode = self.quality_var.get()
        quality_label = self.t("a4") if quality_mode == "A4" else self.t("original")
        mode_label = ctk.CTkLabel(conf_frame, text=self.t("selected_mode", mode=quality_label))
        mode_label.pack(pady=5)

        file_container = ctk.CTkScrollableFrame(conf_frame, height=350)
        file_container.pack(fill="both", expand=True, padx=10, pady=10)

        for i, folder in enumerate(self.folders):
            folder_name = os.path.basename(folder)
            folder_frame = ctk.CTkFrame(file_container)
            folder_frame.pack(fill="x", expand=True, padx=5, pady=5)

            folder_label = ctk.CTkLabel(folder_frame, 
                                        text=self.t("folder_number", number=i + 1, name=folder_name),
                                        font=ctk.CTkFont(weight="bold"))
            folder_label.pack(anchor="w", padx=10, pady=5)

            folder_files = [f for f in self.image_files if os.path.dirname(f) == folder]
            for file_path in folder_files:
                file_name = os.path.basename(file_path)
                file_label = ctk.CTkLabel(folder_frame, text=file_name, anchor="w")
                file_label.pack(fill="x", padx=20, pady=2)

            # Aggiungi i file esclusi con l'etichetta "(escluso)"
            if hasattr(self, 'excluded_files'):
                excluded_files = [f for f in self.excluded_files if os.path.dirname(f) == folder]
                for file_path in excluded_files:
                    file_name = os.path.basename(file_path)
                    file_label = ctk.CTkLabel(folder_frame, text=self.t("excluded", name=file_name), anchor="w", font=ctk.CTkFont(slant="italic"))
                    file_label.pack(fill="x", padx=20, pady=2)

        button_frame = ctk.CTkFrame(conf_frame)
        button_frame.pack(pady=15)

        preview_button = ctk.CTkButton(button_frame, text=self.t("view_images"), command=self.show_preview_window)
        preview_button.pack(side="left", padx=10)

        cancel_button = ctk.CTkButton(button_frame, text=self.t("cancel"),
                                      command=self.confirm_window.destroy,
                                      fg_color="#c0392b", hover_color="#e74c3c")
        cancel_button.pack(side="left", padx=10)

        proceed_button = ctk.CTkButton(button_frame, text=self.t("proceed"),
                                       command=self.proceed_conversion)
        proceed_button.pack(side="left", padx=10)

    def proceed_conversion(self):
        if not self.image_files:
            messagebox.showwarning(self.t("error"), self.t("no_images_selected"))
            return
        self.confirm_window.destroy()
        default_name = "New_PDF"
        if self.folders and len(self.folders) > 0:
            first_folder = os.path.basename(self.folders[0])
            if first_folder:
                default_name = first_folder
        ensure_database_directory()
        output_file = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title=self.t("save_pdf"),
            initialdir=DATABASE_DIR,
            initialfile=f"{default_name}.pdf"
        )
        if not output_file:
            self.status_label.configure(text=self.t("operation_cancelled"))
            return
        self.status_label.configure(text=self.t("creating_pdf"))
        self.status_label_bottom.configure(text=self.t("creating_pdf"))
        self.progress_window = ctk.CTkToplevel(self)
        self.progress_window.title(self.t("creation_window"))
        self.progress_window.geometry("400x150")
        self.progress_window.transient(self)
        self.progress_window.grab_set()
        progress_frame = ctk.CTkFrame(self.progress_window)
        progress_frame.pack(fill="both", expand=True, padx=20, pady=20)
        progress_label = ctk.CTkLabel(progress_frame, text=self.t("creation_progress"),
                                      font=ctk.CTkFont(size=14))
        progress_label.pack(pady=10)
        self.progress_bar = ctk.CTkProgressBar(progress_frame, width=300)
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)
        pdf_thread = threading.Thread(
            target=self.create_pdf_thread,
            args=(output_file, self.quality_var.get(), list(self.image_files), list(self.folders)),
            daemon=True
        )
        pdf_thread.start()

    def create_pdf_thread(self, output_file, quality_mode, image_files, folders):
        total_files = len(image_files)
        try:
            if total_files == 0:
                raise ValueError(self.t("no_images_selected"))
            images = []
            for i, img_path in enumerate(image_files):
                progress = i / total_files
                self.worker_queue.put(("conversion_progress", (progress, self.t("processing_image", current=i + 1, total=total_files))))
                with Image.open(img_path) as source_img:
                    img = source_img.convert('RGB')
                if quality_mode == "A4":
                    a4_width_px = int(8.27 * 300)
                    a4_height_px = int(11.69 * 300)
                    img_width, img_height = img.size
                    ratio = min(a4_width_px / img_width, a4_height_px / img_height)
                    new_size = (max(1, int(img_width * ratio)), max(1, int(img_height * ratio)))
                    new_img = Image.new('RGB', (a4_width_px, a4_height_px), (255, 255, 255))
                    offset = ((a4_width_px - new_size[0]) // 2, (a4_height_px - new_size[1]) // 2)
                    resized_img = img.resize(new_size, Image.LANCZOS)
                    new_img.paste(resized_img, offset)
                    img.close()
                    resized_img.close()
                    img = new_img
                images.append(img)
            images[0].save(
                output_file,
                save_all=True,
                append_images=images[1:],
                resolution=300.0,
                quality=95
            )
            for image in images:
                image.close()
            folder_names = ", ".join(os.path.basename(folder) for folder in folders)
            self.worker_queue.put(("conversion_progress", (1.0, self.t("finalizing"))))
            self.worker_queue.put((
                "conversion_done",
                (True, self.t("pdf_created", count=len(images), path=output_file), output_file, len(images), folder_names)
            ))
        except Exception as e:
            for image in locals().get("images", []):
                image.close()
            self.worker_queue.put((
                "conversion_done",
                (False, self.t("creation_error", error=str(e)), output_file, 0, "")
            ))

    def show_compression_info(self):
        """Mostra una finestra di dialogo con informazioni sulle modalità di compressione."""
        messagebox.showinfo(self.t("compression_info_title"), self.t("compression_info"))

if __name__ == "__main__":
    app = AdvancedPDFApp()
    app.mainloop()