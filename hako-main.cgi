#!/usr/local/bin/perl
# ↑はサーバーに合わせて変更して下さい。
# perl5用です。

#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# メインスクリプト(ver1.02)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# 箱庭諸島のページ: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# 箱庭チームトーナメント
# メインスクリプト
# $Id: hako-main.cgi,v 1.3 2004/06/02 02:04:26 gaba Exp $

require './hako-ini.cgi';

#----------------------------------------
# 基地の経験値
#----------------------------------------
# 経験値の最大値
$HmaxExpPoint = 200; # ただし、最大でも255まで

# レベルの最大値
my($maxBaseLevel) = 5;  # ミサイル基地
my($maxSBaseLevel) = 3; # 海底基地

# 経験値がいくつでレベルアップか
my(@baseLevelUp, @sBaseLevelUp);
@baseLevelUp = (20, 60, 120, 200); # ミサイル基地
@sBaseLevelUp = (50, 200);         # 海底基地

#----------------------------------------
# 災害
#----------------------------------------
# 地盤沈下
$HdisFallBorder = 110; # 安全限界の広さ(Hex数)
$HdisFalldown   = 30; # その広さを超えた場合の確率

#----------------------------------------
# 賞関係
#----------------------------------------

# 賞の名前
$Hprize[0] = 'ターン杯';
$Hprize[1] = '繁栄賞';
$Hprize[2] = '超繁栄賞';
$Hprize[3] = '究極繁栄賞';
$Hprize[4] = '平和賞';
$Hprize[5] = '超平和賞';
$Hprize[6] = '究極平和賞';
$Hprize[7] = '災難賞';
$Hprize[8] = '超災難賞';
$Hprize[9] = '究極災難賞';

#----------------------------------------
# 外見関係
#----------------------------------------
# <BODY>タグのオプション
my($htmlBody) = 'BGCOLOR="#EEFFFF"';
$Body = "<BODY $htmlBody>";
# タグ
# タイトル文字
$HtagTitle_ = '<FONT SIZE=7 COLOR="#8888ff">';
$H_tagTitle = '</FONT>';

# H1タグ用
$HtagHeader_ = '<FONT COLOR="#4444ff">';
$H_tagHeader = '</FONT>';

# 大きい文字
$HtagBig_ = '<FONT SIZE=6>';
$H_tagBig = '</FONT>';

# 島の名前など
$HtagName_ = '<FONT COLOR="#a06040"><B>';
$H_tagName = '</B></FONT>';

# チームの名前
$HtagTName_ = '<FONT COLOR="#A0522D"><B>[';
$H_tagTName = ']</B></FONT>';

#$HtagTName_ = '<FONT COLOR="#A0522D"><B>&lt';
#$H_tagTName = '&gt</B></FONT>';

# 薄くなった島の名前
$HtagName2_ = '<FONT COLOR="#808080"><B>';
$H_tagName2 = '</B></FONT>';

# 薄くなったチームの名前
$HtagTName2_ = '<FONT COLOR="#808080"><B>[';
$H_tagTName2 = ']</B></FONT>';

# 順位の番号など
$HtagNumber_ = '<FONT COLOR="#800000"><B>';
$H_tagNumber = '</B></FONT>';

# 順位表における見だし
$HtagTH_ = '<FONT COLOR="#C00000"><B>';
$H_tagTH = '</B></FONT>';

# 開発計画の名前
$HtagComName_ = '<FONT COLOR="#d08000"><B>';
$H_tagComName = '</B></FONT>';

# 災害
$HtagDisaster_ = '<FONT COLOR="#ff0000"><B>';
$H_tagDisaster = '</B></FONT>';

# ローカル掲示板、観光者の書いた文字
$HtagLbbsSS_ = '<FONT COLOR="#0000ff"><B>';
$H_tagLbbsSS = '</B></FONT>';

# ローカル掲示板、島主の書いた文字
$HtagLbbsOW_ = '<FONT COLOR="#ff0000"><B>';
$H_tagLbbsOW = '</B></FONT>';

# ローカル掲示板、島無し観光者の書いた文字
$HtagLbbsSK_ = '<FONT COLOR="#003333"><B>';
$H_tagLbbsSK = '</B></FONT>';

# 通常の文字色(これだけでなく、BODYタグのオプションもちゃんと変更すべし
$HnormalColor = '#000000';

# 何回戦目
$HtagFico_ = '<FONT SIZE="7" COLOR="#4444ff">';
$H_tagFico = '</FONT>';

# 順位表、セルの属性
$HbgTitleCell   = 'BGCOLOR="#ccffcc"'; # 順位表見出し
$HbgNumberCell  = 'BGCOLOR="#ccffcc"'; # 順位表順位
$HbgNameCell    = 'BGCOLOR="#ccffff"'; # 順位表島の名前
$HbgInfoCell    = 'BGCOLOR="#ccffff"'; # 順位表島の情報
$HbgCommentCell = 'BGCOLOR="#ccffcc"'; # 順位表コメント欄
$HbgInputCell   = 'BGCOLOR="#ccffcc"'; # 開発計画フォーム
$HbgMapCell     = 'BGCOLOR="#ccffcc"'; # 開発計画地図
$HbgCommandCell = 'BGCOLOR="#ccffcc"'; # 開発計画入力済み計画

# 予選用落ちレッドライン
$YbgNumberCell  = 'BGCOLOR="#F0BBDA"'; # 順位表順位
$YbgNameCell    = 'BGCOLOR="#E4CCF5"'; # 順位表島の名前
$YbgInfoCell    = 'BGCOLOR="#E4CCF5"'; # 順位表島の情報
$YbgCommentCell = 'BGCOLOR="#F0BBDA"'; # 順位表コメント欄

#----------------------------------------------------------------------
# 好みによって設定する部分は以上
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# これ以降のスクリプトは、変更されることを想定していませんが、
# いじってもかまいません。
# コマンドの名前、値段などは解りやすいと思います。
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# 各種定数
#----------------------------------------------------------------------
# このファイル
$HthisFile = "$baseDir/hako-main.cgi";

# アプレット通信用 CGI
$HjavaFile = "$baseDir/hako-java.cgi";

# 地形番号
$HlandSea      = 0;  # 海
$HlandWaste    = 1;  # 荒地
$HlandPlains   = 2;  # 平地
$HlandTown     = 3;  # 町系
$HlandForest   = 4;  # 森
$HlandFarm     = 5;  # 農場
$HlandFactory  = 6;  # 工場
$HlandBase     = 7;  # ミサイル基地
$HlandDefence  = 8;  # 防衛施設
$HlandSbase    = 9;  # 海底基地
$HlandHaribote = 12; # ハリボテ

# コマンド
$HcommandTotal = 22; # コマンドの種類

# 計画番号の設定
# 整地系
$HcomPrepare  = 01; # 整地
$HcomPrepare2 = 02; # 地ならし
$HcomReclaim  = 03; # 埋め立て
$HcomDestroy  = 04; # 掘削
$HcomSellTree = 05; # 伐採
$HcomPrepRecr = 06; # 埋め立て＋地ならし

