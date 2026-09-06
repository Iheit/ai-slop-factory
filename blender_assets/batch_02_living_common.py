import bpy,sys,os
HERE=os.path.dirname(bpy.data.filepath) if bpy.data.filepath else ''
if HERE and HERE not in sys.path: sys.path.append(HERE)
from house_asset_common import generate_batch
specs=[('Living_Sofa','sofa'),('Living_Armchair','chair'),('Living_CoffeeTable','table'),('Living_Bookshelf','shelf'),('Living_SideTable','table'),('Living_FloorLamp','lamp'),('Living_TVStand','cabinet'),('Living_Cabinet','cabinet'),('Living_Rug','rug'),('Living_Mirror','mirror'),('Living_WallClock','clock'),('Living_Painting','painting'),('Living_Telephone','phone'),('Living_CurtainRod','pipe'),('Living_Vase','lamp'),('Living_EntryTable','table'),('Living_StorageShelf','shelf'),('Living_ExtraChair','chair'),('Living_SmallRug','rug_round'),('Living_PictureFrame','photograph')]
generate_batch('Batch_02_Living_Common',specs)
