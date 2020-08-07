import os


def get_basename(file_path):
    """get base file name of file or path (no postfix)

    Args:
        file_path (str): input path or file

    Returns:
        str: base name
    """
    basename = os.path.splitext(os.path.basename(file_path))[0]

    return basename