import json
import sys
import download
from instance import *
from rich.progress import track
import PixivAPI


def update():
    download_test = False
    response = PixivAPI.get("https://raw.githubusercontent.com/Elaina-Alex/pixiv_crawler/main/update.json")
    if not os.path.exists('update.json'):
        json.dump(response, open('update.json', 'w'))
        download_test = True
    data = json.loads(open('update.json', 'r').read())
    if data['version'] < response['version']:
        print("检测到有新版本", response['version'], "是否进行更新？[yes/no]")
        choice = PixivAPI.input_('>').strip()
        if choice == "yes":
            download_test = True
            print("开始更新", response['version'], "版本")
        else:
            download_test = False

    if download_test:
        with open(data['name'] + ".exe", 'wb') as file:
            print(response['download_url'].format(response['version']))
            file.write(PixivAPI.HttpUtil.get(response['download_url'].format(response['version'])).content)
        print(data['name'] + ".exe", "下载完毕")
        json.dump(response, open('update.json', 'w'))
        print("三秒后自动退出脚本...")
        sys.exit()


def shell_download_author_works(author_id: str):
    for index, page in enumerate(range(20), start=1):
        image_id_list = PixivAPI.PixivApp.author_information(author_id, index)
        if isinstance(image_id_list, list) and len(image_id_list) != 0:
            download.ThreadGetImagesInfo.get_images_info(image_id_list)
            download.ThreadDownload().threading_downloader()
        else:
            break


@count_time
def shell_illustration(inputs):
    if len(inputs) >= 2:
        if isinstance(inputs, list) and len(inputs) == 3 and inputs[2] == "a":
            shell_download_author_works(inputs[1])  # 通过作者ID下载作者的作品集
        else:
            Vars.images_info = PixivAPI.PixivApp.images_information(PixivAPI.rec_id(inputs[1]))
            if isinstance(Vars.images_info, dict):
                Vars.images_info = download.ImageInfo(Vars.images_info)
                Vars.images_info.show_images_information()
                if Vars.images_info.page_count == 1:
                    Vars.images_info.save_image(Vars.images_info.original_url)
                else:
                    Vars.images_info.save_image(Vars.images_info.original_url_list)
            else:
                print("没有找到相应的作品！")
    else:
        print("你没有输入id或者链接")


@count_time
def shell_search(inputs: list):
    if len(inputs) < 2:
        print("没有输入搜索信息")
        return
    for index, page in enumerate(range(20), start=1):
        image_id_list = PixivAPI.PixivApp.search_information(inputs[1], index)
        print("本页一共:", len(image_id_list), "幅插画，开始下载")
        if isinstance(image_id_list, list) and len(image_id_list) != 0:
            for image_id in track(image_id_list, description=f"插画集加载中..."):
                Vars.images_info = PixivAPI.PixivApp.images_information(image_id)
                if isinstance(Vars.images_info, dict):
                    Vars.images_info_list.append(download.ImageInfo(Vars.images_info))

            download.ThreadDownload().threading_downloader()
        else:
            print("搜索画集下载完毕！")


@count_time
def shell_download_follow_author():
    follow_information_list = PixivAPI.PixivApp.follow_information()
    if isinstance(follow_information_list, list):
        print("共有", len(follow_information_list), "个关注")
        for follow_information in follow_information_list:
            print("开始下载", follow_information['user']['name'], "的作品")
            for illusts in follow_information['illusts']:
                Vars.images_info = download.ImageInfo(illusts)
                Vars.images_info.show_images_information()
                if Vars.images_info.page_count == 1:
                    Vars.images_info.save_image(Vars.images_info.original_url)
                else:
                    Vars.images_info.save_image(Vars.images_info.original_url_list)
            print(follow_information['user']['name'], "的作品下载完毕")


@count_time
def shell_download_rank():
    pixiv_app_api, next_page = PixivAPI.PixivToken.instantiation_api(), {"mode": "day"}
    while next_page:
        response_ranking = pixiv_app_api.illust_ranking(**next_page)
        if response_ranking.error is not None:
            print(response_ranking.error)
            break
        image_id_list = list(set([data.id for data in response_ranking.illusts]))
        print("本页一共:", len(image_id_list), "幅插画，开始下载")
        if isinstance(image_id_list, list) and len(image_id_list) != 0:
            for image_id in track(image_id_list, description=f"排行榜插画集加载中..."):
                Vars.images_info = PixivAPI.PixivApp.images_information(image_id)
                if isinstance(Vars.images_info, dict):
                    Vars.images_info_list.append(download.ImageInfo(Vars.images_info))
            download.ThreadDownload().threading_downloader()
            next_page = pixiv_app_api.parse_qs(response_ranking.next_url)
        else:
            print("Pixiv排行榜插图下载完毕")


