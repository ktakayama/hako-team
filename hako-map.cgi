#----------------------------------------------------------------------
# Ȣ����� ver2.30
# �Ͽޥ⡼�ɥ⥸�塼��(ver1.00)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# Ȣ�����Υڡ���: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# Ȣ�������ȡ��ʥ���
# �Ͽޥ⡼�ɥ⥸�塼��
# $Id: hako-map.cgi,v 1.1 2003/07/02 03:09:49 gaba Exp $

#----------------------------------------------------------------------
# �Ѹ��⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub printIslandMain {
	# ����
	unlock();

	# id�������ֹ�����
	$HcurrentNumber = $HidToNumber{$HcurrentID};

	# �ʤ��������礬�ʤ����
	if($HcurrentNumber eq '') {
		tempProblem();
		return;
	}

	# ̾���μ���
	$HcurrentName = $Hislands[$HcurrentNumber]->{'name'};

	# �Ѹ�����
	tempPrintIslandHead(); # �褦����!!
	islandInfo(); # ��ξ���
	islandMap(0); # ����Ͽޡ��Ѹ��⡼��
	islandJump();
	# �����������Ǽ���
	if($HuseLbbs) {
		tempLbbsHead();	 # ������Ǽ���
		tempLbbsInput();   # �񤭹��ߥե�����
		tempLbbsContents(); # �Ǽ�������
	}

	# �ᶷ
	tempRecent(0);
}

#----------------------------------------------------------------------
# ��ȯ�⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub ownerMain {
	# ����
	unlock();

	# �⡼�ɤ�����
	$HmainMode = 'owner';

	# id����������
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = $island->{'name'};

	# �ѥ����
	if(!checkPassword($island->{'password'},$HinputPassword)) {
		# password�ְ㤤
		tempWrongPassword();
		return;
	}
	writeownerlog($HimgLine);

	# ��ȯ����
	if($HjavaMode eq 'java') {
		tempOwnerJava(); # ��Java������ץȳ�ȯ�ײ��
	}else{			   # ���̾�⡼�ɳ�ȯ�ײ��
		tempOwner();
	}


	# �����������Ǽ���
#	if($HuseLbbs) {
#		tempLbbsHead();	 # ������Ǽ���
#		tempLbbsInputOW();   # �񤭹��ߥե�����
#		tempLbbsContents(); # �Ǽ�������
#	}

	# �����������Ǽ���
	if($HuseLbbs) {
		tempLbbsHead();	 # ������Ǽ���
				if($HjavaMode eq 'java') {  # Java������ץ��ѽ񤭹��ߥե�����
						tempLbbsInputJava();
				}else{ tempLbbsInputOW(); } # �̾�⡼�ɤν񤭹��ߥե�����
		tempLbbsContents(); # �Ǽ�������
	}

	# �ᶷ
	tempRecent(1);
}

#----------------------------------------------------------------------
# ���ޥ�ɥ⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub commandMain {
	# id����������
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = $island->{'name'};

	# �ѥ����
	if(!checkPassword($island->{'password'},$HinputPassword)) {
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
	}

	# �⡼�ɤ�ʬ��
	my($command) = $island->{'command'};

	if($HcommandMode eq 'delete') {
		slideFront($command, $HcommandPlanNumber);
		tempCommandDelete();
	} elsif(($HcommandKind == $HcomAutoPrepare) ||
			($HcommandKind == $HcomAutoPrepare2)) {
		# �ե����ϡ��ե��Ϥʤ餷
		# ��ɸ�������
		makeRandomPointArray();
		my($land) = $island->{'land'};

		# ���ޥ�ɤμ������
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
		# ���ä�
		my($i);
		for($i = 0; $i < $HcommandMax; $i++) {
			slideFront($command, $HcommandPlanNumber);
		}
		tempCommandDelete();
	} elsif($HcommandKind == $HcomPrepRecr) {
		# ���Ω�ơ��Ϥʤ餷
		if($HcommandMode eq 'insert') {
			slideBack($command, $HcommandPlanNumber);
		}
		slideBack($command, $HcommandPlanNumber);
		tempCommandAdd();
		# ���ޥ�ɤ���Ͽ
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
		# ���ޥ�ɤ���Ͽ
		$command->[$HcommandPlanNumber] = {
			'kind' => $HcommandKind,
			'target' => $HcommandTarget,
			'x' => $HcommandX,
			'y' => $HcommandY,
			'arg' => $HcommandArg
			};
	}

	# �ǡ����ν񤭽Ф�
	writeIslandsFile($HcurrentID);

	# owner mode��
	ownerMain();

}

