# -*- coding:utf8 -*-
"""
@author: xiaolong.huang
@email: xiaolonghuang@emotibot.com
@time: 2023/1/1 14:04
@file: setup.py
@desc:
"""

# 引入构建包信息的模块
from setuptools import setup, find_packages
#
# try:  # for pip >= 10
#     from pip._internal.req import parse_requirements
#     from pip._internal.network.session import PipSession
# except ImportError:  # for pip <= 9.0.3
#     from pip.req import parse_requirements
#     from pip.download import PipSession
#
# install_reqs = parse_requirements('requirements.txt', session=PipSession())
# print(install_reqs)
# reqs = [str(ir.req) for ir in install_reqs]
# # 定义发布的包文件的信息
setup(
    name="kmapitool",  # 发布的包的名称
    version="1.0.3",  # 发布包的版本序号
    description="km api tool",  # 发布包的描述信息
    author="xiaolong.huang",  # 发布包的作者信息
    author_email="xiaolonghuang@emotibot.com",  # 作者的联系邮箱
    packages=["kmApi"],
    # include_package_data=True,  # include everything in source control
    # ...but exclude README.txt from all packages
    exclude_package_data={'': ['README.md'],
                          'tests': ['*.py']},
    install_requires=['requests==2.24.0']
)