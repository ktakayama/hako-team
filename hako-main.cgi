#!/usr/local/bin/perl
# ���ϥ����С��˹�碌���ѹ����Ʋ�������
# perl5�ѤǤ���

#----------------------------------------------------------------------
# Ȣ����� ver2.30
# �ᥤ�󥹥���ץ�(ver1.02)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# Ȣ�����Υڡ���: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# Ȣ�������ȡ��ʥ���
# �ᥤ�󥹥���ץ�
# $Id: hako-main.cgi,v 1.3 2004/06/02 02:04:26 gaba Exp $

require './hako-ini.cgi';

#----------------------------------------
# ���Ϥηи���
#----------------------------------------
# �и��ͤκ�����
$HmaxExpPoint = 200; # ������������Ǥ�255�ޤ�

# ��٥�κ�����
my($maxBaseLevel) = 5;  # �ߥ��������
my($maxSBaseLevel) = 3; # �������

# �и��ͤ������Ĥǥ�٥륢�åפ�
my(@baseLevelUp, @sBaseLevelUp);
@baseLevelUp = (20, 60, 120, 200); # �ߥ��������
@sBaseLevelUp = (50, 200);         # �������

#----------------------------------------
# �ҳ�
#----------------------------------------
# ��������
$HdisFallBorder = 110; # �����³��ι���(Hex��)
$HdisFalldown   = 30; # ���ι�����Ķ�������γ�Ψ

#----------------------------------------
# �޴ط�
#----------------------------------------

# �ޤ�̾��
$Hprize[0] = '��������';
$Hprize[1] = '�˱ɾ�';
$Hprize[2] = 'Ķ�˱ɾ�';
$Hprize[3] = '����˱ɾ�';
$Hprize[4] = 'ʿ�¾�';
$Hprize[5] = 'Ķʿ�¾�';
$Hprize[6] = '���ʿ�¾�';
$Hprize[7] = '�����';
$Hprize[8] = 'Ķ�����';
$Hprize[9] = '��˺����';

#----------------------------------------
# �����ط�
#----------------------------------------
# <BODY>�����Υ��ץ����
my($htmlBody) = 'BGCOLOR="#EEFFFF"';
$Body = "<BODY $htmlBody>";
# ����
# �����ȥ�ʸ��
$HtagTitle_ = '<FONT SIZE=7 COLOR="#8888ff">';
$H_tagTitle = '</FONT>';

# H1������
$HtagHeader_ = '<FONT COLOR="#4444ff">';
$H_tagHeader = '</FONT>';

# �礭��ʸ��
$HtagBig_ = '<FONT SIZE=6>';
$H_tagBig = '</FONT>';

# ���̾���ʤ�
$HtagName_ = '<FONT COLOR="#a06040"><B>';
$H_tagName = '</B></FONT>';

# �������̾��
$HtagTName_ = '<FONT COLOR="#A0522D"><B>[';
$H_tagTName = ']</B></FONT>';

#$HtagTName_ = '<FONT COLOR="#A0522D"><B>&lt';
#$H_tagTName = '&gt</B></FONT>';

# �����ʤä����̾��
$HtagName2_ = '<FONT COLOR="#808080"><B>';
$H_tagName2 = '</B></FONT>';

# �����ʤä��������̾��
$HtagTName2_ = '<FONT COLOR="#808080"><B>[';
$H_tagTName2 = ']</B></FONT>';

# ��̤��ֹ�ʤ�
$HtagNumber_ = '<FONT COLOR="#800000"><B>';
$H_tagNumber = '</B></FONT>';

# ���ɽ�ˤ����븫����
$HtagTH_ = '<FONT COLOR="#C00000"><B>';
$H_tagTH = '</B></FONT>';

# ��ȯ�ײ��̾��
$HtagComName_ = '<FONT COLOR="#d08000"><B>';
$H_tagComName = '</B></FONT>';

# �ҳ�
$HtagDisaster_ = '<FONT COLOR="#ff0000"><B>';
$H_tagDisaster = '</B></FONT>';

# ������Ǽ��ġ��Ѹ��Ԥν񤤤�ʸ��
$HtagLbbsSS_ = '<FONT COLOR="#0000ff"><B>';
$H_tagLbbsSS = '</B></FONT>';

# ������Ǽ��ġ����ν񤤤�ʸ��
$HtagLbbsOW_ = '<FONT COLOR="#ff0000"><B>';
$H_tagLbbsOW = '</B></FONT>';

# ������Ǽ��ġ���̵���Ѹ��Ԥν񤤤�ʸ��
$HtagLbbsSK_ = '<FONT COLOR="#003333"><B>';
$H_tagLbbsSK = '</B></FONT>';

# �̾��ʸ����(��������Ǥʤ���BODY�����Υ��ץ�����������ѹ����٤�
$HnormalColor = '#000000';

# ��������
$HtagFico_ = '<FONT SIZE="7" COLOR="#4444ff">';
$H_tagFico = '</FONT>';

# ���ɽ�������°��
$HbgTitleCell   = 'BGCOLOR="#ccffcc"'; # ���ɽ���Ф�
$HbgNumberCell  = 'BGCOLOR="#ccffcc"'; # ���ɽ���
$HbgNameCell    = 'BGCOLOR="#ccffff"'; # ���ɽ���̾��
$HbgInfoCell    = 'BGCOLOR="#ccffff"'; # ���ɽ��ξ���
$HbgCommentCell = 'BGCOLOR="#ccffcc"'; # ���ɽ��������
$HbgInputCell   = 'BGCOLOR="#ccffcc"'; # ��ȯ�ײ�ե�����
$HbgMapCell     = 'BGCOLOR="#ccffcc"'; # ��ȯ�ײ��Ͽ�
$HbgCommandCell = 'BGCOLOR="#ccffcc"'; # ��ȯ�ײ����ϺѤ߷ײ�

# ͽ���������åɥ饤��
$YbgNumberCell  = 'BGCOLOR="#F0BBDA"'; # ���ɽ���
$YbgNameCell    = 'BGCOLOR="#E4CCF5"'; # ���ɽ���̾��
$YbgInfoCell    = 'BGCOLOR="#E4CCF5"'; # ���ɽ��ξ���
$YbgCommentCell = 'BGCOLOR="#F0BBDA"'; # ���ɽ��������

#----------------------------------------------------------------------
# ���ߤˤ�ä����ꤹ����ʬ�ϰʾ�
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# ����ʹߤΥ�����ץȤϡ��ѹ�����뤳�Ȥ����ꤷ�Ƥ��ޤ��󤬡�
# �����äƤ⤫�ޤ��ޤ���
# ���ޥ�ɤ�̾�������ʤʤɤϲ��䤹���Ȼפ��ޤ���
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# �Ƽ����
#----------------------------------------------------------------------
# ���Υե�����
$HthisFile = "$baseDir/hako-main.cgi";

# ���ץ�å��̿��� CGI
$HjavaFile = "$baseDir/hako-java.cgi";

# �Ϸ��ֹ�
$HlandSea      = 0;  # ��
$HlandWaste    = 1;  # ����
$HlandPlains   = 2;  # ʿ��
$HlandTown     = 3;  # Į��
$HlandForest   = 4;  # ��
$HlandFarm     = 5;  # ����
$HlandFactory  = 6;  # ����
$HlandBase     = 7;  # �ߥ��������
$HlandDefence  = 8;  # �ɱһ���
$HlandSbase    = 9;  # �������
$HlandHaribote = 12; # �ϥ�ܥ�

# ���ޥ��
$HcommandTotal = 22; # ���ޥ�ɤμ���

# �ײ��ֹ������
# ���Ϸ�
$HcomPrepare  = 01; # ����
$HcomPrepare2 = 02; # �Ϥʤ餷
$HcomReclaim  = 03; # ���Ω��
$HcomDestroy  = 04; # ����
$HcomSellTree = 05; # Ȳ��
$HcomPrepRecr = 06; # ���Ω�ơ��Ϥʤ餷

# ����
$HcomPlant    = 11; # ����
$HcomFarm     = 12; # ��������
$HcomFactory  = 13; # �������
$HcomBase     = 14; # �ߥ�������Ϸ���
$HcomDbase    = 15; # �ɱһ��߷���
$HcomHaribote = 16; # �ϥ�ܥ�����
$HcomFastFarm = 17; # ��®��������

# ȯ�ͷ�
$HcomMissileNM   = 31; # �ߥ�����ȯ��
$HcomMissilePP   = 32; # PP�ߥ�����ȯ��

# ���ķ�
$HcomDoNothing  = 41; # ��ⷫ��
$HcomSell       = 42; # ����͢��
$HcomFood       = 43; # �������
$HcomPropaganda = 44; # Ͷ�׳�ư

# ��ư���Ϸ�
$HcomAutoPrepare  = 61; # �ե�����
$HcomAutoPrepare2 = 62; # �ե��Ϥʤ餷
$HcomAutoDelete   = 63; # �����ޥ�ɾõ�
$HcomAutoPrepare3 = 64; # ��缫ư�Ϥʤ餷

# ����
@HcomList =
    ($HcomPrepare, $HcomPrepare2, $HcomReclaim, $HcomDestroy, $HcomPrepRecr, 
     $HcomSellTree, $HcomPlant, $HcomFarm, $HcomFactory, $HcomFastFarm,
     $HcomBase, $HcomDbase, $HcomMissileNM, $HcomMissilePP, 
     $HcomDoNothing, $HcomSell, $HcomFood, $HcomPropaganda,
     $HcomAutoPrepare, $HcomAutoPrepare2, $HcomAutoPrepare3, $HcomAutoDelete);

# �ײ��̾��������
$HcomName[$HcomPrepare]      = '����';
$HcomCost[$HcomPrepare]      = 5;
$HcomName[$HcomPrepare2]     = '�Ϥʤ餷';
$HcomCost[$HcomPrepare2]     = 100;
$HcomName[$HcomReclaim]      = '���Ω��';
$HcomCost[$HcomReclaim]      = 100;
$HcomName[$HcomPrepRecr]    = '���Ω��+�Ϥʤ餷';
$HcomCost[$HcomPrepRecr]    = 0;
$HcomName[$HcomDestroy]      = '����';
$HcomCost[$HcomDestroy]      = 200;
$HcomName[$HcomSellTree]     = 'Ȳ��';
$HcomCost[$HcomSellTree]     = 0;
$HcomName[$HcomPlant]        = '����';
$HcomCost[$HcomPlant]        = 10;
$HcomName[$HcomFarm]         = '��������';
$HcomCost[$HcomFarm]         = 20;
$HcomName[$HcomFastFarm]     = '��®��������';
$HcomCost[$HcomFastFarm]     = 500;
$HcomName[$HcomFactory]      = '�������';
$HcomCost[$HcomFactory]      = 100;
$HcomName[$HcomBase]         = '�ߥ�������Ϸ���';
$HcomCost[$HcomBase]         = 300;
$HcomName[$HcomDbase]        = '�ɱһ��߷���';
$HcomCost[$HcomDbase]        = 600;
$HcomName[$HcomHaribote]     = '�ϥ�ܥ�����';
$HcomCost[$HcomHaribote]     = 1;
$HcomName[$HcomMissileNM]    = '�ߥ�����ȯ��';
$HcomCost[$HcomMissileNM]    = 20;
$HcomName[$HcomMissilePP]    = 'PP�ߥ�����ȯ��';
$HcomCost[$HcomMissilePP]    = 50;
$HcomName[$HcomPropaganda]   = 'Ͷ�׳�ư';
$HcomCost[$HcomPropaganda]   = 800;
$HcomName[$HcomDoNothing]    = '��ⷫ��';
$HcomCost[$HcomDoNothing]    = 0;
$HcomName[$HcomSell]         = '����͢��';
$HcomCost[$HcomSell]         = -100;
$HcomName[$HcomFood]         = '�������';
$HcomCost[$HcomFood]         = -100;
$HcomName[$HcomAutoPrepare]  = '���ϼ�ư����';
$HcomCost[$HcomAutoPrepare]  = 0;
$HcomName[$HcomAutoPrepare2] = '�Ϥʤ餷��ư����';
$HcomCost[$HcomAutoPrepare2] = 0;
$HcomName[$HcomAutoPrepare3] = '��缫ư�Ϥʤ餷';
$HcomCost[$HcomAutoPrepare3] = 0;
$HcomName[$HcomAutoDelete]   = '���ײ�����ű��';
$HcomCost[$HcomAutoDelete]   = 0;