# 作る系
$HcomPlant    = 11; # 植林
$HcomFarm     = 12; # 農場整備
$HcomFactory  = 13; # 工場建設
$HcomBase     = 14; # ミサイル基地建設
$HcomDbase    = 15; # 防衛施設建設
$HcomHaribote = 16; # ハリボテ設置
$HcomFastFarm = 17; # 高速農場整備

# 発射系
$HcomMissileNM   = 31; # ミサイル発射
$HcomMissilePP   = 32; # PPミサイル発射

# 運営系
$HcomDoNothing  = 41; # 資金繰り
$HcomSell       = 42; # 食料輸出
$HcomFood       = 43; # 食料援助
$HcomPropaganda = 44; # 誘致活動

# 自動入力系
$HcomAutoPrepare  = 61; # フル整地
$HcomAutoPrepare2 = 62; # フル地ならし
$HcomAutoDelete   = 63; # 全コマンド消去
$HcomAutoPrepare3 = 64; # 一括自動地ならし

# 順番
@HcomList =
    ($HcomPrepare, $HcomPrepare2, $HcomReclaim, $HcomDestroy, $HcomPrepRecr, 
     $HcomSellTree, $HcomPlant, $HcomFarm, $HcomFactory, $HcomFastFarm,
     $HcomBase, $HcomDbase, $HcomMissileNM, $HcomMissilePP, 
     $HcomDoNothing, $HcomSell, $HcomFood, $HcomPropaganda,
     $HcomAutoPrepare, $HcomAutoPrepare2, $HcomAutoPrepare3, $HcomAutoDelete);

# 計画の名前と値段
$HcomName[$HcomPrepare]      = '整地';
$HcomCost[$HcomPrepare]      = 5;
$HcomName[$HcomPrepare2]     = '地ならし';
$HcomCost[$HcomPrepare2]     = 100;
$HcomName[$HcomReclaim]      = '埋め立て';
$HcomCost[$HcomReclaim]      = 100;
$HcomName[$HcomPrepRecr]    = '埋め立て+地ならし';
$HcomCost[$HcomPrepRecr]    = 0;
$HcomName[$HcomDestroy]      = '掘削';
$HcomCost[$HcomDestroy]      = 200;
$HcomName[$HcomSellTree]     = '伐採';
$HcomCost[$HcomSellTree]     = 0;
$HcomName[$HcomPlant]        = '植林';
$HcomCost[$HcomPlant]        = 10;
$HcomName[$HcomFarm]         = '農場整備';
$HcomCost[$HcomFarm]         = 20;
$HcomName[$HcomFastFarm]     = '高速農場整備';
$HcomCost[$HcomFastFarm]     = 500;
$HcomName[$HcomFactory]      = '工場建設';
$HcomCost[$HcomFactory]      = 100;
$HcomName[$HcomBase]         = 'ミサイル基地建設';
$HcomCost[$HcomBase]         = 300;
$HcomName[$HcomDbase]        = '防衛施設建設';
$HcomCost[$HcomDbase]        = 600;
$HcomName[$HcomHaribote]     = 'ハリボテ設置';
$HcomCost[$HcomHaribote]     = 1;
$HcomName[$HcomMissileNM]    = 'ミサイル発射';
$HcomCost[$HcomMissileNM]    = 20;
$HcomName[$HcomMissilePP]    = 'PPミサイル発射';
$HcomCost[$HcomMissilePP]    = 50;
$HcomName[$HcomPropaganda]   = '誘致活動';
$HcomCost[$HcomPropaganda]   = 800;
$HcomName[$HcomDoNothing]    = '資金繰り';
$HcomCost[$HcomDoNothing]    = 0;
$HcomName[$HcomSell]         = '食料輸出';
$HcomCost[$HcomSell]         = -100;
$HcomName[$HcomFood]         = '食料援助';
$HcomCost[$HcomFood]         = -100;
$HcomName[$HcomAutoPrepare]  = '整地自動入力';
$HcomCost[$HcomAutoPrepare]  = 0;
$HcomName[$HcomAutoPrepare2] = '地ならし自動入力';
$HcomCost[$HcomAutoPrepare2] = 0;
$HcomName[$HcomAutoPrepare3] = '一括自動地ならし';
$HcomCost[$HcomAutoPrepare3] = 0;
$HcomName[$HcomAutoDelete]   = '全計画を白紙撤回';
$HcomCost[$HcomAutoDelete]   = 0;

#----------------------------------------------------------------------
# 変数
#----------------------------------------------------------------------

# COOKIE
my($defaultID);       # 島の名前
my($defaultTarget);   # ターゲットの名前


# 島の座標数
$HpointNumber = $HislandSize * $HislandSize;

#----------------------------------------------------------------------
# メイン
#----------------------------------------------------------------------

# jcode.plをrequire
require($jcode);

# 「戻る」リンク
$HtempBack = "<A HREF=\"$HthisFile?\">${HtagBig_}トップへ戻る${H_tagBig}</A>";

# ロックをかける
if(!hakolock()) {
    # ロック失敗
    # ヘッダ出力
    tempHeader();

    # ロック失敗メッセージ
    tempLockFail();

    # フッタ出力
    tempFooter();

    # 終了
    exit(0);
}

# 乱数の初期化
srand(time^$$);

# COOKIE読みこみ
cookieInput();

# CGI読みこみ
cgiInput();

# 島データの読みこみ
if(readIslandsFile($HcurrentID) == 0) {
    unlock();
    tempHeader();
    tempNoDataFile();
    tempFooter();
    exit(0);
}

# チームデータ読み込み
if(readTeamsFile() == 0) {
    unlock();
    tempHeader();
    tempNoDataFile();
    tempFooter();
    exit(0);
}


# テンプレートを初期化
tempInitialize();

# COOKIE出力
cookieOutput();

# ヘッダ出力
#tempHeader();
if($HmainMode eq 'owner' && $HjavaMode eq 'java' ||
   $HmainMode eq 'commandJava' || # コマンド入力モード
   $HmainMode eq 'comment' && $HjavaMode eq 'java' || #コメント入力モード
   $HmainMode eq 'lbbs' && $HjavaMode eq 'java') { #コメント入力モード
	$Body = "<BODY onload=\"init()\" $htmlBody>";
   	require('hako-js.cgi');
	require('hako-map.cgi');
	# ヘッダ出力
	tempHeader();
    if($HmainMode eq 'commandJava') {
    	# 開発モード
    	commandJavaMain();
    } elsif($HmainMode eq 'comment') {
    	# コメント入力モード
    	commentMain();
    } elsif($HmainMode eq 'lbbs') {
	# ローカル掲示板モード
        localBbsMain();
    }else{
	ownerMain();
    }
	# フッタ出力
	tempFooter();
	# 終了
	exit(0);
    }elsif($HmainMode eq 'landmap'){
   	require('hako-js.cgi');
        require('hako-map.cgi');
	$Body = "<BODY $htmlBody>";
	# ヘッダ出力
	tempHeaderJava();
    # 観光モード
    printIslandJava();
	# フッタ出力
	tempFooter();
	# 終了
	exit(0);
}else{
	# ヘッダ出力
	tempHeader();
}

