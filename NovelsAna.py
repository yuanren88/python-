#coding:utf-8

# 自动提取小说的角色，情节。
#分析步骤：
#1、扫描提取主要角色名称，自动提取，手动删除，手动归类。图形分析（角色出现次数、时间线）。
#2、扫描角色关系，建立关系线，gephi图，GIF图
#3、角色关系自动判断？角色情节自动提取？情节情绪判断？人物关系程度判断？（利用情节库进行训练，进行情节归类）
#4、建立数据结构，存储分析中间结果，方便进行复现。
#5、建立Django网站提供文本分析服务：txt上载，角色列表编辑，多线程管理，关系图展示与下载，各类结果数据存储管理。
#用户表，原始文本表，角色表，关系表，
import jieba
import collections
import re
import TSocial
import json
import networkx as nx
# import matplotlib.pyplot as plt
import matplotlib
class textAna:
	def __init__(self): 
		self.G = nx.DiGraph()

	TEXT_PATH = 'c:/temp/死人经.txt'  # 文本路径
	# TEXT_PATH = 'c:/temp/射雕英雄传.txt'  # 文本路径
	person_counter = collections.defaultdict(int)	# 人物出场次数计数器
	person_per_paragraph = []
	relationships = {}
	synonymous_dict = {}
	same_name_list_file='sirenjingname.json'
	remove_words_file='removewords.json'

	pattern1 = r'[赵|钱|孙|李|周|吴|郑|王|冯|陈|褚|卫|蒋|沈|韩|杨|朱|秦|尤|许|何|吕|施|张|孔|曹|严|华|金|魏|陶|姜|戚|谢|邹|喻|柏|水|窦|章|云|苏|潘|葛|奚|范|彭|郎|鲁|韦|昌|马|苗|凤|花|方|俞|任|袁|柳|酆|鲍|史|唐|费|廉|岑|薛|雷|贺|倪|汤|滕|殷|罗|毕|郝|邬|安|常|乐|于|时|傅|皮|卞|齐|康|伍|余|元|卜|顾|孟|平|黄|和|穆|萧|尹|姚|邵|湛|汪|祁|毛|禹|狄|米|贝|明|臧|计|伏|成|戴|谈|宋|茅|庞|熊|纪|舒|屈|项|祝|董|梁|杜|阮|蓝|闵|席|季|麻|强|贾|路|娄|危|江|童|颜|郭|梅|盛|林|刁|锺|徐|邱|骆|高|夏|蔡|田|樊|胡|凌|霍|虞|万|支|柯|昝|管|卢|莫|经|房|裘|缪|干|解|应|宗|丁|宣|贲|邓|郁|单|杭|洪|包|诸|左|石|崔|吉|钮|龚|程|嵇|邢|滑|裴|陆|荣|翁|荀|羊|於|惠|甄|麴|家|封|芮|羿|储|靳|汲|邴|糜|松|井|段|富|巫|乌|焦|巴|弓|牧|隗|山|谷|车|侯|宓|蓬|全|郗|班|仰|秋|仲|伊|宫|宁|仇|栾|暴|甘|钭|历|戎|祖|武|符|刘|景|詹|束|龙|叶|幸|司|韶|郜|黎|溥|印|宿|白|怀|蒲|邰|从|鄂|索|咸|籍|卓|蔺|屠|蒙|池|乔|阳|郁|胥|能|苍|双|闻|莘|党|翟|谭|贡|劳|逄|姬|申|扶|堵|冉|宰|郦|雍|却|桑|桂|濮|牛|寿|通|边|扈|燕|冀|浦|尚|农|温|别|庄|晏|柴|瞿|充|慕|连|茹|习|宦|艾|鱼|容|向|古|易|慎|戈|廖|庾|终|暨|居|衡|步|都|耿|满|弘|匡|国|文|寇|广|禄|阙|东|欧|沃|利|蔚|越|夔|隆|师|巩|厍|聂|晁|勾|敖|融|冷|訾|辛|阚|那|简|饶|空|曾|毋|沙|乜|养|鞠|须|丰|巢|关|蒯|相|荆|红|游|竺|权|司马|上官|欧阳|夏侯|诸葛|闻人|东方|赫连|皇甫|尉迟|公羊|澹台|公冶宗政|濮阳|淳于|单于|太叔|申屠|公孙|仲孙|轩辕|令狐|钟离|宇文|长孙|慕容|司徒|司空|召|有|舜|岳|黄辰|寸|贰|皇|侨|彤|竭|端|赫|实|甫|集|象|翠|狂|辟|典|良|函|芒|苦|其|京|中|夕|乌孙|完颜|富察|费莫|蹇|称|诺|来|多|繁|戊|朴|回|毓|鉏|税|荤|靖|绪|愈|硕|牢|买|但|巧|枚|撒|泰|秘|亥|绍|以|壬|森|斋|释|奕|姒|朋|求|羽|用|占|真|穰|翦|闾|漆|贵|代|贯|旁|崇|栋|告|休|褒|谏|锐|皋|闳|在|歧|禾|示|是|委|钊|频|嬴|呼|大|威|昂|律|冒|保|系|抄|定|化|莱|校|么|抗|祢|綦|悟|宏|功|庚|务|敏|捷|拱|兆|丑|丙|畅|苟|随|类|卯|俟|友|答|乙|允|甲|留|尾|佼|玄|乘|裔|延|植|环|矫|赛|昔|侍|度|旷|遇|偶|前|由|咎|塞|敛|受|泷|袭|衅|叔|圣|御|夫|仆|镇|藩|邸|府|掌|首|员|焉|戏|可|智|尔|凭|悉|进|笃|厚|仁|业|肇|资|合|仍|九|衷|哀|刑|俎|仵|圭|夷|徭|蛮|汗|孛|乾|帖|罕|洛|淦|洋|邶|郸|郯|邗|邛|剑|虢|隋|蒿|茆|菅|苌|树|桐|锁|钟|机|盘|铎|斛|玉|线|针|箕|庹|绳|磨|蒉|瓮|弭|刀|疏|牵|浑|恽|势|世|仝|同|蚁|止|戢|睢|冼|种|涂|肖|己|泣|潜|卷|脱|谬|蹉|赧|浮|顿|说|次|错|念|夙|斯|完|丹|表|聊|源|姓|吾|寻|展|出|不|户|闭|才|无|书|学|愚|本|性|雪|霜|烟|寒|少|字|桥|板|斐|独|千|诗|嘉|扬|善|揭|祈|析|赤|紫|青|柔|刚|奇|拜|佛|陀|弥|阿|素|长|僧|隐|仙|隽|宇|祭|酒|淡|塔|琦|闪|始|星|南|天|接|波|碧|速|禚|腾|潮|镜|似|澄|潭|謇|纵|渠|奈|风|春|濯|沐|茂|英|兰|檀|藤|枝|检|生|折|登|驹|骑|貊|虎|肥|鹿|雀|野|禽|飞|节|宜|鲜|粟|栗|豆|帛|官|布|衣|藏|宝|钞|银|门|盈|庆|喜|及|普|建|营|巨|望|希|道|载|声|漫|犁|力|贸|勤|革|改|兴|亓|睦|修|信|闽|北|守|坚|勇|汉|练|尉|士|旅|五|令|将|旗|军|行|奉|敬|恭|仪|母|堂|丘|义|礼|慈|孝|理|伦|卿|问|永|辉|位|让|尧|依|犹|介|承|市|所|苑|杞|剧|第|零|谌|招|续|达|忻|六|鄞|战|迟|候|宛|励|粘|萨|邝|覃|辜|初|楼|城|区|局|台|原|考|妫|纳|泉|老|清|德|卑|过|麦|曲|竹|百|福|言|第五|佟|爱|年|笪|谯|哈|墨|连|南宫|赏|伯|佴|佘|牟|商|西门|东门|左丘|梁丘|琴|后|况|亢|缑|帅|微生|羊舌|海|归|呼延|南门|东郭|百里|钦|鄢|汝|法|闫|楚|晋|谷梁|宰父|夹谷|拓跋|壤驷|乐正|漆雕|公西|巫马|端木|颛孙|子车|督|仉|司寇|亓官|三小|鲜于|锺离|盖|逯|库|郏|逢|阴|薄|厉|稽|闾丘|公良|段干|开|光|操|瑞|眭|泥|运|摩|郄|伟|铁|迮|木|荷|虚|君][\u4e00-\u9fa5]{1,3}$'

	'''
	person_counter是一个计数器，用来统计人物出现的次数。{'a':1,'b':2}
	person_per_paragraph每段文字中出现的人物[['a','b'],[]]
	relationships保存的是人物间的关系。key为人物A，value为字典，包含人物B和权值。
	'''

	def get_clean_paragraphs(self):
		# 读取文件
		# fn = open('QTSK2.txt') # 打开文件
		fn = open(self.TEXT_PATH, encoding='UTF-8') # 打开文件
		paragraphs = fn.readlines() # 读出整个文件
		fn.close() # 关闭文件
		para=[]
		# 文本预处理
		pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"') # 定义正则表达式匹配模式
		for p in paragraphs:
			p1=[]
			p= re.sub(pattern, '', p)
			p1=p.split('。')
			# if len(p)>0:
			# 	para.append(p) # 将符合模式的字符去除
			for pp1 in p1:
				para.append(pp1) 
		return para
		
	Social_list_str=[]
	#寻找角色关系 dead_line 表示截至统计点
	def find_relation(self,dead_line):
		'''
		1、人物名称添加jieba自定义字典
		2、分割段落
		3、段落分析，关系入库。
		'''
		paragraphs = self.get_clean_paragraphs()
		# same_name_list=[['顾慎为','龙王','小顾','杨欢','欢奴'],['荷女','御众师'],['上官如','九公子'],['上官怒','八少主'],['大头神'],['罗宁茶','八少奶'],['上官伐','堡主','独步王'],['屠狗'],['许小益','小益','许益'],['许烟微'],['遥奴'],['木老头'],['杨元帅'],['顾仑'],['杨峥'],['顾翠兰','翠兰']]
		same_name_list=[]
		newfile= open(self.same_name_list_file, 'r',encoding='gb18030')  
		s=newfile.read()
		same_name_list=json.loads(s)

		# jieba.load_userdict('namedict.txt')
		# for p in paragraphs:
		# 	pp=jieba.cut(p)
		# 	for x in pp:
		# 		if x in same_name_list[0]:
		# 			print(p)
		# 			continue
		#初始化角色名称信息列表  name_info_list
		#角色名称信息包含角色名称、角色使用名称，角色出现计数，角色出现语句列表，角色关系。 name_info={'name':'顾慎为','same_name':['顾慎为','龙王','小顾','杨欢','欢奴'],'name_count':133,'paragraphs':[],'tss':[]}
		name_info_list=[]
		nameID=1
		for n in same_name_list:
			name_info={}
			tss=TSocial.TSocial()
			tss.Bubble=n[0]
			name_info['nameID']=nameID
			nameID+=1
			name_info['name']=tss.Bubble=n[0]
			name_info['tss']=tss
			name_info['name_count']=0
			name_info['same_name']=n
			name_info_list.append(name_info)
		
		#开始逐句搜索关系
		p_count=0  
		for p in paragraphs:
			p_count+=1
			if p_count/len(paragraphs) >dead_line/100:
				break
			
			#统计段落包含的角色名称
			name_in_p=[]
			for name_info in name_info_list:
				for sn in name_info['same_name']:
					if sn in p:
						name_info['name_count']+=1
						name_in_p.append(name_info)
			if len(name_in_p)<=1:
				continue
			# 开始处理关系线
			p1=p.replace(' ','')			
			Scene={'eventname':p1[0:8],'roundcount':p_count} #paragraphs.index(p)}
			for name_info in name_info_list:
				if name_info not in name_in_p:
					continue
				for name_info_other in name_in_p:
					if name_info_other['name'] in name_info['tss'].OtherIDs:
						name_info['tss'].RelationsModify(Scene,name_info_other['name'])#维护旧关系
					else:
						name_info['tss'].RelationsRegist1(Scene,name_info_other['name'])#注册新关系
			

		# print(name_info_lisjt)
		print(paragraphs[p_count-2])
		#关系结果输出到字符串Social_list_str
		for n in name_info_list:
			x=n['tss'].ToDic()
			x['主人ID']=n['nameID']
			x['主人姓名']=n['name']
			self.Social_list_str.append(x)
		#作图
		self.MakeMatplot(self.Social_list_str)
		self.Drawplt()

	def MakeMatplot(self,j):
		# print (matplotlib.matplotlib_fname()) # 将会获得matplotlib包所在文件夹
		matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS']
		matplotlib.rcParams['font.serif'] = ['Arial Unicode MS']
		# 显示matplatlib全部字体
		# plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
		# a=sorted([f.name for f in matplotlib.font_manager.fontManager.ttflist])  
		# for i in a:  
		#     print (i)  

		import seaborn as sns
		sns.set_style("darkgrid",{"font.sans-serif":['Arial Unicode MS', 'Arial']})

		# print(j)
		#         import json
		#         j = json.dumps(BubbleList.Bubbles[0].MySocial.ToDic(), ensure_ascii=False)
		for SocialText in j:
			if SocialText['关系数量']!=0:
				self.G.add_node(SocialText['主人姓名'],node_color='b',weight=SocialText['关系数量'])
		for SocialText in j:
			for gx in SocialText['关系']:
				self.G.add_edge(SocialText['主人姓名'],gx['对端姓名'],weight=gx['交往密切程度'])

	def Drawplt(self):
		# print("输出全部节点：{}".format(self.G.nodes()))
		# print("输出全部边：{}".format(self.G.edges()))
		print("输出全部点的数量：{}".format(self.G.number_of_nodes()))        
		print("输出全部边的数量：{}".format(self.G.number_of_edges()))
		nx.draw_networkx(self.G, edge_color='b',node_shape = 'o', node_size=800,cmap=matplotlib.pyplot.cm.gray,dpi = 4000)
		matplotlib.pyplot.show()
		


	def find_name(self):
		# 读取文件
		# fn = open('QTSK2.txt') # 打开文件
		fn = open(self.TEXT_PATH, encoding='UTF-8') # 打开文件
		string_data = fn.read() # 读出整个文件
		fn.close() # 关闭文件

		# 文本预处理
		pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"|的') # 定义正则表达式匹配模式
		string_data = re.sub(pattern, '', string_data) # 将符合模式的字符去除

		# 文本分词
		seg_list_exact = jieba.cut(string_data, cut_all = False) # 精确模式分词
		object_list = []
		remove_words = [u'的', u'，',u'和', u'是', u'随着', u'对于', u'对',u'等',u'能',u'都',u'。',u' ',u'、',u'中',u'在',u'了',
						u'通常',u'如果',u'我们',u'需要',u'卷',u'_',u'【',u'】',u'·',u'\u3000',u'：',u'“',u'”',u'我',u'道',u'他',u'说',
						u'你',u'也',u'人',u'但是',u'就',u'一个',u'自己',u'这',u'但',u'不',u'没有',u'有',u'被',u'要',u'就是',
						u'这个',u'他们',u'到',u'并',u'！',u'（',u'）',u'而',u'已经',u'还',u'却',u'着',u'不是',u'很',u'会',u'？',u'上',
						u'[',u']',u'们',u'去',u'这些',u'这样',u'先',u'因为',u'把',u'后',u'什么',u'让',u'可以',u'地',u'来',u'—',u'不过',
						u'这种',u'将',u'那',u'从',u'虽然',u'还是',u'这位',u'给',u'个',u'十分',u'又',u'与',u'下',u'做',u'过',u'好',
						u'很多',u'得',u'实在',u'用',u'终于',u'此时',u'呢',u'可能',u'不能',u'时',u'开始',u'似乎',u'之',u'可',
						u'时候',u'才',u'应该',u'可是',u'于是',u'吧',u'向',u'现在',u'当',u'能够',u'想',u'之后',u'多',u'她',
						u'还有',u'所以',u'这里',u'便',u'所谓',u'说道',u'你们',u'只',u'…',u'见',u'跟',u'一声',u'请',u'谁',
						u'有点',u'以为',u'公子',u'有人',u'士兵',u'出来',u'计划',u'许多',u'仍然',u'武功',u'说话',u'不想',u'军队',u'请',u'谁',
						u'问道',u'咱们',u'已',u'再',u'罢',u'怎么',u'不知',u'只见',u'里',u'啊',u'本书',u'小说网',u'用户',u'明白',u'希望',u'那个'] # 自定义去除词库

		name_list=[]
		# for word in seg_list_exact: # 循环读出每个分词
		# 	if word not in remove_words: # 如果不在去除词库中
		# 		object_list.append(word) # 分词追加到列表
		# 		match = re.match(self.pattern1,word)
		# 		if match != None:
		# 			name_list.append(word)
		name_found=0
		name_1=''
		name_2=''
		name_3=''
		for word in seg_list_exact: # 循环读出每个分词
			if word not in remove_words: # 如果不在去除词库中
				object_list.append(word) # 分词追加到列表
				match = re.match(self.pattern1,word)
				if match != None and len(word)>=2:
					name_list.append(word)	
								
				
				if match != None and name_found==0:
					name_found=1
					name_1=word
					# if word =='木':
					# 	print(word)
					continue
				

				if name_found==1 and len(name_2)==1 and len(word)==1:
					name_3=word
					name_found=0
					name_list.append(name_1+name_2+name_3)
					name_2=''
					name_3=''
					continue
				if name_found==1 and len(word)==1: 
					name_2=word
					if len(name_1+name_2)>=3:
						name_found=0
						name_list.append(name_1+name_2)
						name_2=''
						name_3=''	
						continue					
						
				if name_found==1 and len(word)==2:
					name_2=word
					name_found=0
					name_list.append(name_1+name_2)
					name_2=''
		# 词频统计
		# word_counts = collections.Counter(object_list) # 对分词做词频统计
		# word_counts_top10 = word_counts.most_common(40) # 获取前10最高频的词
		word_counts = collections.Counter(name_list) # 对分词做词频统计
		word_counts_top10 = word_counts.most_common(40) # 获取前10最高频的词		
		print (word_counts_top10) # 输出检查



	#寻找作品中的名字并统计
	def find_name1(self):
		# 读取文件
		# fn = open('QTSK2.txt') # 打开文件
		fn = open(self.TEXT_PATH, encoding='UTF-8') # 打开文件
		string_data = fn.read() # 读出整个文件
		fn.close() # 关闭文件

		# 文本预处理
		pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"') # 定义正则表达式匹配模式
		string_data = re.sub(pattern, '', string_data) # 将符合模式的字符去除

		# 文本分词
		seg_list_exact = jieba.cut(string_data, cut_all = False) # 精确模式分词
		
		object_list = []
		remove_words = [] # 自定义去除词库
		# with open('removewords1s.json', 'w') as f_obj:  
		# 	json.dump(remove_words, f_obj,ensure_ascii=False)
		with open(self.remove_words_file, 'r', encoding='utf-8') as f_obj:
			remove_words = json.load(f_obj)
		name_list=[]

		name_found=0
		name_1=''
		name_2=''
		name_3=''	
		tnames=[]

		def comp_name(thename):
			if thename not in remove_words and '的' not in thename :	
				if re.match(self.pattern1,thename)!=None:
					name_list.append(thename)

		for i in range(10,len(string_data)):
			if i>10:
				name_1=string_data[i-2]+string_data[i-1]+string_data[i]
				comp_name(name_1)
				name_1=string_data[i-1]+string_data[i]
				comp_name(name_1)
				name_1=string_data[i-3]+string_data[i-2]+string_data[i-1]+string_data[i]
				comp_name(name_1)

		# 词频统计
		word_counts = collections.Counter(name_list) # 对分词做词频统计
		word_counts_top10 = word_counts.most_common(500) # 获取前10最高频的词	
		word_counts_top=[]
		def quchong():#去除名字列表中的重复。
			Flag=0
			for name01 in word_counts_top10:
				Flag=0
				if name01 in word_counts_top:
					continue
				for name02 in word_counts_top10:
					if (name01[0] in name02[0])  and (name01[0] != name02[0]) and abs((name01[1]/name02[1])-1)<0.09:
						Flag=1
						if name02 not in word_counts_top:
							word_counts_top.append(name02) 	
				if Flag==0:
					if name01 not in word_counts_top:
						word_counts_top.append(name01) 	
	
		quchong()
		word_counts_top10=word_counts_top
		word_counts_top=[]
		quchong()
		
		print (word_counts_top) # 输出检查
		print('\n')
		name_single=[]
	
		for w in word_counts_top :
			x=[]
			x.append(w[0])
			name_single.append(x)
		print(name_single)