#----------------------------------------------------------------------
# �ѿ�
#----------------------------------------------------------------------

# COOKIE
my($defaultID);       # ���̾��
my($defaultTarget);   # �������åȤ�̾��


# ��κ�ɸ��
$HpointNumber = $HislandSize * $HislandSize;

#----------------------------------------------------------------------
# �ᥤ��
#----------------------------------------------------------------------

# jcode.pl��require
require($jcode);

# �����ץ��
$HtempBack = "<A HREF=\"$HthisFile?\">${HtagBig_}�ȥåפ����${H_tagBig}</A>";

# ��å��򤫤���
if(!hakolock()) {
    # ��å�����
    # �إå�����
    tempHeader();

    # ��å����ԥ�å�����
    tempLockFail();

    # �եå�����
    tempFooter();

    # ��λ
    exit(0);
}

# ����ν����
srand(time^$$);

# COOKIE�ɤߤ���
cookieInput();

# CGI�ɤߤ���
cgiInput();

# ��ǡ������ɤߤ���
if(readIslandsFile($HcurrentID) == 0) {
    unlock();
    tempHeader();
    tempNoDataFile();
    tempFooter();
    exit(0);
}

# ������ǡ����ɤ߹���
if(readTeamsFile() == 0) {
    unlock();
    tempHeader();
    tempNoDataFile();
    tempFooter();
    exit(0);
}


# �ƥ�ץ졼�Ȥ�����
tempInitialize();

# COOKIE����
cookieOutput();

# �إå�����
#tempHeader();
if($HmainMode eq 'owner' && $HjavaMode eq 'java' ||
   $HmainMode eq 'commandJava' || # ���ޥ�����ϥ⡼��
   $HmainMode eq 'comment' && $HjavaMode eq 'java' || #���������ϥ⡼��
   $HmainMode eq 'lbbs' && $HjavaMode eq 'java') { #���������ϥ⡼��
	$Body = "<BODY onload=\"init()\" $htmlBody>";
   	require('hako-js.cgi');
	require('hako-map.cgi');
	# �إå�����
	tempHeader();
    if($HmainMode eq 'commandJava') {
    	# ��ȯ�⡼��
    	commandJavaMain();
    } elsif($HmainMode eq 'comment') {
    	# ���������ϥ⡼��
    	commentMain();
    } elsif($HmainMode eq 'lbbs') {
	# ������Ǽ��ĥ⡼��
        localBbsMain();
    }else{
	ownerMain();
    }
	# �եå�����
	tempFooter();
	# ��λ
	exit(0);
    }elsif($HmainMode eq 'landmap'){
   	require('hako-js.cgi');
        require('hako-map.cgi');
	$Body = "<BODY $htmlBody>";
	# �إå�����
	tempHeaderJava();
    # �Ѹ��⡼��
    printIslandJava();
	# �եå�����
	tempFooter();
	# ��λ
	exit(0);
}else{
	# �إå�����
	tempHeader();
}

if($HmainMode eq 'turn') {
    # ������ʹ�
    require('hako-turn.cgi');
    require('hako-top.cgi');
    turnMain();

} elsif($HmainMode eq 'new') {
    # ��ο�������
    require('hako-turn.cgi');
    require('hako-map.cgi');
    newIslandMain();

} elsif($HmainMode eq 'print') {
    # �Ѹ��⡼��
    require('hako-map.cgi');
    printIslandMain();

} elsif($HmainMode eq 'owner') {

    # ��ȯ�⡼��
    require('hako-map.cgi');
    ownerMain();

} elsif($HmainMode eq 'command') {
    # ���ޥ�����ϥ⡼��
    require('hako-map.cgi');
    commandMain();

} elsif($HmainMode eq 'comment') {
    # ���������ϥ⡼��
    require('hako-map.cgi');
    commentMain();

} elsif($HmainMode eq 'lbbs') {

    # ������Ǽ��ĥ⡼��
    require('hako-map.cgi');
    localBbsMain();

} elsif($HmainMode eq 'change') {
    # �����ѹ��⡼��
    require('hako-turn.cgi');
    require('hako-top.cgi');
    changeMain();

} elsif($HmainMode eq 'logView') {
    # LOG�⡼��
    require('hako-more.cgi');
    logViewMain();

} elsif($HmainMode eq 'logTeam') {
    # LOG�⡼��
    require('hako-more.cgi');
    logTeamMain();

} elsif($HmainMode eq 'help') {
    # ��HELP�⡼��
    require('hako-more.cgi');
    helpMain();

} elsif($HmainMode eq 'teamdata') {
    # ��������
    require('hako-more.cgi');
    teamDataMain();

} elsif($HmainMode eq 'HchangeTName') {
    # ������̾�ѹ�
    require('hako-more.cgi');
    changeTeamNameMain();

} elsif($HmainMode eq 'fightlog') {
    # ����Ʈ�ε�Ͽ�⡼��
    require('hako-more.cgi');
    fightlogMain();

} elsif($HmainMode eq 'adminpage') {
    # �����Բ���
    require('hako-more.cgi');
    pageAdminMain();

} elsif($HmainMode eq 'delete') {
    # �����⡼��
    require('hako-turn.cgi');
    require('hako-top.cgi');
    changeMain();

} else {
    # ����¾�ξ��ϥȥåץڡ����⡼��
    require('hako-top.cgi');
    topPageMain();
}

