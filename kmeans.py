import cv2
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

IMAGE_PATH = "data/brain_mri.jpg"
K = 3

image = cv2.imread(IMAGE_PATH, cv2.IMREAD_GRAYSCALE)

if image is None:
    raise FileNotFoundError(f"Could not find the image at {IMAGE_PATH}")


pixels = image.reshape(-1, 1)

kmeans = KMeans(n_clusters=K, random_state=42, n_init=10)
labels = kmeans.fit_predict(pixels)


segmented = labels.reshape(image.shape)


plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.title("Original")
plt.imshow(image, cmap="gray")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.title(f"K-Means (K={K})")
plt.imshow(segmented, cmap="viridis")
plt.axis("off")

plt.savefig(f"results/segmented_k{K}.png")
plt.show()

print(f"Done! Saved to results/segmented_k{K}.png")
