# start2 파일 분석

* ## class 생성

가장 먼저 Cat이라는 class를 생성해준다.  
Cat이라는 이름을 지은 이유는 따로 없다.

```python
class Cat():
    def __init__(self):
        print('init')
```
참고로 앞으로 설명할 코드들은 모두 class Cat에 속해있는 것들이다.

* ## 파일 생성 코드

```python

    def generate(self, samp_len, mod_names, mod_type):
        self.mod_names = mod_names
        # test2.py 파일에서 modulation의 이름을 넘겨받는다.
        # 넘어오는 modulation이 무엇인지 인식을 하기 위해서 받아온다.
        self.samp_len = samp_len
        # shaping을 하기위한 것이다.
        # 128,256,512,1024, 등등으로 sample length를 지정할 수 있다.
        self.fromfile_path = '/root/capston_folder/file_/'+self.mod_names+'.dat'
        # 생성된 파일들의 저장 경로를 설정하는 부분이다.
        # 예를들어  처음에 bpsk를 생성하였다면 /root/capston_folder/file_안에 bpsk_1.dat파일이 저장되어있는 것을 알 수 있다..

        self.f_file = np.fromfile(self.fromfile_path, dtype=np.float32)
        # 위 코드는 해당 파일을 불러오는 코드로 file의 경로를 입력하도 data type을 설정해주어서 f_file 이라는 변수에 정보들을 저장하게 된다.
        self.mod_type = mod_type
        # 뒤에서 필요한 내용으로, modulation의 이름을 dictionary의 key값으로 설정해 두어서 다시 나오면 설명하기로 한다.
        self.len_f = self.f_file.shape


```

```python
        self.pre_I = []
        self.pre_Q = []

        for i, v in enumerate(self.f_file[self.samp_len*150:self.samp_len*250]):    
            if i % 2 == 0:
                self.pre_I.append(v)    
            else:
                self.pre_Q.append(v)
        # 위 코드는 data의 I값과 Q값을 나누기 위한 과정이다.
        # np.fromfile을 통해 데이터 값을 불러오게 되면, 데이터는 I와 Q순서로 들어오기 때문에 홀짝 알고리즘을 이용해서 분류를 하였다.
        
        self.pre_I = np.reshape(self.pre_I, (-1,self.samp_len))
        self.pre_Q = np.reshape(self.pre_Q, (-1,self.samp_len))
        # I값과 Q값을 각각 나누어서 나타낸다.


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
        # 데이터의 normalization과정을 나타낸다

        self.test=[]
        self.test=np.reshape(self.test, (-1,2,self.samp_len))
        # test값을 만들기 위해서 배열을 재배치 하는 과정이다.
        # 몇 개의 데이터 샘플이 들어올 지 모르기 때문에 -1로 지정해준다.
        self.test= np.hstack([self.post_I, self.post_Q])
        self.test=np.reshape(self.test, (-1,2,self.samp_len))
        self.size=(1, 2, self.test.shape[2])
        self.data_zero=np.zeros(self.size)
        self.dict={}
        
        ## make dictionary type dataset
        self.dict[('QAM16')]=self.data_zero
        self.dict[('BPSK')]=self.data_zero
        self.dict[('8PSK')]=self.data_zero
        self.dict[('CPFSK')]=self.data_zero
        self.dict[('GFSK')]=self.data_zero
        self.dict[('PAM4')]=self.data_zero
        self.dict[('QPSK')]=self.data_zero
        self.dict[('QAM64')]=self.data_zero
        self.dict[('AM-DSB')]=self.data_zero
        self.dict[('AM-SSB')]=self.data_zero
        self.dict[('WBFM')]=self.data_zero
        self.dict[(self.mod_type)]=self.test
        # 각 dictionary의 key값이 모두 대문자로 modulation의 이름을 설정했따.
        # 그렇기 때문에 mod_type을 위에서와 같이 설정해주었다.
``` 

마지막 dictionary부분은 confusion matrix를 표현하기 위해서 다음과 같이 나타냈다.


* ## test sample 생성 코드

