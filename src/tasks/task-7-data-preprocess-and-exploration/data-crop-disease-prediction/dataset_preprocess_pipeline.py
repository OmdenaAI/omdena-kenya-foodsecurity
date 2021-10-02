import numpy as np
import cv2
import pandas as pd
import os

"""
Main script to preprocess data crop disease prediction datasets (links from Kaggles).
This script is applicable for all datasets except dataset 8 (it uses tfrecords).
"""


def resize_image(image, width, height):
    """ Function to resize an image to the dimensions that neural network requests

    Args:
        image (image): image that is needed to be resized
        width (integer): width of the requested image's dimensions
        height (integer): height of the requested image's dimensions

    Returns:
        (image): image with requested dimensions
    """
    return cv2.resize(image, (width, height))


def dataset_preprocess_pipeline(dataset_path, new_dataset_path, width, height):
    """ Main function to preprocess the dataset

    Args:
        dataset_path (string): path to the original dataset
        new_dataset_path (string): path to the new dataset
        width (integer): width of the requested image's dimensions
        height (integer): height of the requested image's dimensions
    """

    #go through each folder class in dataset
    class_folders = np.array([ f.name for f in os.scandir(dataset_path) if f.is_dir()])

    #check if new dataset folders exist to create it first
    if not os.path.exists(new_dataset_path + os.path.sep + 'images'):
            os.makedirs(new_dataset_path + os.path.sep + 'images')

    #create empty dictionary to store image names with corresponding class
    image_class_dictionary = {}

    #iterate over each class in the dataset
    for class_folder in class_folders:

        #get each name of image for concrete class
        images_path = dataset_path + os.path.sep + class_folder
        image_names = np.array([ f.name for f in os.scandir(images_path) if f.is_file()])

        #iterate over images of concrete class
        for image_name in image_names:
            
            #add the image name and class to dictionary
            image_class_dictionary[image_name] = class_folder

            #pipeline for an image: read it -> resize it -> write_into_new_dataset
            current_image = cv2.imread(images_path + os.path.sep + image_name)
            current_image = resize_image(current_image, height, width)
            cv2.imwrite(new_dataset_path + os.path.sep + 'images' + os.path.sep + image_name, current_image)

    #create dataframe and save it as a csv in new dataset
    image_class_dataframe = pd.DataFrame.from_dict(image_class_dictionary, orient="index").reset_index()
    image_class_dataframe.columns = ['image_name', 'image_class']
    image_class_dataframe.to_csv(new_dataset_path + os.path.sep + 'image_class_table.csv', 
                                 index=False)


if __name__ == "__main__":
    #experiment how to properly preprocess dataset1

    #first running the preprocess for **training** dataset
    dataset_preprocess_pipeline(
        dataset_path='./dataset1/train',
        new_dataset_path='./new_dataset1/train',
        width = 256,
        height = 256
    )

    #after running the preprocess for **test** dataset
    dataset_preprocess_pipeline(
        dataset_path='./dataset1/test',
        new_dataset_path='./new_dataset1/test',
        width = 256,
        height = 256
    )
