#!/usr/local/bin/perl

## Petit Board v4.5 (00/04/02) 
## Copyright(C) KENT-WEB 1997-2000
## webmaster@kent-web.com
## http://www.kent-web.com/

$ver = 'PETIT v4.5'; # バージョン情報

## ---[注意事項]------------------------------------------------------
## 1. このスクリプトはフリーソフトです。このスクリプトを使用した
##    いかなる損害に対して作者は一切の責任を負いません。
## 2. 設置に関する質問はサポート掲示板にお願いいたします。直接メール
##    による質問は固くお断りいたします。
## 3. 同梱の「家アイコン (home.gif) 」は、「牛飼いとアイコンの部屋 
##    (http://www.ushikai.com/)」によるもので、作者の合意の元に再配布
##    するものです。
## -------------------------------------------------------------------

#============#
#  設定項目  #
#============#

# jcode.plが同一ディレクトリにある場合
require '../jcode.pl';

# タイトル名
$title = "戦略室";

# タイトル文字の色
$t_color = "#DD0000";

# タイトル文字の大きさ(font size)
$t_size  = 6;

# タイトル文字のフォントタイプ
$t_face  = "ＭＳ Ｐゴシック";

# 壁紙を仕様する場合（http://から指定）
$backgif = "";

# 背景色を指定
$bgcolor = "#E1F0F0";

# 文字色を指定
$text = "#000000";

# リンク色を指定
$link  = "#0000FF";	# 未訪問
$vlink = "#800080";	# 訪問済
$alink = "#FF0000";	# 訪問中


# 戻り先のURL (index.htmlなど)
$homepage = "../../../hako";

# 箱庭のURL
$hakopage = "../hako-main.cgi";

# 親記事最大記事数 (あまり多くすると危険)
#  --> レス記事の数は最大記事数には含まれません
$max = 50;

# 管理者用マスタパスワード(英数字)
$pass = 'password';

# アイコン画像のある「ディレクトリ」
#  --> petit.cgi と別ディレクトリとなる場合は、http://から記述する。
$icon_dir = ".";

# 返信がつくと親記事をトップへ移動 (0=no 1=yes)
$res_sort = 0;

# ホスト名取得モード
#  --> 0 : $ENV{'REMOTE_HOST'} で取得できる場合
#  --> 1 : gethostbyaddr で取得できる場合
$get_remotehost = 0;

# タイトルにGIF画像を使用する時 (http://から記述)
$title_gif = "";
$tg_w = '150';		# GIF画像の幅(ピクセル)
$tg_h = '50';		#   〃     高さ(ピクセル)

# ファイルロック形式
#  --> 0=no 1=symlink関数 2=open関数
#  --> 1 or 2 を設定する場合は、ロックファイルを生成するディレクトリ
#      のパーミッションは 777 に設定する。
$lockkey = 0;

# ロックファイル名
$lockfile = "./petit.lock";

# カウンタのロックファイル名
$cntlock = "./ptcnt.lock";

# ミニカウンタの設置
#  --> 0=no 1=テキスト 2=GIF画像
$counter = 0;
$mini_fig = 5;			# ミニカウンタの桁数
$cnt_color = "#dd0000";		# テキストのとき：ミニカウンタの色
$gif_path = ".";		# ＧＩＦのとき　：画像までのディレクトリ
$mini_w = 8;			#       〃    　：画像の横サイズ
$mini_h = 12;			#       〃    　：画像の縦サイズ
$cntfile = "./count.dat";	# カウンタファイル

# タグの許可 (0=no 1=yes)
$tagkey = 0;

# スクリプトファイル
$script  = "./bbs.cgi";

# ログファイルを指定
#  --> フルパスで指定する場合は / から始まるフルパスで。
#$logfile = "./petit.cgi";

# 日付のタイプ (0=洋式 1=和式)
$date_type = 0;

# 記事の [タイトル] 部の色
$sbj_color = "#006400";

# 記事表示部の下地の色
$tbl_color = "#FFFFFF";

# 家アイコンの使用 (0=no 1=yes)
$home_icon = 0;
$home_gif = "home.gif";	# 家アイコンのファイル名
$home_wid = 25;		# 画像の横サイズ
$home_hei = 22;		#   〃  縦サイズ

# methodの形式 (POST/GET)
$method = 'POST';

# １ページ当たりの記事表示数 (親記事)
$pagelog = 15;

# 投稿があるとメール通知する (0=no 1=yes)
#  --> sendmail必須
$mailing = 0;

# メールアドレス(メール通知する時)
$mailto = 'foo@host.ne.jp';

# sendmailパス（メール通知する時）
$sendmail = '/usr/lib/sendmail';

# 自分の記事はメール送信する (0=no 1=yes)
$mail_me = 0;

# 他サイトから投稿排除する時に指定 (http://から書く)
$base_url = "";

# 文字色の設定。上下の配列は必ずペアで。
@COLORS = ('000000','800000','DF0000','008040','0000FF','C100C1','FF80C0','FF8040','000080');
@IROIRO = ('黒','茶','赤','みどり','青','紫','ピンク','オレンジ','あい色');

