#----------------------------------------------------------------------
# Ȣ����� ver2.30
# ������ʹԥ⥸�塼��(ver1.02)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# Ȣ�����Υڡ���: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# Ȣ�������ȡ��ʥ���
# ������ʹԥ⥸�塼��
# $Id: hako-turn.cgi,v 1.3 2004/02/18 05:35:38 gaba Exp $

#����2�إå����κ�ɸ
my(@ax) = (0, 1, 1, 1, 0,-1, 0, 1, 2, 2, 2, 1, 0,-1,-1,-2,-1,-1, 0);
my(@ay) = (0,-1, 0, 1, 1, 0,-1,-2,-1, 0, 1, 2, 2, 2, 1, 0,-1,-2,-2);

#----------------------------------------------------------------------
# ��ο��������⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub newIslandMain {
	# �礬���äѤ��Ǥʤ��������å�
	if($HislandNumber >= $HmaxIsland or $HislandTurn) {
		unlock();
		tempNewIslandFull();
		return;
	}

	# ̾�������뤫�����å�
	if($HcurrentName eq '') {
		unlock();
		tempNewIslandNoName();
		return;
	}

	# ̾���������������å�
	if($HcurrentName =~ /[,\?\(\)\<\>\$]|^̵��$/) {
		# �Ȥ��ʤ�̾��
		unlock();
		tempNewIslandBadName();
		return;
	}

	# ̾���ν�ʣ�����å�
	if(nameToNumber($HcurrentName) != -1) {
		# ���Ǥ�ȯ������
		unlock();
		tempNewIslandAlready();
		return;
	}

	# password��¸��Ƚ��
	if($HinputPassword eq '') {
		# password̵��
		unlock();
		tempNewIslandNoPassword();
		return;
	}

	# ��ǧ�ѥѥ����
	if($HinputPassword2 ne $HinputPassword) {
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
	}

	# ����������ֹ�����
	$HcurrentNumber = $HislandNumber;
	$HislandNumber++;
	$Hislands[$HcurrentNumber] = makeNewIsland();
	my($island) = $Hislands[$HcurrentNumber];

	# �Ƽ���ͤ�����
	$island->{'name'} = $HcurrentName;
	$island->{'id'} = $HislandNextID;
	$HislandNextID ++;
	$island->{'absent'} = 1;
	$island->{'comment'} = '(̤��Ͽ)';
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
	# �͸�����¾����
	estimate($HcurrentNumber);
	teamEstimate($HcurrentNumber);
	$team->{'member'} .= $island->{'id'} . ",";
	$team->{'money'} += $HinitialMoney;
	# �ǡ����񤭽Ф�
	writeIslandsFile($island->{'id'});
	writeTeamsFile();
	logDiscover($HcurrentName); # ��

	# ����
	unlock();

	# ȯ������
	tempNewIslandHead($HcurrentName); # ȯ�����ޤ���!!
	islandInfo(); # ��ξ���
	islandMap(1); # ����Ͽޡ�owner�⡼��
}

# ����������������
sub makeNewIsland {
	# �Ϸ�����
	my($land, $landValue) = makeNewLand();

	# ������ޥ�ɤ�����
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

	# ����Ǽ��Ĥ����
	my(@lbbs);
	for($i = 0; $i < $HlbbsMax; $i++) {
		 $lbbs[$i] = "0>>";
	}

	# ��ˤ����֤�
	return {
		'land' => $land,
		'landValue' => $landValue,
		'command' => \@command,
		'lbbs' => \@lbbs,
		'food' => $HinitialFood,
		'ownername' => '0'
	};
}

