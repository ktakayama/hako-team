#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# ターン進行モジュール(ver1.02)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# 箱庭諸島のページ: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# 箱庭チームトーナメント
# ターン進行モジュール
# $Id: hako-turn.cgi,v 1.3 2004/02/18 05:35:38 gaba Exp $

#周囲2ヘックスの座標
my(@ax) = (0, 1, 1, 1, 0,-1, 0, 1, 2, 2, 2, 1, 0,-1,-1,-2,-1,-1, 0);
my(@ay) = (0,-1, 0, 1, 1, 0,-1,-2,-1, 0, 1, 2, 2, 2, 1, 0,-1,-2,-2);

#----------------------------------------------------------------------
# 島の新規作成モード
#----------------------------------------------------------------------
# メイン
sub newIslandMain {
	# 島がいっぱいでないかチェック
	if($HislandNumber >= $HmaxIsland or $HislandTurn) {
		unlock();
		tempNewIslandFull();
		return;
	}

	# 名前があるかチェック
	if($HcurrentName eq '') {
		unlock();
		tempNewIslandNoName();
		return;
	}

	# 名前が正当かチェック
	if($HcurrentName =~ /[,\?\(\)\<\>\$]|^無人$/) {
		# 使えない名前
		unlock();
		tempNewIslandBadName();
		return;
	}

	# 名前の重複チェック
	if(nameToNumber($HcurrentName) != -1) {
		# すでに発見ずみ
		unlock();
		tempNewIslandAlready();
		return;
	}

	# passwordの存在判定
	if($HinputPassword eq '') {
		# password無し
		unlock();
		tempNewIslandNoPassword();
		return;
	}

	# 確認用パスワード
	if($HinputPassword2 ne $HinputPassword) {
		# password間違い
		unlock();
		tempWrongPassword();
		return;
	}

	# 新しい島の番号を決める
	$HcurrentNumber = $HislandNumber;
	$HislandNumber++;
	$Hislands[$HcurrentNumber] = makeNewIsland();
	my($island) = $Hislands[$HcurrentNumber];

	# 各種の値を設定
	$island->{'name'} = $HcurrentName;
	$island->{'id'} = $HislandNextID;
	$HislandNextID ++;
	$island->{'absent'} = 1;
	$island->{'comment'} = '(未登録)';
	$island->{'password'} = encode($HinputPassword);
	$island->{'teamid'} = $HteamID;
	my($team) = $Hteams[$HidToTeamNumber{$island->{'teamid'}}];
	my($numMember) = $team->{'member'};
	my($count) = 0;
	while($numMember =~ s/([0-9]*),//) {
		$count++;
		if($HmenberCount == $count){
			unlock();
			tempOverMember();
			return;
		}
	}
	if($HteamID == 0) {
		unlock();
		tempOverMember();
		return;
	}
	# 人口その他算出
	estimate($HcurrentNumber);
	teamEstimate($HcurrentNumber);
	$team->{'member'} .= $island->{'id'} . ",";
	$team->{'money'} += $HinitialMoney;
	# データ書き出し
	writeIslandsFile($island->{'id'});
	writeTeamsFile();
	logDiscover($HcurrentName); # ログ

	# 開放
	unlock();

	# 発見画面
	tempNewIslandHead($HcurrentName); # 発見しました!!
	islandInfo(); # 島の情報
	islandMap(1); # 島の地図、ownerモード
}

# 新しい島を作成する
sub makeNewIsland {
	# 地形を作る
	my($land, $landValue) = makeNewLand();

	# 初期コマンドを生成
	my(@command, $i);
	for($i = 0; $i < $HcommandMax; $i++) {
		 $command[$i] = {
			 'kind' => $HcomDoNothing,
			 'target' => 0,
			 'x' => 0,
			 'y' => 0,
			 'arg' => 0
		 };
	}

	# 初期掲示板を作成
	my(@lbbs);
	for($i = 0; $i < $HlbbsMax; $i++) {
		 $lbbs[$i] = "0>>";
	}

	# 島にして返す
	return {
		'land' => $land,
		'landValue' => $landValue,
		'command' => \@command,
		'lbbs' => \@lbbs,
		'food' => $HinitialFood,
		'ownername' => '0'
	};
}

# 新しい島の地形を作成する
sub makeNewLand {
	# 基本形を作成
	my(@land, @landValue, $x, $y, $i);

	# 海に初期化
	for($y = 0; $y < $HislandSize; $y++) {
		 for($x = 0; $x < $HislandSize; $x++) {
			 $land[$x][$y] = $HlandSea;
			 $landValue[$x][$y] = 0;
		 }
	}

	# 中央の4*4に荒地を配置
	my($center) = int($HislandSize / 2 - 1);
	for($y = $center - 1; $y < $center + 3; $y++) {
		 for($x = $center - 1; $x < $center + 3; $x++) {
			 $land[$x][$y] = $HlandWaste;
		 }
	}

		# 初期の島の面積固定ルール
		my($size,$seacon) = (16,0);

		# 8*8範囲内に陸地を増殖
		while($size < $HlandSizeValue){
			# ランダム座標
			$x = random(8) + $center - 3;
			$y = random(8) + $center - 3;


			my($tmp) = countAround(\@land, $x, $y, $HlandSea, 7);
			if(countAround(\@land, $x, $y, $HlandSea, 7) != 7){
				# 周りに陸地がある場合、浅瀬にする
				# 浅瀬は荒地にする
				# 荒地は平地にする
			 if($land[$x][$y] == $HlandSea) {
					if($landValue[$x][$y] == 1) {
						$land[$x][$y] = $HlandPlains;
						$landValue[$x][$y] = 0;
						$size++;
						$seacon--;
					} else {
		 				$landValue[$x][$y] = 1;
						$seacon++;
					}
			 }
			}
		}

	makeRandomPointArray();
	for($i = 0; $i < $HpointNumber; $i++) {
		last if($seacon == $HseaNum);
		$x = $Hrpx[$i];
		$y = $Hrpy[$i];
		if(countAround(\@land, $x, $y, $HlandPlains, 7) && $land[$x][$y] == $HlandSea && $landValue[$x][$y] == 0){
			$landValue[$x][$y] = 1;
			$seacon += $sea_flag ? -1: 1;
		}
	}

	# 森を作る
	my($count) = 0;
	while($count < 4) {
		 # ランダム座標
		 $x = random(4) + $center - 1;
		 $y = random(4) + $center - 1;

		 # そこがすでに森でなければ、森を作る
		 if($land[$x][$y] != $HlandForest) {
			 $land[$x][$y] = $HlandForest;
			 $landValue[$x][$y] = 5; # 最初は500本
			 $count++;
		 }
	}

	# 町を作る
	$count = 0;
	while($count < 2) {
		 # ランダム座標
		 $x = random(4) + $center - 1;
		 $y = random(4) + $center - 1;

		 # そこが森か町でなければ、町を作る
		 if(($land[$x][$y] != $HlandTown) &&
			($land[$x][$y] != $HlandForest)) {
			 $land[$x][$y] = $HlandTown;
			 $landValue[$x][$y] = 5; # 最初は500人
			 $count++;
		 }
	}


	# 基地を作る
	$count = 0;
	while($count < $HlandFirstMiss) {
		 # ランダム座標
		 $x = random(4) + $center - 1;
		 $y = random(4) + $center - 1;

		 # そこが森か町かでなければ、基地
		 if(($land[$x][$y] != $HlandTown) &&
			($land[$x][$y] != $HlandBase) &&
			($land[$x][$y] != $HlandForest)) {
			 $land[$x][$y] = $HlandBase;
			 $landValue[$x][$y] = 0;
			 $count++;
		 }
	}

	return (\@land, \@landValue);
}

