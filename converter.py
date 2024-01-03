import subprocess
import os


def convert_video(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return

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
        subprocess.run(command, check=True)
        print(f"Conversion successful. Output file: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
    return e

if __name__ == "__main__":
    input_file = input()
    output_file = 'output.mp4'

    error = convert_video(input_file, output_file)
    print()
