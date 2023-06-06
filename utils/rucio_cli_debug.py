# -*- coding: utf-8 -*-
import os

debug_port = os.getenv("DEBUG_PORT")
cli = os.getenv("RUCIO_BIN_NAME")
stage = os.getenv("DEBUG_STAGE")  # pre or post
rucio_bin_dir = "/opt/rucio/bin"
debug_func = [
    "# start_func\n",
    "    import os\n",
    "    import debugpy\n",
    f"    debugpy.listen((\"0.0.0.0\", {debug_port}))\n",
    '    print("⏳ VS Code debugger can now be attached, press F5 in VS Code ⏳", flush=True)\n',
    "    debugpy.wait_for_client()\n",
    '    print("🎉 VS Code debugger attached, enjoy debugging 🎉", flush=True)\n',
    "# end_func\n"
]


def add_debugger(f):
    lines = []
    with open(f, "r") as f:
        for line in f.readlines():
            lines.append(line)
            if "__name__ == " in line:
                lines.extend(debug_func)

    with open(f"{rucio_bin_dir}/{cli}", 'w') as f:
        f.write("".join(lines))


def remove_debugger(f):
    lines = []
    ignore_lines = False
    with open(f, "r") as f:
        for line in f.readlines():
            if "# start_func" in line:
                ignore_lines = True
            if "# end_func" in line:
                ignore_lines = False
                continue
            if not ignore_lines:
                lines.append(line)

    with open(f"{rucio_bin_dir}/{cli}", 'w') as f:
        f.write("".join(lines))


if __name__ == "__main__":
    f = f"{rucio_bin_dir}/{cli}"
    if stage == "pre":
        print(f"Adding debugger code to {f} at port {debug_port}")
        print("Add your debug points in the code and open a terminal to execute the command")
        print("Then run the approprate run config from the debug tab.")
        print("After you are finished debugging, run the appropriate cleanup for rucio-{bin}/")
        add_debugger(f)
        print("debugger added!")
    elif stage == "post":
        print(f"Removing debugger code from {f}")
        remove_debugger(f)
        print("debugger removed!")
    else:
        print("Nothing to do")
        exit(1)
