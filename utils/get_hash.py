# 获取字符串的 sha1 散列值

from hashlib import sha1


def get_hash(string, salt=None):
    """将字符串进行 sha1 加密"""
    string = '!@#$%' + string + '^&*()'  # 提高字符串的复杂度
    if salt:
        # 给字符串加佐料
        string += salt

    sha = sha1()
    sha.update(string.encode('utf-8'))
    return sha.hexdigest()
