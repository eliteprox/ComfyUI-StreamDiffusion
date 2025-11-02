# Model Loader Usage Guide

## Overview

The ComfyUI-StreamDiffusion nodes have been updated to use proper model loaders instead of direct file paths. This prevents errors when the streamdiffusion library tries to interpret local file paths as HuggingFace repository IDs.

## Changes Made

### 1. New Loader Nodes

Three new loader nodes have been added:

#### StreamDiffusionLoraLoader
- **Purpose**: Loads LoRA models from ComfyUI's loras folder
- **Inputs**:
  - `lora_name`: Select from available LoRA files
  - `strength`: LoRA strength/scale (default: 0.5)
  - `previous_loras` (optional): Chain multiple LoRAs together
- **Output**: `LORA_DICT` - Dictionary of LoRA paths and strengths

#### StreamDiffusionIPAdapterLoader
- **Purpose**: Loads IPAdapter models from ComfyUI's ipadapter folder
- **Inputs**:
  - `ipadapter_model`: Select IPAdapter model file (e.g., ip-adapter-plus_sd15.bin)
  - `scale`: IPAdapter strength (default: 0.7)
  - `enabled` (optional): Enable/disable the IPAdapter
- **Output**: `IPADAPTER_MODEL` - IPAdapter model configuration

#### StreamDiffusionImageEncoderLoader
- **Purpose**: Loads image encoder directories from ComfyUI's ipadapter folder
- **Inputs**:
  - `image_encoder`: Select image encoder directory (e.g., image_encoder, clip_vision)
- **Output**: `IMAGE_ENCODER_PATH` - Path to the image encoder

### 2. Updated ControlNetTRTConfig Node

The `ControlNetTRTConfig` node has been updated:

**Removed Required Inputs:**
- `ipadapter_model_path` (STRING) - removed
- `image_encoder_path` (STRING) - removed  
- `ipadapter_scale` (FLOAT) - removed (now in IPAdapter loader)
- `ipadapter_enabled` (BOOLEAN) - removed (now in IPAdapter loader)
- `lora_dict_str` (STRING) - removed

**New Optional Inputs:**
- `lora_dict` (LORA_DICT) - Connect from StreamDiffusionLoraLoader
- `ipadapter_model` (IPADAPTER_MODEL) - Connect from StreamDiffusionIPAdapterLoader
- `image_encoder` (IMAGE_ENCODER_PATH) - Connect from StreamDiffusionImageEncoderLoader

### 3. Model Folder Structure

The custom node now registers the `ipadapter` model folder:
- Default location: `ComfyUI/models/ipadapter/`
- Place IPAdapter .bin files directly in this folder
- Place image encoder directories (e.g., `image_encoder/`) in this folder

## Migration Guide

### Old Workflow (Using File Paths)

```json
{
  "52": {
    "inputs": {
      "lora_dict_str": "{\"/workspace/ComfyUI/models/loras/SD1.5/PixelArt.safetensors\":1.2}",
      "ipadapter_model_path": "/workspace/ComfyUI/models/ipadapter/ip-adapter-plus_sd15.bin",
      "image_encoder_path": "/workspace/ComfyUI/models/ipadapter/image_encoder",
      "ipadapter_scale": 0.7,
      ...
    },
    "class_type": "ControlNetTRTConfig"
  }
}
```

### New Workflow (Using Loader Nodes)

```json
{
  "50": {
    "inputs": {
      "lora_name": "PixelArt.safetensors",
      "strength": 1.2
    },
    "class_type": "StreamDiffusionLoraLoader"
  },
  "51": {
    "inputs": {
      "ipadapter_model": "ip-adapter-plus_sd15.bin",
      "scale": 0.7,
      "enabled": true
    },
    "class_type": "StreamDiffusionIPAdapterLoader"
  },
  "53": {
    "inputs": {
      "image_encoder": "image_encoder"
    },
    "class_type": "StreamDiffusionImageEncoderLoader"
  },
  "52": {
    "inputs": {
      "lora_dict": ["50", 0],
      "ipadapter_model": ["51", 0],
      "image_encoder": ["53", 0],
      ...
    },
    "class_type": "ControlNetTRTConfig"
  }
}
```

## Example Workflow

See `examples/sd15_all_dynamic_params_wlora_fixed.json` for a complete working example.

## Benefits

1. **No more HuggingFace validation errors**: Local file paths are properly handled
2. **Better UI/UX**: Dropdown selectors for models instead of typing paths
3. **Type safety**: Proper data types prevent configuration errors
4. **Reusability**: Multiple LoRAs can be chained using the `previous_loras` input
5. **Consistency**: Matches ComfyUI's standard model loading patterns

## Troubleshooting

### "FileNotFoundError: ipadapter folder not found"
- The ipadapter folder will be automatically created at `ComfyUI/models/ipadapter/`
- Place your IPAdapter models in this folder

### "No models available in dropdown"
- Ensure your model files are in the correct ComfyUI model folders:
  - LoRAs: `ComfyUI/models/loras/`
  - IPAdapter: `ComfyUI/models/ipadapter/`
- Restart ComfyUI after adding new models

### "HFValidationError" when loading models
- If you still see HuggingFace errors, ensure you're using the loader nodes
- Check that the workflow connects the loader outputs to the config node
- Verify no hardcoded file paths remain in the workflow

## Bug Fixes

### Fixed `get_engine_configs()` Path Error
- Fixed bug where `get_engine_configs()` was using `parent_dir` (string name) instead of `parent_path` (full path)
- This was causing `FileNotFoundError: [Errno 2] No such file or directory: 'KBlueLeaf'`

