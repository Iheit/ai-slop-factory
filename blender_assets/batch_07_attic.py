import bpy,sys,os
HERE=os.path.dirname(bpy.data.filepath) if bpy.data.filepath else ''
if HERE and HERE not in sys.path:sys.path.append(HERE)
from house_asset_common import generate_batch
specs=[('Attic_Trunk','trunk'),('Attic_Suitcase_A','suitcase'),('Attic_Suitcase_B','suitcase'),('Attic_Crate_A','crate'),('Attic_Crate_B','crate'),('Attic_StorageShelf','shelf'),('Attic_OldChair','chair'),('Attic_OldDesk','table'),('Attic_Mattress','bed'),('Attic_Lamp','lamp'),('Attic_Mirror','mirror'),('Attic_OldPainting','painting'),('Attic_NewspaperPile','book'),('Attic_BookPile','book'),('Attic_ToyChest','cabinet'),('Attic_Ladder','stairs'),('Attic_HangingBulb','hanging_bulb'),('Attic_Pipe','pipe'),('Attic_Box_A','box'),('Attic_Box_B','box')]
generate_batch('Batch_07_Attic',specs)
