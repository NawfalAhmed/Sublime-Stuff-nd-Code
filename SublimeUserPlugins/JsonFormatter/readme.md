# Json Formatter (through Yapf) Sublime Plugin

### Goals

A Json formatter that can nicely format sublime json files like keybindings, command files etc

### How it works

Instead of a Json Formatter, we use `python` package `YAPF` to format our json file,
Json Syntax can easily be interpeted by `python` as a `list` and `dictionary` combination,
hence the `python` formatter can interpret and format the code.

To handle the `//` comments we simply replace all occurances of `//` with `#` temporarily while formatting - we admit it's quite a primitive approach

### Requirments

Any `python` installed on your system path with the package `yapf`,
it can simply be installed on any `python>3.4` through `pip install yapf`
ST3 uses `python3.3.6` and the package `yapf` doesn't run on anything below `3.4` hence we regrettably can't use it internally in the package

### Configuration

In the `style.txt` folder under the package, in the user settings section, you can alter the 
indentation width and whether to use tabs or not.

To modify anything else refer to the link given inside the file
