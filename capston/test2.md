# test2 파일 분석

* ## 전역변수 지정 생성

```python
class random_pskmod_constel(gr.top_block, Qt.QWidget):
    bpsk = 0
    qpsk = 0
    psk8 = 0
    pam4 = 0
    qam16 = 0
    qam64 = 0
    gfsk = 0
    cpfsk = 0
    fm = 0
    am = 0
    amssb = 0

    # 각 modulation의 변수를 0으로 지정해준 이유는 파일이 생성될 때마다 다른번호를 설정해주기 위해서이다.
    # 예를 들면 bpsk가 만들어지면 bpsk_1, bpsk_2, ...순서로 만들기 위해 지정해 놓은 변수들이다.
    cnt = 0
    # 전체적으로 버튼이 얼마나 눌렸는지를 위한 변수이다
    # 이 변수는 마지막에 각각의 데이터들에 대한 정확도를 확인하기 위해 나타낸 것이다.

    file_path = '/root/capston_folder/file'

    #file_path도 처음에 설정한 이유는 처음에 설정하지 않으면 default값이 지정되지 않아 오류가 생기기 때문에 설정을 해주었다.

    blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, file_path, False)

    # blocks_file_sink_0는 value들이 담길 변수를 나타내는 것이다
    # 저장통 이라고 생각하면 된다

    dic = {}

    # dic은 dictinary를 나타내는 것으로, 다음과 같아 나타난다
    # {bpsk_1.dat :'1', 'qpsk_1' : '2', ...}
    # 즉, 각 modulation의 순서를 나타내는, cnt의 값을 나타내는 것으로 이해 할 수 있다.

    mod_dic = {}
    # 해당 dictinary는 dic과 비슷한데, value값으로 'BPSK','QPSK'등이 들어간다
    # 그 이유는 해당 value값을 Cat() class를 이용하기 위함이다.
    # 다음 내용은 cat class를 불러오는 곳에서 자세하게 설명한다.
```
<br>

* ## Mapper 설정

```python
        self.QPSK = mapper.mapper(mapper.QPSK, ([0,1,3,2]))
        self.BPSK = mapper.mapper(mapper.BPSK, ([0,1]))
        self.PSK8 = mapper.mapper(mapper.PSK8, ([0,1,3,2,7,6,4,5]))
        self.PAM4 = mapper.mapper(mapper.PAM4, ([0,1,3,2]))
        self.QAM16 = mapper.mapper(mapper.QAM16, ([2,6,14,10,3,7,15,11,1,5,13,9,0,4,12,8]))
        self.QAM64 = mapper.mapper(mapper.QAM64, ([0,32,8,40,3,35,11,43,
             48,16,56,24,51,19,59,27,
            12,44,4,36,15,47,7,39,
            60,28,52,20,63,31,55,23,
            2,34,10,42,1,33,9,41,
            50,18,58,26,49,17,57,25,
            14,46,6,38,13,45,5,37,
            62,30,54,22,61,29,53,21]))
```

mapper를 설정하는 부분이다.

analog는 아직 정확히 구현하는 방법을 알지 못하기 때문에 digital만 구현을 해놓았다.

* ## Block 설정

```python
        self._mod_options = (0, 1, 2, 3, 4, 5, )
        self._mod_labels = ('BPSK', 'QPSK','PSK8','PAM4','QAM16','QAM64',)

        self.selector = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=6,
        	num_outputs=1,
        	input_index=mod,
        	output_index=0,
        )
```
앞의 capston.md와 비슷한 부분이 많기 때문에 동일한 부분은 생략한다.



* ## set_mod 설정

### 이 부분은 가장 중요한 부분이라 생각해서 자세하게 설명해농도록 하겠다.

```python
    def set_mod(self, mod):
        self.mod = mod
        print(self.mod)
        self._mod_callback(self.mod)
        self.selector.set_input_index(int(self.mod))
```
가장 먼저 capston.md에서 만들었던 grc파일의 python file을 보게되면 기본적으로 다음과 같은 코드가 생성됨을 알 수 있다.  
이 코드는 button이 클릭될 때마다 변화를 감시하여 callback함수를 호출하고 selector함수의 input_index를 변경하는 부분으로 이해 할 수 있다.  

