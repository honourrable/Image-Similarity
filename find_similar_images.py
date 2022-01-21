from PIL import Image  # To read image files
import numpy  # To store arrays
import os  # To get all files inside a given path (folder) by using os.path.join()


# Constant values
DATADIR = "C:/Users/Onur/PycharmProjects/ImageSimilarity/dataset"
CATEGORIES = ["elephant", "flamingo", "kangaroo", "Leopards", "octopus", "sea_horse"]


def read_prepare_images(image_limit):  # Reading images with category information and loading them to program
    # The list to store all images with the corresponding category
    datasets = []
    # The variable to count number of all images
    number_of_images = 0
    # Counter variable to count skipped grayscale images
    counter_grayscale_images = 0

    for category in CATEGORIES:
        # The list to store images of specific category
        images = []
        # Counter variable to check if it reached image number limit
        counter_image_limit = 0

        path = os.path.join(DATADIR, category)

        for image_file in os.listdir(path):
            if counter_image_limit == image_limit:
                break
            else:
                try:
                    image = Image.open(os.path.join(path, image_file))
                    array = numpy.asarray(image)

                    # Checking the image
                    if len(array.shape) < 3:
                        # If it is grayscale skipping that image
                        counter_grayscale_images += 1

                    else:
                        images.append(array)

                        number_of_images += 1
                        counter_image_limit += 1

                except Exception as e:
                    print(e)

        datasets.append(images)

    # To show the most similar image files' name, this includes file name and type
    file_name_style = os.listdir(os.path.join(DATADIR, CATEGORIES[0]))[0]

    print(">>> Info:", counter_grayscale_images, "grayscale image(s) skipped")
    print("\nImage number in each category :", end=" ")
    for images in datasets:
        print(len(images), end=" ")

    print("\nTotal number of images        :", number_of_images, "\n")

    return datasets, file_name_style


def create_histograms(image):
    # Creating (R,G,B) histograms
    r = []
    g = []
    b = []

    for pixels in image:
        for pixel in pixels:
            r.append(pixel[0])
            g.append(pixel[1])
            b.append(pixel[2])

    total_pixel = len(r)

    r_histogram = [0.0] * 256
    g_histogram = [0.0] * 256
    b_histogram = [0.0] * 256

    for value in r:
        r_histogram[value] += 1
    for value in g:
        g_histogram[value] += 1
    for value in b:
        b_histogram[value] += 1

    # Normalizing to range of (0,1)
    for value in range(256):
        r_histogram[value] = r_histogram[value] / total_pixel
        g_histogram[value] = g_histogram[value] / total_pixel
        b_histogram[value] = b_histogram[value] / total_pixel

    # Creating H histogram by using (R,G,B) values
    hue = []
    for pixel in image[0]:
        r_val = pixel[0]
        g_val = pixel[1]
        b_val = pixel[2]

        h_val = convert_rgb_to_h(r_val, g_val, b_val)
        hue.append(h_val)

    # The range is [0,360], 361 different values
    h_histogram = [0.0] * 361

    for value in hue:
        h_histogram[int(value)] += 1

    # Normalizing to range of (0,1), 360 is the up limit, 361 is not included in range() expression
    for value in range(361):
        h_histogram[value] = h_histogram[value] / total_pixel

    histograms = [r_histogram, g_histogram, b_histogram, h_histogram]

    return histograms


