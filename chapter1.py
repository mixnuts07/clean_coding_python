"""
関数設計
"""

"""
1 関数名だけで処理を想像可能にする!
"""
from dataclasses import dataclass
from datetime import date
from distutils.command.build_scripts import first_line_re
from email.policy import default
from typing import Type


def write_item_csv(item):
    with open("item.csv", mode="w") as f:
        f.write(item.name)


"""
2 関数名は具体的な意味の英単語！　→ より狭い意味！
"""
# get よりは fetch, calc, aggregate(複数の情報から集計) etc..
# Ex.
# load, fetch, retrieve, search, calc, increase, decrease, merge, render, filter, aggregate, build, escape
# dump, create, update, patch, remove, sync, memoize, publish, notify, flatten, minimize, validate


"""
3 関数名から想像できる型の戻り値
"""
# is_, has_, enabled_, _activated, _confirmed などはboolを返すと推測できるから、使う時注意！
# bool型の関数は副作用が無いようにも注意！(外部アクセス、データ保存・読み込み、値の変換 etc.. )
# → if is_valid のように使える！！
def is_valid(name):
    return not name.endswith(".txt")


"""
4 副作用のない関数にまとめる！
"""
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


"""
5 関数を意味づけできるように関数化！　むやみに処理のまとまりだけで分けたりしない。。
"""
# プログラムの意図が分かりずらい。　関数の再利用が難しい。　単体テストしずらい。
# → 再利用性、処理の意味で分けるように！


"""
6 デフォルト引数にリスト・辞書は設定しない
"""
# デフォルト引数の値は関数呼び出しのたびに初期化されない！
# ミュータブル(更新可能)な値はデフォルト引数にしてはいけない→ 該当：リスト、辞書、集合

# ↓　これだと何回fooを呼び出しても"Hi"がreturnされる！
def foo(values = None):
    values = values or []
    values.append("Hi")
    return values


"""
7 コレクションを引数にせず、str or int で受け取る！
"""
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


"""
8 indexに意味を持たせない!
"""
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


"""
9 引数に可変長引数 (*args, *kwargs) を使用しない！
"""
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


"""
10 コメントにはwhyを書く
"""
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



"""
クラス設計
"""


"""
12 辞書ではなくクラスでを定義する！
"""
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


"""
13 引数が多いクラスを定義するのは面倒。。→ dataclass を使う！
"""
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


"""
14 別メソッドに値を渡すためだけに属性を設定してはいけない。
"""
# 事前に他のメソッドを呼び出す必要がある。設計が間違い。
# メソッド同士の呼び出し順番を規定しないようにする？

#Ex. 変数や属性という「状態」を減らし、考えるべきこと・覚えておくことを減らす。
# @propertyを使う。
def age():
# ↓ ageを属性から@propertyに実装
@property
def age():


"""
15 別途のモジュールにアクセスするだけの関数にする
"""

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

"""
モジュール設計
"""


"""
16 汎用的な名前は避ける。(util:便利なもの)
"""


"""
17 ビジネスロジックをモジュール分割する
"""
# ビジネスロジック .. 具体的な業務に必要な処理。


"""
18 モジュール名のおすすめ
"""
# api, commands, consts.py, main.py, models.py などモジュール分割して、
# __init__.py, item.py などにパッケージ分割する。
# Ex.
# 認証              : authentication
# 認可,パーミッション : permission, authorization
# バリデーション      : validation, validators
# 例外              : exceptions


"""
19 テストにテストと同等の処理を書かない。
"""
# →　実装が間違っていてもテストと同じ結果になるから間違いに気付けない。
# →　数値や文字列など具体的に入力したりする。。


"""
20  1つのテストメソッドでは1つの項目のみ確認
"""

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
class TestValidate:
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

# pytest
class TestValidate:
    @pytest.mark.parametrize("text", ["a", "a"*50, "a"*100])
    def test_valid(self, text):
        """
        検証が正しい
        """
        assert  validate(text)

    @pytest.mark.parametrize("text", ["", "a", 101])
    def test_invalid(self, text):
        """
        検証が正しくない
        """
        assert  not validate(text)


"""
21 テストは　準備・実行・検証　に分割！ → Arrange Act Assert パターン
"""
# ユニットテストでやること .. テスト対象を実行するための準備・対象の実行・最後に検証(assert) の３段階