# �եå�����
tempFooter();

# ��λ
exit(0);

# ���ޥ�ɤ����ˤ��餹
sub slideFront {
    my($command, $number) = @_;
    my($i);

    # ���줾�줺�餹
    splice(@$command, $number, 1);

    # �Ǹ�˻�ⷫ��
    $command->[$HcommandMax - 1] = {
	'kind' => $HcomDoNothing,
	'target' => 0,
	'x' => 0,
	'y' => 0,
	'arg' => 0
	};
}

# ���ޥ�ɤ��ˤ��餹
sub slideBack {
    my($command, $number) = @_;
    my($i);

    # ���줾�줺�餹
    return if $number == $#$command;
    pop(@$command);
    splice(@$command, $number, 0, $command->[$number]);
}

#----------------------------------------------------------------------
# ��ǡ���������
#----------------------------------------------------------------------

# ����ǡ����ɤߤ���
sub readIslandsFile {
    my($num) = @_; # 0�����Ϸ��ɤߤ��ޤ�
                   # -1�������Ϸ����ɤ�
                   # �ֹ���Ȥ�������Ϸ��������ɤߤ���

    # �ǡ����ե�����򳫤�
    if(!open(IN, "${HdirName}/hakojima.dat")) {
	rename("${HdirName}/hakojima.tmp", "${HdirName}/hakojima.dat");
	if(!open(IN, "${HdirName}/hakojima.dat")) {
	    return 0;
	}
    }

    # �ƥѥ�᡼�����ɤߤ���
    $HislandTurn     = int(<IN>); # �������

    $HislandLastTime = int(<IN>); # �ǽ���������
    if($HislandLastTime == 0) {
	return 0;
    }
    $HislandNumber   = int(<IN>); # ������
    $HislandNextID   = int(<IN>); # ���˳�����Ƥ�ID
    $HteamNumber     = int(<IN>); # �������
    $HturnCount      = int(<IN>); # ������
    $HnextCTurn      = int(<IN>); # �ڤ��ؤ�������
    $HfightMode      = int(<IN>); # ���ߤ���Ʈ�⡼��
    $HfightCount     = int(<IN>); # �������ܤ�

    # ���������Ƚ��
    my($now) = time;
    if(((($Hdebug == 1) && 
	($HmainMode eq 'Hdebugturn')) ||
       (($now - $HislandLastTime) >= $HunitTime)) && ($HteamNumber > 1)) {
	$HmainMode = 'turn';
	$num = -1; # �����ɤߤ���
    }

    # ����ɤߤ���
    my($i);
    for($i = 0; $i < $HislandNumber; $i++) {
	 $Hislands[$i] = readIsland($num);
	 $HidToNumber{$Hislands[$i]->{'id'}} = $i;
    }

    # �ե�������Ĥ���
    close(IN);

    return 1;
}

# ��ҤȤ��ɤߤ���
sub readIsland {
    my($num) = @_;
    my($name, $id, $prize, $absent, $comment, $password, $food,
       $pop, $area, $farm, $factory, $teamid, $defence, $fire, $ownername);
    $name = <IN>; # ���̾��
    chomp($name);
    if($name =~ s/,(.*)$//g) {
	$defence = int($1);
    } else {
	$defence = 0;
    }
    $id = int(<IN>); # ID�ֹ�
    $prize = int(<IN>); # ����
    $absent = int(<IN>); # Ϣ³��ⷫ���
    $comment = <IN>; # ������
    chomp($comment);
    $password = <IN>; # �Ź沽�ѥ����
    chomp($password);
    $food = int(<IN>);     # ����
    $pop = int(<IN>);      # �͸�
    $area = int(<IN>);     # ����
    $farm = int(<IN>);     # ����
    $factory = int(<IN>);  # ����
    $teamid = int(<IN>);   # ������ID
    $fire = int(<IN>);     # �ߥ�����ȯ�Ͳ�ǽ��
    $ownername = <IN>;     # �����ʡ��͡���
    chomp($ownername);

    # HidToName�ơ��֥����¸
    $HidToName{$id} = $name;	# 

    # �Ϸ�
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

	# ���ޥ��
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

	# ������Ǽ���
	for($i = 0; $i < $HlbbsMax; $i++) {
	    $line = <IIN>;
	    chomp($line);
	    $lbbs[$i] = $line;
	}

	close(IIN);
    }

    # �緿�ˤ����֤�
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

