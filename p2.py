import os
import subprocess
import json

class P2:
    def __init__(self, video_input):
        self.video_input = video_input

    def parse_video(self):
        # This way of storing the metadata shown in the output error was explained me by Alexander Vera
        subprocess.call(
            "ffmpeg -i " + self.video_input , shell=True)
    #        "ffprobe -hide_banner -loglevel fatal -show_error -show_format  -show_programs -show_chapters -show_private_data -print_format json <" + video_input + ">", shell=True)
        output_metadata = subprocess.Popen(["ffmpeg", "-y", "-i", self.video_input],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)

        stdout, stderr = output_metadata.communicate()
        data = stderr.decode("ascii")
        duration_index = data.index("Duration: ")
        duration = data[duration_index + 10 : duration_index + 10 + 11]
        print("Duration: " + duration)
        title_index = data.index("title")
        title = data[title_index + 18 : title_index + 18 + 33]
        print("Title: " + title)
        bitrate_index = data.index("bitrate: ")
        bitrate = data[bitrate_index + 9 : bitrate_index + 9 + 9]
        print("Bitrate: " + bitrate)

    def split_video_audio_mp3(self, audio_output):
        subprocess.call(
            "ffmpeg -y -i " + self.video_input + " " + audio_output, shell=True)

    def split_video_audio_low_bitrate_aac(self, audio_output):
        subprocess.call(
            "ffmpeg -y -i " + self.video_input + " -codec:a aac -b:a 64k " + audio_output, shell=True)

    def join_mp4_video_acc(self, audio_mp3, audio_aac, video_output):
        subprocess.call("ffmpeg -y -i " + self.video_input +
                        " -i " + audio_mp3 +
                        " -i " + audio_aac +
                        " -map 0:v -c:v copy -map 1:a -c:a copy -map 2:a -c:a copy " + video_output
                        , shell=True)

    def resize_video(self, resolution_x, resolution_y, video_output):
        if os.path.exists(video_output):
            os.remove(video_output)
        subprocess.call("ffmpeg -i " + self.video_input +
                        " -vf scale=" +
                        resolution_x + ":" +
                        resolution_y + " " +
                        video_output, shell=True)

    def broadcast_audio(self):
        subprocess.call(
            "ffmpeg -i " + self.video_input , shell=True)
    #        "ffprobe -hide_banner -loglevel fatal -show_error -show_format  -show_programs -show_chapters -show_private_data -print_format json <" + video_input + ">", shell=True)
        output_metadata = subprocess.Popen(["ffmpeg", "-y", "-i", self.video_input],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)

        stdout, stderr = output_metadata.communicate()
        data = stderr.decode("ascii")
        audio_formats = []
        index_audio_format = data.index("Audio")
        #audio_f = data[index_audio_format+7:index_audio_format+7+4]
        #audio_formats.append(audio_f)
        occurrences = data.count("Audio")
        for i in range(occurrences):
            #i = index_audio_format + 60
            index_audio = data.index("Audio", index_audio_format + i, len(data))
            audio_f = data[index_audio+7:index_audio+7+3]
            audio_formats.append(audio_f)
            index_audio_format = index_audio
        print("Audio formats of this video: ")
        print(audio_formats)
        broadcasting_standards = ["DVB", "ISDB", "ATSC", "DTMB"]
        output = []
        for i in audio_formats:
            if i == "mp3":
                output.append(broadcasting_standards[0])
                output.append(broadcasting_standards[3])
                print("Compatible broadcasting standards fot mp3:")
                print(output)
                output = []
            if i == "ac3":
                output.append(broadcasting_standards[0])
                output.append(broadcasting_standards[2])
                output.append(broadcasting_standards[3])
                print("Compatible broadcasting standards fot ac-3:")
                print(output)
                output = []
            if i == "aac":
                output.append(broadcasting_standards[0])
                output.append(broadcasting_standards[1])
                output.append(broadcasting_standards[3])
                print("Compatible broadcasting standards fot aac:")
                print(output)
                output = []
            if i == "dra":
                output.append(broadcasting_standards[3])
                print("Compatible broadcasting standards fot dra:")
                print(output)
                output = []
            if i == "mp2":
                output.append(broadcasting_standards[3])
                print("Compatible broadcasting standards fot mp2:")
                print(output)
                output = []
p2 = P2("bbb_trimmed.mp4")

p2.parse_video()
p2.split_video_audio_mp3("bbb_audio.mp3")
p2.split_video_audio_low_bitrate_aac("bbb_audio.m4a")
p2.join_mp4_video_acc("bbb_audio.mp3", "bbb_audio.m4a", "bbb_container.mp4")
p2.resize_video("100", "100", "bbb_resized.mp4")
p2.broadcast_audio()
