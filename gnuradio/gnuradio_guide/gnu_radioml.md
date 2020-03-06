# GUNRadio에서 생성된 데이터 사용하기

## GNURadio에서 생성된 데이터 가져오기

### GNURadio Block

* Raodom_Source_block<br><br>
![random_source_block](random_source_block.png) ![random_source_properties](random_source_properties.png)<br>
  *<center>Raodom_Source_block & Random_Source_Properties</center>*<br>

  [min,max)범위의 수많은 random sample을 생성하는 block이다. <br>

  만약 Minimum = 0, Maximum =2 이면 이에 해당하는 random source block이 생성하는 값들은 010010100... 값으로 랜덤하게 값이 들어간다.

* PSK_Mod_Block
  
  ![psk_mod_block](psk_mod_block.png)
  ![psk_mod_properties](psk_mod_properties.png)<br>
  *<center>psk_mod_block & psk_mod_properties</center>*

  psk modulation은 디지털 데이터를 전송하는 방식으로 BPSK,QPSK,8PSK 등이 존재한다.<br>
  number of Constellation : <br>
  Samples/Symbol : 
  하나의 Symbol에 몇개의 sample이 들어갈 지를 정하는 곳이다.<br>
* QT_GUI_constellation

![QT_GUI_constellation_block](QT_GUI_constellation_block.png)
![QT_GUI_constellation_properties](QT_GUI_constellation_properties.png)
*<center>QT_GUI_constellation_block & QT_GUI_constellation_properties</center>*

QT_GUI block은 GNURadio flowgraph에 다양한 QT기반 그래픽 사용자 인터페이스 블록이 포함되어 있다. <br>
그 중에서 Constellation sink는 Real값과 Imaginary값을 극좌표 형태로 그려주는 역할을 한다.<br><br>

![QPSK_full](QPSK_full.png)
*<center>데이터를 QPSK를 통과하는 블록생성 과정</center>*

실행을 시키기 위해서는 **F5**을 눌러서 파일을 저장을 한다. <br>
다음으로 파일을 실행시키기 위해서 **F6**을 누른다.<br>

![QPSK_plot](QPSK_plot.png)
*<center>QPSK plot</center>*