if($HmainMode eq 'turn') {
    # ターン進行
    require('hako-turn.cgi');
    require('hako-top.cgi');
    turnMain();

} elsif($HmainMode eq 'new') {
    # 島の新規作成
    require('hako-turn.cgi');
    require('hako-map.cgi');
    newIslandMain();

} elsif($HmainMode eq 'print') {
    # 観光モード
    require('hako-map.cgi');
    printIslandMain();

} elsif($HmainMode eq 'owner') {

    # 開発モード
    require('hako-map.cgi');
    ownerMain();

} elsif($HmainMode eq 'command') {
    # コマンド入力モード
    require('hako-map.cgi');
    commandMain();

} elsif($HmainMode eq 'comment') {
    # コメント入力モード
    require('hako-map.cgi');
    commentMain();

} elsif($HmainMode eq 'lbbs') {

    # ローカル掲示板モード
    require('hako-map.cgi');
    localBbsMain();

} elsif($HmainMode eq 'change') {
    # 情報変更モード
    require('hako-turn.cgi');
    require('hako-top.cgi');
    changeMain();

} elsif($HmainMode eq 'logView') {
    # LOGモード
    require('hako-more.cgi');
    logViewMain();

} elsif($HmainMode eq 'logTeam') {
    # LOGモード
    require('hako-more.cgi');
    logTeamMain();

} elsif($HmainMode eq 'help') {
    # ☆HELPモード
    require('hako-more.cgi');
    helpMain();

} elsif($HmainMode eq 'teamdata') {
    # 作戦本部
    require('hako-more.cgi');
    teamDataMain();

} elsif($HmainMode eq 'HchangeTName') {
    # チーム名変更
    require('hako-more.cgi');
    changeTeamNameMain();

} elsif($HmainMode eq 'fightlog') {
    # ☆戦闘の記録モード
    require('hako-more.cgi');
    fightlogMain();

} elsif($HmainMode eq 'adminpage') {
    # 管理者画面
    require('hako-more.cgi');
    pageAdminMain();

} elsif($HmainMode eq 'delete') {
    # 島削除モード
    require('hako-turn.cgi');
    require('hako-top.cgi');
    changeMain();

} else {
    # その他の場合はトップページモード
    require('hako-top.cgi');
    topPageMain();
}

# フッタ出力
tempFooter();

# 終了
exit(0);

# コマンドを前にずらす
sub slideFront {
    my($command, $number) = @_;
    my($i);

    # それぞれずらす
    splice(@$command, $number, 1);

    # 最後に資金繰り
    $command->[$HcommandMax - 1] = {
	'kind' => $HcomDoNothing,
	'target' => 0,
	'x' => 0,
	'y' => 0,
	'arg' => 0
	};
}

# コマンドを後にずらす
sub slideBack {
    my($command, $number) = @_;
    my($i);

    # それぞれずらす
    return if $number == $#$command;
    pop(@$command);
    splice(@$command, $number, 0, $command->[$number]);
}

#----------------------------------------------------------------------
# 島データ入出力
#----------------------------------------------------------------------

# 全島データ読みこみ
sub readIslandsFile {
    my($num) = @_; # 0だと地形読みこまず
                   # -1だと全地形を読む
                   # 番号だとその島の地形だけは読みこむ

    # データファイルを開く
    if(!open(IN, "${HdirName}/hakojima.dat")) {
	rename("${HdirName}/hakojima.tmp", "${HdirName}/hakojima.dat");
	if(!open(IN, "${HdirName}/hakojima.dat")) {
	    return 0;
	}
    }

    # 各パラメータの読みこみ
    $HislandTurn     = int(<IN>); # ターン数

    $HislandLastTime = int(<IN>); # 最終更新時間
    if($HislandLastTime == 0) {
	return 0;
    }
    $HislandNumber   = int(<IN>); # 島の総数
    $HislandNextID   = int(<IN>); # 次に割り当てるID
    $HteamNumber     = int(<IN>); # チーム数
    $HturnCount      = int(<IN>); # 更新数
    $HnextCTurn      = int(<IN>); # 切り替えターン
    $HfightMode      = int(<IN>); # 現在の戦闘モード
    $HfightCount     = int(<IN>); # 何回戦目か

    # ターン処理判定
    my($now) = time;
    if(((($Hdebug == 1) && 
	($HmainMode eq 'Hdebugturn')) ||
       (($now - $HislandLastTime) >= $HunitTime)) && ($HteamNumber > 1)) {
	$HmainMode = 'turn';
	$num = -1; # 全島読みこむ
    }

    # 島の読みこみ
    my($i);
    for($i = 0; $i < $HislandNumber; $i++) {
	 $Hislands[$i] = readIsland($num);
	 $HidToNumber{$Hislands[$i]->{'id'}} = $i;
    }

    # ファイルを閉じる
    close(IN);

    return 1;
}

# 島ひとつ読みこみ
sub readIsland {
    my($num) = @_;
    my($name, $id, $prize, $absent, $comment, $password, $food,
       $pop, $area, $farm, $factory, $teamid, $defence, $fire, $ownername);
    $name = <IN>; # 島の名前
    chomp($name);
    if($name =~ s/,(.*)$//g) {
	$defence = int($1);
    } else {
	$defence = 0;
    }
    $id = int(<IN>); # ID番号
    $prize = int(<IN>); # 受賞
    $absent = int(<IN>); # 連続資金繰り数
    $comment = <IN>; # コメント
    chomp($comment);
    $password = <IN>; # 暗号化パスワード
    chomp($password);
    $food = int(<IN>);     # 食料
    $pop = int(<IN>);      # 人口
    $area = int(<IN>);     # 広さ
    $farm = int(<IN>);     # 農場
    $factory = int(<IN>);  # 工場
    $teamid = int(<IN>);   # チームID
    $fire = int(<IN>);     # ミサイル発射可能数
    $ownername = <IN>;     # オーナーネーム
    chomp($ownername);

    # HidToNameテーブルへ保存
    $HidToName{$id} = $name;	# 

    # 地形
    my(@land, @landValue, $line, @command, @lbbs);

    if(($num == -1) || ($num == $id)) {
	if(!open(IIN, "${HdirName}/island.$id")) {
	    rename("${HdirName}/islandtmp.$id", "${HdirName}/island.$id");
	    if(!open(IIN, "${HdirName}/island.$id")) {
		exit(0);
	    }
	}
	my($x, $y);
	for($y = 0; $y < $HislandSize; $y++) {
	    $line = <IIN>;
	    for($x = 0; $x < $HislandSize; $x++) {
		$line =~ s/^(.)(..)//;
		$land[$x][$y] = hex($1);
		$landValue[$x][$y] = hex($2);
	    }
	}

	# コマンド
	my($i);
	for($i = 0; $i < $HcommandMax; $i++) {
	    $line = <IIN>;
	    $line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*)$/;
	    $command[$i] = {
		'kind' => int($1),
		'target' => int($2),
		'x' => int($3),
		'y' => int($4),
		'arg' => int($5)
		}
	}

	# ローカル掲示板
	for($i = 0; $i < $HlbbsMax; $i++) {
	    $line = <IIN>;
	    chomp($line);
	    $lbbs[$i] = $line;
	}

	close(IIN);
    }

    # 島型にして返す
    return {
	 'name' => $name,
	 'id' => $id,
	 'defence' => $defence,
	 'prize' => $prize,
	 'absent' => $absent,
	 'comment' => $comment,
	 'password' => $password,
	 'food' => $food,
	 'pop' => $pop,
	 'area' => $area,
	 'farm' => $farm,
	 'factory' => $factory,
	 'teamid' => $teamid,
	 'fire' => $fire,
	 'ownername' => $ownername,
	 'land' => \@land,
	 'landValue' => \@landValue,
	 'command' => \@command,
	 'lbbs' => \@lbbs,
    };
}

