import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile    # WAVファイルの読み込み
from scipy import signal    # 極大値
import pandas as pd    # ピアノの音階辞書
import matplotlib.animation as anm
import matplotlib.patches as pat
import time    # 時間の表示

#音声ファイル読み込み
wav_filename = "./sample.wav"
rate, data = scipy.io.wavfile.read(wav_filename) # サンプリング周波数とデータ

print("サンプリング周波数:", rate)
print("データ数:", len(data))

if data.ndim < 2:    # 配列の次元数
    print("モノラル")
else:
    print("ステレオ")
    # 連結して偶数要素を抽出する？
    data = np.ravel(data)[::2]
print(data)

#（振幅）の配列を作成
data = data / 32768

# データを分割 0.1秒ごと
data_split = np.array_split(data, int(len(data) / (rate / 10)))
print("分割数:", len(data_split))

count = 0
ex_freqency = []
for short_data in data_split:
    ex_freqency.append([])
    # 周波数成分
    fft_short_data = np.abs(np.fft.fft(short_data))    
    freqList = np.fft.fftfreq(short_data.shape[0], d=1.0/rate)

    maxid = signal.argrelmax(fft_short_data, order=2) # 極大値
    #print(maxid)
    #print(len(maxid[0]))
    for i in maxid[0]:
        if fft_short_data[i] > 10 and 25 < freqList[i] < 4200:
            #print(fft_data[i], freqList[i])
            #print(count, fft_short_data[i], freqList[i])
            ex_freqency[count].append([freqList[i], fft_short_data[i]])
    count += 1
    #print(freqList)
#print(ex_freqency)

piano_dic = pd.read_csv("./piano_dict.csv", encoding="utf-8")
print(piano_dic)

black_keys = piano_dic[piano_dic["scaleNameEn"].str.contains("#")].index
print(black_keys)

count = 0
keys = [] # 含まれる周波数の行
for row in ex_freqency:
    keys.append({})
    for i in row:
        #print(i, end=" ")
        #print(piano_dic.loc[abs(piano_dic.frequency - i).idxmin(), "scaleNameEn"], end=" ")
        key = piano_dic.loc[abs(piano_dic.frequency - i[0]).idxmin(), "keyNumber"] - 1    # 差が最小の音階
        if (key in keys[count]) == False or keys[count][key] < i[1]:    # かぶってないか、それより大きいか
            keys[count][key] = i[1]
    #for i in range(0, 88):
    #    if i + 1 in keys[count]:
    #        print("■", end="")
    #    else:
    #        print("□", end="")
    #print()
    count = count + 1
print(keys)

#"""

fig, ax = plt.subplots(figsize = (10, 2))
#ax.grid()
#ax.set_xlim(0, 88)
#ax.set_ylim(-1.5, 1.5)

def update(i, fig_title, data_list, ax):
    if i != 0:
        plt.cla()                      # 現在描写されているグラフを消去
    ax.axis("off")
    ax.set_xlim(0, 52.1)
    ax.set_ylim(-0.5, 2.5)
    skip = False
    white_count = 0
    plt.title(fig_title + time.strftime("%M:%S", time.gmtime(i / 10)))
    for j in range(0, 88):
        if skip == True:
            skip = False
            continue
        if j in black_keys:
            # 黒鍵の後の白鍵を描画
            color = "white"
            if j + 1 in data_list[i]:
                color = "red"
            rec = pat.Rectangle(xy = (white_count, 0), width = 1, height = 1.5, fc = color, ec = "black")
            ax.add_patch(rec)
            skip = True # 次の白鍵を飛ばす
            color = "gray"
            x, y = white_count - 0.3, 0.5
            w, h = 0.6, 1
        else:
            color = "white"
            x, y = white_count, 0
            w, h = 1, 1.5
        
        if j in data_list[i]:
            color = "red"
        
        rec = pat.Rectangle(xy = (x, y), width = w, height = h, fc = color, ec = "black")
        white_count = white_count + 1

        # Axesに正方形を追加
        ax.add_patch(rec)    #plt.plot(x, y, "r")

#ani = anm.FuncAnimation(fig, update, fargs = ("Mimicopy Yannyo ", keys, ax), interval = 100, frames = len(keys), repeat = False)
ani = anm.FuncAnimation(fig, update, fargs = ("Mimicopy ", keys, ax), interval = 100, frames = len(keys))

#plt.show()    # 表示
ani.save("Sample.gif", writer = "imagemagick")
#"""