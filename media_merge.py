"""
	# GitHub :: Merge audio and video file

	*************************************************************************************************
	import ffmpeg


	input_video = ffmpeg.input("../resources/video_with_audio.mp4")
	added_audio = ffmpeg.input("../resources/dance_beat.ogg").audio.filter('adelay', "1500|1500")

	merged_audio = ffmpeg.filter([input_video.audio, added_audio], 'amix')

	(
	    ffmpeg
	    .concat(input_video, merged_audio, v=1, a=1)
	    .output("mix_delayed_audio.mp4")
	    .run(overwrite_output=True)
	)
	*************************************************************************************************
"""

import ffmpeg
import subprocess
import os

def check_and_create_path(PATH):
	if not os.path.isdir(PATH):
		os.mkdir(PATH)
		print('\n> Diretório criado: ', PATH)

def merge_v1(dir_video, dir_audio, name_file_result: str):
	input_video = ffmpeg.input(str(dir_video))
	added_audio = ffmpeg.input(str(dir_audio)).audio.filter('adelay', "1500|1500")

	merged_audio = ffmpeg.filter([input_video.audio, added_audio], 'amix')

	(
	    ffmpeg
	    .concat(input_video, merged_audio, v=1, a=1)
	    .output(f"{name_file_result}.mp4")
	    .run(overwrite_output=True)
	)

	print(">> Mescla realizada com sucesso!")


def merge_v2(name_video, name_audio, name_file_mix: str):
	check_and_create_path('Downloads/Mix')

	cmd = str(f'ffmpeg -y -i Downloads/Audio/{name_audio}  -r 30 -i Downloads/Video/{name_video}  -filter:a aresample=async=1 -c:a flac -c:v copy Downloads/Mix/{name_file_mix}.mkv')
	subprocess.call(cmd, shell=True)	# Muxing Done

	#print('>> Muxing Done')
	print(">> Mescla realizada com sucesso!")