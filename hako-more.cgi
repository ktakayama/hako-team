#----------------------------------------------------------------------
# Ȣ�������ȡ��ʥ��� �ɲå⥸�塼��
# �ɥ󡦥��Х��硧��support@mc.neweb.ne.jp
# Ȣ����� http://espion.s7.xrea.com/tyotou/
# ������ϼ����Ĥ��Ƥ���ޤ���
#----------------------------------------------------------------------
# Ȣ�������ȡ��ʥ���
# �ɲå⥸�塼��
# $Id: hako-more.cgi,v 1.1 2003/07/02 03:09:49 gaba Exp $

#----------------------------------------------------------------------
# ��ɽ���⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub logViewMain {

    # ����
    unlock();

    # �ƥ�ץ졼�Ƚ���
    tempLogPage();
}

sub tempLogPage {

    out(<<END);

<font size=+3><b>${HtagHeader_}�Ƕ�ν����${H_tagHeader}</b></font>��
��<a href="$HthisFile?LogFileView=1"><FONT COLOR="blue" size=2><B>��������</a>
��<a href="$HthisFile?LogFileView=2">2������ʬɽ��</a>
END
for($i = 3; $i -1 < $HlogMax; $i++) {
	out("��<a href=\"$HthisFile?LogFileView=${i}\">${i}������ʬ</a>\n");
}
    out(<<END);
</b></font><br>
END
    logPrintTop();

}

# ��ɽ��
sub logPrintTop {
    my($i);
    for($i = 0; $i < $Hlogturn; $i++) {
	out("<hr>\n");
	logFilePrint($i, 0, 0);

    }
}

