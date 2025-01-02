# Machine Learning Model Specifications

In the following, we describe the machine learning model used and its underlying data.

## Model Overview
- **Name**: SCUNET
- **Version**: SCUNET_25 and SCUNET_50
- **Date**: 01.12.2023
- **Type**: Denoising model

## Introduction
After conducting research on benchmarks for denoising microscopic images, I came across the study *"Towards Scanning Electron Microscopy Image Denoising: A State-of-the-Art Overview, Benchmark, Taxonomies, and Future Direction"* [1]. The paper presents a comprehensive evaluation of multiple denoising architectures, including SCUNet, DnCNN, FFDNet, and SwinIR, specifically on SEM image datasets. Among these, SCUNet consistently demonstrated superior performance in balancing noise removal and preserving fine structural details. While DnCNN and FFDNet struggled with over-smoothing and loss of intricate features, and SwinIR showed limitations in handling highly textured noise patterns, SCUNet excelled across varying noise levels and image complexities. Its hybrid architecture, combining convolutional layers with transformer-based designs, enables it to effectively capture both local and global noise characteristics. These strengths, validated through quantitative benchmarks and qualitative analysis in the study, make SCUNet a clear choice for reliable and high-quality SEM image denoising.

SCUNet is a deep learning model designed for **blind image denoising**, effectively removing various types of noise from images without requiring prior knowledge of the noise characteristics. Its architecture integrates the **Swin Transformer** with a **U-Net backbone**, enabling both local and non-local feature extraction. This design makes SCUNet particularly suitable for denoising microscopy images, which often contain complex noise patterns.

To ensure flexibility and adaptability for different noise levels, I have included **two pretrained SCUNet models**, trained on noise levels of **25** and **50**. These pretrained weights leverage SCUNet's blind denoising capabilities, allowing the models to generalize across diverse noise scenarios without explicit noise parameter inputs. By offering both options, users can **select the degree of denoising** based on the severity of noise in their images. For moderately noisy images, the model trained on noise level **25** may suffice, preserving finer details, while heavily degraded images might benefit from the more aggressive denoising capabilities of the model trained on noise level **50**. This approach ensures adaptability, user control, and optimal image restoration across a wide range of SEM imaging conditions.

## Model Architecture
- **Architecture Type**: Swin-Conv Block: Each block consists of a 1×1 convolution, followed by splitting the input into two feature map groups. One group passes through a Swin Transformer block, and the other through a residual 3×3 convolutional block. The outputs are concatenated and processed through another 1×1 convolution to produce the residual of the input.
- **Layers/Components Summary**:
  - Swin-Conv Block: Each block consists of a 1×1 convolution, followed by splitting the input into two feature map groups. One group passes through a Swin Transformer block, and the other through a residual 3×3 convolutional block. The outputs are concatenated and processed through another 1×1 convolution to produce the residual of the input.
  - U-Net Backbone: Utilizes an encoder-decoder structure with skip connections to capture multi-scale features, enhancing the model's ability to reconstruct clean images from noisy inputs.
- **Framework Used**: PyTorch

<img src="figs/arch_scunet.png" width="900px"/> 

## Input Requirements
Gray scale images

## Data Specifications
- **Dataset Name**: [SEM-Dataset-500](https://github.com/motiurinfo/SEM-Dataset-500/tree/main)
- **Source**: A selction of high quality images made by the authors of [1] originally from [2]
- **Size**: [500 Samples, 1024x768]
- **Preprocessing Steps**:
  - **1. Normalize Image (`pil2unit`)**  
   - Converts the image pixel values to a **[0,1] range** for consistency.  

  - **2. Convert to Single Precision (`uint2single`)**  
    - Changes the image format to **single-precision floating point** for model compatibility.  

  - **3. Add Noise (for training and testing, if no real noisy images are available) (Optional, `need_degradation`)**  
    - Adds **Gaussian noise** to the image if `need_degradation` is enabled.  
    - Noise level is controlled by `noise_level_img/255.`.  
    - Ensures reproducibility using a **fixed random seed (`0`)**.  

  - **4. Convert to Tensor (`single2tensor`)**  
    - Transforms the image into a **PyTorch tensor** for model processing.  

  - **5. Move to Device (`to(device)`)**  
    - Sends the tensor to the specified **device (CPU or GPU)** for efficient computation.  

  These steps ensure the image is properly formatted, optionally degraded for testing, and ready for SCUNet's denoising process.


## Training Details
- **Training done by**: The authors of SCUNET
- **Training Duration**: 3 days [3]. 
- **Hardware Used**: four NVIDIA RTX 2080 Ti GPUs [3].
- **Optimizer**: Adam [3].
- **Loss Function**: 
$$
\min_W \sum_i \mathcal{L}(\hat{x}_i(y_i, W), x_i)
$$
where \( W \) denotes the network parameters to be learned, \(\{y_i, x_i\}\) represents the training noisy-clean image pairs, \( \mathcal{L}(\cdot) \) is the **loss** function. In this sense, the deep blind denoising model should capture the knowledge of degradation.

## Evaluation Metrics
**PSNR (Peak Signal-to-Noise Ratio):** Measures image quality by comparing pixel-level differences (between the high quality and the denoised image), with higher values indicating better quality.

**SSIM (Structural Similarity Index Measure):** Measures image similarity (between the high quality and the denoised image) based on structure, luminance, and contrast, with values closer to 1 indicating higher similarity.
| Dataset | Noise level | PSNR | SSIM |
|----------|----------|----------|----------|
| SEM-Dataset-500 | 25 | 16.400 | 0.418 |
| SEM-Dataset-500 | 50 | 23.263 | 0.628 |

## Limitations
Identify the limitations and constraints of the model and link related publications if available.

## References
1. Rahman, S.S.M.M., Salomon, M. & Dembélé, S. Towards scanning electron microscopy image denoising: a state-of-the-art overview, benchmark, taxonomies, and future direction. Machine Vision and Applications 35, 87 (2024). https://doi.org/10.1007/s00138-024-01573-9.
2. Aversa, R., Modarres, M., Cozzini, S. et al. The first annotated set of scanning electron microscopy images for nanoscience. Sci Data 5, 180172 (2018). https://doi.org/10.1038/sdata.2018.172.
3. Zhang, K., Li, Y., Liang, J., Cao, J., Zhang, Y., Tang, H., Fan, D.-P., Timofte, R., Gool, L.V.: Practical blind image denoising via Swin-Conv-UNet and data synthesis. Mach. Intell. Res. (2023). https://doi.org/10.1007/s11633-023-1466-0

## Contact Information
- **Author**: Abdelrahman Elsharkawi
- **Email**: a.elsharkawi99@gmail.com
