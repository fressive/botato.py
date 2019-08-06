# botato.py
一个使用 Python 编写的多功能 QQBot 。

[QQLight](https://www.52chat.cc/) 库来自 [qqRobot](https://github.com/QPromise/qqRobot) by [QPromise](https://github.com/QPromise) 。


## 使用

本 Bot 需要 Python 3.5 及更高版本运行。

1. 安装依赖

```
pip install -r requirements.txt
```

2. 修改配置文件 (`config.py.example`) 及重命名至 `config.py`.

3. 运行

```
python QQLightBot.py -H 127.0.0.1 -P 49632 -U / -L INFO botato:BotatoHandler
```

## 已完成的功能

### 杂项
#### paper

从 konachan 中获取图片，结果均过滤 NSFW 内容（rating = safe）。

```
paper [query] [{x} limit] [{on} source]
// query [str]  Tags
// limit [int]  图片数量，最多不超过 10 张。

paper
// 随机获取一张图片
paper neko
// 获取一张 tags 为 neko 的图片
paper neko x 10
// 获取十张 tags 为 neko 的图片
paper neko on danbooru
// 从 danbooru 获取一张 tags 为 neko 的图片
paper neko x 10 on danbooru
// 从 danbooru 获取十张 tags 为 neko 的图片
```

#### artist

从 SauceNAO 以及 ascii2d（未完成）查找图片来源。

```
artist <image>
```