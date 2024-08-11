try:
    import os
    import csv
    import time
    import subprocess
    from datetime import datetime
except:
    import os
    import subprocess
    import csv
    import time
    from datetime import datetime


def get_file_size(file_path):
    try:
        file_size = os.path.getsize(file_path) // 1024  # Convert bytes to kilobytes
        return file_size
    except:
        return False


def compress_videos(input_path, output_path, given_extension=None):
    global video_extensions
    # Flag to check any error
    any_error = False
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # List all files in the input directory
    files = os.listdir(input_path)

    # Filter video files 
    video_files = [file for file in files if file.lower().endswith(video_extensions)]

    # Open CSV file for writing
    csv_file_path = os.path.join(output_path, 'compression_data.csv')
    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(
            ['File', 'Actual File Size (KB)', 'Compressed File Size (KB)'])

        # Compress each video file
        for video_file in video_files:
            input_file_path = os.path.join(input_path, video_file)
            if given_extension is None:
                output_file_path = os.path.join(output_path, video_file)
            else:
                filename, _ = os.path.splitext(video_file)
                output_file_path = os.path.join(output_path, (f"{filename}.{given_extension}"))
                            
            # Get the actual file size before compression
            actual_size = get_file_size(input_file_path)
            if not actual_size:
                print("File couldn't be found, Check permissions")
                any_error = True
                break
            
            # Run ffmpeg command to compress the video            
            try:
                subprocess.run(["ffmpeg.exe", "-i", input_file_path, output_file_path], check=True)
            except subprocess.CalledProcessError:
                print(" Video compression failed.")
                return
            
            # Get the compressed file size after compression
            compressed_size = get_file_size(output_file_path)

            # Write data to CSV file
            csv_writer.writerow([video_file, actual_size, compressed_size])
            print(f" Compression successful: {video_file}")

    if any_error:
        return
    print(f" All videos compressed and exported to {output_directory}")
    print(f" Compression data written to {csv_file_path}")
    
    base_dir, last_dir = os.path.split(output_directory)
    if str(last_dir).upper() != "DESKTOP":
        os.system(f"explorer {output_directory}")
        
        
def compress_video():

    # Prompt the user for the input video file
    input_path = input(" Enter the path to the input video file: ").strip()
    
    # Remove quotes from the input path if present
    input_path = input_path.strip('"')
    
    # Check if the input file exists
    if not os.path.exists(input_path):
        print(" The specified input file does not exist.")
        return

    # Get the file name and directory of the input video
    input_dir, input_name = os.path.split(input_path)
    input_name, input_extension = os.path.splitext(input_name)
    
    choice = input(" Do you want to change the extension (Y/N): ").upper()
    
    if choice == "Y":
        given_extension = input(" Enter the extension without dot (.): ").lower().strip().strip(".")
        if given_extension not in video_extensions:
            print(" FFMPEG can't handle this video format!\n Try any other extensions.")
            return
        output_name = f"{input_name}_compressed.{given_extension}"
    else:
        # Specify the output file name with .mp4 extension
        output_name = f"{input_name}_compressed.{input_extension}"

    output_path = os.path.join(input_dir, output_name)
    start_time = time.time()
    
    # Compress the video using FFmpeg
    try:
        subprocess.run(["ffmpeg.exe", "-i", input_path, "-c:v", "libx264", "-crf", "23", "-c:a", "aac", "-strict", "experimental", "-b:a", "128k", output_path], check=True)
    except subprocess.CalledProcessError:
        print(" Video compression failed.")
        return
    
    print("\n Video compression successful. Output file:", output_path)
    print(f" Time Taken: {(time.time() - start_time):.2f} seconds") 
    base_dir, last_dir = os.path.split(input_dir)
    if str(last_dir).upper() != "DESKTOP":
        os.system(f"explorer {input_dir}")

    
