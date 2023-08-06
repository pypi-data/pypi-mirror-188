# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shirasu', 'shirasu.addon', 'shirasu.addons', 'shirasu.util']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0',
 'pydantic>=1.10.4,<2.0.0',
 'ujson>=5.7.0,<6.0.0',
 'websockets>=10.4,<11.0']

setup_kwargs = {
    'name': 'shirasu',
    'version': '0.0.2',
    'description': 'A simple bot framework to study the principles, based on OneBot v11.',
    'long_description': '# Shirasu\n\n## Introduction\n\n`Shirasu` is a simple bot framework to study the principles, based on  `OneBot v11` (especially `go-cqhttp`).\n\n出于练习英语的目的，本篇我就用简单英文写了（来自寒假末尾最后的倔强，其实是 Grammarly 监督才能避免一堆语法错误）。\n\n\n## Features\n\n+ Dependency Injection System, based on certain names with type-checking at runtime.\n\n  I\'m used to Spring\'s dependency injection system, which is like:\n\n  ```java\n  @Autowired\n  private Foo foo;\n  ```\n\n  I know it\'s better to use a setter or constructor, but let me just keep it simple.\n\n  However, dependency injection in `FastAPI` is like this:\n\n  ```python\n  async def get_foo() -> Foo:\n      return Foo()\n  \n  async def use(foo: Foo = Depends(get_foo)) -> None:\n      await foo.use()\n  ```\n\n  There are other frameworks like what Spring does for sure, but to study the principles, I implemented a simple dependency injection system.\n\n  ```python\n  from shirasu.di import inject, provide\n  from datetime import datetime\n  \n  @provide(\'now\')\n  async def provide_now() -> datetime:\n      return datetime.now()\n  \n  @inject()\n  async def use_now(now: datetime) -> None:\n      print(now.strftime(\'%Y-%m-%d %H:%M:%S\'))\n  \n  @inject()\n  async def use_now_wrong_type(now: int) -> None:\n      print(f\'This will not be executed because {now} is a datetime, not an int.\')\n  \n  # Prints current datetime.\n  await use_now()\n  \n  # Raises.\n  await use_now_wrong_type()\n  ```\n\n  To keep the code simple, everything should be `async`.\n\n  The annotation of each injected parameter **cannot be a string**(e.g. using `"datetime"` as the annotation for the parameter `now` is incorrect).\n\n  They should be real types because the injector will check if they are correct.\n\n+ Addon System, without the need of ensuring import orders.\n\n  Write later.\n\n+ Convenient(Maybe) Configuration.\n\n  Write later.\n\n\n+ Easy to test.\n\n  Writer later.\n\n',
    'author': 'kifuan',
    'author_email': 'kifuan@foxmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
