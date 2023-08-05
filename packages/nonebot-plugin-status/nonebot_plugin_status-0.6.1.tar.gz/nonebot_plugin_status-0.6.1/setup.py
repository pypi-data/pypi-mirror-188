# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '..'}

packages = \
['nonebot_plugin_status']

package_data = \
{'': ['*'], 'nonebot_plugin_status': ['dist/*']}

install_requires = \
['Jinja2>=3.0.0,<4.0.0',
 'humanize>=4.0.0,<5.0.0',
 'nonebot2>=2.0.0-beta.1,<3.0.0',
 'psutil>=5.7.2,<6.0.0']

extras_require = \
{'onebot': ['nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0']}

setup_kwargs = {
    'name': 'nonebot-plugin-status',
    'version': '0.6.1',
    'description': 'Check your server status (CPU, Memory, Disk Usage) via nonebot',
    'long_description': '<!--\n * @Author         : yanyongyu\n * @Date           : 2020-11-15 14:40:25\n * @LastEditors    : yanyongyu\n * @LastEditTime   : 2022-11-05 16:13:36\n * @Description    : None\n * @GitHub         : https://github.com/yanyongyu\n-->\n\n<!-- markdownlint-disable MD033 MD036 MD041 -->\n\n<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>\n</p>\n\n<div align="center">\n\n# nonebot-plugin-status\n\n_✨ NoneBot 服务器状态（CPU, Memory, Disk Usage）查看插件 ✨_\n\n</div>\n\n<p align="center">\n  <a href="https://raw.githubusercontent.com/cscs181/QQ-Github-Bot/master/LICENSE">\n    <img src="https://img.shields.io/github/license/cscs181/QQ-Github-Bot.svg" alt="license">\n  </a>\n  <a href="https://pypi.python.org/pypi/nonebot-plugin-status">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-status.svg" alt="pypi">\n  </a>\n  <img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="python">\n</p>\n\n## 使用方式\n\n通用:\n\n- 发送 Command `状态` 或者 `status`\n\nOneBot:\n\n- 向机器人发送戳一戳表情\n- 双击机器人头像戳一戳\n\n## 配置项\n\n> **warning**\n> GitHub 仓库中的文档为最新 DEV 版本，配置方式请参考 [PyPI](https://pypi.org/project/nonebot-plugin-status/) 上的文档。\n\n配置方式：直接在 NoneBot 全局配置文件中添加以下配置项即可。\n\n### server_status_enabled\n\n- 类型：`bool`\n- 默认值：`True`\n- 说明：是否启用服务器状态查看功能\n\n### server_status_truncate\n\n- 类型：`bool`\n- 默认值：`True`\n- 说明：是否启用模板变量按需注入功能（节约时间）\n\n### server_status_only_superusers\n\n- 类型: `bool`\n- 默认: `True`\n- 说明: 是否仅允许超级用户使用\n\n> 超级用户需在配置文件中如下配置:\n>\n> ```dotenv\n> SUPERUSERS=["your qq id"]\n> ```\n\n### server_status_template\n\n- 类型: `str`\n- 默认: 请参考示例\n- 说明：发送的消息模板，支持的方法、变量以及类型如下：\n  - relative_time (`Callable[[datetime], timedelta]`): 获取相对时间\n  - humanize_date (`Callable[[datetime], str]`): [人性化时间](https://python-humanize.readthedocs.io/en/latest/time/#humanize.time.naturaldate)\n  - humanize_delta (`Callable[[timedelta], str]`): [人性化时间差](https://python-humanize.readthedocs.io/en/latest/time/#humanize.time.precisiondelta)\n  - cpu_usage (`float`): CPU 使用率\n  - per_cpu_usage (`List[float]`): 每个 CPU 核心的使用率\n  - memory_usage (`svmem`): 内存使用情况，包含 total, available, percent, used, free(, active, inactive, buffers, cached, shared) 属性\n  - swap_usage (`sswap`): 内存使用情况，包含 total, used, free, percent, sin, sout 属性\n  - disk_usage (`Dict[str, psutil._common.sdiskusage]`): 磁盘使用率，包含 total, used, free, percent 属性\n  - uptime (`datetime`): 服务器运行时间\n  - runtime (`datetime`): NoneBot 运行时间\n  - bot_connect_time (`Dict[str, datetime]`): 机器人连接时间\n\n配置文件示例（默认模板）\n\n```dotenv\nSERVER_STATUS_TEMPLATE=\'\nCPU: {{ "%02d" % cpu_usage }}%\nMemory: {{ "%02d" % memory_usage.percent }}%\nRuntime: {{ runtime | relative_time | humanize_delta }}\n{% if swap_usage.total %}Swap: {{ "%02d" % swap_usage.percent }}%{% endif %}\nDisk:\n{% for name, usage in disk_usage.items() %}\n  {{ name }}: {{ "%02d" % usage.percent }}%\n{% endfor %}\n\'\n```\n',
    'author': 'yanyongyu',
    'author_email': 'yanyongyu_1@126.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/cscs181/QQ-GitHub-Bot/tree/master/src/plugins/nonebot_plugin_status',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
