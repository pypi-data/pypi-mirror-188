# Time Trcaker Python Package on any platform.
## First use my template repo to create this repo.
- template repo = https://github.com/SachinMishra-ux/pypi_template

```
python template.py
```

```
bash init_setup.sh
```
```
1) conda activate ./env
2) pip list
```
```
mypy src/  - for checking any issues in your python code.
```
- o/p of above command - Success: no issues found in 3 source files
```
pytest -v   - for any unit test
```
```
tox
```
- then commit everything on github
- then add new workflow for python package
- ![](./Assets/img1.png)
- ![](./Assets/img2.png)

- Now add secrets to your github and change the ```python publish.yml``` file according to your needs. To acchieve this get API from python-pypi site



Tracking the desktop applications in real time and time spent on each application and saving the data in json format.

Dependencies:

- selenium


Windows Depencies

- pywin32
- python-dateutil
- uiautomation 
