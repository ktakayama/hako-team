#!/usr/local/bin/perl
# ���ϥ����С��˹�碌���ѹ����Ʋ�������

#----------------------------------------------------------------------
# Ȣ������ ver2.30
# ���ƥʥ󥹥ġ���(ver1.01)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# Ȣ������Υڡ���: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# Ȣ��������ȡ��ʥ���
# ���ƥʥ󥹥ġ���
# $Id: hako-mente.cgi,v 1.1 2003/07/02 03:09:49 gaba Exp $

require './hako-ini.cgi';

# ������������������������������������������������������������
# �Ƽ�������
# ������������������������������������������������������������


# ���Υե�����
my($thisFile) = './hako-mente.cgi';


# use Time::Local���Ȥ��ʤ��Ķ��Ǥϡ�'use Time::Local'�ιԤ�ä��Ʋ�������
# ���������������֤��ѹ���'�û�����ѹ�'�����Ǥ��ʤ��ʤ�ޤ���
use Time::Local;

# ������������������������������������������������������������
# ������ܤϰʾ�
# ������������������������������������������������������������

# �Ƽ��ѿ�
my($mainMode);
my($inputPass);
my($deleteID);
my($currentID);
my($ctYear);
my($ctMon);
my($ctDate);
my($ctHour);
my($ctMin);
my($ctSec);

print <<END;
Content-type: text/html

<HTML>
<HEAD>
<TITLE>Ȣ�磲 ���ƥʥ󥹥ġ���</TITLE>
</HEAD>
<BODY>
END

cgiInput();

if($mainMode eq 'delete') {
    if(passCheck()) {
	deleteMode();
    }
} elsif($mainMode eq 'current') {
    if(passCheck()) {
	currentMode();
    }
} elsif($mainMode eq 'time') {
    if(passCheck()) {
	timeMode();
    }
} elsif($mainMode eq 'stime') {
    if(passCheck()) {
	stimeMode();
    }
} elsif($mainMode eq 'new') {
    if(passCheck()) {
	newMode();
    }
}
mainMode();

print <<END;
</FORM>
</BODY>
</HTML>
END

sub myrmtree {
    my($dn) = @_;
    opendir(DIN, "$dn/");
    my($fileName);
    while($fileName = readdir(DIN)) {
	unlink("$dn/$fileName");
    } 
    closedir(DIN);
    rmdir($dn);
}

sub currentMode {
    myrmtree "${HdirName}";
    mkdir("${HdirName}", $HdirMode);
    opendir(DIN, "${HdirName}.bak$currentID/");
    my($fileName);
    while($fileName = readdir(DIN)) {
	fileCopy("${HdirName}.bak$currentID/$fileName", "${HdirName}/$fileName");
    }
    closedir(DIN);
    open(FIN, "${HdirName}/teams.dat");
	while($name = <FIN>) {
	    chomp($name);
	    $id = int(<FIN>);
	    $dummy = <FIN>;
	    $password = <FIN>;
	    chomp($password);
	    $dummy = <FIN>;
	    $dummy = <FIN>;
	    $dummy = <FIN>;
	    $dummy = <FIN>;
	    $dummy = <FIN>;
	    $dummy = <FIN>;
	    $dummy = <FIN>;
	    $dummy = <FIN>;
	    $dummy = <FIN>; # �󽷶��ѥ������
	    $fightcgi .= "${id}\n${name}\n${password}\n";
#	    chop(@fightcgi);
	}
    close(FIN);

    open(DAT, ">>team.tmp.cgi");
	print DAT "$fightcgi";
    close(DAT);

    rename ("team.tmp.cgi", "team.cgi");

}

sub deleteMode {
    if($deleteID eq '') {
	myrmtree "${HdirName}";
    } else {
	myrmtree "${HdirName}.bak$deleteID";
    }
    unlink "hakojimalockflock";
}