#----------------------------------------------------------------------
# ���������ϥ⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub commentMain {
	# id����������
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = $island->{'name'};

	# �ѥ����
	if(!checkPassword($island->{'password'},$HinputPassword)) {
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
	}

	# ��å������򹹿�
	$island->{'comment'} = htmlEscape($Hmessage);

	# �ǡ����ν񤭽Ф�
	writeIslandsFile($HcurrentID);

	# �����ȹ�����å�����
	tempComment();

	# owner mode��
	ownerMain();
}

#----------------------------------------------------------------------
# ������Ǽ��ĥ⡼��
#----------------------------------------------------------------------
# �ᥤ��

sub localBbsMain {
	# id�������ֹ�����
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	my($foreignName);

	# �ʤ��������礬�ʤ����
	if($HcurrentNumber eq '' && $HcurrentID != 0) {
		unlock();
		tempProblem();
		return;
	}

	# ����⡼�ɤ���ʤ���̾������å��������ʤ����
	if($HlbbsMode != 2) {
		if(($HlbbsName eq '') || ($HlbbsMessage eq '')) {
			unlock();
			tempLbbsNoMessage();
			return;
		}
	}

	# ��̵���Ѹ��԰ʳ��ϥѥ���ɥ����å�
		if($HlbbsMode == 0 && $HforID != 0) {
			# ����ԥ⡼��
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
			# ���⡼��
			if(!checkPassword($island->{'password'},$HinputPassword)) {
				# password�ְ㤤
				unlock();
				tempWrongPassword();
				return;
			}
		}

	my($lbbs);
	$lbbs = $island->{'lbbs'};

	# �⡼�ɤ�ʬ��
	if($HlbbsMode == 2) {
		# ����⡼��
		# ��å����������ˤ��餹
		slideBackLbbsMessage($lbbs, $HcommandPlanNumber);
		tempLbbsDelete();
	} else {
		# ��Ģ�⡼��
		# ��å���������ˤ��餹
		slideLbbsMessage($lbbs);

		if($HforID == 0 and $HlbbsMode == 0){
			$HlbbsMessage = htmlEscape($HlbbsMessage);
			$message = '3';
		} elsif (($HlbbsMode == 0) && ($HforID != $island->{'id'})){
			$HlbbsMessage = htmlEscape($HlbbsMessage) . "����<font size=-1 color=gray>(${foreignName}��)</font>";
			$message = '0';
		} else {
			$HlbbsMessage = htmlEscape($HlbbsMessage);
			$message = '1';
		}
		$HlbbsName = "$HislandTurn��" . htmlEscape($HlbbsName);
		$lbbs->[0] = "$message>$HlbbsName>$HlbbsMessage";

		tempLbbsAdd();
	}

	# �ǡ����񤭽Ф�
	writeIslandsFile($HcurrentID);

	# ��ȤΥ⡼�ɤ�
	if($HlbbsMode == 0) {
		printIslandMain();
	} else {
		ownerMain();
	}
}

# ������Ǽ��ĤΥ�å��������ĸ��ˤ��餹
sub slideLbbsMessage {
	my($lbbs) = @_;
	my($i);
#	pop(@$lbbs);
#	push(@$lbbs, $lbbs->[0]);
	pop(@$lbbs);
	unshift(@$lbbs, $lbbs->[0]);
}

# ������Ǽ��ĤΥ�å������������ˤ��餹
sub slideBackLbbsMessage {
	my($lbbs, $number) = @_;
	my($i);
	splice(@$lbbs, $number, 1);
	$lbbs->[$HlbbsMax - 1] = '0>>';
}

#----------------------------------------------------------------------
# ����Ͽ�
#----------------------------------------------------------------------

