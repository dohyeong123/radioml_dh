import matplotlib.pyplot as plt
import numpy as np
import scipy


import os,random
#os.environ["KERAS_BACKEND"] = "theano"
os.environ["KERAS_BACKEND"] = "tensorflow"
#os.environ["THEANO_FLAGS"]  = "device=gpu%d"%(1)
import numpy as np
#import theano as th
#import theano.tensor as T
import keras
from keras.utils import np_utils
import keras.models as models
from keras.layers.core import Reshape,Dense,Dropout,Activation,Flatten
from keras.layers.noise import GaussianNoise
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D,Conv2D
from keras.regularizers import *
from keras.optimizers import adam
import matplotlib.pyplot as plt
import seaborn as sns
import cPickle, random, sys, keras
import numpy as np
import math


import keras.backend as K

class Cat():
    def __init__(self):
        print('init')
    def draw(self,url):
        
        self.file_path = url
        self.saved_I_data = []
        self.saved_Q_data = []
    
        for i, v in enumerate(self.file_path[:500]):    
            if i % 2 == 0:
                self.saved_I_data.append(v)    
            else:
                self.saved_Q_data.append(v)

        import matplotlib.pyplot as plt

        plt.scatter(self.saved_I_data,self.saved_Q_data)
        plt.grid(b=True)
        plt.show()


    def generate_BPSK(self, samp_len, mod_names, mod_type):
        self.mod_names_BPSK = mod_names
        self.samp_len = samp_len
        self.fromfile_path = '/root/capston_folder/file_/'+self.mod_names_BPSK+'.dat'

        self.f_BPSK = np.fromfile(self.fromfile_path, dtype=np.float32)
        self.mod_type = mod_type

        self.len_f = self.f_BPSK.shape

        self.pre_I = []
        self.pre_Q = []
        ## shaping (?,2,128)
        for i, v in enumerate(self.f_BPSK[self.samp_len*150:self.samp_len*250]):    
            if i % 2 == 0:
                self.pre_I.append(v)    
            else:
                self.pre_Q.append(v)

        self.pre_I = np.reshape(self.pre_I, (-1,self.samp_len))
        self.pre_Q = np.reshape(self.pre_Q, (-1,self.samp_len))
        
        ##IQ_data normalization
        self.isquared=np.power(self.pre_I, 2.0)
        self.qsquared=np.power(self.pre_Q, 2.0)
        self.energy=np.sqrt(self.isquared+self.qsquared)
        self.post_I=np.zeros((self.energy.shape[0], self.energy.shape[1]))
        self.post_Q=np.zeros((self.energy.shape[0], self.energy.shape[1]))
        self.total_energy=0
        for i in range(0, self.energy.shape[0]):
            for j in range (0, self.energy.shape[1]):
                self.total_energy=self.total_energy+self.energy[i][j]
            self.post_I[i]=self.pre_I[i]/self.total_energy
            self.post_Q[i]=self.pre_Q[i]/self.total_energy
            self.total_energy=0
        
        self.test_BPSK=[]
        self.test_BPSK=np.reshape(self.test_BPSK, (-1,2,self.samp_len))
        self.test_BPSK= np.hstack([self.post_I, self.post_Q])
        self.test_BPSK=np.reshape(self.test_BPSK, (-1,2,self.samp_len))
        self.size=(1, 2, self.test_BPSK.shape[2])
        self.data_zero=np.zeros(self.size)
        self.dict_BPSK={}
        
        ## make dictionary type dataset
        self.dict_BPSK[('QAM16')]=self.data_zero
        self.dict_BPSK[('BPSK')]=self.data_zero
        self.dict_BPSK[('8PSK')]=self.data_zero
        self.dict_BPSK[('CPFSK')]=self.data_zero
        self.dict_BPSK[('GFSK')]=self.data_zero
        self.dict_BPSK[('PAM4')]=self.data_zero
        self.dict_BPSK[('QPSK')]=self.data_zero
        self.dict_BPSK[('QAM64')]=self.data_zero
        self.dict_BPSK[('AM-DSB')]=self.data_zero
        self.dict_BPSK[('AM-SSB')]=self.data_zero
        self.dict_BPSK[('WBFM')]=self.data_zero
        self.dict_BPSK[(self.mod_type)]=self.test_BPSK



        self.Xd_BPSK=self.dict_BPSK
        self.mods_new = ["8PSK", "AM-DSB", "AM-SSB", "BPSK", "CPFSK", "GFSK", "PAM4", "QAM16", "QAM64", "QPSK", "WBFM"]
        self.X_BPSK = []
        self.lbl_BPSK = []
        for mod in self.mods_new:    
            self.X_BPSK.append(self.Xd_BPSK[(mod)])
            for i in range(self.Xd_BPSK[(mod)].shape[0]):
                self.lbl_BPSK.append((mod))
        self.X_BPSK = np.vstack(self.X_BPSK)
        np.random.seed(2017)
        self.n_examples = self.X_BPSK.shape[0]
        self.n_train = int(self.n_examples)
        self.test_idx_BPSK = np.random.choice(range(0,self.n_examples), size=self.n_train, replace=False)
        self.X_test_BPSK = self.X_BPSK[self.test_idx_BPSK]

        def to_onehot(yy):  
            yy1 = np.zeros([len(yy), max(yy)+1])
            yy1[np.arange(len(yy)),yy] = 1
            return yy1

        self.Y_test_BPSK= to_onehot(list(map(lambda x: self.mods_new.index(self.lbl_BPSK[x]), self.test_idx_BPSK)))
        self.in_shp = list(self.X_test_BPSK.shape[1:])



    def score_BPSK(self, batch_size):
        self.batch_size = batch_size
        self.score = self.pre_model.evaluate(self.X_test_BPSK, self.Y_test_BPSK, verbose=1, batch_size = self.batch_size)


    def load_model(self, url):
        from keras.models import load_model
        self.url = url
        self.pre_model =load_model(url)

    def plot_matrix_BPSK(self):
        def plot_confusion_matrix(cm, title='Confusion matrix', cmap=plt.cm.Blues, labels=[]):
            plt.imshow(cm, interpolation='nearest', cmap=cmap)
            plt.title(title)
            plt.colorbar()
            tick_marks = np.arange(len(labels))
            plt.xticks(tick_marks, labels, rotation=45)
            plt.yticks(tick_marks, labels)
            plt.tight_layout()
            plt.ylabel('True label')
            plt.xlabel('Predicted label')
            plt.show()

        self.test_Y_hat = self.pre_model.predict(self.X_test_BPSK, batch_size=400)
        self.conf = np.zeros([len(self.mods_new),len(self.mods_new)])
        self.confnorm = np.zeros([len(self.mods_new),len(self.mods_new)])
        for i in range(0,self.X_test_BPSK.shape[0]):
            j = list(self.Y_test_BPSK[i,:]).index(1)
            k = int(np.argmax(self.test_Y_hat[i,:]))
            self.conf[j,k] = self.conf[j,k] + 1

        for i in range(0,len(self.mods_new)):
            self.confnorm[i,:] = self.conf[i,:] / np.sum(self.conf[i,:])


        cnt = 0
        acc = 0
        max_value = 0
        for real_mod in self.mods_new:
            if real_mod == self.mod_type:
                for j in range(len(self.confnorm[0])):
                    if max_value < self.confnorm[cnt][j]:
                        max_value = self.confnorm[cnt][j]
                        acc=j
                break
            else:
                cnt = cnt + 1

        if max_value >= 0.1 :

            print("Real modulation : ",self.mod_type)
            print("Predict modulation : ", self.mods_new[acc])
            print("Accuracy : ", max_value)
            print("len : ",self.len_f)
            if cnt == acc:
                pass
            else:
                print("Real modulation : ",self.mod_type)
                print("Real modulation : ", self.mods_new[cnt])
                print("Accuracy : ", self.confnorm[cnt][cnt])

            
            ## express 11*11 confusion matrix
            plot_confusion_matrix(self.confnorm, labels=self.mods_new)
        else :
            print("Not Enough dataset!!")
            print("len : ",self.len_f)
            print("require dataset length : 32000")





