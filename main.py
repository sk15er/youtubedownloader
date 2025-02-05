from yt_dlp import YoutubeDL
import os
from tkinter import *
from tkinter import messagebox
from typing import Optional
from urllib.parse import urlparse, parse_qs

def is_playlist_url(url: str) -> bool:
    """
    Check if the provided URL is a playlist or a single video.
    
    Args:
        url (str): YouTube URL to check
        
    Returns:
        bool: True if URL is a playlist, False if single video
    """
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    return 'list' in query_params

def download_youtube_content(url: str, output_path: Optional[str] = None, quality: str = 'best') -> None:
    """
    Download YouTube content (single video or playlist) in MP4 format only.
    
    Args:
        url (str): URL of the YouTube video or playlist
        output_path (str, optional): Directory to save the downloads. Defaults to './downloads'
        quality (str): Desired quality of the video ('best', '720p', '1080p', '4k')
    """
    if output_path is None:
        output_path = os.path.join(os.getcwd(), 'downloads')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    # Configure yt-dlp options for MP4 only
    format_option = {
        'best': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        '720p': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best',
        '1080p': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best',
        '4k': 'bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/best[height<=2160][ext=mp4]/best'
    }.get(quality, 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best')
    
    ydl_opts = {
        'format': format_option,
        'merge_output_format': 'mp4',
        'ignoreerrors': True,
        'no_warnings': False,
        'extract_flat': False,
        'writesubtitles': False,
        'writethumbnail': False,
        'writeautomaticsub': False,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", "Download completed!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def start_download():
    url = url_entry.get()
    save_path = path_entry.get().strip()
    quality = quality_var.get()
    
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL")
        return
    
    if not save_path:
        save_path = os.path.join(os.getcwd(), 'downloads')
    
    download_youtube_content(url, save_path, quality)

# Create the main window
window = Tk()
window.title("YouTube Video Downloader by sk")
window.geometry("600x400")
window.resizable(False, False)

# Create a frame for the main content
frame = Frame(window, padx=20, pady=20)
frame.pack(expand=True)

# URL entry
Label(frame, text="YouTube URL:", font=('Arial', 12)).grid(row=0, column=0, sticky=W, pady=5)
url_entry = Entry(frame, width=50, font=('Arial', 12))
url_entry.grid(row=0, column=1, pady=5)

# Save path entry
Label(frame, text="Save Path:", font=('Arial', 12)).grid(row=1, column=0, sticky=W, pady=5)
path_entry = Entry(frame, width=50, font=('Arial', 12))
path_entry.grid(row=1, column=1, pady=5)

# Quality selection
Label(frame, text="Select Quality:", font=('Arial', 12)).grid(row=2, column=0, sticky=W, pady=5)
quality_var = StringVar(value='best')
quality_options = ['best', '720p', '1080p', '4k']
OptionMenu(frame, quality_var, *quality_options).grid(row=2, column=1, pady=5)

# Download button
Button(frame, text="Download", command=start_download, bg='green', fg='white', font=('Arial', 12)).grid(row=3, columnspan=2, pady=20)

# Add your information in the bottom right corner
Label(window, text="shushank - shushankpawar664@gmail.com", font=('Arial', 10)).place(relx=1.0, rely=1.0, anchor='se')

# Run the main loop
window.mainloop()