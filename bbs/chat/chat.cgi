#!/usr/local/bin/perl

## PONNY CHAT v3.4 (2000/12/13)
## Copyright(C) Kent Web 2000
## webmaster@kent-web.com
## http://www.kent-web.com/

$ver = 'PONNY v3.4'; # バージョン情報

#--- [注意事項] ------------------------------------------------#
# 1. このスクリプトはフリーソフトです。このスクリプトを使用した	#
#    いかなる損害に対して作者は一切の責任を負いません。		#
# 2. 設置に関する質問はサポート掲示板にお願いいたします。	#
#    直接メールによる質問は一切お受けいたしておりません。	#
#---------------------------------------------------------------#

#============#
#  設定項目  #
#============#

# jcode.pl
require '../../jcode.pl';

# タイトル文字の色
$t_color = "#008040";

# タイトルの大きさ
$t_size = '16pt';

# 本文の文字大きさ
$b_size = '10pt';

# bodyタグ
$body = '<body bgcolor="#F1F1F1" text="#000000">';

# 戻り先のURL (index.htmlなど)
$homepage = '../../../hako/';

# 戦略室(掲示板)
$bbs = '../bbs.cgi';

# 最大記事数
$max = 25;

# 文字色を指定(上下の配列は必ずペアで)
@COLORS = ('0000FF','DF0000','008040','800000','C100C1','FF80C0','FF8040','000080');
@IROIRO = ('青','赤','みどり','茶','紫','ピンク','オレンジ','あい色');

# リロード時間
@retime = (0,30,40,50,60);

# リロード時間（初期値）
$retime = 40;

# コメント間の仕切(<br>=改行 <P>=段落 <hr>=罫線)
$sikiri = '<hr>';

# 入退室時メッセージ
$in_msg  = "さん、いらっしゃい。";	# 入室時
$out_msg = "さん、さようなら～。";	# 退室時

# 入退室案内メッセージの色
$rep_color = "#808080";

# methodの形式(POST/GET)
$method = 'POST';

# スクリプトファイル名
$script  = './chat.cgi';

# ロックファイル
$lockfile = './ponny.lock';

#============#
#  設定完了  #
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
#  フォーム1 : 入室時  #
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
<tr><td><b>おなまえ</b> <input type=text name=name size=20></td></tr>
<tr><td>リロード <select name=retime>
EOM
	$in{'retime'} = $retime;
	foreach (@retime) {
		if ($in{'retime'} == $_) { print "<option value=$_ selected>$_秒\n"; }
		else { print "<option value=$_>$_秒\n"; }
	}
	print "</select> 文字色 <select name=color>\n";
	foreach (0 .. $#COLORS) {
		print "<option value=\"$COLORS[$_]\">$IROIRO[$_]\n";
	}

	print <<"EOM";
</select></td></tr></table>
<table cellpadding=0 cellspacing=0><tr>
<th><input type=submit value="入室する"></th></form>
<th><form action="$homepage" target="_top"><input type=submit value="もどる"></th>
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
#  フォーム2 : 発言部  #
#----------------------#
sub form2 {
	&regist('into');

	# MSIEはフォーム長を調整
   	if ($ENV{'HTTP_USER_AGENT'} =~ /MSIE/i) { $text_width = 90; }
	else { $text_width = 50; }

	# 以下のJavaScript(発言自動消去機能)は「ゆいちゃっと」から移植しました
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
<b>発言</b>：<input type=text size="$text_width" name=comment><br>
リロード <select name=retime>
EOM
	foreach (@retime) {
		if ($in{'retime'} == $_) { print "<option value=$_ selected>$_秒\n"; }
		else { print "<option value=$_>$_秒\n"; }
	}
	print "</select> 文字色 <select name=color>\n";
	foreach (0 .. $#COLORS) {
		if ($in{'color'} eq "$COLORS[$_]") {
			print "<option value=$COLORS[$_] selected>$IROIRO[$_]\n";
		} else {
			print "<option value=$COLORS[$_]>$IROIRO[$_]\n";
		}
	}

	print <<"EOM";
</select>
<input type=submit value="発言／リロード"><input type=reset value="クリア"></form>
<form action="$script" method="$method" target=form>
<table><tr>
<td>
  <input type=submit value="退室する">
  <input type=hidden name=teamID value="$in{'teamID'}">
  <input type=hidden name=tPASS value="$in{'tPASS'}">
  <input type=hidden name=mode value="byebye">
  <input type=hidden name=name value="$in{'name'}">
</td></form>
<td valign=top>
  <form name="cmode">
  <input type="checkbox" name="autoclear" checked>発言自動消去
</td></form></tr></table>
</body></html>
EOM
	exit;
}

