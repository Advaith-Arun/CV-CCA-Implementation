import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from PIL import Image


def load_grayscale_image(path, target_size=None):
    """Load an image, convert to grayscale float32 in [0, 1]."""
    img = Image.open(path).convert("L")  # L = 8‑bit grayscale
    if target_size is not None:
        img = img.resize(target_size, Image.BILINEAR)
    img = np.asarray(img, dtype=np.float32)
    img = img / 255.0
    return img


def compute_fft2(image):
    """Compute centered 2D FFT and log‑magnitude spectrum."""
    F = np.fft.fft2(image)
    F_shift = np.fft.fftshift(F)
    magnitude = np.abs(F_shift)
    log_magnitude = np.log1p(magnitude)  # log(1 + |F|)
    return F, F_shift, log_magnitude


def make_circular_masks(shape, low_radius_frac=0.1, high_radius_frac=0.25):
    """
    Create low‑pass and high‑pass circular masks.

    low_radius_frac, high_radius_frac are relative to min(H, W)/2.
    """
    h, w = shape
    cy, cx = h // 2, w // 2
    Y, X = np.ogrid[:h, :w]
    dist = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)

    max_radius = min(h, w) / 2.0
    low_radius = low_radius_frac * max_radius
    high_radius = high_radius_frac * max_radius

    low_pass_mask = dist <= low_radius
    high_pass_mask = dist >= high_radius

    return low_pass_mask.astype(np.float32), high_pass_mask.astype(np.float32), (
        low_radius,
        high_radius,
        (cx, cy),
    )


def reconstruct_from_fft(F_shift, mask):
    """Apply mask in frequency domain and reconstruct spatial image."""
    F_shift_masked = F_shift * mask
    F_unshift = np.fft.ifftshift(F_shift_masked)
    img_rec = np.fft.ifft2(F_unshift)
    img_rec = np.real(img_rec)
    # Normalize to [0, 1] for display
    img_min, img_max = img_rec.min(), img_rec.max()
    if img_max > img_min:
        img_rec = (img_rec - img_min) / (img_max - img_min)
    else:
        img_rec = np.zeros_like(img_rec)
    return img_rec


def main():
    
    # 1. Load MRI/CT slice
    image_path = "mri_slice.png"  # put your MRI/CT PNG/JPG here
    img = load_grayscale_image(image_path, target_size=None)

    # 2. Compute FFT and magnitude spectrum
    F, F_shift, log_mag = compute_fft2(img)

    # 3. Build low‑pass and high‑pass masks
    low_mask, high_mask, (low_r, high_r, center) = make_circular_masks(
        img.shape, low_radius_frac=0.12, high_radius_frac=0.28
    )

    # 4. Reconstruct low‑frequency and high‑frequency images
    img_low = reconstruct_from_fft(F_shift, low_mask)
    img_high = reconstruct_from_fft(F_shift, high_mask)

    # 5. Plot results
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    ax_orig, ax_fft, ax_fft_overlay, ax_low, ax_high, ax_masks = axes.ravel()

    # Original image
    ax_orig.imshow(img, cmap="gray")
    ax_orig.set_title("Original MRI/CT (Spatial Domain)")
    ax_orig.axis("off")

    # Magnitude spectrum
    ax_fft.imshow(log_mag, cmap="gray")
    ax_fft.set_title("Log Magnitude Spectrum\n(Frequency Domain)")
    ax_fft.axis("off")

    # Magnitude spectrum with low/high‑freq rings
    ax_fft_overlay.imshow(log_mag, cmap="gray")
    cy, cx = center
    low_circle = Circle((cx, cy), low_r, edgecolor="lime", facecolor="none", linewidth=1.5)
    high_circle = Circle((cx, cy), high_r, edgecolor="red", facecolor="none", linewidth=1.5)
    ax_fft_overlay.add_patch(low_circle)
    ax_fft_overlay.add_patch(high_circle)
    ax_fft_overlay.set_title("Low vs High Frequencies\n(green: low, red: high)")
    ax_fft_overlay.axis("off")

    # Low‑frequency reconstruction
    ax_low.imshow(img_low, cmap="gray")
    ax_low.set_title("Low‑Frequency Image\n(overall structure)")
    ax_low.axis("off")

    # High‑frequency reconstruction
    ax_high.imshow(img_high, cmap="gray")
    ax_high.set_title("High‑Frequency Image\n(edges / noise)")
    ax_high.axis("off")

    # Visualize masks
    ax_masks.imshow(low_mask + high_mask, cmap="gray")
    ax_masks.set_title("Masks in Frequency Domain\nwhite=kept, black=removed")
    ax_masks.axis("off")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
