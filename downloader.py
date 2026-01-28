
import os
import sys
import subprocess

# Add ffmpeg to PATH if running as PyInstaller bundle
if getattr(sys, 'frozen', False):
    # Running as PyInstaller bundle
    bundle_dir = sys._MEIPASS
    ffmpeg_path = os.path.join(bundle_dir, 'ffmpeg', 'bin')
    if os.path.exists(ffmpeg_path):
        os.environ['PATH'] = ffmpeg_path + os.pathsep + os.environ.get('PATH', '')
else:
    # Running as script - add local ffmpeg to PATH
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ffmpeg_path = os.path.join(script_dir, 'ffmpeg', 'bin')
    if os.path.exists(ffmpeg_path):
        os.environ['PATH'] = ffmpeg_path + os.pathsep + os.environ.get('PATH', '')

def install_dependencies():
    """
    Automatically installs required dependencies if they're missing.
    """
    dependencies = ['yt-dlp']
    
    for package in dependencies:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            print(f"Installing {package}...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✓ {package} installed successfully!")
            except subprocess.CalledProcessError:
                print(f"✗ Failed to install {package}. Please install manually: pip install {package}")
                return False
    return True

# Install dependencies if needed
if not install_dependencies():
    input("Press Enter to exit...")
    sys.exit(1)

try:
    import yt_dlp
except ImportError:
    print("Error: 'yt-dlp' library not found.", file=sys.stderr)
    print("Please install it by running: pip install yt-dlp", file=sys.stderr)
    input("Press Enter to exit...")
    sys.exit(1)

def get_available_resolutions(video_url):
    """
    Fetches available video resolutions for the given URL.
    Returns a list of available resolutions sorted from highest to lowest.
    """
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
        resolutions = set()
        
        # Extract resolutions from available formats
        for fmt in info.get('formats', []):
            height = fmt.get('height')
            if height and fmt.get('vcodec') != 'none':  # Only video formats
                if height >= 2160:
                    resolutions.add('4k')
                elif height >= 1440:
                    resolutions.add('1440')
                elif height >= 1080:
                    resolutions.add('1080')
                elif height >= 720:
                    resolutions.add('720')
                elif height >= 480:
                    resolutions.add('480')
                elif height >= 360:
                    resolutions.add('360')
                elif height >= 240:
                    resolutions.add('240')
        
        # Sort resolutions from highest to lowest
        resolution_order = ['4k', '1440', '1080', '720', '480', '360', '240']
        available = [res for res in resolution_order if res in resolutions]
        
        return available
        
    except Exception as e:
        print(f"Warning: Could not fetch available resolutions. Error: {e}")
        return ['1080', '720', '480']  # Default fallback

def download_video():
    """
    Prompts the user for a video URL, resolution, and output path,
    then downloads the video with the best available audio merged into it.
    """
    print("--- YouTube Video Downloader ---")
    print("This script downloads a video with the best audio included.")
    print("FFmpeg is bundled with this application for merging streams.")
    print("-" * 30)

    # 1. Get Video URL
    video_url = input("Enter the video URL: ")
    if not video_url:
        print("Video URL cannot be empty.", file=sys.stderr)
        return

    # 2. Get available resolutions and display them
    print("Fetching available resolutions...")
    available_resolutions = get_available_resolutions(video_url)
    
    if available_resolutions:
        resolution_examples = ', '.join(available_resolutions)
        resolution_prompt = f"Enter desired video resolution (e.g., {resolution_examples}): "
    else:
        resolution_prompt = "Enter desired video resolution (e.g., 1080, 720, 480): "
    
    resolution_input = input(resolution_prompt).strip().lower()
    
    # Convert resolution input to numeric value
    resolution_map = {
        '4k': 2160,
        '1440': 1440,
        '1080': 1080,
        '720': 720,
        '480': 480,
        '360': 360,
        '240': 240
    }
    
    # Handle both numeric and text input
    if resolution_input in resolution_map:
        resolution = resolution_map[resolution_input]
        resolution_display = resolution_input
    else:
        try:
            resolution = int(resolution_input)
            # Convert back to display format
            if resolution >= 2160:
                resolution_display = '4k'
            elif resolution >= 1440:
                resolution_display = '1440p'
            else:
                resolution_display = f'{resolution}p'
        except ValueError:
            print("Invalid input. Please enter a valid resolution.", file=sys.stderr)
            return

    # 3. Get Output Folder
    output_folder_prompt = r"Enter the full path for the output folder (or press Enter to save to Desktop\yt downloads): "
    output_folder = input(output_folder_prompt)

    # If the user just presses Enter, set the default path
    if not output_folder:
        output_folder = os.path.join(os.path.expanduser('~'), 'Desktop', 'yt downloads')
        print(f"No folder specified. Using default path: {output_folder}")

    # Create the directory if it doesn't exist
    if not os.path.isdir(output_folder):
        print(f"Directory not found. Creating folder: {output_folder}")
        try:
            os.makedirs(output_folder, exist_ok=True)
        except OSError as e:
            print(f"Error: Could not create directory. {e}", file=sys.stderr)
            return

    print("-" * 30)
    print(f"Starting download for: {video_url}")
    print(f"Requested resolution: {resolution_display}")
    print(f"Saving files to: {output_folder}")
    print("-" * 30)

    try:
        # 4. Set yt-dlp options
        # This configuration attempts to download the best video up to the specified
        # resolution and the best audio, merging them into a single file.
        ydl_opts = {
            'format': f'bestvideo[height<={resolution}]+bestaudio[acodec!=opus]/best[height<={resolution}]',
            'outtmpl': os.path.join(output_folder, f'%(title)s-{resolution_display}.%(ext)s'),
            'addmetadata': True,
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'progress_hooks': [lambda d: print(d['_percent_str'], end='\r') if d['status'] == 'downloading' else None],
        }

        # 5. Execute download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        print("\n--- Download Complete! ---")
        print(f"The video has been saved in: {output_folder}")
        input("\nPress Enter to continue...")

    except yt_dlp.utils.DownloadError as e:
        print(f"\nError: Could not download the video.", file=sys.stderr)
        print(f"Details: {e}", file=sys.stderr)
        print("Please check the URL, resolution, and your network connection.", file=sys.stderr)
        print("If the error mentions FFmpeg, please ensure it is installed and accessible.", file=sys.stderr)
        input("\nPress Enter to continue...")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        input("\nPress Enter to continue...")

def main():
    """Main function with loop for multiple downloads."""
    while True:
        try:
            download_video()
            
            # Ask if user wants to download another video
            print("\n" + "="*50)
            choice = input("Do you want to download another video? (y/n): ").strip().lower()
            if choice not in ['y', 'yes']:
                break
                
        except KeyboardInterrupt:
            print("\n\nDownload cancelled by user.")
            break
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            input("Press Enter to continue...")
            break
    
    print("\nThank you for using YouTube Video Downloader!")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