# ����ǡ����񤭹���
sub writeIslandsFile {
    my($num) = @_;

    # �ե�����򳫤�
    open(OUT, ">${HdirName}/hakojima.tmp");

    # �ƥѥ�᡼���񤭹���
    print OUT "$HislandTurn\n";
    print OUT "$HislandLastTime\n";
    print OUT "$HislandNumber\n";
    print OUT "$HislandNextID\n";
    print OUT "$HteamNumber\n";
    print OUT "$HturnCount\n";
    print OUT "$HnextCTurn\n";
    print OUT "$HfightMode\n";
    print OUT "$HfightCount\n";

    # ��ν񤭤���
    my($i);
    for($i = 0; $i < $HislandNumber; $i++) {
	 writeIsland($Hislands[$i], $num);
    }

    # �ե�������Ĥ���
    close(OUT);

    # �����̾���ˤ���
    unlink("${HdirName}/hakojima.dat");
    rename("${HdirName}/hakojima.tmp", "${HdirName}/hakojima.dat");
}

# ��ҤȤĽ񤭹���
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

    # �Ϸ�
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

	# ���ޥ��
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

	# ������Ǽ���
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
# ������ǡ���������
#----------------------------------------------------------------------

# ����ǡ����ɤߤ���
sub readTeamsFile {

    # �ǡ����ե�����򳫤�
    if(!open(IN, "${HdirName}/teams.dat")) {
	rename("${HdirName}/teams.tmp", "${HdirName}/teams.dat");
	if(!open(IN, "${HdirName}/teams.dat")) {
	    return 0;
	}
    }
    # ��������ɤߤ���
    my($i);
    for($i = 0; $i < $HteamNumber; $i++) {
	 $Hteams[$i] = readTeam();
	 $HidToTeamNumber{$Hteams[$i]->{'id'}} = $i;
    }

    # �ե�������Ĥ���
    close(IN);

    return 1;
}

# ������ҤȤ��ɤߤ���
sub readTeam {

    my($name, $id, $password, $money, $food, $pop, $farm, $factory, $fightid, $prize, $reward, $rewturn);
    $name = <IN>; # �������̾��
    chomp($name);
    $id = int(<IN>); # ID�ֹ�
    $member = <IN>; # �����������ID
    chomp($member);
    $password = <IN>; # �Ź沽�ѥ����
    chomp($password);
    $money = int(<IN>);    # ���
    $food = int(<IN>);     # ����
    $pop = int(<IN>);      # �͸�
    $farm = int(<IN>);     # ����
    $factory = int(<IN>);  # ����
    $fightid = int(<IN>);  # ���������ID
    $prize = int(<IN>);    # ��
    $reward = int(<IN>);   # �󽷶�
    $rewturn = int(<IN>);  # �󽷶��ѥ������

    # HidToName�ơ��֥����¸
    $HidToTeamName{$id} = $name;


    # �緿�ˤ����֤�
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

# ��������ǡ����񤭹���
sub writeTeamsFile {

    # �ե�����򳫤�
    open(OUT, ">${HdirName}/teams.tmp");

    # ��ν񤭤���
    my($i);
    for($i = 0; $i < $HteamNumber; $i++) {
	 writeTeam($Hteams[$i]);
    }

    # �ե�������Ĥ���
    close(OUT);

    # �����̾���ˤ���
    unlink("${HdirName}/teams.dat");
    rename("${HdirName}/teams.tmp", "${HdirName}/teams.dat");
}

# ������ǡ����ҤȤĽ񤭹���
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
# ������
#----------------------------------------------------------------------

# ɸ����Ϥؤν���
sub out {
    print STDOUT jcode::sjis($_[0]);
}


# ��Ʈ�ε�Ͽ��¸
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
	push(@offset,"<TR><TD $HbgCell><NOBR>��${HtagTName_}${name}${H_tagTName}</nobr></td>");
	push(@offset,"<TD $HbgCell align=center><NOBR><B>${pop}$HunitPop</b></nobr></td>");
	push(@offset,"<TD $HbgCell><NOBR>��${HtagTName2_}${tname}${H_tagTName2}</nobr></td>");
	push(@offset,"<TD $HbgCell align=center><NOBR><B>${tpop}$HunitPop</b></nobr></td>");
	push(@offset,"<TD $HbgCell align=right><NOBR><B>${money}����</b></nobr></td></TR>");
	push(@offset,"<TR><TD $HbgCell COLSPAN=2><NOBR>${HtagTH_}���С���${HtagName_}");
	my($island) = '';
	while($member =~ s/([0-9]*),//) {
	    if($1 eq '') { 
		push(@offset,"${H_tagName}</NOBR></TD><TD $HbgCell COLSPAN=2><NOBR>${HtagTH_}���С���${HtagName2_}");
		$island = '';
		next;
	    } elsif($island ne '') {
		push(@offset," : ");
	    }
	    $island = $Hislands[$HidToNumber{$1}];
	    push(@offset,"$island->{'name'}��");

	}
	push(@offset,"${H_tagName2}</NOBR></TD><TD $HbgCell>��</TD></TR>\n");
    }
}

# ͽ�����
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
	push(@offset,"<TR><TD $HbgCell><NOBR>��${HtagTName2_}${name}${H_tagTName2}</nobr></td>");
	push(@offset,"<TD $HbgCell align=center><NOBR><B>${pop}$HunitPop</b></nobr></td>");
	push(@offset,"<TR><TD $HbgCell COLSPAN=2><NOBR>${HtagTH_}���С���${H_tagTH}${HtagName2_}");
	my($island) = '';
	while($member =~ s/([0-9]*),//) {
	    if($island ne '') {
		push(@offset," : ");
	    }
	    $island = $Hislands[$HidToNumber{$1}];
	    push(@offset,"$island->{'name'}��");

	}
	push(@offset,"${H_tagName2}</NOBR></TD></TR>\n");
    }
}

