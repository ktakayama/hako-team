#----------------------------------------------------------------------
# �Ƽ�������
# (����ʹߤ���ʬ�γ������ͤ�Ŭ�ڤ��ͤ��ѹ����Ƥ�������)
#----------------------------------------------------------------------
# Ȣ��������ȡ��ʥ���
# ����ե�����
# $Id: hako-ini.cgi,v 1.1 2003/07/02 03:09:49 gaba Exp $

#----------------------------------------------------------------------
# �ʲ���ɬ�����ꤹ����ʬ
#----------------------------------------------------------------------

# ������Υ����ȥ�ʸ��
$Htitle = 'Ȣ��������ȡ��ʥ���';

# �ޥ������ѥ����
# ���Υѥ���ɤϡ����٤Ƥ���Υѥ���ɤ����ѤǤ��ޤ���
# �㤨�С���¾����Υѥ�����ѹ�������Ǥ��ޤ���
$masterPassword = 'password';

# �ü�ѥ����
# ���Υѥ���ɤǡ�̾���ѹ��פ�Ԥ��ȡ�������λ�⡢�����������ͤˤʤ�ޤ���
# (�ºݤ�̾�����Ѥ���ɬ�פϤ���ޤ���)
$HspecialPassword = 'special';


# ���Υե�������֤��ǥ��쥯�ȥ�
# $baseDir = 'http://�����С�/�ǥ��쥯�ȥ�';
#
# ��)
# http://cgi2.bekkoame.ne.jp/cgi-bin/user/u5534/hakoniwa/hako-main.cgi
# �Ȥ����֤���硢
# $baseDir = 'http://cgi2.bekkoame.ne.jp/cgi-bin/user/u5534/hakoniwa';
# �Ȥ��롣�Ǹ�˥���å���(/)���դ��ʤ���

$baseDir = 'http://localhost/tag';

# �����ե�������֤��ǥ��쥯�ȥ�
# $imageDir = 'http://�����С�/�ǥ��쥯�ȥ�';
$imageDir = 'http://localhost/tag/img';

# �����Υ�����������������ڡ���
$imageExp = 'http://localhost/tag/imgexp/index.html';

# jcode.pl�ΰ���

# $jcode = '/usr/libperl/jcode.pl';  # �٥å�����ξ��
# $jcode = './jcode.pl';             # Ʊ���ǥ��쥯�ȥ���֤����
$jcode = './jcode.pl';

# �ǥ��쥯�ȥ�Υѡ��ߥå����
# �̾��0755�Ǥ褤����0777��0705��0704���Ǥʤ��ȤǤ��ʤ������С��⤢��餷��
$HdirMode = 0754;

# �ǡ����ǥ��쥯�ȥ��̾��
# ���������ꤷ��̾���Υǥ��쥯�ȥ�ʲ��˥ǡ�������Ǽ����ޤ���
# �ǥե���ȤǤ�'data'�ȤʤäƤ��ޤ������������ƥ��Τ���
# �ʤ�٤��㤦̾�����ѹ����Ƥ���������
$HdirName = 'data';

# ������̾
$adminName = '������';

# �����ԤΥ᡼�륢�ɥ쥹
$email = '***@********.***';

# �Ǽ��Ĥ�̾��
$bbsname = '�Ǽ���';

# �Ǽ��ĥ��ɥ쥹
$bbs = 'http://gaba.elsia.com/tag/cgi/trees.cgi';

# Ʃ�������ΰ���
$cleangif = 'http://localhost/clean.gif';

# �������ѷǼ��ĥǥ��쥯�ȥ�̾
$teambbs = 'bbs';

# �ۡ���ڡ����Υ��ɥ쥹
$toppage = 'http://gaba.elsia.com/';

# �ǡ����ν񤭹�����

# ���å�������
# 1 �ǥ��쥯�ȥ�
# 2 �����ƥॳ����(��ǽ�ʤ�кǤ�˾�ޤ���)
# 3 ����ܥ�å����
# 4 �̾�ե�����(���ޤꤪ����Ǥʤ�)
$lockMode = 1;

# (��)
# 4�����򤹤���ˤϡ�'key-free'�Ȥ������ѡ��ߥ����666�ζ��Υե������
# ���Υե������Ʊ���֤��֤��Ʋ�������

#----------------------------------------------------------------------
# ɬ�����ꤹ����ʬ�ϰʾ�
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# �ʲ������ߤˤ�ä����ꤹ����ʬ
#----------------------------------------------------------------------
#----------------------------------------
# ������οʹԤ�ե�����ʤ�
#----------------------------------------
# ��������οͿ�
$HmenberCount = 3;

# ͽ������ �������
$HyosenTurn = 48;

# ��ȯ���� �������
$HdevTurn = 24;