# 改行形式 (手動=soft 強制=hard)
$wrap = 'soft';

# URLの自動リンク (0=no 1=yes)
#  --> タグ許可の場合は no とすること。
$autolink = 0;

# タグ広告挿入オプション (FreeWebなど）
#   → <!--上部--> <!--下部--> の代わりに「広告タグ」を挿入する。
#   → 広告タグ以外に、MIDIタグ や LimeCounter等のタグにも使用可能です。
$banner1 = '<!--上部-->'; # 掲示板上部に挿入
$banner2 = '<!--下部-->'; # 掲示板下部に挿入

# 過去ログ生成 (0=no 1=yes)
$pastkey = 0;
$nofile  = "./pastno.dat";	# 過去ログ用NOファイル
$past_dir = ".";		# 過去ログのディレクトリ
$log_line = '150';		# 過去ログ１ファイルの行数
$petit2 = "./petit2.cgi";	# 過去ログ管理ファイル

#============#
#  設定完了  #
#============#

#$ref_main = 'http://www.elsia.com/com/hako';
#$ref_page = 'http://www.elsia.com/com/tyotou';

#$page = $ENV{'HTTP_REFERER'};
#$page =~ tr/+/ /;
#$page =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
#if (!($page =~ /$ref_page/i)) { &access; }

