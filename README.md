# PixivCrawler

### pixiv login.

- authentication method is no longer supported to pixiv .
- The Pixiv app now logs in through `https://accounts.pixiv.net/login`
- but this page is protected by Google reCAPTCHA, which seems impossible to circumvent.
- so, you can't use this crawler to with login account,but you can use this crawler to web get the account token to
  login.
- You can refer to the following [link](/doc) to get the account token.
- run `py mian.py` browser automatically login pixiv on startup **[1](/doc/1.png)**
- copy the `code`  **[2](/doc/2.png)**
- enter the `code` it to command terminal  **[3](/doc/3.png)**
- **Congratulations on your login success!**

## start crawler with command line arguments

```
h | help               --- 显示说明
q | quit               --- 退出正在运作的程序
d | picture            --- 输入插画id或url下载插画
t | recommend          --- 批量下载pixiv推荐插画
s | start              --- 批量下载账号收藏插画
u | read text pid      --- 读取本地文本里的pid批量下载
n | tag name           --- 输入插画名或者标签名批量下载
```

## about command line arguments and usage

- **登入账号** ``` -l / --login```
- **下载插画** ``` -d / --download <image_id> ```
- **作者画集** ``` -a / --author <author_id> ```
- **更改线程** ``` -m / --max ```
- **下载收藏** ``` -s / --start ```
- **推荐插画** ``` -r / --recommend```
- **搜索插画** ``` -s / --search <search_word> ```
- **下载排行** ``` -k / --rkaning ```
- **清除缓存** ``` -c / --clear_cache```

| 功能               | 实现  |
|------------------|-----|
| id下载插画           | ✅   |
| 命令行              | ✅   |
| 批量下载搜索插画         | ✅   |
| 批量下载下载收藏插画       | ✅   |
| 批量下载下载推荐和相关插画    | ✅   |
| 多线程 谨慎使用，线程不要开太大 | ✅   |
| 异步 不支持，担心封IP     | ❌   |
| 唤起浏览器获取实现pixiv登入 | ✅   |

### 下载本地插画id

* 可以使用**本地文本**中所列出的插画id进行下载<p>
* 或者輸入:  `-u | --update <文本名>`  <p>
* 若省略`<文本名>`則會下载预设`"pixiv_id_list.txt"`中所列的插画id<br>

* 规则概要 :
    * 每行只能下载最开始的第一个插画id号
    * 插画id开始只能是<空白>或<插画ID_8位數>
    * <插画ID_8位數> 后面的信息会被忽略
* 若不符合正则表达式则忽略该行
    * 可在刻意“**不符合规则**”插画ID自前插入任意符号来停用该次下载，不必删除该行
    * 可自由添加“**不符合规则**”的文字来进行分类管理或注释，增加阅读辨识度
* 提供參考范例 "pixiv_id_list.txt"

