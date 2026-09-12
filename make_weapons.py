import bpy
import bmesh
import math
import os

out_dir = r"c:\Users\Laptop Dell\OneDrive\Desktop\Ssg\IslaSalvaje\Content\Characters\Weapons"
os.makedirs(out_dir, exist_ok=True)

def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. WARRIOR BATTLEAXE
reset_scene()
# Handle
bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=1.1, location=(0, 0, 0.55))
handle = bpy.context.active_object
handle.name = "Battleaxe_Handle"

# Left Blade
bpy.ops.mesh.primitive_cube_add(size=0.3, location=(-0.2, 0, 0.95))
blade_l = bpy.context.active_object
blade_l.scale = (1.2, 0.08, 1.4)

# Right Blade
bpy.ops.mesh.primitive_cube_add(size=0.3, location=(0.2, 0, 0.95))
blade_r = bpy.context.active_object
blade_r.scale = (1.2, 0.08, 1.4)

# Top Spike
bpy.ops.mesh.primitive_cone_add(radius1=0.04, depth=0.25, location=(0, 0, 1.15))
spike = bpy.context.active_object

# Join
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.join()
bpy.context.active_object.name = "SM_Warrior_Battleaxe"
bpy.ops.export_scene.fbx(filepath=os.path.join(out_dir, "SM_Warrior_Battleaxe.fbx"), use_selection=True)
print("Exported SM_Warrior_Battleaxe.fbx")

# 2. ASSASSIN DAGGER
reset_scene()
# Grip
bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.18, location=(0, 0, 0.09))
grip = bpy.context.active_object
# Guard
bpy.ops.mesh.primitive_cube_add(size=0.08, location=(0, 0, 0.18))
guard = bpy.context.active_object
guard.scale = (1.2, 0.4, 0.3)
# Blade
bpy.ops.mesh.primitive_cone_add(radius1=0.035, depth=0.35, location=(0, 0, 0.36))
blade = bpy.context.active_object
blade.scale = (1.0, 0.25, 1.0)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.join()
bpy.context.active_object.name = "SM_Assassin_Dagger"
bpy.ops.export_scene.fbx(filepath=os.path.join(out_dir, "SM_Assassin_Dagger.fbx"), use_selection=True)
print("Exported SM_Assassin_Dagger.fbx")

# 3. MAGE STAFF
reset_scene()
# Long Shaft
bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=1.6, location=(0, 0, 0.8))
staff = bpy.context.active_object
# Crystal Head
bpy.ops.mesh.primitive_ico_sphere_add(radius=0.12, subdivisions=2, location=(0, 0, 1.68))
crystal = bpy.context.active_object
crystal.scale = (0.7, 0.7, 1.4)
# Arcane Rings
bpy.ops.mesh.primitive_torus_add(major_radius=0.14, minor_radius=0.015, location=(0, 0, 1.62))

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.join()
bpy.context.active_object.name = "SM_Mage_Staff"
bpy.ops.export_scene.fbx(filepath=os.path.join(out_dir, "SM_Mage_Staff.fbx"), use_selection=True)
print("Exported SM_Mage_Staff.fbx")

# 4. HUNTER BOW
reset_scene()
# Curved Limbs (Torus section)
bpy.ops.mesh.primitive_torus_add(major_radius=0.6, minor_radius=0.025, location=(0, 0, 0.6))
bow = bpy.context.active_object
bow.scale = (0.3, 1.0, 1.0)
# String
bpy.ops.mesh.primitive_cylinder_add(radius=0.005, depth=1.15, location=(0.15, 0, 0.6))

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.join()
bpy.context.active_object.name = "SM_Hunter_Bow"
bpy.ops.export_scene.fbx(filepath=os.path.join(out_dir, "SM_Hunter_Bow.fbx"), use_selection=True)
print("Exported SM_Hunter_Bow.fbx")

# 5. SHAMAN TOTEM
reset_scene()
# Totem Pole
bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=1.0, location=(0, 0, 0.5))
totem = bpy.context.active_object
# Carved Skull / Totem Top
bpy.ops.mesh.primitive_cube_add(size=0.25, location=(0, 0, 0.95))
top = bpy.context.active_object
top.scale = (1.2, 1.0, 1.1)
# Horn L
bpy.ops.mesh.primitive_cone_add(radius1=0.04, depth=0.22, location=(-0.16, 0, 1.1))
# Horn R
bpy.ops.mesh.primitive_cone_add(radius1=0.04, depth=0.22, location=(0.16, 0, 1.1))

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.join()
bpy.context.active_object.name = "SM_Shaman_Totem"
bpy.ops.export_scene.fbx(filepath=os.path.join(out_dir, "SM_Shaman_Totem.fbx"), use_selection=True)
print("Exported SM_Shaman_Totem.fbx")