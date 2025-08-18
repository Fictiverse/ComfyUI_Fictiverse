# ComfyUI Fictiverse Nodes
 Custom nodes for [ComfyUI](https://github.com/comfyanonymous/ComfyUI).

## Installation
1. Install [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
2. git clone in the ```custom_nodes``` folder inside your ComfyUI installation or download as zip and unzip the contents to ```custom_nodes/ComfyUI_Fictiverse```.
3. Start/restart ComfyUI

## 📂 Available Nodes

### 🖼 Image Nodes
- **AddMarginWithColor**  
  Add margins around an image with a specified color.  

- **IfImageValid**  
  Conditional node that checks if an image is valid, outputs one of two options accordingly.  

- **ImageParams**  
  Provides image-related parameters as outputs.  

- **IsValid**  
  Simple validator node to check the integrity of inputs.  

- **NoneIfSameImage**  
  Compares images and returns `None` if they are the same. Useful to prevent redundant processing.  

- **ResizeImagesToMegapixels**  
  Resize a batch of images to a defined megapixel resolution.  

- **ResizeToMegapixels**  
  Resize a single image to a defined megapixel resolution.  

### 🎥 Video Nodes
- **GetLastOutputVideoPath**  
  Returns the file path of the last generated video in the output folder.  

- **VideoParams**  
  Provides video-related parameters as outputs.  

### 🧩 Utility / Workflow Nodes
- **EssentialParams**  
  Provides essential parameters for workflows.  

- **PromptAssembler**  
  Assemble 3 text prompts with ajustable strength for each.  

---