# ����������Ϸ����������
sub makeNewLand {
	# ���ܷ������
	my(@land, @landValue, $x, $y, $i);

	# ���˽����
	for($y = 0; $y < $HislandSize; $y++) {
		 for($x = 0; $x < $HislandSize; $x++) {
			 $land[$x][$y] = $HlandSea;
			 $landValue[$x][$y] = 0;
		 }
	}

	# �����4*4�˹��Ϥ�����
	my($center) = int($HislandSize / 2 - 1);
	for($y = $center - 1; $y < $center + 3; $y++) {
		 for($x = $center - 1; $x < $center + 3; $x++) {
			 $land[$x][$y] = $HlandWaste;
		 }
	}

		# �����������Ѹ���롼��
		my($size,$seacon) = (16,0);

		# 8*8�ϰ����Φ�Ϥ�����
		while($size < $HlandSizeValue){
			# �������ɸ
			$x = random(8) + $center - 3;
			$y = random(8) + $center - 3;


			my($tmp) = countAround(\@land, $x, $y, $HlandSea, 7);
			if(countAround(\@land, $x, $y, $HlandSea, 7) != 7){
				# �����Φ�Ϥ������硢�����ˤ���
				# �����Ϲ��Ϥˤ���
				# ���Ϥ�ʿ�Ϥˤ���
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

	# ������
	my($count) = 0;
	while($count < 4) {
		 # �������ɸ
		 $x = random(4) + $center - 1;
		 $y = random(4) + $center - 1;

		 # ���������Ǥ˿��Ǥʤ���С�������
		 if($land[$x][$y] != $HlandForest) {
			 $land[$x][$y] = $HlandForest;
			 $landValue[$x][$y] = 5; # �ǽ��500��
			 $count++;
		 }
	}

	# Į����
	$count = 0;
	while($count < 2) {
		 # �������ɸ
		 $x = random(4) + $center - 1;
		 $y = random(4) + $center - 1;

		 # ����������Į�Ǥʤ���С�Į����
		 if(($land[$x][$y] != $HlandTown) &&
			($land[$x][$y] != $HlandForest)) {
			 $land[$x][$y] = $HlandTown;
			 $landValue[$x][$y] = 5; # �ǽ��500��
			 $count++;
		 }
	}


	# ���Ϥ���
	$count = 0;
	while($count < $HlandFirstMiss) {
		 # �������ɸ
		 $x = random(4) + $center - 1;
		 $y = random(4) + $center - 1;

		 # ����������Į���Ǥʤ���С�����
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
# �����ѹ��⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub changeMain {
	# id����������
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	my($flag) = 0;

	# �ѥ���ɥ����å�
	if($HoldPassword eq $HspecialPassword) {
		# �ü�ѥ����
	} elsif(!checkPassword($island->{'password'},$HoldPassword)) {
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
	}

	# ��ǧ�ѥѥ����
	if($HinputPassword2 ne $HinputPassword) {
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
	}

	if($HcurrentName ne '') {
		# ̾���ѹ��ξ��		
		# ̾���������������å�
		if($HcurrentName =~ /[,\?\(\)\<\>]|^̵��$/) {
			# �Ȥ��ʤ�̾��
			unlock();
			tempNewIslandBadName();
			return;
		}

		# ̾���ν�ʣ�����å�
		if(nameToNumber($HcurrentName) != -1) {
			# ���Ǥ�ȯ������
			unlock();
			tempNewIslandAlready();
			return;
		}

		if($team->{'money'} < $HcostChangeName) {
			# �⤬­��ʤ�
			unlock();
			tempChangeNoMoney();
			return;
		}

		# ���
		if($HoldPassword ne $HspecialPassword) {
			$team->{'money'} -= $HcostChangeName;
		}

		# ̾�����ѹ�
		logChangeName($island->{'name'}, $HcurrentName);
		$island->{'name'} = $HcurrentName;
		$flag = 1;
	}

	# password�ѹ��ξ��
	if($HinputPassword ne '') {
		# �ѥ���ɤ��ѹ�
		$island->{'password'} = encode($HinputPassword);
		$flag = 1;
	}

	if($HownerName ne '') {
		# �����ʡ�̾���ѹ�
		$island->{'ownername'} = $HownerName;
		$flag = 1;
	}

	if($HcurrentID == $deleteID and $masterPassword eq $HoldPassword and $HislandTurn == 0){
		# �����⡼��
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
		# �ɤ�����ѹ�����Ƥ��ʤ�
		unlock();
		tempChangeNothing();
		return;
	}

	# �ǡ����񤭽Ф�
	writeIslandsFile($HcurrentID);
	unlock();

	# �ѹ�����
	tempChange();
}

#----------------------------------------------------------------------
# ������ʹԥ⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub turnMain {


	# ���ե��������ˤ��餹
	my($i, $j, $s, $d);
	for($i = ($HlogMax - 1); $i >= 0; $i--) {
		$j = $i + 1;
		my($s) = "${HdirName}/hakojima.log$i";
		my($d) = "${HdirName}/hakojima.log$j";
		unlink($d);
		rename($s, $d);
	}

	# ��ɸ�������
	makeRandomPointArray();

	# �������ֹ�
	$HislandTurn++;

	# ��Ʈ���֤ؤΰʹ���
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
			# �辡�����Ʈ���ֱ�Ĺ
			if($HteamNumber == 2) { $HnextCTurn += $HfigRepTurn;}
			$winlose = 3;
		}
	}

	if($HturnCount > 1) {
		$HturnCount--;
	} elsif($winlose == 1) {
		# �ǽ��������֤򹹿�
		$HislandLastTime += $HinterTime;
		$HturnCount = $HdevRepTurn;
	} elsif($HfightMode or $HislandTurn == $HnextCTurn) {
		# ��Ʈ����
		$HislandLastTime += $HfightTime;
		$HturnCount = $HfigRepTurn;
	} else {
		# ��ȯ����
		$HislandLastTime += $HunitTime;
		$HturnCount = $HdevRepTurn;
	}

	# ���ַ��
	my(@order) = randomArray($HislandNumber);

	# ����������ե�����
	for($i = 0; $i < $HislandNumber; $i++) {
		estimate($order[$i]);
		income($Hislands[$order[$i]]);

		# �����󳫻����ο͸������
		$Hislands[$order[$i]]->{'oldPop'} = $Hislands[$order[$i]]->{'pop'};
	}

	# ������ѥ���ɷ��ꡡBBS�ѥե�����˽񤭽Ф�
	for($i = 0; $i < $HteamNumber; $i++) {
		my($team) = $Hteams[$i];
		# �����󳫻����ο͸������
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

	# ���ޥ�ɽ���
	for($i = 0; $i < $HislandNumber; $i++) {
		# �����1�ˤʤ�ޤǷ����֤�
		while(doCommand($Hislands[$order[$i]]) == 0){};
	}

	# ��Ĺ�����ñ�إå����ҳ�
	for($i = 0; $i < $HislandNumber; $i++) {
		doEachHex($Hislands[$order[$i]]);
	}

	# �����ν���
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
			# �Լ�
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

	# ����Ƚ��
	if($winlose == 1) {
		my($team,@fightLog);
		for($i = 0; $i < $HteamNumber; $i++) {
			$team = $Hteams[$i];
			my($HcurrentTNumber) = $HidToTeamNumber{$team->{'fightid'}};
			my($tTeam) = $Hteams[$HcurrentTNumber];
			if($team->{'pop'} >= $tTeam->{'pop'}) {
				# ����
				# �󽷶�
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

				# �Լ�
				logDead($tTeam->{'name'});
				$tTeam->{'pop'} = -1;
				my($numTTMember) = $tTeam->{'member'};
				while($numTTMember =~ s/([0-9]*),//) {
					my($HcurrentNumber) = $HidToNumber{$1};
					my($Disland) = $Hislands[$HcurrentNumber];
					$Disland->{'pop'} = -1;
					$remainNumber--;
					logDead($Disland->{'name'} . "��");
				}
				$remainTNumber--;
			}
		}
		HfightLog(@fightLog);
	} elsif($winlose == 2) {
		# ����������
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

	# ����ε�Ͽ��¸
	open(FOUT, "${HdirName}/fight.log");
		while($f = <FOUT>){
			chomp($f);
			push(@offset,"$f\n");
		}
	close(FOUT);

	# �͸���˥�����
	islandSort();
	teamSort();

	# ������å�
	$HislandNumber = $remainNumber;
	$HteamNumber   = $remainTNumber;

	# �Хå����åץ�����Ǥ���С�������rename
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

		# ���ե���������᤹
		for($i = 0; $i <= $HlogMax; $i++) {
			rename("${HdirName}.bak0/hakojima.log$i",
				   "${HdirName}/hakojima.log$i");
		}
		rename("${HdirName}.bak0/hakojima.his",
			   "${HdirName}/hakojima.his");
	}

	# �ե�����˽񤭽Ф�
	writeIslandsFile(-1);
	writeTeamsFile();

	# ����ε�Ͽ��¸
	open(FOUT, ">${HdirName}/fight.log");
		print FOUT @offset;
	close(FOUT);

	# ���񤭽Ф�
	logFlush();

	# ��Ͽ��Ĵ��
	logHistoryTrim();

	# �ǡ����ɤ߹���
	readTeamsFile();
	readIslandsFile();

	# �ȥåפ�
	topPageMain();
}

# �ǥ��쥯�ȥ�ä�
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

# ����������ե�����
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

	# ����
	if($pop > $farm) {
		# ���Ȥ�������꤬;����
		$island->{'food'} += $farm; # ����ե��Ư
		$team->{'money'} +=
			min(int(($pop - $farm) / 10),
				 $factory );
	} else {
		# ���Ȥ����Ǽ���դξ��
		$island->{'food'} += $pop; # �������ɻŻ�
	}

	# ��������
	$island->{'food'} = int(($island->{'food'}) - ($pop * $HeatenFood));
}