#----------------------------------------------------------------------
# ����إ�ץ⡼��
#----------------------------------------------------------------------
# �ᥤ��
# �إ�ץڡ���
sub helpMain {

    # ����
    unlock();
my($devrep) = '';
my($firep) = '';
my($unit) = $HunitTime / 3600;
my($fiunit) = $HfightTime / 3600;

if($HdevRepTurn > 1){ $devrep = '��' . $HdevRepTurn . '������ޤȤ�ƹ�����'; }
if($HfigRepTurn > 1){ $firep = '��' . $HfigRepTurn . '������ޤȤ�ƹ�����'; }

    out(<<END);
${HtagTitle_}����إ��${H_tagTitle}
<BR><BR><BR>

<H1>${HtagHeader_}�Ƽ�������${H_tagHeader}</H1>
<table width=300 border $HbgNameCell>
<TR>
<TD colspan=2 $HbgTitleCell>${HtagTH_}����ط�${H_tagTH}</TD>
</TR>
<TR>
<TD>��${HtagName_}�������${H_tagName}��</TD><TD><B>$teamNum������</b></TD>
</TR>
<TR>
<TD>��${HtagName_}���С���${H_tagName}��</TD><TD><B>$HmenberCount��</b></TD>
</TR>
<TR><TD>��${HtagName_}ͽ������${H_tagName}</TD><TD><B>$yteamNum������</b></TD>
</TR>
<TR>
<TD colspan=2 $HbgTitleCell>${HtagTH_}��ν����${H_tagTH}</TD>
</TR>
<TR><TD>��${HtagName_}����${H_tagName}��</TD><TD><B>${HlandSizeValue}${HunitArea}</b></TD></TR>
<TR><TD>��${HtagName_}���Ϥο�${H_tagName}</TD><TD><B>10����</b></TD></TR>
<TR><TD>��${HtagName_}�����ο�${H_tagName}</TD><TD><B>${HseaNum}����</b></TD></TR>
<TR><TD>��${HtagName_}�ߥ�������Ϥο�${H_tagName}��</TD><TD><B>${HlandFirstMiss}��</b></TD></TR>
<TR><TD>��${HtagName_}���${H_tagName}��</TD><TD><B>${HinitialMoney}${HunitMoney}</b></TD></TR>
<TR><TD>��${HtagName_}����${H_tagName}��</TD><TD><B>${HinitialFood}${HunitFood}</b></TD></TR>

<TR>
<TD colspan=2 $HbgTitleCell>${HtagTH_}����¾������${H_tagTH}</TD>
</TR>
<TR><TD>��${HtagName_}��ư����������${H_tagName}</TD><TD><B>${HgiveupTurn}������</b></TD></TR>
<TR><TD>��${HtagName_}���祳�ޥ�����Ͽ�${H_tagName}</TD><TD><B>${HcommandMax}��</b></TD></TR>
</table>
<BR><HR>
<H1>${HtagHeader_}������ʹԥإ��${H_tagHeader}</H1>
<table width=300 border $HbgNameCell>
<TR>
<TD colspan=2 $HbgTitleCell>${HtagTH_}�����󹹿�����${H_tagTH}</TD>
</TR>
<TR>
<td WIDTH=100><NOBR>��${HtagName_}��ȯ����${H_tagName}</NOBR></TD><TD NOWRAP><B>$unit����</b>��${devrep}</TD>
</TR>
<TR><TD><NOBR>��${HtagName_}��Ʈ����${H_tagName}</NOBR></TD><TD NOWRAP><B>$fiunit����</b>��${firep}</TD>
</TR>
<TR>
<TD colspan=2 $HbgTitleCell>${HtagTH_}�ƴ��֤Υ������${H_tagTH}</TD>
</TR>
<TR>
<TD>��${HtagName_}ͽ��${H_tagName}��</TD><TD><B>$HyosenTurn������ޤ�</b></TD>
</TR>
<TR><TD>��${HtagName_}��ȯ����${H_tagName}</TD><TD><B><NOBR>$HdevTurn������</NOBR></b></TD>
</TR>
<TR><TD NOWRAP>��${HtagName_}��Ʈ����${H_tagName}</TD><TD NOWRAP><B>$HfigTurn������</b> (�辡��� + $HfigRepTurn������)</TD>
</TR>
</table>
END

my($fitone) = $HdevTurn + $HyosenTurn;
my($fittwo) = $fitone + $HfigTurn;
my($fitNum) = 1;
    out(<<END);
<BR><HR>
<H1>${HtagHeader_}������ʹԹ��� �ʰ��ḫɽ${H_tagHeader}</H1>
<table height=125 border $HbgNameCell>
<TR>
<td>${HtagName_}ͽ��${H_tagName}</td>
<TD $HbgCommentCell><B>0������$HyosenTurn</B></td>
</tr>
END

for($i = 2;$i <= $yteamNum;$i*=2) {

    if($i >= $yteamNum) { $fittwo += $HfigRepTurn; }

    out(<<END);
<TR>
<TD>$tes${HtagName_}��$fitNum���ﳫȯ����${H_tagName}</td>
<TD $HbgCommentCell><B>$HyosenTurn������$fitone</b></td>
</tr>
<TR>
<TD align=right>${HtagName_}��Ʈ����${H_tagName}</td><TD $HbgCommentCell><B>
END

    out (($fitone + 1) . "������$fittwo</b></td></tr>\n");
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
# ���������⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub teamDataMain {

    my($currentTID) = $HidToTeamNumber{$HteamID};
    my($team) = $Hteams[$currentTID];
    my($trank) = $currentTID + 1;
    # �ʤ������Υ����ब�ʤ����
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
#������ɽ��
my($hour, $min, $sec);
my($now) = time;
my($showTIME) = ($HislandLastTime + $HunitTime - $now);
$hour = int($showTIME / 3600);
$min  = int(($showTIME - ($hour * 3600)) / 60);
$sec  = $showTIME - ($hour * 3600) - ($min * 60);
    out(<<END);
<CENTER>
${HtagBig_}${HtagTName_}$team->{'name'}${H_tagTName}��������${H_tagBig}<P>
������ѥ���ɡ� $team->{'password'} ��
<P>
<B>������$HislandTurn</B> �ʼ��Υ�����ޤǡ�$hour���� $minʬ $sec�á�
<TABLE BORDER>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}������${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���������${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�͸�${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���쵬��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���쵬��${H_tagTH}</NOBR></TH>
</TR>
END
	$id = $team->{'id'};
	$tfarm = $team->{'farm'};
	$tfactory = $team->{'factory'};
	$tfarm = ($tfarm == 0) ? "��ͭ����" : "${tfarm}0$HunitPop";
	$tfactory = ($tfactory == 0) ? "��ͭ����" : "${tfactory}0$HunitPop";
	my($fightName) = '';
	my($fightMember) = '';
	if($team->{'fightid'} > 0) {
	    $fightName = "<A STYlE=\"text-decoration:none\" HREF=$HthisFile?TEAM=$team->{'fightid'}#data>${HtagTName_}$Hteams[$HidToTeamNumber{$team->{'fightid'}}]->{'name'}${H_tagTName}</A>";
	    $fightMember = $Hteams[$HidToTeamNumber{$team->{'fightid'}}]->{'member'};
	} else {
	    $fightName = "${HtagName_}<CENTER>�� �� ��${H_tagName}</CENTER>";
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
	out("</NOBR></TD></TR><TR><TD $HbgCommentCell COLSPAN=9 align=left nowrap=nowrap><NOBR>${HtagTH_}�����������С���${H_tagTH}");
	while($fightMember =~ s/([0-9]*),//) {
	    my($tIsland) = $Hislands[$HidToNumber{$1}];
	    out("<A STYlE=\"text-decoration:none\" HREF=$HthisFile?Sight=$tIsland->{'id'}>${HtagName_}$tIsland->{'name'}��${H_tagName}</A>��");
	}
    }
    out(<<END);
</NOBR></TD>
</TR></TABLE>
<P>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�͸�${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���쵬��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���쵬��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�ߥ�����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�ɱһ���${H_tagTH}</NOBR></TH>
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
	# ����ɽ��
	my($rank) = $iNumber + 1;
	my($farm) = $island->{'farm'};
	my($factory) = $island->{'factory'};
	$farm = ($farm == 0) ? "��ͭ����" : "${farm}0$HunitPop";
	$factory = ($factory == 0) ? "��ͭ����" : "${factory}0$HunitPop";
	my($comname) ="${HtagTH_}�����ȡ�${H_tagTH}";
	if(($island->{'ownername'} ne '0') && ($island->{'ownername'} ne "������")){
	    $comname = "<FONT COLOR=\"blue\"><B>$island->{'ownername'}��</b></font>";
	}
	if($island->{'absent'}  == 0) {
		$name = "${HtagName_}$island->{'name'}��${H_tagName}";
	} else {
	    $name = "${HtagName2_}$island->{'name'}��($island->{'absent'})${H_tagName2}";
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
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'fire'}ȯ</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'defence'}��</NOBR></TD>
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
<INPUT TYPE=TEXT NAME=CTEAMNAME VALUE="$team->{'name'}" SIZE="25">��
<INPUT TYPE=SUBMIT VALUE="������̾�ѹ�" onClick="chengeTeamName()" name=ChangeTeamName>
</FORM>
</CENTER>

END

}

# ���ϺѤߥ��ޥ��ɽ��
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
	$target = "̵��";
    }
    $target = "$HtagName_${target}��$H_tagName";
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

    my($j) = sprintf("%02d��", $number + 1);

    out("<NOBR>$HtagNumber_$j$H_tagNumber<FONT COLOR=\"$HnormalColor\">");

    if(($kind == $HcomDoNothing) || ($kind == $HcomAutoPrepare3) ||
       ($kind == $HcomGiveup)) {
	out("$name");
    } elsif(($kind == $HcomMissileNM) ||
	    ($kind == $HcomMissilePP)) {
	# �ߥ������
	my($n) = ($arg == 0 ? '̵����' : "${arg}ȯ");
	out("$target$point��$name($HtagName_$n$H_tagName)");
    } elsif($kind == $HcomSell) {
	# ����͢��
	out("$name$value");
    } elsif($kind == $HcomPropaganda) {
	# Ͷ�׳�ư
	out("$name");
    } elsif($kind == $HcomFood) {
	# ���
	out("$target��$name$value");
    } elsif($kind == $HcomDestroy) {
	# ����
	out("$point��$name");
    } elsif(($kind == $HcomFarm) ||
	     ($kind == $HcomFactory)) {	
	# ����դ�
	if($arg == 0) {
	    out("$point��$name");
	} else {
	    out("$point��$name($arg��)");
	}
    } else {
	# ��ɸ�դ�
	out("$point��$name");
    }

    out("</FONT></NOBR><BR>");
}

#----------------------------------------------------------------------
# �������̥�ɽ���⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub logTeamMain {
    # ����
    unlock();

    # �ƥ�ץ졼�Ƚ���
    tempTeamLogPage();
}