# 全島データ書き込み
sub writeIslandsFile {
    my($num) = @_;

    # ファイルを開く
    open(OUT, ">${HdirName}/hakojima.tmp");

    # 各パラメータ書き込み
    print OUT "$HislandTurn\n";
    print OUT "$HislandLastTime\n";
    print OUT "$HislandNumber\n";
    print OUT "$HislandNextID\n";
    print OUT "$HteamNumber\n";
    print OUT "$HturnCount\n";
    print OUT "$HnextCTurn\n";
    print OUT "$HfightMode\n";
    print OUT "$HfightCount\n";

    # 島の書きこみ
    my($i);
    for($i = 0; $i < $HislandNumber; $i++) {
	 writeIsland($Hislands[$i], $num);
    }

    # ファイルを閉じる
    close(OUT);

    # 本来の名前にする
    unlink("${HdirName}/hakojima.dat");
    rename("${HdirName}/hakojima.tmp", "${HdirName}/hakojima.dat");
}

# 島ひとつ書き込み
sub writeIsland {
    my($island, $num) = @_;
    my($defence);
    $defence = int($island->{'defence'});
    print OUT $island->{'name'} . ",$defence\n";
    print OUT $island->{'id'} . "\n";
    print OUT $island->{'prize'} . "\n";
    print OUT $island->{'absent'} . "\n";
    print OUT $island->{'comment'} . "\n";
    print OUT $island->{'password'} . "\n";
    print OUT $island->{'food'} . "\n";
    print OUT $island->{'pop'} . "\n";
    print OUT $island->{'area'} . "\n";
    print OUT $island->{'farm'} . "\n";
    print OUT $island->{'factory'} . "\n";
    print OUT $island->{'teamid'} . "\n";
    print OUT $island->{'fire'} . "\n";
    print OUT $island->{'ownername'} . "\n";

    # 地形
    if(($num <= -1) || ($num == $island->{'id'})) {
	open(IOUT, ">${HdirName}/islandtmp.$island->{'id'}");

	my($land, $landValue);
	$land = $island->{'land'};
	$landValue = $island->{'landValue'};
	my($x, $y);
	for($y = 0; $y < $HislandSize; $y++) {
	    for($x = 0; $x < $HislandSize; $x++) {
		printf IOUT ("%x%02x", $land->[$x][$y], $landValue->[$x][$y]);
	    }
	    print IOUT "\n";
	}

	# コマンド
	my($command, $cur, $i);
	$command = $island->{'command'};
	for($i = 0; $i < $HcommandMax; $i++) {
	    printf IOUT ("%d,%d,%d,%d,%d\n", 
			 $command->[$i]->{'kind'},
			 $command->[$i]->{'target'},
			 $command->[$i]->{'x'},
			 $command->[$i]->{'y'},
			 $command->[$i]->{'arg'}
			 );
	}

	# ローカル掲示板
	my($lbbs);
	$lbbs = $island->{'lbbs'};
	for($i = 0; $i < $HlbbsMax; $i++) {
	    print IOUT $lbbs->[$i] . "\n";
	}

	close(IOUT);
	unlink("${HdirName}/island.$island->{'id'}");
	rename("${HdirName}/islandtmp.$island->{'id'}", "${HdirName}/island.$island->{'id'}");
    }
}

#----------------------------------------------------------------------
# チームデータ入出力
#----------------------------------------------------------------------

# 全島データ読みこみ
sub readTeamsFile {

    # データファイルを開く
    if(!open(IN, "${HdirName}/teams.dat")) {
	rename("${HdirName}/teams.tmp", "${HdirName}/teams.dat");
	if(!open(IN, "${HdirName}/teams.dat")) {
	    return 0;
	}
    }
    # チームの読みこみ
    my($i);
    for($i = 0; $i < $HteamNumber; $i++) {
	 $Hteams[$i] = readTeam();
	 $HidToTeamNumber{$Hteams[$i]->{'id'}} = $i;
    }

    # ファイルを閉じる
    close(IN);

    return 1;
}

# チームひとつ読みこみ
sub readTeam {

    my($name, $id, $password, $money, $food, $pop, $farm, $factory, $fightid, $prize, $reward, $rewturn);
    $name = <IN>; # チームの名前
    chomp($name);
    $id = int(<IN>); # ID番号
    $member = <IN>; # チーム員の島ID
    chomp($member);
    $password = <IN>; # 暗号化パスワード
    chomp($password);
    $money = int(<IN>);    # 資金
    $food = int(<IN>);     # 食料
    $pop = int(<IN>);      # 人口
    $farm = int(<IN>);     # 農場
    $factory = int(<IN>);  # 工場
    $fightid = int(<IN>);  # 対戦チームID
    $prize = int(<IN>);    # 賞
    $reward = int(<IN>);   # 報酬金
    $rewturn = int(<IN>);  # 報酬金用ターン数

    # HidToNameテーブルへ保存
    $HidToTeamName{$id} = $name;


    # 島型にして返す
    return {
	 'name' => $name,
	 'id' => $id,
	 'member' => $member,
	 'password' => $password,
	 'money' => $money,
	 'food' => $food,
	 'pop' => $pop,
	 'farm' => $farm,
	 'factory' => $factory,
	 'fightid' => $fightid,
	 'prize' => $prize,
	 'reward' => $reward,
	 'rewturn' => $rewturn,
    };
}

# 全チームデータ書き込み
sub writeTeamsFile {

    # ファイルを開く
    open(OUT, ">${HdirName}/teams.tmp");

    # 島の書きこみ
    my($i);
    for($i = 0; $i < $HteamNumber; $i++) {
	 writeTeam($Hteams[$i]);
    }

    # ファイルを閉じる
    close(OUT);

    # 本来の名前にする
    unlink("${HdirName}/teams.dat");
    rename("${HdirName}/teams.tmp", "${HdirName}/teams.dat");
}

# チームデータひとつ書き込み
sub writeTeam {

    my($team) = @_;
    print OUT $team->{'name'} . "\n";
    print OUT $team->{'id'} . "\n";
    print OUT $team->{'member'} . "\n";
    print OUT $team->{'password'} . "\n";
    print OUT $team->{'money'} . "\n";
    print OUT $team->{'food'} . "\n";
    print OUT $team->{'pop'} . "\n";
    print OUT $team->{'farm'} . "\n";
    print OUT $team->{'factory'} . "\n";
    print OUT $team->{'fightid'} . "\n";
    print OUT $team->{'prize'} . "\n";
    print OUT $team->{'reward'} . "\n";
    print OUT $team->{'rewturn'} . "\n";

}

#----------------------------------------------------------------------
# 入出力
#----------------------------------------------------------------------