def record_screen():
    # Get current date and time
    current_datetime = datetime.now()
    year = str(current_datetime.year)
    month = str(current_datetime.month).zfill(2)
    day = str(current_datetime.day).zfill(2)
    hour = str(current_datetime.hour).zfill(2)
    minute = str(current_datetime.minute).zfill(2)
    second = str(current_datetime.second).zfill(2)

    output_directory = None
    if os.path.exists("output_dir.txt"):    
        with open("output_dir.txt", 'r') as file:
            output_directory = file.read()
    else:
        print(" Output path does not exist!")
        return
    if output_directory is None or output_directory == '':
        print(" Output path is not given!")
        return
        
    output_filename = f"{year}-{month}-{day}-{hour}-{minute}-{second}.mp4"
    output_path = os.path.join(output_directory, output_filename)

    # Run ffmpeg command to record screen
    try:
        os.system(f"ffmpeg.exe -f gdigrab -i desktop -c:v libx264 -crf 25 -pix_fmt yuv420p {output_path}")
    except OSError:
        print(" Screen Recording Ended!")
        return
    
    
def extract_audio():

    # Prompt the user for the input video file
    input_path = input(" Enter the path to the input video file: ").strip()

    # Remove quotes from the input path if present
    input_path = input_path.strip('"')

    # Check if the input file exists
    if not os.path.exists(input_path):
        print(" The specified input file does not exist.")
        return

    # Get the file name and directory of the input video
    input_dir, input_name = os.path.split(input_path)
    input_name, input_extension = os.path.splitext(input_name)

    
    output_name = f"{input_name}.mp3"
    output_path = os.path.join(input_dir, output_name)
    start_time = time.time()
    # Compress the video using FFmpeg
    try:
        subprocess.run(["ffmpeg.exe", "-i", input_path, "-q:a", "0", "-map", "a", output_path], check=True)
    except subprocess.CalledProcessError:
        print(" Audio Extraction failed.")
        return
    
    print("\n Audio Extracted successfully. Output file:", output_path)
    print(f" Time Taken: {(time.time() - start_time):.2f} seconds")    

def image_converter(input_path, extension, single=True):
    
    # Get the file name and directory of the input video
    input_dir, input_name = os.path.split(input_path)
    input_name, input_extension = os.path.splitext(input_name)

    
    output_name = f"{input_name}.{extension}"
    if single:
        output_path = os.path.join(input_dir, output_name)
    else:
        output_dir = os.path.join((input_dir + f"_{extension}"))
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, output_name)
         
    try:
        subprocess.run(["ffmpeg.exe", "-i", input_path, output_path], check=True)
    except subprocess.CalledProcessError:
        print(" Conversion failed.")
        return
    
    print("\n Conversion successful. Output file:", output_path)
    
def audio_converter(input_path, extension, single):
    
    # Get the file name and directory of the input video
    input_dir, input_name = os.path.split(input_path)
    input_name, _ = os.path.splitext(input_name)
    
    output_name = f"{input_name}.{extension}"
    if single:
        output_path = os.path.join(input_dir, output_name)
    else:
        output_dir = os.path.join((input_dir + f"_{extension}"))
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, output_name)
         
    try:
        subprocess.run(["ffmpeg.exe", "-i", input_path, output_path], check=True)
    except subprocess.CalledProcessError:
        print(" Conversion failed.")
        return
    
    print("\n Conversion successful. Output file:", output_path)

        
