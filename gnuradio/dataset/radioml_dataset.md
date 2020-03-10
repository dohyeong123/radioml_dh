# RadioML에서 데이서 생성하기

## 1. 데이터 파일 받아오기

git clone을 이용하여 데이터를 받아온다

```bash

 git clone https://github.com/radioML/dataset.git

```
<brbr>

## 2. gnuradio파일이 없으므로 관련 패키지 설치

gnuradio에 관련된 파일이 없으므로 해당 패키지를 설치한다.

```bash

apt-get install gnuradio
apt-get install doxygen(gr-mapper 설치시 필요)
apt-get install swig    
```

<brbr>

## 3. gr-mapper 모듈을 설치한다
<br>
파일 관리를 쉽게 진행하기 위해서 dataset을 git clone한 상위 폴더에서 설치를 진행하였다.

# 현재 경로
pwd : /root/<br>
ls : dataset

```bash
 git clone  https://github.com/gr-vt/gr-mapper.git
 <br>
 cd gr-mapper
 <br>
 mkdir build && cd build
 <br>
 cmake ..
#(could not find pkgconfig 에러가 발생하지만 이 에러는 apt-get install pkg-config로 해결)
 <br>
 make
 <br>
 make install
 <br>
 ldconfig
```
<br><br>

## 4. gr-mediatools 모듈 설치하기

가장 먼저 gr-mediatools를 설치하기 위한 패키지들을 설치한다.

```bash
apt-get install libavcodec-dev libavformat-dev libavutil-dev
```

그 후 다음 과정을 진행한다.
```bash
git clone https://github.com/osh/gr-mediatools
 cd gr-mediatools && mkdir build && cd build
 <br>
cmake ..
<br>
make
<br>
make install
<br>
ldconfig
```
<br>

>참고로 Make부분에서 생기는 error는 다음과 같이 해결한다.<br>
>> ```bash
>> gr-mediatools/lib/mediatools_audiosource_impl.cc파일을 연다.<br>
>> d_frame=avcodec_alloc_frame(); 을 다음과 같이 변경한다.
>> d_frame=av_frame_alloc();
>> ```

# 5. source_material 파일 불러오기

상위폴더로 이동을 한다

pwd : /root/

```bash
git clone https://github.com.radioML/source_material.git
```

dataset/source_alphabet.py 파일을 열어서 경로를 설정한다.

예시 )self.src = blocks.file_source(gr.sizeof_char, "**/root/workspace/source_material/gutenberg_shakespeare.txt**")
<br>
진한 글씨 부분을 변경 해주면 가능하다.

마지막으로 다음 명령어를 진행하면 데이터가 생성된다.

```bash
python generate_RML2016.04c.py
```
