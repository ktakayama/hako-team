#----------------------------------------------------------------------
# 箱庭チームトーナメント 追加モジュール
# ドン・ガバチョ：　support@mc.neweb.ne.jp
# 箱庭緒島 http://espion.s7.xrea.com/tyotou/
# ご質問は受けつけておりません
#----------------------------------------------------------------------
# 箱庭チームトーナメント
# 追加モジュール
# $Id: hako-more.cgi,v 1.1 2003/07/02 03:09:49 gaba Exp $

#----------------------------------------------------------------------
# ログ表示モード
#----------------------------------------------------------------------
# メイン
sub logViewMain {

    # 開放
    unlock();

    # テンプレート出力
    tempLogPage();
}

sub tempLogPage {

    out(<<END);

<font size=+3><b>${HtagHeader_}最近の出来事${H_tagHeader}</b></font>　
　<a href="$HthisFile?LogFileView=1"><FONT COLOR="blue" size=2><B>現ターン</a>
　<a href="$HthisFile?LogFileView=2">2ターン分表示</a>
END
for($i = 3; $i -1 < $HlogMax; $i++) {
	out("　<a href=\"$HthisFile?LogFileView=${i}\">${i}ターン分</a>\n");
}
    out(<<END);
</b></font><br>
END
    logPrintTop();

}

# ログ表示
sub logPrintTop {
    my($i);
    for($i = 0; $i < $Hlogturn; $i++) {
	out("<hr>\n");
	logFilePrint($i, 0, 0);

    }
}

#----------------------------------------------------------------------
# 設定ヘルプモード
#----------------------------------------------------------------------
# メイン
# ヘルプページ
sub helpMain {

    # 開放
    unlock();
my($devrep) = '';
my($firep) = '';
my($unit) = $HunitTime / 3600;
my($fiunit) = $HfightTime / 3600;

if($HdevRepTurn > 1){ $devrep = '（' . $HdevRepTurn . 'ターンまとめて更新）'; }
if($HfigRepTurn > 1){ $firep = '（' . $HfigRepTurn . 'ターンまとめて更新）'; }

    out(<<END);
${HtagTitle_}設定ヘルプ${H_tagTitle}
<BR><BR><BR>

<H1>${HtagHeader_}各種設定値${H_tagHeader}</H1>
<table width=300 border $HbgNameCell>
<TR>
<TD colspan=2 $HbgTitleCell>${HtagTH_}島数関係${H_tagTH}</TD>
</TR>
<TR>
<TD>　${HtagName_}チーム数${H_tagName}　</TD><TD><B>$teamNumチーム</b></TD>
</TR>
<TR>
<TD>　${HtagName_}メンバー数${H_tagName}　</TD><TD><B>$HmenberCount島</b></TD>
</TR>
<TR><TD>　${HtagName_}予選突破${H_tagName}</TD><TD><B>$yteamNumチーム</b></TD>
</TR>
<TR>
<TD colspan=2 $HbgTitleCell>${HtagTH_}島の初期値${H_tagTH}</TD>
</TR>
<TR><TD>　${HtagName_}面積${H_tagName}　</TD><TD><B>${HlandSizeValue}${HunitArea}</b></TD></TR>
<TR><TD>　${HtagName_}荒地の数${H_tagName}</TD><TD><B>10ヶ所</b></TD></TR>
<TR><TD>　${HtagName_}浅瀬の数${H_tagName}</TD><TD><B>${HseaNum}ヶ所</b></TD></TR>
<TR><TD>　${HtagName_}ミサイル基地の数${H_tagName}　</TD><TD><B>${HlandFirstMiss}機</b></TD></TR>
<TR><TD>　${HtagName_}資金${H_tagName}　</TD><TD><B>${HinitialMoney}${HunitMoney}</b></TD></TR>
<TR><TD>　${HtagName_}食料${H_tagName}　</TD><TD><B>${HinitialFood}${HunitFood}</b></TD></TR>

<TR>
<TD colspan=2 $HbgTitleCell>${HtagTH_}その他設定値${H_tagTH}</TD>
</TR>
<TR><TD>　${HtagName_}自動放棄ターン${H_tagName}</TD><TD><B>${HgiveupTurn}ターン</b></TD></TR>
<TR><TD>　${HtagName_}最大コマンド入力数${H_tagName}</TD><TD><B>${HcommandMax}個</b></TD></TR>
</table>
<BR><HR>
<H1>${HtagHeader_}ターン進行ヘルプ${H_tagHeader}</H1>
<table width=300 border $HbgNameCell>
<TR>
<TD colspan=2 $HbgTitleCell>${HtagTH_}ターン更新時間${H_tagTH}</TD>
</TR>
<TR>
<td WIDTH=100><NOBR>　${HtagName_}開発期間${H_tagName}</NOBR></TD><TD NOWRAP><B>$unit時間</b>　${devrep}</TD>
</TR>
<TR><TD><NOBR>　${HtagName_}戦闘期間${H_tagName}</NOBR></TD><TD NOWRAP><B>$fiunit時間</b>　${firep}</TD>
</TR>
<TR>
<TD colspan=2 $HbgTitleCell>${HtagTH_}各期間のターン数${H_tagTH}</TD>
</TR>
<TR>
<TD>　${HtagName_}予選${H_tagName}　</TD><TD><B>$HyosenTurnターンまで</b></TD>
</TR>
<TR><TD>　${HtagName_}開発期間${H_tagName}</TD><TD><B><NOBR>$HdevTurnターン</NOBR></b></TD>
</TR>
<TR><TD NOWRAP>　${HtagName_}戦闘期間${H_tagName}</TD><TD NOWRAP><B>$HfigTurnターン</b> (決勝戦は + $HfigRepTurnターン)</TD>
</TR>
</table>
END

my($fitone) = $HdevTurn + $HyosenTurn;
my($fittwo) = $fitone + $HfigTurn;
my($fitNum) = 1;
    out(<<END);
<BR><HR>
<H1>${HtagHeader_}ターン進行行程 簡易早見表${H_tagHeader}</H1>
<table height=125 border $HbgNameCell>
<TR>
<td>${HtagName_}予選${H_tagName}</td>
<TD $HbgCommentCell><B>0　〜　$HyosenTurn</B></td>
</tr>
END

for($i = 2;$i <= $yteamNum;$i*=2) {

    if($i >= $yteamNum) { $fittwo += $HfigRepTurn; }

    out(<<END);
<TR>
<TD>$tes${HtagName_}第$fitNum回戦開発期間${H_tagName}</td>
<TD $HbgCommentCell><B>$HyosenTurn　〜　$fitone</b></td>
</tr>
<TR>
<TD align=right>${HtagName_}戦闘期間${H_tagName}</td><TD $HbgCommentCell><B>
END

    out (($fitone + 1) . "　〜　$fittwo</b></td></tr>\n");
    $fitNum++;
    $HyosenTurn = $fittwo + 1;
    $fitone = $HyosenTurn + $HdevTurn - 1;
    $fittwo = $fitone + $HfigTurn;
}

    out(<<END);
</table>
<BR>
<hr><center>$HtempBack</center></hr>
END

}