# �����ɽ��
sub islandInfo {
	my($island) = $Hislands[$HcurrentNumber];
	my($team) = $Hteams[$HidToTeamNumber{$island->{'teamid'}}];

	# ����ɽ��
	my($rank) = $HcurrentNumber + 1;
	my($farm) = $island->{'farm'};
	my($factory) = $island->{'factory'};
	$farm = ($farm == 0) ? "��ͭ����" : "${farm}0$HunitPop";
	$factory = ($factory == 0) ? "��ͭ����" : "${factory}0$HunitPop";

	my($mStr1) = '';
	my($mStr2) = '';
	if(($HhideMoneyMode == 1) || ($HmainMode eq 'owner')) {
		# ̵���ޤ���owner�⡼��
		$mStr1 = "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>";
		$mStr2 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$team->{'money'}$HunitMoney</NOBR></TD>";
	} elsif($HhideMoneyMode == 2) {
		my($mTmp) = aboutMoney($team->{'money'});

		# 1000��ñ�̥⡼��
		$mStr1 = "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>";
		$mStr2 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$mTmp</NOBR></TD>";
	}
	my($fightName) = '';
	my($fightMember) = '';
	if($team->{'fightid'}) {
		$fightName = "<A STYlE=\"text-decoration:none\" HREF=$HthisFile?TEAM=$team->{'fightid'}#data>${HtagTName_}$Hteams[$HidToTeamNumber{$team->{'fightid'}}]->{'name'}${H_tagTName}</A>";
		$fightMember = $Hteams[$HidToTeamNumber{$team->{'fightid'}}]->{'member'};
	} else {
		$fightName = "${HtagName_}<CENTER>�� �� ��${H_tagName}</CENTER>";
	}
	my($comname) ="${HtagTH_}�����ȡ�${H_tagTH}";
	if(($island->{'ownername'} ne '0') && ($island->{'ownername'} ne "������")){
		$comname = "<FONT COLOR=\"blue\"><B>$island->{'ownername'}��</b></font>";
	}
   if($HmainMode eq 'owner') {
		@access = stat("${teambbs}/$island->{'teamid'}.cgi");
		local($sec2,$min2,$hour2,$mday2,$mon2,$year) = localtime($access[9]);
		if($min2 < 10) { $min2 = 0 . $min2; }
		if($hour2 < 10) { $hour2 = 0 . $hour2; } $mon2++;
		$accessTime = "����<B>��ά��ļ��ǽ���������</B> ��$mon2/$mday2 $hour2:$min2��";
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
<B>������$HislandTurn</B> �ʼ��Υ�����ޤǡ�$hour���� $minʬ $sec�á�
$accessTime<TABLE BORDER>
<TR>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}��°������${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���������${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�͸�${H_tagTH}</NOBR></TH>
$mStr1
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���쵬��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���쵬��${H_tagTH}</NOBR></TH>
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
		out("</NOBR></TD></TR><TR><TD $HbgCommentCell COLSPAN=9 align=left nowrap=nowrap><NOBR>${HtagTH_}�����������С���${H_tagTH}");
		while($fightMember =~ s/([0-9]*),//) {
			my($tIsland) = $Hislands[$HidToNumber{$1}];
			out("<A STYlE=\"text-decoration:none\" HREF=$HthisFile?Sight=$tIsland->{'id'} target=_blank>${HtagName_}$tIsland->{'name'}��${H_tagName}</A>��");
		}
	}
out("</NOBR></TD></TR></TABLE></CENTER>");

}

# �Ͽޤ�ɽ��
# ������1�ʤ顢�ߥ�����������򤽤Τޤ�ɽ��
sub islandMap {
	my($mode) = @_;
	my($island);
	$island = $Hislands[$HcurrentNumber];

	out(<<END);
<CENTER><TABLE BORDER><TR><TD>
END
	# �Ϸ����Ϸ��ͤ����
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($l, $lv);

	# ���ޥ�ɼ���
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

	# ��ɸ(��)�����
	out("<IMG SRC=\"xbar.gif\" width=400 height=16><BR>");

	# ���Ϸ�����Ӳ��Ԥ����
	my($x, $y);
	for($y = 0; $y < $HislandSize; $y++) {
		# �������ܤʤ��ֹ�����
		if(($y % 2) == 0) {
			out("<IMG SRC=\"space${y}.gif\" width=16 height=32>");
		}

		# ���Ϸ������
		for($x = 0; $x < $HislandSize; $x++) {
			$l = $land->[$x][$y];
			$lv = $landValue->[$x][$y];
			landString($l, $lv, $x, $y, $mode, $comStr[$x][$y]);
		}

		# ������ܤʤ��ֹ�����
		if(($y % 2) == 1) {
			out("<IMG SRC=\"space${y}.gif\" width=16 height=32>");
		}

		# ���Ԥ����
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
			# ����
			$image = 'land14.gif';
			$alt = '��(����)';
		} else {
			# ��
			$image = 'land0.gif';
			$alt = '��';
		}
	} elsif($l == $HlandWaste) {
		# ����
		if($lv == 1) {
			$image = 'land13.gif'; # ������
			$alt = '����';
		} else {
			$image = 'land1.gif';
			$alt = '����';
		}
	} elsif($l == $HlandPlains) {
		# ʿ��
		$image = 'land2.gif';
		$alt = 'ʿ��';
	} elsif($l == $HlandForest) {
		# ��
		if($mode == 1) {
			$image = 'land6.gif';
			$alt = "��(${lv}$HunitTree)";
		} else {
			# �Ѹ��Ԥξ����ڤ��ܿ�����
			$image = 'land6.gif';
			$alt = '��';
		}
	} elsif($l == $HlandTown) {
		# Į
		my($p, $n);
		if($lv < 30) {
			$p = 3;
			$n = '¼';
		} elsif($lv < 100) {
			$p = 4;
			$n = 'Į';
		} else {
			$p = 5;
			$n = '�Ի�';
		}

		$image = "land${p}.gif";
		$alt = "$n(${lv}$HunitPop)";
	} elsif($l == $HlandFarm) {
		# ����
		$image = 'land7.gif';
		$alt = "����(${lv}0${HunitPop}����)";
	} elsif($l == $HlandFactory) {
		# ����
		$image = 'land8.gif';
		$alt = "����(${lv}0${HunitPop}����)";
	} elsif($l == $HlandBase) {
		if($mode == 0) {
			# �Ѹ��Ԥξ��Ͽ��Τդ�
			$image = 'land6.gif';
			$alt = '��';
		} else {
			# �ߥ��������
			my($level) = expToLevel($l, $lv);
			$image = 'land9.gif';
			$alt = "�ߥ�������� (��٥� ${level}/�и��� $lv)";
		}
	} elsif($l == $HlandDefence) {
		# �ɱһ���
		if($mode == 0) {
			# �Ѹ��Ԥξ��Ͽ��Τդ�
			$image = 'land6.gif';
			$alt = '��';
		} else {
			$image = 'land10.gif';
			$alt = '�ɱһ���';
		}
	} elsif($l == $HlandHaribote) {
		# �ϥ�ܥ�
		$image = 'land10.gif';
		if($mode == 0) {
			# �Ѹ��Ԥξ����ɱһ��ߤΤդ�
			$alt = '�ɱһ���';
		} else {
			$alt = '�ϥ�ܥ�';
		}
	} elsif($l == $HlandMonument) {
		# ��ǰ��
		$image = $HmonumentImage[$lv];
		$alt = $HmonumentName[$lv];
	}


	# ��ȯ���̤ξ��ϡ���ɸ����
	if($mode == 1) {
		out("<A HREF=\"JavaScript:void(0);\" onclick=\"ps($x,$y)\" onMouseOver=\"ShowMsg('$point $alt $comStr'); return true;\">");
	} else{
		out("<A HREF=\"JavaScript:void(0);\" onMouseOver=\"ShowMsg('$point $alt $comStr'); return true;\">");
	}

	out("<IMG SRC=\"$image\" ALT=\"$point $alt $comStr\" width=32 height=32 BORDER=0>");

	# ��ɸ�����Ĥ�
	out("</A>");
}


