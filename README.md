# Ableton Live Clip mixer

This module generates drum patterns from a random selection of Ableton Live Clips.
Ableton Live Clip files can be found [here](https://www.ableton.com/en/packs/#?item_type=sounds), in packs such as `Skitter and Step` etc.

While this could be done based on midi files, Ableton Live Clip drum kit setups are standardized and have some fire grooves. 
So by combining them you can get extra fire sauce ideas.

# Installation

    pip install alcmixer

or

    pip install git+https://github.com/danikavu/Ableton-Live-Clip-Mixer.git

# Creating a lookup directory

**This only needs to be done once & may take a bit.**

Create a directory of json files extracted from `.alc` files.


    from alcmixer import *
    paths = 'C:/Users/USERNAME/Documents/Ableton/Factory Packs' # Windows default path example.
    
    # Get paths of `.alc` files..
    alc_folder_path = alc_path(paths)

    # Extract an save to a directory.
    output_path = 'C:/Users/USERNAME/ALC_JSON' # Example output path.
    make_json_dir(alc_folder_path, output_path)

# Usage

Generate drum pattern midi clips from a randomized mix of Ableton Live Clips.

    from alcmixer import *
    
    # Directory of generated json files in example above.
    json_dir = 'C:/Users/USERNAME/ALC_JSON'

    # Set output path. Optional
    midi_path = 'C:/Users/USERNAME/alc_generated_midi' # Example output path. Personally I import this folder to Ableton.

    # Generate midi file.
    generate_pattern(json_dir, out_path=midi_path, fname='alcmixer_midi', bars=4, fills=True)

