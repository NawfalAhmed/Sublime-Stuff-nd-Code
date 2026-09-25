import sublime
import sublime_plugin
import os
import re
import shutil
import tempfile
import textwrap
from functools import lru_cache
from threading import Thread
from subprocess import CalledProcessError, SubprocessError
import subprocess

WINDOWS = os.name == "nt"

# ~/Sublime/json-style.txt, resolved through the UserPlugins symlink
STYLE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "json-style.txt"
)
TEMP = os.path.join(tempfile.gettempdir(), "sublime-json-format-temp.py")


def run(cmd, **kwargs):
    if WINDOWS:  # don't flash a console window per call
        kwargs.setdefault("creationflags", subprocess.CREATE_NO_WINDOW)
    return subprocess.run(cmd, **kwargs)


@lru_cache(maxsize=None)
def shell_path():
    # GUI apps on macOS/Linux can get a bare PATH, so borrow the login shell's.
    # Windows GUI apps already inherit the full user PATH.
    path = os.environ.get("PATH", "")
    shell = os.environ.get("SHELL")
    if shell and not WINDOWS:
        try:
            path = (
                run(
                    [shell, "-lc", "printenv PATH"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                ).stdout.strip()
                or path
            )
        except (OSError, SubprocessError):
            pass
    return path


def shell_env():
    env = dict(os.environ)
    env["PATH"] = shell_path()
    env["PYTHONIOENCODING"] = "utf-8"  # Windows defaults to the ANSI codepage
    return env


def find_yapf(env):
    path = env["PATH"]
    yapf = shutil.which("yapf", path=path)
    if yapf:
        return [yapf]
    pythons = [["py", "-3"], ["python"]] if WINDOWS else [["python3"], ["python"]]
    for python in pythons:
        exe = shutil.which(python[0], path=path)
        if (
            exe
            and run(
                [exe] + python[1:] + ["-c", "import yapf"],
                capture_output=True,
                env=env,
            ).returncode
            == 0
        ):
            return [exe] + python[1:] + ["-m", "yapf"]
    return None


def run_async(select, view):
    def fixstr(contents):
        contents = contents.replace("//", "#").replace("res:#", "res://")
        contents = contents.replace("true", "True").replace("false", "False")
        return re.sub(r",(\s*[\)\]\}])", r"\1", contents)

    env = shell_env()
    yapf = find_yapf(env)
    if not yapf:
        sublime.status_message(
            "FormatJson: yapf not found on PATH, install it with `{}`".format(
                "brew install yapf"
                if sublime.platform() == "osx"
                else "pip install yapf"
            )
        )
        return

    name = TEMP
    open(name, "w").close()  # clear file contents
    indents = []
    with open(name, "a", encoding="utf-8") as file:
        if not select:
            contents = view.substr(sublime.Region(0, view.size()))
            file.write(fixstr(contents))
        else:
            regions = map(view.line, view.sel()) if select == "lines" else view.sel()
            for region in regions:
                contents = view.substr(region)
                match = re.match(r"[\s\n]+", contents)
                indents.append(match.group() if match else None)
                file.write(fixstr(contents.lstrip()))
                file.write("\n# end region\n")

    try:
        yapf_result = run(
            yapf + [name, "--style", STYLE],
            capture_output=True,
            encoding="utf-8",
            env=env,
        )
        contents = yapf_result.stdout
        yapf_result.check_returncode()
    except CalledProcessError:
        annotation = textwrap.dedent(
            """
				<body>
					<style>
						#annotation-error {
							background-color: color(var(--background) blend(#fff 95%));
						}
						html.dark #annotation-error {
							background-color: color(var(--background) blend(#fff 95%));
						}
						html.light #annotation-error {
							background-color: color(var(--background) blend(#000 85%));
						}
						a {
							text-decoration: inherit;
						}
					</style>
					<div class="error" id=annotation-error>
						<span class="content">
							__content__
						</span>
					</div>
				</body>
			"""
        ).lstrip()
        view.add_regions(
            "format_error",
            [sublime.Region(view.line(view.sel()[0]).begin() + 1)],
            scope="invalid",
            annotations=[annotation.replace("__content__", "Invalid Syntax")],
            flags=(sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE),
            on_close=lambda: (
                view.erase_regions("format_error"),
                view.hide_popup(),
            ),
        )
        sublime.status_message(
            "FormatJson's dependency 'yapf' ran into an error"
            "while trying to format :'("
        )
        print(yapf_result.stderr)
        return
    contents = contents.replace("\r", "").replace("#", "//")
    contents = contents.replace("True", "true").replace("False", "false")
    sublime.set_timeout_async(
        lambda: view.run_command(
            "format_json_step2",
            {"select": select, "contents": contents, "indents": indents},
        )
    )


class FormatJsonCommand(sublime_plugin.WindowCommand):
    def run(self, select=False):
        Thread(
            target=run_async,
            args=(select, self.window.active_view()),
            name="FormatJson.run_async",
        ).start()


class FormatJsonStep2Command(sublime_plugin.TextCommand):
    def run(self, edit, select, contents, indents):
        contents = re.sub(r'("keys": \[.*\],)\s*("command")', r"\1 \2", contents)
        contents = re.sub(r"([^\s])}", r"\1 }", contents)
        if select:
            contents = list(filter(None, contents.split("\n// end region\n")))
            regions = reversed(self.view.sel())
            if select == "lines":
                regions = map(self.view.line, regions)
            zipped = zip(regions, reversed(contents), reversed(indents))
            for region, region_contents, indent in zipped:
                if indent:
                    region_contents = textwrap.indent(region_contents, indent)
                self.view.replace(edit, region, region_contents)
        else:
            self.view.replace(edit, sublime.Region(0, self.view.size()), contents)
