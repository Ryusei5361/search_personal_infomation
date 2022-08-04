import sqlite3
import cgi
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
form = cgi.FieldStorage()
v_name_kanji = form.getvalue("name_kanji", "")  # 名前（漢字）
v_name_hiragana = form.getvalue("name_hiragana", "")  # 名前（ふりがな）
v_address = form.getvalue("address", "")  # アドレス
v_sex = form.getvalue("sex", "")  # 性別
v_age = form.getvalue("age", "")  # 年齢
v_year = form.getvalue("year", "")  # 誕生日（年）
v_month = form.getvalue("month", "")  # 誕生日（月）
v_date = form.getvalue("date", "")  # 誕生日（日）
v_marry = form.getvalue("marry", "")  # 婚姻
v_blood = form.getvalue("blood", "")  # 血液型
v_prefecture = form.getvalue("prefecture", "")  # 都道府県
v_phone_number1 = form.getvalue("phone_number1", "")  # 電話番号（1ブロック目）
v_phone_number2 = form.getvalue("phone_number2", "")  # 電話番号（2ブロック目）
v_phone_number3 = form.getvalue("phone_number3", "")  # 電話番号（3ブロック目）
v_option1 = form.getvalue("option1", "")  # 並べ替え条件 1
v_order = form.getvalue("order", "")  # ソート条件

connection = sqlite3.connect("personal_info.sqlite3")
cur = connection.cursor()


# csv ファイルを読み込んでデータベースを作成
personal_info_list = []
try:
    with open("dummy.csv", "r") as file:
        for line in file:
            ten = [line.rstrip('\n')]
            personal_info_list.append(tuple(ten[0].split(",")))
    cur.execute(f"""
    create table personal_info({personal_info_list[0][0]}, {personal_info_list[0][1]}, {personal_info_list[0][2]},
    {personal_info_list[0][3]}, {personal_info_list[0][4]}, {personal_info_list[0][5]}, {personal_info_list[0][6]},
    {personal_info_list[0][7]}, {personal_info_list[0][8]}, {personal_info_list[0][9]});
    """)
    # 名前、ふりがな、アドレス、性別、年齢、誕生日、婚姻、血液型、都道府県、電話番号
except sqlite3.OperationalError:
    cur.execute("delete from personal_info")


# データベースに値を入れる
for i in personal_info_list:
    if i[0] == "名前":
        pass
    else:
        cur.execute(f"""
                insert into personal_info values('{i[0]}', '{i[1]}', '{i[2]}', '{i[3]}', '{i[4]}', '{i[5]}', '{i[6]}',
                '{i[7]}', '{i[8]}', '{i[9]}')
                """)


# 条件に当てはまるものをデータベースから検索
def execute(condition):
    cur.execute(f"""
            select * from personal_info where 名前 like '%{v_name_kanji}%' and ふりがな like '%{v_name_hiragana}%'
            and アドレス like '%{v_address}%' and 性別 like '%{v_sex}%' and 年齢 like '%{v_age}%'
            and 誕生日 like '%{v_year}%/%{v_month}%/%{v_date}%' and 婚姻 like '%{v_marry}%' and 血液型 like '%{v_blood}%'
            and 都道府県 like '%{v_prefecture}%' and 電話番号 like '%{v_phone_number1}%-%{v_phone_number2}%-%{v_phone_number3}%'
            {condition}
            """)


# 条件が設定されたか判定
if len(v_option1) != 0:
    execute(f"order by {v_option1} {v_order}")
else:
    execute("")


# 検索結果を表形式にする
result_1 = cur.fetchall()
contents = "<tr>"
if len(result_1) == 0:
    contents += "条件と一致する情報はありません。</tr>"
else:
    for i in result_1:
        contents += f"<td>{i[0]}</td> <td>{i[1]}</td> <td>{i[2]}</td> <td>{i[3]}</td> <td>{i[4]}歳</td>" \
                    f" <td>{i[5]}</td> <td>{i[6]}</td> <td>{i[7]}</td> <td>{i[8]}</td> <td>{i[9]}</td> </tr> <tr>"
    contents += "</tr>"


# 表示結果
template = """
<html>
<head>
    <meta charset="utf-8">
    <title> 個人情報検索 </title>
</head>
<body>
    <p><a href="/cgi-bin/search_personal_info.py"> 検索条件へ戻る </a></p>
    <h1> 出力結果 </h1>
    <h2> 該当人数：{people} 人 </h2>
    <table border=1>
        <tr>
            <th> 名前 </th>
            <th> ふりがな </th>
            <th> アドレス </th>
            <th> 性別 </th>
            <th> 年齢 </th>
            <th> 誕生日 </th>
            <th> 婚姻 </th>
            <th> 血液型 </th>
            <th> 都道府県 </th>
            <th> 電話番号 </th>
        </tr>
        {contents} 
    </table>
    <p><a href="/cgi-bin/search_personal_info.py"> 検索条件へ戻る </a></p>
</body>
</html>
"""

result_2 = template.format(name_kanji=v_name_kanji, name_hiragana=v_name_hiragana, address=v_address, sex=v_sex,
                           age=v_age, year=v_year, month=v_month, date=v_date, marry=v_marry, blood=v_blood,
                           prefecture=v_prefecture, phone_number1=v_phone_number1, phone_number2=v_phone_number2,
                           phone_number3=v_phone_number3, people=len(result_1), contents=contents, option1=v_option1)

print("Content-type: text/html\n")
print(result_2)