# 標準出力への出力
sub out {
    print STDOUT jcode::sjis($_[0]);
}


# 戦闘の記録保存
sub HfightLog {
    my(@fightLog) = @_;
    $fCount2 = $#fightLog + 1;
    push(@offset,"$HfightCount\n");
    push(@offset,"$fCount2\n");
    for($i = 0 ; $i <= $#fightLog; $i++) {
	if($i %2 == 0) {
	    $HbgCell = $HbgInfoCell;
	} else {
	    $HbgCell = $HbgCommentCell;
	}
	my($fight) = $fightLog[$i];
	my($name,$pop,$money,$tname,$tpop,$member) = split(/<>/,$fight);
	push(@offset,"<TR><TD $HbgCell><NOBR>　${HtagTName_}${name}${H_tagTName}</nobr></td>");
	push(@offset,"<TD $HbgCell align=center><NOBR><B>${pop}$HunitPop</b></nobr></td>");
	push(@offset,"<TD $HbgCell><NOBR>　${HtagTName2_}${tname}${H_tagTName2}</nobr></td>");
	push(@offset,"<TD $HbgCell align=center><NOBR><B>${tpop}$HunitPop</b></nobr></td>");
	push(@offset,"<TD $HbgCell align=right><NOBR><B>${money}億円</b></nobr></td></TR>");
	push(@offset,"<TR><TD $HbgCell COLSPAN=2><NOBR>${HtagTH_}メンバー：${HtagName_}");
	my($island) = '';
	while($member =~ s/([0-9]*),//) {
	    if($1 eq '') { 
		push(@offset,"${H_tagName}</NOBR></TD><TD $HbgCell COLSPAN=2><NOBR>${HtagTH_}メンバー：${HtagName2_}");
		$island = '';
		next;
	    } elsif($island ne '') {
		push(@offset," : ");
	    }
	    $island = $Hislands[$HidToNumber{$1}];
	    push(@offset,"$island->{'name'}島");

	}
	push(@offset,"${H_tagName2}</NOBR></TD><TD $HbgCell>　</TD></TR>\n");
    }
}

# 予選落ち
sub HyosenLog {
    my(@fightLog) = @_;
    $fCount2 = $#fightLog + 1;
    push(@offset,"0\n");
    push(@offset,"$fCount2\n");
    for($i = 0 ; $i <= $#fightLog; $i++) {
	if($i %2 == 0) {
	    $HbgCell = $HbgInfoCell;
	} else {
	    $HbgCell = $HbgCommentCell;
	}
	my($fight) = $fightLog[$i];
	my($name,$pop,$member) = split(/<>/,$fight);
	push(@offset,"<TR><TD $HbgCell><NOBR>　${HtagTName2_}${name}${H_tagTName2}</nobr></td>");
	push(@offset,"<TD $HbgCell align=center><NOBR><B>${pop}$HunitPop</b></nobr></td>");
	push(@offset,"<TR><TD $HbgCell COLSPAN=2><NOBR>${HtagTH_}メンバー：${H_tagTH}${HtagName2_}");
	my($island) = '';
	while($member =~ s/([0-9]*),//) {
	    if($island ne '') {
		push(@offset," : ");
	    }
	    $island = $Hislands[$HidToNumber{$1}];
	    push(@offset,"$island->{'name'}島");

	}
	push(@offset,"${H_tagName2}</NOBR></TD></TR>\n");
    }
}

# CGIの読みこみ
sub cgiInput {
    my($line, $getLine);

    # 入力を受け取って日本語コードをEUCに
    $line = <>;
    $line =~ tr/+/ /;
    $line =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
    $line = jcode::euc($line);
    $line =~ s/[\x00-\x1f\,]//g;

    # GETのやつも受け取る
    $getLine = $ENV{'QUERY_STRING'};

    # 対象の島
    if($line =~ /CommandButton([0-9]+)=/) {
	# コマンド送信ボタンの場合
	$HcurrentID = $1;
	$defaultID = $1;
    }

    if($line =~ /ISLANDNAME=([^\&]*)\&/){
	# 名前指定の場合
	$HcurrentName = cutColumn($1, 32);
    }

    if($line =~ /ISLANDID=([0-9]+)\&/){
	# その他の場合
	$HcurrentID = $1;
	$defaultID = $1;
    }

    if($line =~ /TEAMID=([0-9]+)\&/){
	# その他の場合
	$HteamID = $1;
    }

    # パスワード
    if($line =~ /OLDPASS=([^\&]*)\&/) {
	$HoldPassword = $1;
	$HdefaultPassword = $1;
    }
    if($line =~ /PASSWORD=([^\&]*)\&/) {
	$HinputPassword = $1;
	$HdefaultPassword = $1;
    }
    if($line =~ /PASSWORD2=([^\&]*)\&/) {
	$HinputPassword2 = $1;
    }

    # メッセージ
    if($line =~ /MESSAGE=([^\&]*)\&/) {
	$Hmessage = cutColumn($1, 80);
    }

    if($line =~ /JAVAMODE=(cgi|java)/) {
	$HjavaMode = $1;
    }

    if($line =~ /CommandJavaButton([0-9]+)=/) {
	# コマンド送信ボタンの場合（Ｊａｖａスクリプト）
	$HcurrentID = $1;
	$defaultID = $1;
    }

    # ローカル掲示板
    if($line =~ /LBBSNAME=([^\&]*)\&/) {
	$HlbbsName = $1;
	$HdefaultName = $1;
    }
    if($line =~ /LBBSMESSAGE=([^\&]*)\&/) {
	$HlbbsMessage = cutColumn($1, 80);
    }
    if($line =~ /OWNERNAME=([^\&]*)\&/){
	# オーナー名指定の場合
	$HownerName = cutColumn($1, 22);
    }

    if($line =~ /IMGLINEMAC=([^&]*)\&/){
	my($flag) = 'file:///' . $1;
	$HimgLine = $flag;
    }

    if($line =~ /IMGLINE=([^&]*)\&/){
	my($flag) = substr($1, 0 , -10);
	$flag =~ tr/\\/\//;
	if($flag eq 'del'){ $flag = $imageDir; } else { $flag = 'file:///' . $flag; }
	$HimgLine = $flag;
    }

    if($line =~ /CTEAMNAME=([^\&]*)\&/){
	# チーム名指定の場合
	$teamName = $1;
    }

    if($line =~ /DELISLAND=([0-9]+)\&/){
	# 削除用
	$deleteID = $1;
    }

    # main modeの取得
    if($line =~ /TurnButton/) {
	if($Hdebug == 1) {
	    $HmainMode = 'Hdebugturn';
	}
    } elsif($line =~ /OwnerButton/) {
	$HmainMode = 'owner';
    } elsif($line =~ /teamData/) {
	$HmainMode = 'teamdata';
    } elsif($line =~ /ChangeOwnerName/) {
	$HmainMode = 'change';
    } elsif($line =~ /ChangeTeamName/) {
	$HmainMode = 'HchangeTName';
    } elsif($getLine =~ /Sight=([0-9]*)/) {
	$HmainMode = 'print';
	$HcurrentID = $1;
    } elsif($getLine =~ /IslandMap=([0-9]*)/) {
	$HmainMode = 'landmap';
	$HcurrentID = $1;
    } elsif($getLine =~ /TEAM=([0-9]*)/) {
	$HteamMode = $1;
    } elsif($line =~ /AdminPage/) {
	$HmainMode = 'adminpage';
    } elsif($line =~ /DeleteIsland/) {
        $HmainMode = 'delete';		# 削除モード
    } elsif($getLine =~ /FightLog/) {
	$HmainMode = 'fightlog';
    } elsif($getLine =~ /HELP/) {
	$HmainMode = 'help';
    } elsif($line =~ /NewIslandButton/) {
	$HmainMode = 'new';
    } elsif($getLine =~ /LogFileView=([0-9]*)/) {
	$HmainMode = 'logView';
	$Hlogturn = ($1 > $HlogMax) ? $HlogMax : $1;
    } elsif($getLine =~ /LogFileTeam=([0-9]*)/) {
	$HmainMode = 'logTeam';
	$HlogteamID = $1;
    } elsif($line =~ /LbbsButton(..)([0-9]*)/) {
	$HmainMode = 'lbbs';
	if($1 eq 'FO') {
	    # 観光者
	    $HlbbsMode = 0;
	    $HforID = $HcurrentID;
	} elsif($1 eq 'OW') {
	    # 島主
	    $HlbbsMode = 1;
	} else {
	    # 削除
	    $HlbbsMode = 2;
	}
	$HcurrentID = $2;

	# 削除かもしれないので、番号を取得
	$line =~ /NUMBER=([^\&]*)\&/;
	$HcommandPlanNumber = $1;

    } elsif($line =~ /ChangeInfoButton/) {
	$HmainMode = 'change';
    } elsif($line =~ /MessageButton([0-9]*)/) {
	$HmainMode = 'comment';
	$HcurrentID = $1;
    } elsif($line =~ /CommandJavaButton/) {
	$HmainMode = 'commandJava';
	$line =~ /COMARY=([^\&]*)\&/;
	$HcommandComary = $1;
    } elsif($line =~ /CommandButton/) {
	$HmainMode = 'command';

	# コマンドモードの場合、コマンドの取得
	$line =~ /NUMBER=([^\&]*)\&/;
	$HcommandPlanNumber = $1;
	$line =~ /COMMAND=([^\&]*)\&/;
	$HcommandKind = $1;
	$HdefaultKind = $1;
	$line =~ /AMOUNT=([^\&]*)\&/;
	$HcommandArg = $1;
	$line =~ /TARGETID=([^\&]*)\&/;
	$HcommandTarget = $1;
	$defaultTarget = $1;
	$line =~ /POINTX=([^\&]*)\&/;
	$HcommandX = $1;
	$HdefaultX = $1;
        $line =~ /POINTY=([^\&]*)\&/;
	$HcommandY = $1;
	$HdefaultY = $1;
	$line =~ /COMMANDMODE=(write|insert|delete)/;
	$HcommandMode = $1;
    } else {
	$HmainMode = 'top';
    }

}


