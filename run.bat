set pth=%cd%

python3 -m venv %pth%\.venv

%pth%\.venv\Scripts\python*.exe -m pip install --upgrade pip
%pth%\.venv\Scripts\python*.exe -m pip install --upgrade pip3

%pth%\.venv\Scripts\pip.exe install -r %pth%\requirements.txt

%pth%\.venv\Scripts\pip3.exe install -r %pth%\requirements.txt

%pth%\.venv\Scripts\python.exe %pth%\src\main.py

del %pth%\run*