#----------------------------------------------------------------------
# 作戦本部モード
#----------------------------------------------------------------------
# メイン
sub teamDataMain {

    my($currentTID) = $HidToTeamNumber{$HteamID};
    my($team) = $Hteams[$currentTID];
    my($trank) = $currentTID + 1;
    # なぜかそのチームがない場合
    if($currentTID eq '') {
	unlock();
	tempProblem();
	return;
    }
    if($team->{'password'} ne $HinputPassword2) {
	unlock();
	tempWrongPassword();
	return;
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
${HtagBig_}${HtagTName_}$team->{'name'}${H_tagTName}作戦本部${H_tagBig}<P>
チームパスワード【 $team->{'password'} 】
<P>
<B>ターン$HislandTurn</B> （次のターンまで、$hour時間 $min分 $sec秒）
<TABLE BORDER>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}順位${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}チーム${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}対戦チーム${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}人口${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}資金${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}食料${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}農場規模${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}工場規模${H_tagTH}</NOBR></TH>
</TR>
END
	$id = $team->{'id'};
	$tfarm = $team->{'farm'};
	$tfactory = $team->{'factory'};
	$tfarm = ($tfarm == 0) ? "保有せず" : "${tfarm}0$HunitPop";
	$tfactory = ($tfactory == 0) ? "保有せず" : "${tfactory}0$HunitPop";
	my($fightName) = '';
	my($fightMember) = '';
	if($team->{'fightid'} > 0) {
	    $fightName = "<A STYlE=\"text-decoration:none\" HREF=$HthisFile?TEAM=$team->{'fightid'}#data>${HtagTName_}$Hteams[$HidToTeamNumber{$team->{'fightid'}}]->{'name'}${H_tagTName}</A>";
	    $fightMember = $Hteams[$HidToTeamNumber{$team->{'fightid'}}]->{'member'};
	} else {
	    $fightName = "${HtagName_}<CENTER>− − −${H_tagName}</CENTER>";
	}

	    $mStr1 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$team->{'money'}$HunitMoney</NOBR></TD>";
	out(<<END);
<TR>
<TD $HbgNumberCell ROWSPAN=2 align=center nowrap=nowrap><NOBR>${HtagNumber_}${trank}${H_tagNumber}</NOBR></TD>
<TD $HbgNameCell align=left nowrap=nowrap>
<NOBR>${HtagTName_}$team->{'name'}${H_tagTName}</NOBR></TD>
<TD $HbgNameCell align=left nowrap=nowrap>
<NOBR>${fightName}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><A NAME=team$team->{'id'}>
<NOBR>$team->{'pop'}$HunitPop</NOBR></TD>
$mStr1
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$team->{'food'}$HunitFood</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$tfarm</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$tfactory
END
    if($fightMember ne '') {
	out("</NOBR></TD></TR><TR><TD $HbgCommentCell COLSPAN=9 align=left nowrap=nowrap><NOBR>${HtagTH_}対戦チームメンバー：${H_tagTH}");
	while($fightMember =~ s/([0-9]*),//) {
	    my($tIsland) = $Hislands[$HidToNumber{$1}];
	    out("<A STYlE=\"text-decoration:none\" HREF=$HthisFile?Sight=$tIsland->{'id'}>${HtagName_}$tIsland->{'name'}島${H_tagName}</A>　");
	}
    }
    out(<<END);
</NOBR></TD>
</TR></TABLE>
<P>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}順位${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}島${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}人口${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}食料${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}面積${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}農場規模${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}工場規模${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}ミサイル${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}防衛施設${H_tagTH}</NOBR></TH>
</TR>
END
    my($numMember) = $team->{'member'};
    while($numMember =~ s/([0-9]*),//) {
	$iNumber = $HidToNumber{$1};
	push(@islanddata,$iNumber);
    }
    @islanddata = sort { $a <=> $b } @islanddata;
