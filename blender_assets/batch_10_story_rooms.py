import bpy,sys,os
HERE=os.path.dirname(bpy.data.filepath) if bpy.data.filepath else ''
if HERE and HERE not in sys.path:sys.path.append(HERE)
from house_asset_common import generate_batch
specs=[('Study_Typewriter','typewriter'),('Study_Desk','table'),('Study_LockedDrawer','drawer'),('Study_Bookshelf','shelf'),('Study_OldPhotograph','photograph'),('Child_Toy','toy'),('Child_ToyChest','cabinet'),('Child_Bed','bed'),('Child_Drawing','note'),('Child_Clock','clock'),('Dining_Table','table'),('Dining_Chair_A','chair'),('Dining_Chair_B','chair'),('Dining_Cabinet','cabinet'),('Dining_Painting','painting'),('Master_Vanity','table'),('Master_Mirror','mirror'),('Master_Trunk','trunk'),('Mystery_PuzzleBox','puzzle_box'),('Mystery_RitualTable','ritual_table')]
generate_batch('Batch_10_Story_Rooms',specs)
