#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# 地図モードモジュール(ver1.00)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# 箱庭諸島のページ: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# 箱庭チームトーナメント
# 地図モードモジュール
# $Id: hako-map.cgi,v 1.1 2003/07/02 03:09:49 gaba Exp $

#----------------------------------------------------------------------
# 観光モード
#----------------------------------------------------------------------
# メイン
sub printIslandMain {
	# 開放
	unlock();

	# idから島番号を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};

	# なぜかその島がない場合
	if($HcurrentNumber eq '') {
		tempProblem();
		return;
	}

	# 名前の取得
	$HcurrentName = $Hislands[$HcurrentNumber]->{'name'};

	# 観光画面
	tempPrintIslandHead(); # ようこそ!!
	islandInfo(); # 島の情報
	islandMap(0); # 島の地図、観光モード
	islandJump();
	# ○○島ローカル掲示板
	if($HuseLbbs) {
		tempLbbsHead();	 # ローカル掲示板
		tempLbbsInput();   # 書き込みフォーム
		tempLbbsContents(); # 掲示板内容
	}

	# 近況
	tempRecent(0);
}

#----------------------------------------------------------------------
# 開発モード
#----------------------------------------------------------------------
# メイン
sub ownerMain {
	# 開放
	unlock();

	# モードを明示
	$HmainMode = 'owner';

	# idから島を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = $island->{'name'};

	# パスワード
	if(!checkPassword($island->{'password'},$HinputPassword)) {
		# password間違い
		tempWrongPassword();
		return;
	}
	writeownerlog($HimgLine);

	# 開発画面
	if($HjavaMode eq 'java') {
		tempOwnerJava(); # 「Javaスクリプト開発計画」
	}else{			   # 「通常モード開発計画」
		tempOwner();
	}


	# ○○島ローカル掲示板
#	if($HuseLbbs) {
#		tempLbbsHead();	 # ローカル掲示板
#		tempLbbsInputOW();   # 書き込みフォーム
#		tempLbbsContents(); # 掲示板内容
#	}

	# ○○島ローカル掲示板
	if($HuseLbbs) {
		tempLbbsHead();	 # ローカル掲示板
				if($HjavaMode eq 'java') {  # Javaスクリプト用書き込みフォーム
						tempLbbsInputJava();
				}else{ tempLbbsInputOW(); } # 通常モードの書き込みフォーム
		tempLbbsContents(); # 掲示板内容
	}

	# 近況
	tempRecent(1);
}

#----------------------------------------------------------------------
# コマンドモード
#----------------------------------------------------------------------
# メイン
sub commandMain {
	# idから島を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = $island->{'name'};

	# パスワード
	if(!checkPassword($island->{'password'},$HinputPassword)) {
		# password間違い
		unlock();
		tempWrongPassword();
		return;
	}

	# モードで分岐
	my($command) = $island->{'command'};

	if($HcommandMode eq 'delete') {
		slideFront($command, $HcommandPlanNumber);
		tempCommandDelete();
	} elsif(($HcommandKind == $HcomAutoPrepare) ||
			($HcommandKind == $HcomAutoPrepare2)) {
		# フル整地、フル地ならし
		# 座標配列を作る
		makeRandomPointArray();
		my($land) = $island->{'land'};

		# コマンドの種類決定
		my($kind) = $HcomPrepare;
		if($HcommandKind == $HcomAutoPrepare2) {
			$kind = $HcomPrepare2;
		}

		my($i) = 0;
		my($j) = 0;
		while(($j < $HpointNumber) && ($i < $HcommandMax)) {
			my($x) = $Hrpx[$j];
			my($y) = $Hrpy[$j];
			if($land->[$x][$y] == $HlandWaste) {
				slideBack($command, $HcommandPlanNumber);
				$command->[$HcommandPlanNumber] = {
					'kind' => $kind,
					'target' => 0,
					'x' => $x,
					'y' => $y,
					'arg' => 0
					};
				$i++;
			}
			$j++;
		}
		tempCommandAdd();
	} elsif($HcommandKind == $HcomAutoDelete) {
		# 全消し
		my($i);
		for($i = 0; $i < $HcommandMax; $i++) {
			slideFront($command, $HcommandPlanNumber);
		}
		tempCommandDelete();
	} elsif($HcommandKind == $HcomPrepRecr) {
		# 埋め立て＋地ならし
		if($HcommandMode eq 'insert') {
			slideBack($command, $HcommandPlanNumber);
		}
		slideBack($command, $HcommandPlanNumber);
		tempCommandAdd();
		# コマンドを登録
		$command->[$HcommandPlanNumber] = {
			'kind' => $HcomReclaim,
			'target' => $HcommandTarget,
			'x' => $HcommandX,
			'y' => $HcommandY,
			'arg' => $HcommandArg
			};
		$command->[$HcommandPlanNumber + 1] = {
			'kind' => $HcomPrepare2,
			'target' => $HcommandTarget,
			'x' => $HcommandX,
			'y' => $HcommandY,
			'arg' => $HcommandArg
			};
	} else {
		if($HcommandMode eq 'insert') {
			slideBack($command, $HcommandPlanNumber);
		}
		tempCommandAdd();
		# コマンドを登録
		$command->[$HcommandPlanNumber] = {
			'kind' => $HcommandKind,
			'target' => $HcommandTarget,
			'x' => $HcommandX,
			'y' => $HcommandY,
			'arg' => $HcommandArg
			};
	}

	# データの書き出し
	writeIslandsFile($HcurrentID);

	# owner modeへ
	ownerMain();

}

