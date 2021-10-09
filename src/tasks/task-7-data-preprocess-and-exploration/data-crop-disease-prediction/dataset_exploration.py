import pandas as pd
import matplotlib.pyplot as plt


def dataset_exploration(dataset_csv_path):
    """ Function to print and plot the distribution of classes in given dataset csv file

    Args:
        dataset_csv_path (string): path to the dataset csv file
    """
    #read csv file
    csv_df = pd.read_csv(dataset_csv_path)

    #get size for each class in dataset and plot it
    class_size_df = csv_df['image_class'].value_counts().sort_values()
    class_size_df.plot(kind = 'barh')
    plt.show()

    #print the size for each class in terminal
    print('\nClass distribution in dataset:')
    for class_name, class_size in class_size_df.iteritems():
        print(f'\t{class_name} -> {class_size}')


if __name__ == "__main__":
    #experiment how to properly do exploration for dataset1

    #first lets go with train dataset
    dataset_exploration(dataset_csv_path='new_dataset1/train/image_class_table.csv')

    #now lets go with test dataset
    dataset_exploration(dataset_csv_path='new_dataset1/test/image_class_table.csv')
