from sys import argv
from pathlib import Path
from shutil import move
import os

sort_logic_dict = {
    **dict.fromkeys(['kick', 'kik'], "kick"),
    **dict.fromkeys(['snare', 'snr', 'clap', 'rim'], "snare"),
    **dict.fromkeys(['snap'], "snap"),
    **dict.fromkeys(['tom'], 'tom'),
    **dict.fromkeys(['open', 'ride'], 'open_hat'),
    **dict.fromkeys(['closed', 'hat'], 'closed_hat'),
    **dict.fromkeys(['crash', 'cymbal'], 'cymbal'),
    **dict.fromkeys(['shaker', 'shake'], 'shaker')
}
extensions = {"mp3", "wav"}
sample_path = "/Users/jacksonkurtz/ableton/samples/"

def move_file(path_to_file, dest):
    dest_dir = Path(sample_path + dest)
    if not dest_dir.exists():
        dest_dir.mkdir()
    if os.path.isfile(str(dest_dir) + "/" + Path(path_to_file).name):
        return False
    move(str(path_to_file), str(dest_dir.absolute()))
    return True

def sort_files(path_arg):
    num_files_moved = 0
    num_files_ignored = 0
    num_files_skipped = 0
    for filename in path_arg.rglob("*"): # iterate recursively through all files
        path_to_file = filename.absolute()

        if path_to_file.is_file() and filename.suffix[1:] in extensions:
            found_matching_dir = False
            moved = False
            for substr, dir in sort_logic_dict.items():
                if substr in str.lower(Path(path_to_file).stem):
                    moved = move_file(path_to_file, dir) 
                    found_matching_dir = True
                    break
            # file does not match anything in logic dict
            if not found_matching_dir:
                moved = move_file(path_to_file, "misc") 

            if moved:
                num_files_moved += 1
            else:
                num_files_skipped += 1
        else: 
            num_files_ignored += 1

    print("Ignored {0} files because wrong extension".format(num_files_ignored))
    print("Skipped {0} files because already exist".format(num_files_skipped))
    print("Moved {0} files".format(num_files_moved))
            
if len(argv) != 2:
    print("=" * 35)
    print("[ERROR] Invalid number of arguments were given")
    print(f"[Usage] python {Path(__file__).name} <dir_path>")
    print("=" * 35)
    exit(1)
path_arg = Path(argv[1])
sort_files(path_arg)