#----------------------------------------------------------------------
# コメント入力モード
#----------------------------------------------------------------------
# メイン
sub commentMain {
	# idから島を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = $island->{'name'};

	# パスワード
	if(!checkPassword($island->{'password'},$HinputPassword)) {
		# password間違い
		unlock();
		tempWrongPassword();
		return;
	}

	# メッセージを更新
	$island->{'comment'} = htmlEscape($Hmessage);

	# データの書き出し
	writeIslandsFile($HcurrentID);

	# コメント更新メッセージ
	tempComment();

	# owner modeへ
	ownerMain();
}

#----------------------------------------------------------------------
# ローカル掲示板モード
#----------------------------------------------------------------------
# メイン

sub localBbsMain {
	# idから島番号を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	my($foreignName);

	# なぜかその島がない場合
	if($HcurrentNumber eq '' && $HcurrentID != 0) {
		unlock();
		tempProblem();
		return;
	}

	# 削除モードじゃなくて名前かメッセージがない場合
	if($HlbbsMode != 2) {
		if(($HlbbsName eq '') || ($HlbbsMessage eq '')) {
			unlock();
			tempLbbsNoMessage();
			return;
		}
	}

	# 島無し観光者以外はパスワードチェック
		if($HlbbsMode == 0 && $HforID != 0) {
			# 外国者モード
			my($foreignNumber) = $HidToNumber{$HforID};
			if($foreignNumber eq ''){
				unlock();
				tempProblem();
				return;
			}
			my($fIsland) = $Hislands[$foreignNumber];
			if(!checkPassword($fIsland->{'password'},$HinputPassword)) {
				unlock();
				tempWrongPassword();
				return;
			}
			$foreignName = $fIsland->{'name'};
		} elsif($HlbbsMode) {
			# 島主モード
			if(!checkPassword($island->{'password'},$HinputPassword)) {
				# password間違い
				unlock();
				tempWrongPassword();
				return;
			}
		}

	my($lbbs);
	$lbbs = $island->{'lbbs'};

	# モードで分岐
	if($HlbbsMode == 2) {
		# 削除モード
		# メッセージを前にずらす
		slideBackLbbsMessage($lbbs, $HcommandPlanNumber);
		tempLbbsDelete();
	} else {
		# 記帳モード
		# メッセージを後ろにずらす
		slideLbbsMessage($lbbs);

		if($HforID == 0 and $HlbbsMode == 0){
			$HlbbsMessage = htmlEscape($HlbbsMessage);
			$message = '3';
		} elsif (($HlbbsMode == 0) && ($HforID != $island->{'id'})){
			$HlbbsMessage = htmlEscape($HlbbsMessage) . "　　<font size=-1 color=gray>(${foreignName}島)</font>";
			$message = '0';
		} else {
			$HlbbsMessage = htmlEscape($HlbbsMessage);
			$message = '1';
		}
		$HlbbsName = "$HislandTurn：" . htmlEscape($HlbbsName);
		$lbbs->[0] = "$message>$HlbbsName>$HlbbsMessage";

		tempLbbsAdd();
	}

	# データ書き出し
	writeIslandsFile($HcurrentID);

	# もとのモードへ
	if($HlbbsMode == 0) {
		printIslandMain();
	} else {
		ownerMain();
	}
}

