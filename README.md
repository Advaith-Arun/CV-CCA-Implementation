# Computer Vision Coursework Portfolio

- **Name:** Advaith Arun Kashyap  
- **USN:** 1BY23AI011  
- **Subject:** Computer Vision  

---

## Task 3 – Spatial Frequency and Fourier Transforms in Medical Imaging

This mini-project demonstrates how spatial frequencies in medical images (MRI/CT) can be analyzed and manipulated using the 2D Fourier Transform. The implementation operates on a single MRI/CT slice stored as an image file (e.g., `mri_slice.png`) and shows how low- and high-frequency components contribute differently to the final image.

The work is directly inspired by how clinical MRI systems represent raw data in k-space (frequency domain) and reconstruct images using inverse Fourier transforms. 

---

## Implementation Overview

The core implementation is a single Python script (e.g., `FourierTransformCaseStudy.py`), which uses `NumPy`, `Pillow`, and `Matplotlib`:

1. **Image Acquisition (MRI/CT Slice)**  
   - Load a 2D MRI/CT slice from disk (PNG/JPEG) using `PIL.Image`, convert it to grayscale, and normalize intensities to \([0,1]\).  
   - The input is treated as a spatial-domain image, analogous to what a radiologist would see on a scanner console.

2. **Fourier Transform and Spectrum Visualization**  
   - Compute the 2D Fast Fourier Transform (FFT) of the image and apply an FFT shift so that the zero-frequency component is centered.  
   - Display the **log-magnitude spectrum**, which reveals how image energy is distributed across spatial frequencies (low frequencies near the center, high frequencies toward the edges). 

3. **Frequency-Domain Masking (Low-Pass & High-Pass)**  
   - Construct **circular low-pass and high-pass masks** in the frequency domain:
     - **Low-pass mask:** keeps frequencies within a small radius of the center, removing higher frequencies.  
     - **High-pass mask:** keeps frequencies outside a larger radius, removing most low frequencies.   
   - Overlay the inner (low-pass) and outer (high-pass) circles on the magnitude spectrum to visually distinguish which parts of k-space are being kept for each reconstruction.

4. **Reconstruction via Inverse FFT**  
   - Apply the low-pass mask to the shifted spectrum, inverse-shift, then use the 2D inverse FFT to reconstruct a **low-frequency image**.  
   - Apply the high-pass mask similarly to reconstruct a **high-frequency image**.  
   - Normalize both reconstructions to \([0,1]\) for consistent visualization.

5. **Visualization Layout**  
   - The script displays six panels in a single Matplotlib figure:
     - Original MRI/CT slice (spatial domain).  
     - Log-magnitude spectrum (frequency domain).  
     - Spectrum with low/high frequency rings overlaid.  
     - Low-frequency reconstruction (blurred, denoised structure).  
     - High-frequency reconstruction (edge-enhanced, detail/noise).  
     - Binary mask visualization showing which frequencies are retained in each filter.

---

## Results and Interpretation

- The **original image** shows full anatomical detail, combining both low-contrast structures and sharp boundaries.  
- The **Fourier magnitude spectrum** has most of its energy concentrated at the center, confirming that low spatial frequencies dominate the global appearance, while higher frequencies at the periphery encode edges and fine detail.

- The **low-pass reconstructed image**:
  - Preserves global anatomy and intensity trends.  
  - Appears smoother and slightly blurred, with reduced noise and softened edges, as expected from low-pass filtering. 

- The **high-pass reconstructed image**:
  - Suppresses smooth background regions and large-scale gradients.  
  - Emphasizes edges, contours, and small structures, but also amplifies high-frequency noise. 

Together, these views provide an intuitive demonstration of how different regions of k-space contribute to image contrast, structure, and sharpness.

---

## Real-World Relevance (MRI/CT)

Although this is a simplified 2D example using a single image slice, it reflects several core ideas from real medical imaging practice:

- **k-Space and Reconstruction**  
  - In MRI, raw data are naturally acquired in k-space (frequency domain), and applying a 2D inverse Fourier Transform reconstructs the final image, just as in this project.

- **Noise Reduction and Smoothing**  
  - Low-pass style operations in the frequency domain reduce high-frequency noise at the cost of edge sharpness, a trade-off that MRI/CT vendors must manage carefully in their reconstruction pipelines. 

- **Edge Enhancement and Feature Emphasis**  
  - High-pass or edge-emphasizing operations can make anatomical boundaries more visible but simultaneously increase noise, illustrating why clinical systems use more sophisticated, often hybrid filters.

Companies such as **Siemens Healthineers** and **GE HealthCare** apply these same Fourier and frequency-domain concepts in their reconstruction engines and image processing chains, combining them with advanced sampling strategies, regularization, and artifact correction to produce diagnostic-quality MRI/CT images.
