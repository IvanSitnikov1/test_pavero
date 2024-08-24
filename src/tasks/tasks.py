import os
import urllib.request

from celery import Celery


celery = Celery(
	'tasks',
	broker='redis://redis:6379/0',
	backend='redis://redis:6379/0'
)


@celery.task
def save_file(link):
	"""Задача для скачивания и сохранения файла на сервере"""
	with urllib.request.urlopen(link) as response:
		file_name = os.path.basename(response.geturl()).split("?")[0]
		download_dir = os.path.join(os.getcwd(), 'Download')
		save_path = os.path.join(download_dir, file_name)
		with open(save_path, 'wb') as f:
			f.write(response.read())
