""" Create midi file from a combined pattern of `.alc` files """
import os
import json
import random
import note_seq
from note_seq.protobuf import music_pb2
# Randomness
SYS_RAND = random.SystemRandom()


def generate_pattern(json_dirs, out_path=None, fname='python_als_gen_def_test', bars=1, fills=False):
    """
        Generates a midi pattern from 16 random kits.
        Additional option to add fills at the end of every 2 bars.
    :param json_dirs: Path of generated json files.
    :param out_path: Path for output midi files.
    :param fname: Midi filename.
    :param bars: Number of bars in sequence.
    :param fills: If True generate drum fills.
    :return: Exports `.mid` file.
    """
    # List of `.alc` files.
    jsons = os.listdir(json_dirs)
    # Chose 16 random kits.
    random_kits = [SYS_RAND.choice(jsons) for x in range(16)]
    # Blank midi file.
    midi_outp = music_pb2.NoteSequence()
    # Fill to be added every 2 bars if bars not 1.
    fill_kits = int(bars / 2)
    # If fills selected create fill midi sequence from kits.
    if fills and bars > 1:
        bar = 1
        for fill in range(fill_kits):
            fkits = [SYS_RAND.choice(jsons) for x in range(16)]
            for n, rando in enumerate(fkits, start=36):
                with open(f'{json_dirs}{os.sep}{rando}', 'r', encoding="utf8") as f:
                    array = json.load(f)
                _notes = array['{}'.format(n)]
                if _notes:
                    for _m_note in _notes:
                        if 6 < float(_m_note[0]) < 7.95:
                            midi_outp.notes.add(pitch=n,
                                                start_time=(float(_m_note[0]) / 2) + (bar * 4),
                                                end_time=((float(_m_note[0]) + float(_m_note[1])) / 2) + (bar * 4),
                                                velocity=int(float(_m_note[2])))
            bar += 2
    # Create midi sequence from kits.
    for n, rando in enumerate(random_kits, start=36):
        with open(f'{json_dirs}{os.sep}{rando}', 'r', encoding="utf8") as f:
            array = json.load(f)
        _notes = array['{}'.format(n)]
        if _notes:
            for _m_note in _notes:
                bar = 0
                for _bar in range(bars):
                    for _m_note in _notes:
                        if fills and bar % 2 != 0:
                            if float(_m_note[0]) < 5.95:
                                midi_outp.notes.add(pitch=n,
                                                    start_time=(float(_m_note[0]) / 2) + (bar * 4),
                                                    end_time=((float(_m_note[0]) + float(_m_note[1])) / 2) + (bar * 4),
                                                    velocity=int(float(_m_note[2])))
                        else:
                            if float(_m_note[0]) < 7.95:
                                midi_outp.notes.add(pitch=n,
                                                    start_time=(float(_m_note[0]) / 2) + (bar * 4),
                                                    end_time=((float(_m_note[0]) + float(_m_note[1])) / 2) + (bar * 4),
                                                    velocity=int(float(_m_note[2])))
                    bar += 1
    # Export path.
    exp_path = out_path + os.sep + fname + '.mid' if out_path else fname + '.mid'
    # Export midi file.
    note_seq.sequence_proto_to_midi_file(midi_outp, exp_path)