# ローカル掲示板のメッセージを一つ後ろにずらす
sub slideLbbsMessage {
	my($lbbs) = @_;
	my($i);
#	pop(@$lbbs);
#	push(@$lbbs, $lbbs->[0]);
	pop(@$lbbs);
	unshift(@$lbbs, $lbbs->[0]);
}

# ローカル掲示板のメッセージを一つ前にずらす
sub slideBackLbbsMessage {
	my($lbbs, $number) = @_;
	my($i);
	splice(@$lbbs, $number, 1);
	$lbbs->[$HlbbsMax - 1] = '0>>';
}

#----------------------------------------------------------------------
# 島の地図
#----------------------------------------------------------------------

# 情報の表示
sub islandInfo {
	my($island) = $Hislands[$HcurrentNumber];
	my($team) = $Hteams[$HidToTeamNumber{$island->{'teamid'}}];

	# 情報表示
	my($rank) = $HcurrentNumber + 1;
	my($farm) = $island->{'farm'};
	my($factory) = $island->{'factory'};
	$farm = ($farm == 0) ? "保有せず" : "${farm}0$HunitPop";
	$factory = ($factory == 0) ? "保有せず" : "${factory}0$HunitPop";

	my($mStr1) = '';
	my($mStr2) = '';
	if(($HhideMoneyMode == 1) || ($HmainMode eq 'owner')) {
		# 無条件またはownerモード
		$mStr1 = "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}資金${H_tagTH}</NOBR></TH>";
		$mStr2 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$team->{'money'}$HunitMoney</NOBR></TD>";
	} elsif($HhideMoneyMode == 2) {
		my($mTmp) = aboutMoney($team->{'money'});

		# 1000億単位モード
		$mStr1 = "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}資金${H_tagTH}</NOBR></TH>";
		$mStr2 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$mTmp</NOBR></TD>";
	}
	my($fightName) = '';
	my($fightMember) = '';
	if($team->{'fightid'}) {
		$fightName = "<A STYlE=\"text-decoration:none\" HREF=$HthisFile?TEAM=$team->{'fightid'}#data>${HtagTName_}$Hteams[$HidToTeamNumber{$team->{'fightid'}}]->{'name'}${H_tagTName}</A>";
		$fightMember = $Hteams[$HidToTeamNumber{$team->{'fightid'}}]->{'member'};
	} else {
		$fightName = "${HtagName_}<CENTER>− − −${H_tagName}</CENTER>";
	}
	my($comname) ="${HtagTH_}コメント：${H_tagTH}";
	if(($island->{'ownername'} ne '0') && ($island->{'ownername'} ne "コメント")){
		$comname = "<FONT COLOR=\"blue\"><B>$island->{'ownername'}：</b></font>";
	}
   if($HmainMode eq 'owner') {
		@access = stat("${teambbs}/$island->{'teamid'}.cgi");
		local($sec2,$min2,$hour2,$mday2,$mon2,$year) = localtime($access[9]);
		if($min2 < 10) { $min2 = 0 . $min2; }
		if($hour2 < 10) { $hour2 = 0 . $hour2; } $mon2++;
		$accessTime = "　　<B>戦略会議室最終更新日時</B> （$mon2/$mday2 $hour2:$min2）";
	}
#　時間表示
my($hour, $min, $sec);
my($now) = time;
my($showTIME) = ($HislandLastTime + $HunitTime - $now);
$hour = int($showTIME / 3600);
$min  = int(($showTIME - ($hour * 3600)) / 60);
$sec  = $showTIME - ($hour * 3600) - ($min * 60);

	out(<<END);
<CENTER>
<B>ターン$HislandTurn</B> （次のターンまで、$hour時間 $min分 $sec秒）
$accessTime<TABLE BORDER>
<TR>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}順位${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}所属チーム${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}対戦チーム${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}人口${H_tagTH}</NOBR></TH>
$mStr1
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}食料${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}面積${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}農場規模${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}工場規模${H_tagTH}</NOBR></TH>
</TR>
<TR>
<TD $HbgNumberCell align=middle nowrap=nowrap><NOBR>${HtagNumber_}$rank${H_tagNumber}</NOBR></TD>
<TD $HbgInfoCell align=left nowrap=nowrap><NOBR>
<A STYlE=\"text-decoration:none\" HREF=$HthisFile?TEAM=$team->{'id'}#data>${HtagTName_}$team->{'name'}${H_tagTName}</A>
</NOBR></TD>
<TD $HbgInfoCell align=left nowrap=nowrap><NOBR>$fightName</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'pop'}$HunitPop</NOBR></TD>
$mStr2
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'food'}$HunitFood</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'area'}$HunitArea</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${farm}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${factory}</NOBR></TD>
</TR><TR>
<TD $HbgCommentCell COLSPAN=9 align=left nowrap=nowrap><NOBR>$comname$island->{'comment'}


