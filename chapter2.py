"""モデル設計"""

"""
データ設計
"""


"""
46 RDBではマスターデータ・トランザクションデータ にわけて考える！！

6W3Hでデータを分類する!!
マスターデータ .. データの中の基礎。１つ１つの基礎的な情報を記録。
Whom  :(顧客、販売先)
Who   :(ユーザ、管理者)
What  :(商品、記事)
Where :(販売所、地域)

トランザクションデータ .. 行為により記録された履歴のようなもの。
How   :(販売、購入、出荷、操作)
When  :(登録日時、更新日時)
How Many   :(注文数、数量)
How Much   :(金額)
Why   :(売上、返品、値引き、補充)
"""


"""
47 トランザクションデータの取り扱いに注意!!
Ex. 単価が変わった時、、過去のデータに依存しないよう単価をマスターからトランザクションに書くなど。。
One Fact In One Place!!
"""


"""
48 クエリで使いやすいテーブル設計。
あえて正規化を崩して冗長にするなど。。
"""


"""
テーブル設計
"""


"""
49 NULLを避ける
いかに制約をつけるか！！が重要。
"""
class Product(models.Model):
    name = models.CharField("商品名",max_length=255);


"""
50 一意制約をつける
不正データが混入してからエラーが発生するより
混入する前にエラーを吐かすなど。
"""
class Review(models.Model):
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["product","user"],
                name = "unique_product_review"
            ),
        ]