이에 실시간으로 변화하는 신호들의 modulation의 변화를 감지하기 위해서 다음과 같은 코드를 추가해 주었다.

```python 
        if self.mod == 0:
            self.bpsk +=1
            self.file_path = 'bpsk_{}.dat'.format(self.bpsk)
            self.title = 'bpsk_{}'.format(self.bpsk)
            self.dic[self.title] = self.cnt
            mod_title = 'BPSK'
            self.mod_dic[self.title] = mod_title
```

if문 하나로 구성되었지만 elif까지 한번에 모두 작성하면 길어지므로 다음과 같이 하나의 조건문으로 설명을 하겠다.  
아래의 코드들은 거의 비슷하므로 동일하게 생각하면 된다.

* self.mod  
  이 변수는 radio button에서 label의 option값이라고 생각하면 된다. 
  즉, bpsk는 0번, qpsk 는1번 ...이라고 생각하면 쉽게 이해 가능하다.

* self.bpsk +=1  
   이 변수는 전역변수인 bpsk의 값을 1 증가시키는 코드이다.
   bpsk가 여러번 들어올 수 있으므로 그에 대한 다양한 파일을 만들기 위해 지정해주었다.  

* self.file_path = 'bpsk_{}.dat'.format(self.bpsk)  
  file의 이름을 지정하기 위한 코드이다.  
  format형식으로 다음과 같이 설정을 하게 되면 {}안에 format에 들어있는 값들이 들어가게 된다.
  여기서는 self.bpsk이므로 위 코드는 bpsk의 값을 1씩 증가된 값을 삽입하게 된다.

* self.title = 'bpsk_{}'.format(self.bpsk)
  self.title변수는 bpsk의 순서를 나타내기 위한 함수이다

* self.dic[self.title] = self.cnt
  이는 예를 들어서 설명을 하겠다.  
  버튼을 bpsk, qpsk, bpsk 순서로 눌르게 된다면 다음과 같이 dic이 형성된다.  
  dic = {'bpsk_1' : '1', 'qpsk_1' : '2', 'bpsk_3' : '3'}

* mod_title = 'BPSK'  
  이 부분은 각 modulation의 이름을 설정하기 위한 부분이다.

* self.mod_dic[self.title] = mod_title
  mod_dic은 dic의 형태와 비슷한데, value값에 int대신 str이 들어간다.  
  dic = {'bpsk_1' : 'BPSK', 'qpsk_1' : 'QPSK', 'bpsk_3' : 'BPSK'}

밑의 코드들은 다음과 같다.  

```python
        if self.mod == 0:
            self.bpsk +=1
            self.file_path = 'bpsk_{}.dat'.format(self.bpsk)
            self.title = 'bpsk_{}'.format(self.bpsk)
            self.dic[self.title] = self.cnt
            mod_title = 'BPSK'
            self.mod_dic[self.title] = mod_title
        
        elif self.mod == 1:
            self.qpsk +=1
            self.file_path = 'qpsk_{}.dat'.format(self.qpsk)
            title = 'qpsk_{}'.format(self.qpsk)
            self.dic[title] = self.cnt
            mod_title = 'QPSK'
            self.mod_dic[title] = mod_title

        elif self.mod == 2:
            self.psk8 +=1
            self.file_path = 'psk8_{}.dat'.format(self.psk8)
            title = 'psk8_{}'.format(self.psk8)
            self.dic[title] = self.cnt
            mod_title = '8PSK'
            self.mod_dic[title] = mod_title

        elif self.mod == 3:
            self.pam4 +=1
            self.file_path = 'pam4_{}.dat'.format(self.pam4)
            title = 'pam4_{}'.format(self.pam4)
            self.dic[title] = self.cnt
            mod_title = 'PAM4'
            self.mod_dic[title] = mod_title

        elif self.mod == 4:
            self.qam16 +=1
            self.file_path = 'qam16_{}.dat'.format(self.qam16)
            title = 'qam16_{}'.format(self.qam16)
            self.dic[title] = self.cnt
            mod_title = 'QAM16'
            self.mod_dic[title] = mod_title

        elif self.mod == 5:
            self.qam64 +=1
            self.file_path = 'qam64_{}.dat'.format(self.qam64)
            title = 'qam64_{}'.format(self.qam64)
            self.dic[title] = self.cnt
            mod_title = 'QAM64'
            self.mod_dic[title] = mod_title
```