END
	if($fightMember ne '') {
		out("</NOBR></TD></TR><TR><TD $HbgCommentCell COLSPAN=9 align=left nowrap=nowrap><NOBR>${HtagTH_}対戦チームメンバー：${H_tagTH}");
		while($fightMember =~ s/([0-9]*),//) {
			my($tIsland) = $Hislands[$HidToNumber{$1}];
			out("<A STYlE=\"text-decoration:none\" HREF=$HthisFile?Sight=$tIsland->{'id'} target=_blank>${HtagName_}$tIsland->{'name'}島${H_tagName}</A>　");
		}
	}
out("</NOBR></TD></TR></TABLE></CENTER>");

}

# 地図の表示
# 引数が1なら、ミサイル基地等をそのまま表示
sub islandMap {
	my($mode) = @_;
	my($island);
	$island = $Hislands[$HcurrentNumber];

	out(<<END);
<CENTER><TABLE BORDER><TR><TD>
END
	# 地形、地形値を取得
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($l, $lv);

	# コマンド取得
	my($command) = $island->{'command'};
	my($com, @comStr, $i);
	if($HmainMode eq 'owner') {
		for($i = 0; $i < $HcommandMax; $i++) {
			my($j) = $i + 1;
			$com = $command->[$i];
			if($com->{'kind'} < 20) {
				$comStr[$com->{'x'}][$com->{'y'}] .=
					" [${j}]$HcomName[$com->{'kind'}]";
			}
		}
	}

	# 座標(上)を出力
	out("<IMG SRC=\"xbar.gif\" width=400 height=16><BR>");

	# 各地形および改行を出力
	my($x, $y);
	for($y = 0; $y < $HislandSize; $y++) {
		# 偶数行目なら番号を出力
		if(($y % 2) == 0) {
			out("<IMG SRC=\"space${y}.gif\" width=16 height=32>");
		}

		# 各地形を出力
		for($x = 0; $x < $HislandSize; $x++) {
			$l = $land->[$x][$y];
			$lv = $landValue->[$x][$y];
			landString($l, $lv, $x, $y, $mode, $comStr[$x][$y]);
		}

		# 奇数行目なら番号を出力
		if(($y % 2) == 1) {
			out("<IMG SRC=\"space${y}.gif\" width=16 height=32>");
		}

		# 改行を出力
		out("<BR>");
	}
	out("</TD></TR></TABLE></CENTER>\n");
}

