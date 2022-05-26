"""関数設計"""
# 1 関数名だけで処理を想像可能にする!
from dataclasses import dataclass
from datetime import date
from distutils.command.build_scripts import first_line_re
from email.policy import default


def write_item_csv(item):
    with open("item.csv", mode="w") as f:
        f.write(item.name)


# 2 関数名は具体的な意味の英単語！　→ より狭い意味！
# get よりは fetch, calc, aggregate(複数の情報から集計) etc..
# Ex.
# load, fetch, retrieve, search, calc, increase, decrease, merge, render, filter, aggregate, build, escape
# dump, create, update, patch, remove, sync, memoize, publish, notify, flatten, minimize, validate


# 3 関数名から想像できる型の戻り値
# is_, has_, enabled_, _activated, _confirmed などはboolを返すと推測できるから、使う時注意！
# bool型の関数は副作用が無いようにも注意！(外部アクセス、データ保存・読み込み、値の変換 etc.. )
# → if is_valid のように使える！！
def is_valid(name):
    return not name.endswith(".txt")


# 4 副作用のない関数にまとめる！
# →同じ入力を与えると常に同じ結果が出力するように！　→　テストしやすい！
# 変更できない値を引数に入れる。という考え。（オブジェクトではなく文字列。リストではなくタプル）

# (titleが含まれてるかどうかだけを確認する関数) → 再利用しやすい！
def is_valid_title(title):
    return title not in INVALID_TITLES:
# (update_articleだと副作用があることがわかりやすい！)
def update_article(article, title, body):
    if not is_valid_title(title):
        return
    article.title = title
    article.body = body
    article.valid = True
    article.save()
    return article


# 5 関数を意味づけできるように関数化！　むやみに処理のまとまりだけで分けたりしない。。
# プログラムの意図が分かりずらい。　関数の再利用が難しい。　単体テストしずらい。
# → 再利用性、処理の意味で分けるように！


# 6　デフォルト引数にリスト・辞書は設定しない
# デフォルト引数の値は関数呼び出しのたびに初期化されない！
# ミュータブル(更新可能)な値はデフォルト引数にしてはいけない→ 該当：リスト、辞書、集合

# ↓　これだと何回fooを呼び出しても"Hi"がreturnされる！
def foo(values = None):
    values = values or []
    values.append("Hi")
    return values


# 7 コレクションを引数にせず、str or int で受け取る！
# Ex. 失敗例(消費税を計算したい場合でも、毎度["price"]をキーに持つ辞書を用意しないといけない。。)
# → 関数の再利用性が低くなる！
def calc_tax_included(item, tax_rate = 0.1):
    return item["price"] * (1 + tax_rate)
# ↓ みたいにコレクションでない値で受け取る！
def calc_tax_included(price, tax_rate = 0.1):
    return price * (1 + tax_rate)

# 上だとテストが楽！（１００を渡すだけで良い！）
def test_calc_tax_included():
    assert calc_tax_included(100) == 110

# もし「商品」値を扱うときに、税込計算を頻繁にするならclass定義し、propertyから税込価格をreturnする！
class Item:
    # ...
    @property
    def price_including_tax(self):
        return calc_tax_included(self.price)


# 8 indexに意味を持たせない！
# 間に値が入ると意味が壊れる。index番号を覚えていなければいけない。
# タプルで管理せず、辞書やクラスにする！！
@dataclass
class Sale:
    sale_id : int
    item_id : int
    user_id : int
    amount : int
    sold_at : datetime

def validate_sales(sale):
    if not item_exists(sale.item_id):
        raise # ...
    if sale.amount < 1:
        raise # ..

# ループの時も気をつける　→ イテレータを使う！
# Ex .(bad)
for idx in range(len(items)):
    items[idx]
# Ex .(good)
for item in items:
    item
# indexが明示的に必要な場合　→ enumerate
for n, item in enumerate(items, start=1):
    print(n, "個目を処理中...")


# 9 引数に可変長引数 (*args, *kwargs) を使用しない！
# → 引数に間違えて値を与えてもエラーを吐かないから！
# → 個別の引数で指定！
class User:
    def __init__(self, name, mail=None):
        self.name = name
        self.mail = mail

# 可変長引数を使うのは、どんな値が来ても良い関数のみ！！
def as_json(obj, **fields):
    data = {getattr(obj, key, default) for key, default in fields.items()}
    return json.dumps(data)

some_obj = get_some_obj()
json_ste = as_json(some_obj, first_name = "John", last_name = "Doe")


