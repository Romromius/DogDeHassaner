import os
import shutil
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pathlib import Path

class PhotoSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Сортировка фото")
        self.root.geometry("800x600")
        
        self.source_dir = Path("SOURCE")
        self.output_dirs = {
            "1": "normal",
            "2": "sniff", 
            "3": "pick"
        }
        
        for dir_name in self.output_dirs.values():
            (self.source_dir / dir_name).mkdir(parents=True, exist_ok=True)
        
        self.photos = []
        for f in self.source_dir.glob("*.png"):
            if f.is_file():
                self.photos.append(f)
        self.photos.sort()
        
        self.current_index = 0
        self.total_photos = len(self.photos)
        
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
        
        self.quit_button = tk.Button(self.root, text="Выйти", command=self.quit_app, 
                                     font=("Times New Roman", 20))
        self.quit_button.pack(pady=5)
        
    def bind_keys(self):
        self.root.bind('1', lambda e: self.sort_photo('1'))
        self.root.bind('2', lambda e: self.sort_photo('2'))
        self.root.bind('3', lambda e: self.sort_photo('3'))
        self.root.bind('<KP_1>', lambda e: self.sort_photo('1'))
        self.root.bind('<KP_2>', lambda e: self.sort_photo('2'))
        self.root.bind('<KP_3>', lambda e: self.sort_photo('3'))
        
    def show_current_photo(self):
        if self.current_index >= self.total_photos:
            self.complete_sorting()
            return
            
        self.progress_label.config(text=f"Фото {self.current_index + 1} из {self.total_photos}")
        
        photo_path = self.photos[self.current_index]
        img = Image.open(photo_path)
        
        display_size = (700, 500)
        img.thumbnail(display_size, Image.Resampling.LANCZOS)
        
        self.photo_image = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.photo_image)
        
    def sort_photo(self, category_key):
        if self.current_index >= self.total_photos:
            return
            
        current_photo = self.photos[self.current_index]
        category = self.output_dirs[category_key]
        dest_dir = self.source_dir / category
        
        shutil.copy2(current_photo, dest_dir)
        
        self.current_index += 1
        
        if self.current_index < self.total_photos:
            self.show_current_photo()
        else:
            self.complete_sorting()
            
    def complete_sorting(self):
        messagebox.showinfo("Завершено", 
                           f"Сортировка завершена!\nВсе {self.total_photos} фото распределены по папкам.")
        self.quit_app()
        
    def quit_app(self):
        self.root.quit()
        self.root.destroy()

def main():
    if not os.path.exists("SOURCE"):
        os.makedirs("SOURCE")
        print("=" * 50)
        print("СОЗДАНА ПАПКА 'SOURCE'")
        print("Положите туда фото 1.png, 2.png и т.д.")
        print("Затем запустите программу снова")
        print("=" * 50)
        input("Нажмите Enter для выхода...")
        return
    
    source_dir = Path("SOURCE")
    photos = []
    for f in source_dir.glob("*.png"):
        if f.is_file():
            photos.append(f)
    
    if not photos:
        print("=" * 50)
        print("В папке 'SOURCE' нет PNG файлов для сортировки")
        print("Добавьте файлы 1.png, 2.png и т.д.")
        print("=" * 50)
        input("Нажмите Enter для выхода...")
        return
    
    root = tk.Tk()
    app = PhotoSorterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
