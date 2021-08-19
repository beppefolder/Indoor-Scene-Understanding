import dhash
import operator
import os
from PIL import Image
from image_with_Hash import Images_with_Hash

class DHash_Helper():
    def __init__(self, folder):
        self.folder = folder

    # computing the hash value for each image in the retrieval dataset
    def compute_hash_dataset(self):
        all_images_hashed = []
        for f in os.listdir(self.folder):
            img = Image.open(os.path.join(self.folder, f))
            row, col = dhash.dhash_row_col(img)
            hashed_image = Images_with_Hash(f, int(dhash.format_hex(row, col), 16))
            all_images_hashed.append(hashed_image)

        return all_images_hashed


    # computing the hash bit differences between the input image and the rest of the retrieval dataset
    # returning the first 11 most similar objects, not considering a threshold value
    def match_furniture(self , img, all_images_hashed):

        threshold = 40

        img_row, img_col = dhash.dhash_row_col(img)
        img_hash = dhash.format_hex(img_row, img_col)
        img_hash = int(img_hash, 16)
        differences = {}

        # Computing Hamming distance bewtween query and dataset image 
        for idx, single_hash_image in enumerate(all_images_hashed):
            differences[idx] = dhash.get_num_bits_different(img_hash, single_hash_image.hash)

        print(differences)

        # sorting images of dataset by difference value
        sorted_x = sorted(differences.items(), key=operator.itemgetter(1))
        print('ordinati:')
        print(sorted_x)

        # taking only the first 11 images
        first_eleven = sorted_x[:11]

        res_img_name = []
        for rel in first_eleven:
            res_img_name.append(all_images_hashed[rel[0]])

        '''res_img_name = []
        for idx , d in enumerate(differences):
            if d <= threshold:
            res_img_name.append(all_images_hashed[idx]) '''

        return res_img_name