sub landString {
	my($l, $lv, $x, $y, $mode, $comStr) = @_;
	my($point) = "($x,$y)";
	my($image, $alt);

	if($l == $HlandSea) {

		if($lv == 1) {
			# 浅瀬
			$image = 'land14.gif';
			$alt = '海(浅瀬)';
		} else {
			# 海
			$image = 'land0.gif';
			$alt = '海';
		}
	} elsif($l == $HlandWaste) {
		# 荒地
		if($lv == 1) {
			$image = 'land13.gif'; # 着弾点
			$alt = '荒地';
		} else {
			$image = 'land1.gif';
			$alt = '荒地';
		}
	} elsif($l == $HlandPlains) {
		# 平地
		$image = 'land2.gif';
		$alt = '平地';
	} elsif($l == $HlandForest) {
		# 森
		if($mode == 1) {
			$image = 'land6.gif';
			$alt = "森(${lv}$HunitTree)";
		} else {
			# 観光者の場合は木の本数隠す
			$image = 'land6.gif';
			$alt = '森';
		}
	} elsif($l == $HlandTown) {
		# 町
		my($p, $n);
		if($lv < 30) {
			$p = 3;
			$n = '村';
		} elsif($lv < 100) {
			$p = 4;
			$n = '町';
		} else {
			$p = 5;
			$n = '都市';
		}

		$image = "land${p}.gif";
		$alt = "$n(${lv}$HunitPop)";
	} elsif($l == $HlandFarm) {
		# 農場
		$image = 'land7.gif';
		$alt = "農場(${lv}0${HunitPop}規模)";
	} elsif($l == $HlandFactory) {
		# 工場
		$image = 'land8.gif';
		$alt = "工場(${lv}0${HunitPop}規模)";
	} elsif($l == $HlandBase) {
		if($mode == 0) {
			# 観光者の場合は森のふり
			$image = 'land6.gif';
			$alt = '森';
		} else {
			# ミサイル基地
			my($level) = expToLevel($l, $lv);
			$image = 'land9.gif';
			$alt = "ミサイル基地 (レベル ${level}/経験値 $lv)";
		}
	} elsif($l == $HlandDefence) {
		# 防衛施設
		if($mode == 0) {
			# 観光者の場合は森のふり
			$image = 'land6.gif';
			$alt = '森';
		} else {
			$image = 'land10.gif';
			$alt = '防衛施設';
		}
	} elsif($l == $HlandHaribote) {
		# ハリボテ
		$image = 'land10.gif';
		if($mode == 0) {
			# 観光者の場合は防衛施設のふり
			$alt = '防衛施設';
		} else {
			$alt = 'ハリボテ';
		}
	} elsif($l == $HlandMonument) {
		# 記念碑
		$image = $HmonumentImage[$lv];
		$alt = $HmonumentName[$lv];
	}


	# 開発画面の場合は、座標設定
	if($mode == 1) {
		out("<A HREF=\"JavaScript:void(0);\" onclick=\"ps($x,$y)\" onMouseOver=\"ShowMsg('$point $alt $comStr'); return true;\">");
	} else{
		out("<A HREF=\"JavaScript:void(0);\" onMouseOver=\"ShowMsg('$point $alt $comStr'); return true;\">");
	}

	out("<IMG SRC=\"$image\" ALT=\"$point $alt $comStr\" width=32 height=32 BORDER=0>");

	# 座標設定閉じ
	out("</A>");
}


#----------------------------------------------------------------------
# テンプレートその他
#----------------------------------------------------------------------
# 個別ログ表示
sub logPrintLocal {
	my($mode) = @_;
	my($i);
	for($i = 0; $i < $HlogMax; $i++) {
		logFilePrint($i, $HcurrentID, $mode, 1);
	}
}

# ○○島へようこそ！！
sub tempPrintIslandHead {
	out(<<END);
<CENTER>
${HtagBig_}${HtagName_}「${HcurrentName}島」${H_tagName}へようこそ！！${H_tagBig}<BR>
$HtempBack<BR>
</CENTER>
END
}

