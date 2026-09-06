import bpy,sys,os
HERE=os.path.dirname(bpy.data.filepath) if bpy.data.filepath else ''
if HERE and HERE not in sys.path:sys.path.append(HERE)
from house_asset_common import generate_batch
specs=[('Prop_Bottle_A','bottle'),('Prop_Bottle_B','bottle'),('Prop_Book_A','book'),('Prop_Book_B','book'),('Prop_Note','note'),('Prop_Photograph','photograph'),('Prop_Vase','vase'),('Prop_Mug','cylinder'),('Prop_Can','cylinder'),('Prop_Candle','cylinder'),('Prop_CoatHanger','pipe'),('Prop_Umbrella','pipe'),('Prop_Shoe','box'),('Prop_TrashBag','box'),('Prop_Keys','cylinder'),('Prop_KeyBowl','vase'),('Prop_CardboardBox','box'),('Prop_WoodCrate','crate'),('Prop_Bucket','bucket'),('Prop_WallClock','clock')]
generate_batch('Batch_08_Generic_Props',specs)
