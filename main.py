import yaml
import json
import os
import re
import aiohttp
import asyncio


# 读取LinksPath.txt文件中的所有路径
def read_paths_from_file(file_path: str) -> list:
    paths = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        for line in file:
            # 移除换行符并添加到列表中
            paths.append(line.strip()) if line.strip() != "" else None
    return paths


# 检查路径是否存在
def check_paths_exist(paths: list) -> list:
    valid_paths = []
    for path in paths:
        if os.path.exists(path):
            valid_paths.append(path)
    return valid_paths


# 提取第一层的文件夹名称，后面使用它当成为key键使用
def get_first_folder_name(directory: str) -> str:
    # 使用os.path.split()函数获取目录路径和文件名
    dir_path, _ = os.path.split(directory)
    # 使用os.path.sep获取路径分隔符
    sep = os.path.sep
    # 使用split()函数以路径分隔符分割目录路径
    directories = dir_path.split(sep)
    # 获取第一段文件夹名称
    first_folder = directories[0]
    return first_folder


# 从指定目录下所有.bat文件中提取链接，并以文件夹名称为键，多个url为值，存储到字典中
def extract_links_from_bat_files(directory: str) -> dict:
    links_dict = dict()
    for root, dirs, files in os.walk(directory):
        folder_name = get_first_folder_name(directory)
        for file in files:
            if file.endswith(".bat"):
                file_path = os.path.join(root, file)
                # 使用errors='ignore'参数来忽略解码时出现的错误
                with open(file_path, 'r', encoding='utf-8-sig', errors='ignore') as bat_file:
                    bat_content = bat_file.read()
                    # 使用正则表达式提取链接
                    extracted_links = re.findall(r'https?://\S+', bat_content)
                    if folder_name not in links_dict:
                        links_dict[folder_name] = set(extracted_links)
                    else:
                        links_dict[folder_name].update(set(extracted_links))
    return links_dict


# 从可用的路径中，提取路径内所有.bat后缀文件内的所有https://链接
def read_links_from_valid_paths(valid_paths: list) -> dict:
    all_links = dict()
    for path in valid_paths:
        if os.path.isdir(path):
            # 提取该目录下所有.bat文件中的链接
            links_dict = extract_links_from_bat_files(path)
            all_links.update(links_dict)
    return all_links


# 检查download文件夹是否存在，存在就删除文件夹内的所有文件，不存在就创建文件夹
def check_download_folder(output_folder: str) -> None:
    # 检查download文件夹是否存在，不存在就创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    else:
        # 检查到文件夹存在，就遍历文件夹中的所有文件，把它们删除
        for file_name in os.listdir(output_folder):
            file_path = os.path.join(output_folder, file_name)
            # 确保当前路径是一个文件而不是文件夹
            if os.path.isfile(file_path):
                os.remove(file_path)


# 格式化从网页读取到的内容，控制内容缩进
def format_data(data_str: str) -> str:
    try:
        # 尝试解析为 JSON 格式
        json_data = json.loads(data_str)
        # 如果成功，漂亮地格式化 JSON 数据
        return json.dumps(json_data, indent=2)
    except ValueError:
        try:
            # 尝试解析为 YAML 格式
            data = yaml.safe_load(data_str)
            # pretty_yaml = yaml.dump(data, default_flow_style=False, indent=2, sort_keys=False)
            # 编码为 UTF-8 字节序列，然后解码为 Unicode 字符串（解决\u开头的字符的问题）
            # decoded_pretty_yaml = pretty_yaml.encode("UTF-8").decode('unicode_escape')
            # yaml代码格式化不符合个人要求，这里的返回数据，没有使用yaml格式化
            return data_str
        except yaml.YAMLError:
            # 如果无法解析为 JSON 或 YAML 格式，则返回原始数据
            return data_str


async def fetch_url_content(url: str, timeout=5) -> (str, str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
        try:
            async with session.get(url, headers=headers, ssl=False) as response:
                content = await response.text()
                pretty_content = format_data(content)
                print(f"{url} fetched successfully")
                return url, pretty_content
        except asyncio.TimeoutError:
            print(f"{url} Timeout error occurred while fetching")
            return url, None
        except aiohttp.client_exceptions.ClientConnectorError:
            print(f"{url} Connection error occurred while fetching")
            return url, None
        except Exception as e:
            print(f"{url} Other error occurred while fetching")
            return url, None


async def fetch_urls_content(key: str, urls: set) -> (str, dict, dict):
    # 创建空字典来存放结果
    valid_links = {}
    web_datas = {}

    # 异步并发地获取链接的内容
    tasks = [fetch_url_content(url) for url in urls]
    results = await asyncio.gather(*tasks)

    # 处理结果
    for url, content in results:
        if content is not None:
            # 将有效的链接存入 valid_links 字典中，键为原始的键，值为对应的 URL。数据结构类似：{xray:{xray_web1_url,xray_web2_url}}
            if key not in valid_links:
                valid_links[key] = set()
            valid_links[key].add(url)
            # 将网页数据存入 web_data 字典中，键为原始的键，值为网页内容。数据结构类似：{xray:{xray_web1_data,xray_web2_data}}
            if key not in web_datas:
                web_datas[key] = set()
            web_datas[key].add(content)
    # 返回结果
    return key, valid_links, web_datas


async def main():
    # 文件名和文件夹
    subscribed_links_file = "SubscribedPath.txt"
    valid_links_file = "valid_links.txt"
    output_folder = "Download"

    # 从LinksPath.txt读取路径
    all_paths = read_paths_from_file(subscribed_links_file)

    # 检查路径是否存在，检查"download"文件夹是否存在
    valid_paths = check_paths_exist(all_paths)
    check_download_folder(output_folder)

    # 从可用的路径中，提取路径内所有.bat后缀文件内的所有https://链接
    links_dict = read_links_from_valid_paths(valid_paths)

    # 异步并发
    tasks = [fetch_urls_content(key, urls) for key, urls in links_dict.items()]
    results = await asyncio.gather(*tasks)

    # 处理结果
    with open(valid_links_file, mode='w', encoding='utf-8') as wf:
        for _, valid_links, web_datas in results:
            for key, values in valid_links.items():
                sorted_links = sorted(values)
                links_str = "\n".join(sorted_links)
                wf.write(f"# {key}\n{links_str}\n")
            if key.lower() in ["quick", "clash.meta", "clash", "v2go"]:
                suffix = "yaml"
            else:
                suffix = "json"
            for key, values in web_datas.items():
                # 为相同的key添加序号
                for index, value in enumerate(values):
                    if "Package size exceeded the configured limit of 50 MB." in value:
                        output_file = f'{output_folder}/{key}-{index + 1}-exceeded.txt'
                    else:
                        output_file = f'{output_folder}/{key}-{index + 1}.{suffix}'
                    with open(output_file, mode='w', encoding='utf-8') as wf2:
                        wf2.write(value)
    print(f"能使用的链接，已经写入到{valid_links_file}文件中；")
    print(f"各种代理的配置文件，已经全部下载到{output_folder}文件夹中。")


if __name__ == "__main__":
    asyncio.run(main())