# メイン処理
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
#  記事表示部  #
#--------------#
sub html_log {
	# クッキーを取得
	&get_cookie;

	# フォーム長を調整
	&get_bros;

	# ログを読み込み
	open(IN,"$logfile") || &error("Can't open $logfile");
	@lines = <IN>;
	close(IN);

	# 記事番号をカット
	shift(@lines);

	# 親記事のみの配列データを作成
	@new = ();
	foreach $line (@lines) {
		local($num,$k,$date,$name,$email,
			$subj,$com,$url,$host,$pw,$color) = split(/<>/,$line);
		# 親記事を集約
		if ($k eq "") { push(@new,$line); }
	}

	# レス記事はレス順につけるため配列を逆順にする
	@lines = reverse(@lines);

	# ヘッダを出力
	&header;

	# カウンタ処理
	if ($counter) { &counter; }

	print "<center>$banner1<P>\n";

	# タイトル部
	if ($title_gif eq '') {
		print "<font color=$t_color size=$t_size face=\"$t_face\">";
		print "<b>$title</b></font>\n";
	} else {
		print "<img src=\"$title_gif\" width=\"$tg_w\" height=\"$tg_h\">\n";
	}

	print "<hr width=90%>\n";
	print "[<a href=\"$homepage\" target='_top'>トップにもどる</a>]\n";
	print "[<a href=\"$hakopage\" target='_top'>箱庭にもどる</a>]\n";
	print "[<a href=\"$script?mode=howto&teamID=$tid&tPASS=$tpass\">使い方</a>]\n";
	print "[<a href=\"$script?mode=find&teamID=$tid&tPASS=$tpass\">ワード検索</a>]\n";

	if ($pastkey) {
		print "[<a href=\"$petit2\">過去ログ</a>]\n";
	}

	print <<"EOM";
[<a href="$script?teamID=$tid&tPASS=$tpass&mode=msg_del">記事削除</a>]
[<a href="${script}?teamID=$tid&tPASS=$tpass&mode=admin">管理用</a>]
<hr width="90%">
<BR><FONT SIZE=+2>
<A HREF="chat/chat.cgi?teamID=$tid&tPASS=$tpass&mode=top">会議室(チャット)</A>
</FONT>
</center>
<form method="$method" action="$script">
<input type=hidden name=teamID value="$tid">
<input type=hidden name=tPASS value="$tpass">
<input type=hidden name=mode value="msg">
<blockquote>
<table border=0 cellspacing=0>
<tr>
  <td nowrap><b>おなまえ</b></td>
  <td>
    <input type=text name=name size="$nam_wid" value="$c_name">
  </td>
</tr>
<tr>
  <td nowrap><b>Ｅメール</b></td>
  <td>
    <input type=text name=email size="$nam_wid" value="$c_email">
  </td>
</tr>
<tr>
  <td nowrap><b>題　　名</b></td>
  <td>
    <input type=text name=subj size="$subj_wid">
　  <input type=submit value="投稿する"><input type=reset value="リセット">
  </td>
</tr>
<tr>
  <td colspan=2>
    <b>コメント</b><br>
    <textarea cols="$com_wid" rows=7 name=comment wrap="$wrap"></textarea>
  </td>
</tr>

<tr>
  <td nowrap><b>削除キー</b></td>
  <td>
    <input type=password name=pwd size=8 maxlength=8 value="$c_pwd">
    <small>(自分の記事を削除時に使用。英数字で8文字以内)</small>
  </td>
</tr>
<tr>
  <td nowrap>
    <b>文字色</b>
  </td>
  <td>
EOM

	if ($c_color eq "") { $c_color = "$COLORS[0]"; }
	foreach (@COLORS) {
		if ($c_color eq "$_") {
			print "<input type=radio name=color value=\"$_\" checked>";
			print "<font color=$_>■</font>\n";
		} else {
			print "<input type=radio name=color value=\"$_\">";
			print "<font color=$_>■</font>\n";
		}
	}

	print "</td></tr></table></form></blockquote><hr>\n";

	if ($FORM{'page'} eq '') { $page = 0; } 
	else { $page = $FORM{'page'}; }

	# 記事数を取得
	$end_data = @new - 1;
	$page_end = $page + ($pagelog - 1);

	if ($page_end >= $end_data) { $page_end = $end_data; }
	foreach ($page .. $page_end) {
		($num,$k,$date,$name,$email,$sbj,
			$com,$url,$host,$pwd,$color) = split(/<>/, $new[$_]);

		if ($email) { $name = "<a href=mailto\:$email>$name</a>"; }
		if (!$sbj) { $sbj = "Untitled"; }

		# URL表示
		if ($url && $home_icon) {
			$url = "<a href=\"http://$url\" target=_top><img src=\"$icon_dir\/$home_gif\" border=0 align=top HSPACE=10 WIDTH=\"$home_wid\" HEIGHT=\"$home_hei\"></a>";

		} elsif ($url && $home_icon == 0) {
			$url = "<small>[<a href=\"http://$url\" target=_top>HOME</a>]</small>";
		}

		# 自動リンク
		if ($autolink) { &auto_link($com); }

		print "<center><table border=1 width=95% cellpadding=5 cellspacing=0 bgcolor=$tbl_color>\n";
		print "<tr><td>\n";
		print "<table border=0 cellspacing=0><tr>\n";
		print "<td>[<b>$num</b>] <font color=$sbj_color><b>$sbj</b></font></td>\n";
		print "<td width=10></td><td>投稿者：<font color=$link><b>$name</b></font></td>\n";
		print "<td><small>投稿日：$date</small></td><td>$url</td></tr></table>\n";
		print "<blockquote><font color=\"$color\">$com</font></blockquote>\n";

		## レスメッセージを表示
		$flag = 0;
		foreach $line (@lines) {
			($rnum,$rk,$rd,$rname,$rem,
				$rsub,$rcom,$rurl,$rho,$rp,$rc) = split(/<>/, $line);

			if ($num eq "$rk") {
				if ($flag == 0) { print "<P><hr width=95% size=1>\n"; $flag=1; }

				# 自動リンク
				if ($autolink) { &auto_link($rcom); }

				print "<table border=0 width=100% cellspacing=0><tr>\n";
				print "<td><font color=$rc><b>$rname</b> ＞ $rcom ";
				print "<small>($rd)</small></font></td></tr></table>\n";
			}
		}

		print "</td></tr></table>\n";
		print "<form action=\"$script\" method=$method>\n";
		print "<input type=hidden name=teamID value=\"$tid\">\n";
		print "<input type=hidden name=tPASS value=\"$tpass\">\n";
		print "<a href=./bbs.cgi?teamID=$tid&tPASS=$tpass>リロード</a>\n";
		print "<input type=hidden name=mode value=\"msg\">\n";
		print "<input type=hidden name=resno value=\"$num\">\n";
		print "<input type=hidden name=page value=\"$FORM{'page'}\">\n";
		print "<input type=hidden name=email value=\"$c_email\">\n";
		print "<input type=hidden name=url value=\"$c_url\">\n";

		print "名前<input type=text name=name size=$nam_wid2 value=\"$c_name\">\n";
		print "レス<input type=text name=comment size=$subj_wid>\n";
		print "文字色<select name=color>\n";

		foreach (0 .. $#COLORS) {
			if ($c_color eq "$COLORS[$_]") {
				print "<option value=\"$COLORS[$_]\" selected>$IROIRO[$_]\n";
			} else {
				print "<option value=\"$COLORS[$_]\">$IROIRO[$_]\n";
			}
		}

		print "</select> 削除キー<input type=password name=pwd size=4 value=\"$c_pwd\">\n";
		print "<input type=submit value=\"返信する\"></form></center><hr>\n";
	}

	print "<table border=0><tr>\n";

	# 改頁処理
	$next_line = $page_end + 1;
	$back_line = $page - $pagelog;

	# 前頁処理
	if ($back_line >= 0) {
		print "<td><form method=\"$method\" action=\"$script\">\n";
		print "<input type=hidden name=teamID value=\"$tid\">\n";
		print "<input type=hidden name=tPASS value=\"$tpass\">\n";
		print "<input type=hidden name=page value=\"$back_line\">\n";
		print "<input type=hidden name=mode value=\"page\">\n";
		print "<input type=submit value=\"前の$pagelog件\">\n";
		print "</form></td>\n";	
	}

	# 次頁処理
	if ($page_end ne $end_data) {
		print "<td><form method=\"$method\" action=\"$script\">\n";
		print "<input type=hidden name=teamID value=\"$tid\">\n";
		print "<input type=hidden name=tPASS value=\"$tpass\">\n";
		print "<input type=hidden name=page value=\"$next_line\">\n";
		print "<input type=hidden name=mode value=\"page\">\n";
		print "<input type=submit value=\"次の$pagelog件\">\n";
		print "</form></td>\n";
	}

	print "</tr></table>\n";
	&footer;
	exit;
}

