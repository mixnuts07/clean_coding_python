"""関数設計"""
# 1 関数名だけで処理を想像可能にする!
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