```python
    self.file_path = '/root/capston_folder/file_/' + self.file_path
    # 각각의 file_path를 설정하는 부분이다./
    self.disconnect((self.channels_dynamic_channel_model_0, 0), (self.blocks_file_sink_0, 0))


    self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1,self.file_path, False)
    self.blocks_file_sink_0.set_unbuffered(False)

    self.connect((self.channels_dynamic_channel_model_0, 0), (self.blocks_file_sink_0, 0))
```

* self.disconnect
  연결된 block을 끊기 위해서 사용되는 함수이다.  
  원래는 file_sink의 속성만을 변경하려고 했지만, 이미 연결된 block들은 한번 열결되면 속성을 변경하기는 어렵다는 결론을 내렸다.  
  그 결과 연결을 끊고 나서 끊긴 block의 속성을 변경하고 다시 연결하는 방법을 생각하여 실행하게 되었다.  

* self.blocks_file_sink_0  
  이 부분이 block의 설정값을 변경해 주는 부분이다.  
  여기서 바뀌는 부분은 file_path로, 파일이 저장되는 경로를 변경해 주는 것이다.  

* self.connect
  이제 마지막으로 끊어졌던 block들을 다시 연결해주면 된다.


```python
import time
time.sleep(1)
```

sleep을 주는 이유에 대해 가장 먼저 설명을 하겠다.  
sleep이 갑자기 튀어나와서 당황할 수 있지만 이는 굉장히 중요한 것이다.  
sleep없이 해당 코드를 실행하게 되면 데이터가 잘 안모이는, 즉, 데이터가 없는 상태를 여러번 만나게 된다.  
하지만, cat에 대한 함수를 main문 안에서 grc 끝나는 부분에 넣으면 데이터의 양이 어마어마하게 쌓여있는 상황을 많이 보았다.  

그 이유에 대해 생각을 하다가, set_mod 함수에서는 delay가 없기 때문에 데이터를 못넣은다고 판단하여 delay를 넣었더니 결과는 최종적으로 file sink에 들어가는 데이터의 양에 약 1/5 정도가 들어가는 것을 확인 할 수 있었다.  

이는 순식간에 데이터가 많이 들어가기 때문에 1/5의 데이터 양도 충분하다고 생각하여 time sleep의 시간을 '1'로 설정을 하였다.

시간을 늘리면 데이터의 양이 더더욱 많이 들어오기 때문에 이는 내가 조정을 한 것이다.  




``` python
        if self.cnt == 0:
            pass
        else : 
            self.mod_ = list(self.dic.keys())[list(self.dic.values()).index(self.cnt-1)]
            self.mod_type_ = self.mod_dic[self.mod_]
            cat = start2.Cat()

            cat.generate(128, self.mod_,self.mod_type_)
            cat.train_test()
            cat.load_model('/root/workspace/RF-Signal-Model/weight_4layers.wts.h5')
            cat.score(1)
            cat.plot_matrix()

        self.cnt +=1
```

* 조건문
  가장 먼저 조건문을 설정한 이유는 라디오 버튼이 default값이 설정되어 있기 때문에 이는 내가 원하는 값이 아니기 때문에 이를 제외하기 위해서 설정을 하였다.
* self.mod
  다음 코드는 cnt-1 의 값에 해당하는 value값을 기준으로 key값을 뽑아내는 코드이다.
  dic의 형태는 {'bpsk_1' : '1', 'bpsk_2' : 2}와 같은 형태로 되어있기 때문에 value값을 기준으로 key값을 뽑아내게 된다.

*  self.mod_type  
  이는 self.mod를 key값으로 이용해서 mod_dic의 value를 뽑아내는 것이다.
  mod_dic의 형태는 {'bpsk_1' : 'BPSK', 'bpsk_2' : 'BPSK'}와 같이 되어있다.

* cat()
  이제 start2로 부터 class cat을 불러와서 generate,train_test, load, score, plot과정을 지나서 완성을 하면 된다.
