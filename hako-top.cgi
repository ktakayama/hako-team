#----------------------------------------------------------------------
# Ȣ����� ver2.30
# �ȥåץ⥸�塼��(ver1.00)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# Ȣ�����Υڡ���: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# Ȣ�������ȡ��ʥ���
# �ȥåץ⥸�塼��
# $Id: hako-top.cgi,v 1.1 2003/07/02 03:09:49 gaba Exp $

#----------------------------------------------------------------------
# �ȥåץڡ����⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub topPageMain {
    # ����
    unlock();

    # �ƥ�ץ졼�Ƚ���
    tempTopPage();
}

# �ȥåץڡ���
sub tempTopPage {

my($fightmode);

if($HislandTurn < $HyosenTurn){
    $fightmode = '<font color=blue>��ȯ����</font>[������' . ($HyosenTurn) . '�ޤ�ͽ��]';
} elsif($HfightMode) {
    $fightmode = '<font color=red>��Ʈ����</font>';
    if($HnextCTurn == $HislandTurn){
      $fightmode .= '[����������<font color=blue>��ȯ����</font>]';
    } else {
      $fightmode .= '[������' . ($HnextCTurn) . '�ޤ���Ʈ]';
    }
} else {
    $fightmode = '<font color=blue>��ȯ����</font>';
    if($HnextCTurn == $HislandTurn){
      $fightmode .= '[����������<font color=red>��Ʈ����</font>]';
    } else {
      $fightmode .= '[������' . ($HnextCTurn + 1) . '�����Ʈ����]';
    }
}
    # �����ȥ�
    out(<<END);
${HtagTitle_}$Htitle${H_tagTitle}
END
if($HteamNumber == 2 && $HislandTurn != 0){
    out(<<END);
${HtagFico_}��辡���${H_tagFico}
END
} elsif($HteamNumber == 1 && $HislandTurn != 0) {
    out(<<END);
${HtagFico_}�㽪λ��${H_tagFico}
END
} elsif($HislandTurn < $HyosenTurn) {
    out(<<END);
${HtagFico_}��ͽ����${H_tagFico}
END
} else {
    out(<<END);
${HtagFico_}����$HfightCount�����${H_tagFico}
END
}
    # �ǥХå��⡼�ɤʤ�֥������ʤ��ץܥ���
    if($Hdebug == 1) {
        out(<<END);
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="submit" VALUE="�������ʤ��" NAME="TurnButton">
</FORM>
END
    }

    my($mStr1) = '';
    if($HhideMoneyMode != 0) {
	$mStr1 = "<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>";
    }
    if($CjavaMode eq java) {
	$javacheck = 'checked';
    } else { $cgicheck = 'checked'; }
        out(<<END);
<H1>${HtagHeader_}������$HislandTurn${H_tagHeader}��$fightmode</H1>
END

#������ɽ��
my($hour, $min, $sec);
my($now) = time;
my($showTIME) = ($HislandLastTime + $HunitTime - $now);
$hour = int($showTIME / 3600);
$min  = int(($showTIME - ($hour * 3600)) / 60);
$sec  = $showTIME - ($hour * 3600) - ($min * 60);
if ($sec < 0){
    if($HteamNumber > 1) {
        out("<B><font size=+1>��${HtagHeader_}�������Ʋ�����${H_tagHeader}��</font></b>");
    }
} else {
    out("<B><font size=+1>�ʼ��Υ�����ޤǡ����� $hour ���� $min ʬ $sec �á�</font></b>");
}
    # �ե�����
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
<H1>${HtagHeader_}��ʬ�����${H_tagHeader}</H1>
<FORM name="Island" action="$HthisFile" method="POST">
���ʤ������̾���ϡ�<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT><BR>
<INPUT TYPE=HIDDEN NAME="OwnerButton">
�ѥ���ɤ�ɤ�������<BR>
<INPUT TYPE="password" NAME="PASSWORD" VALUE="$HdefaultPassword" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="submit" VALUE="��ȯ���˹Ԥ�">
<INPUT TYPE="BUTTON" VALUE="���������̤ǳ�ȯ" onClick="develope()"><BR>
<INPUT TYPE="radio" NAME=JAVAMODE VALUE=cgi $cgicheck>�̾�⡼��
<INPUT TYPE="radio" NAME=JAVAMODE VALUE=java $javacheck>Java������ץȥ⡼��
<BR>
</FORM>
<a name=data>
<HR>
<BR>
<a href="$HthisFile?LogFileView=1" target=_blank STYlE="text-decoration:none">
<font size=+3><b>${HtagHeader_}�Ƕ�ν����${H_tagHeader}</b></font></a>
������������
<a href="$HthisFile?LogFileTeam=${HteamMode}" target=_blank STYlE="text-decoration:none">
<font size=+3><b>${HtagHeader_}�������̽����${H_tagHeader}</b></font></a>
������������
<a href="$HthisFile?FightLog" target=_blank STYlE="text-decoration:none">
<font size=+3><b>${HtagHeader_}����ε�Ͽ${H_tagHeader}</b></font></a>
<BR><BR>
<HR>
END
if($HteamMode == 0 and $HteamMode ne '') {
    out(<<END);
<TABLE><TR><TD WIDTH=250>
<H1>${HtagHeader_}����ξ���${H_tagHeader}</H1></TD>
<TD>
<FORM ACTION="${HthisFile}" METHOD=GET>
<INPUT TYPE=SUBMIT VALUE="������ξ�������ɽ��">
</FORM>
</TD></TR></TABLE>
<P>
���̾���򥯥�å�����ȡ�<B>�Ѹ�</B>���뤳�Ȥ��Ǥ��ޤ���<BR>
�������̾���򥯥�å�����ȡ���������ΰ�����ɽ�����ޤ���
</P>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}��°������${H_tagTH}��${HtagTH_}���������${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�͸�${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
$mStr1
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���쵬��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���쵬��${H_tagTH}</NOBR></TH>
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
	$farm = ($farm == 0) ? "��ͭ����" : "${farm}0$HunitPop";
	$factory = ($factory == 0) ? "��ͭ����" : "${factory}0$HunitPop";
	if($island->{'absent'}  == 0) {
		$name = "${HtagName_}$island->{'name'}��${H_tagName}";
	} else {
	    $name = "${HtagName2_}$island->{'name'}��($island->{'absent'})${H_tagName2}";
	}

	$flags = $island->{'prize'};
	$prize = '';

	# ̾���˾ޤ�ʸ�����ɲ�
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
	    $fightName = "��VS��<A STYlE=\"text-decoration:none\" HREF=$HthisFile?TEAM=$team->{'fightid'}#data>${HtagTName_}$Hteams[$HidToTeamNumber{$team->{'fightid'}}]->{'name'}${H_tagTName}</A>";
	} else {
	    $fightName = "${HtagName_}<CENTER>�� �� ��${H_tagName}</CENTER>";
	}
	my($comname) ="${HtagTH_}�����ȡ�${H_tagTH}";
	if(($island->{'ownername'} ne '0') && ($island->{'ownername'} ne "������")){
	    $comname = "<FONT COLOR=\"blue\"><B>$island->{'ownername'}��</b></font>";
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
	$tfarm = ($tfarm == 0) ? "��ͭ����" : "${tfarm}0$HunitPop";
	$tfactory = ($tfactory == 0) ? "��ͭ����" : "${tfactory}0$HunitPop";
	my($numMember) = $team->{'member'};
	my($member) = '';
	while($numMember =~ s/([0-9]*),//) {
	    push(@islanddata,$HidToNumber{$1});
	}
	@islanddata = sort { $a <=> $b } @islanddata;
	$flags = $team->{'prize'};
	$prize = '';

	# ̾���˾ޤ�ʸ�����ɲ�
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
	    $fightName = "${HtagName_}<CENTER>�� �� ��${H_tagName}</CENTER>";
	}

    out(<<END);
<TABLE><TR><TD WIDTH=250>
<NOBR><H1>${HtagHeader_}$team->{'name'}�ξ���${H_tagHeader}��</H1></NOBR></TD>
<TD>
<FORM ACTION="${HthisFile}" METHOD=GET>
��<INPUT TYPE=HIDDEN VALUE="0" NAME="TEAM">
<INPUT TYPE=SUBMIT VALUE="����ξ���">
</FORM>
</TD>
<TD>
<FORM ACTION="${HthisFile}" METHOD=GET>
��<INPUT TYPE=SUBMIT VALUE="������ξ�������">
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
<INPUT TYPE=SUBMIT VALUE="���Υ�����ξ���ɽ��">
</FORM>
<P>
���̾���򥯥�å�����ȡ�<B>�Ѹ�</B>���뤳�Ȥ��Ǥ��ޤ���
</P>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}������${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���������${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�͸�${H_tagTH}</NOBR></TH>
$mStr1
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���쵬��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���쵬��${H_tagTH}</NOBR></TH>
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
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�͸�${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���쵬��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���쵬��${H_tagTH}</NOBR></TH>
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
	$farm = ($farm == 0) ? "��ͭ����" : "${farm}0$HunitPop";
	$factory = ($factory == 0) ? "��ͭ����" : "${factory}0$HunitPop";
	if($island->{'absent'}  == 0) {
		$name = "${HtagName_}$island->{'name'}��${H_tagName}";
	} else {
	    $name = "${HtagName2_}$island->{'name'}��($island->{'absent'})${H_tagName2}";
	}

	$flags = $island->{'prize'};
	$prize = '';

	# ̾���˾ޤ�ʸ�����ɲ�
	my($f) = 1;
	my($i);
	for($i = 1; $i < 10; $i++) {
	    if($flags & $f) {
		$prize .= "<IMG SRC=\"prize${i}.gif\" ALT=\"${Hprize[$i]}\" WIDTH=16 HEIGHT=16> ";
	    }
	    $f *= 2;
	}

	my($comname) ="${HtagTH_}�����ȡ�${H_tagTH}";
	if(($island->{'ownername'} ne '0') && ($island->{'ownername'} ne "������")){
	    $comname = "<FONT COLOR=\"blue\"><B>$island->{'ownername'}��</b></font>";
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
<H1>${HtagHeader_}������ξ���${H_tagHeader}</H1></TD>
<TD>
<FORM ACTION="${HthisFile}" METHOD=GET>
<INPUT TYPE=HIDDEN VALUE="0" NAME="TEAM">
<INPUT TYPE=SUBMIT VALUE="����ξ���ɽ��">
</FORM>
</TD></TR></TABLE>
<P>
���̾���򥯥�å�����ȡ�<B>�Ѹ�</B>���뤳�Ȥ��Ǥ��ޤ���<BR>
�������̾���򥯥�å�����ȡ���������ξ���������ɽ������ޤ���<BR>
����������̾���򥯥�å�����ȡ����ν�̤����Ӥޤ���
</P>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}������${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���������${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�͸�${H_tagTH}</NOBR></TH>
$mStr1
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���쵬��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���쵬��${H_tagTH}</NOBR></TH>
</TR>
END
my($team, $g, $tname, $tmoney, $tpop, $tfarm, $tfactory, $jj, $flags, $prize);
for($g = 0;$g < $HteamNumber;$g++) {

if($g == $yteamNum){
    $HbgInfoCell    = $YbgInfoCell;
    $HbgCommentCell = $YbgCommentCell;
    $HbgNameCell = $YbgNameCell;
    $HbgNumberCell = $YbgNumberCell;
    out ("<TR><TD colspan=10>��</TD></TR>");
}

	$jj = $g + 1;
	$team = $Hteams[$g];
	$id = $team->{'id'};
	$tfarm = $team->{'farm'};
	$tfactory = $team->{'factory'};
	$tfarm = ($tfarm == 0) ? "��ͭ����" : "${tfarm}0$HunitPop";
	$tfactory = ($tfactory == 0) ? "��ͭ����" : "${tfactory}0$HunitPop";
	my($numMember) = $team->{'member'};
	my($member) = '';
	while($numMember =~ s/([0-9]*),//) {
	    if($member ne '') { $member .=  "<B> : </B>"; }
	    my($island) = $Hislands[$HidToNumber{$1}];
	    $member .= "<A STYlE=\"text-decoration:none\" HREF=\"${HthisFile}?Sight=$island->{'id'}\" target=_blank>${HtagName_}$island->{'name'}��${H_tagName}</A>";
	}

	$flags = $team->{'prize'};
	$prize = '';

	# ̾���˾ޤ�ʸ�����ɲ�
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
	    $fightName = "${HtagName_}<CENTER>�� �� ��${H_tagName}</CENTER>";
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
<TD $HbgCommentCell COLSPAN=5 align=left nowrap=nowrap><NOBR>${HtagTH_}���С���${H_tagTH}$member</NOBR></TD>
</TR>
END

}


}
if(!($HteamMode)) {

    out(<<END);
</TABLE>

<HR>
<H1>${HtagHeader_}���������õ��${H_tagHeader}</H1>
END

    if($HislandNumber < $HmaxIsland && $HislandTurn == 0) {
	out(<<END);
<FORM action="$HthisFile" method="POST">
�ޤ��ϥ���������򤷤Ʋ�����<BR>
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
�ɤ��̾����Ĥ���ͽ�ꡩ<BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>��<BR>
�ѥ���ɤϡ�<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32><BR>
ǰ�Τ���ѥ���ɤ�⤦���<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32><BR>

<INPUT TYPE="submit" VALUE="õ���˹Ԥ�" NAME="NewIslandButton">
</FORM>
END
    } elsif($HislandTurn > 0) {
	out(<<END);
        ���滲�äϽ���ޤ��󡣼�����Ͽ���Ϥޤǡ������Ф餯���Ԥ��������ޤ���<BR>
END
    } else {
	out(<<END);
        ��ο���������Ǥ�������������Ͽ�Ǥ��ޤ���
END
    }

    out(<<END);
<HR>
<TABLE>
<TR><TD WIDTH=420 ROWSPAN=2>
<NOBR><H1>${HtagHeader_}���̾���ȥѥ���ɤ��ѹ�${H_tagHeader}</H1></NOBR>
<P>
(���)̾�����ѹ��ˤ�<B>$HcostChangeName${HunitMoney}</b>������ޤ���
</P>
<FORM action="$HthisFile" method="POST">
�ɤ���Ǥ�����<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT><BR>
�ɤ��̾�����Ѥ��ޤ�����(�ѹ�������Τ�)<BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>��<BR>
�ѥ���ɤϡ�(ɬ��)<BR>
<INPUT TYPE="password" NAME="OLDPASS" SIZE=32 MAXLENGTH=32><BR>
�������ѥ���ɤϡ�(�ѹ�������Τ�)<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32><BR>
ǰ�Τ���ѥ���ɤ�⤦���(�ѹ�������Τ�)<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="submit" VALUE="�ѹ�����" NAME="ChangeInfoButton">
</FORM>


END
my($Himfflag);
if($HimgLine eq '' || $HimgLine eq $imageDir){
    $Himfflag = '<FONT COLOR=RED>̤����</FONT>';
} else {
    $Himfflag = $HimgLine;
}

   out(<<END);
</TD>

<TD VALIGN=TOP WIDTH=350>
<H1>${HtagHeader_}�����Υ���������${H_tagHeader}</H1>
���ߤ�����<B>[</b> ${Himfflag} <B>]</B>
����<A HREF=${imageExp} target=_blank><FONT SIZE=+1> �� �� </FONT></A>
<form action=$HthisFile method=POST>
<INPUT TYPE=file NAME="IMGLINE">
<INPUT TYPE="submit" VALUE="����" name=IMGSET>
</form>

<form action=$HthisFile method=POST>
Mac�桼������<BR>
<INPUT TYPE=text NAME="IMGLINEMAC">
<INPUT TYPE="submit" VALUE="����" name=IMGSET><BR>
<FONT SIZE=-1>Mac�����ϡ����������Ѥ��Ʋ�������</FONT>
</form>
</TD></TR>

<TR HEIGHT=100><TD ALIGN=CENTER>
<form action=$HthisFile method=POST>
<INPUT TYPE=hidden NAME="IMGLINE" value="deletemodenow">
<INPUT TYPE="submit" VALUE="�����������" name=IMGSET>
</form>
</TD></TR>
</TABLE>

<HR>
<H1>${HtagHeader_}�����ʡ���̾�����ꡪ${H_tagHeader}</H1>
<FORM action="$HthisFile" method="POST">
���ʤ�����ϡ�
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>����̾������
<INPUT TYPE="text" NAME="OWNERNAME" SIZE=16 MAXLENGTH=32>
�����ѥ����
<INPUT TYPE="password" NAME="OLDPASS" SIZE=16 MAXLENGTH=32>
<INPUT TYPE="submit" VALUE="����ˤ���" NAME="ChangeOwnerName">
</form>
<HR>

<H1>${HtagHeader_}ȯ���ε�Ͽ${H_tagHeader}</H1>
END
    historyPrint();
    out(<<END);
<BR><HR><div align=right><table><TR><td>
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="password" NAME="OLDPASS" SIZE=16 MAXLENGTH=32>
<INPUT TYPE="submit" VALUE="��������" NAME="AdminPage">
</FORM></td></tr></table>
</div>
END
} else {
   out(<<END);
</TABLE>
END

}
}
# ��Ͽ�ե�����ɽ��
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
	out("<NOBR>${HtagNumber_}������${1}${H_tagNumber}��${2}</NOBR><BR>\n");
    }
    close(HIN);
}

1;
