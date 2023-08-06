# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src',
 'src.data_pipeline',
 'src.data_pipeline.feature_engineering',
 'src.data_pipeline.pre_processing',
 'src.parser']

package_data = \
{'': ['*'], 'src': ['yamls/*']}

install_requires = \
['Jinja2==3.1.2',
 'MarkupSafe==2.1.1',
 'Pillow==9.4.0',
 'PyYAML==6.0',
 'altair==4.2.0',
 'attrs==22.2.0',
 'bpemb==0.3.4',
 'certifi==2022.12.7',
 'charset-normalizer==2.1.1',
 'contourpy==1.0.6',
 'coverage==7.0.2',
 'cycler==0.11.0',
 'entrypoints==0.4',
 'exceptiongroup==1.1.0',
 'fonttools==4.38.0',
 'gensim==3.8.3',
 'idna==3.4',
 'importlib-resources==5.10.2',
 'iniconfig==1.1.1',
 'joblib==1.2.0',
 'jsonschema==4.17.3',
 'kiwisolver==1.4.4',
 'matplotlib==3.6.2',
 'numpy==1.24.1',
 'packaging==22.0',
 'pandas==1.5.2',
 'pkgutil-resolve-name==1.3.10',
 'pluggy==1.0.0',
 'pyparsing==3.0.9',
 'pyrsistent==0.19.3',
 'pytest-cov==4.0.0',
 'pytest==7.2.0',
 'python-dateutil==2.8.2',
 'pytz==2022.7',
 'requests==2.28.1',
 'scikit-learn==1.2.0',
 'scipy==1.9.3',
 'sentencepiece==0.1.97',
 'six==1.16.0',
 'smart-open==6.3.0',
 'threadpoolctl==3.1.0',
 'tomli==2.0.1',
 'toolz==0.12.0',
 'tqdm==4.64.1',
 'urllib3==1.26.13',
 'whatlies==0.7.0',
 'zipp==3.11.0']

setup_kwargs = {
    'name': 'trabalho-de-gces',
    'version': '0.1.2',
    'description': '',
    'long_description': "# Trabalho GCES\n\n\n\n## Getting started\n\nTo make it easy for you to get started with GitLab, here's a list of recommended next steps.\n\nAlready a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!\n\n## Add your files\n\n- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files\n- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:\n\n```\ncd existing_repo\ngit remote add origin https://gitlab.com/spiker32/trabalho-de-gces.git\ngit branch -M main\ngit push -uf origin main\n```\n\n## Integrate with your tools\n\n- [ ] [Set up project integrations](https://gitlab.com/spiker32/trabalho-de-gces/-/settings/integrations)\n\n## Collaborate with your team\n\n- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)\n- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)\n- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)\n- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)\n- [ ] [Automatically merge when pipeline succeeds](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)\n\n## Test and Deploy\n\nUse the built-in continuous integration in GitLab.\n\n- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)\n- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing(SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)\n- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)\n- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)\n- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)\n\n***\n\n# Editing this README\n\nWhen you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thank you to [makeareadme.com](https://www.makeareadme.com/) for this template.\n\n## Suggestions for a good README\nEvery project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.\n\n## Name\nChoose a self-explaining name for your project.\n\n## Description\nLet people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.\n\n## Badges\nOn some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.\n\n## Visuals\nDepending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.\n\n## Installation\nWithin a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.\n\n## Usage\nUse examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.\n\n## Support\nTell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.\n\n## Roadmap\nIf you have ideas for releases in the future, it is a good idea to list them in the README.\n\n## Contributing\nState if you are open to contributions and what your requirements are for accepting them.\n\nFor people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.\n\nYou can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.\n\n## Authors and acknowledgment\nShow your appreciation to those who have contributed to the project.\n\n## License\nFor open source projects, say how it is licensed.\n\n## Project status\nIf you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.\n",
    'author': 'Antonio Igor Carvalho',
    'author_email': 'antonioigorcarvalho@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.16,<4.0.0',
}


setup(**setup_kwargs)