#cookie入力
sub cookieInput {
    my($cookie);

    $cookie = jcode::euc($ENV{'HTTP_COOKIE'});

    if($cookie =~ /${HthisFile}OWNISLANDID=\(([^\)]*)\)/) {
	$defaultID = $1;
    }
    if($cookie =~ /${HthisFile}OWNISLANDPASSWORD=\(([^\)]*)\)/) {
	$HdefaultPassword = $1;
    }
    if($cookie =~ /${HthisFile}TARGETISLANDID=\(([^\)]*)\)/) {
	$defaultTarget = $1;
    }
    if($cookie =~ /${HthisFile}LBBSNAME=\(([^\)]*)\)/) {
	$HdefaultName = $1;
    }
    if($cookie =~ /${HthisFile}POINTX=\(([^\)]*)\)/) {
	$HdefaultX = $1;
    }
    if($cookie =~ /${HthisFile}POINTY=\(([^\)]*)\)/) {
	$HdefaultY = $1;
    }
    if($cookie =~ /${HthisFile}KIND=\(([^\)]*)\)/) {
	$HdefaultKind = $1;
    }
    if($cookie =~ /${HthisFile}IMGLINE=\(([^\)]*)\)/) {
	$HimgLine = $1;
    }
    if($cookie =~ /${HthisFile}JAVAMODE=\(([^\)]*)\)/) {
	$CjavaMode = $1;
    }
}

#cookie出力
sub cookieOutput {
    my($cookie, $info);

    # 消える期限の設定
    my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) =
	gmtime(time + 30 * 86400); # 現在 + 30日

    # 2ケタ化
    $year += 1900;
    if ($date < 10) { $date = "0$date"; }
    if ($hour < 10) { $hour = "0$hour"; }
    if ($min < 10) { $min  = "0$min"; }
    if ($sec < 10) { $sec  = "0$sec"; }

    # 曜日を文字に
    $day = ("Sunday", "Monday", "Tuesday", "Wednesday",
	    "Thursday", "Friday", "Saturday")[$day];

    # 月を文字に
    $mon = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
	    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")[$mon];

    # パスと期限のセット
    $info = "; expires=$day, $date\-$mon\-$year $hour:$min:$sec GMT\n";
    $cookie = '';
    
    if(($HcurrentID) && ($HmainMode eq 'owner')){
	$cookie .= "Set-Cookie: ${HthisFile}OWNISLANDID=($HcurrentID) $info";
    }
    if($HinputPassword) {
	$cookie .= "Set-Cookie: ${HthisFile}OWNISLANDPASSWORD=($HinputPassword) $info";
    }
    if($HcommandTarget) {
	$cookie .= "Set-Cookie: ${HthisFile}TARGETISLANDID=($HcommandTarget) $info";
    }
    if($HlbbsName) {
	$cookie .= "Set-Cookie: ${HthisFile}LBBSNAME=($HlbbsName) $info";
    }
    if($HcommandX) {
	$cookie .= "Set-Cookie: ${HthisFile}POINTX=($HcommandX) $info";
    }
    if($HcommandY) {
	$cookie .= "Set-Cookie: ${HthisFile}POINTY=($HcommandY) $info";
    }
    if($HcommandKind) {
	# 自動系以外
	$cookie .= "Set-Cookie: ${HthisFile}KIND=($HcommandKind) $info";
    }
    if($HimgLine) {
	$cookie .= "Set-Cookie: ${HthisFile}IMGLINE=($HimgLine) $info";
    }
    if($HjavaMode) {
	$cookie .= "Set-Cookie: ${HthisFile}JAVAMODE=($HjavaMode) $info";
    }
    print jcode::sjis($cookie);
}

#----------------------------------------------------------------------
# ユーティリティ
#----------------------------------------------------------------------
sub hakolock {
    if($lockMode == 1) {
	# directory式ロック
	return hakolock1();

    } elsif($lockMode == 2) {
	# flock式ロック
	return hakolock2();
    } elsif($lockMode == 3) {
	# symlink式ロック
	return hakolock3();
    } else {
	# 通常ファイル式ロック
	return hakolock4();
    }
}