for($g = 0;$g < $HmenberCount;$g++) {
	$iNumber = $islanddata[$g];
	if($iNumber eq '') { last; }
	
	readIslandsFile($Hislands[$islanddata[$g]]->{'id'});
	$island = $Hislands[$iNumber];
	# 情報表示
	my($rank) = $iNumber + 1;
	my($farm) = $island->{'farm'};
	my($factory) = $island->{'factory'};
	$farm = ($farm == 0) ? "保有せず" : "${farm}0$HunitPop";
	$factory = ($factory == 0) ? "保有せず" : "${factory}0$HunitPop";
	my($comname) ="${HtagTH_}コメント：${H_tagTH}";
	if(($island->{'ownername'} ne '0') && ($island->{'ownername'} ne "コメント")){
	    $comname = "<FONT COLOR=\"blue\"><B>$island->{'ownername'}：</b></font>";
	}
	if($island->{'absent'}  == 0) {
		$name = "${HtagName_}$island->{'name'}島${H_tagName}";
	} else {
	    $name = "${HtagName2_}$island->{'name'}島($island->{'absent'})${H_tagName2}";
	}
	out(<<END);
<TR>
<TD $HbgNumberCell ROWSPAN=3 align=middle nowrap=nowrap><NOBR>${HtagNumber_}$rank${H_tagNumber}</NOBR></TD>
<TD $HbgInfoCell ROWSPAN=2 nowrap=nowrap><NOBR>
<A STYlE=\"text-decoration:none\" HREF=$HthisFile?Sight=$island->{'id'} target=_blank>$name</A>
</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'pop'}$HunitPop</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'food'}$HunitFood</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'area'}$HunitArea</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${farm}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${factory}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'fire'}発</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'defence'}基</NOBR></TD>
</TR>
<TR>
<TD $HbgCommentCell COLSPAN=7 nowrap=nowrap><NOBR>$comname$island->{'comment'}</NOBR>
</TD>
<TR>
<TD $HbgInfoCell COLSPAN=3 nowrap=nowrap>
END
    for($i = 0; $i < 6; $i++) {
	if($i == 3) {
	    out("</TD><TD $HbgInfoCell COLSPAN=5 nowrap=nowrap VALIGN=TOP>");
	}
	tempCommand($i, $island->{'command'}->[$i]);
    }
	out(<<END);

