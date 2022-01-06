import os
import re
import sys
import config

G_spat = re.compile(
    "^22-sht\.me|-fhd|_fhd|^fhd_|^fhd-|-hd|_hd|^hd_|^hd-|-sd|_sd|-1080p|_1080p|-720p|_720p|^hhd800\.com@|-uncensored|_uncensored|-leak|_leak",
    re.IGNORECASE)


def get_number(debug,file_path: str) -> str:
    # """
    # >>> from number_parser import get_number
    # >>> get_number("/Users/Guest/AV_Data_Capture/snis-829.mp4")
    # 'snis-829'
    # >>> get_number("/Users/Guest/AV_Data_Capture/snis-829-C.mp4")
    # 'snis-829'
    # >>> get_number("C:¥Users¥Guest¥snis-829.mp4")
    # 'snis-829'
    # >>> get_number("C:¥Users¥Guest¥snis-829-C.mp4")
    # 'snis-829'
    # >>> get_number("./snis-829.mp4")
    # 'snis-829'
    # >>> get_number("./snis-829-C.mp4")
    # 'snis-829'
    # >>> get_number(".¥snis-829.mp4")
    # 'snis-829'
    # >>> get_number(".¥snis-829-C.mp4")
    # 'snis-829'
    # >>> get_number("snis-829.mp4")
    # 'snis-829'
    # >>> get_number("snis-829-C.mp4")
    # 'snis-829'
    # """
    filepath = os.path.basename(file_path)
    filename = filepath.split('.')[0]
    if '-cd' or '-CD' in filename:
        file_number = re.sub(r'-[Cc][Dd][0-9]', '', filename)
        return file_number
    return filename


# 按javdb数据源的命名规范提取number
G_TAKE_NUM_RULES = {
    'tokyo.*hot' : lambda x:str(re.search(r'(cz|gedo|k|n|red-|se)\d{2,4}', x, re.I).group()),
    'carib' : lambda x:str(re.search(r'\d{6}(-|_)\d{3}', x, re.I).group()).replace('_', '-'),
    '1pon|mura|paco' : lambda x:str(re.search(r'\d{6}(-|_)\d{3}', x, re.I).group()).replace('-', '_'),
    '10mu'  : lambda x:str(re.search(r'\d{6}(-|_)\d{2}', x, re.I).group()).replace('-', '_'),
    'x-art' : lambda x:str(re.search(r'x-art\.\d{2}\.\d{2}\.\d{2}', x, re.I).group()),
    'xxx-av': lambda x:''.join(['xxx-av-', re.findall(r'xxx-av[^\d]*(\d{3,5})[^\d]*', x, re.I)[0]]),
    'heydouga': lambda x:'heydouga-' + '-'.join(re.findall(r'(\d{4})[\-_](\d{3,4})[^\d]*', x, re.I)[0]),
    'heyzo' : lambda x: 'HEYZO-' + re.findall(r'heyzo[^\d]*(\d{4})', x, re.I)[0]
}

def get_number_by_dict(filename: str) -> str:
    try:
        for k,v in G_TAKE_NUM_RULES.items():
            if re.search(k, filename, re.I):
                return v(filename)
    except:
        pass
    return None

class Cache_uncensored_conf:
    prefix = None
    def is_empty(self):
        return bool(self.prefix is None)
    def set(self, v: list):
        if not v or not len(v) or not len(v[0]):
            raise ValueError('input prefix list empty or None')
        s = v[0]
        if len(v) > 1:
            for i in v[1:]:
                s += f"|{i}.+"
        self.prefix = re.compile(s, re.I)
    def check(self, number):
        if self.prefix is None:
            raise ValueError('No init re compile')
        return self.prefix.match(number)

G_cache_uncensored_conf = Cache_uncensored_conf()

# ========================================================================是否为无码
def is_uncensored(number):
    if re.match(
r'[\d-]{4,}|\d{6}_\d{2,3}|(cz|gedo|k|n|red-|se)\d{2,4}|heyzo.+|xxx-av-.+|heydouga-.+|x-art\.\d{2}\.\d{2}\.\d{2}',
        number,
        re.I
    ):
        return True
    if G_cache_uncensored_conf.is_empty():
        G_cache_uncensored_conf.set(config.getInstance().get_uncensored().split(','))
    return G_cache_uncensored_conf.check(number)