#------------#
#  記事表示  #
#------------#
sub log_view {
	if ($in{'retime'} eq "") { $in{'retime'} = $retime; }
	&header;
	if ($in{'retime'} != 0) {
		print "<META HTTP-EQUIV=\"refresh\" CONTENT=\"$in{'retime'}; URL=$script?retime=$in{'retime'}&teamID=$in{'teamID'}&tPASS=$in{'tPASS'}\">\n";
	}
	print "</head>\n$body\n";
	print "<TABLE WIDTH=100%><TR><TD><A HREF=$bbs?teamID=$in{'teamID'}&tPASS=$in{'tPASS'} target=_top>戦略室</A>\n";
	print "</TD><TD align=right>リロード設定：";
	if ($in{'retime'} == 0) { print "手動"; } else { print "$in{'retime'}秒"; }
	print "</TD></TR></TABLE><hr>\n";

	open(IN,"$logfile") || &error("Open Error : $logfile");
	while (<IN>) {
		($date,$name,$com,$color) = split(/<>/);
		print "<font color=\"$color\"><b>$name</b> ＞ $com</font> ($date)$sikiri\n";
	}
	close(IN);

	# 著作権を表示（削除不可）
	print "<center><small><!-- $ver -->\n";
	print "- <a href='http://www.kent-web.com/' target='_top'>Ponny Chat</a> -\n";
    print "<BR>Edit:<a href=\"http://espion.s7.xrea.com/\" target='_top'>Web note</a> -\n";
	print "</small></center>\n</body></html>\n";
	exit;
}

#----------------#
#  ログ書込処理  #
#----------------#
sub regist {
	# 日時の取得
	($sec,$min,$hour,$mday,$mon) = localtime(time);
	$date = sprintf("%02d/%02d-%02d:%02d:%02d",$mon+1,$mday,$hour,$min,$sec);

	# ログ形態を判断
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

	# ロック開始
	&lock;

	open(IN,"$logfile") || &error("Open Error : $logfile");
	@lines = <IN>;
	close(IN);

	# 更新処理
	while ($max <= @lines) { pop(@lines); }
	unshift (@lines,"$date<>$name<>$in{'comment'}<>$color<>$ENV{'REMOTE_ADDR'}\n");
	open(OUT,">$logfile") || &error("Write Error : $logfile");
	print OUT @lines;
	close(OUT);

	# ロック解除
	unlink($lockfile) if (-e $lockfile);

}

#----------------#
#  デコード処理  #
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

		# 文字コードをシフトJIS変換
		&jcode'convert(*value,'sjis');

		# 改行は削除
		$value =~ s/\r//g;
		$value =~ s/\n//g;

		$value =~ s/</&lt;/g; $value =~ s/>/&gt;/g;

		$in{$name} = $value;
	}
	if ($in{'name'} eq "") { $in{'name'} = "名無しのゴンベエ"; }
}

#------------#
#  退室処理  #
#------------#
sub byebye {
	&regist('bye');
	&header('body');
	print <<"EOM";
<center><h3>$in{'name'}さん、ご利用ありがとうございました</h3>
[<a href="$bbs?teamID=$in{'teamID'}&tPASS=$in{'tPASS'}" target="_top">戦略室へもどる</a>]　　
[<a href="$homepage" target="_top">トップへもどる</a>]

</center>
</body></html>
EOM
	exit;
}

#--------------#
#  エラー処理  #
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
#  HTMLヘッダ  #
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
#  ロックファイル処理  #
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
#  トップ表示  #
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
<h3>フレーム非対応のブラウザの方はご利用できません</h3>
</body></noframes>
</frameset>
</html>


_HTML_

exit;

}

#----------------#
#  ログファイル  #
#----------------#
sub logpass {
	my($i) = 0;

	# ログを読み込み
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

		    $title = jcode::sjis($tname) . '戦略会議室';
			last;
		}
    }
	close(IN);
	if(!$logfile) {
		&error2();
	}
}

#---------------#
#  エラー処理2  #
#---------------#
sub error2 {
	unlink($lockfile) if (-e $lockfile);

	&header('body') if (!$head_flag);
	print<<_HTML_;

<center><hr width='70%'><h3>ERROR !</h3>
<font color=red><B>
ターン更新した可\能\性がありますので、<BR>
お手数ですが開発画面より入りなおして下さい。<BR>
</B>
</font>
<P><hr width='70%'>
</center>
</body>
</html>

_HTML_

	exit;
}