</TD></TR>
END
    }

    unlock();

	out(<<END);

</TABLE>
<SCRIPT language=JavaScript>
<!--
    function chengeTeamName() {
	CTNAME = window.open("", 'CTNAME', 'menubar=no,toolbar=no,location=no,directories=no,status=no,scrollbars=no,resizable=no,width=750,height=250');
    }
//-->
</SCRIPT>

<FORM ACTION=$HthisFile METHOD=POST TARGET="CTNAME">
<INPUT TYPE=HIDDEN NAME=TEAMID VALUE=$team->{'id'}>
<INPUT TYPE=HIDDEN NAME=PASSWORD2 VALUE=$team->{'password'}>
<INPUT TYPE=TEXT NAME=CTEAMNAME VALUE="$team->{'name'}" SIZE="25">　
<INPUT TYPE=SUBMIT VALUE="チーム名変更" onClick="chengeTeamName()" name=ChangeTeamName>
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

    out("<NOBR>$HtagNumber_$j$H_tagNumber<FONT COLOR=\"$HnormalColor\">");

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
	out("$pointで$name");
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

    out("</FONT></NOBR><BR>");
}

#----------------------------------------------------------------------
# チーム別ログ表示モード
#----------------------------------------------------------------------
# メイン
sub logTeamMain {
    # 開放
    unlock();

    # テンプレート出力
    tempTeamLogPage();
}

sub tempTeamLogPage {
    my($HcurrentTNumber) = $HidToTeamNumber{$HlogteamID};
    my($team) = $Hteams[$HcurrentTNumber];
    # なぜかそのチームがない場合
    if($HcurrentTNumber eq '' and $HlogteamID != 0) {
	tempProblem();
	return;
    }
    if($HlogteamID != 0) { $tName = $team->{'name'}; } else { $tName = 'チーム別'; }
    out(<<END);
<CENTER>
<font size=+3><b>${HtagHeader_}${HtagName_}$tName ${H_tagName}最近の出来事${H_tagHeader}</b></font>
<FORM ACTION=$HthisFile METHOD=GET>
<SELECT NAME=LogFileTeam>
END
    for($i = 0; $i < $HteamNumber; $i++) {
	my($tTeam) = $Hteams[$i];
	out("<OPTION VALUE=$tTeam->{'id'}>$tTeam->{'name'}\n");
    }
    out(<<END);
</SELECT>
<INPUT TYPE=SUBMIT VALUE="表示">
</FORM>
</CENTER>
END
    if($HlogteamID != 0) { logPrintTeamTop($team); }

}

# ログ表示
sub logPrintTeamTop {
    my($i,$f) = (0,0);
    my($team) = @_;
    my($numMember) = $team->{'member'};
    while($numMember =~ s/([0-9]*),//) {
	my($HcurrentNumber) = $HidToNumber{$1};
	my($island) = $Hislands[$HcurrentNumber];
	$teamLog[$f] = $island->{'id'};
	$f++;
    }
    for($i = 0; $i < 3; $i++) {
	out("<hr>\n");
	for($j = 0; $j <= $#teamLog; $j++) {
	    logFilePrint($i, $teamLog[$j], 0, 1);
	}
    }
}

#----------------------------------------------------------------------
# 情報変更モード
#----------------------------------------------------------------------
# メイン
sub changeTeamNameMain {
    # idから島を取得
    my($currentTID) = $HidToTeamNumber{$HteamID};
    my($team) = $Hteams[$currentTID];
    $tempclose = '</TD><TD><INPUT TYPE="BUTTON" VALUE="  CLOSE  " onClick="top.close();"></TD></TR></TABLE>';
    # なぜかそのチームがない場合
    if($currentTID eq '') {
	unlock();
	tempProblem();
	return;
    }
    if($team->{'password'} ne $HinputPassword2) {
	unlock();
	tempWrongPassword();
	return;
    }
    out ("<TABLE><TR><TD>\n");

    if($teamName ne '') {
	# 名前変更の場合	
	# 名前が正当かチェック
	if($teamName =~ /[,\?\(\)\<\>]|^無人$/) {
	    # 使えない名前
	    unlock();
	    tempNewTeamBadName();
	    return;
	}

	# 名前の重複チェック
	if(nameToTeamNumber($teamName) != -1){
	    # すでに発見ずみ
	    unlock();
	    tempNewTeamAlready();
	    return;
	}

	# 名前を変更
	logChangeName($team->{'name'}, $teamName);
	$team->{'name'} = $teamName;
    } else {
	unlock();
	tempChangeNothing();
	return;
    }

    for($i = 0; $i < $HteamNumber; $i++) {
	my($team) = $Hteams[$i];
	open(DAT, ">>team.tmp.cgi");
	    print DAT "$team->{'id'}\n";
	    print DAT "$team->{'name'}\n";
	    print DAT "$team->{'password'}\n";
	close(DAT);
    }
    rename ("team.tmp.cgi", "team.cgi");

    # データ書き出し
    writeTeamsFile();
    unlock();

    # 変更成功
    tempChange();
}

