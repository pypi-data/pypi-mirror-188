# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nlhappy',
 'nlhappy.algorithms',
 'nlhappy.callbacks',
 'nlhappy.configs',
 'nlhappy.data',
 'nlhappy.datamodules',
 'nlhappy.layers',
 'nlhappy.layers.attention',
 'nlhappy.layers.classifier',
 'nlhappy.layers.embedding',
 'nlhappy.metrics',
 'nlhappy.models',
 'nlhappy.models.entity_extraction',
 'nlhappy.models.event_extraction',
 'nlhappy.models.prompt_relation_extraction',
 'nlhappy.models.question_answering',
 'nlhappy.models.relation_extraction',
 'nlhappy.models.span_extraction',
 'nlhappy.models.text_classification',
 'nlhappy.models.text_multi_classification',
 'nlhappy.models.text_pair_classification',
 'nlhappy.models.text_pair_regression',
 'nlhappy.models.token_classification',
 'nlhappy.tricks',
 'nlhappy.utils']

package_data = \
{'': ['*'],
 'nlhappy.configs': ['callbacks/*',
                     'datamodule/*',
                     'log_dir/*',
                     'logger/*',
                     'model/*',
                     'trainer/*']}

install_requires = \
['datasets>=2.0.0',
 'hydra-colorlog>=1.1.0',
 'hydra-core==1.1',
 'pydantic==1.10.2',
 'pytorch-lightning>=1.6.5',
 'rich>=12.4.3,<13.0.0',
 'srsly>=2.4.5',
 'torch>=1.8.0',
 'transformers>=4.17.0']

entry_points = \
{'console_scripts': ['nlhappy = nlhappy.run:train']}

setup_kwargs = {
    'name': 'nlhappy',
    'version': '2023.1.31',
    'description': '自然语言处理(NLP)',
    'long_description': '\n<div align=\'center\'>\n\n# nlhappy\n<a href="https://pytorch.org/get-started/locally/"><img alt="PyTorch" src="https://img.shields.io/badge/PyTorch-ee4c2c?logo=pytorch&logoColor=white"></a>\n<a href="https://pytorchlightning.ai/"><img alt="Lightning" src="https://img.shields.io/badge/-Lightning-792ee5?logo=pytorchlightning&logoColor=white"></a>\n<a href="https://hydra.cc/"><img alt="Config: Hydra" src="https://img.shields.io/badge/Config-Hydra-89b8cd"></a>\n<a href="https://github.com/ashleve/lightning-hydra-template"><img alt="Template" src="https://img.shields.io/badge/-Lightning--Hydra--Template-017F2F?style=flat&logo=github&labelColor=gray"></a>\n<a href="https://wandb.ai/"><img alt="WanDB" src="https://img.shields.io/badge/Log-WanDB-brightgreen"></a>\n</div>\n<br><br>\n\n## 📌&nbsp;&nbsp; 简介\n\nnlhappy致力于复现自然语言处理各类任务的SOTA模型。\n> 文档地址:\n- [notion文档](https://wangmengdi.notion.site/NLHAPPY-264f05d1084848efa42068c83539904a)\n> 它主要的依赖有\n- [transformers](https://huggingface.co/docs/transformers/index): 下载预训练权重\n- [pytorch-lightning](https://pytorch-lightning.readthedocs.io/en/latest/): 模型训练\n- [datasets](https://huggingface.co/docs/datasets/index): 构建数据集\n- [pydantic](https://wandb.ai/): 数据校验\n\n\n## 📌&nbsp;&nbsp; 安装\n<details>\n<summary><b>安装nlhappy</b></summary>\n\n> 推荐先去[pytorch官网](https://pytorch.org/get-started/locally/)安装pytorch和对应cuda\n```bash\n# pip 安装\npip install --upgrade pip\npip install --upgrade nlhappy\n```\n</details>\n\n<details>\n<summary><b>其他可选</b></summary>\n\n> 推荐安装wandb用于可视化训练日志\n- 安装: \n```bash\npip install wandb \n```\n- 注册: https://wandb.ai/\n- 获取认证: https://wandb.ai/authorize\n- 登陆:\n```bash\nwandb login\n```\n- 使用\n```\n# 命令行训练\nnlhappy datamodule=xxx model=xxx trainer=xxx logger=wandb\n```\n模型训练开始后去[官网](https://wandb.ai/)查看训练实况\n</details>\n\n\n## 📌&nbsp;&nbsp; 模型复现\n\n### 实体抽取\n|模型名称|参考链接|\n|----|----|\n|GlobalPointer|[科学空间](https://kexue.fm/archives/8373)|\n|EfficientGlobalPointer|[科学空间](https://kexue.fm/archives/8877)|\n\n### 关系抽取\n|模型名称|参考链接|\n|----|----|\n|GPLinker|[科学空间](https://kexue.fm/archives/8888)|\n\n### 事件抽取\n|模型名称|参考链接|\n|----|----|\n|GPLinker|[科学空间](https://kexue.fm/archives/8926)|\n\n### 答案抽取\n|模型名称|参考链接|\n|----|----|\n|GPLinker|-|',
    'author': 'wangmengdi',
    'author_email': '790990241@qq.om',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
