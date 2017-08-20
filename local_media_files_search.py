#! /usr/bin/python

"""
Script to find multimedia files in passed directory and all its subdirectories
"""


import os
import csv
import argparse
from time import strftime, gmtime


class LocalMediaFiles(object):

    AUDIO_FORMATS = ('.mp3', '.wma')
    VIDEO_FORMATS = ('.avi', '.mpeg', '.mpg', '.mp4' '.mkv')
    RES_FILE = 'media_files'
    DATE_FORMAT = "%d %b %Y %H:%M:%S"

    def __init__(self):
        # TODO: add ability to add another extensions to the list of already existing
        self.arg_parser = argparse.ArgumentParser()
        self.arg_parser.add_argument('root_dir', help='Root directory to start searching for the media files')
        self.arg_parser.add_argument('-a', '--audio_files', default=False, action='store_true',
                                     help='Search for audio files in root directory and subdirectories')
        self.arg_parser.add_argument('-v', '--video_files', default=False, action='store_true',
                                     help='Search for video files in root directory and subdirectories')
        self.arg_parser.add_argument('-c', '--save_as_csv', default=False, action='store_true',
                                     help='Extension of result file. If false file is txt else file extension is csv.')
        self.audio_files = {}
        self.video_files = {}

        self.args = self.arg_parser.parse_args()

    def get_audio_files(self):
        self.__get_files('audio')

    def get_video_files(self):
        self.__get_files('video')

    def __get_files(self, file_type):
        error_msg = "Option to collect {} files does not selected.".format(file_type.capitalize())
        if ((file_type.lower() == 'audio' and self.args.audio_files) or
                (file_type.lower() == 'video' and self.args.video_files)):
            file_format = self.AUDIO_FORMATS if file_type.lower() == 'audio' else self.VIDEO_FORMATS
            self.__write_to_file(self.__get_files_by_extension(self.args.root_dir, file_format), file_type)
        else:
            print(error_msg)

    def __write_to_file(self, file_dict, file_type):
        num = 1
        file_type = file_type.capitalize()
        file_name = '{}.csv'.format(self.RES_FILE) if self.args.save_as_csv else '{}.txt'.format(self.RES_FILE)
        with open(file_name, mode='wt') as fd:
            if self.args.save_as_csv:
                headers = ['File extension', 'Full file name', 'Created Date']

                csv_f = csv.DictWriter(fd, headers)
                csv_f.writeheader()
                csv_f.writerows([{headers[0]: file_type, headers[1]: file,
                                  headers[2]: strftime(self.DATE_FORMAT, gmtime(created_time))}
                                 for file, created_time in file_dict.items()])
            else:
                for file, created_time in file_dict.items():
                    fd.write("|{} file |{:<140}| created date {:>10}|\n".format(file_type, file,
                                                                                strftime(self.DATE_FORMAT,
                                                                                         gmtime(created_time))))

    @staticmethod
    def __get_files_by_extension(directory, file_formats):
        output_dict = {}
        for dir_name, *_, files in os.walk(directory):
            if files:
                for file in files:
                    if file.endswith(file_formats):
                        output_dict[os.path.join(dir_name, file)] = os.path.getatime(os.path.join(dir_name, file))

        return output_dict

if __name__ == '__main__':
    media_files = LocalMediaFiles()
    media_files.get_audio_files()
    media_files.get_video_files()
