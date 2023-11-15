import sys
import subprocess
import os

def main():
    if len(sys.argv) != 2:
        print("need an arg for new post position: /yyyy/mm/dd(-n).md")
        sys.exit(1)

    # 获取参数
    param = sys.argv[1]

    # 保存当前目录
    original_directory = os.getcwd()

    try:
        # 更改工作目录到 /pages/diary/
        os.chdir('./pages/diary/')

        # 运行 markdown_convertor.py 脚本
        subprocess.run(['python', 'markdown_convertor.py', param], check=True)

        # 运行 index_generator.py 脚本
        subprocess.run(['python', 'index_generator.py'], check=True)

    finally:
        # 无论如何都返回原始目录
        os.chdir(original_directory)

    # 执行 Git 相关命令
    subprocess.run(['git', 'add', '*'], check=True)
    subprocess.run(['git', 'commit', '-m', 'post'], check=True)
    subprocess.run(['git', 'push'], check=True)


if __name__ == "__main__":
    main()