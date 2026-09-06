import bpy,sys,os
HERE=os.path.dirname(bpy.data.filepath) if bpy.data.filepath else ''
if HERE and HERE not in sys.path:sys.path.append(HERE)
from house_asset_common import generate_batch
specs=[('Bedroom_Bed_A','bed'),('Bedroom_Bed_B','bed'),('Bedroom_Nightstand','cabinet'),('Bedroom_Dresser','cabinet'),('Bedroom_Wardrobe','cabinet'),('Bedroom_Desk','table'),('Bedroom_Chair','chair'),('Bedroom_Mirror','mirror'),('Bedroom_BedsideLamp','lamp'),('Bedroom_Rug','rug'),('Bedroom_Clock','clock'),('Bedroom_Picture','photograph'),('Bedroom_Drawer','drawer'),('Bedroom_Shelf','shelf'),('Bedroom_Suitcase','suitcase'),('Bedroom_Trunk','trunk'),('Bedroom_Toy','toy'),('Bedroom_Books','book'),('Bedroom_Bottle','bottle'),('Bedroom_CurtainRod','pipe')]
generate_batch('Batch_04_Bedrooms',specs)