if __name__ == "__main__":
    audio_extensions = (
        'aac', 'ac3', 'aif', 'aiff', 'alac', 'amr', 'ape', 'au', 'awb', 'flac', 'gsm', 'm4a',
        'm4b', 'm4p', 'mp3', 'ogg', 'oga', 'mogg', 'opus', 'ra', 'wav', 'wma', 'webm'
    )
    image_extensions = (
        'jpg', 'jpeg', 'png', 'tiff', 'tif', 'bmp', 'gif', 'webp', 'svg'
    )
    video_extensions = ('mp4', 'avi', 'mkv', 'mov', 'nix', 'org')
    
    while True:
        os.system("cls")
        os.system("color 0a")
        print(" ============================================")
        print("                     Menu                    ")
        print(" ============================================")
        print(" [1] Compress a video")
        print(" [2] Compress a directory of videos")
        print(" [3] Record Screen without audio")
        print(" [4] Save output path for Screen Recording")
        print(" [5] Extract Audio from Video")
        print(" [6] Convert Audio to any format")
        print(" [7] Convert Image into any format")
        print(" [8] Exit")
        try:
            choice = int(input("\n >> "))
        except:
            print(" Enter only integers!")
            continue
        
        if choice == 1:
            try:
                compress_video()
            except:
                continue

        elif choice == 2:
            # Input directory containing videos
            input_directory = input(" Enter the path of the input directory: ")

            # Remove surrounding quotes from input directory path
            input_directory = input_directory.strip('"')

            choice = input(" Do you want to change the extension (Y/N): ").upper()
    
            if choice == "Y":
                given_extension = input(" Enter the extension without dot (.): ").lower().strip().strip(".")

            
            # Output directory for compressed videos
            output_directory = os.path.join(input_directory + "_compressed")
            
            start_time = time.time()
            if given_extension:
                if given_extension in video_extensions:
                    # Compress videos
                    compress_videos(input_directory, output_directory, given_extension)
                else:
                    print(" FFMPEG can't handle this video format!\n Try any other extensions.")
                    input("\n Press enter to continue...")
                    continue
            else:
                compress_videos(input_directory, output_directory)
                
            print(f" Time Taken: {(time.time() - start_time):.2f} seconds")
            
        elif choice == 3:
            start_time = time.time()
            try:
                record_screen()
            except:
                # When you stop the video recording using ctrl + c
                with open("output_dir.txt", 'r') as file:
                    output_directory = file.read()
                print(" Screen recording completed.")
                print(f" Duration: {(time.time() - start_time):.2f} seconds")
                os.system(f"explorer {output_directory}")
                input("\n Press enter to continue...")
                continue   
            
        elif choice == 4:
            output_path = input(" Enter output path for screen recording: ").strip()
            output_path = output_path.replace('"', '')
            if os.path.exists(output_path):    
                with open("output_dir.txt", 'w') as file:
                    file.write(output_path)
                print(" Output path for screen recording is saved!")
            else:
                print(" Output Path does not exist!")
                
        elif choice == 5:
            extract_audio()
            
        elif choice == 6:
            input_path = input(" File/Direcotry Path: ").strip()
            
            extension = input(" Extension to convert: ").lower().strip().strip(".")
           
            if extension not in audio_extensions:
                print(" FFMPEG can't handle this video format!\n Try any other extensions.")
                input("\n Press enter to continue...")
                continue
            
            file_or_dir = input(" Single File or Directory of Files (s/d): ").lower().strip()
            input_path = input_path.strip('"')
            
            start_time = time.time()
            if file_or_dir == "s":
                audio_converter(input_path, extension, True)
            elif file_or_dir == "d":
                files = [file for file in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, file))]
                files = [file for file in files if file.lower().endswith(audio_extensions)]
                for file in files:
                    audio_converter(os.path.join(input_path, file), extension, False)
            else:
                print(" Invalid Choice!")
                input("\n Press enter to continue...")
                continue
            print(f" Time Taken: {(time.time() - start_time):.2f} seconds")  
              
        elif choice == 7:
            input_path = input(" File/Direcotry Path: ").strip()
            
            extension = input(" Extension to convert: ").lower().strip().strip(".")
            if extension not in image_extensions:
                print(" FFMPEG can't handle this video format!\n Try any other extensions.")
                input("\n Press enter to continue...")
                continue
            
            file_or_dir = input(" Single File or Directory of Files (s/d): ").lower().strip()
            input_path = input_path.strip('"')
            
            
            start_time = time.time()
            if file_or_dir == "s":
                image_converter(input_path, extension, True)
            elif file_or_dir == "d":
                files = [file for file in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, file))]
                files = [file for file in files if file.lower().endswith(image_extensions)]
                for file in files:
                    image_converter(os.path.join(input_path, file), extension, False)
            else:
                print(" Invalid Choice!")
                input("\n Press enter to continue...")
                continue
            print(f" Time Taken: {(time.time() - start_time):.2f} seconds")    

        elif choice == 8:
            exit()
            
        else:
            print("\n Invalid choice!")        
    
        input("\n Press enter to continue...")