sub newMode {
    mkdir($HdirName, $HdirMode);

    # ���ߤλ��֤����
    my($now) = time;
    $now = $now - ($now % ($HunitTime));
    $now += $HunitTime;
    open(OUT, ">$HdirName/hakojima.dat"); # �ե�����򳫤�
    print OUT "0\n";         # �������1
    print OUT "$now\n";      # ���ϻ���
    print OUT "0\n";         # ��ο�
    print OUT "1\n";         # ���˳�����Ƥ�ID
    print OUT "$teamNum\n";  # �������
    print OUT "$HdevRepTurn\n";# ������
    print OUT "0\n";         # �ڤ��ؤ�������
    print OUT "0\n";         # ���ߤ���Ʈ�⡼��
    print OUT "1\n";         # �������ܤ�

    # �ե�������Ĥ���
    close(OUT);
    open(DOUT, ">$HdirName/teams.dat"); # �ե�����򳫤�
    my($passkey) = rand(1200) + 1;
    for($i= 1 ;$i <= $teamNum;$i++) {
	print DOUT "������${i}:̾��̤����\n";
	print DOUT "$i\n";
	print DOUT "\n";
	$tpass[$i] = crypt($i * $passkey,hp);
	print DOUT "$tpass[$i]\n";
	for($f= 4 ;$f < $teamFileNum;$f++) {
	    print DOUT "\n";
	}
    }

    # �ե�������Ĥ���
    close(DOUT);

    open(TOUT, ">team.cgi");
	for($i= 1 ;$i <= $teamNum;$i++) {
	    print TOUT "$i\n";
	    print TOUT "������${i}:̾��̤����\n";
	    print TOUT "$tpass[$i]\n";
	}
    close(TOUT);

    for ($f = 1;$f <= $teamNum;$f++) {
	open(BOUT, ">${teambbs}/${f}.cgi");
	    print BOUT "0\n";
	close(BOUT);
	open(BOUT, ">${teambbs}/chat/${f}.cgi");
	close(BOUT);

    }
}

sub timeMode {
    $ctMon--;
    $ctYear -= 1900;
    $ctSec = timelocal($ctSec, $ctMin, $ctHour, $ctDate, $ctMon, $ctYear);
    stimeMode();
}

sub stimeMode {
    my($t) = $ctSec;
    open(IN, "${HdirName}/hakojima.dat");
    my(@lines);
    @lines = <IN>;
    close(IN);

    $lines[1] = "$t\n";

    open(OUT, ">${HdirName}/hakojima.dat");
    print OUT @lines;
    close(OUT);
}

sub mainMode {
    opendir(DIN, "./");

    print <<END;
<FORM action="$thisFile" method="POST">
<H1>Ȣ�磲 ���ƥʥ󥹥ġ���ʥ�����ȡ��ʥ��ȡ�</H1>
<B>�ѥ����:</B><INPUT TYPE=password SIZE=32 MAXLENGTH=32 NAME=PASSWORD></TD>
END

    # ����ǡ���
    if(-d "${HdirName}") {
	dataPrint("");
    } else {
	print <<END;
    <HR>
    <INPUT TYPE="submit" VALUE="�������ǡ�������" NAME="NEW">
END
    }

    # �Хå����åץǡ���
    my($dn);
    while($dn = readdir(DIN)) {
	if($dn =~ /^${HdirName}.bak(.*)/) {
	    dataPrint($1);
	}
    } 
    closedir(DIN);
}