# 名前の変更
sub logChangeName {
    my($name1, $name2) = @_;
    logHistory("${HtagTName_}${name1}${H_tagTName}、名称を${HtagTName_}${name2}${H_tagTName}に変更する。");
}

# 変更成功
sub tempChange {
    out(<<END);
${HtagBig_}変更完了しました${H_tagBig}$tempclose
END
}

# すでにその名前の島がある場合
sub tempNewTeamAlready {
    out(<<END);
${HtagBig_}そのチームは、すでにあります。${H_tagBig}$tempclose
END
}

# 新規で名前が不正な場合
sub tempNewTeamBadName {
    out(<<END);
${HtagBig_}',?()<>\$'とか入ってたり、<BR>「無人」とかいった変な名前はやめましょうよ〜${H_tagBig}$tempclose
END
}

# 名前変更失敗
sub tempChangeNothing {
    out(<<END);
${HtagBig_}空欄は駄目です${H_tagBig}$tempclose
END
}

# 記録ログ
sub logHistory {
    open(HOUT, ">>${HdirName}/hakojima.his");
    print HOUT "$HislandTurn,$_[0]\n";
    close(HOUT);
}

#----------------------------------------------------------------------
# 戦闘の記録モード
#----------------------------------------------------------------------
# メイン
sub fightlogMain {

	out ("${HtagTitle_}対戦の記録${H_tagTitle}<P>\n");
    # 対戦の記録読み込み
    open(FOUT, "${HdirName}/fight.log");
	while($f = <FOUT>){
	    chomp($f);
	    $data = <FOUT>;
	    if($f == 0) {
		$fcount = "予選落ち";
	    } elsif($data == 1) {
		$fcount = "決勝戦";
	    } else {
		$fcount = "第" . $f . "回戦";
	    }
    out(<<END);
<HR><BLOCKQUOTE>
<H1>${HtagHeader_}　　$fcount${H_tagHeader}</H1>
<TABLE BORDER>
<TR>
END

if($f) {
    out(<<END);
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}勝者${H_tagTH}</TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}人口${H_tagTH}</TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}敗者${H_tagTH}</TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}人口${H_tagTH}</TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}報酬金${H_tagTH}</TH></TR>
END
} else {
    out(<<END);
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}チーム${H_tagTH}</TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}人口${H_tagTH}</TH>
END

}
	    for($i = 0;$i < $data;$i++) {
		$fdata = <FOUT>;
		out("$fdata");
	    }
    out(<<END);
</TABLE></BLOCKQUOTE><BR>
END

	}
    close(FOUT);


    # 開放
    unlock();


}

#----------------------------------------------------------------------
# 管理人専用ページ
#----------------------------------------------------------------------
# メイン
sub pageAdminMain {

    # パスワードチェック
    if($HoldPassword ne $masterPassword) {
	# password間違い
	unlock();
	tempWrongPassword();
	return;
    }

    # 開放
    unlock();
    out(<<END);
<table><TR><TD width=100>
</TD>
<TD valign=top>
<H1>${HtagHeader_}島の強制退去${H_tagHeader}</H1>

<FORM action="$HthisFile" method="POST">
どの島を削除しますか？<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT><BR><BR>
念の為もう一回<BR>
<SELECT NAME="DELISLAND">
$HislandList
</SELECT><BR>
<INPUT TYPE="hidden" NAME ="OLDPASS" VALUE="$masterPassword"><BR>
<INPUT TYPE="submit" VALUE="　削　除　" NAME="DeleteIsland"><BR><BR>
<font color=red><B>キケン！</B></font>お間違え無き様お願いします。
</FORM>
</TD>
</TR></table>


<HR>
<center>$HtempBack</center>
END

}

1;
