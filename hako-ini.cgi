#----------------------------------------------------------------------
# 各種設定値
# (これ以降の部分の各設定値を、適切な値に変更してください)
#----------------------------------------------------------------------
# 箱庭チームトーナメント
# 設定ファイル
# $Id: hako-ini.cgi,v 1.1 2003/07/02 03:09:49 gaba Exp $

#----------------------------------------------------------------------
# 以下、必ず設定する部分
#----------------------------------------------------------------------

# ゲームのタイトル文字
$Htitle = '箱庭チームトーナメント';

# マスターパスワード
# このパスワードは、すべての島のパスワードを代用できます。
# 例えば、「他の島のパスワード変更」等もできます。
$masterPassword = 'password';

# 特殊パスワード
# このパスワードで「名前変更」を行うと、その島の資金、食料が最大値になります。
# (実際に名前を変える必要はありません。)
$HspecialPassword = 'special';


# このファイルを置くディレクトリ
# $baseDir = 'http://サーバー/ディレクトリ';
#
# 例)
# http://cgi2.bekkoame.ne.jp/cgi-bin/user/u5534/hakoniwa/hako-main.cgi
# として置く場合、
# $baseDir = 'http://cgi2.bekkoame.ne.jp/cgi-bin/user/u5534/hakoniwa';
# とする。最後にスラッシュ(/)は付けない。

$baseDir = 'http://localhost/tag';

# 画像ファイルを置くディレクトリ
# $imageDir = 'http://サーバー/ディレクトリ';
$imageDir = 'http://localhost/tag/img';

# 画像のローカル設定の説明ページ
$imageExp = 'http://localhost/tag/imgexp/index.html';

# jcode.plの位置

# $jcode = '/usr/libperl/jcode.pl';  # ベッコアメの場合
# $jcode = './jcode.pl';             # 同じディレクトリに置く場合
$jcode = './jcode.pl';

# ディレクトリのパーミッション
# 通常は0755でよいが、0777、0705、0704等でないとできないサーバーもあるらしい
$HdirMode = 0754;

# データディレクトリの名前
# ここで設定した名前のディレクトリ以下にデータが格納されます。
# デフォルトでは'data'となっていますが、セキュリティのため
# なるべく違う名前に変更してください。
$HdirName = 'data';

# 管理者名
$adminName = '管理者';

# 管理者のメールアドレス
$email = '***@********.***';

# 掲示板の名称
$bbsname = '掲示板';

# 掲示板アドレス
$bbs = 'http://gaba.elsia.com/tag/cgi/trees.cgi';

# 透明画像の位置
$cleangif = 'http://localhost/clean.gif';

# チーム用掲示板ディレクトリ名
$teambbs = 'bbs';

# ホームページのアドレス
$toppage = 'http://gaba.elsia.com/';

# データの書き込み方

# ロックの方式
# 1 ディレクトリ
# 2 システムコール(可能ならば最も望ましい)
# 3 シンボリックリンク
# 4 通常ファイル(あまりお勧めでない)
$lockMode = 1;

# (注)
# 4を選択する場合には、'key-free'という、パーミション666の空のファイルを、
# このファイルと同位置に置いて下さい。

#----------------------------------------------------------------------
# 必ず設定する部分は以上
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# 以下、好みによって設定する部分
#----------------------------------------------------------------------
#----------------------------------------
# ゲームの進行やファイルなど
#----------------------------------------
# １チームの人数
$HmenberCount = 3;

# 予選期間 ターン数
$HyosenTurn = 48;

# 開発期間 ターン数
$HdevTurn = 24;

# 開発(予選)期間　何ターンまとめて進むか
$HdevRepTurn = 1;

# 戦闘期間 ターン数
$HfigTurn = 12;

# 戦闘期間　何ターンまとめて進むか
$HfigRepTurn = 3;

# 開発(予選)期間の更新時間
$HunitTime = 10800; # 3時間

# 戦闘期間の更新時間
$HfightTime = 86400; # 24時間

# 戦闘期間終了後のインターバル
$HinterTime = 97200; # 27時間

# 異常終了基準時間
# (ロック後何秒で、強制解除するか)
$unlockTime = 60;

# 島の最大数
$HmaxIsland = 60;

# トップページに表示するログのターン数
$HtopLogTurn = 1;

# ログファイル保持ターン数
$HlogMax = 8; 

# バックアップを何ターンおきに取るか
$HbackupTurn = 3;

# バックアップを何回分残すか
$HbackupTimes = 3;

# 発見ログ保持行数
$HhistoryMax = 10;

# 放棄コマンド自動入力ターン数
$HgiveupTurn = 5;

# 放棄後のコメント
$HgiveupComment = '<FONT COLOR=RED>チーム預かり！</FONT>';

# コマンド入力限界数
# (ゲームが始まってから変更すると、データファイルの互換性が無くなります。)
$HcommandMax = 30;

# ローカル掲示板行数を使用するかどうか(0:使用しない、1:使用する)
$HuseLbbs = 1;

# ローカル掲示板行数
$HlbbsMax = 8;

# 島の大きさ
# (変更できないかも)
$HislandSize = 12;

# チーム数
$teamNum = 20;

# 予選通過チーム数
$yteamNum = 16;

# １チームのデータ行数（通常はこのままで大丈夫です）
$teamFileNum = 13;

# 他人から資金を見えなくするか
# 0 見えない
# 1 見える
# 2 100の位で四捨五入
$HhideMoneyMode = 2;

# パスワードの暗号化(0だと暗号化しない、1だと暗号化する)
$cryptOn = 1;

# デバッグモード(1だと、「ターンを進める」ボタンが使用できる)
$Hdebug = 0;

#----------------------------------------
# 資金、食料などの設定値
#----------------------------------------
# 初期資金
$HinitialMoney = 2000;

# 初期食料
$HinitialFood = 1000;

# 初期面積
$HlandSizeValue = 32;

# 初期浅瀬の数
$HseaNum = 20;

#----------------------------------------
# 資金、食料などの設定値と単位
#----------------------------------------
# お金の単位
$HunitMoney = '億円';

# 食料の単位
$HunitFood = '00トン';

# 人口の単位
$HunitPop = '00人';

# 広さの単位
$HunitArea = '00万坪';

# 木の数の単位
$HunitTree = '00本';

# 木の単位当たりの売値
$HtreeValue = 5;

# 名前変更のコスト
$HcostChangeName = 0;

# 人口1単位あたりの食料消費料
$HeatenFood = 0.2;

# 初期ミサイル基地の数
$HlandFirstMiss = 0;

# 一括自動地ならし用
# 何個目の荒地から割り引きか（この数の次の荒地から）
$precheap = 10;
# その際の割引率（8にしたら、2割引ということになります）
$precheap2 = 8;

# １ターンで木の増える本数
$HtreeUp = 2;

# 資金繰り何ターン続くと人口増加ストップするか？
$HstopAddPop = 3;

# チーム用 各賞の取得規模
$HprizePoint[1] = '5000';   # 繁栄賞
$HprizePoint[2] = '10000';  # 超繁栄賞
$HprizePoint[3] = '15000';  # 究極繁栄賞
$HprizePoint[4] = '500';    # 平和賞
$HprizePoint[5] = '800';    # 超平和賞
$HprizePoint[6] = '1500';   # 究極平和賞
$HprizePoint[7] = '1000';   # 災難賞
$HprizePoint[8] = '2000';   # 超災難賞
$HprizePoint[9] = '3000';   # 究極災難賞


1;
