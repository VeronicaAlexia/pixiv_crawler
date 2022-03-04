from setting import *
from rich import print


class Vars:
    def __init__(self):
        pass

    cfg = Config('Pixiv-Config.conf', os.getcwd())


def count_time(func):
    def wrapper(*arg, **kwargs):
        start_time = time.time()
        result = func(*arg, **kwargs)
        print(f"下载耗时:{time.time() - start_time:.2f}s")
        return result

    return wrapper


def str_mid(string: str, left: str, right: str, start=None, end=None):
    pos1 = string.find(left, start, end)
    if pos1 > -1:
        pos2 = string.find(right, pos1 + len(left), end)
        if pos2 > -1:
            return string[pos1 + len(left): pos2]
    return ''


def remove_str(content: str):
    res_compile = re.compile(u'[\U00010000-\U0010ffff\\uD800-\\uDBFF\\uDC00-\\uDFFF]')
    return res_compile.sub("", re.sub('[/:*?"<>|]', '-', content))


def rec_id(book_id: str):
    book_id = book_id if 'http' not in book_id else re.findall(r'/([0-9]+)/?', book_id)[0]
    return str(book_id) if book_id.isdigit() else f'输入信息 {book_id} 不是数字或链接！'


def index_title(division_index: int, image_name: str):
    print(division_index, image_name)
    return str(division_index).rjust(4, "0") + '-' + str(image_name)


def mkdir(file_path: str):
    if not os.path.exists(file_path):
        os.mkdir(file_path)


def makedirs(file_path: str):
    if not os.path.exists(file_path):
        os.makedirs(file_path)


def input_(prompt, default=None):
    while True:
        ret = input(prompt)
        if ret != '':
            return ret
        elif default is not None:
            return default


def list_derivation(list_, key2):
    return ''.join([data[key2] for data in list_ if data[key2]])


def set_config():
    Vars.cfg.load()
    # +++++++++++++++++++++headers=======================
    if type(Vars.cfg.data("headers", "User-Agent")) is not str:
        Vars.cfg.save(
            "headers", "User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"
        )
    if not isinstance(Vars.cfg.data("headers", "Cookie"), str):
        Vars.cfg.save("headers", "Cookie", "")
    if not isinstance(Vars.cfg.data("headers", "retry"), str):
        Vars.cfg.save("headers", "retry", "5")
    if not isinstance(Vars.cfg.data("headers", "referer"), str):
        Vars.cfg.save(
            "headers", "referer", "https://www.pixiv.net/ranking.php?mode=daily&content=illust"
        )
    # +++++++++++++++++++++user=======================
    if not isinstance(Vars.cfg.data("user", "max_thread"), str):
        Vars.cfg.save("user", "max_thread", "5")
    if not isinstance(Vars.cfg.data("user", "save_file"), str):
        Vars.cfg.save("user", "save_file", "pixiv")
    if not isinstance(Vars.cfg.data("user", "out_file"), str):
        Vars.cfg.save("user", "out_file", "downloaded")
    if not isinstance(Vars.cfg.data("user", "access_token"), str):
        Vars.cfg.save("user", "access_token", "")
    if not isinstance(Vars.cfg.data("user", "refresh_token"), str):
        Vars.cfg.save("user", "refresh_token", "")
    if not isinstance(Vars.cfg.data("user", "help"), str):
        Vars.cfg.save(
            "user", "help",
            "输入首字母\n"
            "h | help\t\t\t\t\t\t--- 显示说明\n"
            "q | quit\t\t\t\t\t\t--- 退出正在运作的程序\n"
            "d | picture\t\t\t\t\t\t--- 输入id或url下载插画\n"
            "t | recommend\t\t\t\t\t\t--- 下载pixiv推荐插画\n"
            "s | start\t\t\t\t\t\t--- 下载账号收藏插画\n"
            "r | rank\t\t\t\t\t\t--- 下载排行榜作品\n"
            "n | tag name\t\t\t\t\t\t--- 输入插画名或者表情名\n"
            "f | follow\t\t\t\t\t--- 下载关注的画师作品"
        )
