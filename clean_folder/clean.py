import glob
import os
import shutil
import re
import sys

main_path = sys.argv[1]

extensions = {

    'video': ['mp4', 'mov', 'avi', 'mkv'],

    'audio': ['mp3', 'wav', 'ogg', "amr"],

    'image': ['jpg', 'png', 'jpeg', 'svg'],

    'archive': ['zip', 'gz', 'tar'],

    'documents': ['pdf', 'txt', 'doc', 'docx', 'xlsx', 'pptx'],

    "other": []
}


def normalize(path):
    path_list = path.split('\\')

    name = path_list[-1]

    CYRILLIC_SYMBOLS = ("а", 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п',
                        'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'є', 'і', 'ї', 'ґ')
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "y", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    translated_name = name.translate(TRANS)

    if os.path.isfile(path):
        file_list = translated_name.split(".")
        i = file_list.pop(-1)
        file_name = ".".join(file_list)
        new_name = re.sub(r"\W", "_", file_name)
        res = new_name + "." + i

    else:
        res = re.sub(r"\W", "_", translated_name)

    path_list[-1] = res
    new_path = "//".join(path_list)
    return (new_path)


def create_folders_from_list(folder_path, folder_names):
    for folder in folder_names:
        if not os.path.exists(f'{folder_path}\\{folder}'):
            os.mkdir(f'{folder_path}\\{folder}')


def get_subfolder_paths(folder_path) -> list:
    subfolder_paths = [f.path for f in os.scandir(folder_path) if f.is_dir()]

    return subfolder_paths


scripts = []


def recrusion(path):
    for pat in glob.iglob(f'{path}/**/*', recursive=True):
        if os.path.isfile(pat):
            file_path, file_name = os.path.split(pat)
            split_filename = file_name.split(".")
            scripts.append(split_filename[1])
            for key, value in extensions.items():
                if split_filename[1] in value:
                    new_path = os.path.join(path, key)
                    if not os.path.exists(os.path.join(path, key, file_name)):
                        shutil.move(pat, new_path)


def remove_empty_folders(folder_path):
    subfolder_paths = get_subfolder_paths(folder_path)

    for p in subfolder_paths:
        if not os.listdir(p):
            os.rmdir(p)


def unarchive(path):
    arh_list = os.listdir(os.path.join(path, "archive"))
    for arh in arh_list:
        a = str(arh.removesuffix(".zip"))
        shutil.unpack_archive(os.path.join(
            path, "archive", arh), os.path.join(path, a))


def printing(main_path, extensions):
    known = ["known_ends:"]
    unknown = ["unknown_values:"]
    result = {}
    all_folders = os.listdir(main_path)
    for pice in all_folders:
        fils = os.listdir(os.path.join(main_path, pice))
        result.update({pice: fils})
        for f in fils:
            ends = f.split('.')
            for val in extensions.values():
                if ends[-1] in val and ends[-1] not in known:
                    known.append(ends[-1])
            if ends[-1] not in known and ends[-1] not in unknown:
                unknown.append(ends[-1])
    print(result)
    print(known, unknown)


def start():
    for pat in glob.iglob(f'{main_path}/**/*', recursive=True):
        os.rename(pat, normalize(pat))
    create_folders_from_list(main_path, extensions)
    recrusion(main_path)
    remove_empty_folders(main_path)
    if os.path.exists(os.path.join(main_path, "archive")):
        unarchive(main_path)
    printing(main_path, extensions)


if __name__ == "__main__":
    start()
