#!/usr/local/bin/perl

## PONNY CHAT v3.4 (2000/12/13)
## Copyright(C) Kent Web 2000
## webmaster@kent-web.com
## http://www.kent-web.com/

$ver = 'PONNY v3.4'; # �o�[�W�������

#--- [���ӎ���] ------------------------------------------------#
# 1. ���̃X�N���v�g�̓t���[�\�t�g�ł��B���̃X�N���v�g���g�p����	#
#    �����Ȃ鑹�Q�ɑ΂��č�҂͈�؂̐ӔC�𕉂��܂���B		#
# 2. �ݒu�Ɋւ��鎿��̓T�|�[�g�f���ɂ��肢�������܂��B	#
#    ���ڃ��[���ɂ�鎿��͈�؂��󂯂������Ă���܂���B	#
#---------------------------------------------------------------#

#============#
#  �ݒ荀��  #
#============#

# jcode.pl
require '../../jcode.pl';

# �^�C�g�������̐F
$t_color = "#008040";

# �^�C�g���̑傫��
$t_size = '16pt';

# �{���̕����傫��
$b_size = '10pt';

# body�^�O
$body = '<body bgcolor="#F1F1F1" text="#000000">';

# �߂���URL (index.html�Ȃ�)
$homepage = '../../../hako/';

# �헪��(�f����)
$bbs = '../bbs.cgi';

# �ő�L����
$max = 25;

# �����F���w��(�㉺�̔z��͕K���y�A��)
@COLORS = ('0000FF','DF0000','008040','800000','C100C1','FF80C0','FF8040','000080');
@IROIRO = ('��','��','�݂ǂ�','��','��','�s���N','�I�����W','�����F');

# �����[�h����
@retime = (0,30,40,50,60);

# �����[�h���ԁi�����l�j
$retime = 40;

# �R�����g�Ԃ̎d��(<br>=���s <P>=�i�� <hr>=�r��)
$sikiri = '<hr>';

# ���ގ������b�Z�[�W
$in_msg  = "����A��������Ⴂ�B";	# ������
$out_msg = "����A���悤�Ȃ�`�B";	# �ގ���

# ���ގ��ē����b�Z�[�W�̐F
$rep_color = "#808080";

# method�̌`��(POST/GET)
$method = 'POST';

# �X�N���v�g�t�@�C����
$script  = './chat.cgi';

# ���b�N�t�@�C��
$lockfile = './ponny.lock';

#============#
#  �ݒ芮��  #
#============#

&decode;
&logpass;
if ($in{'mode'} eq "form") { &form1; }
elsif ($in{'mode'} eq "into") { &form2; }
elsif ($in{'comment'} && $in{'mode'} eq "regist") { &regist; }
elsif ($in{'mode'} eq "byebye") { &byebye; }
elsif ($in{'mode'} eq "top") { &top_view; }
&log_view;