sub hakolock1 {
    # ロックを試す
    if(mkdir('hakojimalock', $HdirMode)) {
	# 成功
	return 1;
    } else {
	# 失敗
	my($b) = (stat('hakojimalock'))[9];
	if(($b > 0) && ((time() -  $b)> $unlockTime)) {
	    # 強制解除
	    unlock();

	    # ヘッダ出力
	    tempHeader();

	    # 強制解除メッセージ
	    tempUnlock();

	    # フッタ出力
	    tempFooter();

	    # 終了
	    exit(0);
	}
	return 0;
    }
}

sub hakolock2 {
    open(LOCKID, '>>hakojimalockflock');
    if(flock(LOCKID, 2)) {
	# 成功
	return 1;
    } else {
	# 失敗
	return 0;
    }
}

sub hakolock3 {
    # ロックを試す
    if(symlink('hakojimalockdummy', 'hakojimalock')) {
	# 成功
	return 1;
    } else {
	# 失敗
	my($b) = (lstat('hakojimalock'))[9];
	if(($b > 0) && ((time() -  $b)> $unlockTime)) {
	    # 強制解除
	    unlock();

	    # ヘッダ出力
	    tempHeader();

	    # 強制解除メッセージ
	    tempUnlock();

	    # フッタ出力
	    tempFooter();

	    # 終了
	    exit(0);
	}
	return 0;
    }
}

sub hakolock4 {
    # ロックを試す
    if(unlink('key-free')) {
	# 成功
	open(OUT, '>key-locked');
	print OUT time;
	close(OUT);
	return 1;
    } else {
	# ロック時間チェック
	if(!open(IN, 'key-locked')) {
	    return 0;
	}

	my($t);
	$t = <IN>;
	close(IN);
	if(($t != 0) && (($t + $unlockTime) < time)) {
	    # 120秒以上経過してたら、強制的にロックを外す
	    unlock();

	    # ヘッダ出力
	    tempHeader();

	    # 強制解除メッセージ
	    tempUnlock();

	    # フッタ出力
	    tempFooter();

	    # 終了
	    exit(0);
	}
	return 0;
    }
}

# ロックを外す
sub unlock {
    if($lockMode == 1) {
	# directory式ロック
	rmdir('hakojimalock');

    } elsif($lockMode == 2) {
	# flock式ロック
	close(LOCKID);

    } elsif($lockMode == 3) {
	# symlink式ロック
	unlink('hakojimalock');
    } else {
	# 通常ファイル式ロック
	my($i);
	$i = rename('key-locked', 'key-free');
    }
}

# 小さい方を返す
sub min {
    return ($_[0] < $_[1]) ? $_[0] : $_[1];
}

# パスワードエンコード
sub encode {
    if($cryptOn == 1) {
	return crypt($_[0], 'h2');
    } else {
	return $_[0];
    }
}

# パスワードチェック
sub checkPassword {
    my($p1, $p2) = @_;

    # nullチェック
    if($p2 eq '') {
	return 0;
    }

    # マスターパスワードチェック
    if($masterPassword eq $p2) {
	return 1;
    }

    # 本来のチェック
    if($p1 eq encode($p2)) {
	return 1;
    }

    return 0;
}

# 1000億単位丸めルーチン
sub aboutMoney {
    my($m) = @_;
    if($m < 500) {
	return "推定500${HunitMoney}未満";
    } else {
	$m = int(($m + 500) / 1000);
	return "推定${m}000${HunitMoney}";
    }
}

# エスケープ文字の処理
sub htmlEscape {
    my($s) = @_;
    $s =~ s/&/&amp;/g;
    $s =~ s/</&lt;/g;
    $s =~ s/>/&gt;/g;
    $s =~ s/\"/&quot;/g; #"
    return $s;
}

# 80ケタに切り揃え
sub cutColumn {
    my($s, $c) = @_;
    if(length($s) <= $c) {
	return $s;
    } else {
	# 合計80ケタになるまで切り取り
	my($ss) = '';
	my($count) = 0;
	while($count < $c) {
	    $s =~ s/(^[\x80-\xFF][\x80-\xFF])|(^[\x00-\x7F])//;
	    if($1) {
		$ss .= $1;
		$count ++;
	    } else {
		$ss .= $2;
	    }
	    $count ++;
	}
	return $ss;
    }
}

# 島の名前から番号を得る(IDじゃなくて番号)
sub nameToNumber {
    my($name) = @_;

    # 全島から探す
    my($i);
    for($i = 0; $i < $HislandNumber; $i++) {
	if($Hislands[$i]->{'name'} eq $name) {
	    return $i;
	}
    }

    # 見つからなかった場合
    return -1;
}

# チームの名前から番号を得る(IDじゃなくて番号)
sub nameToTeamNumber {
    my($name) = @_;

    # 全島から探す
    my($i);
    for($i = 0; $i < $HteamNumber; $i++) {
	if($Hteams[$i]->{'name'} eq $name) {
	    return $i;
	}
    }

    # 見つからなかった場合
    return -1;
}

# 経験地からレベルを算出
sub expToLevel {
    my($kind, $exp) = @_;
    my($i);
    if($kind == $HlandBase) {
	# ミサイル基地
	for($i = $maxBaseLevel; $i > 1; $i--) {
	    if($exp >= $baseLevelUp[$i - 2]) {
		return $i;
	    }
	}
	return 1;
    } else {
	# 海底基地
	for($i = $maxSBaseLevel; $i > 1; $i--) {
	    if($exp >= $sBaseLevelUp[$i - 2]) {
		return $i;
	    }
	}
	return 1;
    }

}

# (0,0)から(size - 1, size - 1)までの数字が一回づつ出てくるように
# (@Hrpx, @Hrpy)を設定
sub makeRandomPointArray {
    # 初期値
    my($y);
    @Hrpx = (0..$HislandSize-1) x $HislandSize;
    for($y = 0; $y < $HislandSize; $y++) {
	push(@Hrpy, ($y) x $HislandSize);
    }

    # シャッフル
    my ($i);
    for ($i = $HpointNumber; --$i; ) {
	my($j) = int(rand($i+1)); 
	if($i == $j) { next; }
	@Hrpx[$i,$j] = @Hrpx[$j,$i];
	@Hrpy[$i,$j] = @Hrpy[$j,$i];
    }
}

# 0から(n - 1)の乱数
sub random {
    return int(rand(1) * $_[0]);
}

#----------------------------------------------------------------------
# ログ表示
#----------------------------------------------------------------------
# ファイル番号指定でログ表示
sub logFilePrint {
    my($fileNumber, $id, $mode, $kankou) = @_;
    open(LIN, "${HdirName}/hakojima.log$_[0]");
    my($line, $m, $turn, $id1, $id2, $message);
    my($fi) = 0;

    while($line = <LIN>) {
	$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),(.*)$/;
	($m, $turn, $id1, $id2, $message) = ($1, $2, $3, $4, $5);

	# 機密関係
	if($m == 1) {
	    if(($mode == 0) || ($id1 != $id)) {
		# 機密表示権利なし
		next;
	    }
	    $m = '<B>(機密)</B>';
	} else {
	    $m = '';
	}

	# 表示的確か
	if($id != 0) {
	    if(($id != $id1) &&
	       ($id != $id2)) {
		next;
	    }
	}

	# 表示
	if($kankou == 1) {

	out("<NOBR>${HtagNumber_}ターン$turn$m${H_tagNumber}：$message</NOBR><BR>\n");

    } elsif(($fi == 0) && ($mode == 0)) {
     out("<NOBR><BR><B><I><FONT COLOR='#000000' SIZE=+2>ターン$turn$m：</FONT></I></B><BR><HR width=50% align=left>\n");
	out("<NOBR>${HtagNumber_}ターン$turn$m${H_tagNumber}：$message</NOBR><BR>\n");
	  $fi++;
	} else {
	out("<NOBR>${HtagNumber_}ターン$turn$m${H_tagNumber}：$message</NOBR><BR>\n");
	}
    }
