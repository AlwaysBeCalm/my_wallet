set pth=%cd%

python3 -m venv %pth%\.venv

%pth%\.venv\Scripts\python.exe -m pip install --upgrade pip

%pth%\.venv\Scripts\pip.exe install -r requirements.txt

%pth%\.venv\Scripts\pip3.exe install -r requirements.txt

%pth%\.venv\Scripts\python.exe %pth%\src\main.py