def convert_rgb_to_h(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0

    max_value = max(r, g, b)
    min_value = min(r, g, b)
    df = max_value-min_value

    # In HSV color space, it's required only H information, thus only H is calculated
    h = None
    if max_value == min_value:
        h = 0
    elif max_value == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif max_value == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif max_value == b:
        h = (60 * ((r-g)/df) + 240) % 360

    return h


def find_distance(test_histogram, train_histogram):
    h_distance = 0
    rgb_distance = [0] * 3

    for colours in range(4):
        # Finding distance of R,G,B histograms
        if colours < 3:
            summ = 0
            for i in range(256):
                summ = summ + (test_histogram[colours][i] - train_histogram[colours][i]) ** 2
            distance = summ ** (1/2)

            rgb_distance[colours] = distance

        # Finding distance of H histograms
        else:
            summ = 0
            for i in range(361):
                summ = summ + (test_histogram[colours][i] - train_histogram[colours][i]) ** 2
            h_distance = summ ** (1 / 2)

    # Applying Euclidean distance again for distance results of R,G,B channels to have an average distance
    rgb_avg_distance = (rgb_distance[0] ** 2 + rgb_distance[1] ** 2 + rgb_distance[2] ** 2) ** (1/2)

    return rgb_avg_distance, h_distance


def selection_sort(array, similar_image_number):
    array_indices = []

    # Sorting the array for desired "similar_image_number" times, instead of sorting all
    for i in range(similar_image_number):
        min_idx = i
        for j in range(i + 1, len(array)):
            if array[min_idx] > array[j]:
                min_idx = j

        # Swaping the min item with the first element
        array[i], array[min_idx] = array[min_idx], array[i]
        array_indices.append(min_idx)

    return array[:5], array_indices


def main():
    image_limit = int(input("\nPlease enter total image number for train and test: "))
    train_image_number = int(input("Please enter train images number: "))
    similar_image_number = int(input("Please enter most similar images number: "))
    print("")
    datasets, file_name_style = read_prepare_images(image_limit)

    # Creating histograms of the first "train_image_number" images
    train_image_histograms = []
    test_image_histograms = []
    for images in datasets:
        for image_index in range(len(images)):
            # Creating histogram of train images
            if image_index < train_image_number:
                histogram = create_histograms(images[image_index])
                train_image_histograms.append(histogram)

            # Creating histogram of test images
            else:
                histogram = create_histograms(images[image_index])
                test_image_histograms.append(histogram)

    print(len(train_image_histograms), "image histograms created for training")
    print(len(test_image_histograms), "image histograms created for test")

    print("\n\nFinding most similar", similar_image_number, "images")
    for test_index, test_histogram in enumerate(test_image_histograms):
        rgb_distances = []
        h_distances = []

        for train_index, train_histogram in enumerate(train_image_histograms):
            rgb_distance, h_distance = find_distance(test_histogram, train_histogram)

            rgb_distances.append(rgb_distance)
            h_distances.append(h_distance)

        rgb_most_similar, rgb_most_similar_indices = selection_sort(rgb_distances, similar_image_number)
        h_most_similar, h_most_similar_indices = selection_sort(h_distances, similar_image_number)

        # Finding the image file's in directory with index
        test_category = int(test_index / (image_limit-train_image_number))
        test_image_order = int(test_index % (image_limit-train_image_number))

        # Folder and file info is already extracted, lines below are written for this dataset specifically
        file_name = file_name_style.split('.')[0].split('0')[0]
        file_type = file_name_style.split('.')[1]

        print("\n\nTest image ", test_index + 1, " - ", CATEGORIES[test_category],
              '/', file_name, test_image_order + 1 + train_image_number, '.', file_type, '\n', sep='')

        # Showing the distances and most similar images' indices, commented not to complicate console output
        # print("Min distances (RGB):", ["%.4f" % val for val in rgb_most_similar],
        #       "most similar images:", rgb_most_similar_indices)
        # print("Min distances (Hue):", ["%.4f" % val for val in h_most_similar],
        #       "most similar images:", h_most_similar_indices)

        print("With RGB Histogram: ", end=" ")
        for i in range(5):
            rgb_category = int((rgb_most_similar_indices[i]) / train_image_number)
            rgb_image_order = int((rgb_most_similar_indices[i]) % train_image_number)

            print(CATEGORIES[rgb_category], '/', file_name, rgb_image_order + 1, '.', file_type, sep='', end=" ")

        print("\nWith Hue Histogram: ", end=" ")
        for i in range(5):
            h_category = int((h_most_similar_indices[i]) / train_image_number)
            h_image_order = int((h_most_similar_indices[i]) % train_image_number)

            print(CATEGORIES[h_category], '/', file_name, h_image_order + 1, '.', file_type, sep='', end=" ")

    return


if __name__ == '__main__':
    main()
