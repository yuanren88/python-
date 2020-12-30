# python-
中文小说情节分析/角色分析/角色关系分析， 中文小说情节分析/角色分析/角色关系分析 Plot analysis / role analysis / role relationship analysis of Chinese Novels
主要函数：
textAna：
  find_name:统计小说人物名称；
  find_relation：利用同时出现原则建立人物间的关系；
  DrawAni：按百分比分一百份，连续统计人物关系，并批量绘制关系图；
TSocial：社会关系类


主要配置文件（json格式）：
  remove_words_file='removewords.json'：去除关键字列表；
  same_name_list_file='sirenjingname.json'相同名字列表；
  TEXT_PATH = 'c:/temp/死人经.txt' 小说文件。（注意，有些小说文本文件需要转换格式，在记事本选择另存--编码格式选择UTF-8）
  


![image](https://github.com/yuanren88/python-/blob/master/image/quanzhigaoshou.gif)