#--------------------#
#  ログ書き込み処理  #
#--------------------#
sub regist {
	# 他サイトからのアクセスを排除
	if ($base_url) {
		$ref_url = $ENV{'HTTP_REFERER'};
		$ref_url =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		if ($ref_url !~ /$base_url/i) { &error("不正なアクセスです"); }
	}

	# 名前とコメントは必須
	if ($name eq "") { &error("名前が入力されていません"); }
	if ($comment eq "") { &error("コメントが入力されていません"); }
	if ($email && $email !~ /(.*)\@(.*)\.(.*)/) {
		&error("Ｅメールの入力内容が正しくありません");
	}

	# ホスト名を取得
	&get_host;

	# ファイルロック
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }

	# ログを開く
	open(IN,"$logfile") || &error("Can't open $logfile");
	@lines = <IN>;
	close(IN);

	# 親記事NO処理
	$oya = $lines[0];
	if ($oya =~ /<>/) {
		&error("ログが正しくありません。<P>
			(v2.5以前のログの場合は変換の必要があります)");
	}
	$oya =~ s/\n//;
	shift(@lines);

	# 二重投稿の禁止
	local($flag) = 0;
	foreach $line (@lines) {
		($knum,$kk,$kd,$kname,$kem,$ksub,$kcom) = split(/<>/,$line);
		if ($name eq "$kname" && $comment eq "$kcom") {
			$flag=1; last;
		}
	}
	if ($flag) { &error("二重投稿は禁止です"); }

	# 親記事の場合、記事Noをカウントアップし、クッキーを発行
	if ($FORM{'resno'} eq "") { $oya++; }
	&set_cookie;
	$number = $oya;

	# 削除キーを暗号化
	if ($pwd) { $ango = &passwd_encode($pwd); }

	# 時間を取得
	&get_time;

	# ログをフォーマット
	$new_msg = "$number<>$FORM{'resno'}<>$date<>$name<>$email<>$subj<>$comment<>$url<>$host<>$ango<>$color<>\n";

	## 自動ソート時は、レス記事投稿時は親記事はトップへ移動
	if ($res_sort && $FORM{'resno'} ne "") {
		@res_data = ();
		@new = ();
		foreach $line (@lines) {
		  $flag = 0;
		  ($num,$k,$d,$na,$em,$sub,$com,$u,$ho,$p,$c,$ico) = split(/<>/,$line);

		  # 親記事を抜き出す
		  if ($k eq "" && $FORM{'resno'} eq "$num") {
			$new_line = "$line";
			$flag = 1;
		  }
		  # 関連のレス記事を抜き出す
		  elsif ($k eq "$FORM{'resno'}") {
			push(@res_data,$line);
			$flag = 1;
		  }
		  if ($flag == 0) { push(@new,$line); }
		}

		# 関連レス記事をトップへ
		unshift(@new,@res_data);

		# 新規メッセージをトップへ
		unshift(@new,$new_msg);

		# 親記事をトップへ
		unshift(@new,$new_line);

	## 親記事の場合、最大記事数を超える記事をカット
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

		## 過去記事生成
		if ($kflag) {
			@past_res = reverse(@past_res);
			push(@past_data,@past_res);
			&pastlog;
		}

		unshift(@new,$new_msg);

	## レス記事は記事数の調整はしない
	} else {
		@res_data = ();
		@new = ();

		foreach $line (@lines) {
		  $flag = 0;
		  ($num,$k,$d,$na,$em,$sub,$com,$u,$ho,$p,$c,$ico) = split(/<>/,$line);

		  # 親記事を抜き出す
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

	# 親記事NOを付加
	unshift (@new,"$oya\n");

	# ログを更新
	open(OUT,">$logfile") || &error("Can't write $logfile");
	print OUT @new;
	close(OUT);

	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }

	# メール処理
	if ($mailing && $mail_me) { &mail_to; }
	elsif ($mailing && $mail_me == 0 && $email ne "$mailto") { &mail_to; }
}

#---------------#
#  デコード処理 #
#---------------#
sub decode {
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		if ($ENV{'CONTENT_LENGTH'} > 51200) { &error("投稿量が大きすぎます"); }
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	} else { $buffer = $ENV{'QUERY_STRING'}; }

	@pairs = split(/&/,$buffer);
	foreach $pair (@pairs) {
		($name, $value) = split(/=/, $pair);
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

		# 文字コード変換
		&jcode'convert(*value,'sjis');

		# タグ処理
		if ($tagkey == 0) {
			$value =~ s/</&lt\;/g;
			$value =~ s/>/&gt\;/g;
		} else {
			$value =~ s/<!--(.|\n)*-->//g;
			$value =~ s/<>/&lt\;&gt\;/g;
		}

		# 一括削除用
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
#  掲示板の使い方メッセージ  #
#----------------------------#
sub howto {
	if ($tagkey == 0) { $tag_msg = "投稿内容には、<b>タグは一切使用できません。</b>\n"; }
	else { $tag_msg = "コメント欄には、<b>タグ使用をすることができます。</b>\n"; }

	&header;
	print <<"HTML";
[<a href="$script?teamID=$tid&tPASS=$tpass\">掲示板にもどる</a>]
<table width="100%"><tr><th bgcolor="#0000A0">
<font color="#FFFFFF">掲示板の利用上の注意</font>
</th></tr></table>
<P><center>
<table width=90% border=1 cellpadding=10>
<tr><td bgcolor="$tbl_color">
<OL>
<LI>この掲示板は<b>クッキー対応</b>です。１度記事を投稿いただくと、おなまえ、Ｅメール、ＵＲＬ、削除キーの情報は２回目以降は自動入力されます。（ただし利用者のブラウザがクッキー対応の場合）<P>
<LI>$tag_msg<P>
<LI>記事を投稿する上での必須入力項目は<b>「おなまえ」</b>と<b>「メッセージ」</b>です。Ｅメール、ＵＲＬ、題名、削除キーは任意です。<P>
<LI>記事には、<b>半角カナは一切使用しないで下さい。</b>文字化けの原因となります。<P>
<LI>記事の投稿時に<b>「削除キー」</b>にパスワード（英数字で8文字以内）を入れておくと、その記事は次回<b>削除キー</b>によって削除することができます。<P>
<LI>記事の保持件数は<b>最大 $max件</b>です。それを超えると古い順に自動削除されます。<P>
<LI>既存の記事に<b>「１行レス」</b>を付けることができます。記事表\示欄下部にある返信用フォームから記事を投稿することができます。<P>
<LI>過去の投稿記事から<b>「キーワード」によって簡易検索ができます。</b>トップメニューの<a href="$script?mode=find&teamID=$tid&tPASS=$tpass">「ワード検索」</a>のリンクをクリックすると検索モードとなります。<P>
<LI>管理者が著しく不利益と判断する記事や他人を誹謗中傷する記事は\予\告\なく削除することがあります。
</OL>
</td></tr></table>
</center><hr>
HTML
	&footer;
	exit;
}

#--------------------------#
#  ワード検索サブルーチン  #
#--------------------------#
sub find {
	&header;
	print <<"HTML";
[<a href="$script?teamID=$tid&tPASS=$tpass">掲示板にもどる</a>]
<table width="100%"><tr><th bgcolor="#0000A0">
<font color="#FFFFFF">ワード検索</font></th></tr></table>
<P><center>
<table cellpadding=5>
<tr><td bgcolor="$tbl_color" nowrap>
  <UL>
  <LI>検索したい<b>キーワード</b>を入力し、検索領域を選択して「検索ボタン」
      を押してください。
  <LI>キーワードを「半角スペース」で区切って複数指定することができます。
  </UL>
</td></tr></table><P>
<form action="$script" method="$method">
<input type=hidden name=teamID value="$tid">
<input type=hidden name=tPASS value="$tpass">
<input type=hidden name=mode value="find">
<table border=1>
<tr>
  <th colspan=2>キーワード <input type=text name=word size=30></th>
</tr>
<tr>
  <td>検索条件</td>
  <td>
    <input type=radio name=cond value="and" checked>AND
    <input type=radio name=cond value="or">OR
  </td>
</tr>
<tr>
  <th colspan=2>
    <input type=submit value="検索する"><input type=reset value="リセット">
  </th>
</tr>
</table>
</form>
</center>
HTML
	# ワード検索の実行と結果表示
	if ($FORM{'word'} ne "") {

		# 入力内容を整理
		$cond = $FORM{'cond'};
		$word = $FORM{'word'};
		$word =~ s/　/ /g;
		$word =~ s/\t/ /g;
		@pairs = split(/ /,$word);

		# ファイルを読み込み
		open(DB,"$logfile") || &error("Can't open $logfile");
		@lines = <DB>;
		close(DB);

		# 検索処理
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

		# 検索終了
		$count = @new;
		print "<hr><b><font color=$t_color>検索結果：$count件</font></b><P>\n";
		print "<OL>\n";

		foreach $line (@new) {
			($num,$k,$date,$name,$email,$sub,$com,$url) = split(/<>/, $line);
			if (!$sub) { $sub = "Untitled"; }
			if ($email) { $name = "<a href=mailto\:$email>$name</a>"; }
			if ($url) { $url = "[<a href=\"http://$url\" target=_top>HOME</a>]"; }

			if ($k) { $num = "$kへのレス"; }

			# 結果を表示
			print "<LI>[$num] <font color=$sbj_color><b>$sub</b></font>\n";
			print "投稿者：<b>$name</b> <small>$url 投稿日：$date</small><P>\n";
			print "<blockquote>$com</blockquote><hr size=2>\n";
		}

		print "</OL><P>\n";
	}
	&footer;
	exit;
}

#--------------#
#  日時の取得  #
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

	# 日時のフォーマット
	if ($date_type && $FORM{'resno'} eq "") {
		$youbi = ('日','月','火','水','木','金','土') [$wday];
		$date = "$year年$mon月$mday日 ($youbi) $hour時$min分$sec秒";
	} else {
		$youbi = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat') [$wday];
		$date = "$year/$mon/$mday($youbi) $hour\:$min\:$sec";
	}
}

#------------------------------------#
#  ブラウザを判断しフォーム幅を調整  #
#------------------------------------#
sub get_bros {
	# ブラウザ名を取得
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
#  削除画面  #
#------------#
sub msg_del {
	if ($FORM{'action'} eq 'admin' && $FORM{'pass'} ne "$pass") {
		&error("パスワードが違います");
	}

	open(DB,$logfile) || &error("Can't open $logfile");
	@lines = <DB>;
	close(DB);

	shift(@lines);

	# 親記事のみの配列データを作成
	@new = ();
	foreach $line (@lines) {
		local($num,$k,$date,$name,
			$email,$sub,$com,$url,$host,$pw) = split(/<>/,$line);

		# RES記事を外す
		if ($k eq "") { push(@new,$line); }
	}

	@lines = reverse(@lines);

	&header;
	print "[<a href=\"$script?teamID=$tid&tPASS=$tpass\">掲示板へ戻る</a>]\n";
	print "<table width=100%><tr><th bgcolor=\"#0000A0\">\n";
	print "<font color=\"#FFFFFF\">コメント削除画面</font></th></tr></table>\n";
	print "<P><center>\n";
	print "<table border=0 cellpadding=5><tr>\n";
	print "<td bgcolor=\"$tbl_color\">\n";

	if ($FORM{'action'} eq '') {
		print "■投稿時に記入した「削除キー」により、記事を削除します。<br>\n";
	}

	print "■削除したい記事のチェックボックスにチェックを入れ、下記フォームに「削除キー」を入力してください。<br>\n";
	print "■親記事を削除する場合、そのレスメッセージも同時に消滅してしまうことになりますので、ご注意ください。<br>\n";
	print "</td></tr></table><P>\n";
	print "<form action=\"$script\" method=$method>\n";

	if ($FORM{'action'} eq '') {
		print "<input type=hidden name=mode value=\"usr_del\">\n";
		print "<b>削除キー</b> <input type=text name=del_key size=10>\n";
	} else {
		print "<input type=hidden name=mode value=\"admin_del\">\n";
		print "<input type=hidden name=action value=\"admin\">\n";
		print "<input type=hidden name=pass value=\"$FORM{'pass'}\">\n";
	}
	print "<input type=hidden name=teamID value=\"$tid\">\n";
	print "<input type=hidden name=tPASS value=\"$tpass\">\n";
	print "<input type=submit value=\"削除する\"><input type=reset value=\"リセット\">\n";
	print "<P><table border=1>\n";
	print "<tr><th>削除</th><th>記事No</th><th>題名</th><th>投稿者</th>";
	print "<th>投稿日</th><th>コメント</th>\n";

	if ($FORM{'action'} eq 'admin') { print "<th>ホスト名</th>\n"; }

	print "</tr>\n";

	if ($FORM{'page'} eq '') { $page = 0; }
	else { $page = $FORM{'page'}; }

	# 記事数を取得
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

		## レスメッセージを表示
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

				print "<td colspan=2 align=center><b>$num</b>へのレス</td>\n";
				print "<td>$rname</td><td><small>$rd</small></td><td>$rcom</td>\n";

				if ($FORM{'action'} eq 'admin') { print "<td>$rho</td>\n"; }

				print "</tr>\n";
			}
		}
	}
	print "</table></form>\n";
	print "<table border=0 width=100%><tr>\n";

	# 改頁処理
	$next_line = $page_end + 1;
	$back_line = $page - $pagelog;

	# 前頁処理
	if ($back_line >= 0) {
		print "<td><form method=\"$method\" action=\"$script\">\n";
		print "<input type=hidden name=teamID value=\"$tid\">\n";
		print "<input type=hidden name=tPASS value=\"$tpass\">\n";
		print "<input type=hidden name=page value=\"$back_line\">\n";
		print "<input type=hidden name=mode value=msg_del>\n";
		print "<input type=submit value=\"前の親記事$pagelog件\">\n";

		if ($FORM{'action'} eq 'admin') {
		  print "<input type=hidden name=action value=\"admin\">\n";
		  print "<input type=hidden name=pass value=\"$FORM{'pass'}\">\n";
		}

		print "</form></td>\n";	
	}

	# 次頁処理
	if ($page_end ne $end_data) {
		print "<td><form method=\"$method\" action=\"$script\">\n";
		print "<input type=hidden name=teamID value=\"$tid\">\n";
		print "<input type=hidden name=tPASS value=\"$tpass\">\n";
		print "<input type=hidden name=page value=\"$next_line\">\n";
		print "<input type=hidden name=mode value=msg_del>\n";
		print "<input type=submit value=\"次の親記事$pagelog件\">\n";

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

## --- ユーザ記事削除処理
sub usr_del {
	if ($FORM{'del_key'} eq "") { &error("削除キーが入力モレです。"); }
	if ($FORM{'del'} eq "") { &error("ラジオボタンの選択がありません。"); }

	# ロック開始
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }

	# ログを読み込む
	open(DB,"$logfile") || &error("Can't open $logfile");
	@lines = <DB>;
	close(DB);

	# 親記事NO
	$oya = $lines[0];
	if ($oya =~ /<>/) {
		&error("ログが正しくありません。<P><small>\(v2.5以前のログの場合は変換の必要があります\)<\/small>");
	}

	shift(@lines);

	## 削除キーによる記事削除 ##
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

	if ($del_num eq '') { &error("削除対象記事が見つかりません"); }
	else {
		if ($encode_pwd eq '') { &error("削除キーが設定されていません"); }
		$check = &passwd_decode("$FORM{'del_key'}","$encode_pwd");
		if ($check ne 'yes') { &error("パスワードが違います"); }
	}

	# 親記事NOを付加
	unshift(@new,$oya);

	## ログを更新 ##
	open(DB,">$logfile") || &error("Can't write $logfile");
	print DB @new;
	close(DB);

	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }

	# 削除画面にもどる
	&msg_del;
}

