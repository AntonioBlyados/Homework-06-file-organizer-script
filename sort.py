import os
import shutil
import string
import sys
from unidecode import unidecode
import re
import transliterate

IMAGE_EXTENSIONS = ('JPEG', 'PNG', 'JPG', 'SVG')
VIDEO_EXTENSIONS = ('AVI', 'MP4', 'MOV', 'MKV')
DOCUMENT_EXTENSIONS = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
MUSIC_EXTENSIONS = ('MP3', 'OGG', 'WAV', 'AMR')
ARCHIVE_EXTENSIONS = ('ZIP', 'GZ', 'TAR', 'RAR')


def normalize(filename):
    valid_chars = '-_.() %s%s' % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in filename if c in valid_chars)
    print(f'Before transliteration: {filename}')
    filename = transliterate.translit(filename, 'ru', reversed=True)
    print(f'After transliteration: {filename}')
    return filename



def process_folder(path, overwrite=False, visited=set()):
    
    if os.path.abspath(path) in visited:
        print(f'Skipping directory {path}: already visited')
        return
    visited.add(os.path.abspath(path))

    files = os.listdir(path)
    known_extensions = set()
    unknown_extensions = set()
    images = []
    videos = []
    documents = []
    music = []
    archives = []
    other = []

    for file in files:
        full_path = os.path.join(path, file)
        if os.path.isfile(full_path):
            extension = file.split('.')[-1].upper()
            if extension in (IMAGE_EXTENSIONS + VIDEO_EXTENSIONS + DOCUMENT_EXTENSIONS + MUSIC_EXTENSIONS + ARCHIVE_EXTENSIONS):
                known_extensions.add(extension)
            else:
                unknown_extensions.add(extension)

            if extension in IMAGE_EXTENSIONS:
                images.append(full_path)
            elif extension in VIDEO_EXTENSIONS:
                videos.append(full_path)
            elif extension in DOCUMENT_EXTENSIONS:
                documents.append(full_path)
            elif extension in MUSIC_EXTENSIONS:
                music.append(full_path)
            elif extension in ARCHIVE_EXTENSIONS:
                archives.append(full_path)
            else:
                other.append(full_path)
        elif os.path.isdir(full_path):
           
            if os.path.islink(full_path):
                print(f'Skipping symbolic link {full_path}')
            else:
                process_folder(full_path, overwrite=overwrite, visited=visited)

    for file_list, folder_name in [(images, 'Images'), (videos, 'Videos'), (documents, 'Documents'), (music, 'Music'), (archives, 'Archives'), (other, 'Other')]:
        folder_path = os.path.join(path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        moved_files = 0
        for file in file_list:
            file_name = os.path.basename(file)
            normalized_name = normalize(file_name)
            new_path = os.path.join(folder_path, normalized_name)
            if not os.path.exists(new_path) or overwrite:
                shutil.copy(file, new_path)
                moved_files += 1
            else:
                print(f'File {normalized_name} already exists in folder {folder_name}')
        print(f'Moved {moved_files} files to {folder_name}')
    
    return {
        'known_extensions': known_extensions,
        'unknown_extensions': unknown_extensions,
        'images': images,
        'videos': videos,
        'documents': documents,
        'music': music,
        'archives': archives,
        'other': other,
    }





if __name__ == '__main__':
    import sys
    folder_path = sys.argv[1]
    result = process_folder(folder_path)
    print('Known extensions:', result['known_extensions'])
    print('Unknown extensions:', result['unknown_extensions'])
    print('Images:', result['images'])
    print('Videos:', result['videos'])
    print('Documents:', result['documents'])
    print('Music:', result['music'])
    print('Archives:', result['archives'])
    print('Other:', result['other'])
