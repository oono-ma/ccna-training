import re
import os
import pathlib
import beautifulsoup 
from datetime import datetime as dt

# スクレイピングをするなら

path = 'index.html'

with open(path,'r', encoding='utf-8') as file:
    # index.htmlを読み込む
    s = file.read()

    # 面倒な最初の部分を”>1<”まで削除することによって簡略化
    while(s[0] != ">" or s[1] != "1" or s[2] !="<"):
      s = s.lstrip(s[0])
    # その後文字を合わせるため、">"を削除
    s = s.lstrip(s[0])

    # csvの邪魔になるのでコンマ削除
    s = s.replace(',','')

    # </td>まで削除することによって後半を簡略化
    while(s[-1] != ">" or s[-2] != "d" or s[-3] != "t" or s[-4] != "/" or s[-5] != "<"):
      s = s.rstrip(s[-1])
    s = s.rstrip(s[-5:])

    # 正誤判定を行う。
    s = re.sub('(|\n)\n<i class="far fa-circle fa-fw"></i>\n</td>\n(|\n)','〇',s)
    s = re.sub('(|\n)\n<i class="fas fa-times fa-fw"></i>\n</td>\n(|\n)','×',s)

    # タグ文字を削除する。
    s = re.sub('<i class="fa. fa-(pencil|star|building|lightbulb) fa-fw text-cyan (invisible|false)"></i>\n','',s)
    s = re.sub("<td class='text-right'>",'',s)
    s = re.sub("\n<br />",'',s)
    s = re.sub('</(p|a|td)>\n(\n|)(\n|)(<tr>|<p>|)','',s)

    # 設問数 , 正誤 , ID , 設問 , 分野となるようにコンマを挿入していく
    # 設問数-正誤間にコンマを挿入する。
    s = re.sub("<td class='text-center'>",',',s)
    # URLを置き換える
    # 正誤からIDにコンマを挿入する。
    s = re.sub('(|\n)<a href="/question_subjects/53/question_sessions/\d{7}/progressing_questions/\d{8}(\?result=true|)">(|\n)',',',s)
    # IDから設問間にコンマを挿入する。
    s = re.sub('<td>\n<p>(\n|)',',',s)
    # 設問-分野間にコンマを挿入する。
    s = re.sub('(|\n)<td>',',',s)

    # 分野-次の問題間に改行を挿入する。
    s = re.sub('</tr>\n<tr>','',s)

# ファイル名を決める工程
# ファイル名はccna-日付.cssになるようにする。
today = dt.now()
today = today.strftime('%Y_%m_%d')
csv_path ="ccna-"+today+".csv"
ccna_test = open(csv_path,'w')
ccna_test.write(s)