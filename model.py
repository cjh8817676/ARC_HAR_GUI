import tensorflow as tf
from keras import optimizers
# model
import model
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Dropout
from keras.layers import TimeDistributed
from keras.layers import Conv2D, MaxPooling2D,GRU,BatchNormalization
from tensorflow.keras.utils import to_categorical
from matplotlib import pyplot
import keras
epochs = 50
window_size = 50



# GRU inputs 3D Tensor : [batch, timesteps, feature]
class HalNet(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.num_classes = 6
        self.n_timesteps_2 = window_size
    #---------------model1----------------#
        self.model1 = Sequential()
        self.model1.add(Conv2D(filters=16, kernel_size=(3,3), activation='relu', input_shape=(self.n_timesteps_2,3,1)))
        self.model1.add(Conv2D(filters=32, kernel_size=(3,1), activation='relu'))
        self.model1.add(Dropout(0.5))
        self.model1.add(MaxPooling2D(pool_size=(2,1)))
        self.model1.add(Flatten())
        self.model1.add(tf.keras.layers.Reshape((1,self.model1.output.shape[1])))
        self.model1.add(GRU(32, return_sequences=True,unroll=True))
    #---------------model2----------------#
        self.model2 = Sequential()  
        self.model2.add(Conv2D(filters=16, kernel_size=(5,3), activation='relu', input_shape=(self.n_timesteps_2,3,1)))
        self.model2.add(Conv2D(filters=32, kernel_size=(5,1), activation='relu'))
        self.model2.add(Dropout(0.5))
        self.model2.add(MaxPooling2D(pool_size=(2,1)))
        self.model2.add(Flatten())
        self.model2.add(tf.keras.layers.Reshape((1,self.model2.output.shape[1])))
        self.model2.add(GRU(32, return_sequences=True,unroll=True))
    
    #---------------model3----------------#
        self.model3 = Sequential() 
        self.model3.add(Conv2D(filters=16, kernel_size=(11,3), activation='relu', input_shape=(self.n_timesteps_2,3,1)))
        self.model3.add(Conv2D(filters=32, kernel_size=(11,1), activation='relu'))
        self.model3.add(Dropout(0.5))
        self.model3.add(MaxPooling2D(pool_size=(2,1)))
        self.model3.add(Flatten())
        self.model3.add(tf.keras.layers.Reshape((1,self.model3.output.shape[1])))
        self.model3.add(GRU(32, return_sequences=True,unroll=True))
        #self.model3.summary()
        
    #--------------model4----------------  
        self.model4 = Sequential() 
        self.model4.add(Flatten()) 
        self.model4.add(Dense(32, activation='relu'))
        self.model4.add(BatchNormalization())
        self.model4.add(Dense(self.num_classes, activation='softmax'))
        # self.model4.summary()
       
        
    def call(self, inputs):
        # s0, s1, s2 = tf.split(inputs, num_or_size_splits=3, axis=2)
        # print(s0.shape)
        out_up = self.model1(inputs)
        out_down = self.model2(inputs)
        out_middle =  self.model3(inputs)
        print(out_up.shape,out_down.shape,out_middle.shape)
        
        out_temp = tf.keras.layers.Concatenate(axis=1)([out_up,out_down,out_middle])
        print(out_temp.shape)
        out = self.model4(out_temp)

        return out
    def model_save(self):
        self.model
        
model = HalNet()
model.build((None,window_size,3,1))

#sgd = tf.keras.optimizers.SGD(lr=0.0001, clipvalue=0.5)
model.compile(loss='categorical_crossentropy', optimizer="Adam", metrics=['accuracy'])
model.summary()