sub tempTeamLogPage {
    my($HcurrentTNumber) = $HidToTeamNumber{$HlogteamID};
    my($team) = $Hteams[$HcurrentTNumber];
    # �ʤ������Υ����ब�ʤ����
    if($HcurrentTNumber eq '' and $HlogteamID != 0) {
	tempProblem();
	return;
    }
    if($HlogteamID != 0) { $tName = $team->{'name'}; } else { $tName = '��������'; }
    out(<<END);
<CENTER>
<font size=+3><b>${HtagHeader_}${HtagName_}$tName ${H_tagName}�Ƕ�ν����${H_tagHeader}</b></font>
<FORM ACTION=$HthisFile METHOD=GET>
<SELECT NAME=LogFileTeam>
END
    for($i = 0; $i < $HteamNumber; $i++) {
	my($tTeam) = $Hteams[$i];
	out("<OPTION VALUE=$tTeam->{'id'}>$tTeam->{'name'}\n");
    }
    out(<<END);
</SELECT>
<INPUT TYPE=SUBMIT VALUE="ɽ��">
</FORM>
</CENTER>
END
    if($HlogteamID != 0) { logPrintTeamTop($team); }

}

# ��ɽ��
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
# �����ѹ��⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub changeTeamNameMain {
    # id����������
    my($currentTID) = $HidToTeamNumber{$HteamID};
    my($team) = $Hteams[$currentTID];
    $tempclose = '</TD><TD><INPUT TYPE="BUTTON" VALUE="  CLOSE  " onClick="top.close();"></TD></TR></TABLE>';
    # �ʤ������Υ����ब�ʤ����
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
	# ̾���ѹ��ξ��	
	# ̾���������������å�
	if($teamName =~ /[,\?\(\)\<\>]|^̵��$/) {
	    # �Ȥ��ʤ�̾��
	    unlock();
	    tempNewTeamBadName();
	    return;
	}

	# ̾���ν�ʣ�����å�
	if(nameToTeamNumber($teamName) != -1){
	    # ���Ǥ�ȯ������
	    unlock();
	    tempNewTeamAlready();
	    return;
	}

	# ̾�����ѹ�
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

    # �ǡ����񤭽Ф�
    writeTeamsFile();
    unlock();

    # �ѹ�����
    tempChange();
}