#----------------------------------------------------------------------
# 情報変更モード
#----------------------------------------------------------------------
# メイン
sub changeMain {
	# idから島を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	my($flag) = 0;

	# パスワードチェック
	if($HoldPassword eq $HspecialPassword) {
		# 特殊パスワード
	} elsif(!checkPassword($island->{'password'},$HoldPassword)) {
		# password間違い
		unlock();
		tempWrongPassword();
		return;
	}

	# 確認用パスワード
	if($HinputPassword2 ne $HinputPassword) {
		# password間違い
		unlock();
		tempWrongPassword();
		return;
	}

	if($HcurrentName ne '') {
		# 名前変更の場合		
		# 名前が正当かチェック
		if($HcurrentName =~ /[,\?\(\)\<\>]|^無人$/) {
			# 使えない名前
			unlock();
			tempNewIslandBadName();
			return;
		}

		# 名前の重複チェック
		if(nameToNumber($HcurrentName) != -1) {
			# すでに発見ずみ
			unlock();
			tempNewIslandAlready();
			return;
		}

		if($team->{'money'} < $HcostChangeName) {
			# 金が足りない
			unlock();
			tempChangeNoMoney();
			return;
		}

		# 代金
		if($HoldPassword ne $HspecialPassword) {
			$team->{'money'} -= $HcostChangeName;
		}

		# 名前を変更
		logChangeName($island->{'name'}, $HcurrentName);
		$island->{'name'} = $HcurrentName;
		$flag = 1;
	}

	# password変更の場合
	if($HinputPassword ne '') {
		# パスワードを変更
		$island->{'password'} = encode($HinputPassword);
		$flag = 1;
	}

	if($HownerName ne '') {
		# オーナー名を変更
		$island->{'ownername'} = $HownerName;
		$flag = 1;
	}

	if($HcurrentID == $deleteID and $masterPassword eq $HoldPassword and $HislandTurn == 0){
		# 島削除モード
		$team = $Hteams[$HidToTeamNumber{$island->{'teamid'}}];
		$team->{'pop'} -= $island->{'pop'};
		$team->{'money'} -= $HinitialMoney;
		$team->{'food'} -= $HinitialFood;
		$team->{'member'} =~ s/${HcurrentID},//;
		$island->{'pop'} = 0;
		$HislandNumber -= 1;
		islandSort();
		$flag = 1;
		writeTeamsFile();
	}

	if(($flag == 0) && ($HoldPassword ne $HspecialPassword)) {
		# どちらも変更されていない
		unlock();
		tempChangeNothing();
		return;
	}

	# データ書き出し
	writeIslandsFile($HcurrentID);
	unlock();

	# 変更成功
	tempChange();
}

#----------------------------------------------------------------------
# ターン進行モード
#----------------------------------------------------------------------
# メイン
sub turnMain {


	# ログファイルを後ろにずらす
	my($i, $j, $s, $d);
	for($i = ($HlogMax - 1); $i >= 0; $i--) {
		$j = $i + 1;
		my($s) = "${HdirName}/hakojima.log$i";
		my($d) = "${HdirName}/hakojima.log$j";
		unlink($d);
		rename($s, $d);
	}

	# 座標配列を作る
	makeRandomPointArray();

	# ターン番号
	$HislandTurn++;

	# 戦闘期間への以降等
	$winlose = 0;
	if($HnextCTurn == 0 && $HislandTurn == $HyosenTurn) {
		$HnextCTurn = $HyosenTurn + $HdevTurn;
		$winlose = 2;
	} elsif($HislandTurn == $HnextCTurn && $HislandTurn > $HyosenTurn && $HfightMode == 1) {
		$winlose = 1;
	} elsif($HislandTurn > $HnextCTurn && $HislandTurn > $HyosenTurn) {
		if($HfightMode) {
			$HfightMode = 0;
			$HfightCount++;
			$HnextCTurn += $HdevTurn;
			$winlose = 2;
		} else {
			$HfightMode = 1;
			$HnextCTurn += $HfigTurn;
			# 決勝戦は戦闘期間延長
			if($HteamNumber == 2) { $HnextCTurn += $HfigRepTurn;}
			$winlose = 3;
		}
	}

	if($HturnCount > 1) {
		$HturnCount--;
	} elsif($winlose == 1) {
		# 最終更新時間を更新
		$HislandLastTime += $HinterTime;
		$HturnCount = $HdevRepTurn;
	} elsif($HfightMode or $HislandTurn == $HnextCTurn) {
		# 戦闘期間
		$HislandLastTime += $HfightTime;
		$HturnCount = $HfigRepTurn;
	} else {
		# 開発期間
		$HislandLastTime += $HunitTime;
		$HturnCount = $HdevRepTurn;
	}

	# 順番決め
	my(@order) = randomArray($HislandNumber);

	# 収入、消費フェイズ
	for($i = 0; $i < $HislandNumber; $i++) {
		estimate($order[$i]);
		income($Hislands[$order[$i]]);

		# ターン開始前の人口をメモる
		$Hislands[$order[$i]]->{'oldPop'} = $Hislands[$order[$i]]->{'pop'};
	}

	# チームパスワード決定　BBS用ファイルに書き出し
	for($i = 0; $i < $HteamNumber; $i++) {
		my($team) = $Hteams[$i];
		# ターン開始前の人口をメモる
		$team->{'oldPop'} = $team->{'pop'};
		$team->{'pop'} = 0;
		$team->{'farm'} = 0;
		$team->{'factory'} = 0;
		$team->{'food'} = 0;

		my($passkey) = random(1200);
		$team->{'password'} = crypt($team->{'id'} * $passkey * $HislandTurn,hp);
		open(DAT, ">>team.tmp.cgi");
			print DAT "$team->{'id'}\n";
			print DAT "$team->{'name'}\n";
			print DAT "$team->{'password'}\n";
		close(DAT);
	}
	rename ("team.tmp.cgi", "team.cgi");

	# コマンド処理
	for($i = 0; $i < $HislandNumber; $i++) {
		# 戻り値1になるまで繰り返し
		while(doCommand($Hislands[$order[$i]]) == 0){};
	}

	# 成長および単ヘックス災害
	for($i = 0; $i < $HislandNumber; $i++) {
		doEachHex($Hislands[$order[$i]]);
	}

	# 島全体処理
	my($remainNumber) = $HislandNumber;
	my($island);
	for($i = 0; $i < $HislandNumber; $i++) {
		$island = $Hislands[$order[$i]];
		doIslandProcess($order[$i], $island); 
	}

	for($i = 0; $i < $HislandNumber; $i++) {
		teamEstimate($order[$i]);
	}

	my($remainTNumber) = $HteamNumber;
	if($HislandTurn == $HyosenTurn) {
		teamSort();
		for($i = $yteamNum; $i < $HteamNumber; $i++) {
			$team = $Hteams[$i];
			# 敗者
			logDeadyt($team->{'name'});
			push(@fightLog, "$team->{'name'}<>$team->{'pop'}<>$team->{'member'}");
			$team->{'pop'} = -1;
			my($numTTMember) = $team->{'member'};
			while($numTTMember =~ s/([0-9]*),//) {
				my($HcurrentNumber) = $HidToNumber{$1};
				my($Disland) = $Hislands[$HcurrentNumber];
				$Disland->{'pop'} = -1;
				$remainNumber--;
				logDeady($Disland->{'name'});
			}
			$remainTNumber--;

		}
		HyosenLog(@fightLog);
	}

	# 勝敗判定
	if($winlose == 1) {
		my($team,@fightLog);
		for($i = 0; $i < $HteamNumber; $i++) {
			$team = $Hteams[$i];
			my($HcurrentTNumber) = $HidToTeamNumber{$team->{'fightid'}};
			my($tTeam) = $Hteams[$HcurrentTNumber];
			if($team->{'pop'} >= $tTeam->{'pop'}) {
				# 勝者
				# 報酬金
				my($rewardMoney) = $tTeam->{'reward'} * $tTeam->{'rewturn'} * 5 + $team->{'waste'} * $HcomCost[$HcomPrepare2];
				$team->{'reward'} = 0;
				$team->{'rewturn'} = 0;
				$team->{'money'} += $rewardMoney;
				logWin(0,$team->{'name'},$rewardMoney,$tTeam->{'name'});
				my($numMember) = $team->{'member'};
				while($numMember =~ s/([0-9]*),//) {
					my($HcurrenTNumber) = $HidToNumber{$1};
					my($island) = $Hislands[$HcurrenTNumber];
					logWin($island->{'id'},$island->{'name'},$rewardMoney,$tTeam->{'name'});
				}
				$team->{'fightid'} = 0;
				push(@fightLog, "$team->{'name'}<>$team->{'pop'}<>$rewardMoney<>$tTeam->{'name'}<>$tTeam->{'pop'}<>$team->{'member'},$tTeam->{'member'}");

				# 敗者
				logDead($tTeam->{'name'});
				$tTeam->{'pop'} = -1;
				my($numTTMember) = $tTeam->{'member'};
				while($numTTMember =~ s/([0-9]*),//) {
					my($HcurrentNumber) = $HidToNumber{$1};
					my($Disland) = $Hislands[$HcurrentNumber];
					$Disland->{'pop'} = -1;
					$remainNumber--;
					logDead($Disland->{'name'} . "島");
				}
				$remainTNumber--;
			}
		}
		HfightLog(@fightLog);
	} elsif($winlose == 2) {
		# 対戦相手決定
		if($HislandTurn == $HyosenTurn) {
			$HTnumber = $remainTNumber;
		} else {
			$HTnumber = $HteamNumber;
		}
		my(@ordert) = randomArray($HTnumber);
		my($team);
		for($i = 0; $i < $HTnumber; $i++) {
			$team = $Hteams[$ordert[$i]];
			if($team->{'fightid'} <= 0) {
				my($jj) = $i + 1;
				$tTeam = $Hteams[$ordert[$jj]];
				$team->{'fightid'} = $tTeam->{'id'};
				$tTeam->{'fightid'} = $team->{'id'};
			}
		}
	}

	# 対戦の記録保存
	open(FOUT, "${HdirName}/fight.log");
		while($f = <FOUT>){
			chomp($f);
			push(@offset,"$f\n");
		}
	close(FOUT);

	# 人口順にソート
	islandSort();
	teamSort();

	# 島数カット
	$HislandNumber = $remainNumber;
	$HteamNumber   = $remainTNumber;

	# バックアップターンであれば、書く前にrename
	if(($HislandTurn % $HbackupTurn) == 0) {
		my($i);
		my($tmp) = $HbackupTimes - 1;
		myrmtree("${HdirName}.bak$tmp");
		for($i = ($HbackupTimes - 1); $i > 0; $i--) {
			my($j) = $i - 1;
			rename("${HdirName}.bak$j", "${HdirName}.bak$i");
		}
		rename("${HdirName}", "${HdirName}.bak0");
		mkdir("${HdirName}", $HdirMode);

		# ログファイルだけ戻す
		for($i = 0; $i <= $HlogMax; $i++) {
			rename("${HdirName}.bak0/hakojima.log$i",
				   "${HdirName}/hakojima.log$i");
		}
		rename("${HdirName}.bak0/hakojima.his",
			   "${HdirName}/hakojima.his");
	}

	# ファイルに書き出し
	writeIslandsFile(-1);
	writeTeamsFile();

	# 対戦の記録保存
	open(FOUT, ">${HdirName}/fight.log");
		print FOUT @offset;
	close(FOUT);

	# ログ書き出し
	logFlush();

	# 記録ログ調整
	logHistoryTrim();

	# データ読み込み
	readTeamsFile();
	readIslandsFile();

	# トップへ
	topPageMain();
}

