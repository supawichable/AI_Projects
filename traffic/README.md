Different numbers of layers and the types of layers are tested using this model and the results are as follows. 

- The increase of number of convolutional layers could increase accuracy but also dramatically increase the loss produced by the model. At one point, the increase of number of layers couls also decrease the accuracy of the model.

- The increase of number of pooling layers could increase the accuracy of the model as well as decrease the loss value. However, at one point it could decrease the model's accuracy.

- The increase of number of filters could slightly bring up the model's accuracy but it could at the same time dramatically increase the model's loss value.

- The increase of size of filters is a other way to increase model's accuracy but could also result in the increase of loss value.

- The increase of pool size is one effective way to both increase model accuracy and decrease loss value. But once go beyond an appropriate threshold, it could produce worse result.

- The increase of number of hidden values could dramatically increase model's accuracy and at the same time decrease loss value. Also, once goes beyond appropriate number of layers it could produce worse results for both aspects.

- The increse of size of hidden layers could both increase the accuracy and decrease loss value as for result investigated in this experiment.

- Different dropout values also affect the result of the model. In this case, the model produces best accuracy when dropout = 0.3 but best loss value when dropout = 0.25 .

The set of parameters that produces best value in this experiement is as follows.

Convolutional layer(s): 1
Pooling layer(s): 1
Hidden layer(s): 2
Filter number: 32
Filter size: (3, 3)
Pool size: (2, 2)
Hidden layer's size: 512
Dropout: 0.25
-----
Loss: 1.2006
Accuracy: 0.9434

------------

All Experimentation Results

1. Increase number of convolutional layers

Control Experiment:

Convolutional layer(s): 1
Pooling layer(s): 1
Hidden layer(s): 1
Filter number: 32
Filter size: (3, 3)
Pool size: (2, 2)
Hidden layer's size: 128
Dropout: 0.5
-----
Loss: 1270.8444
Accuracy: 0.4753
------------
Experiment 1:

Convolutional layer(s): 2
Pooling layer(s): 1
Hidden layer(s): 1
Filter number: 32
Filter size: (3, 3)
Pool size: (2, 2)
Hidden layer's size: 128
Dropout: 0.5
-----
Loss: 152748.1875
Accuracy: 0.7782
------------
Experiment 2:

Convolutional layer(s): 4
Pooling layer(s): 1
Hidden layer(s): 1
Filter number: 32
Filter size: (3, 3)
Pool size: (2, 2)
Hidden layer's size: 128
Dropout: 0.5
-----
Loss: 29381115904.0000
Accuracy: 0.5419
------------

2. Increase number of pooling layers

Control Experiment:

Convolutional layer(s): 1
Pooling layer(s): 1
Hidden layer(s): 1
Filter number: 32
Filter size: (3, 3)
Pool size: (2, 2)
Hidden layer's size: 128
Dropout: 0.5
-----
Loss: 1270.8444
Accuracy: 0.4753
------------
Experiment 1:

Convolutional layer(s): 1
Pooling layer(s): 2
Hidden layer(s): 1
Filter number: 32
Filter size: (3, 3)
Pool size: (2, 2)
Hidden layer's size: 128
Dropout: 0.5
-----
Loss: 189.3486
Accuracy: 0.5433
------------
Experiment 2:

Convolutional layer(s): 1
Pooling layer(s): 3
Hidden layer(s): 1
Filter number: 32
Filter size: (3, 3)
Pool size: (2, 2)
Hidden layer's size: 128
Dropout: 0.5
-----
Loss: 9.3829
Accuracy:0.6522
------------
Experiment 4:

Convolutional layer(s): 1
Pooling layer(s): 4
Hidden layer(s): 1
Filter number: 32
Filter size: (3, 3)
Pool size: (2, 2)
Hidden layer's size: 128
Dropout: 0.5
-----
Loss: 2.2434
Accuracy:0.4154
------------

3. Increase number of filters

Control Experiment:

Convolutional layer(s): 1
Pooling layer(s): 1
Hidden layer(s): 1
Filter number: 32
Filter size: (3, 3)
Pool size: (2, 2)
Hidden layer's size: 128
Dropout: 0.5
-----
Loss: 1270.8444
Accuracy: 0.4753
------------
Experiment 1:

Convolutional layer(s): 1
Pooling layer(s): 1
Hidden layer(s): 1
Filter number: 64
Filter size: (3, 3)
Pool size: (2, 2)
Hidden layer's size: 128
Dropout: 0.5
-----
Loss: 1978.9633
Accuracy: 0.6274
------------
Experiment 2:

Convolutional layer(s): 1
Pooling layer(s): 1
Hidden layer(s): 1
Filter number: 128
Filter size: (3, 3)
Pool size: (2, 2)
Hidden layer's size: 128
Dropout: 0.5
-----
Loss: 2636.2366
Accuracy: 0.6631

4. Increase sizes of filters

Control Experiment:

Convolutional layer(s): 1
Pooling layer(s): 1
Hidden layer(s): 1
Filter number: 32
Filter size: (3, 3)
Pool size: (2, 2)
Hidden layer's size: 128
Dropout: 0.5
-----
Loss: 1270.8444
Accuracy: 0.4753
------------
Experiment 1:

Convolutional layer(s): 1
Pooling layer(s): 1
Hidden layer(s): 1
Filter number: 32
Filter size: (4, 4)
Pool size: (2, 2)
Hidden layer's size: 128
Dropout: 0.5
-----
Loss: 1472.8306
Accuracy: 0.6931
------------
Experiment 2:

Convolutional layer(s): 1
Pooling layer(s): 1
Hidden layer(s): 1
Filter number: 32
Filter size: (5, 5)
Pool size: (2, 2)
Hidden layer's size: 128
Dropout: 0.5
-----
Loss: 1054.8196
Accuracy: 0.7279
------------

5. Increase pool sizes of pooling layers:

Control Experiment:

Convolutional layer(s): 1
Pooling layer(s): 1
Hidden layer(s): 1
Filter number: 32
Filter size: (3, 3)
Pool size: (2, 2)
Hidden layer's size: 128
Dropout: 0.5
-----
Loss: 1270.8444
Accuracy: 0.4753
------------
Experiment 1:

Convolutional layer(s): 1
Pooling layer(s): 1
Hidden layer(s): 1
Filter number: 32
Filter size: (3, 3)
Pool size: (3, 3)
Hidden layer's size: 128
Dropout: 0.5
-----
Loss: 384.2010
Accuracy: 0.5676
------------
Experiment 1:

Convolutional layer(s): 1
Pooling layer(s): 1
Hidden layer(s): 1
Filter number: 32
Filter size: (3, 3)
Pool size: (4, 4)
Hidden layer's size: 128
Dropout: 0.5
-----
Loss: 175.5518
Accuracy: 0.4860
------------

6. Increase number of hidden layers

Control Experiment:

Convolutional layer(s): 1
Pooling layer(s): 1
Hidden layer(s): 1
Filter number: 32
Filter size: (3, 3)
Pool size: (2, 2)
Hidden layer's size: 128
Dropout: 0.5
-----
Loss: 1270.8444
Accuracy: 0.4753
------------
Experiment 1:

Convolutional layer(s): 1
Pooling layer(s): 1
Hidden layer(s): 2
Filter number: 32
Filter size: (3, 3)
Pool size: (2, 2)
Hidden layer's size: 128
Dropout: 0.5
-----
Loss: 398.7784
Accuracy: 0.8929
------------
Experiment 2:

Convolutional layer(s): 1
Pooling layer(s): 1
Hidden layer(s): 4
Filter number: 32
Filter size: (3, 3)
Pool size: (2, 2)
Hidden layer's size: 128
Dropout: 0.5
-----
Loss: 30076.6523
Accuracy: 0.8570
------------

7. Increase sizes of hidden layers 

Control Experiment:

Convolutional layer(s): 1
Pooling layer(s): 1
Hidden layer(s): 1
Filter number: 32
Filter size: (3, 3)
Pool size: (2, 2)
Hidden layer's size: 128
Dropout: 0.5
-----
Loss: 1270.8444
Accuracy: 0.4753
------------
Experiment 1:

Convolutional layer(s): 1
Pooling layer(s): 1
Hidden layer(s): 2
Filter number: 32
Filter size: (2, 2)
Pool size: (2, 2)
Hidden layer's size: 256
Dropout: 0.5
-----
Loss: 571.6905
Accuracy: 0.8098
------------
Experiment 2:

Convolutional layer(s): 1
Pooling layer(s): 1
Hidden layer(s): 4
Filter number: 32
Filter size: (2, 2)
Pool size: (2, 2)
Hidden layer's size: 512
Dropout: 0.5
-----
Loss: 214.7848
Accuracy: 0.9352
------------
8. Different dropout values

Control Experiment:

Convolutional layer(s): 1
Pooling layer(s): 1
Hidden layer(s): 1
Filter number: 32
Filter size: (3, 3)
Pool size: (2, 2)
Hidden layer's size: 128
Dropout: 0.5
-----
Loss: 1270.8444
Accuracy: 0.4753
------------
Experiment 1:

Convolutional layer(s): 1
Pooling layer(s): 1
Hidden layer(s): 1
Filter number: 32
Filter size: (2, 2)
Pool size: (2, 2)
Hidden layer's size: 256
Dropout: 0.25
-----
Loss: 2.6823
Accuracy: 0.9291
------------
Experiment 2:

Convolutional layer(s): 1
Pooling layer(s): 1
Hidden layer(s): 1
Filter number: 32
Filter size: (2, 2)
Pool size: (2, 2)
Hidden layer's size: 512
Dropout: 0.3
-----
Loss: 5.6687
Accuracy: 0.9312
------------
Experiment 3:

Convolutional layer(s): 1
Pooling layer(s): 1
Hidden layer(s): 1
Filter number: 32
Filter size: (2, 2)
Pool size: (2, 2)
Hidden layer's size: 512
Dropout: 0.75
-----
Loss: 5770.2446
Accuracy: 0.7343
------------