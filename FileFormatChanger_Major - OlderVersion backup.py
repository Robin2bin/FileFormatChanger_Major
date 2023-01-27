from moviepy.video.fx.speedx import speedx
import streamlit as st
from moviepy.editor import *
from proglog import ProgressBarLogger
from pytube import YouTube
from pytube import Playlist
import os

class MyBarLogger(ProgressBarLogger):
    def callback(self, **changes):
        # Every time the logger message is updated, this function is called with
        # the `changes` dictionary of the form `parameter: new value`.
        for (parameter, value) in changes.items():
            print('Parameter %s is now %s' % (parameter, value))

    def bars_callback(self, bar, attr, value, old_value=None):
        # Every time the logger progress is updated, this function is called
        percentage = (value / self.bars[bar]['total']) * 100
        status.progress(int(percentage))

st.set_page_config(page_title='File Converter App',layout="wide",page_icon="https://cdn.movavi.io/pages/0012/67/f97f4053080a1d1ecc3e23c4095de7e73522ea17.png")
logger = MyBarLogger()
hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                header {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
set_background = """
                <style>
                .stApp {
                     background-image: url("https://i.pinimg.com/originals/13/83/07/138307c749c670d6d5ebffcbf15fe025.jpg");
                     background-size: cover;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
#st.markdown(set_background, unsafe_allow_html=True)

def Youtube_casts(url):
    Download = YouTube(url)
    resolutions = ["--select--"]
    for resolution in Download.streams.filter(progressive=True):
        resolutions.append(resolution.resolution)
    res = st.selectbox("Choose your quality: ", (resolutions))
    if (res != "--select--"):
        st.success("You choose: " + res)
        st.write("Here is your file => " + "[View/Download](" +
                 Download.streams.filter(resolution=res, progressive=True)[0].url + ")")
        st.info("Not happy with the resolutions available! You can download upto 1080p with our desktop app try now")
        items = os.getcwd() + "/Robin2bin-Video2audio-Desktop.zip"
        with open(items, "rb") as file:
            btn = st.download_button(
                label='Download desktop application here' + " (" + f'{round(os.stat(items).st_size / (1024 * 1024), 1)}' + " MB)",
                data=file,
                file_name='Robin2bin-Video2audio-Desktop.zip',
                mime="application/octet-stream"
            )
with st.container():
    st.title("Format Changer App")
    st.header("Hi I am your app to change the format of your files: ")
    st.write("---")
    st.sidebar.header("Admin Portal")
    id = st.sidebar.text_input("Enter Login Id: ")
    password = hash(st.sidebar.text_input("Enter Password",type="password"))
    true_password = hash("PassFile@2023#")
    if(id and password):
        if(password == true_password):
            st.sidebar.success("Successfully loggged in as admin")
            with st.expander("ADMIN PORTAL"):
                file_uploads = st.file_uploader("Upoad your file")
                if file_uploads:
                    with open(file_uploads.name, "wb") as f:
                        f.write(file_uploads.read())
                    st.success(file_uploads.name + " uploaded successfully!")
                files = ["--select--"]
                for items in os.listdir(os.getcwd()):
                    if (".idea" in items):
                        pass
                    elif ("requirements.txt" in items):
                        pass
                    elif (".py" in items):
                        pass
                    elif (".git" in items):
                        pass
                    elif (".streamlit" in items):
                        pass
                    else:
                        files.append(items)
                sec = st.selectbox("Choose the file you want to delete: ",files)
                if(sec != "--select--"):
                    os.remove(sec)
                    st.success("Successfully deleted " + sec)
        else:
            st.sidebar.error("Incorrect id/password")


with st.container():
    st.subheader("Choose the service: ")
    left,right = st.columns(2)
    with left:
        st.subheader("Convert video files to audio files: ")
        video_file = st.file_uploader("Choose a video file", type=['mp4', 'avi'])
        st.subheader("OR")
        online_File = st.text_input("Enter Youtube URL: ")
        if(video_file):
            st.video(video_file)
            video = video_file.name
            with open(video,"wb") as f:
                f.write(video_file.read())
            output = "audio_file.wav"
            video = VideoFileClip(video)
            audio = video.audio
            status = st.progress(0)
            audio.write_audiofile(output,logger=logger)
            st.success("Successful Conversion!")
            st.audio(output)
            audio.close()
            video.close()
            os.remove(output)
            os.remove(video_file.name)
        elif(online_File):
            Download = YouTube(online_File)
            try:
                st.write("Here is your audio file => " + "[View/Download](" +
                         Download.streams.filter(type="audio",mime_type="audio/mp4")[0].url + ")")
            except Exception as e:
                st.error("This video has no audio")

    with right:
        st.subheader("Combine audio and video files: ")
        video_file = st.file_uploader("Choose your video file: ",type=['mp4','avi'])
        audio_file = st.file_uploader("Choose your audio file: ",type=['mp3','wav'])
        if(video_file and audio_file):
            st.video(video_file, format='video/mp4')
            video = video_file.name
            with open(video, "wb") as f:
                f.write(video_file.read())

            st.audio(audio_file)
            audio = audio_file.name
            with open(audio, "wb") as f:
                f.write(audio_file.read())
            Video = VideoFileClip(video)
            Audio = AudioFileClip(audio)
            vid_duration = Video.duration
            audio_duration = Audio.duration
            output = 'final_video.mp4'
            final_clip = None
            if (vid_duration < audio_duration or vid_duration > audio_duration):
                audio = AudioFileClip(audio)
                video = VideoFileClip(video).fx(speedx, vid_duration / audio_duration)
                final_clip = video.set_audio(audio)
            else:
                video = VideoFileClip(video)
                audio = AudioFileClip(audio)
                final_clip = video.set_audio(audio)
            status = st.progress(0)
            final_clip.write_videofile(output, logger=logger)
            st.success("Successfull conversion")
            st.video(output)
            os.remove(output)
            audio.close()
            video.close()
            Video.close()
            Audio.close()
            os.remove(video_file.name)
            os.remove(audio_file.name)

with st.container():
    st.header("Youtube video downloader: ")
    url = st.text_input(label="Enter youtube URL: ")
    if(url):
        if("playlist" not in url):
            Youtube_casts(url)
        else:
            Player = Playlist(url)
            videos = ["--Select--"]
            urls = ["--select--"]
            for i in Player.video_urls:
                name = YouTube(i)
                videos.append(name.title)
                urls.append(i)
            sec_vid = st.selectbox("Choose the video: ",videos)
            if(sec_vid != "--Select--"):
                st.success("You choose = " + sec_vid)
                Youtube_casts(urls[videos.index(sec_vid)])



with st.container():
    st.write("---")
    left,middle,right_middle,right = st.columns(4)
    with left:
        st.subheader("Developer Contact: ")
        st.write("Contact us: cosmosbeta99@gmail.com")
    with middle:
        st.subheader("Explore our channel")
        st.write("[Check out here>](https://www.youtube.com/c/robin2bin)")
    with right_middle:
        st.subheader("Want to get more feature?")
        st.write("Try our desktop app version: ")
        items = os.getcwd() + "/Robin2bin-Video2audio-Desktop.zip"
        with open(items, "rb") as file:
            btn = st.download_button(
                label= 'Robin2bin-Video2audio-Desktop.zip' + " (" + f'{round(os.stat(items).st_size / (1024 * 1024),1)}' + " MB)",
                data=file,
                file_name='Robin2bin-Video2audio-Desktop.zip',
                mime="application/octet-stream"
            )
    with right:
        st.image("https://yt3.ggpht.com/ytc/AMLnZu-iZi_tq1cWBc90QKMCe3WSRXDn7L_ny9i57CSj=s900-c-k-c0x00ffffff-no-rj",width=200)
