from pathlib import Path

def pathlib_traverse_iter(path, pattern):
    """
    使用 pathlib 模块递归遍历目录并返回迭代器
    :param path: 要遍历的目录路径
    :return: 迭代器，每次迭代返回文件或目录的完整路径
    """
    path_obj = Path(path)
    if path_obj.exists():
        for item in path_obj.rglob(pattern):
            yield item

# 示例用法
directory_path = './data/premarket'  # 当前目录
for item in pathlib_traverse_iter(directory_path, '*.csv'):
    print(item)

def shirk_up_raw_csv(path):
    pass