#----------------------------------------------------------------------
# �ƥ�ץ졼�Ȥ���¾
#----------------------------------------------------------------------
# ���̥�ɽ��
sub logPrintLocal {
	my($mode) = @_;
	my($i);
	for($i = 0; $i < $HlogMax; $i++) {
		logFilePrint($i, $HcurrentID, $mode, 1);
	}
}

# ������ؤ褦��������
sub tempPrintIslandHead {
	out(<<END);
<CENTER>
${HtagBig_}${HtagName_}��${HcurrentName}���${H_tagName}�ؤ褦��������${H_tagBig}<BR>
$HtempBack<BR>
</CENTER>
END
}

# �����糫ȯ�ײ�
sub tempOwner {
	my($island);
	$island = $Hislands[$HcurrentNumber];
	my($team) = $Hteams[$HidToTeamNumber{$island->{'teamid'}}];
	out(<<END);
<CENTER>
${HtagBig_}${HtagName_}${HcurrentName}��${H_tagName}��ȯ�ײ�${H_tagBig}<BR>
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
<INPUT TYPE=submit VALUE="�ײ�����" NAME=CommandButton$island->{'id'}>
<HR>
<B>�ѥ����</B></BR>
<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword">
<HR>
<B>�ײ��ֹ�</B><SELECT NAME=NUMBER>
END
	# �ײ��ֹ�
	my($j, $i);
	for($i = 0; $i < $HcommandMax; $i++) {
		$j = $i + 1;
		out("<OPTION VALUE=$i>$j\n");
	}

	out(<<END);
</SELECT><BR>
<HR>
<B>��ȯ�ײ�</B><BR>
<SELECT NAME=COMMAND>
END

	#���ޥ��
	my($kind, $cost, $s);
	for($i = 0; $i < $HcommandTotal; $i++) {
		$kind = $HcomList[$i];
		$cost = $HcomCost[$kind];
		if($cost == 0) {
			$cost = '̵��'
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
<B>��ɸ(</B>
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
<B>����</B><SELECT NAME=AMOUNT>
END

	# ����
	for($i = 0; $i < 50; $i++) {
		out("<OPTION VALUE=$i>$i\n");
	}

	out(<<END);
</SELECT>
<HR>
<B>��ɸ����</B><BR>
<SELECT NAME=TARGETID>
END
out(getTargetList($team->{'id'},$team->{'fightid'}));
	out(<<END);
<BR>
</SELECT>
<HR>
<B>ư��</B><BR>
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=insert CHECKED>����
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=write>���<BR>
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=delete>���
<HR>
<INPUT TYPE=submit VALUE="�ײ�����" NAME=CommandButton$island->{'id'}>

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
<nobr><center>�ߥ�����ȯ�;�¿�[<b> $island->{'fire'} </b>]ȯ</center></nobr>
</TD>
<TD $HbgMapCell ALIGN=CENTER>
<FONT SIZE=+1><B>
<A HREF="JavaScript:void(0);" STYlE="text-decoration:none" onClick="openBBS();return false;">
��ά��ļ���</A>
����������
<A HREF="JavaScript:void(0);" STYlE="text-decoration:none" onClick="openTEAM();return false;">
 ���������� </A>
</B>
</FONT>
END
	islandMap(1);	# ����Ͽޡ���ͭ�ԥ⡼��
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
${HtagBig_}�����ȹ���${H_tagBig}<BR>
<FORM action="$HthisFile" method="POST">
������<INPUT TYPE=text NAME=MESSAGE SIZE=80 VALUE="$island->{'comment'}"><BR>
�ѥ����<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword">
<INPUT TYPE=submit VALUE="�����ȹ���" NAME=MessageButton$island->{'id'}>
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

	out("<A STYlE=\"text-decoration:none\" HREF=\"JavaScript:void(0);\" onClick=\"ns($number)\"><NOBR>$HtagNumber_$j$H_tagNumber<FONT COLOR=\"$HnormalColor\">");

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
		if($arg != 0) {
			out("$point��$name(ͽ��${value})");
		} else {
			out("$point��$name");
		}
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

	out("</FONT></NOBR></A><BR>");
}

# ������Ǽ���
sub tempLbbsHead {
	out(<<END);
<CENTER>
<HR>
${HtagBig_}${HtagName_}${HcurrentName}��${H_tagName}�Ѹ����̿�${H_tagBig}<BR>
</CENTER>
END
}

# ������Ǽ������ϥե�����
sub tempLbbsInput {
	out(<<END);
<CENTER>
<FORM action="$HthisFile" method="POST">
<font color=red><B>�礬̵�����⵭Ģ�Ǥ��ޤ����������������Ƥ˴ط���̵��ȯ���ϡ�����������${bbsname}�ؤ��ꤤ���ޤ���</b></font>
<TABLE BORDER>
<TR>
<TH>̾��</TH>
<TH>����</TH>
</TR>
<TR>
<TD><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD><INPUT TYPE="text" SIZE=80 NAME="LBBSMESSAGE"></TD>
</TR>
<TR>
<TD colspan="2">��ʬ���硧
<SELECT NAME="ISLANDID">
<OPTION value="0">��̵���Ѹ���
$HislandList</SELECT>
���ѥ���ɡ�<INPUT TYPE="password" SIZE=32 MAXLENGTH=32 NAME=PASSWORD VALUE="$HdefaultPassword">
<INPUT TYPE="submit" VALUE="��Ģ����" NAME="LbbsButtonFO$HcurrentID"></TD>
</TR>
</TABLE>
</FORM>
</CENTER>
END
}

# ������Ǽ������ϥե����� owner mode��
sub tempLbbsInputOW {
	out(<<END);
<CENTER>
<FORM action="$HthisFile" method="POST">
<TABLE BORDER>
<TR>
<TH>̾��</TH>
<TH COLSPAN=2>����</TH>
</TR>
<TR>
<TD><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD COLSPAN=2><INPUT TYPE="text" SIZE=80 NAME="LBBSMESSAGE"></TD>
</TR>
<TR>
<TH>�ѥ����</TH>
<TH COLSPAN=2>ư��</TH>
</TR>
<TR>
<TD><INPUT TYPE=password SIZE=32 MAXLENGTH=32 NAME=PASSWORD VALUE="$HdefaultPassword"></TD>
<TD align=right>
<INPUT TYPE="submit" VALUE="��Ģ����" NAME="LbbsButtonOW$HcurrentID">
</TD>
<TD align=right>
�ֹ�
<SELECT NAME=NUMBER>
END
	# ȯ���ֹ�
	my($j, $i);
	for($i = 0; $i < $HlbbsMax; $i++) {
		$j = $i + 1;
		out("<OPTION VALUE=$i>$j\n");
	}
	out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="�������" NAME="LbbsButtonDL$HcurrentID">
</TD>
</TR>
</TABLE>
</FORM>
</CENTER>
END
}

# ������Ǽ�������
sub tempLbbsContents {
	my($lbbs, $line);
	$lbbs = $Hislands[$HcurrentNumber]->{'lbbs'};
	out(<<END);
<CENTER>
<TABLE BORDER>
<TR>
<TH>�ֹ�</TH>
<TH>��Ģ����</TH>
</TR>
END

	my($i);
	for($i = 0; $i < $HlbbsMax; $i++) {
		$line = $lbbs->[$i];
		if($line =~ /([0-9]*)\>(.*)\>(.*)$/) {
			my($j) = $i + 1;
			out("<TR><TD align=center>$HtagNumber_$j$H_tagNumber</TD>");
			if($1 == 0) {
				# �Ѹ���
				out("<TD>$HtagLbbsSS_$2 > $3$H_tagLbbsSS</TD></TR>");
			} elsif($1 == 3) {
				# ��̵���Ѹ���
				out("<TD>$HtagLbbsSK_$2 > $3$H_tagLbbsSK</TD></TR>");
			} else {
				# ���
				out("<TD>$HtagLbbsOW_$2 > $3$H_tagLbbsOW</TD></TR>");
			}
		}
	}

	out(<<END);
</TD></TR></TABLE></CENTER>
END
}

# ������Ǽ��Ĥ�̾������å��������ʤ����
sub tempLbbsNoMessage {
	out(<<END);
${HtagBig_}̾���ޤ������Ƥ��󤬶���Ǥ���${H_tagBig}$HtempBack
END
}

# �񤭤��ߺ��
sub tempLbbsDelete {
	out(<<END);
${HtagBig_}��Ģ���Ƥ������ޤ���${H_tagBig}<HR>
END
}

# ���ޥ����Ͽ
sub tempLbbsAdd {
	out(<<END);
${HtagBig_}��Ģ��Ԥ��ޤ���${H_tagBig}<HR>
END
}

# ���ޥ�ɺ��
sub tempCommandDelete {
	out(<<END);
${HtagBig_}���ޥ�ɤ������ޤ���${H_tagBig}<HR>
END
}

# ���ޥ����Ͽ
sub tempCommandAdd {
	out(<<END);
${HtagBig_}���ޥ�ɤ���Ͽ���ޤ���${H_tagBig}<HR>
END
}

# �������ѹ�����
sub tempComment {
	out(<<END);
${HtagBig_}�����Ȥ򹹿����ޤ���${H_tagBig}<HR>
END
}

# �ᶷ
sub tempRecent {
	my($mode) = @_;
	out(<<END);
<HR>
${HtagBig_}${HtagName_}${HcurrentName}��${H_tagName}�ζᶷ${H_tagBig}<BR>
END
	logPrintLocal($mode);
}

#��ȯ��ˬ������������
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
	#�ޤ��񤭽Ф�
	open(OwOut, ">>${log_file}");
		$userIP = $ENV{'REMOTE_ADDR'};

		printf OwOut "%04d\/%02d\/%02d %02d:%02d:%02d", $Year, $month, $day, $hour, $min, $sec;
		print OwOut jcode::sjis(", $userIP, ${HcurrentName}��, $team->{'name'}, ${view}, ${wJavaMode}\n");

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