```python
    def train_test(self):
        self.Xd=self.dict

        self.mods_new = ["8PSK", "AM-DSB", "AM-SSB", "BPSK", "CPFSK", "GFSK", "PAM4", "QAM16", "QAM64", "QPSK", "WBFM"]

        # modulation의 이름들을 설정해 준다.
        # 지금은 digital과 analog값 모두 들어가 있기 때문에 다음과 같이 설정한다.

        self.X = []
        self.lbl = []
        for mod in self.mods_new:    
            self.X.append(self.Xd[(mod)])
            for i in range(self.Xd[(mod)].shape[0]):
                self.lbl.append((mod))
        
        # X값에는 dictionary에 있는 value값을, lbl에는 key값을 넣어준다.

        self.X = np.vstack(self.X)
        np.random.seed(2017)
        self.n_examples = self.X.shape[0]
        self.n_train = int(self.n_examples)
        self.test_idx = np.random.choice(range(0,self.n_examples), size=self.n_train, replace=False)
        self.X_test = self.X[self.test_idx]

        def to_onehot(yy):  
            yy1 = np.zeros([len(yy), max(yy)+1])
            yy1[np.arange(len(yy)),yy] = 1
            return yy1
        # Y_test의 값을 onehot 인코딩 방식을 이용해서 지정한다.
        self.Y_test= to_onehot(list(map(lambda x: self.mods_new.index(self.lbl[x]), self.test_idx)))
        self.in_shp = list(self.X_test.shape[1:])
```

* ## CNN model 불러오기
  
  ```python
    def load_model(self, url):
        from keras.models import load_model
        self.url = url
        self.pre_model =load_model(url)     
  ```

  이미 존재하는 model을 불러와서 사용하기 위해서 생성된 코드이다.

  radioML을 기반으로 만든 CNN 모델 중 정확도가 높다고 판단되는 모델을 가져왔다.

    참고 사이트 :  
  **<a target=_blank>https://github.com/RobinChenRichmond/RF-Signal-Model/</a>**

* ##  평균적인 정확도 나타내기
  ```python
    def score(self, batch_size):
        self.batch_size = batch_size
        self.score = self.pre_model.evaluate(self.X_test, self.Y_test, verbose=1, batch_size = self.batch_size)
  ```
batch size의 크기를 설정해서 load한 model을 이용해서 X_test와 Y_test의 값을 통해 테스트를 하고 그 결과값으로 정확도를 나타낼 수 있다.

* ## matrix 그리기

confusion matrix를 그리기 위한 코드이다.

```python
    def plot_matrix(self):
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

```
위 코드는 matrix를 짜는 코드인데, 중요한 부분이 아니므로 따로 코드설명을 하지는 않겠다.


```python
        cnt = 0
        acc = 0
        max_value = 0
        # cnt는 count, acc는 정확도, max_value는 acc의 최대값을 나타낸다.

        for real_mod in self.mods_new:
            if real_mod == self.mod_type:
        #mods_new에서 현재 modulation type과 동일한 것을 찾기 위한 과정이다.
                for j in range(len(self.confnorm[0])):
                    if max_value < self.confnorm[cnt][j]:
                        max_value = self.confnorm[cnt][j]
                        acc=j
        # acc의 정확도를 찾아내기 위한 과정이다.
                break
            else:
                cnt = cnt + 1

        if max_value >= 0.1 :

            print("Real modulation : ",self.mod_type)
            print("Predict modulation : ", self.mods_new[acc])
            print("Accuracy : ", max_value)
            print("len : ",self.len_f)

        # 정확도가 가장 높은 modulation이 True modulation과 동일하다면 위 코드만 실행한다.
            if cnt == acc:
                pass
            else:
                print("Real modulation : ",self.mod_type)
                print("Real modulation : ", self.mods_new[cnt])
                print("Accuracy : ", self.confnorm[cnt][cnt])

        # 정확도가 가장 높은 modulation이 True modulation과 동일하지 않다면, True modulation이 동일한 modulation을 예측할 acc를 밑에 나타내준다.
            
            ## express 11*11 confusion matrix
            plot_confusion_matrix(self.confnorm, labels=self.mods_new)
        else :
            print("Not Enough dataset!!")
            print("len : ",self.len_f)
            print("require dataset length : 32000")

        # 데이터의 값이 충분하지 않다면 다음과 같은 문구가 뜨도록 한다.
        # 에러와 같은 상황이라고 생각한다.

```

