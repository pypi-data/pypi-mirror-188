# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['batch_ida']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'batch-ida',
    'version': '0.1.2',
    'description': '',
    'long_description': "# Batch-IDA\n\nA python library for comparing folders and generate ida and bindiff files in batch mode. \n\n## Purpose\n\n1. Batch generation of idb files from binary files\n2. Use bindiff to batch compare idb files\n3. Roughly read the comparison results\n\n## Notice\n\n+ IDA pro 7 and Bindiff 7 requires pre-installation. (Only tested on IDA pro 7.7 and bindiff 7)\n\n## Install\n\n```\npip install --upgrade batch-ida\n```\n\n## Usage\n\n### BI_Dircmp\n\nCompare files in dirA & dirB, and move different files to dst_a & dst_b.\n\n```python\n# 1. BI_Dircmp比较原文件夹，并复制哈希不同的文件到目标文件夹\nfrom batch_ida import BI_Dircmp\n\n# 原始文件夹dirA，dirB，包含需要比较的二进制\ndirA = r'\\\\wsl.localhost\\Ubuntu-22.04\\home\\zzh\\fw_project/d9_idrac/_5.00.10.20.d9.extracted/squashfs-root/usr/lib/'\ndirB = r'\\\\wsl.localhost\\Ubuntu-22.04\\home\\zzh\\fw_project/d9_idrac/_5.00.20.00.d9.extracted/squashfs-root/usr/lib/'\n\n# 目标文件夹dstA，dstB，用来存放哈希值不同的二进制，是空文件夹\ndst_a = r'C:\\Users\\zzhihan\\Desktop\\36347\\1020'\ndst_b = r'C:\\Users\\zzhihan\\Desktop\\36347\\2000'\n\n# 使用Dircmp比较两个文件夹中文件的差异，并将哈希不同的文件复制到目标文件夹\nbid = BI_Dircmp(dirA, dirB, dst_a, dst_b)\nbid.cmp()\n```\n\n### BI_Bindiff\n\nGenerate .ida and .bindiff files in batch mode.\n\n```python\n# 使用Bindiff批量分析二进制文件\nfrom batch_ida import BI_Bindiff\n\nbib = BI_Bindiff()\n\n# 设置ida和bindiff路径\nbib.set_ida_path('C:\\Tools\\IDA Pro')\nbib.set_bindiff_path('C:\\Program Files\\BinDiff')\nbib.max_subprocess = 16\n\n# 开始比较，结果输出到output文件夹，批量生成idb比较慢\noutput = bib.batch_bindiff(dst_a, dst_b)\n```\n\n### BI_Analyzer\n\nAnalyze Bindiff files (sqlite3 file format) in batch mode and print the results.\n\n```python\n# 使用Analyzer批量读输出的Bindiff文件，其实就是sqlite3数据库文件\nfrom batch_ida import BI_Analyzer\n\nbia = BI_Analyzer(r'C:\\Users\\zzhihan\\Desktop\\test\\4_4010_vs_4_4040')\nbia.print_base_info()\n```\n",
    'author': 'ZhengZH',
    'author_email': '41407837+chnzzh@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/chnzzh/batch-ida',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
