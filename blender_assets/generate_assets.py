import bpy
import os
import sys

# One-click runner for the complete Creepy House asset library.
# Run this file from Blender 5.1's Text Editor. It executes all ten batches.


def find_script_dir():
    # When run from Blender's Text Editor, the text block retains its filepath.
    text = bpy.data.texts.get('generate_assets.py')
    if text and text.filepath:
        return os.path.dirname(bpy.path.abspath(text.filepath))

    # Useful when this file is executed with Python/Blender from disk.
    if '__file__' in globals() and globals()['__file__']:
        return os.path.dirname(os.path.abspath(globals()['__file__']))

    blend_dir = os.path.dirname(bpy.data.filepath) if bpy.data.filepath else os.getcwd()
    candidate = os.path.join(blend_dir, 'blender_assets')
    if os.path.isdir(candidate):
        return candidate
    return blend_dir


SCRIPT_DIR = os.path.abspath(find_script_dir())
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

BATCHES = [
    'batch_01_core_house.py',
    'batch_02_living_common.py',
    'batch_03_kitchen.py',
    'batch_04_bedrooms.py',
    'batch_05_bathroom.py',
    'batch_06_basement_utility.py',
    'batch_07_attic.py',
    'batch_08_generic_props.py',
    'batch_09_puzzle_gameplay.py',
    'batch_10_story_rooms.py',
]


def run_batch(filename):
    path = os.path.join(SCRIPT_DIR, filename)
    if not os.path.isfile(path):
        raise FileNotFoundError(f'Missing batch script: {path}')
    print(f'=== Running {filename} ===')
    with open(path, 'r', encoding='utf-8') as handle:
        source = handle.read()
    code = compile(source, path, 'exec')
    namespace = {
        '__name__': '__main__',
        '__file__': path,
        '__package__': None,
    }
    exec(code, namespace, namespace)


print('=== Creepy House Asset Generator ===')
print(f'Script directory: {SCRIPT_DIR}')
print(f'Output directory: {os.path.join(SCRIPT_DIR, "generated_assets")}')

for batch in BATCHES:
    run_batch(batch)

print('=== COMPLETE ===')
print('All assets were exported as isolated .blend files.')