# ○○島開発計画
sub tempOwner {
	my($island);
	$island = $Hislands[$HcurrentNumber];
	my($team) = $Hteams[$HidToTeamNumber{$island->{'teamid'}}];
	out(<<END);
<CENTER>
${HtagBig_}${HtagName_}${HcurrentName}島${H_tagName}開発計画${H_tagBig}<BR>
$HtempBack<BR>

<SCRIPT Language="JavaScript">
<!--
function ps(x, y) {
	document.forms[0].elements[4].options[x].selected = true;
	document.forms[0].elements[5].options[y].selected = true;
	return true;
}

function ns(x) {
	document.forms[0].elements[2].options[x].selected = true;
	return true;
}
function openBBS()
{
  document.bbsform.submit();
}

function openTEAM()
{
  document.teamform.submit();
}
//-->
</SCRIPT>

</CENTER>

END

	islandInfo();

	out(<<END);
<CENTER>
<TABLE BORDER>
<TR>
<TD $HbgInputCell >
<CENTER>
<FORM name="myForm" action="$HthisFile" method=POST>
<INPUT TYPE=submit VALUE="計画送信" NAME=CommandButton$island->{'id'}>
<HR>
<B>パスワード</B></BR>
<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword">
<HR>
<B>計画番号</B><SELECT NAME=NUMBER>
END
	# 計画番号
	my($j, $i);
	for($i = 0; $i < $HcommandMax; $i++) {
		$j = $i + 1;
		out("<OPTION VALUE=$i>$j\n");
	}

	out(<<END);
</SELECT><BR>
<HR>
<B>開発計画</B><BR>
<SELECT NAME=COMMAND>
END

	#コマンド
	my($kind, $cost, $s);
	for($i = 0; $i < $HcommandTotal; $i++) {
		$kind = $HcomList[$i];
		$cost = $HcomCost[$kind];
		if($cost == 0) {
			$cost = '無料'
		} elsif($cost < 0) {
			$cost = - $cost;
			$cost .= $HunitFood;
		} else {
			$cost .= $HunitMoney;
		}
		if($kind == $HdefaultKind) {
			$s = 'SELECTED';
		} else {
			$s = '';
		}
#		print "<OPTION VALUE=$kind $s>$HcomName[$kind]($cost)\n";
		out("<OPTION VALUE=$kind $s>$HcomName[$kind]($cost)\n");
	}

	out(<<END);
</SELECT>
<HR>
<B>座標(</B>
<SELECT NAME=POINTX>

END
	for($i = 0; $i < $HislandSize; $i++) {
		if($i == $HdefaultX) {
			out("<OPTION VALUE=$i SELECTED>$i\n");
		} else {
			out("<OPTION VALUE=$i>$i\n");
		}
	}

	out(<<END);
</SELECT>, <SELECT NAME=POINTY>
END

	for($i = 0; $i < $HislandSize; $i++) {
		if($i == $HdefaultY) {
			out("<OPTION VALUE=$i SELECTED>$i\n");
		} else {
			out("<OPTION VALUE=$i>$i\n");
		}
	}
	out(<<END);
</SELECT><B>)</B>
<HR>
<B>数量</B><SELECT NAME=AMOUNT>
END

	# 数量
	for($i = 0; $i < 50; $i++) {
		out("<OPTION VALUE=$i>$i\n");
	}

	out(<<END);
</SELECT>
<HR>
<B>目標の島</B><BR>
<SELECT NAME=TARGETID>
END
out(getTargetList($team->{'id'},$team->{'fightid'}));
	out(<<END);
<BR>
</SELECT>
<HR>
<B>動作</B><BR>
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=insert CHECKED>挿入
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=write>上書き<BR>
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=delete>削除
<HR>
<INPUT TYPE=submit VALUE="計画送信" NAME=CommandButton$island->{'id'}>

</CENTER>
</FORM>
<FORM NAME=bbsform ACTION="${baseDir}/${teambbs}/bbs.cgi" METHOD=POST TARGET=_blank>
<INPUT TYPE=HIDDEN NAME=teamID VALUE=$team->{'id'}>
<INPUT TYPE=HIDDEN NAME=tPASS VALUE=$team->{'password'}>
</FORM>
<FORM NAME=teamform ACTION=$HthisFile METHOD=POST TARGET=_blank>
<INPUT TYPE=HIDDEN NAME=TEAMID VALUE=$team->{'id'}>
<INPUT TYPE=HIDDEN NAME=PASSWORD2 VALUE=$team->{'password'}>
<INPUT TYPE=HIDDEN NAME=teamData VALUE=''>
</FORM>
<nobr><center>ミサイル発射上限数[<b> $island->{'fire'} </b>]発</center></nobr>
</TD>
<TD $HbgMapCell ALIGN=CENTER>
<FONT SIZE=+1><B>
<A HREF="JavaScript:void(0);" STYlE="text-decoration:none" onClick="openBBS();return false;">
戦略会議室へ</A>
　　　　　
<A HREF="JavaScript:void(0);" STYlE="text-decoration:none" onClick="openTEAM();return false;">
 作戦本部へ </A>
</B>
</FONT>
END
	islandMap(1);	# 島の地図、所有者モード
	out(<<END);
</TD>
<TD $HbgCommandCell>
END
	for($i = 0; $i < $HcommandMax; $i++) {
		tempCommand($i, $island->{'command'}->[$i]);
	}

	out(<<END);

</TD>
</TR>
</TABLE>
</CENTER>
<HR>
<CENTER>
${HtagBig_}コメント更新${H_tagBig}<BR>
<FORM action="$HthisFile" method="POST">
コメント<INPUT TYPE=text NAME=MESSAGE SIZE=80 VALUE="$island->{'comment'}"><BR>
パスワード<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword">
<INPUT TYPE=submit VALUE="コメント更新" NAME=MessageButton$island->{'id'}>
</FORM>
</CENTER>
END

}

