import bpy, os, re

# Shared helpers for Creepy House procedural asset batches.
# Every asset is placed in its own named collection and can be auto-saved
# individually as a .blend file when the batch script calls finalize_asset().

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(bpy.data.filepath) or os.getcwd(), "generated_assets"))


def safe_filename(name):
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", name).strip("._") or "Asset"


def asset_collection(name):
    name = safe_filename(name)
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)
    return col


def finalize_asset(name, objects, auto_save=True):
    """Normalize names, isolate an asset, and optionally save it as name.blend."""
    asset_name = safe_filename(name)
    col = asset_collection(asset_name)

    # Move generated objects into this asset's collection.
    for obj in objects:
        if obj is None:
            continue
        obj.name = asset_name if obj == objects[0] else f"{asset_name}_{obj.name.split('_', 1)[-1]}"
        for old_col in list(obj.users_collection):
            old_col.objects.unlink(obj)
        if obj.name not in col.objects:
            col.objects.link(obj)

    # Keep the asset as the only selected objects in the current scene.
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        if obj and obj.name in bpy.data.objects:
            obj.select_set(True)
    if objects and objects[0]:
        bpy.context.view_layer.objects.active = objects[0]

    if auto_save:
        os.makedirs(ROOT_DIR, exist_ok=True)
        path = os.path.join(ROOT_DIR, f"{asset_name}.blend")
        # Save a copy so generating an asset does not destroy the main batch file.
        bpy.ops.wm.save_as_mainfile(filepath=path, copy=True)

    return col


def clean_generated_assets():
    """Remove previously generated asset collections/objects from the current scene."""
    for col in list(bpy.data.collections):
        if col.name.startswith("CH_"):
            bpy.data.collections.remove(col)
