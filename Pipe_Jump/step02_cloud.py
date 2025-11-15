# step02_cloud.py
"""
Step02: 背景に「雲」を足すステップ

★ねらい
- 背景の上に、画像をいくつか重ねて表示する方法を知る
- 画像ファイル(cloud.png)を、場所を変えて何回も使う練習
"""

from pathlib import Path  # ファイルやフォルダの場所を扱う標準ライブラリです

from kivy.app import App                        # Kivy アプリの土台になるクラス
from kivy.uix.widget import Widget              # 画面に置ける「なにもない箱」のようなもの
from kivy.uix.image import Image                # 画像を表示するための部品
from kivy.core.window import Window             # ウィンドウの大きさなどを扱うもの
from kivy.uix.floatlayout import FloatLayout    # 自由配置できるレイアウト 


# ------------------------------------------------------------
# 画像ファイルが入っているフォルダへの「道」をつくる
# ------------------------------------------------------------

# この Python ファイル(step01_bg.py)が置かれているフォルダを基準にします
BASE_DIR = Path(__file__).resolve().parent

# ./assets/img フォルダまでのパスを組み立てます
ASSETS_DIR = BASE_DIR / "assets"
IMG_DIR = ASSETS_DIR / "img"


def first_existing(*candidates: Path) -> str:
    """
    Step01と同じヘルパー関数。最初に見つかったファイルのパスを返します。
    いくつか候補を受け取って、
    「最初に見つかったファイル」のパスを文字列で返す関数。

    例:
        first_existing(IMG_DIR / "bg.png", IMG_DIR / "bg.jpg")

    どれも存在しない場合は、わざとエラーを出して気づけるようにします。
    """
    for p in candidates:
        if p.is_file():  # 実際にそのファイルが存在するか？
            return str(p)

    # ここに来るということは、候補がぜんぶ見つからなかったということ
    raise FileNotFoundError(
        "背景画像が見つかりません。\n"
        "./assets/img を確認してください。"
    )


# ------------------------------------------------------------
# 画面に背景と雲を出すウィジェット
# ------------------------------------------------------------
class BackgroundWithClouds(FloatLayout):
    """
    背景 + 雲を表示する画面
    
    - 背景：画面いっぱいに敷き詰める
    - 雲  ：cloud.pn を複数コピーして配置
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 背景画像と雲画像のパスを探します
        bg_path = first_existing(IMG_DIR / "bg.png", IMG_DIR / "bg.jpg")
        cloud_path = first_existing(IMG_DIR / "cloud.png")

        # まずは背景を一番下に敷きます
        bg = Image(
            source=bg_path,
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos = (0, 0)
        )
        self.add_widget(bg)
        
        # 雲をいくつか配置します
        # size_hint を　Noneにして、ピクセルサイズを直接指定しています
        cloud_positions =[
            (80, 360),
            (420, 420),
            (720, 360),
        ]
        for x, y in cloud_positions:
            cloud = Image(
                source=cloud_path,
                size=(256, 96),
                pos=(x, y),
                size_hint=(None, None),
            )
            self.add_widget(cloud)
            
# ------------------------------------------------------------
# アプリ本体
# ------------------------------------------------------------

class Step02CloudApp(App):
    """
    Kivy アプリ本体のクラス。

    - build() の戻り値が「最初に表示する画面」になります。
    """

    def build(self):
        # ウィンドウの初期サイズを決めておきます（フルHD の半分くらい）
        Window.size = (960, 540)

        # ウィンドウに表示するタイトル(左上などに出る名前)
        self.title = "Pipe & Jump 10 Lessons - Step01 Background"

        # さきほど作った画面(BackgroundWithClouds)を、最初の画面として返します
        return BackgroundWithClouds()


# このファイルを「直接」実行したときだけ、アプリを起動します。
# （ほかのファイルから import したときには動かないようにするおまじない）
if __name__ == "__main__":
    Step02CloudApp().run()