# 入力済みコマンド表示
sub tempCommand {
	my($number, $command) = @_;
	my($kind, $target, $x, $y, $arg) =
		(
		 $command->{'kind'},
		 $command->{'target'},
		 $command->{'x'},
		 $command->{'y'},
		 $command->{'arg'}
		 );
	my($name) = "$HtagComName_${HcomName[$kind]}$H_tagComName";
	my($point) = "$HtagName_($x,$y)$H_tagName";
	$target = $HidToName{$target};
	if($target eq '') {
		$target = "無人";
	}
	$target = "$HtagName_${target}島$H_tagName";
	my($value) = $arg * $HcomCost[$kind];
	if($value == 0) {
		$value = $HcomCost[$kind];
	}
	if($value < 0) {
		$value = -$value;
		$value = "$value$HunitFood";
	} else {
		$value = "$value$HunitMoney";
	}
	$value = "$HtagName_$value$H_tagName";

	my($j) = sprintf("%02d：", $number + 1);

	out("<A STYlE=\"text-decoration:none\" HREF=\"JavaScript:void(0);\" onClick=\"ns($number)\"><NOBR>$HtagNumber_$j$H_tagNumber<FONT COLOR=\"$HnormalColor\">");

	if(($kind == $HcomDoNothing) || ($kind == $HcomAutoPrepare3) ||
	   ($kind == $HcomGiveup)) {
		out("$name");
	} elsif(($kind == $HcomMissileNM) ||
			($kind == $HcomMissilePP)) {
		# ミサイル系
		my($n) = ($arg == 0 ? '無制限' : "${arg}発");
		out("$target$pointへ$name($HtagName_$n$H_tagName)");
	} elsif($kind == $HcomSell) {
		# 食料輸出
		out("$name$value");
	} elsif($kind == $HcomPropaganda) {
		# 誘致活動
		out("$name");
	} elsif($kind == $HcomFood) {
		# 援助
		out("$targetへ$name$value");
	} elsif($kind == $HcomDestroy) {
		# 掘削
		if($arg != 0) {
			out("$pointで$name(予算${value})");
		} else {
			out("$pointで$name");
		}
	} elsif(($kind == $HcomFarm) ||
			 ($kind == $HcomFactory)) {		
		# 回数付き
		if($arg == 0) {
			out("$pointで$name");
		} else {
			out("$pointで$name($arg回)");
		}
	} else {
		# 座標付き
		out("$pointで$name");
	}

	out("</FONT></NOBR></A><BR>");
}

# ローカル掲示板
sub tempLbbsHead {
	out(<<END);
<CENTER>
<HR>
${HtagBig_}${HtagName_}${HcurrentName}島${H_tagName}観光者通信${H_tagBig}<BR>
</CENTER>
END
}

# ローカル掲示板入力フォーム
sub tempLbbsInput {
	out(<<END);
<CENTER>
<FORM action="$HthisFile" method="POST">
<font color=red><B>島が無い方も記帳できます。又、ゲーム内容に関係の無い発言は、出来るだけ、${bbsname}へお願いします。</b></font>
<TABLE BORDER>
<TR>
<TH>名前</TH>
<TH>内容</TH>
</TR>
<TR>
<TD><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD><INPUT TYPE="text" SIZE=80 NAME="LBBSMESSAGE"></TD>
</TR>
<TR>
<TD colspan="2">自分の島：
<SELECT NAME="ISLANDID">
<OPTION value="0">島無い観光者
$HislandList</SELECT>
　パスワード：<INPUT TYPE="password" SIZE=32 MAXLENGTH=32 NAME=PASSWORD VALUE="$HdefaultPassword">
<INPUT TYPE="submit" VALUE="記帳する" NAME="LbbsButtonFO$HcurrentID"></TD>
</TR>
</TABLE>
</FORM>
</CENTER>
END
}

# ローカル掲示板入力フォーム owner mode用
sub tempLbbsInputOW {
	out(<<END);
<CENTER>
<FORM action="$HthisFile" method="POST">
<TABLE BORDER>
<TR>
<TH>名前</TH>
<TH COLSPAN=2>内容</TH>
</TR>
<TR>
<TD><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD COLSPAN=2><INPUT TYPE="text" SIZE=80 NAME="LBBSMESSAGE"></TD>
</TR>
<TR>
<TH>パスワード</TH>
<TH COLSPAN=2>動作</TH>
</TR>
<TR>
<TD><INPUT TYPE=password SIZE=32 MAXLENGTH=32 NAME=PASSWORD VALUE="$HdefaultPassword"></TD>
<TD align=right>
<INPUT TYPE="submit" VALUE="記帳する" NAME="LbbsButtonOW$HcurrentID">
</TD>
<TD align=right>
番号
<SELECT NAME=NUMBER>
END
	# 発言番号
	my($j, $i);
	for($i = 0; $i < $HlbbsMax; $i++) {
		$j = $i + 1;
		out("<OPTION VALUE=$i>$j\n");
	}
	out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="削除する" NAME="LbbsButtonDL$HcurrentID">
</TD>
</TR>
</TABLE>
</FORM>
</CENTER>
END
}

