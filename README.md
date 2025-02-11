# BilibiliCollectionDownloader
## 项目简介
完全使用Python语言编写，大量抄袭csdn上已有项目，没有GUI，纯命令行，150行屎山，无多线程，极致单线下载，些许AI辅助，未实现全自动下载

Written entirely in Python, heavily plagiarized from existing projects on CSDN, without a GUI, purely command-line based, a 150-line mess of code, no multithreading, single-threaded downloading at its finest, with some AI assistance, and not fully automated for downloading.
————translated from AI model of Baidu
## API解析
act_id指代属于up的收藏集，lottery_id指代具体收藏集（因为一个账号可以有多个收藏集）。通常act_id+1就是lottery_id，但依然会有意外情况。为此，键入"m"即可进入手动下载模式。第一个填act_id,第二个填lottery_id。不知道在哪看就用电脑浏览器打开收藏集链接，f12然后转到“网络”，f5刷新，过滤器为“Fetch/XHR”。观察开头为“lottery_home_detail”的对象，单击，在右边的详细信息里切换到“载荷”项，其中会有上述提到的几个变量和值。
使用main.py即可解决该问题。新版加入搜索功能，无痛获取收藏集链接。
## 铸币开发者の疑问
1.难道除了java这种面向对象编程的语言就没有方法去实现自动获取收藏集源的方法了吗？主播才高二学不了那么多东西嘤嘤嘤。
## 提示
默认下载在D盘，要改下载路径自己改。uapool.txt要和py文件放在同一个目录下。