# ディレクトリ消し
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

# 収入、消費フェイズ
sub income {
	my($island) = @_;
	my($HcurrentTNumber) = $HidToTeamNumber{$island->{'teamid'}};
	my($team) = $Hteams[$HcurrentTNumber];
	my($pop, $farm, $factory) = 
		(	  
		 $island->{'pop'},
		 $island->{'farm'} * 10,
		 $island->{'factory'},
		 );

	# 収入
	if($pop > $farm) {
		# 農業だけじゃ手が余る場合
		$island->{'food'} += $farm; # 農場フル稼働
		$team->{'money'} +=
			min(int(($pop - $farm) / 10),
				 $factory );
	} else {
		# 農業だけで手一杯の場合
		$island->{'food'} += $pop; # 全員野良仕事
	}

	# 食料消費
	$island->{'food'} = int(($island->{'food'}) - ($pop * $HeatenFood));
}


# コマンドフェイズ
sub doCommand {
	my($island) = @_;
	my($HcurrentTNumber) = $HidToTeamNumber{$island->{'teamid'}};
	my($team) = $Hteams[$HcurrentTNumber];

	# コマンド取り出し
	my($comArray, $command);
	$comArray = $island->{'command'};
	$command = $comArray->[0]; # 最初のを取り出し
	slideFront($comArray, 0); # 以降を詰める

	# 各要素の取り出し
	my($kind, $target, $x, $y, $arg) = 
		(
		 $command->{'kind'},
		 $command->{'target'},
		 $command->{'x'},
		 $command->{'y'},
		 $command->{'arg'}
		 );

	# 導出値
	my($name) = $island->{'name'};
	my($id) = $island->{'id'};
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($landKind) = $land->[$x][$y];
	my($lv) = $landValue->[$x][$y];
	my($cost) = $HcomCost[$kind];
	my($comName) = $HcomName[$kind];
	my($point) = "($x, $y)";
	my($landName) = landName($landKind, $lv);

	if($kind == $HcomDoNothing) {
		# 資金繰り
		logDoNothing($id, $name, $comName);
		$team->{'money'} += 10;
		$island->{'absent'} ++;
		
		# 自動放棄
		if($island->{'absent'} >= $HgiveupTurn) {
			$island->{'password'} = encode($team->{'password'});
			$island->{'comment'} = $HgiveupComment;
		}
		return 1;
	}

	$island->{'absent'} = 0;

	# コストチェック
	if($cost > 0) {
		# 金の場合
		if($team->{'money'} < $cost) {
			logNoMoney($id, $name, $comName);
			return 0;
		}
	} elsif($cost < 0) {
		# 食料の場合
		if($island->{'food'} < (-$cost)) {
			logNoFood($id, $name, $comName);
			return 0;
		}
	}

	if(($kind == $HcomAutoPrepare3 or $kind == $HcomFastFarm) && ($HfightMode)){
		logLandNG($id, $name, $comName, $landName, $point, '現在戦闘期間中のため');
		return 0;
	}

	# コマンドで分岐
	if(($kind == $HcomPrepare) ||
	   ($kind == $HcomPrepare2)) {
		# 整地、地ならし
		if(($landKind == $HlandSea) || 
		   ($landKind == $HlandSbase)) {
			# 海、海底基地、は整地できない
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		# 目的の場所を平地にする
		$land->[$x][$y] = $HlandPlains;
		$landValue->[$x][$y] = 0;
		logLandSuc($id, $name, '整地', $point);

		# 金を差し引く
		$team->{'money'} -= $cost;

		if($kind == $HcomPrepare2) {
			# 地ならし
			return 0;
		} else {
			return 1;
		}
	} elsif($kind == $HcomAutoPrepare3) {
		# 一括自動地ならし
		my($prepareM, $preFlag) = ($HcomCost[$HcomPrepare2], 0);
		for($i = 0; $i < $HpointNumber; $i++) {
			$bx = $Hrpx[$i];
			$by = $Hrpy[$i];
			if(($land->[$bx][$by] == $HlandWaste) && ($team->{'money'} >= $prepareM)){
				# 目的の場所を平地にする
				$land->[$bx][$by] = $HlandPlains;
				$landValue->[$bx][$by] = 0;
				logLandSuc($id, $name, '整地', "($bx, $by)");
				# 金を差し引く
				$team->{'money'} -= $prepareM;
				$preFlag++;
				if($preFlag == $precheap){ $prepareM = int($prepareM * $precheap2 / 10); }
			}
		}
		# ターン消費せず
		return 0;
	} elsif($kind == $HcomReclaim) {
		# 埋め立て
		if(($landKind != $HlandSea) &&
		   ($landKind != $HlandSbase)) {
			# 海、海底基地、しか埋め立てできない
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		# 周りに陸があるかチェック
		my($seaCount) =
			countAround($land, $x, $y, $HlandSea, 7) +
			countAround($land, $x, $y, $HlandSbase, 7);

		if($seaCount == 7) {
			# 全部海だから埋め立て不能
			logNoLandAround($id, $name, $comName, $point);
			return 0;
		}

		if(($landKind == $HlandSea) && ($lv == 1)) {
			# 浅瀬の場合
			# 目的の場所を荒地にする
			$land->[$x][$y] = $HlandWaste;
			$landValue->[$x][$y] = 0;
			logLandSuc($id, $name, $comName, $point);
			$island->{'area'}++;

			if($seaCount <= 4) {
				# 周りの海が3ヘックス以内なので、浅瀬にする
				my($i, $sx, $sy);

				for($i = 1; $i < 7; $i++) {
					$sx = $x + $ax[$i];
					$sy = $y + $ay[$i];

					# 行による位置調整
					if((($sy % 2) == 0) && (($y % 2) == 1)) {
						$sx--;
					}

					if(($sx < 0) || ($sx >= $HislandSize) ||
					   ($sy < 0) || ($sy >= $HislandSize)) {
					} else {
						# 範囲内の場合
						if($land->[$sx][$sy] == $HlandSea) {
							$landValue->[$sx][$sy] = 1;
						}
					}
				}
			}
		} else {
			# 海なら、目的の場所を浅瀬にする
			$land->[$x][$y] = $HlandSea;
			$landValue->[$x][$y] = 1;
			logLandSuc($id, $name, $comName, $point);
		}
		
		# 金を差し引く
		$team->{'money'} -= $cost;
		return 1;
	} elsif($kind == $HcomDestroy) {
		# 掘削
		if(($landKind == $HlandSea && $lv == 0) && ($landKind == $HlandSbase)) {
			# 海、海底基地は掘削できない
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}
		# 目的の場所を海にする。浅瀬なら海に。
		if($landKind == $HlandSea) {
			$landValue->[$x][$y] = 0;
		} else {
			$land->[$x][$y] = $HlandSea;
			$landValue->[$x][$y] = 1;
			$island->{'area'}--;
		}
		logLandSuc($id, $name, $comName, $point);

		# 金を差し引く
		$team->{'money'} -= $cost;
		return 1;
	} elsif($kind == $HcomSellTree) {
		# 伐採
		if($landKind != $HlandForest) {
			# 森以外は伐採できない
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		# 目的の場所を平地にする
		$land->[$x][$y] = $HlandPlains;
		$landValue->[$x][$y] = 0;
		logLandSuc($id, $name, $comName, $point);

		# 売却金を得る
		$team->{'money'} += $HtreeValue * $lv;
		return 0;
	} elsif(($kind == $HcomPlant) ||
			($kind == $HcomFarm) ||
			($kind == $HcomFastFarm) ||
			($kind == $HcomFactory) ||
			($kind == $HcomBase) ||
			($kind == $HcomHaribote) ||
			($kind == $HcomDbase)) {

		# 地上建設系
		if(!
		   (($landKind == $HlandPlains) ||
			($landKind == $HlandTown) ||
			(($landKind == $HlandFarm) && ($kind == $HcomFarm)) ||
			(($landKind == $HlandFactory) && ($kind == $HcomFactory)))) {
			# 不適当な地形
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		# 種類で分岐
		if($kind == $HcomPlant) {
			# 目的の場所を森にする。
			$land->[$x][$y] = $HlandForest;
			$landValue->[$x][$y] = 1; # 木は最低単位
			logPBSuc($id, $name, $comName, $point);
		} elsif($kind == $HcomBase) {
			# 目的の場所をミサイル基地にする。
			$land->[$x][$y] = $HlandBase;
			$landValue->[$x][$y] = 0; # 経験値0
			logPBSuc($id, $name, $comName, $point);
			if($HfightMode) { $team->{'rewturn'}++; } # 戦闘期間中はカウント
		} elsif($kind == $HcomHaribote) {
			# 目的の場所をハリボテにする
			$land->[$x][$y] = $HlandHaribote;
			$landValue->[$x][$y] = 0;
			logHariSuc($id, $name, $comName, $HcomName[$HcomDbase], $point);
		} elsif(($kind == $HcomFarm) || ($kind == $HcomFastFarm)) {
			# 農場
			if($landKind == $HlandFarm) {
				# すでに農場の場合
				$landValue->[$x][$y] += 2; # 規模 + 2000人
				if($landValue->[$x][$y] > 50) {
					$landValue->[$x][$y] = 50; # 最大 50000人
				}
			} else {
				# 目的の場所を農場に
				$land->[$x][$y] = $HlandFarm;
				$landValue->[$x][$y] = 10; # 規模 = 10000人
			}
			logLandSuc($id, $name, $comName, $point);
			if($kind == $HcomFastFarm){
				$team->{'money'} -= $cost;
				return 0;
			}
		} elsif($kind == $HcomFactory) {
			# 工場
			if($landKind == $HlandFactory) {
				# すでに工場の場合
				$landValue->[$x][$y] += 10; # 規模 + 10000人
				if($landValue->[$x][$y] > 100) {
					$landValue->[$x][$y] = 100; # 最大 100000人
				}
			} else {
				# 目的の場所を工場に
				$land->[$x][$y] = $HlandFactory;
				$landValue->[$x][$y] = 30; # 規模 = 10000人
			}
			logLandSuc($id, $name, $comName, $point);
		} elsif($kind == $HcomDbase) {
			# 防衛施設
			# 目的の場所を防衛施設に
			$land->[$x][$y] = $HlandDefence;
			$landValue->[$x][$y] = 0;
			logPBSuc($id, $name, $comName, $point);
			if($HfightMode) { $team->{'rewturn'}++; } # 戦闘期間中はカウント
		}

		# 金を差し引く
		$team->{'money'} -= $cost;

		# 回数付きなら、コマンドを戻す
		if(($kind == $HcomFarm) ||
		   ($kind == $HcomFactory)) {
			if($arg > 1) {
				my($command);
				$arg--;
				slideBack($comArray, 0);
				$comArray->[0] = {
					'kind' => $kind,
					'target' => $target,
					'x' => $x,
					'y' => $y,
					'arg' => $arg
					};
			}
		}

		return 1;
	} elsif(($kind == $HcomMissileNM) ||
			($kind == $HcomMissilePP)) {
		# ミサイル系
		# ターゲット取得
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# ターゲットがすでにない
			logMsNoTarget($id, $name, $comName);
			return 0;
		}

		my($flag) = 0;
		if($arg == 0) {
			# 0の場合は撃てるだけ
			$arg = 10000;
		}

		# 事前準備
		my($tIsland) = $Hislands[$tn];
		my($tName) = $tIsland->{'name'};
		my($tLand) = $tIsland->{'land'};
		my($tLandValue) = $tIsland->{'landValue'};
		my($tx, $ty, $err);

		# 難民の数
		my($boat) = 0;

		if(($HfightMode == 0) && ($tIsland->{'teamid'} != $island->{'teamid'})){
			# 開発期間中はキャンセル
			logLandNG($id, $name, $comName, $landName, $point, '現在開発期間中のため');
			return 0;
		} elsif($HfightMode && $tIsland->{'teamid'} != $team->{'fightid'} && $tIsland->{'teamid'} != $island->{'teamid'}){
			# 対戦相手以外はキャンセル
			logLandNG($id, $name, $comName, $landName, $point, '目標が対戦チームでないため');
			return 0;
		}  elsif($island->{'pop'} < 1000 and $HteamNumber > 2) {
			 logLandNG($id, $name, $comName, $landName, $point, '人口が10万人以下の為');
			 return 0;
		}

		# 誤差
		if($kind == $HcomMissilePP) {
			$err = 7;
		} else {
			$err = 19;
		}

		# 金が尽きるか指定数に足りるか基地全部が撃つまでループ
		my($bx, $by, $count) = (0,0,0);
		while(($arg > 0) &&
			  ($team->{'money'} >= $cost)) {
			# 基地を見つけるまでループ
			while($count < $HpointNumber) {
				$bx = $Hrpx[$count];
				$by = $Hrpy[$count];
				if(($land->[$bx][$by] == $HlandBase) ||
				   ($land->[$bx][$by] == $HlandSbase)) {
					last;
				}
				$count++;
			}
			if($count >= $HpointNumber) {
				# 見つからなかったらそこまで
				last;
			}
			# 最低一つ基地があったので、flagを立てる
			$flag = 1;		   

			# 基地のレベルを算出
			my($level) = expToLevel($land->[$bx][$by], $landValue->[$bx][$by]);
			# 基地内でループ
			while(($level > 0) &&
				  ($arg > 0) &&
				  ($team->{'money'} > $cost)) {
				# 撃ったのが確定なので、各値を消耗させる
				$level--;
				$arg--;
				$team->{'money'} -= $cost;

				# 着弾点算出
				my($r) = random($err);
				$tx = $x + $ax[$r];
				$ty = $y + $ay[$r];
				if((($ty % 2) == 0) && (($y % 2) == 1)) {
					$tx--;
				}

				# 着弾点範囲内外チェック
				if(($tx < 0) || ($tx >= $HislandSize) ||
				   ($ty < 0) || ($ty >= $HislandSize)) {
					# 範囲外
					# 通常系
					logMsOut($id, $target, $name, $tName,
								  $comName, $point);
					next;
				}

				# 着弾点の地形等算出
				my($tL) = $tLand->[$tx][$ty];
				my($tLv) = $tLandValue->[$tx][$ty];
				my($tLname) = landName($tL, $tLv);
				my($tPoint) = "($tx, $ty)";

				# 防衛施設判定
				my($defence) = 0;
				if($HdefenceHex[$id][$tx][$ty] == 1) {
					$defence = 1;
				} elsif($HdefenceHex[$id][$tx][$ty] == -1) {
					$defence = 0;
				} else {
					if($tL == $HlandDefence) {
						# 防衛施設に命中
						# フラグをクリア
						my($i, $count, $sx, $sy);
						for($i = 0; $i < 19; $i++) {
							$sx = $tx + $ax[$i];
							$sy = $ty + $ay[$i];

							# 行による位置調整
							if((($sy % 2) == 0) && (($ty % 2) == 1)) {
								$sx--;
							}

							if(($sx < 0) || ($sx >= $HislandSize) ||
							   ($sy < 0) || ($sy >= $HislandSize)) {
								# 範囲外の場合何もしない
							} else {
								# 範囲内の場合
								$HdefenceHex[$id][$sx][$sy] = 0;
							}
						}
					} elsif(countAround($tLand, $tx, $ty, $HlandDefence, 19)) {
						$HdefenceHex[$id][$tx][$ty] = 1;
						$defence = 1;
					} else {
						$HdefenceHex[$id][$tx][$ty] = -1;
						$defence = 0;
					}
				}
				
				if($defence == 1) {
					# 空中爆破
					# 通常系
					logMsCaught($id, $target, $name, $tName,
									 $comName, $point, $tPoint);
					next;
				}

				# 「効果なし」hexを最初に判定
				if((($tL == $HlandSea) && ($tLv == 0))|| # 深い海
				   (($tL == $HlandSea) ||   # 海または・・・
					 ($tL == $HlandSbase))) {   # 海底基地以外
					# 海底基地の場合、海のフリ
					if($tL == $HlandSbase) {
						$tL = $HlandSea;
					}
					$tLname = landName($tL, $tLv);

					# 無効化
					logMsNoDamage($id, $target, $name, $tName,
									   $comName, $tLname, $point, $tPoint);
					next;
				}

					if($tL == $HlandWaste) {
						# 荒地(被害なし)
						logMsWaste($id, $target, $name, $tName,
										$comName, $tLname, $point, $tPoint);
					} else {
						# 通常地形
						logMsNormal($id, $target, $name, $tName,
										 $comName, $tLname, $point,
										 $tPoint);
					}
					# 経験値
					if($tL == $HlandTown) {
						if(($land->[$bx][$by] == $HlandBase) ||
							($land->[$bx][$by] == $HlandSbase)) {
							$landValue->[$bx][$by] += int($tLv / 20);
							$boat += $tLv; # 通常ミサイルなので難民にプラス
							if($landValue->[$bx][$by] > $HmaxExpPoint) {
								$landValue->[$bx][$by] = $HmaxExpPoint;
							}
						}
						$tIsland->{'pop'} -= $tLv;
					}
					
					# 荒地になる
					$tLand->[$tx][$ty] = $HlandWaste;
					$tLandValue->[$tx][$ty] = 1; # 着弾点

			}

			# カウント増やしとく
			$count++;
		}


		if($flag == 0) {
			# 基地が一つも無かった場合
			logMsNoBase($id, $name, $comName);
			return 0;
		}

		if($HfightMode) {
			# 戦闘期間中はカウント
			$team->{'rewturn'}++;
		}

		# 難民判定
		$boat = int($boat / 2);
		if(($boat > 0) && ($id != $target)) {
			# 難民漂着
			my($achive); # 到達難民
			my($i);
			for($i = 0; ($i < $HpointNumber && $boat > 0); $i++) {
				$bx = $Hrpx[$i];
				$by = $Hrpy[$i];
				if($land->[$bx][$by] == $HlandTown) {
					# 町の場合
					my($lv) = $landValue->[$bx][$by];
					if($boat > 50) {
						$lv += 50;
						$boat -= 50;
						$achive += 50;
					} else {
						$lv += $boat;
						$achive += $boat;
						$boat = 0;
					}
					if($lv > 200) {
						$boat += ($lv - 200);
						$achive -= ($lv - 200);
						$lv = 200;
					}
					$landValue->[$bx][$by] = $lv;
				} elsif($land->[$bx][$by] == $HlandPlains) {
					# 平地の場合
					$land->[$bx][$by] = $HlandTown;;
					if($boat > 10) {
						$landValue->[$bx][$by] = 5;
						$boat -= 10;
						$achive += 10;
					} elsif($boat > 5) {
						$landValue->[$bx][$by] = $boat - 5;
						$achive += $boat;
						$boat = 0;
					}
				}
				if($boat <= 0) {
					last;
				}
			}
			if($achive > 0) {
				# 少しでも到着した場合、ログを吐く
				logMsBoatPeople($id, $name, $achive);
				$island->{'achive'} = $achive;
				# 難民の数が一定数以上なら、平和賞の可能性あり
				if($achive >= 200) {
					my($flags) = $island->{'prize'};

					if((!($flags & 8)) &&  $achive >= 200){
						$flags |= 8;
						logPrize($id, $name, $Hprize[4]);
					} elsif((!($flags & 16)) &&  $achive > 500){
						$flags |= 16;
						logPrize($id, $name, $Hprize[5]);
					} elsif((!($flags & 32)) &&  $achive > 800){
						$flags |= 32;
						logPrize($id, $name, $Hprize[6]);
					}
					$island->{'prize'} = $flags;
				}
			}
		}
		return 1;
	} elsif($kind == $HcomSell) {
		# 輸出量決定
		if($arg == 0) { $arg = 1; }
		my($value) = min($arg * (-$cost), $island->{'food'});

		# 輸出ログ
		logSell($id, $name, $comName, $value);
		$island->{'food'} -=  $value;
		$team->{'money'} += ($value / 10);
		return 0;
	} elsif($kind == $HcomFood) {
		# 援助系
		# ターゲット取得
		my($tn) = $HidToNumber{$target};
		my($tIsland) = $Hislands[$tn];
		my($tName) = $tIsland->{'name'};
		if($island->{'teamid'} != $tIsland->{'teamid'}) {
			logLandNG($id, $name, $comName, $landName, $point, '援助先が他チームの為に');
			return 0;
		}
		# 援助量決定
		if($arg == 0) { $arg = 1; }
		my($value, $str);
		$value = min($arg * (-$cost), $island->{'food'});
		$str = "$value$HunitFood";

		# 援助ログ
		logAid($id, $target, $name, $tName, $comName, $str);

		$island->{'food'} -= $value;
		$tIsland->{'food'} += $value;
		return 0;
	} elsif($kind == $HcomPropaganda) {
		# 誘致活動
		if($HyosenTurn >= $HislandTurn) {
			 logLandNG($id, $name, $comName, $landName, $point, '予選期間の為');
			 return 0;
		}
		logPropaganda($id, $name, $comName);
		$island->{'propaganda'} = 1;
		$island->{'money'} -= $cost;
		return 1;
	}

	return 1;
}


# 成長および単ヘックス災害
sub doEachHex {
	my($island) = @_;

	# 導出値
	my($name) = $island->{'name'};
	my($id) = $island->{'id'};
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($HcurrentTNumber) = $HidToTeamNumber{$island->{'teamid'}};
	my($team) = $Hteams[$HcurrentTNumber];

	# 増える人口のタネ値
	my($addpop)  = 10;  # 村、町
	my($addpop2) = 0; # 都市
	if($island->{'food'} < 0) {
		# 食料不足
		$addpop = -30;
	}
	if($island->{'absent'} >= $HstopAddPop) {
		$addpop = -10;
	} elsif($island->{'propaganda'}) {
		# 誘致活動中
		$addpop = 30;
		$addpop2 = 3;
	}
	# ループ
	my($x, $y, $i);
	for($i = 0; $i < $HpointNumber; $i++) {
		$x = $Hrpx[$i];
		$y = $Hrpy[$i];
		my($landKind) = $land->[$x][$y];
		my($lv) = $landValue->[$x][$y];

		if($landKind == $HlandTown) {
			# 町系
			if($addpop < 0) {
				# 不足
				$lv -= (random(-$addpop) + 1);
				if($lv <= 0) {
					# 平地に戻す
					$land->[$x][$y] = $HlandPlains;
					$landValue->[$x][$y] = 0;
					next;
				}
			} elsif($addpop > 0) {
				# 成長
				if($lv < 100) {
					$lv += random($addpop) + 1;
					if($lv > 100) {
						$lv = 100;
					}
				} else {
					# 都市になると成長遅い
					if($addpop2 > 0) {
						$lv += random($addpop2) + 1;
					}
				}
			}
			if($lv > 200) {
				$lv = 200;
			}
			$landValue->[$x][$y] = $lv;
		} elsif($landKind == $HlandPlains) {
			# 平地
			if(random(5) == 0) {
				# 周りに農場、町があれば、ここも町になる
				if(countGrow($land, $landValue, $x, $y) || $island->{'propaganda'}){
					$land->[$x][$y] = $HlandTown;
					$landValue->[$x][$y] = 1;
				}
			}
		} elsif($landKind == $HlandForest) {
			# 森
			if($lv < 200) {
				# 木を増やす
				$landValue->[$x][$y] += $HtreeUp;
			}
		}
	}
}

# 周囲の町、農場があるか判定
sub countGrow {
	my($land, $landValue, $x, $y) = @_;
	my($i, $sx, $sy);
	for($i = 1; $i < 7; $i++) {
		 $sx = $x + $ax[$i];
		 $sy = $y + $ay[$i];

		 # 行による位置調整
		 if((($sy % 2) == 0) && (($y % 2) == 1)) {
			 $sx--;
		 }

		 if(($sx < 0) || ($sx >= $HislandSize) ||
			($sy < 0) || ($sy >= $HislandSize)) {
		 } else {
			 # 範囲内の場合
			 if(($land->[$sx][$sy] == $HlandTown) ||
				($land->[$sx][$sy] == $HlandFarm)) {
				 if($landValue->[$sx][$sy] != 1) {
					 return 1;
				 }
			 }
		 }
	}
	return 0;
}

# 島全体
sub doIslandProcess {
	my($number, $island) = @_;

	# 導出値
	my($name) = $island->{'name'};
	my($id) = $island->{'id'};
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($HcurrentTNumber) = $HidToTeamNumber{$island->{'teamid'}};
	my($team) = $Hteams[$HcurrentTNumber];

	# 食料不足
	if($island->{'food'} < 0) {
		# 不足メッセージ
		logStarve($id, $name);
		$island->{'food'} = 0;

		my($x, $y, $landKind, $lv, $i);
		for($i = 0; $i < $HpointNumber; $i++) {
			$x = $Hrpx[$i];
			$y = $Hrpy[$i];
			$landKind = $land->[$x][$y];
			$lv = $landValue->[$x][$y];

			if(($landKind == $HlandFarm) ||
			   ($landKind == $HlandFactory) ||
			   ($landKind == $HlandBase) ||
			   ($landKind == $HlandDefence)) {
				# 1/4で壊滅
				if(random(4) == 0) {
					logSvDamage($id, $name, landName($landKind, $lv),
								"($x, $y)");
					$land->[$x][$y] = $HlandWaste;
					$landValue->[$x][$y] = 0;
				}
			}
		}
	}

	# 地盤沈下判定
	if(($island->{'area'} > $HdisFallBorder) &&
	   (random(1000) < $HdisFalldown)) {
		# 地盤沈下発生
		logFalldown($id, $name);

		my($x, $y, $landKind, $lv, $i);
		for($i = 0; $i < $HpointNumber; $i++) {
			$x = $Hrpx[$i];
			$y = $Hrpy[$i];
			$landKind = $land->[$x][$y];
			$lv = $landValue->[$x][$y];

			if(($landKind != $HlandSea) &&
			   ($landKind != $HlandSbase)) {

				# 周囲に海があれば、値を-1に
				if(countAround($land, $x, $y, $HlandSea, 7) + 
				   countAround($land, $x, $y, $HlandSbase, 7)) {
					logFalldownLand($id, $name, landName($landKind, $lv),
								"($x, $y)");
					$land->[$x][$y] = -1;
					$landValue->[$x][$y] = 0;
				}
			}
		}

		for($i = 0; $i < $HpointNumber; $i++) {
			$x = $Hrpx[$i];
			$y = $Hrpy[$i];
			$landKind = $land->[$x][$y];

			if($landKind == -1) {
				# -1になっている所を浅瀬に
				$land->[$x][$y] = $HlandSea;
				$landValue->[$x][$y] = 1;
			} elsif ($landKind == $HlandSea) {
				# 浅瀬は海に
				$landValue->[$x][$y] = 0;
			}

		}
	}

	# 食料があふれてたら換金
	if($island->{'food'} > 9999) {
		$team->{'money'} += int(($island->{'food'} - 9999) / 10);
		$island->{'food'} = 9999;
	} 

	# 各種の値を計算
	estimate($number);

	# 繁栄、災難賞
	$pop = $island->{'pop'};
	my($damage) = $island->{'oldPop'} - $pop;
	my($flags) = $island->{'prize'};


	# 繁栄賞
	if((!($flags & 1)) &&  $pop >= 3000){
		$flags |= 1;
		logPrize($id, $name, $Hprize[1]);
	} elsif((!($flags & 2)) &&  $pop >= 5000){
		$flags |= 2;
		logPrize($id, $name, $Hprize[2]);
	} elsif((!($flags & 4)) &&  $pop >= 10000){
		$flags |= 4;
		logPrize($id, $name, $Hprize[3]);
	}

	# 災難賞
	if((!($flags & 64)) &&  $damage >= 500){
		$flags |= 64;
		logPrize($id, $name, $Hprize[7]);
	} elsif((!($flags & 128)) &&  $damage >= 1000){
		$flags |= 128;
		logPrize($id, $name, $Hprize[8]);
	} elsif((!($flags & 256)) &&  $damage >= 2000){
		$flags |= 256;
		logPrize($id, $name, $Hprize[9]);
	}

	$island->{'prize'} = $flags;
}

# 人口順にソート
sub islandSort {
	my($flag, $i, $tmp);

	# 人口が同じときは直前のターンの順番のまま
	my @idx = (0..$#Hislands);
	@idx = sort { $Hislands[$b]->{'pop'} <=> $Hislands[$a]->{'pop'} || $a <=> $b } @idx;
	@Hislands = @Hislands[@idx];
}
# 人口順にソート
sub teamSort {
	my($flag, $i, $tmp);

	# 人口が同じときは直前のターンの順番のまま
	my @idx = (0..$#Hteams);
	@idx = sort { $Hteams[$b]->{'pop'} <=> $Hteams[$a]->{'pop'} || $a <=> $b } @idx;
	@Hteams = @Hteams[@idx];
}

# ログへの出力
# 第1引数:メッセージ
# 第2引数:当事者
# 第3引数:相手
# 通常ログ
sub logOut {
	push(@HlogPool,"0,$HislandTurn,$_[1],$_[2],$_[0]");
}

# 遅延ログ
sub logLate {
	push(@HlateLogPool,"0,$HislandTurn,$_[1],$_[2],$_[0]");
}

# 機密ログ
sub logSecret {
	push(@HsecretLogPool,"1,$HislandTurn,$_[1],$_[2],$_[0]");
}

# 記録ログ
sub logHistory {
	open(HOUT, ">>${HdirName}/hakojima.his");
	print HOUT "$HislandTurn,$_[0]\n";
	close(HOUT);
}

# 記録ログ調整
sub logHistoryTrim {
	open(HIN, "${HdirName}/hakojima.his");
	my(@line, $l, $count);
	$count = 0;
	while($l = <HIN>) {
		chomp($l);
		push(@line, $l);
		$count++;
	}
	close(HIN);

	if($count > $HhistoryMax) {
		open(HOUT, ">${HdirName}/hakojima.his");
		my($i);
		for($i = ($count - $HhistoryMax); $i < $count; $i++) {
			print HOUT "$line[$i]\n";
		}
		close(HOUT);
	}
}

# ログ書き出し
sub logFlush {
	open(LOUT, ">${HdirName}/hakojima.log0");

	# 全部逆順にして書き出す
	my($i);
	for($i = $#HsecretLogPool; $i >= 0; $i--) {
		print LOUT $HsecretLogPool[$i];
		print LOUT "\n";
	}
	for($i = $#HlateLogPool; $i >= 0; $i--) {
		print LOUT $HlateLogPool[$i];
		print LOUT "\n";
	}
	for($i = $#HlogPool; $i >= 0; $i--) {
		print LOUT $HlogPool[$i];
		print LOUT "\n";
	}
	close(LOUT);
}

#----------------------------------------------------------------------
# ログテンプレート
#----------------------------------------------------------------------

# 勝利
sub logWin {
	my($id, $name, $money, $tName) = @_;
	$fTurn = $HfightCount + 1;
	if($HteamNumber == 4) {
		$fTurn = '決勝戦';
	} elsif($HteamNumber == 8) { 
		$fTurn = '準決勝';
	} else {
		$fTurn .= '回戦';
	}
	if($HteamNumber == 2) {
		if($id) {
			logOut("${HtagName_}${name}島${H_tagName}<B>優勝！！</B>",$id);
		} else {
			logOut("${HtagTName_}${name}${H_tagTName}が${HtagName_}${tName}${H_tagName}に勝利し、<B>優勝！！</B>");
			logHistory("${HtagTName_}${name}${H_tagTName}、<B>優勝！！</B>");
		}
	} elsif($id) {
		logOut("${HtagName_}${name}島${H_tagName}勝利し、<B>$fTurn</B>進出！",$id);
		logOut("<B>報酬金</B>として、<B>$money$HunitMoney</B>支払われました。",$id);
	} else {
		logOut("${HtagTName_}${name}${H_tagTName}が${HtagTName_}${tName}${H_tagTName}に勝利し、<B>$fTurn</B>進出！");
		logHistory("${HtagTName_}${name}${H_tagTName}、<B>$fTurn</B>進出！");
	}
}
# 死滅
sub logDead {
	my($name) = @_;
	logOut("${HtagName_}${name}${H_tagName}、敗退。");
}

# 死滅　予選落ち
sub logDeady {
	my($name) = @_;
	logOut("${HtagName_}${name}島${H_tagName}、予選落ち。");
}

# 死滅　予選落ち　チーム
sub logDeadyt {
	my($name) = @_;
	logOut("${HtagTName_}${name}${H_tagTName}、予選落ち。");
}

# 開発期間のため失敗
sub logLandNG {
	my($id, $name, $comName, $kind, $point, $cancel) = @_;
	logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、<B>$cancel</B>、実行できませんでした。",$id);
END
}

# 資金足りない
sub logNoMoney {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、資金不足のため中止されました。",$id);
}

# 食料足りない
sub logNoFood {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、備蓄食料不足のため中止されました。",$id);
}

# 対象地形の種類による失敗
sub logLandFail {
	my($id, $name, $comName, $kind, $point) = @_;
	logSecret("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、予定地の${HtagName_}$point${H_tagName}が<B>$kind</B>だったため中止されました。",$id);
END
}

# 周りに陸がなくて埋め立て失敗
sub logNoLandAround {
	my($id, $name, $comName, $point) = @_;
	logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、予定地の${HtagName_}$point${H_tagName}の周辺に陸地がなかったため中止されました。",$id);
END
}

# 整地系成功
sub logLandSuc {
	my($id, $name, $comName, $point) = @_;
	logOut("${HtagName_}${name}島$point${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id);
END
}

# 植林orミサイル基地
sub logPBSuc {
	my($id, $name, $comName, $point) = @_;
	logSecret("${HtagName_}${name}島$point${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id);
	logOut("こころなしか、${HtagName_}${name}島${H_tagName}の<B>森</B>が増えたようです。",$id);
END
}

# ハリボテ
sub logHariSuc {
	my($id, $name, $comName, $comName2, $point) = @_;
	logSecret("${HtagName_}${name}島$point${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id);
	logLandSuc($id, $name, $comName2, $point);
END
}

# ミサイル撃とうとしたが基地がない
sub logMsNoBase {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}島${H_tagName}で予定されていた${HtagComName_}${comName}${H_tagComName}は、<B>ミサイル設備を保有していない</B>ために実行できませんでした。",$id);
END
}

# ミサイル撃ったが範囲外
sub logMsOut {
	my($id, $tId, $name, $tName, $comName, $point) = @_;
	logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、<B>領域外の海</B>に落ちた模様です。",$id, $tId);
}

# ミサイル撃ったが防衛施設でキャッチ
sub logMsCaught {
	my($id, $tId, $name, $tName, $comName, $point, $tPoint) = @_;
	logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}地点上空にて力場に捉えられ、<B>空中爆発</B>しました。",$id, $tId);
}

# ミサイル撃ったが効果なし
sub logMsNoDamage {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
	logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に落ちたので被害がありませんでした。",$id, $tId);
}

# 通常ミサイル、荒地に着弾
sub logMsWaste {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
	logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に落ちました。",$id, $tId);
}

# 通常ミサイル通常地形に命中
sub logMsNormal {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
	logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中、一帯が壊滅しました。",$id, $tId);
}

# ミサイル難民到着
sub logMsBoatPeople {
	my($id, $name, $achive) = @_;
	logOut("${HtagName_}${name}島${H_tagName}にどこからともなく<B>$achive${HunitPop}もの難民</B>が漂着しました。${HtagName_}${name}島${H_tagName}は快く受け入れたようです。",$id);
}

# 資金繰り
sub logDoNothing {
	my($id, $name, $comName) = @_;
#	logOut("${HtagName_}${name}島${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id);
}

# 輸出
sub logSell {
	my($id, $name, $comName, $value) = @_;
	logOut("${HtagName_}${name}島${H_tagName}が<B>$value$HunitFood</B>の${HtagComName_}${comName}${H_tagComName}を行いました。",$id);
}

# 援助
sub logAid {
	my($id, $tId, $name, $tName, $comName, $str) = @_;
	logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}へ<B>$str</B>の${HtagComName_}${comName}${H_tagComName}を行いました。",$id, $tId);
}

# 誘致活動
sub logPropaganda {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}島${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id);
}

# 発見
sub logDiscover {
	my($name) = @_;
	logHistory("${HtagName_}${name}島${H_tagName}が発見される。");
}

# 名前の変更
sub logChangeName {
	my($name1, $name2) = @_;
	logHistory("${HtagName_}${name1}島${H_tagName}、名称を${HtagName_}${name2}島${H_tagName}に変更する。");
}

# 飢餓
sub logStarve {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}島${H_tagName}の${HtagDisaster_}食料が不足${H_tagDisaster}しています！！",$id);
}

# 食料不足被害
sub logSvDamage {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>に<B>食料を求めて住民が殺到</B>。<B>$lName</B>は壊滅しました。",$id);
}

# 地盤沈下発生
sub logFalldown {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}島${H_tagName}で${HtagDisaster_}地盤沈下${H_tagDisaster}が発生しました！！",$id);
}

# 地盤沈下被害
sub logFalldownLand {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は海の中へ沈みました。",$id);
}

# 受賞
sub logPrize {
	my($id, $name, $pName) = @_;
	logOut("${HtagName_}${name}島${H_tagName}が<B>$pName</B>を受賞しました。",$id);
	logHistory("${HtagName_}${name}島${H_tagName}、<B>$pName</B>を受賞");
}

# 受賞(チーム)
sub logTPrize {
	my($name, $pName) = @_;
	logHistory("${HtagTName_}${name}${H_tagTName}、<B>$pName</B>を受賞");
}

# 島がいっぱいな場合
sub tempNewIslandFull {
	out(<<END);
${HtagBig_}申し訳ありません、島が一杯で登録できません！！${H_tagBig}$HtempBack
END
}

# 新規で名前がない場合
sub tempNewIslandNoName {
	out(<<END);
${HtagBig_}島につける名前が必要です。${H_tagBig}$HtempBack
END
}

# 新規で名前が不正な場合
sub tempNewIslandBadName {
	out(<<END);
${HtagBig_}',?()<>\$'とか入ってたり、「無人島」とかいった変な名前はやめましょうよ〜${H_tagBig}$HtempBack
END
}

# すでにその名前の島がある場合
sub tempNewIslandAlready {
	out(<<END);
${HtagBig_}その島ならすでに発見されています。${H_tagBig}$HtempBack
END
}

# パスワードがない場合
sub tempNewIslandNoPassword {
	out(<<END);
${HtagBig_}パスワードが必要です。${H_tagBig}$HtempBack
END
}

# 島を発見しました!!
sub tempNewIslandHead {
	out(<<END);
<CENTER>
${HtagBig_}島を発見しました！！${H_tagBig}<BR>
${HtagBig_}${HtagName_}「${HcurrentName}島」${H_tagName}と命名します。${H_tagBig}<BR>
$HtempBack<BR>
</CENTER>
END
}

# 地形の呼び方
sub landName {
	my($land, $lv) = @_;
	if($land == $HlandSea) {
		if($lv == 1) {
			return '浅瀬';
		} else {
			return '海';
		}
	} elsif($land == $HlandWaste) {
		return '荒地';
	} elsif($land == $HlandPlains) {
		return '平地';
	} elsif($land == $HlandTown) {
		if($lv < 30) {
			return '村';
		} elsif($lv < 100) {
			return '町';
		} else {
			return '都市';
		}
	} elsif($land == $HlandForest) {
		return '森';
	} elsif($land == $HlandFarm) {
		return '農場';
	} elsif($land == $HlandFactory) {
		return '工場';
	} elsif($land == $HlandBase) {
		return 'ミサイル基地';
	} elsif($land == $HlandDefence) {
		return '防衛施設';
	} elsif($land == $HlandHaribote) {
		return 'ハリボテ';
	}
}

# 人口その他の値を算出
sub estimate {
	my($number) = $_[0];
	my($island);
	my($pop, $area, $farm, $factory, $burnmis, $reward, $defence, $waste) = (0, 0, 0, 0, 0, 0, 0, 0);

	# 地形を取得
	$island = $Hislands[$number];
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};

	# 数える
	my($x, $y, $kind, $value);
	for($y = 0; $y < $HislandSize; $y++) {
		for($x = 0; $x < $HislandSize; $x++) {
			$kind = $land->[$x][$y];
			$value = $landValue->[$x][$y];
			if(($kind != $HlandSea) &&
			   ($kind != $HlandSbase)){
				$area++;
				if($kind == $HlandTown) {
					# 町
					$pop += $value;
				} elsif($kind == $HlandFarm) {
					# 農場
					$farm += $value;
				} elsif($kind == $HlandFactory) {
					# 工場
					$factory += $value;
				} elsif($kind == $HlandWaste and $value == 1) {
					# 荒地
					$waste++;
				} elsif($kind == $HlandBase) {
					# ミサイル基地
					$burnmis += expToLevel($kind, $value);
					$reward++;
				} elsif($kind == $HlandDefence) {
					# 防衛施設
					$defence++;
				}
			}
		}
	}

	# 代入
	$island->{'pop'}	  = $pop;
	$island->{'area'}	 = $area;
	$island->{'farm'}	 = $farm;
	$island->{'factory'}  = $factory;
	$island->{'fire'}	 = $burnmis;
	$island->{'defence'}  = $defence;
	if($winlose == 3 and $island->{'rewflag'} == 0) {
		$island->{'reward'} = $reward + $defence * 2;
		$island->{'rewflag'} = 1;
	} elsif($winlose == 1) { 
		$island->{'waste'} = $waste;
	}
}

# 人口その他の値を算出
sub teamEstimate {
	my($number) = $_[0];
	my($island);
	$island = $Hislands[$number];
	my($HcurrentTNumber) = $HidToTeamNumber{$island->{'teamid'}};
	my($team) = $Hteams[$HcurrentTNumber];

	$team->{'pop'} += $island->{'pop'};
	$team->{'farm'} += $island->{'farm'};
	$team->{'factory'} += $island->{'factory'};
	$team->{'food'} += $island->{'food'};
	$team->{'achive'} += $island->{'achive'};
	if($winlose == 3) { $team->{'reward'} += $island->{'reward'};
	} elsif($winlose == 1) { $team->{'waste'} += $island->{'waste'}; }
	$team->{'estiMateFlag'}++;

	if($team->{'estiMateFlag'} != $HmenberCount) {
		return;
	}

	# 繁栄、災難賞
	my($pop) = $team->{'pop'};
	my($damage) = $team->{'oldPop'} - $pop;
	my($flags) = $team->{'prize'};
	my($name) = $team->{'name'};
	my($achive) = $team->{'achive'};

	# 繁栄賞
	if((!($flags & 1)) &&  $pop >= $HprizePoint[1]){
		$flags |= 1;
		logTPrize($name, $Hprize[1]);
	} elsif((!($flags & 2)) &&  $pop >= $HprizePoint[2]){
		$flags |= 2;
		logTPrize($name, $Hprize[2]);
	} elsif((!($flags & 4)) &&  $pop >= $HprizePoint[3]){
		$flags |= 4;
		logTPrize($name, $Hprize[3]);
	}

	if((!($flags & 8)) &&  $achive >= $HprizePoint[4]){
		$flags |= 8;
		logTPrize($name, $Hprize[4]);
	} elsif((!($flags & 16)) &&  $achive > $HprizePoint[5]){
		$flags |= 16;
		logTPrize($name, $Hprize[5]);
	} elsif((!($flags & 32)) &&  $achive > $HprizePoint[6]){
		$flags |= 32;
		logTPrize($name, $Hprize[6]);
	}

	# 災難賞
	if((!($flags & 64)) &&  $damage >= $HprizePoint[7]){
		$flags |= 64;
		logTPrize($name, $Hprize[7]);
	} elsif((!($flags & 128)) &&  $damage >= $HprizePoint[8]){
		$flags |= 128;
		logTPrize($name, $Hprize[8]);
	} elsif((!($flags & 256)) &&  $damage >= $HprizePoint[9]){
		$flags |= 256;
		logTPrize($name, $Hprize[9]);
	}

	$team->{'prize'} = $flags;

}


# 範囲内の地形を数える
sub countAround {
	my($land, $x, $y, $kind, $range) = @_;
	my($i, $count, $sx, $sy);
	$count = 0;
	for($i = 0; $i < $range; $i++) {
		 $sx = $x + $ax[$i];
		 $sy = $y + $ay[$i];

		 # 行による位置調整
		 if((($sy % 2) == 0) && (($y % 2) == 1)) {
			 $sx--;
		 }

		 if(($sx < 0) || ($sx >= $HislandSize) ||
			($sy < 0) || ($sy >= $HislandSize)) {
			 # 範囲外の場合
			 if($kind == $HlandSea) {
				 # 海なら加算
				 $count++;
			 }
		 } else {
			 # 範囲内の場合
			 if($land->[$sx][$sy] == $kind) {
				 $count++;
			 }
		 }
	}
	return $count;
}

# 0から(n - 1)までの数字が一回づつ出てくる数列を作る
sub randomArray {
	my($n) = @_;
	my(@list, $i);

	# 初期値
	if($n == 0) {
		$n = 1;
	}
	@list = (0..$n-1);

	# シャッフル
	for ($i = $n; --$i; ) {
		my($j) = int(rand($i+1));
		if($i == $j) { next; };
		@list[$i,$j] = @list[$j,$i];
	}

	return @list;
}

# 名前変更失敗
sub tempChangeNothing {
	out(<<END);
${HtagBig_}名前、パスワードともに空欄です${H_tagBig}$HtempBack
END
}

# 名前変更資金足りず
sub tempChangeNoMoney {
	out(<<END);
${HtagBig_}資金不足のため変更できません${H_tagBig}$HtempBack
END
}

# 名前変更成功
sub tempChange {
	out(<<END);
${HtagBig_}変更完了しました${H_tagBig}$HtempBack
END
}

1;
