from tensorflow import keras
import matplotlib.pyplot as plt

plot_num = 3
subplt_num = 1


def CreateModel(x_train, y_train, x_test, y_test, layers, activation, out_activation, opt, epochs,
                batch_size=32, lr=0, momentum=0.9):
    model = keras.Sequential()
    # to add convolutional layer
    # model.add(keras.layers.Conv2D(62, (3, 3), activation=activation, input_shape=(28, 28, 1)))
    # model.add(keras.layers.MaxPool2D(2, 2))
    model.add(keras.layers.Flatten())
    for i in range(len(layers) - 1):
        model.add(keras.layers.Dense(layers[i], activation=activation))
    model.add(keras.layers.Dense(layers[len(layers) - 1], activation=out_activation))

    opt_str = opt
    if opt.lower() == 'sgd':
        opt = keras.optimizers.SGD(learning_rate=lr, momentum=momentum)

    model.compile(optimizer=opt,
                  loss=keras.losses.SparseCategoricalCrossentropy(),
                  metrics=['accuracy'])

    hist = model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.2)

    test_eval = model.evaluate(x_test, y_test)

    print(test_eval)

    PlotHist(hist, layers, activation, out_activation, opt_str, lr)

    # model.save('doodle5Model.h5')


def PlotSubPLots(hist, layers, activation, out_activation, opt, lr):
    global subplt_num
    plt.figure(2)
    plt.subplot(2, 3, subplt_num)
    plt.ylim([0, 1.1])
    plt.plot(hist.history['accuracy'])
    plt.plot(hist.history['val_accuracy'])
    plt.legend(['accuracy', 'val_accuracy'])
    fname = 'l_'
    fname += f'_lr_{lr}'
    plt.title(fname)
    # plt.savefig('./plot/' + fname)
    subplt_num += 1


def PlotHist(hist, layers, activation, out_activation, opt, lr):
    global plot_num
    plt.figure(plot_num)
    plt.ylim([0, 1.1])
    plt.plot(hist.history['accuracy'])
    plt.plot(hist.history['val_accuracy'])
    plt.legend(['accuracy', 'val_accuracy'])
    fname = 'l_'
    for i in range(len(layers)):
        fname += f'{layers[i]}' + '_'
    fname += '_ac_' + activation
    fname += '_outac_' + out_activation
    fname += '_op_' + opt
    fname += f'_lr_{lr}'
    plt.title(fname)
    # plt.savefig('./plot/' + fname)
    plot_num += 1