# ���ޥ�ɥե�����
sub doCommand {
	my($island) = @_;
	my($HcurrentTNumber) = $HidToTeamNumber{$island->{'teamid'}};
	my($team) = $Hteams[$HcurrentTNumber];

	# ���ޥ�ɼ��Ф�
	my($comArray, $command);
	$comArray = $island->{'command'};
	$command = $comArray->[0]; # �ǽ�Τ���Ф�
	slideFront($comArray, 0); # �ʹߤ�ͤ��

	# �����Ǥμ��Ф�
	my($kind, $target, $x, $y, $arg) = 
		(
		 $command->{'kind'},
		 $command->{'target'},
		 $command->{'x'},
		 $command->{'y'},
		 $command->{'arg'}
		 );

	# Ƴ����
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
		# ��ⷫ��
		logDoNothing($id, $name, $comName);
		$team->{'money'} += 10;
		$island->{'absent'} ++;
		
		# ��ư����
		if($island->{'absent'} >= $HgiveupTurn) {
			$island->{'password'} = encode($team->{'password'});
			$island->{'comment'} = $HgiveupComment;
		}
		return 1;
	}

	$island->{'absent'} = 0;

	# �����ȥ����å�
	if($cost > 0) {
		# ��ξ��
		if($team->{'money'} < $cost) {
			logNoMoney($id, $name, $comName);
			return 0;
		}
	} elsif($cost < 0) {
		# �����ξ��
		if($island->{'food'} < (-$cost)) {
			logNoFood($id, $name, $comName);
			return 0;
		}
	}

	if(($kind == $HcomAutoPrepare3 or $kind == $HcomFastFarm) && ($HfightMode)){
		logLandNG($id, $name, $comName, $landName, $point, '������Ʈ������Τ���');
		return 0;
	}

	# ���ޥ�ɤ�ʬ��
	if(($kind == $HcomPrepare) ||
	   ($kind == $HcomPrepare2)) {
		# ���ϡ��Ϥʤ餷
		if(($landKind == $HlandSea) || 
		   ($landKind == $HlandSbase)) {
			# ����������ϡ������ϤǤ��ʤ�
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		# ��Ū�ξ���ʿ�Ϥˤ���
		$land->[$x][$y] = $HlandPlains;
		$landValue->[$x][$y] = 0;
		logLandSuc($id, $name, '����', $point);

		# ��򺹤�����
		$team->{'money'} -= $cost;

		if($kind == $HcomPrepare2) {
			# �Ϥʤ餷
			return 0;
		} else {
			return 1;
		}
	} elsif($kind == $HcomAutoPrepare3) {
		# ��缫ư�Ϥʤ餷
		my($prepareM, $preFlag) = ($HcomCost[$HcomPrepare2], 0);
		for($i = 0; $i < $HpointNumber; $i++) {
			$bx = $Hrpx[$i];
			$by = $Hrpy[$i];
			if(($land->[$bx][$by] == $HlandWaste) && ($team->{'money'} >= $prepareM)){
				# ��Ū�ξ���ʿ�Ϥˤ���
				$land->[$bx][$by] = $HlandPlains;
				$landValue->[$bx][$by] = 0;
				logLandSuc($id, $name, '����', "($bx, $by)");
				# ��򺹤�����
				$team->{'money'} -= $prepareM;
				$preFlag++;
				if($preFlag == $precheap){ $prepareM = int($prepareM * $precheap2 / 10); }
			}
		}
		# ��������񤻤�
		return 0;
	} elsif($kind == $HcomReclaim) {
		# ���Ω��
		if(($landKind != $HlandSea) &&
		   ($landKind != $HlandSbase)) {
			# ����������ϡ��������Ω�ƤǤ��ʤ�
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		# �����Φ�����뤫�����å�
		my($seaCount) =
			countAround($land, $x, $y, $HlandSea, 7) +
			countAround($land, $x, $y, $HlandSbase, 7);

		if($seaCount == 7) {
			# ���������������Ω����ǽ
			logNoLandAround($id, $name, $comName, $point);
			return 0;
		}

		if(($landKind == $HlandSea) && ($lv == 1)) {
			# �����ξ��
			# ��Ū�ξ�����Ϥˤ���
			$land->[$x][$y] = $HlandWaste;
			$landValue->[$x][$y] = 0;
			logLandSuc($id, $name, $comName, $point);
			$island->{'area'}++;

			if($seaCount <= 4) {
				# ����γ���3�إå�������ʤΤǡ������ˤ���
				my($i, $sx, $sy);

				for($i = 1; $i < 7; $i++) {
					$sx = $x + $ax[$i];
					$sy = $y + $ay[$i];

					# �Ԥˤ�����Ĵ��
					if((($sy % 2) == 0) && (($y % 2) == 1)) {
						$sx--;
					}

					if(($sx < 0) || ($sx >= $HislandSize) ||
					   ($sy < 0) || ($sy >= $HislandSize)) {
					} else {
						# �ϰ���ξ��
						if($land->[$sx][$sy] == $HlandSea) {
							$landValue->[$sx][$sy] = 1;
						}
					}
				}
			}
		} else {
			# ���ʤ顢��Ū�ξ��������ˤ���
			$land->[$x][$y] = $HlandSea;
			$landValue->[$x][$y] = 1;
			logLandSuc($id, $name, $comName, $point);
		}
		
		# ��򺹤�����
		$team->{'money'} -= $cost;
		return 1;
	} elsif($kind == $HcomDestroy) {
		# ����
		if(($landKind == $HlandSea && $lv == 0) && ($landKind == $HlandSbase)) {
			# ����������ϤϷ���Ǥ��ʤ�
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}
		# ��Ū�ξ��򳤤ˤ��롣�����ʤ鳤�ˡ�
		if($landKind == $HlandSea) {
			$landValue->[$x][$y] = 0;
		} else {
			$land->[$x][$y] = $HlandSea;
			$landValue->[$x][$y] = 1;
			$island->{'area'}--;
		}
		logLandSuc($id, $name, $comName, $point);

		# ��򺹤�����
		$team->{'money'} -= $cost;
		return 1;
	} elsif($kind == $HcomSellTree) {
		# Ȳ��
		if($landKind != $HlandForest) {
			# ���ʳ���Ȳ�ΤǤ��ʤ�
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		# ��Ū�ξ���ʿ�Ϥˤ���
		$land->[$x][$y] = $HlandPlains;
		$landValue->[$x][$y] = 0;
		logLandSuc($id, $name, $comName, $point);

		# ��Ѷ������
		$team->{'money'} += $HtreeValue * $lv;
		return 0;
	} elsif(($kind == $HcomPlant) ||
			($kind == $HcomFarm) ||
			($kind == $HcomFastFarm) ||
			($kind == $HcomFactory) ||
			($kind == $HcomBase) ||
			($kind == $HcomHaribote) ||
			($kind == $HcomDbase)) {

		# �Ͼ���߷�
		if(!
		   (($landKind == $HlandPlains) ||
			($landKind == $HlandTown) ||
			(($landKind == $HlandFarm) && ($kind == $HcomFarm)) ||
			(($landKind == $HlandFactory) && ($kind == $HcomFactory)))) {
			# ��Ŭ�����Ϸ�
			logLandFail($id, $name, $comName, $landName, $point);
			return 0;
		}

		# �����ʬ��
		if($kind == $HcomPlant) {
			# ��Ū�ξ��򿹤ˤ��롣
			$land->[$x][$y] = $HlandForest;
			$landValue->[$x][$y] = 1; # �ڤϺ���ñ��
			logPBSuc($id, $name, $comName, $point);
		} elsif($kind == $HcomBase) {
			# ��Ū�ξ���ߥ�������Ϥˤ��롣
			$land->[$x][$y] = $HlandBase;
			$landValue->[$x][$y] = 0; # �и���0
			logPBSuc($id, $name, $comName, $point);
			if($HfightMode) { $team->{'rewturn'}++; } # ��Ʈ������ϥ������
		} elsif($kind == $HcomHaribote) {
			# ��Ū�ξ���ϥ�ܥƤˤ���
			$land->[$x][$y] = $HlandHaribote;
			$landValue->[$x][$y] = 0;
			logHariSuc($id, $name, $comName, $HcomName[$HcomDbase], $point);
		} elsif(($kind == $HcomFarm) || ($kind == $HcomFastFarm)) {
			# ����
			if($landKind == $HlandFarm) {
				# ���Ǥ�����ξ��
				$landValue->[$x][$y] += 2; # ���� + 2000��
				if($landValue->[$x][$y] > 50) {
					$landValue->[$x][$y] = 50; # ���� 50000��
				}
			} else {
				# ��Ū�ξ��������
				$land->[$x][$y] = $HlandFarm;
				$landValue->[$x][$y] = 10; # ���� = 10000��
			}
			logLandSuc($id, $name, $comName, $point);
			if($kind == $HcomFastFarm){
				$team->{'money'} -= $cost;
				return 0;
			}
		} elsif($kind == $HcomFactory) {
			# ����
			if($landKind == $HlandFactory) {
				# ���Ǥ˹���ξ��
				$landValue->[$x][$y] += 10; # ���� + 10000��
				if($landValue->[$x][$y] > 100) {
					$landValue->[$x][$y] = 100; # ���� 100000��
				}
			} else {
				# ��Ū�ξ��򹩾��
				$land->[$x][$y] = $HlandFactory;
				$landValue->[$x][$y] = 30; # ���� = 10000��
			}
			logLandSuc($id, $name, $comName, $point);
		} elsif($kind == $HcomDbase) {
			# �ɱһ���
			# ��Ū�ξ����ɱһ��ߤ�
			$land->[$x][$y] = $HlandDefence;
			$landValue->[$x][$y] = 0;
			logPBSuc($id, $name, $comName, $point);
			if($HfightMode) { $team->{'rewturn'}++; } # ��Ʈ������ϥ������
		}

		# ��򺹤�����
		$team->{'money'} -= $cost;

		# ����դ��ʤ顢���ޥ�ɤ��᤹
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
		# �ߥ������
		# �������åȼ���
		my($tn) = $HidToNumber{$target};
		if($tn eq '') {
			# �������åȤ����Ǥˤʤ�
			logMsNoTarget($id, $name, $comName);
			return 0;
		}

		my($flag) = 0;
		if($arg == 0) {
			# 0�ξ��Ϸ�Ƥ����
			$arg = 10000;
		}

		# ��������
		my($tIsland) = $Hislands[$tn];
		my($tName) = $tIsland->{'name'};
		my($tLand) = $tIsland->{'land'};
		my($tLandValue) = $tIsland->{'landValue'};
		my($tx, $ty, $err);

		# ��̱�ο�
		my($boat) = 0;

		if(($HfightMode == 0) && ($tIsland->{'teamid'} != $island->{'teamid'})){
			# ��ȯ������ϥ���󥻥�
			logLandNG($id, $name, $comName, $landName, $point, '���߳�ȯ������Τ���');
			return 0;
		} elsif($HfightMode && $tIsland->{'teamid'} != $team->{'fightid'} && $tIsland->{'teamid'} != $island->{'teamid'}){
			# �������ʳ��ϥ���󥻥�
			logLandNG($id, $name, $comName, $landName, $point, '��ɸ�����������Ǥʤ�����');
			return 0;
		}  elsif($island->{'pop'} < 1000 and $HteamNumber > 2) {
			 logLandNG($id, $name, $comName, $landName, $point, '�͸���10���Ͱʲ��ΰ�');
			 return 0;
		}

		# ��
		if($kind == $HcomMissilePP) {
			$err = 7;
		} else {
			$err = 19;
		}

		# �⤬�Ԥ��뤫�������­��뤫������������Ĥޤǥ롼��
		my($bx, $by, $count) = (0,0,0);
		while(($arg > 0) &&
			  ($team->{'money'} >= $cost)) {
			# ���Ϥ򸫤Ĥ���ޤǥ롼��
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
				# ���Ĥ���ʤ��ä��餽���ޤ�
				last;
			}
			# �����Ĵ��Ϥ����ä��Τǡ�flag��Ω�Ƥ�
			$flag = 1;		   

			# ���ϤΥ�٥�򻻽�
			my($level) = expToLevel($land->[$bx][$by], $landValue->[$bx][$by]);
			# ������ǥ롼��
			while(($level > 0) &&
				  ($arg > 0) &&
				  ($team->{'money'} > $cost)) {
				# ��ä��Τ�����ʤΤǡ����ͤ���פ�����
				$level--;
				$arg--;
				$team->{'money'} -= $cost;

				# ����������
				my($r) = random($err);
				$tx = $x + $ax[$r];
				$ty = $y + $ay[$r];
				if((($ty % 2) == 0) && (($y % 2) == 1)) {
					$tx--;
				}

				# �������ϰ��⳰�����å�
				if(($tx < 0) || ($tx >= $HislandSize) ||
				   ($ty < 0) || ($ty >= $HislandSize)) {
					# �ϰϳ�
					# �̾��
					logMsOut($id, $target, $name, $tName,
								  $comName, $point);
					next;
				}

				# ���������Ϸ�������
				my($tL) = $tLand->[$tx][$ty];
				my($tLv) = $tLandValue->[$tx][$ty];
				my($tLname) = landName($tL, $tLv);
				my($tPoint) = "($tx, $ty)";

				# �ɱһ���Ƚ��
				my($defence) = 0;
				if($HdefenceHex[$id][$tx][$ty] == 1) {
					$defence = 1;
				} elsif($HdefenceHex[$id][$tx][$ty] == -1) {
					$defence = 0;
				} else {
					if($tL == $HlandDefence) {
						# �ɱһ��ߤ�̿��
						# �ե饰�򥯥ꥢ
						my($i, $count, $sx, $sy);
						for($i = 0; $i < 19; $i++) {
							$sx = $tx + $ax[$i];
							$sy = $ty + $ay[$i];

							# �Ԥˤ�����Ĵ��
							if((($sy % 2) == 0) && (($ty % 2) == 1)) {
								$sx--;
							}

							if(($sx < 0) || ($sx >= $HislandSize) ||
							   ($sy < 0) || ($sy >= $HislandSize)) {
								# �ϰϳ��ξ�粿�⤷�ʤ�
							} else {
								# �ϰ���ξ��
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
					# ��������
					# �̾��
					logMsCaught($id, $target, $name, $tName,
									 $comName, $point, $tPoint);
					next;
				}

				# �ָ��̤ʤ���hex��ǽ��Ƚ��
				if((($tL == $HlandSea) && ($tLv == 0))|| # ������
				   (($tL == $HlandSea) ||   # ���ޤ��ϡ�����
					 ($tL == $HlandSbase))) {   # ������ϰʳ�
					# ������Ϥξ�硢���Υե�
					if($tL == $HlandSbase) {
						$tL = $HlandSea;
					}
					$tLname = landName($tL, $tLv);

					# ̵����
					logMsNoDamage($id, $target, $name, $tName,
									   $comName, $tLname, $point, $tPoint);
					next;
				}

					if($tL == $HlandWaste) {
						# ����(�ﳲ�ʤ�)
						logMsWaste($id, $target, $name, $tName,
										$comName, $tLname, $point, $tPoint);
					} else {
						# �̾��Ϸ�
						logMsNormal($id, $target, $name, $tName,
										 $comName, $tLname, $point,
										 $tPoint);
					}
					# �и���
					if($tL == $HlandTown) {
						if(($land->[$bx][$by] == $HlandBase) ||
							($land->[$bx][$by] == $HlandSbase)) {
							$landValue->[$bx][$by] += int($tLv / 20);
							$boat += $tLv; # �̾�ߥ�����ʤΤ���̱�˥ץ饹
							if($landValue->[$bx][$by] > $HmaxExpPoint) {
								$landValue->[$bx][$by] = $HmaxExpPoint;
							}
						}
						$tIsland->{'pop'} -= $tLv;
					}
					
					# ���Ϥˤʤ�
					$tLand->[$tx][$ty] = $HlandWaste;
					$tLandValue->[$tx][$ty] = 1; # ������

			}

			# ����������䤷�Ȥ�
			$count++;
		}


		if($flag == 0) {
			# ���Ϥ���Ĥ�̵���ä����
			logMsNoBase($id, $name, $comName);
			return 0;
		}

		if($HfightMode) {
			# ��Ʈ������ϥ������
			$team->{'rewturn'}++;
		}

		# ��̱Ƚ��
		$boat = int($boat / 2);
		if(($boat > 0) && ($id != $target)) {
			# ��̱ɺ��
			my($achive); # ��ã��̱
			my($i);
			for($i = 0; ($i < $HpointNumber && $boat > 0); $i++) {
				$bx = $Hrpx[$i];
				$by = $Hrpy[$i];
				if($land->[$bx][$by] == $HlandTown) {
					# Į�ξ��
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
					# ʿ�Ϥξ��
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
				# �����Ǥ����夷����硢�����Ǥ�
				logMsBoatPeople($id, $name, $achive);
				$island->{'achive'} = $achive;
				# ��̱�ο���������ʾ�ʤ顢ʿ�¾ޤβ�ǽ������
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
		# ͢���̷���
		if($arg == 0) { $arg = 1; }
		my($value) = min($arg * (-$cost), $island->{'food'});

		# ͢�Х�
		logSell($id, $name, $comName, $value);
		$island->{'food'} -=  $value;
		$team->{'money'} += ($value / 10);
		return 0;
	} elsif($kind == $HcomFood) {
		# �����
		# �������åȼ���
		my($tn) = $HidToNumber{$target};
		my($tIsland) = $Hislands[$tn];
		my($tName) = $tIsland->{'name'};
		if($island->{'teamid'} != $tIsland->{'teamid'}) {
			logLandNG($id, $name, $comName, $landName, $point, '����褬¾������ΰ٤�');
			return 0;
		}
		# ����̷���
		if($arg == 0) { $arg = 1; }
		my($value, $str);
		$value = min($arg * (-$cost), $island->{'food'});
		$str = "$value$HunitFood";

		# �����
		logAid($id, $target, $name, $tName, $comName, $str);

		$island->{'food'} -= $value;
		$tIsland->{'food'} += $value;
		return 0;
	} elsif($kind == $HcomPropaganda) {
		# Ͷ�׳�ư
		if($HyosenTurn >= $HislandTurn) {
			 logLandNG($id, $name, $comName, $landName, $point, 'ͽ�����֤ΰ�');
			 return 0;
		}
		logPropaganda($id, $name, $comName);
		$island->{'propaganda'} = 1;
		$island->{'money'} -= $cost;
		return 1;
	}

	return 1;
}


# ��Ĺ�����ñ�إå����ҳ�
sub doEachHex {
	my($island) = @_;

	# Ƴ����
	my($name) = $island->{'name'};
	my($id) = $island->{'id'};
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($HcurrentTNumber) = $HidToTeamNumber{$island->{'teamid'}};
	my($team) = $Hteams[$HcurrentTNumber];

	# ������͸��Υ�����
	my($addpop)  = 10;  # ¼��Į
	my($addpop2) = 0; # �Ի�
	if($island->{'food'} < 0) {
		# ������­
		$addpop = -30;
	}
	if($island->{'absent'} >= $HstopAddPop) {
		$addpop = -10;
	} elsif($island->{'propaganda'}) {
		# Ͷ�׳�ư��
		$addpop = 30;
		$addpop2 = 3;
	}
	# �롼��
	my($x, $y, $i);
	for($i = 0; $i < $HpointNumber; $i++) {
		$x = $Hrpx[$i];
		$y = $Hrpy[$i];
		my($landKind) = $land->[$x][$y];
		my($lv) = $landValue->[$x][$y];

		if($landKind == $HlandTown) {
			# Į��
			if($addpop < 0) {
				# ��­
				$lv -= (random(-$addpop) + 1);
				if($lv <= 0) {
					# ʿ�Ϥ��᤹
					$land->[$x][$y] = $HlandPlains;
					$landValue->[$x][$y] = 0;
					next;
				}
			} elsif($addpop > 0) {
				# ��Ĺ
				if($lv < 100) {
					$lv += random($addpop) + 1;
					if($lv > 100) {
						$lv = 100;
					}
				} else {
					# �ԻԤˤʤ����Ĺ�٤�
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
			# ʿ��
			if(random(5) == 0) {
				# ��������졢Į������С�������Į�ˤʤ�
				if(countGrow($land, $landValue, $x, $y) || $island->{'propaganda'}){
					$land->[$x][$y] = $HlandTown;
					$landValue->[$x][$y] = 1;
				}
			}
		} elsif($landKind == $HlandForest) {
			# ��
			if($lv < 200) {
				# �ڤ����䤹
				$landValue->[$x][$y] += $HtreeUp;
			}
		}
	}
}

# ���Ϥ�Į�����줬���뤫Ƚ��
sub countGrow {
	my($land, $landValue, $x, $y) = @_;
	my($i, $sx, $sy);
	for($i = 1; $i < 7; $i++) {
		 $sx = $x + $ax[$i];
		 $sy = $y + $ay[$i];

		 # �Ԥˤ�����Ĵ��
		 if((($sy % 2) == 0) && (($y % 2) == 1)) {
			 $sx--;
		 }

		 if(($sx < 0) || ($sx >= $HislandSize) ||
			($sy < 0) || ($sy >= $HislandSize)) {
		 } else {
			 # �ϰ���ξ��
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

# ������
sub doIslandProcess {
	my($number, $island) = @_;

	# Ƴ����
	my($name) = $island->{'name'};
	my($id) = $island->{'id'};
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($HcurrentTNumber) = $HidToTeamNumber{$island->{'teamid'}};
	my($team) = $Hteams[$HcurrentTNumber];

	# ������­
	if($island->{'food'} < 0) {
		# ��­��å�����
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
				# 1/4�ǲ���
				if(random(4) == 0) {
					logSvDamage($id, $name, landName($landKind, $lv),
								"($x, $y)");
					$land->[$x][$y] = $HlandWaste;
					$landValue->[$x][$y] = 0;
				}
			}
		}
	}

	# ��������Ƚ��
	if(($island->{'area'} > $HdisFallBorder) &&
	   (random(1000) < $HdisFalldown)) {
		# ��������ȯ��
		logFalldown($id, $name);

		my($x, $y, $landKind, $lv, $i);
		for($i = 0; $i < $HpointNumber; $i++) {
			$x = $Hrpx[$i];
			$y = $Hrpy[$i];
			$landKind = $land->[$x][$y];
			$lv = $landValue->[$x][$y];

			if(($landKind != $HlandSea) &&
			   ($landKind != $HlandSbase)) {

				# ���Ϥ˳�������С��ͤ�-1��
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
				# -1�ˤʤäƤ�����������
				$land->[$x][$y] = $HlandSea;
				$landValue->[$x][$y] = 1;
			} elsif ($landKind == $HlandSea) {
				# �����ϳ���
				$landValue->[$x][$y] = 0;
			}

		}
	}

	# ���������դ�Ƥ��鴹��
	if($island->{'food'} > 9999) {
		$team->{'money'} += int(($island->{'food'} - 9999) / 10);
		$island->{'food'} = 9999;
	} 

	# �Ƽ���ͤ�׻�
	estimate($number);

	# �˱ɡ������
	$pop = $island->{'pop'};
	my($damage) = $island->{'oldPop'} - $pop;
	my($flags) = $island->{'prize'};


	# �˱ɾ�
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

	# �����
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

# �͸���˥�����
sub islandSort {
	my($flag, $i, $tmp);

	# �͸���Ʊ���Ȥ���ľ���Υ�����ν��֤Τޤ�
	my @idx = (0..$#Hislands);
	@idx = sort { $Hislands[$b]->{'pop'} <=> $Hislands[$a]->{'pop'} || $a <=> $b } @idx;
	@Hislands = @Hislands[@idx];
}
# �͸���˥�����
sub teamSort {
	my($flag, $i, $tmp);

	# �͸���Ʊ���Ȥ���ľ���Υ�����ν��֤Τޤ�
	my @idx = (0..$#Hteams);
	@idx = sort { $Hteams[$b]->{'pop'} <=> $Hteams[$a]->{'pop'} || $a <=> $b } @idx;
	@Hteams = @Hteams[@idx];
}

# ���ؤν���
# ��1����:��å�����
# ��2����:������
# ��3����:���
# �̾��
sub logOut {
	push(@HlogPool,"0,$HislandTurn,$_[1],$_[2],$_[0]");
}

# �ٱ��
sub logLate {
	push(@HlateLogPool,"0,$HislandTurn,$_[1],$_[2],$_[0]");
}

# ��̩��
sub logSecret {
	push(@HsecretLogPool,"1,$HislandTurn,$_[1],$_[2],$_[0]");
}

# ��Ͽ��
sub logHistory {
	open(HOUT, ">>${HdirName}/hakojima.his");
	print HOUT "$HislandTurn,$_[0]\n";
	close(HOUT);
}

# ��Ͽ��Ĵ��
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

# ���񤭽Ф�
sub logFlush {
	open(LOUT, ">${HdirName}/hakojima.log0");

	# �����ս�ˤ��ƽ񤭽Ф�
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
# ���ƥ�ץ졼��
#----------------------------------------------------------------------

# ����
sub logWin {
	my($id, $name, $money, $tName) = @_;
	$fTurn = $HfightCount + 1;
	if($HteamNumber == 4) {
		$fTurn = '�辡��';
	} elsif($HteamNumber == 8) { 
		$fTurn = '��辡';
	} else {
		$fTurn .= '����';
	}
	if($HteamNumber == 2) {
		if($id) {
			logOut("${HtagName_}${name}��${H_tagName}<B>ͥ������</B>",$id);
		} else {
			logOut("${HtagTName_}${name}${H_tagTName}��${HtagName_}${tName}${H_tagName}�˾�������<B>ͥ������</B>");
			logHistory("${HtagTName_}${name}${H_tagTName}��<B>ͥ������</B>");
		}
	} elsif($id) {
		logOut("${HtagName_}${name}��${H_tagName}��������<B>$fTurn</B>�ʽС�",$id);
		logOut("<B>�󽷶�</B>�Ȥ��ơ�<B>$money$HunitMoney</B>��ʧ���ޤ�����",$id);
	} else {
		logOut("${HtagTName_}${name}${H_tagTName}��${HtagTName_}${tName}${H_tagTName}�˾�������<B>$fTurn</B>�ʽС�");
		logHistory("${HtagTName_}${name}${H_tagTName}��<B>$fTurn</B>�ʽС�");
	}
}
# ����
sub logDead {
	my($name) = @_;
	logOut("${HtagName_}${name}${H_tagName}�����ࡣ");
}

# ���ǡ�ͽ�����
sub logDeady {
	my($name) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��ͽ�������");
}

# ���ǡ�ͽ�������������
sub logDeadyt {
	my($name) = @_;
	logOut("${HtagTName_}${name}${H_tagTName}��ͽ�������");
}

# ��ȯ���֤Τ��Ἲ��
sub logLandNG {
	my($id, $name, $comName, $kind, $point, $cancel) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ�<B>$cancel</B>���¹ԤǤ��ޤ���Ǥ�����",$id);
END
}

# ���­��ʤ�
sub logNoMoney {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ������­�Τ�����ߤ���ޤ�����",$id);
}

# ����­��ʤ�
sub logNoFood {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ����߿�����­�Τ�����ߤ���ޤ�����",$id);
}

# �о��Ϸ��μ���ˤ�뼺��
sub logLandFail {
	my($id, $name, $comName, $kind, $point) = @_;
	logSecret("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ�ͽ���Ϥ�${HtagName_}$point${H_tagName}��<B>$kind</B>���ä�������ߤ���ޤ�����",$id);
END
}

# �����Φ���ʤ������Ω�Ƽ���
sub logNoLandAround {
	my($id, $name, $comName, $point) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ�ͽ���Ϥ�${HtagName_}$point${H_tagName}�μ��դ�Φ�Ϥ��ʤ��ä�������ߤ���ޤ�����",$id);
END
}

# ���Ϸ�����
sub logLandSuc {
	my($id, $name, $comName, $point) = @_;
	logOut("${HtagName_}${name}��$point${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",$id);
END
}

# ����or�ߥ��������
sub logPBSuc {
	my($id, $name, $comName, $point) = @_;
	logSecret("${HtagName_}${name}��$point${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",$id);
	logOut("������ʤ�����${HtagName_}${name}��${H_tagName}��<B>��</B>���������褦�Ǥ���",$id);
END
}

# �ϥ�ܥ�
sub logHariSuc {
	my($id, $name, $comName, $comName2, $point) = @_;
	logSecret("${HtagName_}${name}��$point${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",$id);
	logLandSuc($id, $name, $comName2, $point);
END
}

# �ߥ������Ȥ��Ȥ��������Ϥ��ʤ�
sub logMsNoBase {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}${comName}${H_tagComName}�ϡ�<B>�ߥ�������������ͭ���Ƥ��ʤ�</B>����˼¹ԤǤ��ޤ���Ǥ�����",$id);
END
}

# �ߥ������ä����ϰϳ�
sub logMsOut {
	my($id, $tId, $name, $tName, $comName, $point) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������<B>�ΰ賰�γ�</B>����������ͤǤ���",$id, $tId);
}

# �ߥ������ä����ɱһ��ߤǥ���å�
sub logMsCaught {
	my($id, $tId, $name, $tName, $comName, $point, $tPoint) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������${HtagName_}$tPoint${H_tagName}��������ˤ��Ͼ��ª����졢<B>������ȯ</B>���ޤ�����",$id, $tId);
}

# �ߥ������ä������̤ʤ�
sub logMsNoDamage {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��������Τ��ﳲ������ޤ���Ǥ�����",$id, $tId);
}

# �̾�ߥ����롢���Ϥ�����
sub logMsWaste {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�������${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>������ޤ�����",$id, $tId);
}

# �̾�ߥ������̾��Ϸ���̿��
sub logMsNormal {
	my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�桢���Ӥ����Ǥ��ޤ�����",$id, $tId);
}

# �ߥ�������̱����
sub logMsBoatPeople {
	my($id, $name, $achive) = @_;
	logOut("${HtagName_}${name}��${H_tagName}�ˤɤ�����Ȥ�ʤ�<B>$achive${HunitPop}�����̱</B>��ɺ�夷�ޤ�����${HtagName_}${name}��${H_tagName}�ϲ����������줿�褦�Ǥ���",$id);
}

# ��ⷫ��
sub logDoNothing {
	my($id, $name, $comName) = @_;
#	logOut("${HtagName_}${name}��${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",$id);
}

# ͢��
sub logSell {
	my($id, $name, $comName, $value) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��<B>$value$HunitFood</B>��${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�����",$id);
}

# ���
sub logAid {
	my($id, $tId, $name, $tName, $comName, $str) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}��<B>$str</B>��${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�����",$id, $tId);
}

# Ͷ�׳�ư
sub logPropaganda {
	my($id, $name, $comName) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",$id);
}

# ȯ��
sub logDiscover {
	my($name) = @_;
	logHistory("${HtagName_}${name}��${H_tagName}��ȯ������롣");
}

# ̾�����ѹ�
sub logChangeName {
	my($name1, $name2) = @_;
	logHistory("${HtagName_}${name1}��${H_tagName}��̾�Τ�${HtagName_}${name2}��${H_tagName}���ѹ����롣");
}

# ����
sub logStarve {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��${HtagDisaster_}��������­${H_tagDisaster}���Ƥ��ޤ�����",$id);
}

# ������­�ﳲ
sub logSvDamage {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>��������ƽ�̱������</B>��<B>$lName</B>�ϲ��Ǥ��ޤ�����",$id);
}

# ��������ȯ��
sub logFalldown {
	my($id, $name) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��${HtagDisaster_}��������${H_tagDisaster}��ȯ�����ޤ�������",$id);
}

# ���������ﳲ
sub logFalldownLand {
	my($id, $name, $lName, $point) = @_;
	logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�ϳ���������ߤޤ�����",$id);
}

# ����
sub logPrize {
	my($id, $name, $pName) = @_;
	logOut("${HtagName_}${name}��${H_tagName}��<B>$pName</B>����ޤ��ޤ�����",$id);
	logHistory("${HtagName_}${name}��${H_tagName}��<B>$pName</B>�����");
}

# ����(������)
sub logTPrize {
	my($name, $pName) = @_;
	logHistory("${HtagTName_}${name}${H_tagTName}��<B>$pName</B>�����");
}

# �礬���äѤ��ʾ��
sub tempNewIslandFull {
	out(<<END);
${HtagBig_}����������ޤ����礬���դ���Ͽ�Ǥ��ޤ��󡪡�${H_tagBig}$HtempBack
END
}

# ������̾�����ʤ����
sub tempNewIslandNoName {
	out(<<END);
${HtagBig_}��ˤĤ���̾����ɬ�פǤ���${H_tagBig}$HtempBack
END
}

# ������̾���������ʾ��
sub tempNewIslandBadName {
	out(<<END);
${HtagBig_}',?()<>\$'�Ȥ����äƤ��ꡢ��̵����פȤ����ä��Ѥ�̾���Ϥ��ޤ��礦���${H_tagBig}$HtempBack
END
}

# ���Ǥˤ���̾�����礬������
sub tempNewIslandAlready {
	out(<<END);
${HtagBig_}������ʤ餹�Ǥ�ȯ������Ƥ��ޤ���${H_tagBig}$HtempBack
END
}

# �ѥ���ɤ��ʤ����
sub tempNewIslandNoPassword {
	out(<<END);
${HtagBig_}�ѥ���ɤ�ɬ�פǤ���${H_tagBig}$HtempBack
END
}

# ���ȯ�����ޤ���!!
sub tempNewIslandHead {
	out(<<END);
<CENTER>
${HtagBig_}���ȯ�����ޤ�������${H_tagBig}<BR>
${HtagBig_}${HtagName_}��${HcurrentName}���${H_tagName}��̿̾���ޤ���${H_tagBig}<BR>
$HtempBack<BR>
</CENTER>
END
}

# �Ϸ��θƤ���
sub landName {
	my($land, $lv) = @_;
	if($land == $HlandSea) {
		if($lv == 1) {
			return '����';
		} else {
			return '��';
		}
	} elsif($land == $HlandWaste) {
		return '����';
	} elsif($land == $HlandPlains) {
		return 'ʿ��';
	} elsif($land == $HlandTown) {
		if($lv < 30) {
			return '¼';
		} elsif($lv < 100) {
			return 'Į';
		} else {
			return '�Ի�';
		}
	} elsif($land == $HlandForest) {
		return '��';
	} elsif($land == $HlandFarm) {
		return '����';
	} elsif($land == $HlandFactory) {
		return '����';
	} elsif($land == $HlandBase) {
		return '�ߥ��������';
	} elsif($land == $HlandDefence) {
		return '�ɱһ���';
	} elsif($land == $HlandHaribote) {
		return '�ϥ�ܥ�';
	}
}

# �͸�����¾���ͤ򻻽�
sub estimate {
	my($number) = $_[0];
	my($island);
	my($pop, $area, $farm, $factory, $burnmis, $reward, $defence, $waste) = (0, 0, 0, 0, 0, 0, 0, 0);

	# �Ϸ������
	$island = $Hislands[$number];
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};

	# ������
	my($x, $y, $kind, $value);
	for($y = 0; $y < $HislandSize; $y++) {
		for($x = 0; $x < $HislandSize; $x++) {
			$kind = $land->[$x][$y];
			$value = $landValue->[$x][$y];
			if(($kind != $HlandSea) &&
			   ($kind != $HlandSbase)){
				$area++;
				if($kind == $HlandTown) {
					# Į
					$pop += $value;
				} elsif($kind == $HlandFarm) {
					# ����
					$farm += $value;
				} elsif($kind == $HlandFactory) {
					# ����
					$factory += $value;
				} elsif($kind == $HlandWaste and $value == 1) {
					# ����
					$waste++;
				} elsif($kind == $HlandBase) {
					# �ߥ��������
					$burnmis += expToLevel($kind, $value);
					$reward++;
				} elsif($kind == $HlandDefence) {
					# �ɱһ���
					$defence++;
				}
			}
		}
	}

	# ����
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

# �͸�����¾���ͤ򻻽�
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

	# �˱ɡ������
	my($pop) = $team->{'pop'};
	my($damage) = $team->{'oldPop'} - $pop;
	my($flags) = $team->{'prize'};
	my($name) = $team->{'name'};
	my($achive) = $team->{'achive'};

	# �˱ɾ�
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

	# �����
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


# �ϰ�����Ϸ��������
sub countAround {
	my($land, $x, $y, $kind, $range) = @_;
	my($i, $count, $sx, $sy);
	$count = 0;
	for($i = 0; $i < $range; $i++) {
		 $sx = $x + $ax[$i];
		 $sy = $y + $ay[$i];

		 # �Ԥˤ�����Ĵ��
		 if((($sy % 2) == 0) && (($y % 2) == 1)) {
			 $sx--;
		 }

		 if(($sx < 0) || ($sx >= $HislandSize) ||
			($sy < 0) || ($sy >= $HislandSize)) {
			 # �ϰϳ��ξ��
			 if($kind == $HlandSea) {
				 # ���ʤ�û�
				 $count++;
			 }
		 } else {
			 # �ϰ���ξ��
			 if($land->[$sx][$sy] == $kind) {
				 $count++;
			 }
		 }
	}
	return $count;
}

# 0����(n - 1)�ޤǤο��������ŤĽФƤ���������
sub randomArray {
	my($n) = @_;
	my(@list, $i);

	# �����
	if($n == 0) {
		$n = 1;
	}
	@list = (0..$n-1);

	# ����åե�
	for ($i = $n; --$i; ) {
		my($j) = int(rand($i+1));
		if($i == $j) { next; };
		@list[$i,$j] = @list[$j,$i];
	}

	return @list;
}

# ̾���ѹ�����
sub tempChangeNothing {
	out(<<END);
${HtagBig_}̾�����ѥ���ɤȤ�˶���Ǥ�${H_tagBig}$HtempBack
END
}

# ̾���ѹ����­�ꤺ
sub tempChangeNoMoney {
	out(<<END);
${HtagBig_}�����­�Τ����ѹ��Ǥ��ޤ���${H_tagBig}$HtempBack
END
}

# ̾���ѹ�����
sub tempChange {
	out(<<END);
${HtagBig_}�ѹ���λ���ޤ���${H_tagBig}$HtempBack
END
}

1;
