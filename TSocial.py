#-- coding:UTF-8 --
'''
社会关系及社交能力 TSocial
    个人关系  TRelationship
        共同经历： TSocialLine
            当时—建立关系线
            过后—回忆，维护关系线'''

#类：社交线 描述两者之间每一次的接触
class TSocialLine:
    def __init__(self): 
        self.OnActive=0 #是否有效，true：有效，false：失效。。
        self.LineState='' #关系线状态
        self.OtherID=0    #对端ID
        self.OtherIDName=''  #对端姓名
        self.POther=0 #对端地址
        self.SpcialSocialType=''        #特殊的交往类型：如夫妻，奴役，师徒，上下级等等。
        self.CreateTime=0               #创建时间-回合
#解析场景
    def ExplanScene(self,Scene):
#         self.SpcialSocialType=Scene[0]
#         self.CreateTime=Scene[1]
        self.SpcialSocialType=Scene['eventname']
        self.CreateTime=Scene['roundcount']


#输出字典
    def ToDic(self):
        return {'对端ID':self.OtherID,'状态': self.LineState,'类型':self.SpcialSocialType,'创建时间':self.CreateTime}
    

    
#类：关系  描述两者之间的关系
class TRelationship:
    def __init__(self): 
    #社交线数组
        self.SocialLines=[]       
    #社交线数量
        self.SocialLineCount=0

        self.OtherID=0    #对端ID
        self.OtherIDName=''  #对端姓名
        self.Other=None        #对端对象
        self.Famely=0                     #是否家庭成员
        self.CreateTime=0               #创建时间-回合
        self.LeftInfluence,self.RightInfluence=0,0 #影响力与被影响力：程度数值
        self.SocialCloseClassName=0  #交往密切程度等级，
        self.SocialCloseCount=0     #交往程度打分0至1000，影响密切程度。
        self.impression=0     #对对方对印象 -1000  至  1000
        self.SpcialSocialTypes=[]        #特殊的交往类型 集合：如夫妻，奴役，师徒，上下级等等。
#关系线注册
    def SocialLineRegist(self,Scene,OtherID):
        sl=TSocialLine()
        sl.OnActive=1
        sl.OtherID=OtherID
        sl.ExplanScene(Scene)
        self.SocialLines.append(sl)
#关系线注销--未完成---删除指定I
    def SocialLineCancel():
        del self.SocialLines[0]
        
#计算亲密等级--未完成        
    def getSocialCloseClassName(self):
        self.SocialCloseCount=len(self.SocialLines)
        if self.SocialCloseCount<2: 
            self.SocialCloseClassName='认识'
        elif self.SocialCloseCount<10: 
            self.SocialCloseClassName='朋友'
        elif self.SocialCloseCount<20: 
            self.SocialCloseClassName='亲密'

        return self.SocialCloseCount
#输出字典        
    def ToDic(self):
        self.getSocialCloseClassName()
        a=TSocialLine
        b=[]
        for a in range(len(self.SocialLines)):
            b.append(self.SocialLines[a].ToDic())
        if self.SocialLines[a].SpcialSocialType not in self.SpcialSocialTypes:
                self.SpcialSocialTypes.append(self.SocialLines[a].SpcialSocialType)


        # return {'对端ID':self.OtherID,'对端姓名':self.Other.surname+self.Other.firstname,'交往密切程度':self.SocialCloseCount,'交往密切程度等                级':self.SocialCloseClassName,'类型':self.SpcialSocialTypes,'创建时间':self.CreateTime,'联系线':b}
        return {'对端ID':self.OtherID,'对端姓名':self.OtherID,'交往密切程度':self.SocialCloseCount,'交往密切程度等级':self.SocialCloseClassName,'类型':self.SpcialSocialTypes,'创建时间':self.CreateTime,'联系线':b}




#类：社会关系。描述一个个体的社会关系及社交能力
class TSocial:
    def __init__(self): 
    #关系人数组
        self.Relations=[] #关系数组
        self.OtherIDs=[]  #有关系的人们的ID
        self.Others=[]    #有关系的人们
    #主人
        self.BubbleID=0
        self.Bubble=None
    #社交能力
        self.SocialAbility=0
    #社交趋向,是偏向上层还是偏向下层
        self.SocialDes=0

    #最佳社交数量
        self.BestSocialLineCount=0
    #社交满意状态
        self.SocialSatisfy=0#饥渴的，一般的，满足的
    #社交地位
        self.WorldSocialClass=0
    #正在被绘制

        self.OnDrawing=0
        self.DrawedCount=0
    # 关系支援力量
        self.SocailPower=0      
#关系注册--------
    def RelationsRegist1(self,Scene,OtherID):
        #判断第一次发生关系---源自一次事件
        if OtherID not in self.OtherIDs:
            self.OtherIDs.append(OtherID)
            r=TRelationship()
            r.OtherID=OtherID
            r.SocialLineRegist(Scene,OtherID)
            self.Relations.append(r)

            
#关系注册--------
    def RelationsRegist(self,Scene,Other):
        #判断第一次发生关系---源自一次事件
        if Other.BubbleID not in self.OtherIDs:
            self.OtherIDs.append(Other.BubbleID)
            self.Others.append(Other)
            r=TRelationship()
            r.OtherID=Other.BubbleID
            r.Other=Other
            r.SocialLineRegist(Scene,Other.BubbleID)
            self.Relations.append(r)
            
#关系维护
    def RelationsModify(self,Scene,OtherID):
        #找到对应关系
        for r in (self.Relations):
            if r.OtherID ==OtherID:
                #添加事件
                r.SocialLineRegist(Scene,OtherID)
                break
                
#关系注销
    def RelationsCancel(self,Scene,OtherID):
        for r in self.Relations:
            if r.OtherID==OtherID:
                del self.Relations[r]
                break
#关系字典描述                    
    def ToDic(self):
        
        x=[]
        for a in range(len(self.Relations)):
            x.append(self.Relations[a].ToDic())
        
        sorted(x,key=lambda y:y['交往密切程度'])
        #for a in self.Relations:
            #x.append( a().ToDic() )
        # return {'主人ID':self.Bubble.BubbleID,'主人姓名':self.Bubble.surname+self.Bubble.firstname,'主人性别':self.Bubble.gender,'社交能力': self.SocialAbility,'关系数量':len(x),'关系':x}
        return {'社交能力': self.SocialAbility,'关系数量':len(x),'关系':x}
'''
s=TSocial()
s.RelationsRegist('xx',2) 
s.RelationsRegist('xx1',3)
s.RelationsRegist('xx2',4)
s.RelationsRegist('xx3',5)
s.RelationsRegist('xx4',6)
print(s.ToDic())

import json
json = json.dumps(s.ToDic())
print(json)
'''

