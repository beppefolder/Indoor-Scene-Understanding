import torch
from torch.utils.data import DataLoader
from torchvision import transforms
from autoencoder_retrieval.retrieval_dataset import RetrievalDataset
from autoencoder_retrieval.autoencoder_utils import AutoencoderHelper
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt

# the dataset 'grabcut_kaggle_dataset' is on Drive

if __name__ == '__main__':

    helper = AutoencoderHelper('Grabcut_EncodeModel_kaggle_50_arch2.pth')
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])

    full_dataset = RetrievalDataset('grabcut_kaggle_dataset/', transforms=transform)
    full_loader = torch.utils.data.DataLoader(full_dataset, batch_size=2, shuffle=False)

    print("starting training...")
    # model=train(full_loader)
    print("training ended.")

    i = 0
    test_dataset = RetrievalDataset('test_kaggle/', transforms=transform)

    embedding_dim = (1, 256, 7, 7)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(device)
    # --> this two line to create the embedding file <--
    # do not use these unless you change the dataset

    #embedding = helper.create_embedding_full_dataset(full_dataset, embedding_dim)
    # torch.save(embedding, 'embedding_50_arch2.pt')

    embedding = torch.load('embedding_50_arch2.pt', map_location=device)
    numpy_embedding = embedding.cpu().detach().numpy()
    num_images = numpy_embedding.shape[0]
    flattened_embedding = numpy_embedding.reshape((num_images, -1))
    print(flattened_embedding.shape)

    knn = NearestNeighbors(n_neighbors=5, metric="cosine")
    knn.fit(flattened_embedding)

    for inputImage in test_dataset:
        trueImage = inputImage.squeeze(0).squeeze(0)
        trueImage = trueImage.permute(1, 2, 0)
        plt.imshow(trueImage)
        plt.title('true')
        plt.show()

        embedded_img = helper.create_embedding_single_image(inputImage)
        helper.find_similar(knn, embedded_img, full_dataset)


        i += 1
        if i > 200:
            break

