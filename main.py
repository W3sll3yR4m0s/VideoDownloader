#from tqdm import tqdm
#from time import sleep
#import sys

from pytube import YouTube, Playlist

import media_merge as mix

import subprocess
import os


class VideoDownloader:
	__version__ = "0.7"

	def __init__(self):
		self.url = ''
		self.url_playlist = ''

		self.youtube = None
		self.playlist = None

		self.current_video = None

		self.current_video_title = ''
		self.current_video_id = ''
		self.current_video_age = ''

		self.set_res_manually = ''
		self.selected_stream = ''

		self.again = ''
		self.path = ''

	def initial_data(self, url_link):
		try:
			self.url  = str(url_link)

			# Load URL in Function Youtube:
			self.youtube = YouTube(self.url)
		except Exception as ex:
			print(" >> FALHA :: ", ex)

	def set_with_or_without_selected_stream(self):
		try:
			# Set with or without selected_stream:
			self.set_res_manually = (input("\n> [s/n] Selecionar Stream? ")).lower()
			if self.set_res_manually == 's':
				check_list_of_streams = (input("> [s/n/d] Buscar Lista de Streams ou Ver Lista Padrão? ")).lower()
				if check_list_of_streams == 's':
					# List Streams Resolution:
					resolutions = self.youtube.streams.all()
					print('\n')
					print("*"*80)
					count = 0
					for res in resolutions:
						print(f'[{count}] > {res}')
						count += 1
					print("*"*80)

					# Select resolution:
					print("\n[ Conforme a lista anterior ]")
				elif check_list_of_streams == 'd':
					self.get_default_list_itag()
				self.selected_stream = input("TAG da Stream: ")
				#video_format = input("Digite o formato de vídeo que você quer: ")
			elif self.set_res_manually == 'n':
				# Set Streams Resolution:
				#video = youtube.streams.first() # or
				self.current_video = self.youtube.streams.get_highest_resolution()
				#print("\n > Mais alta resolução encontrada: ", self.current_video)
		except Exception as ex:
			print(" >> FALHA :: ", ex)

	def results_log(self, download_complete):
		try:
			if download_complete:
				print("\nDownload concluído com sucesso!")

				# Get Information of Video:
				self.current_video_title = self.youtube.title
				self.current_video_id = self.youtube.video_id
				self.current_video_age = self.youtube.age_restricted

				print("\n")
				print("*"*80)
				print("""Download finalizado!
					  \nInformações do vídeo baixado: 
					  \nID: {}, \nTítulo: {}, \nIdade: {}
					  """.format(self.current_video_id, 
					  			 self.current_video_title, 
					  			 self.current_video_age))
				print("*"*80)
			else:
				print("\n")
				print("*"*80)
				print("""Não foi possível realizar o download!
					  """)
				print("*"*80)
		except Exception as ex:
			print(" >> FALHA :: ", ex)

	def download_again(self):
		try:
			self.again = (input("> [s/n] Baixar algo mais? ")).lower()
			if self.again == 's':
				self.main(self.url)
			else:
				print(">> YouTube Downloader encerrado!")
		except Exception as ex:
			print(" >> FALHA :: ", ex)

	def download(self, path):
		try:
			print("\nDownload iniciado. Aguarde!!!")
			if self.set_res_manually == "n":
				if isinstance(path, str):
					if len(path) > 0:
						self.current_video.download('Downloads'+'/'+str(path)) # In other folder
						return True
				elif path == 0:
					self.current_video.download('Downloads') # In other folder
					return True
			elif self.set_res_manually == "s":
				video = self.youtube.streams.get_by_itag(int(self.selected_stream))
				#video = self.youtube.streams.get_by_resolution(resolution=str(selected_stream))
				if isinstance(path, str):
					if len(path) > 0:
						video.download('Downloads'+'/'+str(path)) # In other folder
						return True
				elif path == 0:
					video.download('Downloads') # In other folder
					return True
			else:
				return False
		except Exception as ex:
			print(" >> FALHA :: ", ex)
			return False

	def view_current_dir(self):
		try:
			print("\n> Diretório atual: ")
			
			cmd0 = str(f'pwd')
			current_dir = subprocess.call(cmd0, shell=True)

			#cmd1 = str(f'cd current_dir')
			#subprocess.call(cmd1, shell=True)
		except Exception as ex:
			print(" >> FALHA :: ", ex)

	def get_default_list_itag(self):
		try:
			if os.path.exists('default_list_itag.txt'):
				cmd = str(f'cat default_list_itag.txt')
				subprocess.call(cmd, shell=True)
			else:
				print("\n> AVISO: O diretório atual não contém o arquivo default_list_itag.txt\n")
		except:
			pass

	def main(self, url_link):
		try:
			download_complete = False

			if self.again != 's':
				self.initial_data(url_link)

			# Download Video:
			#video.download() # In same folder # or
			
			path = input("\n> Pasta: ")
			if path.upper() == 'V':
				path = 'Video'
			elif path.upper() == 'A':
				path = 'Audio'

			self.path = self.path if self.path == '=' else path

			self.set_with_or_without_selected_stream()

			self.view_current_dir()

			download_complete = self.download(self.path)

			self.results_log(download_complete)
			self.download_again()

		except Exception as ex:
			print(" >> FALHA :: ", ex)
			self.download_again()

	def download_playlist(self, url_link):
		try:
			self.url_playlist  = str(url_link)

			self.playlist = Playlist(self.url_playlist)

			playlist_name = input("\n> Digite um nome para a pasta dessa PLaylist: ")

			print("\n> Os vídeos a seguir serão baixados: ")
			for video in self.playlist:
				print(video)

			for video in self.playlist.video_urls:
				try:
					# Download video in Playlist:
					self.youtube = YouTube(video)
				except VideoUnavailable:
					print(f'\nO vídeo {video} não está disponível, saltando!\n')
				else:
					print(f'Baixando o vídeo: {video}')
					#self.youtube.streams.get_highest_resolution().download('Downloads'+'/'+str(playlist_name))
					self.youtube.streams.get_highest_resolution().download('Downloads'+'/'+str(playlist_name))

			print("\n")
			print("*"*80)
			print("""Download da playlist finalizado!
				  """)
			print("*"*80)
		except Exception as ex:
			print(" >> FALHA :: ", ex)

	def stream_video(self):
		try:
			# Streams Format:
			self.current_video.streams.all()
			stream = self.current_video.streams.all()
			for i in stream:
				print(i)
		except Exception as ex:
			print(" >> FALHA :: ", ex)


class MergeFiles:
	__version__ = "0.1"

	def __init__(self):
		pass

	def start_merge(self):
		try:
			print("*"*80)
			dir_video = input("> Nome com extensão do arquivo Vídeo: ")
			dir_audio = input("> Nome com extensão do arquivo Áudio: ")
			result_name = input("> Nome para o vídeo final: ")

			mix.merge_v2(dir_video, dir_audio, result_name)
			print("*"*80)
		except Exception as ex:
			print(" >> FALHA :: ", ex)


if __name__ == "__main__":
	what_to_do = int(input("0 : Download \n1 : Merge \n> "))

	if what_to_do == 0:
		videoDownloader = VideoDownloader()
		url = input("> URL: ")
		is_playlist = (input("> [s/n] Playlist? ")).lower()
		#videoDownloader.download(sys.argv)
		if ( is_playlist == "sim" or 
			 is_playlist == "s" or 
			 is_playlist == "yes" or 
			 is_playlist == "y" ):
			videoDownloader.download_playlist(url)
		else:
			videoDownloader.main(url)
	elif what_to_do == 1:
		mergeFiles = MergeFiles()
		mergeFiles.start_merge()