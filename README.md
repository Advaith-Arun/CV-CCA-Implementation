# Computer Vision CCA README details

- Name: Advaith Arun Kashyap
- USN: 1BY23AI011
- Subject: BAI505B (Computer Vision)

## Task 3 - Fourier Analysis and Filtering in Medical Imaging

This project explores the application of Fourier Transforms in the context of medical imaging (specifically CT scans using the Shepp-Logan Phantom). The primary goal is to visualize the frequency domain and demonstrate how filtering specific frequencies affects image reconstruction.

### Key Objectives
 - Converting spatial domain images (CT Scans) into the frequency domain using Fourier Transform (FFT).
 - Identifying and separating signal components. Low frequencies represent overall structure, smooth gradients, and contrast.High frequencies represent sharp edges, fine details, and sensor noise.

---

## Experiments and Implementation

The core script (FourierTransformAnalysis.ipynb) implements the following processing pipeline:

1. Image Acquisition: Loading a standard medical test image (Shepp-Logan Phantom) to simulate a CT scan.
2. Spectrum Analysis: Computing the 2D Discrete Fourier Transform to visualize the magnitude spectrum (K-space).
3. Filter Simulation:
   * Low Pass Filter: Applies a mask to block high frequencies. The result removes noise and fine details while retaining overall structure (blurring effect).
   * High Pass Filter: Applies a mask to block low frequencies. The result removes structural gradients and extracts edges and boundaries.
4. Reconstruction: Utilizing the Inverse Fast Fourier Transform (IFFT) to convert the filtered spectrums back into viewable spatial images.

---

## Real-World Applications

This module covers the theoretical foundations for:

* Medical Imaging: Improving MRI/CT clarity by dampening high-frequency sensor noise.
* Artifact Removal: Using Notch filters to remove periodic electrical interference patterns.
* Image Compression: Understanding how algorithms discard high-frequency data to reduce file sizes without significant visual loss.
