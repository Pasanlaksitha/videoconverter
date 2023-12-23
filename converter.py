import subprocess
import os
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

        #duration = re.compile(r'DURATION: ([\d:.]+)')
        frames = re.compile(r'frame=\s+(\d+)')
        fps = re.compile(r'fps=([\d.]+)')
        time = re.compile(r'time=([\d:.]+)')
        bitrate = re.compile(r'bitrate=([\d.]+kbits/s)')
        speed = re.compile(r'speed=([\d.]+x)')
        while True:
            output_line = process.stderr.readline()
            if output_line == '' and process.poll() is not None:
                break
            #print(output_line.strip())


            frame_ = frames.search(output_line)
            fps_ = fps.search(output_line)
            time_ = time.search(output_line)
            bitrate_ = bitrate.search(output_line)
            speed_ = speed.search(output_line)

            if frame_:
                frame = int(frame_.group(1))
                print(f"Frame: {frame}")

            if fps_:
                fps = float(fps_.group(1))
                print(f"FPS: {fps}")

            if time_:
                time_value = time_.group(1)
                print(f"Time: {time_value}")

            if bitrate_:
                bitrate = float(bitrate_.group(1))
                print(f"Bitrate: {bitrate} kbits/s")

            if speed_:
                speed = float(speed_.group(1))
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
    print()
