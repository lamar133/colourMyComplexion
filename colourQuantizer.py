# Colour Quantizer using kMeans
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin
from sklearn.datasets import load_sample_image
from sklearn.utils import shuffle
from scipy.ndimage import imread
import os
import settings
import pdb

def recreate_image(codebook, labels, w, h):
    d = codebook.shape[1]
    image = np.zeros((w, h, d))
    label_idx = 0
    for i in range(w):
        for j in range(h):
            image[i][j] = codebook[labels[label_idx]]
            label_idx += 1
    return image

def transformPhotos(album, n_colours):
    print("starting transformPhotos function")
    count = 0
    counter = 0
    pdb.set_trace()
    for root, dirs, filenames in os.walk('.'):
        colours = []
        print("inside first for loop")
        for pic in filenames:
            print("inside second for loop")
            count += 1
            # Convert to floats instead of the default 8 bits integer coding. Dividing by
            # 255 is important so that plt.imshow behaves works well on float data (need to
            # be in the range [0-1]
            img = imread(os.path.join(root, pic))
            jpg = np.array(img, dtype=np.float64) / 255

            # Load Image and transform to a 2D numpy array.
            w, h, d = tuple(jpg.shape)
            image_array = np.reshape(jpg, (w * h, d))

            image_array_sample = shuffle(image_array, random_state=0)[:1000]
            kmeans = KMeans(n_clusters=n_colours, random_state=0).fit(image_array_sample)

            # Get labels for all points
            labels = kmeans.predict(image_array)

            quantized_image = recreate_image(kmeans.cluster_centers_, labels, w, h)
            quantized_rgb = (kmeans.cluster_centers_ * 255).tolist()
            quantized_rgb = [[int(i) for i in j] for j in  quantized_rgb]
            colours.append(quantized_rgb)
            print("transforming photo ", count)
        settings.COLOURS.append(colours)
        print(settings.COLOURS[counter])
        counter += 1
    emptyList = settings.COLOURS[0]
    settings.COLOURS.remove(emptyList)
        
if __name__ == '__main__':
    main()