word_counts_top10=[('叶修', 21713), ('兴欣', 8842), ('莫笑', 8763), ('战队', 7530), ('陈果', 7039), ('公会', 6091), ('唐柔', 4653), ('嘉世', 3787), ('包子', 3674), ('叶修说', 3439), ('方锐', 3261), ('苏沐橙', 3122), ('荣耀', 3053), ('家伙', 2892), ('魏琛', 2888), ('战斗', 2674), ('操作', 2659), ('说着', 2446), ('黄少天', 2309), ('居然', 2384), ('叶秋', 2324), ('人不倦', 2149), ('孙翔', 2054), ('包子入', 1995), ('子入侵', 1992), ('包子入侵', 1992), ('寒烟柔', 1944), ('赛季', 1942), ('业选手', 1874), ('有什', 1865), ('蓝河', 1852), ('那边', 1850), ('生命', 1841), ('大神', 1826), ('游戏', 1822), ('百花', 1792), ('蓝雨', 1786), ('是很', 1727), ('连忙', 1659), ('顿时', 1608), ('乔一帆', 1580), ('却也', 1580), ('肖时钦', 1577), ('周泽楷', 1565), ('李艺博', 1575), ('潘林', 1561), ('法师', 1535), ('莫凡', 1530), ('实力', 1486), ('相当', 1478), ('海无量', 1442), ('上来', 1399), ('位置', 1398), ('乐部', 1390), ('张新杰', 1364), ('么一', 1347), ('是什', 1336), ('战术', 1328), ('在了', 1325), ('是叶', 1314), ('本就', 1310), ('叶之秋', 1293), ('方面', 1296), ('微草', 1288), ('节奏', 1274), ('有了', 1258), ('呼啸', 1253), ('上了', 1251), ('经验', 1221), ('开了', 1217), ('沐雨橙', 1214), ('沐雨橙风', 1213), ('局面', 1207), ('牧师', 1181), ('张佳乐', 1171), ('刘皓', 1156), ('依然', 1152), ('明星', 1152), ('韩文清', 1135), ('毕竟', 1131), ('三人', 1130), ('大公会', 1126), ('完成', 1121), ('双方', 1117), ('王杰希', 1114), ('无敌最', 1034), ('无敌最俊', 1025), ('是他们', 1106), ('林敬言', 1078), ('楼兰', 1068), ('不错', 1065), ('方向', 1057), ('全明星', 1040), ('都已经', 970), ('千机伞', 1044), ('让人', 1040), ('水平', 1035), ('召唤', 987), ('频道', 977), ('那样', 972), ('战赛', 969), ('家都', 967), ('方式', 960), ('喻文州', 948), ('战斗法师', 952), ('接下来', 876), ('骑士', 933), ('和他', 926), ('在那', 921), ('剑士', 912), ('蒋游', 912), ('那就', 905), ('武器', 893), ('叶修这', 885), ('况下', 880), ('烟雨', 880), ('赛中', 876), ('台赛', 870), ('五人', 863), ('是叶修', 856), ('小手冰', 788), ('小手冰凉', 787), ('蓝溪阁', 851), ('招呼', 847), ('经是', 845), ('江波涛', 840), ('陈夜辉', 833), ('么多', 833), ('空中', 833), ('寸灰', 829), ('兴欣战队', 804), ('速度', 809), ('第十', 806), ('么样', 804), ('说是', 803), ('在是', 803), ('百分', 801), ('关注',795), ('经不', 793), ('第一千', 790), ('但这', 785), ('范围', 784), ('却还', 777), ('义斩', 777), ('有可', 775), ('卢瀚文', 749), ('是无', 765), ('季后赛', 740), ('出这', 754), ('是可', 753), ('不断', 747), ('纪录', 747), ('随便', 743), ('大招', 739), ('老板', 736), ('时也', 736),('是没有', 733), ('出场', 730), ('声烦', 725), ('安文逸', 708), ('罗辑', 714), ('频道里', 676), ('能是', 707), ('飞快', 691), ('业圈', 689),('本没', 681), ('有可能', 680), ('时就', 679), ('应对', 679), ('来就', 674), ('道这', 673), ('大家都', 672), ('出来了', 665), ('后就', 663),('是比', 661), ('波动', 660), ('杜明', 660), ('是兴欣', 623), ('是可以', 651), ('不只', 651), ('陈果说', 650), ('可就', 647), ('解说', 643),('系统', 641), ('是相', 640), ('无极', 637), ('雷霆', 636), ('于锋', 633), ('成绩', 632), ('第十区', 630), ('让他们', 626), ('百分之', 623),('不是一', 619), ('却已', 618), ('关键', 618), ('却又', 616), ('赵禹哲', 615), ('全没', 615), ('施展', 613), ('王朝', 611), ('但是这', 611),('叶修一', 599), ('不及', 610), ('风格', 607), ('兴欣这', 601), ('不够', 600), ('刚才', 599), ('赛场', 596), ('安排', 594), ('无奈', 594), ('大漠孤', 592), ('大漠孤烟', 591), ('布阵', 591), ('是现', 590), ('实上', 589), ('家公会', 582), ('叶修也', 586), ('定是', 588), ('完全不', 571), ('能不', 581), ('唐昊', 578), ('原本', 576), ('能力', 575), ('无疑', 571), ('普通玩家', 569), ('普通玩', 569), ('通玩家', 569), ('实在是', 568), ('是说', 568), ('在不', 568), ('邱非', 568), ('圣诞', 567), ('在这一', 566), ('完全没', 564), ('闪避', 564), ('进了', 563), ('向了',562), ('是会', 558), ('和叶', 557), ('小怪', 557), ('在此', 556), ('过程', 554), ('望着', 553), ('子弹', 551), ('人赛', 551), ('所有人都', 545), ('伍晨', 543), ('高英杰', 534), ('嘉王朝', 535), ('左右', 535), ('但在', 534), ('程度', 534), ('田七', 533), ('春易老', 498), ('来看', 527), ('赛里', 527), ('是现在', 525), ('是看', 524), ('相比', 521), ('来越', 521), ('虚空', 521), ('三零一', 492), ('是让', 518), ('功师', 518), ('有些不', 515), ('连续', 512), ('用了', 511), ('无比', 511), ('是相当', 511), ('度寒潭', 501), ('完了', 510), ('练级', 510), ('无浪', 510), ('却已经', 508), ('那种', 508), ('风布阵', 506), ('实是', 503), ('叶修问', 501), ('陶轩', 501), ('经有', 499), ('不过这', 497), ('战矛', 495), ('常先', 494), ('清晰', 493), ('野图', 492), ('业联', 491), ('回复', 490), ('是这一', 488), ('空当', 488), ('回道', 487), ('有一些', 486), ('有任何', 478), ('出了一', 485), ('孙哲平', 483), ('考虑', 482), ('有意', 482), ('在此时', 481), ('接连', 481), ('在场', 481), ('郁闷', 480), ('本就是', 479), ('不说', 479), ('厉害', 477), ('叶修和', 474), ('在他们', 474), ('上场', 474), ('遇到', 473), ('是职业', 469), ('是如',469), ('第四', 469), ('楼冠宁', 469), ('有没有', 454), ('元素', 467), ('不算', 464), ('干脆', 463), ('不至于', 456), ('来是', 459), ('是以',459), ('察觉', 458), ('连击', 456), ('在这样', 454), ('是叶秋', 452), ('叶修说着', 447), ('是和', 451), ('出现在', 450), ('随即', 449), ('经开', 448), ('是完', 448), ('和叶修', 448), ('是太', 447), ('说什么', 446), ('掌握', 446), ('赫然', 446), ('飞出', 445), ('任何一', 440), ('三位', 444), ('完全没有', 436), ('依旧', 440), ('有时', 440), ('李艺博说', 440), ('回头', 439), ('有这样', 438), ('正面', 438), ('但现在', 425), ('人们', 437), ('于这', 435), ('在网', 434), ('有过', 434), ('经被', 430), ('以说', 429), ('吕泊远', 429), ('留意', 428), ('休息', 427), ('狂剑', 427), ('五个', 426), ('表情', 426), ('可惜', 425), ('么一个', 425), ('无极战队', 425), ('花缭乱', 424), ('百花缭', 390), ('百花缭乱',390), ('在第', 422), ('用这', 422), ('不大', 421), ('但是他', 420), ('是此', 419), ('波动剑', 419), ('空间', 418), ('法力', 416), ('是第', 416), ('坚持', 416), ('世界', 415), ('是两', 414), ('召唤兽', 414), ('针对', 413), ('时一', 413), ('在这个', 411), ('叶修他', 410), ('修他们',404), ('叶修他们', 403), ('和包子', 405), ('但也', 409), ('法术', 406), ('回了', 405), ('通过', 405), ('千成', 405), ('却都', 403), ('大多',402), ('强力', 402), ('以他', 400), ('支队', 400), ('冷却', 399), ('集中', 399), ('却还是', 398), ('那也', 398), ('强大', 397), ('达到', 394), ('不得不', 393), ('经开始', 393), ('时不', 393), ('时机', 393), ('云山乱', 392), ('有两', 392), ('能在', 392), ('第六', 390), ('嘉世战', 389), ('么不', 389), ('来得', 389), ('以来', 389)]