# CGI���ɤߤ���
sub cgiInput {
    my($line, $getLine);

    # ���Ϥ������ä����ܸ쥳���ɤ�EUC��
    $line = <>;
    $line =~ tr/+/ /;
    $line =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
    $line = jcode::euc($line);
    $line =~ s/[\x00-\x1f\,]//g;

    # GET�Τ�Ĥ�������
    $getLine = $ENV{'QUERY_STRING'};

    # �оݤ���
    if($line =~ /CommandButton([0-9]+)=/) {
	# ���ޥ�������ܥ���ξ��
	$HcurrentID = $1;
	$defaultID = $1;
    }

    if($line =~ /ISLANDNAME=([^\&]*)\&/){
	# ̾������ξ��
	$HcurrentName = cutColumn($1, 32);
    }

    if($line =~ /ISLANDID=([0-9]+)\&/){
	# ����¾�ξ��
	$HcurrentID = $1;
	$defaultID = $1;
    }

    if($line =~ /TEAMID=([0-9]+)\&/){
	# ����¾�ξ��
	$HteamID = $1;
    }

    # �ѥ����
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

    # ��å�����
    if($line =~ /MESSAGE=([^\&]*)\&/) {
	$Hmessage = cutColumn($1, 80);
    }

    if($line =~ /JAVAMODE=(cgi|java)/) {
	$HjavaMode = $1;
    }

    if($line =~ /CommandJavaButton([0-9]+)=/) {
	# ���ޥ�������ܥ���ξ��ʣʣ���᥹����ץȡ�
	$HcurrentID = $1;
	$defaultID = $1;
    }

    # ������Ǽ���
    if($line =~ /LBBSNAME=([^\&]*)\&/) {
	$HlbbsName = $1;
	$HdefaultName = $1;
    }
    if($line =~ /LBBSMESSAGE=([^\&]*)\&/) {
	$HlbbsMessage = cutColumn($1, 80);
    }
    if($line =~ /OWNERNAME=([^\&]*)\&/){
	# �����ʡ�̾����ξ��
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
	# ������̾����ξ��
	$teamName = $1;
    }

    if($line =~ /DELISLAND=([0-9]+)\&/){
	# �����
	$deleteID = $1;
    }

    # main mode�μ���
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
        $HmainMode = 'delete';		# ����⡼��
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
	    # �Ѹ���
	    $HlbbsMode = 0;
	    $HforID = $HcurrentID;
	} elsif($1 eq 'OW') {
	    # ���
	    $HlbbsMode = 1;
	} else {
	    # ���
	    $HlbbsMode = 2;
	}
	$HcurrentID = $2;

	# ������⤷��ʤ��Τǡ��ֹ�����
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

	# ���ޥ�ɥ⡼�ɤξ�硢���ޥ�ɤμ���
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


#cookie����
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

#cookie����
sub cookieOutput {
    my($cookie, $info);

    # �ä�����¤�����
    my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) =
	gmtime(time + 30 * 86400); # ���� + 30��

    # 2������
    $year += 1900;
    if ($date < 10) { $date = "0$date"; }
    if ($hour < 10) { $hour = "0$hour"; }
    if ($min < 10) { $min  = "0$min"; }
    if ($sec < 10) { $sec  = "0$sec"; }

    # ������ʸ����
    $day = ("Sunday", "Monday", "Tuesday", "Wednesday",
	    "Thursday", "Friday", "Saturday")[$day];

    # ���ʸ����
    $mon = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
	    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")[$mon];

    # �ѥ��ȴ��¤Υ��å�
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
	# ��ư�ϰʳ�
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
# �桼�ƥ���ƥ�
#----------------------------------------------------------------------
sub hakolock {
    if($lockMode == 1) {
	# directory����å�
	return hakolock1();

    } elsif($lockMode == 2) {
	# flock����å�
	return hakolock2();
    } elsif($lockMode == 3) {
	# symlink����å�
	return hakolock3();
    } else {
	# �̾�ե����뼰��å�
	return hakolock4();
    }
}

sub hakolock1 {
    # ��å���
    if(mkdir('hakojimalock', $HdirMode)) {
	# ����
	return 1;
    } else {
	# ����
	my($b) = (stat('hakojimalock'))[9];
	if(($b > 0) && ((time() -  $b)> $unlockTime)) {
	    # �������
	    unlock();

	    # �إå�����
	    tempHeader();

	    # ���������å�����
	    tempUnlock();

	    # �եå�����
	    tempFooter();

	    # ��λ
	    exit(0);
	}
	return 0;
    }
}

sub hakolock2 {
    open(LOCKID, '>>hakojimalockflock');
    if(flock(LOCKID, 2)) {
	# ����
	return 1;
    } else {
	# ����
	return 0;
    }
}

sub hakolock3 {
    # ��å���
    if(symlink('hakojimalockdummy', 'hakojimalock')) {
	# ����
	return 1;
    } else {
	# ����
	my($b) = (lstat('hakojimalock'))[9];
	if(($b > 0) && ((time() -  $b)> $unlockTime)) {
	    # �������
	    unlock();

	    # �إå�����
	    tempHeader();

	    # ���������å�����
	    tempUnlock();

	    # �եå�����
	    tempFooter();

	    # ��λ
	    exit(0);
	}
	return 0;
    }
}

sub hakolock4 {
    # ��å���
    if(unlink('key-free')) {
	# ����
	open(OUT, '>key-locked');
	print OUT time;
	close(OUT);
	return 1;
    } else {
	# ��å����֥����å�
	if(!open(IN, 'key-locked')) {
	    return 0;
	}

	my($t);
	$t = <IN>;
	close(IN);
	if(($t != 0) && (($t + $unlockTime) < time)) {
	    # 120�ðʾ�вᤷ�Ƥ��顢����Ū�˥�å��򳰤�
	    unlock();

	    # �إå�����
	    tempHeader();

	    # ���������å�����
	    tempUnlock();

	    # �եå�����
	    tempFooter();

	    # ��λ
	    exit(0);
	}
	return 0;
    }
}

