import bpy,sys,os
HERE=os.path.dirname(bpy.data.filepath) if bpy.data.filepath else ''
if HERE and HERE not in sys.path: sys.path.append(HERE)
from house_asset_common import generate_batch
specs=[('Kitchen_Counter','cabinet'),('Kitchen_UpperCabinet','cabinet'),('Kitchen_Sink','sink'),('Kitchen_Faucet','pipe'),('Kitchen_Fridge','fridge'),('Kitchen_Stove','stove'),('Kitchen_Oven','stove'),('Kitchen_DiningTable','table'),('Kitchen_DiningChair_A','chair'),('Kitchen_DiningChair_B','chair'),('Kitchen_PantryShelf','shelf'),('Kitchen_TrashBin','bucket'),('Kitchen_Crate','crate'),('Kitchen_Cabinet','cabinet'),('Kitchen_WallClock','clock'),('Kitchen_Lamp','lamp'),('Kitchen_Pot','bucket'),('Kitchen_Pan','cylinder'),('Kitchen_CuttingBoard','note'),('Kitchen_Vase','lamp')]
generate_batch('Batch_03_Kitchen',specs)
