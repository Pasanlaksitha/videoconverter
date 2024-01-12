import subprocess
import os
import threading
import tkinter as tk
from tkinter import filedialog

class VideoConverterApp:

    def __init__(self, master):
        self.master = master
        self.master.title("MKV to MP4 Converter")

        self.input_files = []
        self.output_folder = tk.StringVar()
        self.output_folder.set(os.getcwd())

        self.create_widgets()

    def create_widgets(self):
        """
        Create the GUI widgets for the application.
        """
        tk.Label(self.master, text="Input Files:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.file_listbox = tk.Listbox(self.master, selectmode=tk.MULTIPLE, height=5, width=40)
        self.file_listbox.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tk.Button(self.master, text="Browse", command=self.browse_input_files).grid(row=0, column=2, padx=5, pady=5, sticky="w")

        tk.Label(self.master, text="Output Folder:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(self.master, textvariable=self.output_folder, width=30).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        tk.Button(self.master, text="Browse", command=self.browse_output_folder).grid(row=1, column=2, padx=5, pady=5, sticky="w")
        tk.Button(self.master, text="Convert", command=self.convert_videos).grid(row=2, column=0, columnspan=3, pady=10)

    def browse_input_files(self):
        """
        Open a file dialog to select input video files and add them to the file listbox.
        """
        files = filedialog.askopenfilenames(title="Select Video Files", filetypes=[("Video Files", "*.mkv;*.avi")])
        for file in files:
            self.file_listbox.insert(tk.END, file)

    def browse_output_folder(self):
        """
        Open a folder dialog to select the output folder and set it as the output folder path.
        """
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder.set(folder)

    def convert_videos(self):
        """
        Convert the selected input video files to MP4 format using FFmpeg.
        """
        self.input_files = self.file_listbox.get(0, tk.END)
        output_folder = self.output_folder.get()

        for input_file in self.input_files:
            output_file = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(input_file))[0]}.mp4")
            threading.Thread(target=self.convert_video_thread, args=(input_file, output_file)).start()

    def convert_video_thread(self, input_file, output_file):
        """
        Convert a single video file to MP4 format using FFmpeg in a separate thread.

        Args:
            input_file (str): The path of the input video file.
            output_file (str): The path of the output MP4 file.
        """
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
        
        try:
            output = subprocess.run(command, check=True)
            result = output.decode('utf-8').split('\n')
            print(result)
            print(f"Conversion successful. Output file: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error during conversion: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("icon.ico")
    app = VideoConverterApp(root)
    root.mainloop()
