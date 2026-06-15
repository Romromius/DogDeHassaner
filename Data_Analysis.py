import os
import shutil
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from manifest_reader import ManifestReader
import logging
import sys

logger = logging.getLogger(__name__)
logging.FileHandler("latest.log", mode='w')
logging.basicConfig(handlers=[
    logging.FileHandler("latest.log"),  # Write to file
    logging.StreamHandler(sys.stdout)   # Print to console
    ], level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s")
logger.info('Started')

class PhotoType:  # Для удобного использования set_type
    none = 0
    normal = 1
    sniff = 2
    pick = 3

class PhotoSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Сортировка фото")
        self.root.geometry("800x600")
        
        # self.source_dir = Path("SOURCE")
        # self.output_dirs = {
        #     "1": "normal",
        #     "2": "sniff",
        #     "3": "pick"
        # }
        
        # for dir_name in self.output_dirs.values():
        #     (self.source_dir / dir_name).mkdir(parents=True, exist_ok=True) // Убираем прямую сортировку, будем записывать в manifest
        
        # self.photos = []
        # for f in self.source_dir.glob("*.png"):
        #     if f.is_file():
        #         self.photos.append(f)
        # self.photos.sort()

        self.manifest = ManifestReader("manifest.json")
        
        self.current_index = 1
        self.total_photos = self.manifest.total

        while self.manifest.get_type(self.current_index):
            if self.current_index == self.total_photos:
                print("Все фото отсортированы!")
                print("Эта программа не доделана, так что ввиду того, что все фото отсортированы, не будет открываться.")
                print("Попробуйте установить null на последнее фото в manifest.json чтобы запустить программу")
                # TODO: Сделать нормально
                quit()
            self.current_index += 1
        
        self.setup_ui()
        
        self.bind_keys()
        
        self.show_current_photo()
        
    def setup_ui(self):
        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.progress_label = tk.Label(self.info_frame, text="", font=("Arial", 12))
        self.progress_label.pack()
        
        self.hint_label = tk.Label(self.info_frame, 
                                   text="Нажмите 1 (normal), 2 (sniff) или 3 (pick) для сортировки",
                                   font=("Times New Roman", 20))
        self.hint_label.pack(pady=5)
        
        self.quit_button = tk.Button(self.root, text="Выйти", command=self.complete_sorting,
                                     font=("Times New Roman", 20))
        self.quit_button.pack(pady=5)
        self.undo_button = tk.Button(self.root, text="Назад", command=self.undo,
                                     font=("Times New Roman", 20))
        self.undo_button.pack(pady=5)

    def undo(self):
        self.manifest.set_type(self.current_index, PhotoType.none)
        self.current_index -= 1
        self.show_current_photo()
        
    def bind_keys(self):
        self.root.bind('1', lambda e: self.sort_photo(PhotoType.normal))
        self.root.bind('2', lambda e: self.sort_photo(PhotoType.sniff))
        self.root.bind('3', lambda e: self.sort_photo(PhotoType.pick))
        self.root.bind('<KP_1>', lambda e: self.sort_photo(PhotoType.normal))
        self.root.bind('<KP_2>', lambda e: self.sort_photo(PhotoType.sniff))
        self.root.bind('<KP_3>', lambda e: self.sort_photo(PhotoType.pick))
        
    def show_current_photo(self):
        if self.current_index >= self.total_photos + 1:
            self.complete_sorting()
            return
            
        self.progress_label.config(text=f"Фото {self.current_index} из {self.total_photos}")
        
        photo_path = "SOURCE/" + str(self.current_index) + ".png"
        img = Image.open(photo_path)
        
        display_size = (700, 500)
        img.thumbnail(display_size, Image.Resampling.LANCZOS)
        
        self.photo_image = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.photo_image)
        
    def sort_photo(self, category_key):
        if self.current_index >= self.total_photos + 1:
            return

        self.manifest.set_type(self.current_index, category_key)
        
        self.current_index += 1
        
        if self.current_index < self.total_photos:
            self.show_current_photo()
        else:
            self.complete_sorting()
            
    def complete_sorting(self):
        self.manifest.commit()
        messagebox.showinfo("Завершено",
                           f"Сортировка завершена!\nФото размечены вплоть до {self.current_index - 1}-го.")
        self.quit_app()
        
    def quit_app(self):
        self.root.quit()
        self.root.destroy()

def main():
    if not os.path.exists("manifest.json"):
        print("=" * 50)
        print("файл manifest.json не найден")
        print("Используйте video-to-photo.py")
        print("Затем запустите программу снова")
        print("=" * 50)
        input("Нажмите Enter для выхода...")
        return

    # source_dir = Path("SOURCE")
    # photos = []
    # for f in source_dir.glob("*.png"):
    #     if f.is_file():
    #         photos.append(f)
    
    # if not photos:
    #     print("=" * 50)
    #     print("В папке 'SOURCE' нет PNG файлов для сортировки")
    #     print("Добавьте файлы 1.png, 2.png и т.д.")
    #     print("=" * 50)
    #     input("Нажмите Enter для выхода...")
    #     return

    interface = ManifestReader("manifest.json")

    remain = 0

    for i in range(1, interface.total + 1):
        if interface.get_type(i) is None:
            remain += 1

    logger.info(f"У нас {remain} неразмеченых фото.")
    
    root = tk.Tk()
    app = PhotoSorterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
