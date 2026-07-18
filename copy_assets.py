import os
import shutil

# Source paths from brain directory
avatar_src = "/home/dctrng/.gemini/antigravity/brain/8f7999df-9982-4062-871f-af762c092256/default_avatar_1784357067217.png"
group_src = "/home/dctrng/.gemini/antigravity/brain/8f7999df-9982-4062-871f-af762c092256/default_group_1784357078704.png"

# Target paths
targets = [
    ("/home/dctrng/Documents/Teky_12_Chat/media/avatars", "default_avatar.png", avatar_src),
    ("/home/dctrng/Documents/Teky_12_Chat/static/images", "default_avatar.png", avatar_src),
    ("/home/dctrng/Documents/Teky_12_Chat/static/images", "default_group.png", group_src)
]

for folder, filename, src in targets:
    os.makedirs(folder, exist_ok=True)
    dst = os.path.join(folder, filename)
    shutil.copy(src, dst)
    print(f"Copied {src} -> {dst}")