#Ex. 準備【Arrange】 実行【Act】 検証【Assert】
class TestSignupAPIView:

    @pytest.fixture
    def target_api(self):
        return "/api/signup"

    def test_do_signup(self, target_api, django_app):
        # 準備---
        from account.models import User

        params = {
            "email" : "signup@example.com",
            "name"  : "yamadataro",
            "passwords" : "xxxxxxxxxx", 
        }

        # 実行---
        res = django_app.post_json(target_api, params = params)

        # 検証---
        user = User.objects.all()[0]
        expected = {
            "status_code" : 201,
            "user_email" : "signup@example.com",
        }
        actual = {
            "status_code" : res.status_code,
            "user_email" : user.email,
        }
        assert expected == actual


"""
22 単体テストしやすいか？　視点から　実装の設計へ！ → テストしにくい実装は設計が悪い！
"""
# 関数の引数に大きな値（csvファイルなど）が必要な設計にしない！
# 処理を分離し、すべての動作確認に全てのデータが必要な設計にしない！
# → 引数を id : int のように簡単なものにする！
# どうしてもファイルなどの引数が必要なものもあっても良いが、数を減らす！


"""
23 テストが外部環境に依存しないよう気をつける！
"""
# → POST など外部通信を行う処理をそのままテストに書かない！

# 外部APIは　responses ライブラリを使う！！
# DBサーバーなどのミドルウェアは　SQLite / Redis は　fakeredis
# S3/ DynamoDB　は　moto でモック
# PC環境やディレクトリ構成は　tempfile


"""
24 テスト用のデータはテスト後に削除
"""
# テストケースが終わるタイミングで削除
# tempfile モジュールの　NamedTemporaryFile は一時的なファイルが作られ、ファイルクローズと同時に削除してくれる！


"""
25 テストはテストユーティリティを使う！
"""
# Ex..
# django.test / tempfile / responses / freezegun / pytest / pytest-django / pytest-freezegun / pytest-responses


"""
26 テストケースごとにデータを用意する！
"""
# データを使い回すと予期せぬエラーが発生するかも。。

# function
def square_list(nums):
    return [n * n for n in nums]
square_list([1,2,3]) # => [1,4,9]
# test
class TestSquareList:
    def test_square(self):
        # Arrange 
        test_list = [1,2,3]

        # Act
        actual = square_list(test_list)

        # Assert
        expected = [1,4,9]
        assert actual == expected


"""
27 必要十分なデータを用意
"""


"""
28 テストの実行順序に依存しないテストを書く！！！！
"""
# 1つのテストメソッドとして正しさの補償ができるように！
# 単体テストは冗長になっても良いからメソッド間で共通のデータを持たないように！
class TestSum:
    def test_sum(self):
        assert sum([0,1,2,3,4]) == 10
    def test_negative(self):
        assert sum([0,1,2,3,-5]) == 5
    def test_type_error(self):
        with pytest.raises(TypeError):
            sum([1,None])


"""
29 returnがListのテストではリストの要素数もテストする!
"""
# code
def load_items():
    return ({"id":1, "name":"Coffee"}, {"id":2, "name":"Cake"})
# test
class TestLoadItems:
    def test_load(self):
        actual = load_items()

        assert len(actual) == 2
        assert actual[0] == {"id":1, "name":"Coffee"}
        assert actual[1] == {"id":2, "name":"Cake"}


"""
30 テストに関係するデータ、パラメータのみ作る。
31 過剰なmockライブラリの使用は避ける
32 重要な処理は条件網羅！(ユーザ認証、支払い、認証、引き当て、データの変更削除など)
33 公式docを読む!! (Dash, Zeal)
****34 一気に実装する範囲を小さくする!!!!(気をつける!!!!) ****
→ 見積もりができないときは？？　→ タスクの細分化　===> タスクをバラす！　1タスクは3時間ほどで実装できるものを想定。
35 基本機能だけを実装してレビュー
"""


"""
36 実装方法の相談　→ 曖昧さをなくす！　→ 結論の言語化
37 
38 必要十分なコード 複雑さがなければ、いろいろな使われ方が可能であるようにする。
39 開発アーキテクチャDocs → 開発ルールの決定事項のみを俯瞰的に見れるものを１つ作る。
40 コメントに書く内容　→ 事前情報も含めてそれを見ればわかる状態にする。
41 PRに不要な差分は持たせない!!→粒度小さく!!
   コーディング規約を自動チェックするツール .. main:black , (pycodestyle, flake8, pylint)
42 レビューの根拠を明示。
43 レビューのチェックリスト作成。
44 レビューの時間を見積に含める。
45 レビュー後の変更について。→ガッツリ変えないように。→どのみちレビューを行う。
"""





