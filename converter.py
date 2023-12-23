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
# live print converting video to mp4
    try:
        process = subprocess.Popen(command, stderr=subprocess.PIPE, text=True)
        
        while True:
            output_line = process.stderr.readline()
            if output_line == '' and process.poll() is not None:
                break
            print(output_line.strip())  # Adjust as needed

        process.wait()

        if process.returncode == 0:
            print(f"Conversion successful. Output file: {output_file}")
        else:
            print(f"Error during conversion. Return code: {process.returncode}")

    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")

    # try:
    #     output = subprocess.run(command, capture_output=True).stderr
    #     result = output.decode('utf-8').split('\n')
    #     print(result)
    #     print(f"Conversion successful. Output file: {output_file}")
    # except subprocess.CalledProcessError as e:
    #     print(f"Error during conversion: {e}")
    # return e

if __name__ == "__main__":
    input_file = 'sample.mkv'
    output_file = 'output.mp4'

    error = convert_video(input_file, output_file)
    print()