# ��å��򳰤�
sub unlock {
    if($lockMode == 1) {
	# directory����å�
	rmdir('hakojimalock');

    } elsif($lockMode == 2) {
	# flock����å�
	close(LOCKID);

    } elsif($lockMode == 3) {
	# symlink����å�
	unlink('hakojimalock');
    } else {
	# �̾�ե����뼰��å�
	my($i);
	$i = rename('key-locked', 'key-free');
    }
}

# �����������֤�
sub min {
    return ($_[0] < $_[1]) ? $_[0] : $_[1];
}

# �ѥ���ɥ��󥳡���
sub encode {
    if($cryptOn == 1) {
	return crypt($_[0], 'h2');
    } else {
	return $_[0];
    }
}

# �ѥ���ɥ����å�
sub checkPassword {
    my($p1, $p2) = @_;

    # null�����å�
    if($p2 eq '') {
	return 0;
    }

    # �ޥ������ѥ���ɥ����å�
    if($masterPassword eq $p2) {
	return 1;
    }

    # ����Υ����å�
    if($p1 eq encode($p2)) {
	return 1;
    }

    return 0;
}

# 1000��ñ�̴ݤ�롼����
sub aboutMoney {
    my($m) = @_;
    if($m < 500) {
	return "����500${HunitMoney}̤��";
    } else {
	$m = int(($m + 500) / 1000);
	return "����${m}000${HunitMoney}";
    }
}

# ����������ʸ���ν���
sub htmlEscape {
    my($s) = @_;
    $s =~ s/&/&amp;/g;
    $s =~ s/</&lt;/g;
    $s =~ s/>/&gt;/g;
    $s =~ s/\"/&quot;/g; #"
    return $s;
}

# 80�������ڤ�·��
sub cutColumn {
    my($s, $c) = @_;
    if(length($s) <= $c) {
	return $s;
    } else {
	# ���80�����ˤʤ�ޤ��ڤ���
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

# ���̾�������ֹ������(ID����ʤ����ֹ�)
sub nameToNumber {
    my($name) = @_;

    # ���礫��õ��
    my($i);
    for($i = 0; $i < $HislandNumber; $i++) {
	if($Hislands[$i]->{'name'} eq $name) {
	    return $i;
	}
    }

    # ���Ĥ���ʤ��ä����
    return -1;
}

# �������̾�������ֹ������(ID����ʤ����ֹ�)
sub nameToTeamNumber {
    my($name) = @_;

    # ���礫��õ��
    my($i);
    for($i = 0; $i < $HteamNumber; $i++) {
	if($Hteams[$i]->{'name'} eq $name) {
	    return $i;
	}
    }

    # ���Ĥ���ʤ��ä����
    return -1;
}

# �и��Ϥ����٥�򻻽�
sub expToLevel {
    my($kind, $exp) = @_;
    my($i);
    if($kind == $HlandBase) {
	# �ߥ��������
	for($i = $maxBaseLevel; $i > 1; $i--) {
	    if($exp >= $baseLevelUp[$i - 2]) {
		return $i;
	    }
	}
	return 1;
    } else {
	# �������
	for($i = $maxSBaseLevel; $i > 1; $i--) {
	    if($exp >= $sBaseLevelUp[$i - 2]) {
		return $i;
	    }
	}
	return 1;
    }

}

# (0,0)����(size - 1, size - 1)�ޤǤο��������ŤĽФƤ���褦��
# (@Hrpx, @Hrpy)������
sub makeRandomPointArray {
    # �����
    my($y);
    @Hrpx = (0..$HislandSize-1) x $HislandSize;
    for($y = 0; $y < $HislandSize; $y++) {
	push(@Hrpy, ($y) x $HislandSize);
    }

    # ����åե�
    my ($i);
    for ($i = $HpointNumber; --$i; ) {
	my($j) = int(rand($i+1)); 
	if($i == $j) { next; }
	@Hrpx[$i,$j] = @Hrpx[$j,$i];
	@Hrpy[$i,$j] = @Hrpy[$j,$i];
    }
}

# 0����(n - 1)�����
sub random {
    return int(rand(1) * $_[0]);
}

#----------------------------------------------------------------------
# ��ɽ��
#----------------------------------------------------------------------
# �ե������ֹ����ǥ�ɽ��
sub logFilePrint {
    my($fileNumber, $id, $mode, $kankou) = @_;
    open(LIN, "${HdirName}/hakojima.log$_[0]");
    my($line, $m, $turn, $id1, $id2, $message);
    my($fi) = 0;

    while($line = <LIN>) {
	$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),(.*)$/;
	($m, $turn, $id1, $id2, $message) = ($1, $2, $3, $4, $5);

	# ��̩�ط�
	if($m == 1) {
	    if(($mode == 0) || ($id1 != $id)) {
		# ��̩ɽ�������ʤ�
		next;
	    }
	    $m = '<B>(��̩)</B>';
	} else {
	    $m = '';
	}

	# ɽ��Ū�Τ�
	if($id != 0) {
	    if(($id != $id1) &&
	       ($id != $id2)) {
		next;
	    }
	}

	# ɽ��
	if($kankou == 1) {

	out("<NOBR>${HtagNumber_}������$turn$m${H_tagNumber}��$message</NOBR><BR>\n");

    } elsif(($fi == 0) && ($mode == 0)) {
     out("<NOBR><BR><B><I><FONT COLOR='#000000' SIZE=+2>������$turn$m��</FONT></I></B><BR><HR width=50% align=left>\n");
	out("<NOBR>${HtagNumber_}������$turn$m${H_tagNumber}��$message</NOBR><BR>\n");
	  $fi++;
	} else {
	out("<NOBR>${HtagNumber_}������$turn$m${H_tagNumber}��$message</NOBR><BR>\n");
	}
    }
#	out("<hr>\n");
    close(LIN);
}
#----------------------------------------------------------------------
# �ƥ�ץ졼��
#----------------------------------------------------------------------
# �����
sub tempInitialize {
    # �祻�쥯��(�ǥե���ȼ�ʬ)
    $HislandList = getIslandList($defaultID);
}

# ��ǡ����Υץ�������˥塼��
sub getIslandList {
    my($select) = @_;
    my($list, $name, $id, $s, $i);

    #��ꥹ�ȤΥ�˥塼
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
	    "<OPTION VALUE=\"$id\" $s>${name}��\n";
    }
    return $list;
}

