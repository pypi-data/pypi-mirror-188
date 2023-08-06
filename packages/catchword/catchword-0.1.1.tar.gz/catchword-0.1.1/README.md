# Catchword
Catchword prints out the matched lowercase words from the file. Search term exists on the last line of the file at all times. If there is no match, "**There is no word that matches with Search Term!**" will be printed out on console.

The search function was implemented by using **"Prefix Tree"**.

I try to follow [this][google/styleguide] style guide for this project. Check my docstrings and comments for detailed explanations. 

[google/styleguide]: https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings

# Setup
This project uses "setup.py" for packaging project. But since it is not recommened way for packaging the project, [this][packaging] can be followed instead of using "setup.py".

[packaging]: https://packaging.python.org/en/latest/tutorials/packaging-projects/

## 1. Check Python version
This project needs **Python** version that is greater than or equal to **3.10**.
```
python --version
```

## 2. Create virtual environment and activate it
See details at [here][venv].

[venv]: https://docs.python.org/3/library/venv.html

```
python -m venv venv
```
Once you create it.
```
(POSIX) source venv/bin/activate
```

## 3. Install requirements
```
python -m pip install -r requirements.txt
```

## 4. Run tests
```
python -m pytest
```

## 5. Build
This will create "dist" folder.
```
python -m build
```

## 6. Install
You can find the "wheel_file" at the "dist" folder.

```
python -m pip install ["wheel_file".whl]
```

## 7. Usage
"FILEPATH" should be absolute path of a file.
```
wordsearch ["FILEPATH"]
```