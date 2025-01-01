# Machine Learning Model Specifications

In the following, we describe the machine learning model used and its underlying data.

## Model Overview
- **Name**: SCUNET
- **Version**: SCUNET_25 and SCUNET_50
- **Date**: 01.12.2023
- **Type**: Denoising model

## Introduction
SCUNet is a deep learning model designed for blind image denoising, effectively removing various types of noise from images without prior knowledge of the noise characteristics. Its architecture integrates the Swin Transformer with a U-Net backbone, enabling both local and non-local feature extraction. This design makes SCUNet particularly suitable for denoising microscopy images, which often contain complex noise patterns.  

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
  - Step 1: [Description]
  - Step 2: [Description]
  - ...

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


## Ethical Considerations
Discuss any ethical considerations or potential biases in the model.

## Limitations
Identify the limitations and constraints of the model and link related publications if available.

## References
- [Reference 1]: [Description or Link]
- [Reference 2]: [Description or Link]
- ...

## Contact Information
- **Author**: [Your Name]
- **Email**: [Your Email Address]

## Sources
1. Rahman, S.S.M.M., Salomon, M. & Dembélé, S. Towards scanning electron microscopy image denoising: a state-of-the-art overview, benchmark, taxonomies, and future direction. Machine Vision and Applications 35, 87 (2024). https://doi.org/10.1007/s00138-024-01573-9.
2. Aversa, R., Modarres, M., Cozzini, S. et al. The first annotated set of scanning electron microscopy images for nanoscience. Sci Data 5, 180172 (2018). https://doi.org/10.1038/sdata.2018.172.
3. Zhang, K., Li, Y., Liang, J., Cao, J., Zhang, Y., Tang, H., Fan, D.-P., Timofte, R., Gool, L.V.: Practical blind image denoising via Swin-Conv-UNet and data synthesis. Mach. Intell. Res. (2023). https://doi.org/10.1007/s11633-023-1466-0