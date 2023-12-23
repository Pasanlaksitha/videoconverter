import subprocess
import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog

class VideoConverterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("MKV to MP4 Converter")

        self.input_files = []
        self.output_folder = tk.StringVar()
        self.output_folder.set(os.getcwd())

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Input Files:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.file_listbox = tk.Listbox(self.master, selectmode=tk.MULTIPLE, height=5, width=40)
        self.file_listbox.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tk.Button(self.master, text="Browse", command=self.browse_input_files).grid(row=0, column=2, padx=5, pady=5, sticky="w")

        tk.Label(self.master, text="Output Folder:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(self.master, textvariable=self.output_folder, width=30).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        tk.Button(self.master, text="Browse", command=self.browse_output_folder).grid(row=1, column=2, padx=5, pady=5, sticky="w")

        tk.Button(self.master, text="Convert", command=self.convert_videos).grid(row=2, column=0, columnspan=3, pady=10)

    def browse_input_files(self):
        files = filedialog.askopenfilenames(title="Select Video Files", filetypes=[("Video Files", "*.mkv;*.avi")])
        for file in files:
            self.file_listbox.insert(tk.END, file)

    def browse_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder.set(folder)

    def convert_videos(self):
        self.input_files = self.file_listbox.get(0, tk.END)
        output_folder = self.output_folder.get()

        for input_file in self.input_files:
            output_file = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(input_file))[0]}.mp4")
            threading.Thread(target=self.convert_video_thread, args=(input_file, output_file)).start()

    def convert_video_thread(self, input_file, output_file):
        try:
            command = [
                'ffmpeg',
                '-i', input_file,
                '-c:v', 'libx264',
                '-preset', 'medium',
                '-crf', '23',
                '-c:a', 'aac',
                '-strict', 'experimental',
                output_file
            ]

            output = subprocess.run(command, check=True)
            result = output.decode('utf-8').split('\n')
            print(result)
            print(f"Conversion successful. Output file: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error during conversion: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoConverterApp(root)
    root.mainloop()
