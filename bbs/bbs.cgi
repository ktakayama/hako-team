#!/usr/local/bin/perl

## Petit Board v4.5 (00/04/02) 
## Copyright(C) KENT-WEB 1997-2000
## webmaster@kent-web.com
## http://www.kent-web.com/

$ver = 'PETIT v4.5'; # �o�[�W�������

## ---[���ӎ���]------------------------------------------------------
## 1. ���̃X�N���v�g�̓t���[�\�t�g�ł��B���̃X�N���v�g���g�p����
##    �����Ȃ鑹�Q�ɑ΂��č�҂͈�؂̐ӔC�𕉂��܂���B
## 2. �ݒu�Ɋւ��鎿��̓T�|�[�g�f���ɂ��肢�������܂��B���ڃ��[��
##    �ɂ�鎿��͌ł����f�肢�����܂��B
## 3. �����́u�ƃA�C�R�� (home.gif) �v�́A�u�������ƃA�C�R���̕��� 
##    (http://www.ushikai.com/)�v�ɂ����̂ŁA��҂̍��ӂ̌��ɍĔz�z
##    ������̂ł��B
## -------------------------------------------------------------------

#============#
#  �ݒ荀��  #
#============#

# jcode.pl������f�B���N�g���ɂ���ꍇ
require '../jcode.pl';

# �^�C�g����
$title = "�헪��";

# �^�C�g�������̐F
$t_color = "#DD0000";

# �^�C�g�������̑傫��(font size)
$t_size  = 6;

# �^�C�g�������̃t�H���g�^�C�v
$t_face  = "�l�r �o�S�V�b�N";

# �ǎ����d�l����ꍇ�ihttp://����w��j
$backgif = "";

# �w�i�F���w��
$bgcolor = "#E1F0F0";

# �����F���w��
$text = "#000000";

# �����N�F���w��
$link  = "#0000FF";	# ���K��
$vlink = "#800080";	# �K���
$alink = "#FF0000";	# �K�⒆


# �߂���URL (index.html�Ȃ�)
$homepage = "../../../hako";

# �����URL
$hakopage = "../hako-main.cgi";

# �e�L���ő�L���� (���܂葽������Ɗ댯)
#  --> ���X�L���̐��͍ő�L�����ɂ͊܂܂�܂���
$max = 50;

# �Ǘ��җp�}�X�^�p�X���[�h(�p����)
$pass = 'password';

# �A�C�R���摜�̂���u�f�B���N�g���v
#  --> petit.cgi �ƕʃf�B���N�g���ƂȂ�ꍇ�́Ahttp://����L�q����B
$icon_dir = ".";

# �ԐM�����Ɛe�L�����g�b�v�ֈړ� (0=no 1=yes)
$res_sort = 0;

# �z�X�g���擾���[�h
#  --> 0 : $ENV{'REMOTE_HOST'} �Ŏ擾�ł���ꍇ
#  --> 1 : gethostbyaddr �Ŏ擾�ł���ꍇ
$get_remotehost = 0;

# �^�C�g����GIF�摜���g�p���鎞 (http://����L�q)
$title_gif = "";
$tg_w = '150';		# GIF�摜�̕�(�s�N�Z��)
$tg_h = '50';		#   �V     ����(�s�N�Z��)

# �t�@�C�����b�N�`��
#  --> 0=no 1=symlink�֐� 2=open�֐�
#  --> 1 or 2 ��ݒ肷��ꍇ�́A���b�N�t�@�C���𐶐�����f�B���N�g��
#      �̃p�[�~�b�V������ 777 �ɐݒ肷��B
$lockkey = 0;

# ���b�N�t�@�C����
$lockfile = "./petit.lock";

# �J�E���^�̃��b�N�t�@�C����
$cntlock = "./ptcnt.lock";

# �~�j�J�E���^�̐ݒu
#  --> 0=no 1=�e�L�X�g 2=GIF�摜
$counter = 0;
$mini_fig = 5;			# �~�j�J�E���^�̌���
$cnt_color = "#dd0000";		# �e�L�X�g�̂Ƃ��F�~�j�J�E���^�̐F
$gif_path = ".";		# �f�h�e�̂Ƃ��@�F�摜�܂ł̃f�B���N�g��
$mini_w = 8;			#       �V    �@�F�摜�̉��T�C�Y
$mini_h = 12;			#       �V    �@�F�摜�̏c�T�C�Y
$cntfile = "./count.dat";	# �J�E���^�t�@�C��

# �^�O�̋��� (0=no 1=yes)
$tagkey = 0;

# �X�N���v�g�t�@�C��
$script  = "./bbs.cgi";

# ���O�t�@�C�����w��
#  --> �t���p�X�Ŏw�肷��ꍇ�� / ����n�܂�t���p�X�ŁB
#$logfile = "./petit.cgi";

# ���t�̃^�C�v (0=�m�� 1=�a��)
$date_type = 0;

# �L���� [�^�C�g��] ���̐F
$sbj_color = "#006400";

# �L���\�����̉��n�̐F
$tbl_color = "#FFFFFF";

# �ƃA�C�R���̎g�p (0=no 1=yes)
$home_icon = 0;
$home_gif = "home.gif";	# �ƃA�C�R���̃t�@�C����
$home_wid = 25;		# �摜�̉��T�C�Y
$home_hei = 22;		#   �V  �c�T�C�Y

# method�̌`�� (POST/GET)
$method = 'POST';

# �P�y�[�W������̋L���\���� (�e�L��)
$pagelog = 15;

# ���e������ƃ��[���ʒm���� (0=no 1=yes)
#  --> sendmail�K�{
$mailing = 0;

# ���[���A�h���X(���[���ʒm���鎞)
$mailto = 'foo@host.ne.jp';

# sendmail�p�X�i���[���ʒm���鎞�j
$sendmail = '/usr/lib/sendmail';

# �����̋L���̓��[�����M���� (0=no 1=yes)
$mail_me = 0;

# ���T�C�g���瓊�e�r�����鎞�Ɏw�� (http://���珑��)
$base_url = "";

# �����F�̐ݒ�B�㉺�̔z��͕K���y�A�ŁB
@COLORS = ('000000','800000','DF0000','008040','0000FF','C100C1','FF80C0','FF8040','000080');
@IROIRO = ('��','��','��','�݂ǂ�','��','��','�s���N','�I�����W','�����F');

# ���s�`�� (�蓮=soft ����=hard)
$wrap = 'soft';

# URL�̎��������N (0=no 1=yes)
#  --> �^�O���̏ꍇ�� no �Ƃ��邱�ƁB
$autolink = 0;

# �^�O�L���}���I�v�V���� (FreeWeb�Ȃǁj
#   �� <!--�㕔--> <!--����--> �̑���Ɂu�L���^�O�v��}������B
#   �� �L���^�O�ȊO�ɁAMIDI�^�O �� LimeCounter���̃^�O�ɂ��g�p�\�ł��B
$banner1 = '<!--�㕔-->'; # �f���㕔�ɑ}��
$banner2 = '<!--����-->'; # �f�������ɑ}��

# �ߋ����O���� (0=no 1=yes)
$pastkey = 0;
$nofile  = "./pastno.dat";	# �ߋ����O�pNO�t�@�C��
$past_dir = ".";		# �ߋ����O�̃f�B���N�g��
$log_line = '150';		# �ߋ����O�P�t�@�C���̍s��
$petit2 = "./petit2.cgi";	# �ߋ����O�Ǘ��t�@�C��

#============#
#  �ݒ芮��  #
#============#

#$ref_main = 'http://www.elsia.com/com/hako';
#$ref_page = 'http://www.elsia.com/com/tyotou';

#$page = $ENV{'HTTP_REFERER'};
#$page =~ tr/+/ /;
#$page =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
#if (!($page =~ /$ref_page/i)) { &access; }

# ���C������
&decode;
&logpass;
if ($mode eq "howto") { &howto; }
if ($mode eq "find") { &find; }
if ($mode eq "usr_del") { &usr_del; }
if ($mode eq "msg_del") { &msg_del; }
if ($mode eq "msg") { &regist; }
if ($mode eq "res_msg") { &res_msg; }
if ($mode eq "admin") { &admin; }
if ($mode eq "admin_del") { &admin_del; }
&html_log;

#--------------#
#  �L���\����  #
#--------------#
sub html_log {
	# �N�b�L�[���擾
	&get_cookie;

	# �t�H�[�����𒲐�
	&get_bros;

	# ���O��ǂݍ���
	open(IN,"$logfile") || &error("Can't open $logfile");
	@lines = <IN>;
	close(IN);

	# �L���ԍ����J�b�g
	shift(@lines);

	# �e�L���݂̂̔z��f�[�^���쐬
	@new = ();
	foreach $line (@lines) {
		local($num,$k,$date,$name,$email,
			$subj,$com,$url,$host,$pw,$color) = split(/<>/,$line);
		# �e�L�����W��
		if ($k eq "") { push(@new,$line); }
	}

	# ���X�L���̓��X���ɂ��邽�ߔz����t���ɂ���
	@lines = reverse(@lines);

	# �w�b�_���o��
	&header;

	# �J�E���^����
	if ($counter) { &counter; }

	print "<center>$banner1<P>\n";

	# �^�C�g����
	if ($title_gif eq '') {
		print "<font color=$t_color size=$t_size face=\"$t_face\">";
		print "<b>$title</b></font>\n";
	} else {
		print "<img src=\"$title_gif\" width=\"$tg_w\" height=\"$tg_h\">\n";
	}

	print "<hr width=90%>\n";
	print "[<a href=\"$homepage\" target='_top'>�g�b�v�ɂ��ǂ�</a>]\n";
	print "[<a href=\"$hakopage\" target='_top'>����ɂ��ǂ�</a>]\n";
	print "[<a href=\"$script?mode=howto&teamID=$tid&tPASS=$tpass\">�g����</a>]\n";
	print "[<a href=\"$script?mode=find&teamID=$tid&tPASS=$tpass\">���[�h����</a>]\n";

	if ($pastkey) {
		print "[<a href=\"$petit2\">�ߋ����O</a>]\n";
	}

	print <<"EOM";
[<a href="$script?teamID=$tid&tPASS=$tpass&mode=msg_del">�L���폜</a>]
[<a href="${script}?teamID=$tid&tPASS=$tpass&mode=admin">�Ǘ��p</a>]
<hr width="90%">
<BR><FONT SIZE=+2>
<A HREF="chat/chat.cgi?teamID=$tid&tPASS=$tpass&mode=top">��c��(�`���b�g)</A>
</FONT>
</center>
<form method="$method" action="$script">
<input type=hidden name=teamID value="$tid">
<input type=hidden name=tPASS value="$tpass">
<input type=hidden name=mode value="msg">
<blockquote>
<table border=0 cellspacing=0>
<tr>
  <td nowrap><b>���Ȃ܂�</b></td>
  <td>
    <input type=text name=name size="$nam_wid" value="$c_name">
  </td>
</tr>
<tr>
  <td nowrap><b>�d���[��</b></td>
  <td>
    <input type=text name=email size="$nam_wid" value="$c_email">
  </td>
</tr>
<tr>
  <td nowrap><b>��@�@��</b></td>
  <td>
    <input type=text name=subj size="$subj_wid">
�@  <input type=submit value="���e����"><input type=reset value="���Z�b�g">
  </td>
</tr>
<tr>
  <td colspan=2>
    <b>�R�����g</b><br>
    <textarea cols="$com_wid" rows=7 name=comment wrap="$wrap"></textarea>
  </td>
</tr>

<tr>
  <td nowrap><b>�폜�L�[</b></td>
  <td>
    <input type=password name=pwd size=8 maxlength=8 value="$c_pwd">
    <small>(�����̋L�����폜���Ɏg�p�B�p������8�����ȓ�)</small>
  </td>
</tr>
<tr>
  <td nowrap>
    <b>�����F</b>
  </td>
  <td>
EOM

	if ($c_color eq "") { $c_color = "$COLORS[0]"; }
	foreach (@COLORS) {
		if ($c_color eq "$_") {
			print "<input type=radio name=color value=\"$_\" checked>";
			print "<font color=$_>��</font>\n";
		} else {
			print "<input type=radio name=color value=\"$_\">";
			print "<font color=$_>��</font>\n";
		}
	}

	print "</td></tr></table></form></blockquote><hr>\n";

	if ($FORM{'page'} eq '') { $page = 0; } 
	else { $page = $FORM{'page'}; }

	# �L�������擾
	$end_data = @new - 1;
	$page_end = $page + ($pagelog - 1);

	if ($page_end >= $end_data) { $page_end = $end_data; }
	foreach ($page .. $page_end) {
		($num,$k,$date,$name,$email,$sbj,
			$com,$url,$host,$pwd,$color) = split(/<>/, $new[$_]);

		if ($email) { $name = "<a href=mailto\:$email>$name</a>"; }
		if (!$sbj) { $sbj = "Untitled"; }

		# URL�\��
		if ($url && $home_icon) {
			$url = "<a href=\"http://$url\" target=_top><img src=\"$icon_dir\/$home_gif\" border=0 align=top HSPACE=10 WIDTH=\"$home_wid\" HEIGHT=\"$home_hei\"></a>";

		} elsif ($url && $home_icon == 0) {
			$url = "<small>[<a href=\"http://$url\" target=_top>HOME</a>]</small>";
		}

		# ���������N
		if ($autolink) { &auto_link($com); }

		print "<center><table border=1 width=95% cellpadding=5 cellspacing=0 bgcolor=$tbl_color>\n";
		print "<tr><td>\n";
		print "<table border=0 cellspacing=0><tr>\n";
		print "<td>[<b>$num</b>] <font color=$sbj_color><b>$sbj</b></font></td>\n";
		print "<td width=10></td><td>���e�ҁF<font color=$link><b>$name</b></font></td>\n";
		print "<td><small>���e���F$date</small></td><td>$url</td></tr></table>\n";
		print "<blockquote><font color=\"$color\">$com</font></blockquote>\n";

		## ���X���b�Z�[�W��\��
		$flag = 0;
		foreach $line (@lines) {
			($rnum,$rk,$rd,$rname,$rem,
				$rsub,$rcom,$rurl,$rho,$rp,$rc) = split(/<>/, $line);

			if ($num eq "$rk") {
				if ($flag == 0) { print "<P><hr width=95% size=1>\n"; $flag=1; }

				# ���������N
				if ($autolink) { &auto_link($rcom); }

				print "<table border=0 width=100% cellspacing=0><tr>\n";
				print "<td><font color=$rc><b>$rname</b> �� $rcom ";
				print "<small>($rd)</small></font></td></tr></table>\n";
			}
		}

		print "</td></tr></table>\n";
		print "<form action=\"$script\" method=$method>\n";
		print "<input type=hidden name=teamID value=\"$tid\">\n";
		print "<input type=hidden name=tPASS value=\"$tpass\">\n";
		print "<a href=./bbs.cgi?teamID=$tid&tPASS=$tpass>�����[�h</a>\n";
		print "<input type=hidden name=mode value=\"msg\">\n";
		print "<input type=hidden name=resno value=\"$num\">\n";
		print "<input type=hidden name=page value=\"$FORM{'page'}\">\n";
		print "<input type=hidden name=email value=\"$c_email\">\n";
		print "<input type=hidden name=url value=\"$c_url\">\n";

		print "���O<input type=text name=name size=$nam_wid2 value=\"$c_name\">\n";
		print "���X<input type=text name=comment size=$subj_wid>\n";
		print "�����F<select name=color>\n";

		foreach (0 .. $#COLORS) {
			if ($c_color eq "$COLORS[$_]") {
				print "<option value=\"$COLORS[$_]\" selected>$IROIRO[$_]\n";
			} else {
				print "<option value=\"$COLORS[$_]\">$IROIRO[$_]\n";
			}
		}

		print "</select> �폜�L�[<input type=password name=pwd size=4 value=\"$c_pwd\">\n";
		print "<input type=submit value=\"�ԐM����\"></form></center><hr>\n";
	}

	print "<table border=0><tr>\n";

	# ���ŏ���
	$next_line = $page_end + 1;
	$back_line = $page - $pagelog;

	# �O�ŏ���
	if ($back_line >= 0) {
		print "<td><form method=\"$method\" action=\"$script\">\n";
		print "<input type=hidden name=teamID value=\"$tid\">\n";
		print "<input type=hidden name=tPASS value=\"$tpass\">\n";
		print "<input type=hidden name=page value=\"$back_line\">\n";
		print "<input type=hidden name=mode value=\"page\">\n";
		print "<input type=submit value=\"�O��$pagelog��\">\n";
		print "</form></td>\n";	
	}

	# ���ŏ���
	if ($page_end ne $end_data) {
		print "<td><form method=\"$method\" action=\"$script\">\n";
		print "<input type=hidden name=teamID value=\"$tid\">\n";
		print "<input type=hidden name=tPASS value=\"$tpass\">\n";
		print "<input type=hidden name=page value=\"$next_line\">\n";
		print "<input type=hidden name=mode value=\"page\">\n";
		print "<input type=submit value=\"����$pagelog��\">\n";
		print "</form></td>\n";
	}

	print "</tr></table>\n";
	&footer;
	exit;
}

#--------------------#
#  ���O�������ݏ���  #
#--------------------#
sub regist {
	# ���T�C�g����̃A�N�Z�X��r��
	if ($base_url) {
		$ref_url = $ENV{'HTTP_REFERER'};
		$ref_url =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		if ($ref_url !~ /$base_url/i) { &error("�s���ȃA�N�Z�X�ł�"); }
	}

	# ���O�ƃR�����g�͕K�{
	if ($name eq "") { &error("���O�����͂���Ă��܂���"); }
	if ($comment eq "") { &error("�R�����g�����͂���Ă��܂���"); }
	if ($email && $email !~ /(.*)\@(.*)\.(.*)/) {
		&error("�d���[���̓��͓��e������������܂���");
	}

	# �z�X�g�����擾
	&get_host;

	# �t�@�C�����b�N
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }

	# ���O���J��
	open(IN,"$logfile") || &error("Can't open $logfile");
	@lines = <IN>;
	close(IN);

	# �e�L��NO����
	$oya = $lines[0];
	if ($oya =~ /<>/) {
		&error("���O������������܂���B<P>
			(v2.5�ȑO�̃��O�̏ꍇ�͕ϊ��̕K�v������܂�)");
	}
	$oya =~ s/\n//;
	shift(@lines);

	# ��d���e�̋֎~
	local($flag) = 0;
	foreach $line (@lines) {
		($knum,$kk,$kd,$kname,$kem,$ksub,$kcom) = split(/<>/,$line);
		if ($name eq "$kname" && $comment eq "$kcom") {
			$flag=1; last;
		}
	}
	if ($flag) { &error("��d���e�͋֎~�ł�"); }

	# �e�L���̏ꍇ�A�L��No���J�E���g�A�b�v���A�N�b�L�[�𔭍s
	if ($FORM{'resno'} eq "") { $oya++; }
	&set_cookie;
	$number = $oya;

	# �폜�L�[���Í���
	if ($pwd) { $ango = &passwd_encode($pwd); }

	# ���Ԃ��擾
	&get_time;

	# ���O���t�H�[�}�b�g
	$new_msg = "$number<>$FORM{'resno'}<>$date<>$name<>$email<>$subj<>$comment<>$url<>$host<>$ango<>$color<>\n";

	## �����\�[�g���́A���X�L�����e���͐e�L���̓g�b�v�ֈړ�
	if ($res_sort && $FORM{'resno'} ne "") {
		@res_data = ();
		@new = ();
		foreach $line (@lines) {
		  $flag = 0;
		  ($num,$k,$d,$na,$em,$sub,$com,$u,$ho,$p,$c,$ico) = split(/<>/,$line);

		  # �e�L���𔲂��o��
		  if ($k eq "" && $FORM{'resno'} eq "$num") {
			$new_line = "$line";
			$flag = 1;
		  }
		  # �֘A�̃��X�L���𔲂��o��
		  elsif ($k eq "$FORM{'resno'}") {
			push(@res_data,$line);
			$flag = 1;
		  }
		  if ($flag == 0) { push(@new,$line); }
		}

		# �֘A���X�L�����g�b�v��
		unshift(@new,@res_data);

		# �V�K���b�Z�[�W���g�b�v��
		unshift(@new,$new_msg);

		# �e�L�����g�b�v��
		unshift(@new,$new_line);

	## �e�L���̏ꍇ�A�ő�L�����𒴂���L�����J�b�g
	} elsif ($FORM{'resno'} eq "") {

		$i = 0;
		$stop = 0;
		foreach $line (@lines) {
		    ($num,$k,$d,$na,$em,$sub,$com,$u,$ho,$p,$c,$ico)=split(/<>/,$line);

		    if ($k eq "") { $i++; }
		    if ($i > $max-1) {
			$stop = 1;
			if ($pastkey == 0) { last; }
			else {
				if ($k eq "") { $kflag=1; push(@past_data,$line); }
				else { push(@past_res,$line); }
			}
		    }
		    if ($stop == 0) { push(@new,$line); }
		}

		## �ߋ��L������
		if ($kflag) {
			@past_res = reverse(@past_res);
			push(@past_data,@past_res);
			&pastlog;
		}

		unshift(@new,$new_msg);

	## ���X�L���͋L�����̒����͂��Ȃ�
	} else {
		@res_data = ();
		@new = ();

		foreach $line (@lines) {
		  $flag = 0;
		  ($num,$k,$d,$na,$em,$sub,$com,$u,$ho,$p,$c,$ico) = split(/<>/,$line);

		  # �e�L���𔲂��o��
		  if ($k eq "" && $FORM{'resno'} eq "$num") {
			$new_line = "$line";
			$flag = 2;
		  }
		  if ($flag == 0) { push(@new,$line); }
		  elsif ($flag == 2) {
			push(@new,$new_line);
			push(@new,$new_msg);
		  }
		}
	}

	# �e�L��NO��t��
	unshift (@new,"$oya\n");

	# ���O���X�V
	open(OUT,">$logfile") || &error("Can't write $logfile");
	print OUT @new;
	close(OUT);

	# ���b�N����
	if (-e $lockfile) { unlink($lockfile); }

	# ���[������
	if ($mailing && $mail_me) { &mail_to; }
	elsif ($mailing && $mail_me == 0 && $email ne "$mailto") { &mail_to; }
}

#---------------#
#  �f�R�[�h���� #
#---------------#
sub decode {
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		if ($ENV{'CONTENT_LENGTH'} > 51200) { &error("���e�ʂ��傫�����܂�"); }
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	} else { $buffer = $ENV{'QUERY_STRING'}; }

	@pairs = split(/&/,$buffer);
	foreach $pair (@pairs) {
		($name, $value) = split(/=/, $pair);
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

		# �����R�[�h�ϊ�
		&jcode'convert(*value,'sjis');

		# �^�O����
		if ($tagkey == 0) {
			$value =~ s/</&lt\;/g;
			$value =~ s/>/&gt\;/g;
		} else {
			$value =~ s/<!--(.|\n)*-->//g;
			$value =~ s/<>/&lt\;&gt\;/g;
		}

		# �ꊇ�폜�p
		if ($name eq 'del') { push(@delete,$value); }

		$FORM{$name} = $value;
	}
	$name = $FORM{'name'};
	$comment = $FORM{'comment'};
	$comment =~ s/\r\n/<br>/g;
	$comment =~ s/\r|\n/<br>/g;
	$email = $FORM{'email'};
	$url   = $FORM{'url'};
	$url   =~ s/^http\:\/\///;
	$mode  = $FORM{'mode'};
	$subj  = $FORM{'subj'};
	$pwd   = $FORM{'pwd'};
	$color = $FORM{'color'};
}

#----------------------------#
#  �f���̎g�������b�Z�[�W  #
#----------------------------#
sub howto {
	if ($tagkey == 0) { $tag_msg = "���e���e�ɂ́A<b>�^�O�͈�؎g�p�ł��܂���B</b>\n"; }
	else { $tag_msg = "�R�����g���ɂ́A<b>�^�O�g�p�����邱�Ƃ��ł��܂��B</b>\n"; }

	&header;
	print <<"HTML";
[<a href="$script?teamID=$tid&tPASS=$tpass\">�f���ɂ��ǂ�</a>]
<table width="100%"><tr><th bgcolor="#0000A0">
<font color="#FFFFFF">�f���̗��p��̒���</font>
</th></tr></table>
<P><center>
<table width=90% border=1 cellpadding=10>
<tr><td bgcolor="$tbl_color">
<OL>
<LI>���̌f����<b>�N�b�L�[�Ή�</b>�ł��B�P�x�L���𓊍e���������ƁA���Ȃ܂��A�d���[���A�t�q�k�A�폜�L�[�̏��͂Q��ڈȍ~�͎������͂���܂��B�i���������p�҂̃u���E�U���N�b�L�[�Ή��̏ꍇ�j<P>
<LI>$tag_msg<P>
<LI>�L���𓊍e�����ł̕K�{���͍��ڂ�<b>�u���Ȃ܂��v</b>��<b>�u���b�Z�[�W�v</b>�ł��B�d���[���A�t�q�k�A�薼�A�폜�L�[�͔C�ӂł��B<P>
<LI>�L���ɂ́A<b>���p�J�i�͈�؎g�p���Ȃ��ŉ������B</b>���������̌����ƂȂ�܂��B<P>
<LI>�L���̓��e����<b>�u�폜�L�[�v</b>�Ƀp�X���[�h�i�p������8�����ȓ��j�����Ă����ƁA���̋L���͎���<b>�폜�L�[</b>�ɂ���č폜���邱�Ƃ��ł��܂��B<P>
<LI>�L���̕ێ�������<b>�ő� $max��</b>�ł��B����𒴂���ƌÂ����Ɏ����폜����܂��B<P>
<LI>�����̋L����<b>�u�P�s���X�v</b>��t���邱�Ƃ��ł��܂��B�L���\\���������ɂ���ԐM�p�t�H�[������L���𓊍e���邱�Ƃ��ł��܂��B<P>
<LI>�ߋ��̓��e�L������<b>�u�L�[���[�h�v�ɂ���ĊȈՌ������ł��܂��B</b>�g�b�v���j���[��<a href="$script?mode=find&teamID=$tid&tPASS=$tpass">�u���[�h�����v</a>�̃����N���N���b�N����ƌ������[�h�ƂȂ�܂��B<P>
<LI>�Ǘ��҂��������s���v�Ɣ��f����L���⑼�l���排�������L����\�\\��\�Ȃ��폜���邱�Ƃ�����܂��B
</OL>
</td></tr></table>
</center><hr>
HTML
	&footer;
	exit;
}

#--------------------------#
#  ���[�h�����T�u���[�`��  #
#--------------------------#
sub find {
	&header;
	print <<"HTML";
[<a href="$script?teamID=$tid&tPASS=$tpass">�f���ɂ��ǂ�</a>]
<table width="100%"><tr><th bgcolor="#0000A0">
<font color="#FFFFFF">���[�h����</font></th></tr></table>
<P><center>
<table cellpadding=5>
<tr><td bgcolor="$tbl_color" nowrap>
  <UL>
  <LI>����������<b>�L�[���[�h</b>����͂��A�����̈��I�����āu�����{�^���v
      �������Ă��������B
  <LI>�L�[���[�h���u���p�X�y�[�X�v�ŋ�؂��ĕ����w�肷�邱�Ƃ��ł��܂��B
  </UL>
</td></tr></table><P>
<form action="$script" method="$method">
<input type=hidden name=teamID value="$tid">
<input type=hidden name=tPASS value="$tpass">
<input type=hidden name=mode value="find">
<table border=1>
<tr>
  <th colspan=2>�L�[���[�h <input type=text name=word size=30></th>
</tr>
<tr>
  <td>��������</td>
  <td>
    <input type=radio name=cond value="and" checked>AND
    <input type=radio name=cond value="or">OR
  </td>
</tr>
<tr>
  <th colspan=2>
    <input type=submit value="��������"><input type=reset value="���Z�b�g">
  </th>
</tr>
</table>
</form>
</center>
HTML
	# ���[�h�����̎��s�ƌ��ʕ\��
	if ($FORM{'word'} ne "") {

		# ���͓��e�𐮗�
		$cond = $FORM{'cond'};
		$word = $FORM{'word'};
		$word =~ s/�@/ /g;
		$word =~ s/\t/ /g;
		@pairs = split(/ /,$word);

		# �t�@�C����ǂݍ���
		open(DB,"$logfile") || &error("Can't open $logfile");
		@lines = <DB>;
		close(DB);

		# ��������
		foreach (1 .. $#lines) {
			$flag = 0;
			foreach $pair (@pairs){
				if (index($lines[$_],$pair) >= 0){
					$flag = 1;
					if ($cond eq 'or') { last; }
				} else {
					if ($cond eq 'and'){ $flag = 0; last; }
				}
			}
			if ($flag == 1) { push(@new,$lines[$_]); }
		}

		# �����I��
		$count = @new;
		print "<hr><b><font color=$t_color>�������ʁF$count��</font></b><P>\n";
		print "<OL>\n";

		foreach $line (@new) {
			($num,$k,$date,$name,$email,$sub,$com,$url) = split(/<>/, $line);
			if (!$sub) { $sub = "Untitled"; }
			if ($email) { $name = "<a href=mailto\:$email>$name</a>"; }
			if ($url) { $url = "[<a href=\"http://$url\" target=_top>HOME</a>]"; }

			if ($k) { $num = "$k�ւ̃��X"; }

			# ���ʂ�\��
			print "<LI>[$num] <font color=$sbj_color><b>$sub</b></font>\n";
			print "���e�ҁF<b>$name</b> <small>$url ���e���F$date</small><P>\n";
			print "<blockquote>$com</blockquote><hr size=2>\n";
		}

		print "</OL><P>\n";
	}
	&footer;
	exit;
}

#--------------#
#  �����̎擾  #
#--------------#
sub get_time {
	$ENV{'TZ'} = "JST-9";
	($sec,$min,$hour,$mday,$mon,$year,$wday,$dmy,$dmy) = localtime(time);
	$year += 1900;
	$mon++;
	if ($mon  < 10) { $mon  = "0$mon";  }
	if ($mday < 10) { $mday = "0$mday"; }
	if ($hour < 10) { $hour = "0$hour"; }
	if ($min  < 10) { $min  = "0$min";  }
	if ($sec  < 10) { $sec  = "0$sec";  }

	# �����̃t�H�[�}�b�g
	if ($date_type && $FORM{'resno'} eq "") {
		$youbi = ('��','��','��','��','��','��','�y') [$wday];
		$date = "$year�N$mon��$mday�� ($youbi) $hour��$min��$sec�b";
	} else {
		$youbi = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat') [$wday];
		$date = "$year/$mon/$mday($youbi) $hour\:$min\:$sec";
	}
}

#------------------------------------#
#  �u���E�U�𔻒f���t�H�[�����𒲐�  #
#------------------------------------#
sub get_bros {
	# �u���E�U�����擾
	$agent = $ENV{'HTTP_USER_AGENT'};

	if ($agent =~ /MSIE 3/i) { 
		$nam_wid  = 30;
		$subj_wid = 40;
		$com_wid  = 65;
		$url_wid  = 48;
		$nam_wid2 = 15;
	} elsif ($agent =~ /MSIE 4/i || $agent =~ /MSIE 5/i) { 
		$nam_wid  = 30;
		$subj_wid = 40;
		$com_wid  = 65;
		$url_wid  = 78;
		$nam_wid2 = 15;
	} else {
		$nam_wid  = 20;
		$subj_wid = 25;
		$com_wid  = 56;
		$url_wid  = 50;
		$nam_wid2 = 10;
	}
}

#------------#
#  �폜���  #
#------------#
sub msg_del {
	if ($FORM{'action'} eq 'admin' && $FORM{'pass'} ne "$pass") {
		&error("�p�X���[�h���Ⴂ�܂�");
	}

	open(DB,$logfile) || &error("Can't open $logfile");
	@lines = <DB>;
	close(DB);

	shift(@lines);

	# �e�L���݂̂̔z��f�[�^���쐬
	@new = ();
	foreach $line (@lines) {
		local($num,$k,$date,$name,
			$email,$sub,$com,$url,$host,$pw) = split(/<>/,$line);

		# RES�L�����O��
		if ($k eq "") { push(@new,$line); }
	}

	@lines = reverse(@lines);

	&header;
	print "[<a href=\"$script?teamID=$tid&tPASS=$tpass\">�f���֖߂�</a>]\n";
	print "<table width=100%><tr><th bgcolor=\"#0000A0\">\n";
	print "<font color=\"#FFFFFF\">�R�����g�폜���</font></th></tr></table>\n";
	print "<P><center>\n";
	print "<table border=0 cellpadding=5><tr>\n";
	print "<td bgcolor=\"$tbl_color\">\n";

	if ($FORM{'action'} eq '') {
		print "�����e���ɋL�������u�폜�L�[�v�ɂ��A�L�����폜���܂��B<br>\n";
	}

	print "���폜�������L���̃`�F�b�N�{�b�N�X�Ƀ`�F�b�N�����A���L�t�H�[���Ɂu�폜�L�[�v����͂��Ă��������B<br>\n";
	print "���e�L�����폜����ꍇ�A���̃��X���b�Z�[�W�������ɏ��ł��Ă��܂����ƂɂȂ�܂��̂ŁA�����ӂ��������B<br>\n";
	print "</td></tr></table><P>\n";
	print "<form action=\"$script\" method=$method>\n";

	if ($FORM{'action'} eq '') {
		print "<input type=hidden name=mode value=\"usr_del\">\n";
		print "<b>�폜�L�[</b> <input type=text name=del_key size=10>\n";
	} else {
		print "<input type=hidden name=mode value=\"admin_del\">\n";
		print "<input type=hidden name=action value=\"admin\">\n";
		print "<input type=hidden name=pass value=\"$FORM{'pass'}\">\n";
	}
	print "<input type=hidden name=teamID value=\"$tid\">\n";
	print "<input type=hidden name=tPASS value=\"$tpass\">\n";
	print "<input type=submit value=\"�폜����\"><input type=reset value=\"���Z�b�g\">\n";
	print "<P><table border=1>\n";
	print "<tr><th>�폜</th><th>�L��No</th><th>�薼</th><th>���e��</th>";
	print "<th>���e��</th><th>�R�����g</th>\n";

	if ($FORM{'action'} eq 'admin') { print "<th>�z�X�g��</th>\n"; }

	print "</tr>\n";

	if ($FORM{'page'} eq '') { $page = 0; }
	else { $page = $FORM{'page'}; }

	# �L�������擾
	$end_data = @new - 1;
	$page_end = $page + ($pagelog - 1);
	if ($page_end >= $end_data) { $page_end = $end_data; }

	foreach ($page .. $page_end) {
		($num,$k,$date,$name,$email,$sub,
			$com,$url,$host,$pw,$color) = split(/<>/,$new[$_]);

		if ($email) { $name="<a href=mailto\:$email>$name</a>"; }
		if (!$sub) { $sub = "Untitled"; }

		$com =~ s/<br>/ /g;
		if ($tagkey) { $com =~ s/</&lt;/g; $com =~ s/>/&gt;/g; }
		if (length($com) > 60) { $com=substr($com,0,58); $com=$com . '..'; }

		if ($FORM{'action'} eq 'admin') {
			print "<tr><th><input type=checkbox name=del value=\"$date\"></th>\n";

		} else {
			print "<tr><th><input type=radio name=del value=\"$date\"></th>\n";
		}

		print "<th>$num</th><td>$sub</td><td>$name</td>\n";
		print "<td><small>$date</small></td><td>$com</td>\n";

		if ($FORM{'action'} eq 'admin') { print "<td>$host</td>\n"; }

		print "</tr>\n";

		## ���X���b�Z�[�W��\��
		foreach (@lines) {
			($rnum,$rk,$rd,$rname,$rem,$rsub,
				$rcom,$rurl,$rho,$rp,$rc) = split(/<>/, $_);

			$rcom =~ s/<br>/ /g;
			if ($tagkey) { $rcom =~ s/</&lt;/g; $rcom =~ s/>/&gt;/g; }
			if (length($rcom) > 60) { $rcom=substr($rcom,0,58); $rcom=$rcom . '..'; }
			if ($num eq "$rk"){

				if ($FORM{'action'} eq 'admin') {
					print "<tr><th><input type=checkbox name=del value=\"$rd\"></th>\n";
				} else {
					print "<tr><th><input type=radio name=del value=\"$rd\"></th>\n";
				}

				print "<td colspan=2 align=center><b>$num</b>�ւ̃��X</td>\n";
				print "<td>$rname</td><td><small>$rd</small></td><td>$rcom</td>\n";

				if ($FORM{'action'} eq 'admin') { print "<td>$rho</td>\n"; }

				print "</tr>\n";
			}
		}
	}
	print "</table></form>\n";
	print "<table border=0 width=100%><tr>\n";

	# ���ŏ���
	$next_line = $page_end + 1;
	$back_line = $page - $pagelog;

	# �O�ŏ���
	if ($back_line >= 0) {
		print "<td><form method=\"$method\" action=\"$script\">\n";
		print "<input type=hidden name=teamID value=\"$tid\">\n";
		print "<input type=hidden name=tPASS value=\"$tpass\">\n";
		print "<input type=hidden name=page value=\"$back_line\">\n";
		print "<input type=hidden name=mode value=msg_del>\n";
		print "<input type=submit value=\"�O�̐e�L��$pagelog��\">\n";

		if ($FORM{'action'} eq 'admin') {
		  print "<input type=hidden name=action value=\"admin\">\n";
		  print "<input type=hidden name=pass value=\"$FORM{'pass'}\">\n";
		}

		print "</form></td>\n";	
	}

	# ���ŏ���
	if ($page_end ne $end_data) {
		print "<td><form method=\"$method\" action=\"$script\">\n";
		print "<input type=hidden name=teamID value=\"$tid\">\n";
		print "<input type=hidden name=tPASS value=\"$tpass\">\n";
		print "<input type=hidden name=page value=\"$next_line\">\n";
		print "<input type=hidden name=mode value=msg_del>\n";
		print "<input type=submit value=\"���̐e�L��$pagelog��\">\n";

		if ($FORM{'action'} eq 'admin') {
		  print "<input type=hidden name=action value=\"admin\">\n";
		  print "<input type=hidden name=pass value=\"$FORM{'pass'}\">\n";
		}

		print "</form></td>\n";
	}

	print "</tr></table><P><hr><P>\n";
	&footer;
	exit;
}

## --- ���[�U�L���폜����
sub usr_del {
	if ($FORM{'del_key'} eq "") { &error("�폜�L�[�����̓����ł��B"); }
	if ($FORM{'del'} eq "") { &error("���W�I�{�^���̑I��������܂���B"); }

	# ���b�N�J�n
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }

	# ���O��ǂݍ���
	open(DB,"$logfile") || &error("Can't open $logfile");
	@lines = <DB>;
	close(DB);

	# �e�L��NO
	$oya = $lines[0];
	if ($oya =~ /<>/) {
		&error("���O������������܂���B<P><small>\(v2.5�ȑO�̃��O�̏ꍇ�͕ϊ��̕K�v������܂�\)<\/small>");
	}

	shift(@lines);

	## �폜�L�[�ɂ��L���폜 ##
	@new=();
	foreach $line (@lines) {
		$dflag = 0;
		($num,$k,$dt,$name,$email,$sub,$com,$url,$host,$pw) = split(/<>/,$line);

		if ($FORM{'del'} eq "$dt") {
			$dflag = 1;
			$encode_pwd = $pw;
			$del_num = $num;
			if ($k eq '') { $oyaflag=1; }

		} elsif ($oyaflag && $del_num eq "$k") {
			$dflag = 1;
		}

		if ($dflag == 0) { push(@new,$line); }
	}

	if ($del_num eq '') { &error("�폜�ΏۋL����������܂���"); }
	else {
		if ($encode_pwd eq '') { &error("�폜�L�[���ݒ肳��Ă��܂���"); }
		$check = &passwd_decode("$FORM{'del_key'}","$encode_pwd");
		if ($check ne 'yes') { &error("�p�X���[�h���Ⴂ�܂�"); }
	}

	# �e�L��NO��t��
	unshift(@new,$oya);

	## ���O���X�V ##
	open(DB,">$logfile") || &error("Can't write $logfile");
	print DB @new;
	close(DB);

	# ���b�N����
	if (-e $lockfile) { unlink($lockfile); }

	# �폜��ʂɂ��ǂ�
	&msg_del;
}

#----------------------#
#  �Ǘ��҈ꊇ�L���폜  #
#----------------------#
sub admin_del {
	if ($FORM{'pass'} ne "$pass") { &error("�p�X���[�h���Ⴂ�܂�"); }
	if ($FORM{'del'} eq "") { &error("�`�F�b�N�{�b�N�X�̑I��������܂���"); }

	# ���b�N�J�n
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }

	# ���O��ǂݍ���
	open(DB,"$logfile") || &error("Can't open $logfile");
	@lines = <DB>;
	close(DB);

	# �e�L��NO
	$oya = $lines[0];
	if ($oya =~ /<>/) {
		&error("���O������������܂���B<P><small>\(v2.5�ȑO�̃��O�̏ꍇ�͕ϊ��̕K�v������܂�\)<\/small>");
	}

	shift(@lines);

	## �폜����
	foreach $line (@lines) {
		$dflag=0;
		($num,$k,$dt,$name,$email,$sub,$com,$url,$host,$pw) = split(/<>/,$line);

		foreach $del (@delete) {
			if ($del eq "$dt") {
				$dflag = 1;
				$del_num = $num;
				if ($k eq '') { $oyaflag=1; }

			} elsif ($oyaflag && $del_num eq "$k") {
				$dflag = 1;
			}
		}
		if ($dflag == 0) { push(@new,$line); }
	}

	# �e�L��NO��t��
	unshift(@new,$oya);

	## ���O���X�V ##
	open(DB,">$logfile") || &error("Can't write $logfile");
	print DB @new;
	close(DB);

	# ���b�N����
	if (-e $lockfile) { unlink($lockfile); }

	# �폜��ʂɂ��ǂ�
	&msg_del;
}

## --- �Ǘ��ғ������
sub admin {
	&header;
	print "<center><h4>�p�X���[�h����͂��Ă�������</h4>\n";
	print "<form action=\"$script\" method=$method>\n";
	print "<input type=hidden name=teamID value=\"$tid\">\n";
	print "<input type=hidden name=tPASS value=\"$tpass\">\n";
	print "<input type=hidden name=mode value=\"msg_del\">\n";
	print "<input type=hidden name=action value=\"admin\">\n";
	print "<input type=password name=pass size=8><input type=submit value='�F��'>\n";
	print "</form></center>\n";
	print "</body></html>\n";
	exit;
}

## --- �J�E���^����
sub counter {
	# �{�����̂݃J�E���g�A�b�v
	$match=0;
	if ($FORM{'mode'} eq '') {
		# �J�E���^���b�N
		if ($lockkey) { &lock3; }

		$match=1;
	}

	# �J�E���g�t�@�C����ǂ݂���
	open(NO,"$cntfile") || &error("Can't open $cntfile",'0');
	$cnt = <NO>;
	close(NO);

	# �J�E���g�A�b�v
	if ($match) { $cnt++; }

	# �X�V
	open(OUT,">$cntfile") || &error("Write Error : $cntfile");
	print OUT $cnt;
	close(OUT);

	# �J�E���^���b�N����
	if (-e $cntlock) { unlink($cntlock); }

	# ��������
	while(length($cnt) < $mini_fig) { $cnt = '0' . "$cnt"; }
	@cnts = split(//,$cnt);

	print "<table><tr><td>\n";

	# GIF�J�E���^�\��
	if ($counter == 2) {
		foreach (0 .. $#cnts) {
			print "<img src=\"$gif_path/$cnts[$_]\.gif\" alt=\"$cnts[$_]\" width=\"$mini_w\" height=\"$mini_h\">";
		}

	# �e�L�X�g�J�E���^�\��
	} else {
		print "<font color=\"$cnt_color\" face=\"verdana,Times New Roman,Arial\">$cnt</font>";
	}

	print "</td></tr></table>\n";
}

## --- ���b�N�t�@�C���isymlink�֐��j
sub lock1 {
	local($retry) = 5;
	while (!symlink(".", $lockfile)) {
		if (--$retry <= 0) { &error('LOCK is BUSY'); }
		sleep(1);
	}
}

## --- ���b�N�t�@�C���iopen�֐��j
sub lock2 {
	local($flag) = 0;
	foreach (1 .. 5) {
		if (-e $lockfile) { sleep(1); }
		else {
			open(LOCK,">$lockfile");
			close(LOCK);
			$flag = 1;
			last;
		}
	}
	if ($flag == 0) { &error("LOCK is BUSY"); }
}

## --- �J�E���^���b�N
sub lock3 {
	$cnt_flag = 0;
	foreach (1 .. 7) {
		if (-e $cntlock) { sleep(1); }
		else {
			open(LOCK,">$cntlock");
			close(LOCK);
			$cnt_flag = 1;
			last;
		}
	}
	if (!$cnt_flag) { unlink($cntlock); }
}

## --- ���[�����M
sub mail_to {
	$mail_subj = "$title �ɓ��e������܂����B";

    	&jcode'convert(*mail_subj,'jis');
    	&jcode'convert(*name,'jis');
    	&jcode'convert(*subj,'jis');
    	&jcode'convert(*comment,'jis');
	if ($date_type && $FORM{'resno'} eq "") { &jcode'convert(*date,'jis'); }

	$comment =~ s/<br>/\n/g;
	$comment =~ s/\&lt\;/</g;
	$comment =~ s/\&gt\;/>/g;

	open(MAIL,"| $sendmail $mailto") || &error("Can't post sendmail");
	print MAIL "To: $mailto\n";

	# ���[���A�h���X���Ȃ��ꍇ�̓_�~�[���[���ɒu������
	if ($FORM{'email'} eq "") { $email = 'nomail@xxx.xxx'; }

	print MAIL "From: $email\n";
	print MAIL "Subject: $mail_subj\n";
	print MAIL "MIME-Version: 1.0\n";
	print MAIL "Content-type: text/plain; charset=ISO-2022-JP\n";
	print MAIL "Content-Transfer-Encoding: 7bit\n";
	print MAIL "X-Mailer: $ver\n\n";
	print MAIL "$mail_subj\n";
	print MAIL "--------------------------------------------------------\n";
	print MAIL "TIME : $date\n";
	print MAIL "NAME : $name\n";
	print MAIL "EMAIL: $FORM{'email'}\n";
	if ($url ne "") { print MAIL "URL  : http://$url\n"; }

	if ($FORM{'resno'} ne "") { $subj = "(Res Message)"; }
	elsif ($FORM{'resno'} eq "" && $subj eq "") { $subj = "no title"; }

	print MAIL "TITLE: $subj\n\n";
	print MAIL "$comment\n";
	print MAIL "--------------------------------------------------------\n";
	close(MAIL);
}

#----------------------#
#  �p�X���[�h�Í�����  #
#----------------------#
sub passwd_encode {
	$inpw = $_[0];
	@SALT = ('a'..'z', 'A'..'Z', '0'..'9', '.', '/');
	srand;
	$salt = $SALT[int(rand(@SALT))] . $SALT[int(rand(@SALT))];
	return crypt($inpw, $salt);
}

#----------------------#
#  �p�X���[�h�ƍ�����  #
#----------------------#
sub passwd_decode {
	($inpw, $logpw) = @_;
	if ($logpw =~ /^\$1\$/) { $key = 3; } else { $key = 0; }

	local($check) = "no";
	if (crypt($inpw, substr($logpw,$key,2)) eq "$logpw") {
		$check = "yes";
	}
}

#--------------#
#  ���������N  #
#--------------#
sub auto_link {
	$_[0] =~ s/([^=^\"]|^)(http\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#]+)/$1<a href=$2 target=_top>$2<\/a>/g;
}

#------------------#
#  HTML�̃w�b�_�[  #
#------------------#
sub header { 
	print "Content-type: text/html\n\n";
	print <<"EOM";
<html>
<head>
<META http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<title>$title</title></head>
<body background="$backgif" bgcolor="$bgcolor" text="$text" link="$link" vlink="$vlink" alink="$alink">
EOM
}

## --- HTML�̃t�b�^�[
sub footer {
	## ���쌠�\���i�폜�s�j
	print "<center>$banner2<P><small><!-- $ver -->\n";
	print "- <a href=\"http://www.kent-web.com/\" target='_top'>Petit Board</a> -\n";
	print "<BR>Edit:<a href=\"http://espion.s7.xrea.com/\" target='_top'>Web note</a> -\n";
	print "</small></center>\n";
	print "</body></html>\n";
}

## --- �N�b�L�[�̔��s
sub set_cookie {
	# �N�b�L�[��60���ԗL��
	($secg,$ming,$hourg,$mdayg,$mong,$yearg,$wdayg) = gmtime(time + 60*24*60*60);

	$yearg += 1900;
	if ($secg  < 10) { $secg  = "0$secg";  }
	if ($ming  < 10) { $ming  = "0$ming";  }
	if ($hourg < 10) { $hourg = "0$hourg"; }
	if ($mdayg < 10) { $mdayg = "0$mdayg"; }

	$month = ('Jan','Feb','Mar','Apr','May','Jun',
			'Jul','Aug','Sep','Oct','Nov','Dec')[$mong];
	$youbi = ('Sunday','Monday','Tuesday','Wednesday',
			'Thursday','Friday','Saturday')[$wdayg];

	$date_gmt = "$youbi, $mdayg\-$month\-$yearg $hourg:$ming:$secg GMT";
	$cook="name\:$name\,email\:$email\,url\:$url\,pwd\:$pwd\,color\:$color";
	print "Set-Cookie: PETIT=$cook; expires=$date_gmt\n";
}

## --- �N�b�L�[���擾
sub get_cookie {
	@pairs = split(/\;/, $ENV{'HTTP_COOKIE'});
	foreach $pair (@pairs) {
		local($name, $value) = split(/\=/, $pair);
		$name =~ s/ //g;
		$DUMMY{$name} = $value;
	}
	@pairs = split(/\,/, $DUMMY{'PETIT'});
	foreach $pair (@pairs) {
		local($name, $value) = split(/\:/, $pair);
		$COOKIE{$name} = $value;
	}

	$c_name  = $COOKIE{'name'};
	$c_email = $COOKIE{'email'};
	$c_url   = $COOKIE{'url'};
	$c_pwd   = $COOKIE{'pwd'};
	$c_color = $COOKIE{'color'};

	if ($FORM{'name'})  { $c_name  = $FORM{'name'}; }
	if ($FORM{'email'}) { $c_email = $FORM{'email'}; }
	if ($FORM{'url'})   { $c_url   = $url; }
	if ($FORM{'pwd'})   { $c_pwd   = $FORM{'pwd'}; }
	if ($FORM{'color'}) { $c_color = $FORM{'color'}; }
}

## --- �G���[����
sub error {
	if (-e $lockfile) { unlink($lockfile); }
	if ($_[1] ne '0') { &header; }

	print "<center><hr width=\"75%\"><P><h3>ERROR !</h3>\n";
	print "<P><font color=red><B>$_[0]\n";
	print "<P>���`�[���p�X���[�h���ς���Ă���\\��������܂��̂ŁA�ēx�J����ʂ��炨���艺����</B></font>\n";
	print "<P><hr width=\"75%\"></center>\n";
	&footer;
	exit;
}

## --- �z�X�g���擾
sub get_host {
	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};

	if ($get_remotehost) {
		if ($host eq "" || $host eq "$addr") {
			$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
		}
	}
	if ($host eq "") { $host = $addr; }
}

## --- �ߋ����O����
sub pastlog {
	$new_flag = 0;

	# �ߋ�NO���J��
	open(NO,"$nofile") || &error("Can't open $nofile");
	$count = <NO>;
	close(NO);

	# �ߋ����O�̃t�@�C�������`
	$pastfile  = "$past_dir/$count\.html";

	# �ߋ����O���Ȃ��ꍇ�A�V�K�Ɏ�����������
	unless(-e $pastfile) { &new_log; }

	# �ߋ����O���J��
	if ($new_flag == 0) {
		open (IN,"$pastfile") || &error("Can't open $pastfile");
		@past = <IN>;
		close(IN);
	}

	# �K��̍s�����I�[�o�[����ƁA���t�@�C����������������
	if ($#past > $log_line) { &next_log; }

	foreach $pst_line (@past_data) {
		($pnum,$pk,$pdt,$pname,$pemail,$psub,$pcom,
			$purl,$phost,$ppw) = split(/<>/, $pst_line);

		if ($pk eq "" && $psub eq "") { $psub = "no title"; }
		if ($pemail) { $pname = "<a href=mailto:$pemail>$pname</a>"; }
		if ($purl) { $purl="<a href=http://$purl target=_top>http://$purl</a>"; }
		if ($pk) { $pnum = "$pk�ւ̃��X"; }

		# ���������N
		if ($autolink) { &auto_link($pcom); }

		# �ۑ��L�����t�H�[�}�b�g
		$html = <<"HTML";
[$pnum] <font color=$sbj_color><b>$psub</b></font><!--T--> ���e�ҁF<font color=$link><b>$pname</b></font> <small>���e���F$pdt</small><p><blockquote>$pcom<p>$purl</blockquote><!--$phost--><hr>
HTML
		push(@htmls,"$html");
	}

	
	@news = ();
	foreach $line (@past) {
		if ($line =~ /<!--OWARI-->/i) { last; }
		push (@news,$line);
		if ($line =~ /<!--HAJIME-->/i) { push (@news,@htmls); }
	}

	push (@news,"<!--OWARI-->\n</body></html>\n");

	# �ߋ����O���X�V
	open(OUT,">$pastfile") || &error("Can't write $pastfile");
	print OUT @news;
	close(OUT);

}

## --- �ߋ����O���t�@�C���������[�`��
sub next_log {
	# ���t�@�C���̂��߂̃J�E���g�A�b�v
	$count++;

	# �J�E���g�t�@�C���X�V
	open(NO,">$nofile") || &error("Can't write $nofile");
	print NO "$count";
	close(NO);

	$pastfile  = "$past_dir/$count\.html";

	&new_log;
}

## --- �V�K�ߋ����O�t�@�C���������[�`��
sub new_log {
	$new_flag = 1;

	if ($backgif) { $bgkey = "background=\"$backgif\""; }
	else { $bgkey = "bgcolor=$bgcolor"; }

	$past[0] = "<html><head><title>�ߋ����O</title></head>\n";
	$past[1] = "<body $bgkey text=$text link=$link vlink=$vlink alink=$alink><hr size=1>\n";
	$past[2] = "<\!--HAJIME-->\n";
	$past[3] = "<\!--OWARI-->\n";
	$past[4] = "</body></html>\n";

	# �V�K�ߋ����O�t�@�C���𐶐��X�V
	open(OUT,">$pastfile") || &error("Can't write $pastfile");
	print OUT @past;
	close(OUT);

	# �p�[�~�b�V������666�ցB
	chmod(0666,"$pastfile");
}

###-----------------------------------------------------------------###
# �A�N�Z�X�֎~��

sub access {

print <<_HTML_;

<HTML><HEAD><TITLE>�|�|�|</TITLE></HEAD>
<body bgcolor=#EEFFFF>
<BR><BR><center><H1>�s���ȃA�N�Z�X�ł�</H1><br>
  <font size=+1>�g�b�v�y�[�W�͂�����ł�<BR><br>
  <A HREF=
_HTML_

  print $ref_main . ">" . $ref_main;

print <<_HTML_;
</A></font>
</BODY></HTML>
_HTML_

exit;

}
###-----------------------------------------------------------------###
# ���O�t�@�C��OPEN

sub logpass {


# ���O��ǂݍ���
open(IN,"../team.cgi") || &error("Can't open LogFile");

    while($l = <IN>) {
	$tid = int($l);
	$tname = <IN>;
	chomp($tname);
	$tpass = <IN>;
	chomp($tpass);
	if($FORM{'teamID'} eq $tid && $FORM{'tPASS'} eq $tpass){
	    $logfile = $tid . '.cgi';
	    $title = jcode::sjis($tname) . '�헪��';
	    return;
	}
	$team += 1;
    }
close(IN);

}

