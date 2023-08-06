# magic_maze

#### 介绍

迷宫游戏

#### 项目目的

娃最近迷恋迷宫游戏，买的迷宫书走完就没了，他表示还没玩够。

所以就做了这个迷宫游戏，可以实现随机生成迷宫、走迷宫、显示答案等效果，让他可以无限玩。

#### 安装使用

+ 下载可执行文件: 到 https://github.com/HeLiangHIT/magic_maze/releases 下载可执行文件
+ 源码安装: `git clone https://github.com/HeLiangHIT/magic_maze.git && cd magic_maze && python setup.py install`
+ pip源安装: `pip install magic_maze`

#### 软件架构

+ 核心目录结构解释:
    * algorithm 里面核心算法已抽象为通用接口，以支持扩展多种界面展现方式，详情查看[帮助文档](./doc/algorithm.txt)
```py
magic_maze
├── README.md # 项目介绍
├── algorithm # 核心算法和数据结构实现
├── demo # 使用示例模型等
├── doc # 帮助文档，主要基于 script/generate_doc.sh 脚本在提交时自动生成
├── main.py # 主程序
├── requirement.txt # 依赖
├── script # 单元测试、帮助文档生成等自动化脚本
└── ui # pyqt 的 UI 主程序
```

#### TODO

+ [x] 支持在矩阵上画迷宫，默认白色的格子，划过或者点击变成绿色(墙体)
+ [x] 支持走迷宫，走过的路变成绿色，走过的路再次点击编程红色(标记死胡同) - 左键走，右键消
+ [x] 支持自动搜索可行的路径(过程可视化标记死胡同最好) - 死胡同暂时不知道怎么标记
+ [x] 增加测试脚本自动验证 algorithm 的正确性
+ [x] 起点标记小人，终点标记小旗子
+ [x] 当前迷宫刷新太慢，设置的中断时间未生效 --> 需支持迷宫每次刷新只刷新增量部分(map支持diff返回列表、Item支持只刷新列表内容)
+ [x] 支持你画我走的陪玩方法(可以检查可通过性)
+ [x] 支持迷宫地图的加载和保存
+ [ ] 编写 setup.py 生成二进制发布件
    * [ ] 配置CICD自动在tag的时候生成发布件
    * [ ] 配置git提交前自动运行脚本验证LLT
+ [ ] 参考: [pygame迷宫](https://www.cnblogs.com/ksxh/p/13824662.html)  、 [pyqt迷宫](https://blog.csdn.net/cj12345657582255/article/details/115605195) 、 [gif动画制作](https://cloud.tencent.com/developer/news/185919)
+ [ ] 持续做成教程的系列博客文章
+ [ ] 做好后的迷宫可以进一步基于[虚幻引擎](https://docs.unrealengine.com/5.1/zh-CN/how-to-set-up-android-sdk-and-ndk-for-your-unreal-engine-development-environment/)做成3D迷宫(做成手游、微信小游戏类似羊了个羊)，让人走进去 - 虚幻引擎要花点时间才能学习，特别是安卓端的，意义不足，优先级放低
    * [ ] 后面可以增加的玩法会很多，比如增加魔法、怪物之类的惊喜，增加双人对战比谁先走到目标点(也可以是多个目标点谁先逃出去)
+ [ ] 支持将绘制的迷宫保存、悬赏发布，第一个走通的可以获得悬赏，增加交互和联网特性，形成迷宫生态提升用户粘性

