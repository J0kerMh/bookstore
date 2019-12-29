#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   search.py    
@Contact :   caiwenyuok@sina.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/12/28 20:29   wycai      1.0         None
'''
from whoosh.fields import Schema, TEXT, ID,KEYWORD,NUMERIC
from jieba.analyse import ChineseAnalyzer
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.index import create_in
dirname ="index"
command=("author_intro","book_intro","content","tags")
def init_whoosh():
    CA = ChineseAnalyzer()
    schema = Schema(Mongo_ID=ID(stored=True), book_id=NUMERIC(stored=True),author_intro=TEXT(analyzer=CA), book_intro=TEXT(analyzer=CA),
                    content=TEXT(analyzer=CA), tags=KEYWORD)
    import os.path
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    create_in(dirname, schema)

def add_index(Mongo_ID,book_id,author_intro, book_intro, content, tags):
    idx = open_dir(dirname=dirname)  # indexname 为索引名
    writer= idx.writer()# IndexWriter对象
    writer.add_document(Mongo_ID=Mongo_ID,book_id=book_id,author_intro=author_intro, book_intro=book_intro,
                            content=content, tags=tags)
    writer.commit()
    idx.close()

def test_add_index():
    book_intro=u"《他改变了中国：江泽民传》详尽介绍了江泽民同志的人生历程，尤其是阐述和评价了江泽民担任中国主要领导人的十多年中创立的历史功绩。在国内政治方面，书中着重叙述了 1989 年后，在中国政治、社会、经济出现难题的形势下，江泽民同志如何领导全国人民，保持社会稳定，加速经济发展，提高人民生活水平，并最终使中国发生了不可逆转的根本性转变。书中首次披露了若干重大事件与决策的史实细节。比如， 1979 年，江泽民同志在全国人大常委会上作了有关建立经济特区的报告，正是这个报告推动了中国设立经济特区的最终决策； 1992 年党的十四大召开前，江泽民同志提出用 “社会主义市场经济”这一概念来取代“社会主义经济体制”，并使之成为中国改革的新旗帜； 2000 年，江泽民同志提出了“三个代表”重要思想，这一思想最终被载入了党章，成为中国共产党在新世纪的指导思想。在国际政治方面，该书叙述了江泽民同志作为党和国家主要领导人，如何努力把中国塑造为充满生机和活力的备受尊重的政治大国、经济大国、文化大国和外交大国。书中还披露了若干重大外交事件的始末，例如在美国轰炸南联盟、南海撞机等事件中，江泽民如何运用其政治智慧，坚持国家立场，维护民族尊严，疏导公众情绪，平稳化解危机，保持社会稳定。本书在着重于江泽民同志的国事活动的同时，也广泛涉及他的家庭生活、业余爱好、人品风格等方方面面，丰富、生动、多角度、多侧面地展现传主的风采。江泽民同志的人生故事，与沧桑巨变的中国近 80 年的历史密切地联系在一起；本书是一部有关战争、贫困、革命、动荡、经济改革、民族转型和崛起于世界的长篇史诗。要想理解今日中国面临的挑战，就必须理解江泽民为中国作出的杰出贡献，从中体味中国的巨变给整个世界带来的影响。在这部政治与个人生活并重的传记中，库恩所展示的江泽民是当代中国的一个缩影。"
    author_intro=u"罗伯特・劳伦斯・库恩 罗伯特・劳伦斯・库恩（Robert Lawrence Kuhn）博士是著名国际投资银行家和公司战略家，解剖学博士，是作家、编辑、学者、科学家、私人投资家和慈善家。恩博士现任库恩基金会董事长，该基金会由他本人投资创立，运作文化、教育、科技和人文项目，包括追踪和传播科技和学术领域的新知识，举办古典音乐演出，促进中美文化交流、媒体教育以及两国之间的友好关系。目前正在举办的项目有：美国公共广播公司系列节目《走近真实：科学、意义和未来》，这一节目由库恩本人制作和主持，展现了科学家和学者对当今世界的前沿科学、新知识和基本问题的不同观点(www.pbs.org/closertotruth)；纪实片《音乐家阿拉姆・哈恰图良的生平和音乐》（获2003年好莱坞电影节最佳纪实片奖）；中美财经、媒体和科技学者跨文化大会。库恩博士现任花旗集团执行董事，主要从事并购和企业理财，专职负责公司重组、财务战略和资本运作。10多年来，库恩博士担任日内瓦公司总经理和合伙人，该公司在他的经营下成为美国私人拥有的最大的一流并购公司，后来经他洽谈出售给花旗集团。在他领导下，日内瓦公司完成了超过1200家私人公司的并购交易，并对10000家私人公司进行了估价，是美国当时业务量最大的公司。库恩博士担任库恩全球资本公司董事长，通过该公司管理自己的私人投资。自1989年以来，库恩博士应国家科学技术委员会之邀来到中国，一直担任中国国家部委、机构、企业和大公司顾问。他为中国政府提供经济政策、并购、科技、媒体以及中国的国际形象等方面的咨询。库恩博士致力于帮助中国发展市场经济，组织会议讲授并购和科技的商业化以及媒体经营。库恩博士还担任北京前沿科学研究所副理事长。库恩博士编著有25部著作，其中有《投资银行文库》（7卷）、《投资银行学：高风险交易的艺术与科学》、《创造性和创新性管理前沿》、《交易人》、《你所需要的谈判技巧和秘密》、《走近真实：挑战当今观念》、《在巨人当中胜出：中型公司的创造性管理》和《中国制造：新革命之声》等。他的三部著作被翻译成中文：《交易人》、《走近真实》和《投资银行学》（中国出版的第一部投资银行学著作）。库恩博士是克莱蒙特研究生院的理事，美国科学促进会科学自由和责任分会会员。他曾获加州大学洛杉矶分校大脑解剖学博士学位，麻省理工学院管理学硕士学位，担任纽约大学斯特恩商学院商务与财经策略教授。"
    context=u"为了让受人尊敬的陈云了解最新技术，江带了很多道具帮助陈云了解电子革命的含义，江还自始自终说着老人的上海乡音。威望大概仅次于邓小平的陈云，不仅赞赏江泽民掌握最新技术，还！！！赞赏江善解人意，没有令他对不熟悉的东西感到不自在。"
    tags=u"圣经 克苏鲁 上交大 长寿 长者 naive"
    add_index("123",author_intro,book_intro,context,tags)

class search:
    def __init__(self):
        self.idx=open_dir(dirname)
        self.searcher_open()

    def search_index(self,command, input):
        parser = QueryParser(command, self.idx.schema)
        queryString=""
        print(input)
        for i in input:
            queryString=queryString+str(i)+""
        myquery = parser.parse(queryString.strip())
        results = self.searcher.search(myquery)
        return results

    def searcher_close(self):
        self.searcher.close()

    def searcher_open(self):
        idx = open_dir(dirname=dirname)  # indexname 为索引名
        self.searcher = idx.searcher()