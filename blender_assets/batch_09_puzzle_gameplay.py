import bpy,sys,os
HERE=os.path.dirname(bpy.data.filepath) if bpy.data.filepath else ''
if HERE and HERE not in sys.path:sys.path.append(HERE)
from house_asset_common import generate_batch
specs=[('Puzzle_LockedDoor','door'),('Puzzle_Padlock','padlock'),('Puzzle_Key','cylinder'),('Puzzle_CombinationLock','padlock'),('Puzzle_Fuse','cylinder'),('Puzzle_FuseHolder','fusebox'),('Puzzle_BreakerSwitch','switch'),('Puzzle_PullChain','pipe'),('Puzzle_HiddenButton','switch'),('Puzzle_WallSwitch','switch'),('Puzzle_Lever','lever'),('Puzzle_Safe','safe'),('Puzzle_SafeDial','safe'),('Puzzle_Keypad','keypad'),('Puzzle_Note','note'),('Puzzle_TornPhoto','photograph'),('Puzzle_Box','puzzle_box'),('Puzzle_Drawer','drawer'),('Puzzle_SecretBookcase','secret_bookcase'),('Puzzle_RitualTable','ritual_table')]
generate_batch('Batch_09_Puzzle_Gameplay',specs)
