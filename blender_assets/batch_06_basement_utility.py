import bpy,sys,os
HERE=os.path.dirname(bpy.data.filepath) if bpy.data.filepath else ''
if HERE and HERE not in sys.path:sys.path.append(HERE)
from house_asset_common import generate_batch
specs=[('Basement_FuseBox','fusebox'),('Basement_ElectricalPanel','fusebox'),('Basement_Boiler','boiler'),('Basement_WaterHeater','boiler'),('Basement_Pipe_A','pipe'),('Basement_Pipe_B','pipe'),('Basement_Valve','cylinder'),('Basement_Workbench','workbench'),('Basement_Toolbox','toolbox'),('Basement_Shelf','shelf'),('Basement_Crate_A','crate'),('Basement_Crate_B','crate'),('Basement_Barrel','barrel'),('Basement_Bucket','bucket'),('Basement_Generator','box'),('Basement_HangingBulb','hanging_bulb'),('Basement_Vent','vent'),('Basement_Drain','cylinder'),('Basement_LockedDoor','door'),('Basement_Lamp','lamp')]
generate_batch('Batch_06_Basement_Utility',specs)