#----------------------#
#  管理者一括記事削除  #
#----------------------#
sub admin_del {
	if ($FORM{'pass'} ne "$pass") { &error("パスワードが違います"); }
	if ($FORM{'del'} eq "") { &error("チェックボックスの選択がありません"); }

	# ロック開始
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }

	# ログを読み込む
	open(DB,"$logfile") || &error("Can't open $logfile");
	@lines = <DB>;
	close(DB);

	# 親記事NO
	$oya = $lines[0];
	if ($oya =~ /<>/) {
		&error("ログが正しくありません。<P><small>\(v2.5以前のログの場合は変換の必要があります\)<\/small>");
	}

	shift(@lines);

	## 削除処理
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

	# 親記事NOを付加
	unshift(@new,$oya);

	## ログを更新 ##
	open(DB,">$logfile") || &error("Can't write $logfile");
	print DB @new;
	close(DB);

	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }

	# 削除画面にもどる
	&msg_del;
}

## --- 管理者入室画面
sub admin {
	&header;
	print "<center><h4>パスワードを入力してください</h4>\n";
	print "<form action=\"$script\" method=$method>\n";
	print "<input type=hidden name=teamID value=\"$tid\">\n";
	print "<input type=hidden name=tPASS value=\"$tpass\">\n";
	print "<input type=hidden name=mode value=\"msg_del\">\n";
	print "<input type=hidden name=action value=\"admin\">\n";
	print "<input type=password name=pass size=8><input type=submit value='認証'>\n";
	print "</form></center>\n";
	print "</body></html>\n";
	exit;
}