# ̾�����ѹ�
sub logChangeName {
    my($name1, $name2) = @_;
    logHistory("${HtagTName_}${name1}${H_tagTName}��̾�Τ�${HtagTName_}${name2}${H_tagTName}���ѹ����롣");
}

# �ѹ�����
sub tempChange {
    out(<<END);
${HtagBig_}�ѹ���λ���ޤ���${H_tagBig}$tempclose
END
}

# ���Ǥˤ���̾�����礬������
sub tempNewTeamAlready {
    out(<<END);
${HtagBig_}���Υ�����ϡ����Ǥˤ���ޤ���${H_tagBig}$tempclose
END
}

# ������̾���������ʾ��
sub tempNewTeamBadName {
    out(<<END);
${HtagBig_}',?()<>\$'�Ȥ����äƤ��ꡢ<BR>��̵�͡פȤ����ä��Ѥ�̾���Ϥ��ޤ��礦���${H_tagBig}$tempclose
END
}

# ̾���ѹ�����
sub tempChangeNothing {
    out(<<END);
${HtagBig_}��������ܤǤ�${H_tagBig}$tempclose
END
}

# ��Ͽ��
sub logHistory {
    open(HOUT, ">>${HdirName}/hakojima.his");
    print HOUT "$HislandTurn,$_[0]\n";
    close(HOUT);
}

#----------------------------------------------------------------------
# ��Ʈ�ε�Ͽ�⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub fightlogMain {

	out ("${HtagTitle_}����ε�Ͽ${H_tagTitle}<P>\n");
    # ����ε�Ͽ�ɤ߹���
    open(FOUT, "${HdirName}/fight.log");
	while($f = <FOUT>){
	    chomp($f);
	    $data = <FOUT>;
	    if($f == 0) {
		$fcount = "ͽ�����";
	    } elsif($data == 1) {
		$fcount = "�辡��";
	    } else {
		$fcount = "��" . $f . "����";
	    }
    out(<<END);
<HR><BLOCKQUOTE>
<H1>${HtagHeader_}����$fcount${H_tagHeader}</H1>
<TABLE BORDER>
<TR>
END

if($f) {
    out(<<END);
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�͸�${H_tagTH}</TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�Լ�${H_tagTH}</TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�͸�${H_tagTH}</TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�󽷶�${H_tagTH}</TH></TR>
END
} else {
    out(<<END);
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}������${H_tagTH}</TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�͸�${H_tagTH}</TH>
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


    # ����
    unlock();


}

#----------------------------------------------------------------------
# ���������ѥڡ���
#----------------------------------------------------------------------
# �ᥤ��
sub pageAdminMain {

    # �ѥ���ɥ����å�
    if($HoldPassword ne $masterPassword) {
	# password�ְ㤤
	unlock();
	tempWrongPassword();
	return;
    }

    # ����
    unlock();
    out(<<END);
<table><TR><TD width=100>
</TD>
<TD valign=top>
<H1>${HtagHeader_}��ζ������${H_tagHeader}</H1>

<FORM action="$HthisFile" method="POST">
�ɤ���������ޤ�����<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT><BR><BR>
ǰ�ΰ٤⤦���<BR>
<SELECT NAME="DELISLAND">
$HislandList
</SELECT><BR>
<INPUT TYPE="hidden" NAME ="OLDPASS" VALUE="$masterPassword"><BR>
<INPUT TYPE="submit" VALUE="�������" NAME="DeleteIsland"><BR><BR>
<font color=red><B>������</B></font>���ְ㤨̵���ͤ��ꤤ���ޤ���
</FORM>
</TD>
</TR></table>


<HR>
<center>$HtempBack</center>
END

}

1;
