import tkinter
from tkinter import ttk
import customtkinter as ctk
from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip
import os
# import ffmpeg

def start_download():
    yt_object = YouTube(link_entry.get(), on_progress_callback=track_progress)
    # 720p download
    if choice_menu.get() == '720p':
        yt_stream = yt_object.streams.get_highest_resolution()
        try:
            yt_stream.download()
            print("Download Complete")
            finish_label.configure(text="Download complete!", text_color="green")
        except:
            print("Something went wrong")
            finish_label.configure(text="Something went wrong", text_color="red")
    # audio download
    elif choice_menu.get() == 'audio':
        yt_stream = yt_object.streams.filter(only_audio=True).first()
        try:
            yt_stream.download()
            print("Download Complete")
            finish_label.configure(text="Download complete!", text_color="green")
        except:
            print("Something went wrong")
            finish_label.configure(text="Something went wrong", text_color="red")
    # 1080p download
    elif choice_menu.get() == '1080p':
        vid_title = yt_object.title
        yt_stream_audio = yt_object.streams.filter(only_audio=True).first()
        yt_stream_video = yt_object.streams.filter(res="1080p", progressive=False).first()
        video_title = yt_object.title
        try:
            audio_filename = yt_stream_audio.download(filename_prefix="audio")
            print("audio downloaded")
            video_filename = yt_stream_video.download()
            print("video downloaded")
            merged_file = "merged_output.mp4"
            video_clip = VideoFileClip(video_filename)
            audio_clip = AudioFileClip(audio_filename)
            final_clip = video_clip.set_audio(audio_clip)
            final_clip.write_videofile(merged_file, codec="libx264", audio_codec="aac")
            video_clip.close()
            audio_clip.close()
            final_clip.close()
            os.remove(video_filename)
            os.remove(audio_filename)
            finish_label.configure(text="Download complete!", text_color="green")
            print("Download complete")
        except Exception as e:
            print("The error is: ", e)
            print("Something went wrong downloading 1080p video")
            finish_label.configure(text="Something went wrong downloading 1080p video", text_color="red")

def track_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    complete_percentage = bytes_downloaded / total_size * 100
    complete_percentage_string = str(int(complete_percentage))
    progress_no.configure(text=complete_percentage_string + '%')
    progress_no.update()
    progress_bar.set(float(complete_percentage) / 100)

root = ctk.CTk()
root.geometry("720x480")
root.title("YouTube Downloader")

# title_label = ctk.CTkLabel(root, text="YouTube Downloader")
# title_label.pack()

insert_url_label = ctk.CTkLabel(root, text="Insert URL", font=ctk.CTkFont(size=18, weight="bold"))
insert_url_label.pack(padx=10, pady=10)

url_var = tkinter.StringVar()
link_entry = ctk.CTkEntry(root, width=400, textvariable=url_var)
link_entry.pack(pady=10)

choose_type_label = ctk.CTkLabel(root, text="Choose download type: ")
choose_type_label.pack()

choice_menu = ctk.CTkOptionMenu(root, values=["720p", "audio", "1080p"])
choice_menu.pack()

finish_label = ctk.CTkLabel(root, text="")
finish_label.pack(padx=10, pady=10)

progress_no = ctk.CTkLabel(root, text="0%")
progress_no.pack()

progress_bar = ctk.CTkProgressBar(root, width=400)
progress_bar.set(0)
progress_bar.pack(padx=10, pady=10)

download_button = ctk.CTkButton(root, text="Download", command=start_download)
download_button.pack(padx=10, pady=10)

root.mainloop()