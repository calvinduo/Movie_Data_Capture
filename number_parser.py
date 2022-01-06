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

if __name__ == "__main__":
#     import doctest
#     doctest.testmod(raise_on_error=True)
    test_use_cases = (
        "MEYD-594-C.mp4",
        "SSIS-001_C.mp4",
        "SSIS100-C.mp4",
        "SSIS101_C.mp4",
        "ssni984.mp4",
        "ssni666.mp4",
        "SDDE-625_uncensored_C.mp4",
        "SDDE-625_uncensored_leak_C.mp4",
        "SDDE-625_uncensored_leak_C_cd1.mp4",
        "Tokyo Hot n9001 FHD.mp4", # 无-号，以前无法正确提取
        "TokyoHot-n1287-HD SP2006 .mp4",
        "caribean-020317_001.nfo",     # -号误命名为_号的
        "257138_3xplanet_1Pondo_080521_001.mp4",
        "ADV-R0624-CD3.wmv",           # 多碟影片
        "XXX-AV   22061-CD5.iso",      # 新支持片商格式 xxx-av-22061 命名规则来自javdb数据源
        "xxx-av 20589.mp4",
        "Muramura-102114_145-HD.wmv",  # 新支持片商格式 102114_145  命名规则来自javdb数据源
        "heydouga-4102-023-CD2.iso",   # 新支持片商格式 heydouga-4102-023 命名规则来自javdb数据源
        "HeyDOuGa4236-1048 Ai Qiu - .mp4", # heydouga-4236-1048 命名规则来自javdb数据源
        "pacopacomama-093021_539-FHD.mkv", # 新支持片商格式 093021_539 命名规则来自javdb数据源
        "sbw99.cc@heyzo_hd_2636_full.mp4"
    )
    def evprint(evstr):
        code = compile(evstr, "<string>", "eval")
        print("{1:>20} # '{0}'".format(evstr[18:-2], eval(code)))
    for t in test_use_cases:
        evprint(f'get_number(True, "{t}")')

    if len(sys.argv)<=1 or not re.search('^[A-Z]:?', sys.argv[1], re.IGNORECASE):
        sys.exit(0)

    # 使用Everything的ES命令行工具搜集全盘视频文件名作为用例测试number数据，参数为盘符 A .. Z 或带盘符路径
    # https://www.voidtools.com/support/everything/command_line_interface/
    # ES命令行工具需要Everything文件搜索引擎处于运行状态，es.exe单个执行文件需放入PATH路径中。
    # Everything是免费软件
    # 示例：
    # python.exe .\number_parser.py ALL                 # 从所有磁盘搜索视频
    # python.exe .\number_parser.py D                   # 从D盘搜索
    # python.exe .\number_parser.py D:                  # 同上
    # python.exe .\number_parser.py D:\download\JAVs    # 搜索D盘的\download\JAVs目录，路径必须带盘符
    # ==================
    # Linux/WSL1|2 使用mlocate(Ubuntu/Debian)或plocate(Debian sid)搜集全盘视频文件名作为测试用例number数据
    # 需安装'sudo apt install mlocate或plocate'并首次运行sudo updatedb建立全盘索引
    # MAC OS X 使用findutils的glocate，需安装'sudo brew install findutils'并首次运行sudo gupdatedb建立全盘索引
    # 示例：
    # python3 ./number_parser.py ALL
    import subprocess
    ES_search_path = "ALL disks"
    if sys.argv[1] == "ALL":
        if sys.platform == "win32":
            # ES_prog_path = 'C:/greensoft/es/es.exe'
            ES_prog_path = 'es.exe'  # es.exe需要放在PATH环境变量的路径之内
            ES_cmdline = f'{ES_prog_path} -name size:gigantic ext:mp4;avi;rmvb;wmv;mov;mkv;flv;ts;webm;iso;mpg;m4v'
            out_bytes = subprocess.check_output(ES_cmdline.split(' '))
            out_text = out_bytes.decode('gb18030') # 中文版windows 10 x64默认输出GB18030，此编码为UNICODE方言与UTF-8系全射关系无转码损失
            out_list = out_text.splitlines()
        elif sys.platform in ("linux", "darwin"):
            ES_prog_path = 'locate' if sys.platform == 'linux' else 'glocate'
            ES_cmdline = r"{} -b -i --regex '\.mp4$|\.avi$|\.rmvb$|\.wmv$|\.mov$|\.mkv$|\.webm$|\.iso$|\.mpg$|\.m4v$'".format(ES_prog_path)
            out_bytes = subprocess.check_output(ES_cmdline.split(' '))
            out_text = out_bytes.decode('utf-8')
            out_list = [ os.path.basename(line) for line in out_text.splitlines()]
        else:
            print('[-]Unsupported platform! Please run on OS Windows/Linux/MacOSX. Exit.')
            sys.exit(1)
    else: # Windows single disk
        if sys.platform != "win32":
            print('[!]Usage: python3 ./number_parser.py ALL')
            sys.exit(0)
        # ES_prog_path = 'C:/greensoft/es/es.exe'
        ES_prog_path = 'es.exe'  # es.exe需要放在PATH环境变量的路径之内
        if os.path.isdir(sys.argv[1]):
            ES_search_path = sys.argv[1]
        else:
            ES_search_path = sys.argv[1][0] + ':/'
            if not os.path.isdir(ES_search_path):
                ES_search_path = 'C:/'
            ES_search_path = os.path.normcase(ES_search_path)
        ES_cmdline = f'{ES_prog_path} -path {ES_search_path} -name size:gigantic ext:mp4;avi;rmvb;wmv;mov;mkv;webm;iso;mpg;m4v'
        out_bytes = subprocess.check_output(ES_cmdline.split(' '))
        out_text = out_bytes.decode('gb18030') # 中文版windows 10 x64默认输出GB18030，此编码为UNICODE方言与UTF-8系全射关系无转码损失
        out_list = out_text.splitlines()
    print(f'\n[!]{ES_prog_path} is searching {ES_search_path} for movies as number parser test cases...')
    print(f'[+]Find {len(out_list)} Movies.')
    for filename in out_list:
        try:
            n = get_number(True, filename)
            if n:
                print('  [{0}] {2}# {1}'.format(n, filename, '#无码' if is_uncensored(n) else ''))
            else:
                print(f'[-]Number return None. # {filename}')
        except Exception as e:
            print(f'[-]Number Parser exception: {e} [{filename}]')

    sys.exit(0)
