# BilibiliCollectionDownloader
## 项目简介
完全使用Python语言编写，大量抄袭csdn上已有项目，没有GUI，纯命令行，极致单线下载。
## API解析
act_id指代属于up的收藏集，lottery_id指代具体收藏集（因为一个账号可以有多个收藏集）。通常act_id+1就是lottery_id，但依然会有意外情况。现在通过搜索结果的jump_url一项优雅地解决了这个问题。
## 提示
默认下载在与该项目同一路径下，要改自己改。uapool.txt要和py文件放在同一个目录下。
## 用法
输入关键词，当前页没有结果就直接按空格。退出键入e并按enter。