# ��ȯ(ͽ��)���֡���������ޤȤ�ƿʤफ
$HdevRepTurn = 1;

# ��Ʈ���� �������
$HfigTurn = 12;

# ��Ʈ���֡���������ޤȤ�ƿʤफ
$HfigRepTurn = 3;

# ��ȯ(ͽ��)���֤ι�������
$HunitTime = 10800; # 3����

# ��Ʈ���֤ι�������
$HfightTime = 86400; # 24����

# ��Ʈ���ֽ�λ��Υ��󥿡��Х�
$HinterTime = 97200; # 27����

# �۾ｪλ������
# (���å��岿�äǡ�����������뤫)
$unlockTime = 60;

# ��κ����
$HmaxIsland = 60;

# �ȥåץڡ�����ɽ����������Υ������
$HtopLogTurn = 1;

# �����ե������ݻ��������
$HlogMax = 8; 

# �Хå����åפ򲿥����󤪤��˼�뤫
$HbackupTurn = 3;

# �Хå����åפ򲿲�ʬ�Ĥ���
$HbackupTimes = 3;

# ȯ�������ݻ��Կ�
$HhistoryMax = 10;

# �������ޥ�ɼ�ư���ϥ������
$HgiveupTurn = 5;

# ������Υ�����
$HgiveupComment = '<FONT COLOR=RED>�������¤��ꡪ</FONT>';

# ���ޥ�����ϸ³���
# (�����ब�ϤޤäƤ����ѹ�����ȡ��ǡ����ե�����θߴ�����̵���ʤ�ޤ���)
$HcommandMax = 30;

# ��������Ǽ��ĹԿ�����Ѥ��뤫�ɤ���(0:���Ѥ��ʤ���1:���Ѥ���)
$HuseLbbs = 1;

# ��������Ǽ��ĹԿ�
$HlbbsMax = 8;

# ����礭��
# (�ѹ��Ǥ��ʤ�����)
$HislandSize = 12;

# �������
$teamNum = 20;

# ͽ���̲�������
$yteamNum = 16;

# ��������Υǡ����Կ����̾�Ϥ��Τޤޤ�����פǤ���
$teamFileNum = 13;

# ¾�ͤ�����򸫤��ʤ����뤫
# 0 �����ʤ�
# 1 ������
# 2 100�ΰ̤ǻͼθ���
$HhideMoneyMode = 2;

# �ѥ���ɤΰŹ沽(0���ȰŹ沽���ʤ���1���ȰŹ沽����)
$cryptOn = 1;

# �ǥХå��⡼��(1���ȡ��֥������ʤ��ץܥ��󤬻��ѤǤ���)
$Hdebug = 0;

#----------------------------------------
# ��⡢�����ʤɤ�������
#----------------------------------------
# ������
$HinitialMoney = 2000;

# �������
$HinitialFood = 1000;

# �������
$HlandSizeValue = 32;

# ��������ο�
$HseaNum = 20;

#----------------------------------------
# ��⡢�����ʤɤ������ͤ�ñ��
#----------------------------------------
# �����ñ��
$HunitMoney = '����';

# ������ñ��
$HunitFood = '00�ȥ�';

# �͸���ñ��
$HunitPop = '00��';

# ������ñ��
$HunitArea = '00����';

# �ڤο���ñ��
$HunitTree = '00��';

# �ڤ�ñ�������������
$HtreeValue = 5;

# ̾���ѹ��Υ�����
$HcostChangeName = 0;

# �͸�1ñ�̤�����ο���������
$HeatenFood = 0.2;

# ����ߥ�������Ϥο�
$HlandFirstMiss = 0;

# ��缫ư�Ϥʤ餷��
# �����ܤι��Ϥ�����������ʤ��ο��μ��ι��Ϥ����
$precheap = 10;
# ���κݤγ��Ψ��8�ˤ����顢2����Ȥ������Ȥˤʤ�ޤ���
$precheap2 = 8;

# ����������ڤ��������ܿ�
$HtreeUp = 2;

# ��ⷫ�겿������³���ȿ͸����å��ȥåפ��뤫��
$HstopAddPop = 3;

# �������� �ƾޤμ�������
$HprizePoint[1] = '5000';   # �˱ɾ�
$HprizePoint[2] = '10000';  # Ķ�˱ɾ�
$HprizePoint[3] = '15000';  # ����˱ɾ�
$HprizePoint[4] = '500';    # ʿ�¾�
$HprizePoint[5] = '800';    # Ķʿ�¾�
$HprizePoint[6] = '1500';   # ���ʿ�¾�
$HprizePoint[7] = '1000';   # �����
$HprizePoint[8] = '2000';   # Ķ�����
$HprizePoint[9] = '3000';   # ��˺����


1;