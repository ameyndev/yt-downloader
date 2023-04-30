import tkinter
import customtkinter
from pytube import YouTube

# Function to download
def start_download():
    try:
        yt_link = link.get()
        yt_object = YouTube(yt_link, on_progress_callback=track_progress)
        highest_res_vid = yt_object.streams.get_highest_resolution()
        # title.configure(text=yt_object.title)
        video_title = yt_object.title
        highest_res_vid.download()
        finish_label.configure(text="Download complete!", text_color="green")
        print("Download complete!")
    except:
        finish_label.configure(text="Something went wrong!", text_color="red")
        print("Something went wrong")

def track_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    complete_percentage = bytes_downloaded / total_size * 100
    complete_percentage_string = str(int(complete_percentage))
    progress_no.configure(text=complete_percentage_string + '%')
    progress_no.update()
    progress_bar.set(float(complete_percentage) / 100)

# System settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Frame
window = customtkinter.CTk()
window.geometry("720x480")
window.title("Youtube Downloader")

# UI
title = customtkinter.CTkLabel(window, text="Insert URL")
title.pack(padx=10, pady=10)

url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(window, width=350, height=40, textvariable=url_var)
link.pack()

finish_label = customtkinter.CTkLabel(window, text="")
finish_label.pack(padx=10, pady=10)

progress_no = customtkinter.CTkLabel(window, text="0%")
progress_no.pack()

progress_bar = customtkinter.CTkProgressBar(window, width=400)
progress_bar.set(0)
progress_bar.pack(padx=10, pady=10)

download_button = customtkinter.CTkButton(window, text="Download", command=start_download)
download_button.pack(padx=10, pady=10)

# This keeps the window open
window.mainloop()