#	out("<hr>\n");
    close(LIN);
}
#----------------------------------------------------------------------
# テンプレート
#----------------------------------------------------------------------
# 初期化
sub tempInitialize {
    # 島セレクト(デフォルト自分)
    $HislandList = getIslandList($defaultID);
}

# 島データのプルダウンメニュー用
sub getIslandList {
    my($select) = @_;
    my($list, $name, $id, $s, $i);

    #島リストのメニュー
    $list = '';
    for($i = 0; $i < $HislandNumber; $i++) {
	$name = $Hislands[$i]->{'name'};
	$id = $Hislands[$i]->{'id'};
	if($id eq $select) {
	    $s = 'SELECTED';
	} else {
	    $s = '';
	}
	$list .=
	    "<OPTION VALUE=\"$id\" $s>${name}島\n";
    }
    return $list;
}

# 島データのプルダウンメニュー用
sub getTargetList {
    my($id,$tId) = @_;
    my($list, $s, $tTeam, $island, $tNumMember);
    my($team) = $Hteams[$HidToTeamNumber{$id}];
    $currentTNumber = $HidToTeamNumber{$tId};
    if($currentTNumber ne '') {
	$tTeam = $Hteams[$currentTNumber];
	$tNumMember = $tTeam->{'member'};
    }
    $list = '';

    #島リストのメニュー
    while($tNumMember =~ s/([0-9]*),//) {
	$island = $Hislands[$HidToNumber{$1}];
	if($island->{'id'} eq $defaultTarget) {
	    $s = 'SELECTED';
	} else {
	    $s = '';
	}
	$list .= "<OPTION VALUE=\"$island->{'id'}\" $s>$island->{'name'}島\n";
    }
    my($numMember) = $team->{'member'};
    while($numMember =~ s/([0-9]*),//) {
	$island = $Hislands[$HidToNumber{$1}];
	if($island->{'id'} eq $defaultTarget) {
	    $s = 'SELECTED';
	} else {
	    $s = '';
	}
	$list .= "<OPTION VALUE=\"$island->{'id'}\" $s>$island->{'name'}島\n";
    }
    return $list;
}

# ヘッダ
sub tempHeader {
	out("Content-type: text/html\n\n");
	my($HimgFlag) = 0;
	if($HimgLine eq '' || $HimgLine eq $imageDir){
	    $baseIMG = $imageDir;
	    $HimgFlag = 1;
	} else {
	    $baseIMG = $HimgLine;
	}
	$baseIMG =~ s/筑集眺餅/デスクトップ/g;
    out(<<END);
<HTML>
<HEAD>
<TITLE>
$Htitle
</TITLE>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=x-sjis">
<STYLE type="text/css">
<!--
a:link        { color:#3300CC }
a:visited     { color:#3300CC }
a:active      { color:#FF0000 }
a:hover       { color:#FF0000 }
small         { font-size: 9pt}
-->
</STYLE>
<SCRIPT Language="JavaScript">
<!--
function ShowMsg(n){
	window.status = n;
}
//-->
</SCRIPT>
<BASE HREF="$baseIMG/">
</HEAD>
$Body<nobr>
<A HREF="http://t.pos.to/hako/" target=_blank>箱庭諸島スクリプト配布元</A> / 
<A HREF="http://appoh.execweb.cx/hakoniwa/" target="_blank">箱庭Javaスクリプト版 配布元</A>
<A HREF="http://espion.just-size.jp/archives/dist_hako/" target=_blank>箱庭チームトーナメント 配布元 </A>
<BR>
<IMG SRC="$cleangif" width=0 height=3><BR>
　　<A HREF="$toppage">トップページ</A> / 
<A HREF="$bbs">$bbsname</A> / 
<A HREF="$HthisFile?LogFileView=1" target=_blank>最近の出来事</A> / 
<A HREF="$HthisFile?LogFileTeam=0" target=_blank>出来事[チーム別]</A> / 
<A HREF="$HthisFile?HELP">設定ヘルプ</A></nobr>
<DIV ALIGN=RIGHT>
</DIV>
<HR>
END
if($HimgFlag) {
    out(<<END);
<FONT COLOR=RED><B>サーバー負荷軽減の為に、画像のローカル設定を行って下さるようにお願い致します。</B></FONT><HR>
END
}
}

# フッタ
sub tempFooter {
    out(<<END);
<HR>
<P align=right>
<NOBR>
<A HREF="http://t.pos.to/hako/" target=_blank>箱庭諸島スクリプト配布元</A> / 
<A HREF="http://appoh.execweb.cx/hakoniwa/" target="_blank">箱庭Javaスクリプト版 配布元</A>
<BR>
<IMG SRC="$cleangif" width=600 height=3><BR>
<A HREF="$toppage">トップページ</A> / 
<A HREF="$bbs">$bbsname</A> / 
<A HREF="$HthisFile?LogFileView=1" target=_blank>最近の出来事</A> / 
<A HREF="$HthisFile?LogFileTeam=0" target=_blank>出来事[チーム別]</A> / 
<A HREF="$HthisFile?HELP">設定ヘルプ</A>
</nobr><BR><BR>
管理者:$adminName(<A HREF="mailto:$email">$email</A>)<BR>
</P>
</BODY>
</HTML>
END
}

# ロック失敗
sub tempLockFail {
    # タイトル
    out(<<END);
${HtagBig_}同時アクセスエラーです。<BR>
ブラウザの「戻る」ボタンを押し、<BR>
しばらく待ってから再度お試し下さい。${H_tagBig}$HtempBack
END
}

# 強制解除
sub tempUnlock {
    # タイトル
    out(<<END);
${HtagBig_}前回のアクセスが異常終了だったようです。<BR>
ロックを強制解除しました。${H_tagBig}$HtempBack
END
}

# hakojima.datがない
sub tempNoDataFile {
    out(<<END);
${HtagBig_}データファイルが開けません。${H_tagBig}$HtempBack
END
}

# パスワード間違い
sub tempWrongPassword {
    out(<<END);
${HtagBig_}パスワードが違います。${H_tagBig}$HtempBack
END
}

# メンバー最大数より多い
sub tempOverMember {
    out(<<END);
${HtagBig_}このチームにはこれ以上入れません。${H_tagBig}$HtempBack
END
}

# 何か問題発生
sub tempProblem {
    out(<<END);
${HtagBig_}問題発生、とりあえず戻ってください。${H_tagBig}$HtempBack
END
}