#----------------------#
#  �t�H�[��1 : ������  #
#----------------------#
sub form1 {
	&header('body');
	print <<"EOM";
<center>
<form method="$method" action="$script" target="form" name="ponny">
<input type=hidden name=teamID value="$in{'teamID'}">
<input type=hidden name=tPASS value="$in{'tPASS'}">
<input type=hidden name=mode value="into">
<table border=2 cellspacing=0>
<tr><th colspan=2><font color="$t_color" size=5><b style="font-size:$t_size">$title</b></font></th></tr>
<tr><td><b>���Ȃ܂�</b> <input type=text name=name size=20></td></tr>
<tr><td>�����[�h <select name=retime>
EOM
	$in{'retime'} = $retime;
	foreach (@retime) {
		if ($in{'retime'} == $_) { print "<option value=$_ selected>$_�b\n"; }
		else { print "<option value=$_>$_�b\n"; }
	}
	print "</select> �����F <select name=color>\n";
	foreach (0 .. $#COLORS) {
		print "<option value=\"$COLORS[$_]\">$IROIRO[$_]\n";
	}

	print <<"EOM";
</select></td></tr></table>
<table cellpadding=0 cellspacing=0><tr>
<th><input type=submit value="��������"></th></form>
<th><form action="$homepage" target="_top"><input type=submit value="���ǂ�"></th>
</form></tr></table>
<SCRIPT LANGUAGE="JavaScript">
<!--
self.document.ponny.name.focus();
//-->
</SCRIPT>
</body></html>
EOM
	exit;
}

#----------------------#
#  �t�H�[��2 : ������  #
#----------------------#
sub form2 {
	&regist('into');

	# MSIE�̓t�H�[�����𒲐�
   	if ($ENV{'HTTP_USER_AGENT'} =~ /MSIE/i) { $text_width = 90; }
	else { $text_width = 50; }

	# �ȉ���JavaScript(�������������@�\)�́u�䂢������Ɓv����ڐA���܂���
	# http://www.cup.com/yui/
	&header;
	print <<"EOM";
<SCRIPT LANGUAGE="JavaScript">
<!--
function autoclear() {
 if (self.document.send) {
  if (self.document.cmode && self.document.cmode.autoclear) {
   if (self.document.cmode.autoclear.checked) {
    if (self.document.send.comment) {
      self.document.send.comment.value = "";
      self.document.send.comment.focus();
    }
   }
  }
 }
}
// -->
</SCRIPT>
</head>
$body
<form name=send method=$method action="$script" target="log" onSubmit="setTimeout(&quot;autoclear()&quot;,10)">
<input type=hidden name=mode value="regist">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=teamID value="$in{'teamID'}">
<input type=hidden name=tPASS value="$in{'tPASS'}">
<input type=hidden name=name value="$in{'name'}">
<b>����</b>�F<input type=text size="$text_width" name=comment><br>
�����[�h <select name=retime>
EOM
	foreach (@retime) {
		if ($in{'retime'} == $_) { print "<option value=$_ selected>$_�b\n"; }
		else { print "<option value=$_>$_�b\n"; }
	}
	print "</select> �����F <select name=color>\n";
	foreach (0 .. $#COLORS) {
		if ($in{'color'} eq "$COLORS[$_]") {
			print "<option value=$COLORS[$_] selected>$IROIRO[$_]\n";
		} else {
			print "<option value=$COLORS[$_]>$IROIRO[$_]\n";
		}
	}

	print <<"EOM";
</select>
<input type=submit value="�����^�����[�h"><input type=reset value="�N���A"></form>
<form action="$script" method="$method" target=form>
<table><tr>
<td>
  <input type=submit value="�ގ�����">
  <input type=hidden name=teamID value="$in{'teamID'}">
  <input type=hidden name=tPASS value="$in{'tPASS'}">
  <input type=hidden name=mode value="byebye">
  <input type=hidden name=name value="$in{'name'}">
</td></form>
<td valign=top>
  <form name="cmode">
  <input type="checkbox" name="autoclear" checked>������������
</td></form></tr></table>
</body></html>
EOM
	exit;
}

#------------#
#  �L���\��  #
#------------#
sub log_view {
	if ($in{'retime'} eq "") { $in{'retime'} = $retime; }
	&header;
	if ($in{'retime'} != 0) {
		print "<META HTTP-EQUIV=\"refresh\" CONTENT=\"$in{'retime'}; URL=$script?retime=$in{'retime'}&teamID=$in{'teamID'}&tPASS=$in{'tPASS'}\">\n";
	}
	print "</head>\n$body\n";
	print "<TABLE WIDTH=100%><TR><TD><A HREF=$bbs?teamID=$in{'teamID'}&tPASS=$in{'tPASS'} target=_top>�헪��</A>\n";
	print "</TD><TD align=right>�����[�h�ݒ�F";
	if ($in{'retime'} == 0) { print "�蓮"; } else { print "$in{'retime'}�b"; }
	print "</TD></TR></TABLE><hr>\n";

	open(IN,"$logfile") || &error("Open Error : $logfile");
	while (<IN>) {
		($date,$name,$com,$color) = split(/<>/);
		print "<font color=\"$color\"><b>$name</b> �� $com</font> ($date)$sikiri\n";
	}
	close(IN);

	# ���쌠��\���i�폜�s�j
	print "<center><small><!-- $ver -->\n";
	print "- <a href='http://www.kent-web.com/' target='_top'>Ponny Chat</a> -\n";
    print "<BR>Edit:<a href=\"http://espion.s7.xrea.com/\" target='_top'>Web note</a> -\n";
	print "</small></center>\n</body></html>\n";
	exit;
}

#----------------#
#  ���O��������  #
#----------------#
sub regist {
	# �����̎擾
	($sec,$min,$hour,$mday,$mon) = localtime(time);
	$date = sprintf("%02d/%02d-%02d:%02d:%02d",$mon+1,$mday,$hour,$min,$sec);

	# ���O�`�Ԃ𔻒f
	if ($_[0] eq 'into') {
		$in{'comment'} = "<b>$in{'name'}</b>$in_msg";
		$name  = "MASTER";
		$color = $rep_color;
	} elsif ($_[0] eq 'bye') {
		$in{'comment'} = "<b>$in{'name'}</b>$out_msg";
		$name  = "MASTER";
		$color = $rep_color;
	} else {
		$name  = $in{'name'};
		$color = $in{'color'};
	}

	# ���b�N�J�n
	&lock;

	open(IN,"$logfile") || &error("Open Error : $logfile");
	@lines = <IN>;
	close(IN);

	# �X�V����
	while ($max <= @lines) { pop(@lines); }
	unshift (@lines,"$date<>$name<>$in{'comment'}<>$color<>$ENV{'REMOTE_ADDR'}\n");
	open(OUT,">$logfile") || &error("Write Error : $logfile");
	print OUT @lines;
	close(OUT);

	# ���b�N����
	unlink($lockfile) if (-e $lockfile);

}

#----------------#
#  �f�R�[�h����  #
#----------------#
sub decode {
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	} else { $buffer = $ENV{'QUERY_STRING'}; }
	@pairs = split(/&/, $buffer);
	foreach (@pairs) {
		($name,$value) = split(/=/);
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

		# �����R�[�h���V�t�gJIS�ϊ�
		&jcode'convert(*value,'sjis');

		# ���s�͍폜
		$value =~ s/\r//g;
		$value =~ s/\n//g;

		$value =~ s/</&lt;/g; $value =~ s/>/&gt;/g;

		$in{$name} = $value;
	}
	if ($in{'name'} eq "") { $in{'name'} = "�������̃S���x�G"; }
}

#------------#
#  �ގ�����  #
#------------#
sub byebye {
	&regist('bye');
	&header('body');
	print <<"EOM";
<center><h3>$in{'name'}����A�����p���肪�Ƃ��������܂���</h3>
[<a href="$bbs?teamID=$in{'teamID'}&tPASS=$in{'tPASS'}" target="_top">�헪���ւ��ǂ�</a>]�@�@
[<a href="$homepage" target="_top">�g�b�v�ւ��ǂ�</a>]

</center>
</body></html>
EOM
	exit;
}

#--------------#
#  �G���[����  #
#--------------#
sub error {
	unlink($lockfile) if (-e $lockfile);

	&header('body') if (!$head_flag);
	print "<center><hr width='70%'><h3>ERROR !</h3>\n";
	print "<font color=red><B>$_[0]</B></font>\n";
	print "<P><hr width='70%'></center>\n</body></html>\n";
	exit;
}

#--------------#
#  HTML�w�b�_  #
#--------------#
sub header {
	$head_flag = 1;
	print "Content-type: text/html\n\n";
	print <<"EOM";
<html><head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<STYLE TYPE="text/css">
<!-- body,tr,td,th { font-size:$b_size } -->
</STYLE>
<title>$title</title>
EOM
	if ($_[0] eq "body") { print "</head>\n$body\n"; }
}

#----------------------#
#  ���b�N�t�@�C������  #
#----------------------#
sub lock {
	local($flag)=0;
	foreach (1 .. 5) {
		if (-e $lockfile) { sleep(1); }
		else {
			open(LOCK,">$lockfile") || &error("Lock Error");
			close(LOCK);
			$flag=1; last;
		}
	}
	if (!$flag) { &error("LOCK is BUSY"); }
}

#--------------#
#  �g�b�v�\��  #
#--------------#
sub top_view {
print "Content-type:text/html\n\n";
print <<_HTML_;

<html>
<head><title>${title}</title>
</head>
<frameset rows="135,*">
<frame name="form" src="./${script}?mode=form&teamID=$in{'teamID'}&tPASS=$in{'tPASS'}" target="_self">
<frame name="log" src="./${script}?teamID=$in{'teamID'}&tPASS=$in{'tPASS'}">
<noframes>
<body>
<h3>�t���[����Ή��̃u���E�U�̕��͂����p�ł��܂���</h3>
</body></noframes>
</frameset>
</html>


_HTML_

exit;

}

#----------------#
#  ���O�t�@�C��  #
#----------------#
sub logpass {
	my($i) = 0;

	# ���O��ǂݍ���
	open(IN,"../../team.cgi") || &error("Can't open LogFile");

    while($l = <IN>) {
		$i = int($l);
		$tname = <IN>;
		chomp($tname);
		$tpass = <IN>;
		chomp($tpass);
		if($in{'teamID'} == $i && $in{'tPASS'} eq $tpass){
		    $logfile = $i . ".cgi";
			$lockfile = $i . ".lock";

		    $title = jcode::sjis($tname) . '�헪��c��';
			last;
		}
    }
	close(IN);
	if(!$logfile) {
		&error2();
	}
}

#---------------#
#  �G���[����2  #
#---------------#
sub error2 {
	unlink($lockfile) if (-e $lockfile);

	&header('body') if (!$head_flag);
	print<<_HTML_;

<center><hr width='70%'><h3>ERROR !</h3>
<font color=red><B>
�^�[���X�V������\�\\��������܂��̂ŁA<BR>
���萔�ł����J����ʂ�����Ȃ����ĉ������B<BR>
</B>
</font>
<P><hr width='70%'>
</center>
</body>
</html>

_HTML_

	exit;
}

