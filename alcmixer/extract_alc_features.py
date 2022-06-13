""" Ableton `.alc` files to json """
import os
import json
import gzip
from bs4 import BeautifulSoup


def make_json_dir(directory, out_path):
    """
        Creates a directory of json files extracted from `.alc` files.
    :param directory: Path of `.alc` files to be converted.
    :param out_path: Json output path.
    :return:
    """
    for alc_file in directory:
        try:
            extract_alc_features(alc_file, out_path)
        except Exception as e:
            print(f'Failed for {alc_file}\nWith Exception : {e}')


def alc_folder_path(folder, kit=True):
    """
        Returns a list of all `.alc` filepaths from a given directory.
    :param kit: If True will only return paths that contain `KIT` in filename. (Drumkits)
    :param folder: Path of `.alc` files folder
    :return: List of full `.alc` filepaths
    """

    dirs = [x[0] for x in os.walk(folder)]
    dirs = [x for x in dirs if 'MIDI Clips\\' in x]
    alc_paths = []
    for _dir in dirs:
        for alc in os.listdir(_dir):
            if '.alc' in alc and '.ogg' not in alc:
                alc_paths.append(_dir + '\\' + alc)
    if kit:
        alc_paths = [alc for alc in alc_paths if 'KIT' in alc.upper().split('\\')[-1]]

    return alc_paths


def extract_alc_features(alc_file, out_path, drumkit=True):
    """
        Extracts midi features from a `.alc` file and creates a json output file.
    :param alc_file: Path of Ableton alc file. Example -> C:/Users/USERNAME/Documents/Ableton/Factory Packs'
    :param out_path: Path of exported json file.
    :param drumkit: If False full range of midi notes will be processed.
    :return:
    """

    if drumkit:
        key_notes_midi = [str(x) for x in range(36, 52)]
    else:
        key_notes_midi = [str(x) for x in range(128)]
    # Filename.
    fname = alc_file.split('\\')[-1].split('.')[0]
    # Open file with gzip, parse with bs4.
    with gzip.open(alc_file, 'rb') as f:
        file_content = f.read()
        file_content = file_content.decode("utf-8")
        file_content = BeautifulSoup(file_content, 'lxml')
    # Get the midi notes.
    notes = file_content.ableton.liveset.tracks.miditrack.devicechain.mainsequencer.clipslotlist.clipslot.clipslot.value.midiclip.notes
    # Create data pairs for note, time, duration, & velocity.
    preset_pairs = []
    for midi in notes.findAll('keytrack'):
        if drumkit:
            if 36 <= int(midi.midikey['value']) < 52:
                _midi = midi.findAll('midinoteevent')
                midi_group = []
                for _notes in _midi:
                    midi_group.append([_notes['time'], _notes['duration'], _notes['velocity']])
                midi_key = midi.midikey['value']
                preset_pairs.append([midi_key, midi_group])
                key_notes_midi.remove(midi_key)
        else:
            _midi = midi.findAll('midinoteevent')
            midi_group = []
            for _notes in _midi:
                midi_group.append([_notes['time'], _notes['duration'], _notes['velocity']])
            midi_key = midi.midikey['value']
            preset_pairs.append([midi_key, midi_group])
            key_notes_midi.remove(midi_key)
    # Create preset pairs.
    for _m in key_notes_midi:
        preset_pairs.append([_m, []])
    # Create a dictionary for the preset.
    _dict = {}
    for items in preset_pairs:
        _dict[items[0]] = items[1]
    _dict = dict(sorted(_dict.items()))
    # Export json file.
    with open(f'{out_path}{os.sep}{fname}', 'w', encoding='utf-8') as f:
        json.dump(_dict, f, ensure_ascii=False, indent=4)
