import matplotlib.pyplot as plt
import data_processing as dp
import model

lr = [0.0003]
batch_size = 32
epochs = 7

dp.Load()

for i in range(len(lr)):
    a = model.CreateModel(x_train=dp.x_train, y_train=dp.y_train, x_test=dp.x_test, y_test=dp.y_test,
                          layers=[300, 60, 50, 40, dp.no_of_classes],
                          batch_size=batch_size, lr=lr[i], epochs=epochs,
                          activation='relu', out_activation='softmax', opt='SGD')

plt.show()