@count_time
def shell_read_text_id(inputs):
    list_file_name = inputs[1] + '.txt' if len(inputs) >= 2 else 'list.txt'
    try:
        image_id_list = [
            re.sub("^\\s*([0-9]{1,8}).*$\\n?", "\\1", line) for line in
            open(list_file_name, 'r', encoding='utf-8').readlines() if re.match("^\\s*([0-9]{1,8}).*$", line)
        ]
        print("一共:", len(image_id_list), "幅插画，开始下载")
        if isinstance(image_id_list, list) and len(image_id_list) != 0:
            for image_id in track(image_id_list, description=f"本地插画集加载中..."):
                Vars.images_info = PixivAPI.PixivApp.images_information(image_id)
                if isinstance(Vars.images_info, dict):
                    Vars.images_info_list.append(download.ImageInfo(Vars.images_info))
            download.ThreadDownload().threading_downloader()
    except OSError:
        print(f"{list_file_name}文件不存在")


def shell_test_pixiv_token():
    for retry in range(Vars.cfg.data.get("max_retry")):
        if Vars.cfg.data.get("refresh_token") != "":
            return True
        if Vars.cfg.data.get("user_info") is not None:
            return True
        else:
            print("检测到本地档案没有令牌，请登入网站获取code，也可以将token自行写入本地档案")
            code_verifier = PixivAPI.login_pixiv.open_browser()
            code = PixivAPI.input_('code:').strip()
            response = PixivAPI.login_pixiv.login(code_verifier, code)
            if response is True:
                print(f"code:{code} 信息验证成功！")
                return True
            else:
                print(f"输入code:{code} 无效，请重新尝试获取！还剩余{Vars.cfg.data['max_retry'] - retry - 1}次机会")


def shell_download_stars():
    start_information_list = PixivAPI.PixivApp.start_information()
    if isinstance(start_information_list, list):
        for illusts in start_information_list:
            Vars.images_info = download.ImageInfo(illusts)
            Vars.images_info.show_images_information()
            if Vars.images_info.page_count == 1:
                Vars.images_info.save_image(Vars.images_info.original_url)
            else:
                Vars.images_info.save_image(Vars.images_info.original_url_list)
            print(illusts['user']['name'], "的作品下载完毕")



def shell():
    if len(sys.argv) > 1 and isinstance(sys.argv, list):
        command_line = True
        inputs = sys.argv[1:]
    else:
        command_line = False
        for msg_help in Msg.msg_help:
            print('[帮助]', msg_help)
        inputs = re.split('\\s+', PixivAPI.input_('>').strip())
    while True:
        if inputs[0] == 'q' or inputs[0] == 'quit':
            sys.exit("已退出程序")
        elif inputs[0] == 'h' or inputs[0] == 'help':
            for msg_help in Msg.msg_help:
                print('[帮助]', msg_help)
        elif inputs[0] == 'l' or inputs[0] == 'login':
            shell_test_pixiv_token()
        elif inputs[0] == 'd' or inputs[0] == 'download':
            shell_illustration(inputs)
        elif inputs[0] == 's' or inputs[0] == 'stars':
            shell_download_stars()
        elif inputs[0] == 'n' or inputs[0] == 'name':
            shell_search(inputs)
        elif inputs[0] == 't' or inputs[0] == 'recommend':
            PixivAPI.PixivApp.recommend_information()
        elif inputs[0] == 'u' or inputs[0] == 'update':
            shell_read_text_id(inputs)
        elif inputs[0] == 'r' or inputs[0] == 'rank':
            shell_download_rank()
        elif inputs[0] == 'f' or inputs[0] == 'follow':
            shell_download_follow_author()
        else:
            print(inputs[0], "为无效指令")
        if command_line is True:
            sys.exit(1)
        inputs = re.split('\\s+', PixivAPI.input_('>').strip())


if __name__ == '__main__':
    set_config()
    # update()
    shell_test_pixiv_token()
    shell()