# 10 コメントにはwhyを書く
# 関数の仕様を書く場合はコメントではなくdocstringに書く！
def do_something(users):
    """~~する処理

    複数のユーザに対し<do_something>を行う。
    ~~の場合に〜〜だから、ユーザのデータを更新する必要がある！
    """
    # SQLの実行回数を減らすため、以下のループは別関数に分離せず処理する。

# 処理の意味と、なぜそう書くのか？？を書く。　
# なぜこう処理しないのか？？の説明！！


# 11 コントローラー(main(), Djangoのview)に処理は書かない！
# コントローラーには　値の入出力・処理全体の制御　を書く。
# クエリパラメータを扱うライブラリ .. Form(Django), deform, WTForm
# → 単体のモデルやデータとして扱うことを意識する！



"""クラス設計"""
# 12 辞書ではなくクラスでを定義する！
# 再利用性が低い。チェックが増える。

# Ex. (bad)
# 引数にuserという辞書コレクションを期待している。。
def get_full_name(user):
    return user["last_name"] + user["first_name"]

# Ex. (good) 特定のキーを持つ辞書を期待するならクラスを定義！
import json
from dataclasses import dataclass
from datetime import date
@dataclass
class User:
    last_name : str
    first_name : str
    birthday : date
    # クラスにすると、処理をクラスのメソッドやプロパティーとして実装できる！
    @property
    def fullname(self):
        return self.first_name + self.last_name

    @property
    def age(self):
        today = date.today()
        born = self.birthday
        age = today.year - born.year
        if (today.month, today.day) < (born.month, born.day):
            return age - 1
        else:
            return age

    def load_user():
        with open("./user.json", encoding="utf-8") as f:
            return User(**json.load(f))


# 13 引数が多いクラスを定義するのは面倒。。→ dataclass を使う！
# dataclassは型チェックもできるから、mypyで型チェックもできる！

# Ex. (bad)
class User:
    def __init__(self, username, email, last_name, first_name, birthday, bio, role):
        self.username = username
        self.email = email
        self.last_name = last_name
        self.first_name = first_name
        self.birthday = birthday
        self.bio = bio
        self.role = role

# Ex. (good)  型とデフォルト引数に可読性が高くなる！
from dataclasses import dataclass
from datetime import date

@dataclass
class User:
    username :str
    email : str
    last_name : str
    first_name : str
    birthday : date
    role : str


# 14 別メソッドに値を渡すためだけに属性を設定してはいけない。
# 事前に他のメソッドを呼び出す必要がある。設計が間違い。
# メソッド同士の呼び出し順番を規定しないようにする？

#Ex. 変数や属性という「状態」を減らし、考えるべきこと・覚えておくことを減らす。
# @propertyを使う。
def age():
# ↓ ageを属性から@propertyに実装
@property
def age():


# 15 別途のモジュールにアクセスするだけの関数にする
@dataclass
class Product:
    id : int
    name : str

    @classmethod
    def retrieve(cls, id : int) -> "Product":
        data = retrieve_product_detail(id)
        return cls(
            id = data["id"],
            name = data["name"],
        )

"""モジュール設計"""
# 16　汎用的な名前は避ける。(util:便利なもの)


# 17 ビジネスロジックをモジュール分割する
# ビジネスロジック .. 具体的な業務に必要な処理。


# 18 モジュール名のおすすめ
# api, commands, consts.py, main.py, models.py などモジュール分割して、
# __init__.py, item.py などにパッケージ分割する。
# Ex.
# 認証              : authentication
# 認可,パーミッション : permission, authorization
# バリデーション      : validation, validators
# 例外              : exceptions


# 19 テストにテストと同等の処理を書かない。
# →　実装が間違っていてもテストと同じ結果になるから間違いに気付けない。
# →　数値や文字列など具体的に入力したりする。。


# 20  1つのテストメソッドでは１つの項目のみ確認

# Ex. (bad)
# 具体的なエラーがわからない。
class TestValidate:
    def test_validate(self):
        assert validate("a")
        assert validate("a" * 50)
        assert validate("a" * 100)
        assert not validate("a")
        assert not validate("a" * 101)

# Ex. (good)
class TestValidate(self):
    def test_valid(self):
        """
        検証が正しい
        """
        assert validate("a")
        assert validate("a" * 50)
        assert validate("a" * 100)

    def test_invalid_too_short(self):
        """
        検証が正しくない：短い
        """
        assert  not vaidate("")

    def test_invalid_too_long(self):
        """
        検証が正しくない：長い
        """
        assert  not validate("a" * 101)



