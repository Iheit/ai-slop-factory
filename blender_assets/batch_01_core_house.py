import bpy, sys, os
HERE=os.path.dirname(bpy.data.filepath) if bpy.data.filepath else ''
if HERE and HERE not in sys.path: sys.path.append(HERE)
from house_asset_common import generate_batch
specs=[('Core_Wall_A','wall'),('Core_Wall_B','wall'),('Core_Floor_Wood','floor'),('Core_Ceiling','ceiling'),('Core_Door','door'),('Core_Window','window'),('Core_Table','table'),('Core_Chair','chair'),('Core_Cabinet','cabinet'),('Core_Shelf','shelf'),('Core_Sofa','sofa'),('Core_Bed','bed'),('Core_Lamp','lamp'),('Core_Rug','rug'),('Core_Mirror','mirror'),('Core_Stair','stair'),('Core_Beam','wall'),('Core_Corner','wall'),('Core_DoorFrame','door'),('Core_AtticHatch','door')]
generate_batch('Batch_01_Core_House',specs)
