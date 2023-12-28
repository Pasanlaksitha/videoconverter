import subprocess
import os
import sys
import re

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

        duration = re.compile(r'DURATION: ([\d:.]+)')
        frame_pattern = re.compile(r'frame=\s+(\d+)')
        fps_pattern = re.compile(r'fps=([\d.]+)')
        time_pattern = re.compile(r'time=([\d:.]+)')
        bitrate_pattern = re.compile(r'bitrate=([\d.]+kbits/s)')
        speed_pattern = re.compile(r'speed=([\d.]+x)')

        # Read and print output in real-time
        while True:
            output_line = process.stderr.readline()
            if output_line == '' and process.poll() is not None:
                break

            #print(output_line.strip())

            frame_match = frame_pattern.search(output_line)
            fps_match = fps_pattern.search(output_line)
            time_match = time_pattern.search(output_line)
            bitrate_match = bitrate_pattern.search(output_line)
            speed_match = speed_pattern.search(output_line)

            if frame_match:
                frame = frame_match.group(1)
                print(f"Frame: {frame}")

            if fps_match:
                fps_value = fps_match.group(1)
                print(f"FPS: {fps_value}")

            if time_match:
                time_value = time_match.group(1)
                print(f"Time: {time_value}")

            # if bitrate_match:
            #     bitrate = float(bitrate_match.group(1))
            #     print(f"Bitrate: {bitrate} kbits/s")

            if speed_match:
                speed_str = speed_match.group(1)
                speed = float(speed_str.rstrip('x'))
                print(f"Speed: {speed}x")

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
    print(error)
