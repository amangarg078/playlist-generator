from __future__ import unicode_literals

import argparse
import os
import re
import sys

def get_sort_key(s):
    """
    Return key for alpha numeric sorting
    """
    match = re.findall(r"^(\d+)", s)
    if match:
        return int(match[0])
    else:
        return s

class PlaylistCreator(object):
    def __init__(self, directory):
        self.directory = directory

    def create_playlist(self, playlist_path, files):
        with open(playlist_path, 'w+') as p:
            for f in files:
                print >> p, f

    def run(self):
        for (root, dirs, filenames) in os.walk(self.directory, topdown=False):
            media_files = []
            for _file in filenames:
                extension = os.path.splitext(_file)[1]
                if extension in ['.mp4', '.mp3', '.mkv', '.aac']:
                    media_files.append(_file.encode("utf-8"))

            # no file to add to playlist
            if not media_files:
                continue
            playlist_filename = os.path.split(root)[-1]
            playlist_path = os.path.join(root, "Playlist - " + playlist_filename + ".m3u")
            media_files = sorted(media_files, key=get_sort_key)
            self.create_playlist(playlist_path, media_files)

if __name__ == '__main__':
    # take the target root directory as argument
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="Select the root directory",
                    type=lambda s: unicode(s, 'utf8'), nargs='?', default=os.getcwd())
    args = parser.parse_args()
    directory = args.directory

    # if provided directory is not a directory, stop execution
    if not os.path.isdir(directory):
        print "Please enter a valid directory or place the file in the root directory and don't provide any arguments to run the script."
        sys.exit()
    playlist_creator = PlaylistCreator(directory)
    playlist_creator.run()