# ローカル掲示板内容
sub tempLbbsContents {
	my($lbbs, $line);
	$lbbs = $Hislands[$HcurrentNumber]->{'lbbs'};
	out(<<END);
<CENTER>
<TABLE BORDER>
<TR>
<TH>番号</TH>
<TH>記帳内容</TH>
</TR>
END

	my($i);
	for($i = 0; $i < $HlbbsMax; $i++) {
		$line = $lbbs->[$i];
		if($line =~ /([0-9]*)\>(.*)\>(.*)$/) {
			my($j) = $i + 1;
			out("<TR><TD align=center>$HtagNumber_$j$H_tagNumber</TD>");
			if($1 == 0) {
				# 観光者
				out("<TD>$HtagLbbsSS_$2 > $3$H_tagLbbsSS</TD></TR>");
			} elsif($1 == 3) {
				# 島無し観光者
				out("<TD>$HtagLbbsSK_$2 > $3$H_tagLbbsSK</TD></TR>");
			} else {
				# 島主
				out("<TD>$HtagLbbsOW_$2 > $3$H_tagLbbsOW</TD></TR>");
			}
		}
	}

	out(<<END);
</TD></TR></TABLE></CENTER>
END
}

# ローカル掲示板で名前かメッセージがない場合
sub tempLbbsNoMessage {
	out(<<END);
${HtagBig_}名前または内容の欄が空欄です。${H_tagBig}$HtempBack
END
}

# 書きこみ削除
sub tempLbbsDelete {
	out(<<END);
${HtagBig_}記帳内容を削除しました${H_tagBig}<HR>
END
}

# コマンド登録
sub tempLbbsAdd {
	out(<<END);
${HtagBig_}記帳を行いました${H_tagBig}<HR>
END
}

# コマンド削除
sub tempCommandDelete {
	out(<<END);
${HtagBig_}コマンドを削除しました${H_tagBig}<HR>
END
}

# コマンド登録
sub tempCommandAdd {
	out(<<END);
${HtagBig_}コマンドを登録しました${H_tagBig}<HR>
END
}

# コメント変更成功
sub tempComment {
	out(<<END);
${HtagBig_}コメントを更新しました${H_tagBig}<HR>
END
}

# 近況
sub tempRecent {
	my($mode) = @_;
	out(<<END);
<HR>
${HtagBig_}${HtagName_}${HcurrentName}島${H_tagName}の近況${H_tagBig}<BR>
END
	logPrintLocal($mode);
}

#開発者訪問ログを作成する
sub writeownerlog {
	my($view) = @_;
	if($view eq '') { $view = 'NO'; } else { $view = 'LOCAL'; }
	if($HjavaMode eq 'java') { $wJavaMode = 'JS'; } else { $wJavaMode = 'NO'; }
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$id = $island->{'id'};
	my($team) = $Hteams[$HidToTeamNumber{$island->{'teamid'}}];

	my($userName, $userIP);
	my($sec, $min, $hour, $day, $month, $Year, $wday, $isdst) = localtime;
	$month ++;
	$Year += 1900;
	my($log_file) = "access_log/tag_" . $month . "-" . $day . ".cgi";
	#まず書き出す
	open(OwOut, ">>${log_file}");
		$userIP = $ENV{'REMOTE_ADDR'};

		printf OwOut "%04d\/%02d\/%02d %02d:%02d:%02d", $Year, $month, $day, $hour, $min, $sec;
		print OwOut jcode::sjis(", $userIP, ${HcurrentName}島, $team->{'name'}, ${view}, ${wJavaMode}\n");

	close(OwOut);

}
sub islandJump {
	out(<<END);

<CENTER>
<FORM action="$HthisFile" method="GET">
<SELECT NAME="Sight">
END
out(getIslandList($HcurrentID));
	out(<<END);
</SELECT>
<input type="submit" value=" GO ">
</FORM>
</CENTER>
END

}
1;
