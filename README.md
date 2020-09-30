# はじめに

ここには、シェルマガ用のファイルをアップロードしています。

# 開発環境

- Python 3.7.4 

# 仕様

1. WAVファイルを読み込み
    - ステレオならば、連結して偶数要素を抽出
    - モノラルならば、そのまま
2. 0.1秒ごとにデータを分割し、配列に格納
3. 高速フーリエ変換により、周波数成分と振れ幅を取得
    - 88鍵ピアノの音域である帯域の周波数だけを抽出
4. ピアノの音階の辞書を作成
5. 辞書より、一番近い周波数の音階番号を取得
6. 可視化
    - MatplotLibで長方形を描画
    - 音声ファイルより抽出した音の鍵盤の色は赤くして表示
