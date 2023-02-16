# Stash Docs
# Copyright (c) 2023 Arctic Technology

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import shlex; import subprocess
from os.path import isfile, isdir, exists
from typing import Type, Union
from random import randrange
from datetime import datetime, timedelta
from .utils.crawler import Crawler
from .utils.commoncmd import CommonCmd as cmd

class Stash:

	def random_time(self) -> str:
		end = datetime.now()
		start = datetime.strptime('1/1/2005 12:00 AM', '%m/%d/%Y %I:%M %p')
		delta = end - start
		int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
		random_second = randrange(int_delta)
		return str(start + timedelta(seconds=random_second))

	def timetravel(self, path: str) -> dict:
		ppath = Crawler.escape(Crawler.posixize(path))
		command = shlex.split('touch -d "{t}" {p}'.format(t=self.random_time(),p=ppath))
		process = subprocess.run(command,
					stdout=subprocess.PIPE,stderr=subprocess.PIPE)

		returncode = process.returncode

		if returncode == 0:
			return {'status': 200, 'message': 'Timetravelled: ' + str(path)}
		else:
			return {'status': 400, 'message': 'Error timetravelling: ' + str(path)}

	def timetravel_files(self, path: str,
						extension: Union[str, Type[None]] = None) -> dict:
		files = Crawler.get_files(path, extension=extension)

		if len(files) <= 0:
			return {'status': 400, 'message': 'Error timetravelling: no files found.', 'output': []}

		output = [self.timetravel(f)['message'] for f in files]
		return {'status': 200, 'message': 'Timetravel files complete.', 'output': output}

	def timetravel_folders(self, path: str) -> dict:
		folders = Crawler.get_folders(path)

		if exists(path) != True:
			return {'status': 400, 'message': 'Error timetravelling: no directory found.', 'output': []}

		if len(folders) <= 0:
			output = ['No folders found to timetravel, no action taken.']
		else:
			output = [self.timetravel(folder)['message'] for folder in folders]

		output.append(self.timetravel(path)['message'])

		return {'status': 200, 'message': 'Timetravel folders complete.', 'output': output}

	def invalid_stash_data(self, data: dict) -> bool:
		no_origin_dir = 'origin_dir' not in data
		no_stash_dir = 'stash_dir' not in data
		no_stash_key = 'stash_key' not in data
		if no_origin_dir or no_stash_dir or no_stash_key:
			return True
		if type(data['origin_dir']) != str or type(data['stash_dir']) != str:
			return True
		if type(data['stash_key']) != dict:
			return True
		stash_key = data['stash_key']
		keys = list(stash_key.keys())
		values = list(stash_key.values())
		if len(keys) == 0 or len(values) == 0: return True
		if len(keys) != len(values): return True
		return False

	def stash(self, curr_filename: str, curr_dir: str, new_filename: str,
			new_dir: str,overwrite: bool = False, remove: bool = False,
			retrieve: bool = False) -> dict:
		curr_filepath = Crawler.joinpath(curr_dir, curr_filename)
		result = {'status': None, 'message': None}

		if exists(curr_filepath) != True:
			result['status'] = 400
			if retrieve == True:
				result['message'] = 'Error: Retrieval failed, specified file not found in stashed directory.'
			else:
				result['message'] = 'Error: File not found {}'.format(str(curr_filepath))
			return result

		if isfile(curr_filepath) != True: 
			result['status'] = 400
			if retrieve == True:
				result['message'] = 'Error: Retrieval failed, specified file in stashed directory is corrupt.'
			else:
				result['message'] = 'Error: File is corrupt {}'.format(str(curr_filepath))
			return result

		new_filepath = Crawler.joinpath(new_dir, new_filename)
		if exists(new_filepath) == True and overwrite == False:
			result['status'] = 400
			if retrieve == True:
				result['message'] = 'Error: File already exists {}'.format(str(new_filepath))
			else:
				result['message'] = 'Error: Stash failed, file already exists in stashed directory.'
			return result

		response = cmd.copyfile(curr_filepath, new_filepath)
		if response['status'] != 200: return response
		self.timetravel(new_filepath)
		if remove == True: 
			try:
				remove(curr_filepath)
			except:
				if retrieve == True:
					result['message'] = 'Error: Failed to remove file from stashed directory'
				else:
					result['message'] = 'Error: Failed to remove {}'.format(str(curr_filepath))
		return response

	def stash_all(self, data: dict, retrieve: bool = False) -> dict:
		"""
		Data format:
		{"origin_dir": "/home/origin_directory/",
		"stash_dir": "/home/stash_directory/",
		"stash_key": {
		"filename1": "stashed_filename1",
		"filename2": "stashed_filename2",
		"filename3": "stashed_filename3"}}
		"""
		result = {'status': None, 'message': None, 'output': []}
		origin_dir = Crawler.posixize(data['origin_dir'])
		stash_dir = Crawler.posixize(data['stash_dir'])

		if isdir(origin_dir) == False: return {'status': 400,
				'message': 'Error: Could not find origin directory {}'.format(str(origin_dir)), 'output': []}

		if isdir(stash_dir) == False: return {'status': 400,
				'message': 'Error: Could not find stash directory. Directory invalid or missing.', 'output': []}

		stash_key = data['stash_key']
		keys = list(stash_key.keys())
		values = list(stash_key.values())
		statuscodes = []

		for i in range(len(keys)):
			if keys[i] == '' or values[i] == '': return {'status': 400,
				'message': 'Error: Invalid config file, keys and values cannot be blank.',
				'output': []}

		for i in range(len(keys)):
			if retrieve == True:
				response = self.stash(values[i],stash_dir,keys[i],origin_dir,
										overwrite=False,remove=False,retrieve=retrieve)
			else:
				response = self.stash(keys[i],origin_dir,values[i],stash_dir,
										overwrite=True,remove=True,retrieve=retrieve)
			statuscodes.append(response['status'])
			result['output'].append(response['message'])

		if retrieve == True:
			keyword = 'Retrieve'
			if len(statuscodes) > 1 and 200 not in statuscodes:
				result['status'] = 400
				result['message'] = 'Error: No stashed files retrieved. Specified files did not exist.'
				return result
		else:
			keyword = 'Stash'
			if len(statuscodes) > 1 and 200 not in statuscodes:
				result['status'] = 400
				result['message'] = 'Error: No files to stash found in {}'.format(str(origin_dir))
				return result
			timetravel = self.timetravel(stash_dir)
			if timetravel['status'] == 200:
				result['output'].append('Timetravel completed for stash directory.')
			else:
				result['output'].append('Error timetravelling stash directory.')

		result['status'] = 200
		result['message'] = '{} completed.'.format(str(keyword))
		return result