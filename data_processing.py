import numpy as np
from image import TransformImage

no_of_classes = 5
max_images = 15000
random_copies = 5

x_train, y_train, x_test, y_test = [], [], [], []


def SaveData(x, y):
    global no_of_classes
    np.save(f'./randomData/X_{no_of_classes}_{len(x)}_{random_copies}', x)
    np.save(f'./randomData/Y_{no_of_classes}_{len(x)}_{random_copies}', y)


def Save():
    data_name = [
        'cat', 'helicopter', 'octopus', 'popsicle', 'tractor'
    ]

    # making file_names
    file_name = []
    for i in range(no_of_classes):
        file_name.append('./data/full_numpy_bitmap_' + data_name[i] + '.npy')

    # load file 0 to data_name
    list_images = np.load(file_name[0])

    X = list_images[:max_images]
    Y = np.zeros(shape=(max_images, 1))

    print('loading data: ', 0)

    # load rest of files to data_name
    for i in range(1, no_of_classes):
        print('loading data: ', i)
        list_images = np.load(file_name[i])
        X = np.append(X, list_images[:max_images], axis=0)
        Y = np.append(Y, np.zeros(shape=(max_images, 1)) + i, axis=0)

    X = np.reshape(X, newshape=(max_images * no_of_classes, 28, 28))
    X_rand = []
    Y_rand = []
    count = max_images + 1
    lab = -1

    # print(X.shape, Y.shape)

    for k in range(len(X)):
        if count > max_images:
            count = 0
            lab += 1
            print(f'randomizing data: {lab}')
        for i in range(random_copies):
            x_list = X[k].tolist()
            X_rand.append(TransformImage(x_list))
            Y_rand.append(lab)
        count += 1

    X = np.append(X, X_rand, axis=0)
    Y_rand_np = np.reshape(np.array(Y_rand), newshape=(len(Y_rand), 1))
    Y = np.append(Y, Y_rand_np, axis=0)

    np.random.seed(1)
    np.random.shuffle(X)
    np.random.seed(1)
    np.random.shuffle(Y)

    SaveData(X, Y)


def Load():
    global x_train, y_train, x_test, y_test

    print('loading data...')

    X = np.load(f'./randomData/X_{no_of_classes}_{no_of_classes*max_images*(random_copies + 1)}_{random_copies}.npy')

    Y = np.load(f'./randomData/Y_{no_of_classes}_{no_of_classes*max_images*(random_copies + 1)}_{random_copies}.npy')

    print('loading complete!')

    training_num = (len(X) * 4) // 5

    x_train = X[:training_num]
    x_test = X[training_num:]
    y_train = Y[:training_num]
    y_test = Y[training_num:]


# Load()
# Save()
