import cgi
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
form = cgi.FieldStorage()


template = """
<html>
<head>
    <meta charset="utf-8">
    <title> 個人情報検索 </title>
</head>
<body>
    <h1> ~ 個人情報を検索できます。 (一部の情報だけでも検索できます) ~ </h1>
    <form method="POST" action="/cgi-bin/result.py">
        <div style="padding: 10px; margin-bottom: 5px; display: inline-block; border: 1px solid #333333">
        <h3> 名前 : <input type="text" name="name_kanji"> (例：河田 明) < 名前と名字の間に半角スペースを空ける </h3>
        <h3> ふりがな : <input type="text" name="name_hiragana"> (例：かわた あきら) < 名前と名字の間に半角スペースを空ける </h3>
        <h3> アドレス : <input type="text" name="address"> (例：kawata_akira@example.com) </h3>
        <h3> 性別 : <input type="text" name="sex"> (例：男性) </h3>
        <h3> 年齢 : <input type="number" name="age"> (例：80) </h3> 
        <h3> 誕生日： <input type="number" name="year"> / <input type="number" name="month"> / 
        <input type="number" name="date"> (例：1937/5/26) </h3>
        <h3> 婚姻 : <input type="text" name="marry"> (既婚 or 未婚) </h3>
        <h3> 血液型 : <input type="text" name="blood"> (例：AB型) </h3>
        <h3> 都道府県 : <input type="text" name="prefecture"> (例：東京都) </h3>
        <h3> 電話番号： <input type="number" name="phone_number1"> - 
        <input type="number" name="phone_number2"> - 
        <input type="number" name="phone_number3"> (例：123-456-789) </h3>
        </div>
        <h3> 並び替える条件 </h3>
        <div style="padding: 10px; margin-bottom: 50px; display: inline-block; border: 1px solid #333333">
        <h3> 条件1 </h3>
        <p> <input type="radio" name="option1" value="名前"> 名前 <input type="radio" name="option1" value="ふりがな"> ふりがな
            <input type="radio" name="option1" value="アドレス"> アドレス　<input type="radio" name="option1" value="性別"> 性別 
            <input type="radio" name="option1" value="年齢"> 年齢 <input type="radio" name="option1" value="誕生日"> 誕生日 
            <input type="radio" name="option1" value="婚姻"> 婚姻 <input type="radio" name="option1" value="血液型"> 血液型 
            <input type="radio" name="option1" value="都道府県"> 都道府県 <input type="radio" name="option1" value="電話番号"> 電話番号 </p>
        <h3> 条件2 </h3>
        <p> <input type="radio" name="order" value=""> 未ソート <input type="radio" name="order" value="asc"> 昇順 <input type="radio" name="order" value="desc"> 降順 </p>
        <p> <input type="submit"> </p>
        </div>
    </form>
</body>
</html>
"""

print("Content-type: text/html\n")
print(template)