# ��ǡ����Υץ�������˥塼��
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

    #��ꥹ�ȤΥ�˥塼
    while($tNumMember =~ s/([0-9]*),//) {
	$island = $Hislands[$HidToNumber{$1}];
	if($island->{'id'} eq $defaultTarget) {
	    $s = 'SELECTED';
	} else {
	    $s = '';
	}
	$list .= "<OPTION VALUE=\"$island->{'id'}\" $s>$island->{'name'}��\n";
    }
    my($numMember) = $team->{'member'};
    while($numMember =~ s/([0-9]*),//) {
	$island = $Hislands[$HidToNumber{$1}];
	if($island->{'id'} eq $defaultTarget) {
	    $s = 'SELECTED';
	} else {
	    $s = '';
	}
	$list .= "<OPTION VALUE=\"$island->{'id'}\" $s>$island->{'name'}��\n";
    }
    return $list;
}

# �إå�
sub tempHeader {
	out("Content-type: text/html\n\n");
	my($HimgFlag) = 0;
	if($HimgLine eq '' || $HimgLine eq $imageDir){
	    $baseIMG = $imageDir;
	    $HimgFlag = 1;
	} else {
	    $baseIMG = $HimgLine;
	}
	$baseIMG =~ s/�޽�į��/�ǥ����ȥå�/g;
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
<A HREF="http://t.pos.to/hako/" target=_blank>Ȣ����祹����ץ����۸�</A> / 
<A HREF="http://appoh.execweb.cx/hakoniwa/" target="_blank">Ȣ��Java������ץ��� ���۸�</A>
<A HREF="http://espion.just-size.jp/archives/dist_hako/" target=_blank>Ȣ�������ȡ��ʥ��� ���۸� </A>
<BR>
<IMG SRC="$cleangif" width=0 height=3><BR>
����<A HREF="$toppage">�ȥåץڡ���</A> / 
<A HREF="$bbs">$bbsname</A> / 
<A HREF="$HthisFile?LogFileView=1" target=_blank>�Ƕ�ν����</A> / 
<A HREF="$HthisFile?LogFileTeam=0" target=_blank>�����[��������]</A> / 
<A HREF="$HthisFile?HELP">����إ��</A></nobr>
<DIV ALIGN=RIGHT>
</DIV>
<HR>
END
if($HimgFlag) {
    out(<<END);
<FONT COLOR=RED><B>�����С���ٷڸ��ΰ٤ˡ������Υ����������ԤäƲ�����褦�ˤ��ꤤ�פ��ޤ���</B></FONT><HR>
END
}
}

# �եå�
sub tempFooter {
    out(<<END);
<HR>
<P align=right>
<NOBR>
<A HREF="http://t.pos.to/hako/" target=_blank>Ȣ����祹����ץ����۸�</A> / 
<A HREF="http://appoh.execweb.cx/hakoniwa/" target="_blank">Ȣ��Java������ץ��� ���۸�</A>
<BR>
<IMG SRC="$cleangif" width=600 height=3><BR>
<A HREF="$toppage">�ȥåץڡ���</A> / 
<A HREF="$bbs">$bbsname</A> / 
<A HREF="$HthisFile?LogFileView=1" target=_blank>�Ƕ�ν����</A> / 
<A HREF="$HthisFile?LogFileTeam=0" target=_blank>�����[��������]</A> / 
<A HREF="$HthisFile?HELP">����إ��</A>
</nobr><BR><BR>
������:$adminName(<A HREF="mailto:$email">$email</A>)<BR>
</P>
</BODY>
</HTML>
END
}

# ��å�����
sub tempLockFail {
    # �����ȥ�
    out(<<END);
${HtagBig_}Ʊ�������������顼�Ǥ���<BR>
�֥饦���Ρ����ץܥ���򲡤���<BR>
���Ф餯�ԤäƤ�����٤����������${H_tagBig}$HtempBack
END
}

# �������
sub tempUnlock {
    # �����ȥ�
    out(<<END);
${HtagBig_}����Υ����������۾ｪλ���ä��褦�Ǥ���<BR>
��å�����������ޤ�����${H_tagBig}$HtempBack
END
}

# hakojima.dat���ʤ�
sub tempNoDataFile {
    out(<<END);
${HtagBig_}�ǡ����ե����뤬�����ޤ���${H_tagBig}$HtempBack
END
}

# �ѥ���ɴְ㤤
sub tempWrongPassword {
    out(<<END);
${HtagBig_}�ѥ���ɤ��㤤�ޤ���${H_tagBig}$HtempBack
END
}

# ���С���������¿��
sub tempOverMember {
    out(<<END);
${HtagBig_}���Υ�����ˤϤ���ʾ�����ޤ���${H_tagBig}$HtempBack
END
}

# ��������ȯ��
sub tempProblem {
    out(<<END);
${HtagBig_}����ȯ�����Ȥꤢ������äƤ���������${H_tagBig}$HtempBack
END
}
