import bpy
import os
import sys

# Creepy House MEGA GENERATOR
# Run this single file in Blender 5.1.x.
# It runs all ten asset batches in order.


def find_script_dir():
    text = bpy.data.texts.get('generate_assets.py')
    if text and text.filepath:
        return os.path.dirname(bpy.path.abspath(text.filepath))
    if globals().get('__file__'):
        return os.path.dirname(os.path.abspath(__file__))
    blend_dir = os.path.dirname(bpy.data.filepath) if bpy.data.filepath else os.getcwd()
    candidate = os.path.join(blend_dir, 'blender_assets')
    return candidate if os.path.isdir(candidate) else blend_dir


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
    namespace = {
        '__name__': '__main__',
        '__file__': path,
        '__package__': None,
    }
    exec(compile(source, path, 'exec'), namespace, namespace)


print('=== CREEPY HOUSE MEGA GENERATOR ===')
print(f'Script directory: {SCRIPT_DIR}')
print(f'Batch count: {len(BATCHES)}')

failures = []
for number, batch in enumerate(BATCHES, 1):
    print(f'\n[{number}/{len(BATCHES)}] {batch}')
    try:
        run_batch(batch)
        print(f'[{number}/{len(BATCHES)}] COMPLETE')
    except Exception as exc:
        failures.append((batch, repr(exc)))
        print(f'[{number}/{len(BATCHES)}] ERROR: {exc}')

print('\n=== MEGA GENERATOR FINISHED ===')
if failures:
    print('The following batches failed:')
    for batch, error in failures:
        print(f' - {batch}: {error}')
else:
    print('All ten batches completed successfully.')
print('Output folder:', os.path.join(SCRIPT_DIR, 'generated_assets'))
