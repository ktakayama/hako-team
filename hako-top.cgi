#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# トップモジュール(ver1.00)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# 箱庭諸島のページ: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# 箱庭チームトーナメント
# トップモジュール
# $Id: hako-top.cgi,v 1.1 2003/07/02 03:09:49 gaba Exp $

#----------------------------------------------------------------------
# トップページモード
#----------------------------------------------------------------------
# メイン
sub topPageMain {
    # 開放
    unlock();

    # テンプレート出力
    tempTopPage();
}

# トップページ
sub tempTopPage {

my($fightmode);

if($HislandTurn < $HyosenTurn){
    $fightmode = '<font color=blue>開発期間</font>[ターン' . ($HyosenTurn) . 'まで予選]';
} elsif($HfightMode) {
    $fightmode = '<font color=red>戦闘期間</font>';
    if($HnextCTurn == $HislandTurn){
      $fightmode .= '[次ターンより<font color=blue>開発期間</font>]';
    } else {
      $fightmode .= '[ターン' . ($HnextCTurn) . 'まで戦闘]';
    }
} else {
    $fightmode = '<font color=blue>開発期間</font>';
    if($HnextCTurn == $HislandTurn){
      $fightmode .= '[次ターンより<font color=red>戦闘開始</font>]';
    } else {
      $fightmode .= '[ターン' . ($HnextCTurn + 1) . 'より戦闘開始]';
    }
}
    # タイトル
    out(<<END);
${HtagTitle_}$Htitle${H_tagTitle}
END
if($HteamNumber == 2 && $HislandTurn != 0){
    out(<<END);
${HtagFico_}≪決勝戦≫${H_tagFico}
END
} elsif($HteamNumber == 1 && $HislandTurn != 0) {
    out(<<END);
${HtagFico_}≪終了≫${H_tagFico}
END
} elsif($HislandTurn < $HyosenTurn) {
    out(<<END);
${HtagFico_}≪予選≫${H_tagFico}
END
} else {
    out(<<END);
${HtagFico_}≪第$HfightCount回戦≫${H_tagFico}
END
}
    # デバッグモードなら「ターンを進める」ボタン
    if($Hdebug == 1) {
        out(<<END);
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="submit" VALUE="ターンを進める" NAME="TurnButton">
</FORM>
END
    }

    my($mStr1) = '';
    if($HhideMoneyMode != 0) {
	$mStr1 = "<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}資金${H_tagTH}</NOBR></TH>";
    }
    if($CjavaMode eq java) {
	$javacheck = 'checked';
    } else { $cgicheck = 'checked'; }
        out(<<END);
<H1>${HtagHeader_}ターン$HislandTurn${H_tagHeader}　$fightmode</H1>
END

#　時間表示
my($hour, $min, $sec);
my($now) = time;
my($showTIME) = ($HislandLastTime + $HunitTime - $now);
$hour = int($showTIME / 3600);
$min  = int(($showTIME - ($hour * 3600)) / 60);
$sec  = $showTIME - ($hour * 3600) - ($min * 60);
if ($sec < 0){
    if($HteamNumber > 1) {
        out("<B><font size=+1>（${HtagHeader_}更新して下さい${H_tagHeader}）</font></b>");
    }
} else {
    out("<B><font size=+1>（次のターンまで、あと $hour 時間 $min 分 $sec 秒）</font></b>");
}
    # フォーム
    out(<<END);
<SCRIPT language="JavaScript">
<!--
function develope(){

		window.open("", "newWin");
		document.Island.target = "newWin";
		document.Island.submit();

		document.Island.target = "";
		return true;
}

//-->
</SCRIPT>
<HR>
<H1>${HtagHeader_}自分の島へ${H_tagHeader}</H1>
<FORM name="Island" action="$HthisFile" method="POST">
あなたの島の名前は？<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT><BR>
<INPUT TYPE=HIDDEN NAME="OwnerButton">
パスワードをどうぞ！！<BR>
<INPUT TYPE="password" NAME="PASSWORD" VALUE="$HdefaultPassword" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="submit" VALUE="開発しに行く">
<INPUT TYPE="BUTTON" VALUE="新しい画面で開発" onClick="develope()"><BR>
<INPUT TYPE="radio" NAME=JAVAMODE VALUE=cgi $cgicheck>通常モード
<INPUT TYPE="radio" NAME=JAVAMODE VALUE=java $javacheck>Javaスクリプトモード
<BR>
</FORM>
<a name=data>
<HR>
<BR>
<a href="$HthisFile?LogFileView=1" target=_blank STYlE="text-decoration:none">
<font size=+3><b>${HtagHeader_}最近の出来事${H_tagHeader}</b></font></a>
　　　　　　
<a href="$HthisFile?LogFileTeam=${HteamMode}" target=_blank STYlE="text-decoration:none">
<font size=+3><b>${HtagHeader_}チーム別出来事${H_tagHeader}</b></font></a>
　　　　　　
<a href="$HthisFile?FightLog" target=_blank STYlE="text-decoration:none">
<font size=+3><b>${HtagHeader_}対戦の記録${H_tagHeader}</b></font></a>
<BR><BR>
<HR>
END
if($HteamMode == 0 and $HteamMode ne '') {
    out(<<END);
<TABLE><TR><TD WIDTH=250>
<H1>${HtagHeader_}諸島の状況${H_tagHeader}</H1></TD>
<TD>
<FORM ACTION="${HthisFile}" METHOD=GET>
<INPUT TYPE=SUBMIT VALUE="チームの状況一覧表示">
</FORM>
</TD></TR></TABLE>
<P>
島の名前をクリックすると、<B>観光</B>することができます。<BR>
チームの名前をクリックすると、チーム島の一覧を表示します。
</P>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}順位${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}島${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}所属チーム${H_tagTH}／${HtagTH_}対戦チーム${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}人口${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}面積${H_tagTH}</NOBR></TH>
$mStr1
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}食料${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}農場規模${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}工場規模${H_tagTH}</NOBR></TH>
</TR>
END

    my($island, $j, $farm, $factory, $name, $id, $prize, $ii, $team);
    for($ii = 0; $ii < $HislandNumber; $ii++) {
	$j = $ii + 1;
	$island = $Hislands[$ii];
	$team = $Hteams[$HidToTeamNumber{$island->{'teamid'}}];
	$id = $island->{'id'};
	$farm = $island->{'farm'};
	$factory = $island->{'factory'};
	$farm = ($farm == 0) ? "保有せず" : "${farm}0$HunitPop";
	$factory = ($factory == 0) ? "保有せず" : "${factory}0$HunitPop";
	if($island->{'absent'}  == 0) {
		$name = "${HtagName_}$island->{'name'}島${H_tagName}";
	} else {
	    $name = "${HtagName2_}$island->{'name'}島($island->{'absent'})${H_tagName2}";
	}

	$flags = $island->{'prize'};
	$prize = '';

	# 名前に賞の文字を追加
	my($f) = 1;
	my($i);
	for($i = 1; $i < 10; $i++) {
	    if($flags & $f) {
		$prize .= "<IMG SRC=\"prize${i}.gif\" ALT=\"${Hprize[$i]}\" WIDTH=16 HEIGHT=16> ";
	    }
	    $f *= 2;
	}

	my($mStr1) = '';
	if($HhideMoneyMode == 1) {
	    $mStr1 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$Hteams[$HidToTeamNumber{$island->{'teamid'}}]->{'money'}$HunitMoney</NOBR></TD>";
	} elsif($HhideMoneyMode == 2) {
	    my($mTmp) = aboutMoney($Hteams[$HidToTeamNumber{$island->{'teamid'}}]->{'money'});
	    $mStr1 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$mTmp</NOBR></TD>";
	}
	my($fightName) = '';
	if($team->{'fightid'}) {
	    $fightName = "　VS　<A STYlE=\"text-decoration:none\" HREF=$HthisFile?TEAM=$team->{'fightid'}#data>${HtagTName_}$Hteams[$HidToTeamNumber{$team->{'fightid'}}]->{'name'}${H_tagTName}</A>";
	} else {
	    $fightName = "${HtagName_}<CENTER>− − −${H_tagName}</CENTER>";
	}
	my($comname) ="${HtagTH_}コメント：${H_tagTH}";
	if(($island->{'ownername'} ne '0') && ($island->{'ownername'} ne "コメント")){
	    $comname = "<FONT COLOR=\"blue\"><B>$island->{'ownername'}：</b></font>";
	}
	out(<<END);
<TR>
<TD $HbgNumberCell ROWSPAN=2 align=center nowrap=nowrap><NOBR>${HtagNumber_}$j${H_tagNumber}</NOBR></TD>
<TD $HbgNameCell ROWSPAN=2 align=left nowrap=nowrap>
<NOBR>
<A STYlE=\"text-decoration:none\" HREF="${HthisFile}?Sight=${id}" target=_blank>
$name
</A>
</NOBR><BR>
$prize
</TD>
<TD $HbgInfoCell align=left nowrap=nowrap>
<NOBR><A STYlE=\"text-decoration:none\" HREF=$HthisFile?TEAM=$team->{'id'}#data>${HtagTName_}$team->{'name'}${H_tagTName}</A></NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap>
<NOBR>$island->{'pop'}$HunitPop</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'area'}$HunitArea</NOBR></TD>
$mStr1
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'food'}$HunitFood</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$farm</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$factory</NOBR></TD>
</TR>
<TR>
<TD $HbgInfoCell align=left nowrap=nowrap>
<NOBR>$fightName</NOBR></TD>
<TD $HbgCommentCell COLSPAN=6 align=left nowrap=nowrap><NOBR>${HtagTH_}$comname${H_tagTH}$island->{'comment'}</NOBR></TD>
</TR>
END
    }


} elsif($HteamMode) {

    my($team, $g, $tname, $tmoney, $tpop, $tfarm, $tfactory, $jj, $flags, $prize);
    $number = $HidToTeamNumber{$HteamMode};
    $team = $Hteams[$number];
    if($number ne '') {

	$jj = $number + 1;
	$id = $team->{'id'};
	$tfarm = $team->{'farm'};
	$tfactory = $team->{'factory'};
	$tfarm = ($tfarm == 0) ? "保有せず" : "${tfarm}0$HunitPop";
	$tfactory = ($tfactory == 0) ? "保有せず" : "${tfactory}0$HunitPop";
	my($numMember) = $team->{'member'};
	my($member) = '';
	while($numMember =~ s/([0-9]*),//) {
	    push(@islanddata,$HidToNumber{$1});
	}
	@islanddata = sort { $a <=> $b } @islanddata;
	$flags = $team->{'prize'};
	$prize = '';

	# 名前に賞の文字を追加
	my($f) = 1;
	my($i);
	for($i = 1; $i < 10; $i++) {
	    if($flags & $f) {
		$prize .= "<IMG SRC=\"prize${i}.gif\" ALT=\"${Hprize[$i]}\" WIDTH=16 HEIGHT=16> ";
	    }
	    $f *= 2;
	}

	my($mStr2) = '';
	if($HhideMoneyMode == 1) {
	    $mStr2 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$team->{'money'}$HunitMoney</NOBR></TD>";
	} elsif($HhideMoneyMode == 2) {
	    my($mTmp) = aboutMoney($team->{'money'});
	    $mStr2 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$mTmp</NOBR></TD>";
	}
	my($fightName) = '';
	if($team->{'fightid'} > 0) {
	    $fightName = "<A STYlE=\"text-decoration:none\" HREF=$HthisFile?TEAM=$team->{'fightid'}#data>${HtagTName_}$Hteams[$HidToTeamNumber{$team->{'fightid'}}]->{'name'}${H_tagTName}</A>";
	} else {
	    $fightName = "${HtagName_}<CENTER>− − −${H_tagName}</CENTER>";
	}

    out(<<END);
<TABLE><TR><TD WIDTH=250>
<NOBR><H1>${HtagHeader_}$team->{'name'}の状況${H_tagHeader}　</H1></NOBR></TD>
<TD>
<FORM ACTION="${HthisFile}" METHOD=GET>
　<INPUT TYPE=HIDDEN VALUE="0" NAME="TEAM">
<INPUT TYPE=SUBMIT VALUE="諸島の状況">
</FORM>
</TD>
<TD>
<FORM ACTION="${HthisFile}" METHOD=GET>
　<INPUT TYPE=SUBMIT VALUE="チームの状況一覧">
</FORM>
</TD>
</TR></TABLE>
<FORM ACTION="${HthisFile}#data" METHOD=GET>
<SELECT NAME="TEAM">
END
for($if = 0;$if < $HteamNumber;$if++) {
	if($team->{'id'} == $Hteams[$if]->{'id'}) {
	    out("<OPTION VALUE=$Hteams[$if]->{'id'} SELECTED>$Hteams[$if]->{'name'}\n");
	} else {
	    out("<OPTION VALUE=$Hteams[$if]->{'id'}>$Hteams[$if]->{'name'}\n");
	}
}
    out(<<END);
</SELECT>
<INPUT TYPE=SUBMIT VALUE="このチームの状況表示">
</FORM>
<P>
島の名前をクリックすると、<B>観光</B>することができます。
</P>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}順位${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}チーム${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}対戦チーム${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}人口${H_tagTH}</NOBR></TH>
$mStr1
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}食料${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}農場規模${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}工場規模${H_tagTH}</NOBR></TH>
</TR>
<TR>
<TD $HbgNumberCell align=center nowrap=nowrap><NOBR>${HtagNumber_}${jj}${H_tagNumber}</NOBR></TD>
<TD $HbgNameCell ROWSPAN=2 align=left nowrap=nowrap>
<NOBR>${HtagTName_}$team->{'name'}${H_tagTName}
</NOBR><BR>
$prize</TD>
<TD $HbgNameCell align=left nowrap=nowrap>
<NOBR>${fightName}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><A NAME=team$team->{'id'}>
<NOBR>$team->{'pop'}$HunitPop</NOBR></TD>
$mStr2
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$team->{'food'}$HunitFood</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$tfarm</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$tfactory</NOBR></TD>
</TR>
</TABLE><BR><BR>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}順位${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}島${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}人口${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}面積${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}食料${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}農場規模${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}工場規模${H_tagTH}</NOBR></TH>
</TR>
END
for($g = 0;$g < $HmenberCount;$g++) {
	$iNumber = $islanddata[$g];
    if($iNumber ne '') {
	$j = $iNumber + 1;
	$island = $Hislands[$iNumber];
	$id = $island->{'id'};
	$farm = $island->{'farm'};
	$factory = $island->{'factory'};
	$farm = ($farm == 0) ? "保有せず" : "${farm}0$HunitPop";
	$factory = ($factory == 0) ? "保有せず" : "${factory}0$HunitPop";
	if($island->{'absent'}  == 0) {
		$name = "${HtagName_}$island->{'name'}島${H_tagName}";
	} else {
	    $name = "${HtagName2_}$island->{'name'}島($island->{'absent'})${H_tagName2}";
	}

	$flags = $island->{'prize'};
	$prize = '';

	# 名前に賞の文字を追加
	my($f) = 1;
	my($i);
	for($i = 1; $i < 10; $i++) {
	    if($flags & $f) {
		$prize .= "<IMG SRC=\"prize${i}.gif\" ALT=\"${Hprize[$i]}\" WIDTH=16 HEIGHT=16> ";
	    }
	    $f *= 2;
	}

	my($comname) ="${HtagTH_}コメント：${H_tagTH}";
	if(($island->{'ownername'} ne '0') && ($island->{'ownername'} ne "コメント")){
	    $comname = "<FONT COLOR=\"blue\"><B>$island->{'ownername'}：</b></font>";
	}
	out(<<END);
<TR>
<TD $HbgNumberCell ROWSPAN=2 align=center nowrap=nowrap><NOBR>${HtagNumber_}$j${H_tagNumber}</NOBR></TD>
<TD $HbgNameCell ROWSPAN=2 align=left nowrap=nowrap>
<NOBR>
<A STYlE=\"text-decoration:none\" HREF="${HthisFile}?Sight=${id}" target=_blank>
$name
</A>
</NOBR><BR>
$prize
</TD>
<TD $HbgInfoCell align=right nowrap=nowrap>
<NOBR>$island->{'pop'}$HunitPop</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'area'}$HunitArea</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'food'}$HunitFood</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$farm</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$factory</NOBR></TD>
</TR>
<TR>
<TD $HbgCommentCell COLSPAN=8 align=left nowrap=nowrap><NOBR>${HtagTH_}$comname${H_tagTH}$island->{'comment'}</NOBR></TD>
</TR>
END
    }
}
    }
} else {

    out(<<END);
<TABLE><TR><TD WIDTH=250>
<H1>${HtagHeader_}チームの状況${H_tagHeader}</H1></TD>
<TD>
<FORM ACTION="${HthisFile}" METHOD=GET>
<INPUT TYPE=HIDDEN VALUE="0" NAME="TEAM">
<INPUT TYPE=SUBMIT VALUE="諸島の状況表示">
</FORM>
</TD></TR></TABLE>
<P>
島の名前をクリックすると、<B>観光</B>することができます。<BR>
チームの名前をクリックすると、チーム島の状況が一覧表示されます。<BR>
対戦チームの名前をクリックすると、その順位に飛びます。
</P>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}順位${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}チーム${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}対戦チーム${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}人口${H_tagTH}</NOBR></TH>
$mStr1
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}食料${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}農場規模${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}工場規模${H_tagTH}</NOBR></TH>
</TR>
END
my($team, $g, $tname, $tmoney, $tpop, $tfarm, $tfactory, $jj, $flags, $prize);
for($g = 0;$g < $HteamNumber;$g++) {

if($g == $yteamNum){
    $HbgInfoCell    = $YbgInfoCell;
    $HbgCommentCell = $YbgCommentCell;
    $HbgNameCell = $YbgNameCell;
    $HbgNumberCell = $YbgNumberCell;
    out ("<TR><TD colspan=10>　</TD></TR>");
}

	$jj = $g + 1;
	$team = $Hteams[$g];
	$id = $team->{'id'};
	$tfarm = $team->{'farm'};
	$tfactory = $team->{'factory'};
	$tfarm = ($tfarm == 0) ? "保有せず" : "${tfarm}0$HunitPop";
	$tfactory = ($tfactory == 0) ? "保有せず" : "${tfactory}0$HunitPop";
	my($numMember) = $team->{'member'};
	my($member) = '';
	while($numMember =~ s/([0-9]*),//) {
	    if($member ne '') { $member .=  "<B> : </B>"; }
	    my($island) = $Hislands[$HidToNumber{$1}];
	    $member .= "<A STYlE=\"text-decoration:none\" HREF=\"${HthisFile}?Sight=$island->{'id'}\" target=_blank>${HtagName_}$island->{'name'}島${H_tagName}</A>";
	}

	$flags = $team->{'prize'};
	$prize = '';

	# 名前に賞の文字を追加
	my($f) = 1;
	my($i);
	for($i = 1; $i < 10; $i++) {
	    if($flags & $f) {
		$prize .= "<IMG SRC=\"prize${i}.gif\" ALT=\"${Hprize[$i]}\" WIDTH=16 HEIGHT=16> ";
	    }
	    $f *= 2;
	}

	my($mStr1) = '';
	if($HhideMoneyMode == 1) {
	    $mStr1 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$team->{'money'}$HunitMoney</NOBR></TD>";
	} elsif($HhideMoneyMode == 2) {
	    my($mTmp) = aboutMoney($team->{'money'});
	    $mStr1 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$mTmp</NOBR></TD>";
	}
	my($fightName) = '';
	if($team->{'fightid'} > 0) {
	    $fightName = "<A STYlE=\"text-decoration:none\" HREF=$HthisFile?#team$team->{'fightid'}>${HtagTName_}$Hteams[$HidToTeamNumber{$team->{'fightid'}}]->{'name'}${H_tagTName}</A>";
	} else {
	    $fightName = "${HtagName_}<CENTER>− − −${H_tagName}</CENTER>";
	}
	out(<<END);
<TR>
<TD $HbgNumberCell ROWSPAN=2 align=center nowrap=nowrap><NOBR>${HtagNumber_}${jj}${H_tagNumber}</NOBR></TD>
<TD $HbgNameCell ROWSPAN=2 align=left nowrap=nowrap>
<NOBR><A STYlE="text-decoration:none" HREF=$HthisFile?TEAM=$team->{'id'}#data>${HtagTName_}$team->{'name'}${H_tagTName}</A>
</NOBR><BR>
$prize</TD>
<TD $HbgNameCell ROWSPAN=2 align=left nowrap=nowrap>
<NOBR>${fightName}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><A NAME=team$team->{'id'}>
<NOBR>$team->{'pop'}$HunitPop</NOBR></TD>
$mStr1
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$team->{'food'}$HunitFood</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$tfarm</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$tfactory</NOBR></TD>
</TR>
<TR>
<TD $HbgCommentCell COLSPAN=5 align=left nowrap=nowrap><NOBR>${HtagTH_}メンバー：${H_tagTH}$member</NOBR></TD>
</TR>
END

}


}
if(!($HteamMode)) {

    out(<<END);
</TABLE>

<HR>
<H1>${HtagHeader_}新しい島を探す${H_tagHeader}</H1>
END

    if($HislandNumber < $HmaxIsland && $HislandTurn == 0) {
	out(<<END);
<FORM action="$HthisFile" method="POST">
まずはチームを選択して下さい<BR>
<SELECT NAME=TEAMID>
END
for($i = 0;$i < $HteamNumber;$i++) {
    my($numMember) = $Hteams[$i]->{'member'};
    my($count) = 0;
    while($numMember =~ s/([0-9]*),//) { $count++; }
    if($HmenberCount == $count){ next; }
	out(<<END);
<OPTION VALUE=$Hteams[$i]->{'id'}>$Hteams[$i]->{'name'}
END
}
	out(<<END);
</SELECT><BR>
どんな名前をつける予定？<BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>島<BR>
パスワードは？<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32><BR>
念のためパスワードをもう一回<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32><BR>

<INPUT TYPE="submit" VALUE="探しに行く" NAME="NewIslandButton">
</FORM>
END
    } elsif($HislandTurn > 0) {
	out(<<END);
        途中参加は出来ません。次回登録開始まで、今しばらくお待ち下さいませ。<BR>
END
    } else {
	out(<<END);
        島の数が最大数です・・・現在登録できません。
END
    }

    out(<<END);
<HR>
<TABLE>
<TR><TD WIDTH=420 ROWSPAN=2>
<NOBR><H1>${HtagHeader_}島の名前とパスワードの変更${H_tagHeader}</H1></NOBR>
<P>
(注意)名前の変更には<B>$HcostChangeName${HunitMoney}</b>かかります。
</P>
<FORM action="$HthisFile" method="POST">
どの島ですか？<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT><BR>
どんな名前に変えますか？(変更する場合のみ)<BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>島<BR>
パスワードは？(必須)<BR>
<INPUT TYPE="password" NAME="OLDPASS" SIZE=32 MAXLENGTH=32><BR>
新しいパスワードは？(変更する時のみ)<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32><BR>
念のためパスワードをもう一回(変更する時のみ)<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="submit" VALUE="変更する" NAME="ChangeInfoButton">
</FORM>


END
my($Himfflag);
if($HimgLine eq '' || $HimgLine eq $imageDir){
    $Himfflag = '<FONT COLOR=RED>未設定</FONT>';
} else {
    $Himfflag = $HimgLine;
}

   out(<<END);
</TD>

<TD VALIGN=TOP WIDTH=350>
<H1>${HtagHeader_}画像のローカル設定${H_tagHeader}</H1>
現在の設定<B>[</b> ${Himfflag} <B>]</B>
　　<A HREF=${imageExp} target=_blank><FONT SIZE=+1> 説 明 </FONT></A>
<form action=$HthisFile method=POST>
<INPUT TYPE=file NAME="IMGLINE">
<INPUT TYPE="submit" VALUE="設定" name=IMGSET>
</form>

<form action=$HthisFile method=POST>
Macユーザー用<BR>
<INPUT TYPE=text NAME="IMGLINEMAC">
<INPUT TYPE="submit" VALUE="設定" name=IMGSET><BR>
<FONT SIZE=-1>Macの方は、こちらを使用して下さい。</FONT>
</form>
</TD></TR>

<TR HEIGHT=100><TD ALIGN=CENTER>
<form action=$HthisFile method=POST>
<INPUT TYPE=hidden NAME="IMGLINE" value="deletemodenow">
<INPUT TYPE="submit" VALUE="設定を解除する" name=IMGSET>
</form>
</TD></TR>
</TABLE>

<HR>
<H1>${HtagHeader_}オーナーの名前決定！${H_tagHeader}</H1>
<FORM action="$HthisFile" method="POST">
あなたの島は？
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>　　名前入力
<INPUT TYPE="text" NAME="OWNERNAME" SIZE=16 MAXLENGTH=32>
　　パスワード
<INPUT TYPE="password" NAME="OLDPASS" SIZE=16 MAXLENGTH=32>
<INPUT TYPE="submit" VALUE="これにする" NAME="ChangeOwnerName">
</form>
<HR>

<H1>${HtagHeader_}発見の記録${H_tagHeader}</H1>
END
    historyPrint();
    out(<<END);
<BR><HR><div align=right><table><TR><td>
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="password" NAME="OLDPASS" SIZE=16 MAXLENGTH=32>
<INPUT TYPE="submit" VALUE="管理人用" NAME="AdminPage">
</FORM></td></tr></table>
</div>
END
} else {
   out(<<END);
</TABLE>
END

}
}
# 記録ファイル表示
sub historyPrint {
    open(HIN, "${HdirName}/hakojima.his");
    my(@line, $l);
    while($l = <HIN>) {
	chomp($l);
	push(@line, $l);
    }
    @line = reverse(@line);

    foreach $l (@line) {
	$l =~ /^([0-9]*),(.*)$/;
	out("<NOBR>${HtagNumber_}ターン${1}${H_tagNumber}：${2}</NOBR><BR>\n");
    }
    close(HIN);
}

1;
