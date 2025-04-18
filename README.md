# youtube小工具

## 写在前面

这是一个和youtube视频相关的小工具包，目前包括以下内容：
1. 批量获取youtuber某个视频列表的所有视频的URL。
2. 自动批量获取视频的字幕并进行AI分析。
因为要学习一点东西的原因，我去youtube上找视频，但是目前的所有edge和google Chrome的插件都好像不太好使，于是一怒之下怒了一下，用GPT和ds搓了一个能总结视频的小玩意，大家可以用着玩玩，也可以提点修改建议。

## 如何使用

首先配置python环境，还有下载各种包（除了头部import的包以外，还要下载一个yt_dlp包）
1. 批量获取youtuber某个视频列表的所有视频的URL
    你需要获取到一个含有列表键值的URL，最简单的方式是在页面中从播放列表的方式进入一个视频，检查你的URL中有没有"list="字样。运行getVideosInList.py，将URL输入到该程序中即可。视频的URL列表将存储在urls.txt文件中。
2. 自动批量获取视频字幕并进行AI分析。
   你需要一个存储了你需要总结的youtube视频URL的txt文件，文件中每个URL按每一行存储。
   然后将文件youtube.py放置在一个文件夹下，你接下来要修改以下参数：
```py
    url_txt = #你存储URL的txt文件的位置(defalt:相同层的urls.txt文件)
    save_dir = #你存储字幕文件，字幕内容以及总结内容的文件夹（defalt：相同层下downloads文件夹内）
    openai_api_key = #你的API-Key，需要从平台上申请。
    model = #在该平台上你要使用的模型名称。
    base_url = #你的API管理平台的URL。
    max_tokens = #你希望AI给你返回的最大token数。由于有些模型按token数计费，这个限制可以省点钱，要是免费模型就不管了。
    content #在代码中找中文的部分，这块就是你要AI总结的重点，你可以修改成自己的prompt，让AI的总结有更明确的方向。
```
然后你需要科学上网（不科学上网连不上youtube.com）
然后愉快地运行就OK咯~。

## 写在后面

这个脚本的功能大致分为以下几个部分：从youtube上获取vtt字幕文件，然后解析vtt文件到txt文件中，然后再调用API分析txt文件内容。大概一个1h的视频的分析要约半分钟。

### 有点问题

#### vtt转txt这一块
目前这个version有点偷懒的地方，就是vtt转txt的部分，大家可以看一下下面我获取到的.vtt文件的部分节选：
```vtt
WEBVTT
Kind: captions
Language: en

00:00:00.439 --> 00:00:04.070 align:start position:0%
 
uipath<00:00:01.439><c> is</c><00:00:01.800><c> the</c><00:00:02.040><c> most</c><00:00:02.280><c> advanced</c><00:00:02.940><c> RPA</c><00:00:03.480><c> tool</c><00:00:03.959><c> in</c>

00:00:04.070 --> 00:00:04.080 align:start position:0%
uipath is the most advanced RPA tool in
 

00:00:04.080 --> 00:00:07.190 align:start position:0%
uipath is the most advanced RPA tool in
the<00:00:04.259><c> world</c><00:00:04.380><c> I'm</c><00:00:05.160><c> anus</c><00:00:05.520><c> Jensen</c><00:00:06.000><c> a</c><00:00:06.720><c> professional</c>

00:00:07.190 --> 00:00:07.200 align:start position:0%
the world I'm anus Jensen a professional
 

00:00:07.200 --> 00:00:11.570 align:start position:0%
the world I'm anus Jensen a professional
RPA<00:00:07.980><c> teacher</c><00:00:08.639><c> and</c><00:00:09.240><c> a</c><00:00:09.660><c> two-time</c><00:00:10.200><c> UI</c><00:00:10.740><c> path</c><00:00:11.099><c> most</c>

00:00:11.570 --> 00:00:11.580 align:start position:0%
RPA teacher and a two-time UI path most
 

00:00:11.580 --> 00:00:14.330 align:start position:0%
RPA teacher and a two-time UI path most
valuable<00:00:12.300><c> professional</c><00:00:12.960><c> let's</c><00:00:13.799><c> learn</c><00:00:14.099><c> some</c>

00:00:14.330 --> 00:00:14.340 align:start position:0%
valuable professional let's learn some
 

00:00:14.340 --> 00:00:15.829 align:start position:0%
valuable professional let's learn some
uipath

00:00:15.829 --> 00:00:15.839 align:start position:0%
uipath
 

00:00:15.839 --> 00:00:20.810 align:start position:0%
uipath
to<00:00:16.440><c> install</c><00:00:17.000><c> uipath</c><00:00:18.000><c> you</c><00:00:18.240><c> go</c><00:00:18.480><c> to</c><00:00:18.720><c> uipath.com</c>

00:00:20.810 --> 00:00:20.820 align:start position:0%
to install uipath you go to uipath.com
 

00:00:20.820 --> 00:00:24.109 align:start position:0%
to install uipath you go to uipath.com
then<00:00:21.359><c> click</c><00:00:21.720><c> try</c><00:00:22.160><c> uipath3</c><00:00:23.160><c> in</c><00:00:23.640><c> the</c><00:00:23.820><c> upper</c>

00:00:24.109 --> 00:00:24.119 align:start position:0%
then click try uipath3 in the upper
 

00:00:24.119 --> 00:00:27.109 align:start position:0%
then click try uipath3 in the upper
right<00:00:24.240><c> corner</c>

00:00:27.109 --> 00:00:27.119 align:start position:0%
 
```

可以很明显地发现，由于youtube的字幕是有那种流式输出以及滑动式的显示，所以直接获取vtt文件，然后去除掉时间信息把剩下的信息拼在一起会出现大量重复，就像下面这样：

```txt
uipath is the most advanced RPA tool in uipath is the most advanced RPA tool in the world I'm anus Jensen a professional the world I'm anus Jensen a professional the world I'm anus Jensen a professional RPA teacher and a two-time UI path most RPA teacher and a two-time UI path most RPA teacher and a two-time UI path most valuable professional let's learn some valuable professional let's learn some valuable professional let's learn some uipath uipath uipath to install uipath you go to uipath.com to install uipath you go to uipath.com to install uipath you go to uipath.com then click try uipath3 in the upper then click try uipath3 in the upper then click try uipath3 in the upper right corner here we want to install the full here we want to install the full automation Cloud for community that is automation Cloud for community that is automation Cloud for community that is the free full version so click the get the free 
```
这样，这种东西肯定是不能让AI去读的。高级一点的办法就是调一些自然语言处理模型像nltk一类的（GPT告诉我的），但是好像不太好使。我观察了一下，在每一句align:start position:0%接下来的那一行就是当前时间段内出现的这一句话的连贯版（其他的就是相同内容流式输出的方式），而且这个信息要么会完全重复，要么就是完全不同（例如uipath is the most advanced RPA tool in重复了两次）。因此，我在这里偷了个懒，只去检查align:start position:0%后面紧跟的内容，并与前一次获取的内容比较。如果和前一次获取的内容相同，则舍弃这次的内容。若不相同，则将新的内容拼接到结果中。要是有大佬能搞明白这块怎么处理，可以优化一下这里。

#### 总结的网站这一块

目前由于作者是用yt_dlp库实现调取的，因此应该是仅限于youtube的才能稳定获取弹幕，作者正在想办法能不能从B站这些地方搞到字幕，希望大家能提供更多指导。

## 最后的最后

总得来说希望能帮到大家，然后就是希望大家能多提点建议，要是觉得有帮到大家的话请打个星，谢谢大家咯~


