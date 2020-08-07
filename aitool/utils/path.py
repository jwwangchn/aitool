import os
import glob


def get_basename(file_path):
    """get base file name of file or path (no postfix)

    Args:
        file_path (str): input path or file

    Returns:
        str: base name
    """
    basename = os.path.splitext(os.path.basename(file_path))[0]

    return basename

def get_file_paths(path, postfix='.png'):
    """get specific file path from the input path

    Args:
        path (str): input path
        postfix (str, optional): the postfix of return file. Defaults to '.png'.

    Returns:
        list: file paths
    """

    file_list = glob.glob(f"{path}/*{postfix}")

    return file_list