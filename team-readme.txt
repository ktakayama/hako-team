┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓

　箱庭チームトーナメント readme -2005/12/22更新-
　　By　Kyosuke Takayama (ドン・ガバチョ) support@mc.neweb.ne.jp
　　　配布ページ　(http://espion.just-size.jp/archives/dist_hako/)

┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫

　○スクリプト配布元

・箱庭諸島２配布元（現在は配布終了）
  オリジナル箱庭諸島２
  http://t.pos.to/hako/

・ＪＡＶＡスクリプト版箱庭諸島配布元
  あっぽー箱庭諸島
  http://appoh.execweb.cx/hakoniwa/


┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫

　○ご質問はこちらへ・・・

・箱庭チームトーナメントに関する質問は受けません。
	頑張ってご自分で解決して下さい。

・通常の箱庭２に関する質問は、オリジナル配布元の
	「意見・質問・雑談・その他」掲示板に
　http://t.pos.to/hako

・スクリプト設置等に関するご質問は、Tsubasa's HomePageの
	「ＣＧＩ駆け込み寺」に
　http://village.infoweb.ne.jp/~sakatuba/


┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫

　○免責

  使用者の責任において使用してください。
　作者は、いかなる損害・トラブルにも一切責任は負わないものとします。

  
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫

　○設置方法

　通常の箱庭諸島２が設置出来れば特に問題はありません。
　最初にhako-ini.cgiで設定を行ってから設置して下さい。


　＊追加されているファイルの説明です
　hako-ini.cgi
　　各種設定のファイルです
　hako-more.cgi
　　設定一覧や、マニュアルを表示するためのファイルです
　hako-js.cgi
　　JavaScript版の開発画面で開発するためのファイルです

　これらのファイルに新しいパーミッション等を設定する必要はありません。
　hako-turn.cgi等と同じように設置して下さい。 

　設置禁止のサーバー等もありますので、オリジナルの配布元、及び　当配布
　ページもよくお読みの上設置して下さい。

　imgexpフォルダには、画像のローカル設定用の説明ファイルが入ってます。
　ただし、画像は同梱されてませんので、圧縮したファイルをアップしておく
　必要があります。

　bbsフォルダには、戦略掲示板・チャットのCGIスクリプトが含まれてます。
　最低限管理者用パスワードは設定して下さい。
　bbs.cgi chat.cgi には実行権限を与える必要があります。


　○その他

　元々配布するつもりはまったくなかったため、決してキレイなスクリプト
　とは言いがたい状態になってます。
　そのため改造は勿論、設置にも少しばかり苦労するかもしれません。
　多分上級者向けの作りになってると思います。
　箱庭トーナメントの設置経験が無い人は、まず始めにそちらをやる事を
　お勧めします。
　

┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫

　○設定について

　◇セキュリティに関する項目
　hako-ini.cgiで設定を行えますが、以下の項目は必ず変更して下さい。
　変更しないと、セキュリティ上問題が生じ、参加者に迷惑が掛かります。

　$masterPassword　管理人用のマスターパスワードです
　$HspecialPassword　同じくスペシャルパスワードです
　$HdirName　データファイルが保存されているディレクトリです

　bbs/bbs.cgiの$pass　戦略室のマスターパスワードです


　◇追加・変更されている設定個所

　・その他
　hako-mente.cgiのメンテ用パスワードは、hako-ini.cgiで設定した、
　$masterPasswordです。


┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫

　○今後の予定

　◇今後バージョンアップするつもりはありません。


┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫

　○更新履歴

　◇2005/12/22　　Ver.1.04　XSS 脆弱性の対策
　◇2004/06/02　　Ver.1.03　window.open時のバグ修正
                            ステータスバーへの表示処理修正
                            配布サイトへのリンク修正
　◇2004/02/18　　Ver.1.02　マップサイズが奇数の際のバグ修正 (Thx. チヨリスタさん)
　　          　　        　たまに浅瀬が少ない島が出来てしまうバグ修正 (Thx. チヨリスタさん)
　　          　　        　window.open時のバグ修正
　　          　　        　IE6でレイアウトが崩れてしまうバグ修正(多分)
　◇2003/07/02　　Ver.1.01　ログ表示のバグ修正
　◇2002/11/06　　Ver.1.00　配布開始


┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫

　○最後に・・

　配布に至るまでに、沢山の方の協力を頂きました。
　テスト版に参加して下さった方、意見を言って頂いた方、
　この場をお借りしまして、感謝致します。
　みなさんの協力が無ければ、到底完成しなかったでしょう。
　本当に有難う御座います。


　バグ等を発見した場合は、遠慮なさらずにどんどんお知らせ下さい。
　メールでも掲示板でも手段は問いません。
　何卒、宜しくお願い致します。m(_ _)m

┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