## --- カウンタ処理
sub counter {
	# 閲覧時のみカウントアップ
	$match=0;
	if ($FORM{'mode'} eq '') {
		# カウンタロック
		if ($lockkey) { &lock3; }

		$match=1;
	}

	# カウントファイルを読みこみ
	open(NO,"$cntfile") || &error("Can't open $cntfile",'0');
	$cnt = <NO>;
	close(NO);

	# カウントアップ
	if ($match) { $cnt++; }

	# 更新
	open(OUT,">$cntfile") || &error("Write Error : $cntfile");
	print OUT $cnt;
	close(OUT);

	# カウンタロック解除
	if (-e $cntlock) { unlink($cntlock); }

	# 桁数調整
	while(length($cnt) < $mini_fig) { $cnt = '0' . "$cnt"; }
	@cnts = split(//,$cnt);

	print "<table><tr><td>\n";

	# GIFカウンタ表示
	if ($counter == 2) {
		foreach (0 .. $#cnts) {
			print "<img src=\"$gif_path/$cnts[$_]\.gif\" alt=\"$cnts[$_]\" width=\"$mini_w\" height=\"$mini_h\">";
		}

	# テキストカウンタ表示
	} else {
		print "<font color=\"$cnt_color\" face=\"verdana,Times New Roman,Arial\">$cnt</font>";
	}

	print "</td></tr></table>\n";
}

## --- ロックファイル（symlink関数）
sub lock1 {
	local($retry) = 5;
	while (!symlink(".", $lockfile)) {
		if (--$retry <= 0) { &error('LOCK is BUSY'); }
		sleep(1);
	}
}

## --- ロックファイル（open関数）
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

## --- カウンタロック
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

## --- メール送信
sub mail_to {
	$mail_subj = "$title に投稿がありました。";

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

	# メールアドレスがない場合はダミーメールに置き換え
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
#  パスワード暗号処理  #
#----------------------#
sub passwd_encode {
	$inpw = $_[0];
	@SALT = ('a'..'z', 'A'..'Z', '0'..'9', '.', '/');
	srand;
	$salt = $SALT[int(rand(@SALT))] . $SALT[int(rand(@SALT))];
	return crypt($inpw, $salt);
}

#----------------------#
#  パスワード照合処理  #
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
#  自動リンク  #
#--------------#
sub auto_link {
	$_[0] =~ s/([^=^\"]|^)(http\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#]+)/$1<a href=$2 target=_top>$2<\/a>/g;
}

#------------------#
#  HTMLのヘッダー  #
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

## --- HTMLのフッター
sub footer {
	## 著作権表示（削除不可）
	print "<center>$banner2<P><small><!-- $ver -->\n";
	print "- <a href=\"http://www.kent-web.com/\" target='_top'>Petit Board</a> -\n";
	print "<BR>Edit:<a href=\"http://espion.s7.xrea.com/\" target='_top'>Web note</a> -\n";
	print "</small></center>\n";
	print "</body></html>\n";
}

## --- クッキーの発行
sub set_cookie {
	# クッキーは60日間有効
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

## --- クッキーを取得
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

## --- エラー処理
sub error {
	if (-e $lockfile) { unlink($lockfile); }
	if ($_[1] ne '0') { &header; }

	print "<center><hr width=\"75%\"><P><h3>ERROR !</h3>\n";
	print "<P><font color=red><B>$_[0]\n";
	print "<P>＊チームパスワードが変わっている可能\性がありますので、再度開発画面からお入り下さい</B></font>\n";
	print "<P><hr width=\"75%\"></center>\n";
	&footer;
	exit;
}

## --- ホスト名取得
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

## --- 過去ログ生成
sub pastlog {
	$new_flag = 0;

	# 過去NOを開く
	open(NO,"$nofile") || &error("Can't open $nofile");
	$count = <NO>;
	close(NO);

	# 過去ログのファイル名を定義
	$pastfile  = "$past_dir/$count\.html";

	# 過去ログがない場合、新規に自動生成する
	unless(-e $pastfile) { &new_log; }

	# 過去ログを開く
	if ($new_flag == 0) {
		open (IN,"$pastfile") || &error("Can't open $pastfile");
		@past = <IN>;
		close(IN);
	}

	# 規定の行数をオーバーすると、次ファイルを自動生成する
	if ($#past > $log_line) { &next_log; }

	foreach $pst_line (@past_data) {
		($pnum,$pk,$pdt,$pname,$pemail,$psub,$pcom,
			$purl,$phost,$ppw) = split(/<>/, $pst_line);

		if ($pk eq "" && $psub eq "") { $psub = "no title"; }
		if ($pemail) { $pname = "<a href=mailto:$pemail>$pname</a>"; }
		if ($purl) { $purl="<a href=http://$purl target=_top>http://$purl</a>"; }
		if ($pk) { $pnum = "$pkへのレス"; }

		# 自動リンク
		if ($autolink) { &auto_link($pcom); }

		# 保存記事をフォーマット
		$html = <<"HTML";
[$pnum] <font color=$sbj_color><b>$psub</b></font><!--T--> 投稿者：<font color=$link><b>$pname</b></font> <small>投稿日：$pdt</small><p><blockquote>$pcom<p>$purl</blockquote><!--$phost--><hr>
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

	# 過去ログを更新
	open(OUT,">$pastfile") || &error("Can't write $pastfile");
	print OUT @news;
	close(OUT);

}

## --- 過去ログ次ファイル生成ルーチン
sub next_log {
	# 次ファイルのためのカウントアップ
	$count++;

	# カウントファイル更新
	open(NO,">$nofile") || &error("Can't write $nofile");
	print NO "$count";
	close(NO);

	$pastfile  = "$past_dir/$count\.html";

	&new_log;
}

## --- 新規過去ログファイル生成ルーチン
sub new_log {
	$new_flag = 1;

	if ($backgif) { $bgkey = "background=\"$backgif\""; }
	else { $bgkey = "bgcolor=$bgcolor"; }

	$past[0] = "<html><head><title>過去ログ</title></head>\n";
	$past[1] = "<body $bgkey text=$text link=$link vlink=$vlink alink=$alink><hr size=1>\n";
	$past[2] = "<\!--HAJIME-->\n";
	$past[3] = "<\!--OWARI-->\n";
	$past[4] = "</body></html>\n";

	# 新規過去ログファイルを生成更新
	open(OUT,">$pastfile") || &error("Can't write $pastfile");
	print OUT @past;
	close(OUT);

	# パーミッションを666へ。
	chmod(0666,"$pastfile");
}

###-----------------------------------------------------------------###
# アクセス禁止令

sub access {

print <<_HTML_;

<HTML><HEAD><TITLE>－－－</TITLE></HEAD>
<body bgcolor=#EEFFFF>
<BR><BR><center><H1>不正なアクセスです</H1><br>
  <font size=+1>トップページはこちらです<BR><br>
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
# ログファイルOPEN

sub logpass {


# ログを読み込み
open(IN,"../team.cgi") || &error("Can't open LogFile");

    while($l = <IN>) {
	$tid = int($l);
	$tname = <IN>;
	chomp($tname);
	$tpass = <IN>;
	chomp($tpass);
	if($FORM{'teamID'} eq $tid && $FORM{'tPASS'} eq $tpass){
	    $logfile = $tid . '.cgi';
	    $title = jcode::sjis($tname) . '戦略室';
	    return;
	}
	$team += 1;
    }
close(IN);

}