# ɽ���⡼��
sub dataPrint {
    my($suf) = @_;

    print "<HR>";
    if($suf eq "") {
	open(IN, "${HdirName}/hakojima.dat");
	print "<H1>����ǡ���</H1>";
    } else {
	open(IN, "${HdirName}.bak$suf/hakojima.dat");
	print "<H1>�Хå����å�$suf</H1>";
    }

    my($lastTurn);
    $lastTurn = <IN>;
    my($lastTime);
    $lastTime = <IN>;

    my($timeString) = timeToString($lastTime);

    print <<END;
    <B>������$lastTurn</B><BR>
    <B>�ǽ���������</B>:$timeString<BR>
    <B>�ǽ���������(�ÿ�ɽ��)</B>:1970ǯ1��1������$lastTime ��<BR>
    <INPUT TYPE="submit" VALUE="���Υǡ�������" NAME="DELETE$suf">
END

    if($suf eq "") {
	my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) =
	    localtime($lastTime);
	$mon++;
	$year += 1900;

	print <<END;
    <H2>�ǽ��������֤��ѹ�</H2>
    <INPUT TYPE="text" SIZE=4 NAME="YEAR" VALUE="$year">ǯ
    <INPUT TYPE="text" SIZE=2 NAME="MON" VALUE="$mon">��
    <INPUT TYPE="text" SIZE=2 NAME="DATE" VALUE="$date">��
    <INPUT TYPE="text" SIZE=2 NAME="HOUR" VALUE="$hour">��
    <INPUT TYPE="text" SIZE=2 NAME="MIN" VALUE="$min">ʬ
    <INPUT TYPE="text" SIZE=2 NAME="NSEC" VALUE="$sec">��
    <INPUT TYPE="submit" VALUE="�ѹ�" NAME="NTIME"><BR>
    1970ǯ1��1������<INPUT TYPE="text" SIZE=32 NAME="SSEC" VALUE="$lastTime">��
    <INPUT TYPE="submit" VALUE="�û�����ѹ�" NAME="STIME">

END
    } else {
	print <<END;
	<INPUT TYPE="submit" VALUE="���Υǡ��������" NAME="CURRENT$suf">
END
    }
}

sub timeToString {
    my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) =
	localtime($_[0]);
    $mon++;
    $year += 1900;

    return "${year}ǯ ${mon}�� ${date}�� ${hour}�� ${min}ʬ ${sec}��";
}

# CGI���ɤߤ���
sub cgiInput {
    my($line);

    # ���Ϥ�������
    $line = <>;
    $line =~ tr/+/ /;
    $line =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

    if($line =~ /DELETE([0-9]*)/) {
	$mainMode = 'delete';
	$deleteID = $1;
    } elsif($line =~ /CURRENT([0-9]*)/) {
	$mainMode = 'current';
	$currentID = $1;
    } elsif($line =~ /NEW/) {
	$mainMode = 'new';
    } elsif($line =~ /NTIME/) {
	$mainMode = 'time';
	if($line =~ /YEAR=([0-9]*)/) {
	    $ctYear = $1; 
	}
	if($line =~ /MON=([0-9]*)/) {
	    $ctMon = $1; 
	}
	if($line =~ /DATE=([0-9]*)/) {
	    $ctDate = $1; 
	}
	if($line =~ /HOUR=([0-9]*)/) {
	    $ctHour = $1; 
	}
	if($line =~ /MIN=([0-9]*)/) {
	    $ctMin = $1; 
	}
	if($line =~ /NSEC=([0-9]*)/) {
	    $ctSec = $1; 
	}
    } elsif($line =~ /STIME/) {
	$mainMode = 'stime';
	if($line =~ /SSEC=([0-9]*)/) {
	    $ctSec = $1; 
	}
    }

    if($line =~ /PASSWORD=([^\&]*)\&/) {
	$inputPass = $1;
    }
}

# �ե�����Υ��ԡ�
sub fileCopy {
    my($src, $dist) = @_;
    open(IN, $src);
    open(OUT, ">$dist");
    while(<IN>) {
	print OUT;
    }
    close(IN);
    close(OUT);
}

# �ѥ������å�
sub passCheck {
    if($inputPass eq $masterPassword) {
	return 1;
    } else {
	print <<END;
   <FONT SIZE=7>�ѥ���ɤ��㤤�ޤ���</FONT>
END
        return 0;
    }
}

1;