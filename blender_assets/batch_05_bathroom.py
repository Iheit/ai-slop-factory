import bpy,sys,os
HERE=os.path.dirname(bpy.data.filepath) if bpy.data.filepath else ''
if HERE and HERE not in sys.path:sys.path.append(HERE)
from house_asset_common import generate_batch
specs=[('Bathroom_Toilet','toilet'),('Bathroom_Bathtub','bathtub'),('Bathroom_Sink','sink'),('Bathroom_Mirror','mirror'),('Bathroom_Cabinet','cabinet'),('Bathroom_TowelRack','pipe'),('Bathroom_BathMat','rug'),('Bathroom_TrashBin','bucket'),('Bathroom_Bottle_A','bottle'),('Bathroom_Bottle_B','bottle'),('Bathroom_Bottle_C','bottle'),('Bathroom_CabinetSmall','cabinet'),('Bathroom_LaundryBasket','bucket'),('Bathroom_WallVent','vent'),('Bathroom_Light','lamp'),('Bathroom_Shelf','shelf'),('Bathroom_Drain','cylinder'),('Bathroom_Pipe','pipe'),('Bathroom_Clock','clock'),('Bathroom_Drawer','drawer')]
generate_batch('Batch_05_Bathroom',specs)
