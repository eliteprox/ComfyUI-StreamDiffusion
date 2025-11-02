import folder_paths
import os

# Register custom model folder paths for IPAdapter and related models
ipadapter_path = os.path.join(folder_paths.models_dir, "ipadapter")
if not os.path.exists(ipadapter_path):
    try:
        os.makedirs(ipadapter_path, exist_ok=True)
    except OSError as e:
        print(f"[StreamDiffusion] Warning: Could not create ipadapter directory at {ipadapter_path}: {e}")

folder_paths.add_model_folder_path("ipadapter", ipadapter_path)

from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