word_counts_top=[]
def quchong1():#去除名字列表中的重复。
	Flag=0
	for name01 in word_counts_top10:
		Flag=0
		if name01 in word_counts_top:
			continue
		for name02 in word_counts_top10:
			if (name01[0] in name02[0])  and (name01[0] != name02[0]) and abs((name01[1]/name02[1])-1)<0.09:
				Flag=1
				if name02 not in word_counts_top:
					word_counts_top.append(name02) 	
		if Flag==0:
			if name01 not in word_counts_top:
				word_counts_top.append(name01) 	


quchong1()
# print(word_counts_top)

# same_name_list=[['顾慎为','龙王','小顾','杨欢','欢奴'],['荷女','御众师'],['上官如','九公子'],['上官怒','八少主'],['大头神'],['罗宁茶','八少奶'],['上官伐','堡主','独步王'],['屠狗'],['许小益','小益','许益'],['许烟微'],['遥奴'],['木老头'],['杨元帅'],['顾仑'],['杨峥'],['顾翠兰','翠兰']]
# with open('sirenjingname.json', 'w') as f_obj:  
# 	json.dump(same_name_list, f_obj,ensure_ascii=False)
# same_name_list.clear()

textA=textAna()
textA.remove_words_file='removewords.json'
textA.same_name_list_file='sirenjingname.json'
textA.TEXT_PATH = 'c:/temp/死人经.txt' 
# textA.same_name_list_file='sanguo.json'
# textA.TEXT_PATH = 'c:/temp/三国演义.txt' 

# print(match)
# textA.find_name1()
# textA.count_person()
i=-1
deal_line=0

# for i in range(1,100):
# 	textA.find_relation(deal_line)

while 1:
	i=(input('输入时间点：'))
	if int(i) ==0 or len(i)==0:
		break
	deal_line+=int(i)
	print('deal_line=',deal_line)
	textA.find_relation(deal_line)


# textA.count_person()
print('\n')
result = jieba.tokenize(u' 顾慎为平常无事也要生非，这时和父亲一样，将事态看得很“严重”，一本正经地骑着小马在庄园外四处巡逻，一有风吹草动就快马加鞭跑过去，务必要确认那是一只兔子还是一只飞鸟。', mode='search')
seg_list_exact=jieba.cut(u'   从雪娘的角度来看，荷女是一名优秀的弟子。', cut_all = False)
object_list=[]
for word in seg_list_exact: # 循环读出每个分词
    # if word not in remove_words: # 如果不在去除词库中
    object_list.append(word) # 分词追加到列表
print(object_list)

