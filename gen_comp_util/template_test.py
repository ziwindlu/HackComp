from common import *

template_data = {
    "cmd_name": "mycli",
    "options": [
        {
            "name": "--help",
            "description": "帮助"
        },
        {
            "name": "--version",
            "description": "版本"
        }
    ],
    "reg_cmd": template_util.escape_reg_cmd("python mycli")

}

zsh_template = template_util.get_template("zsh_comp_template")
zsh_script = zsh_template.render(**template_data)

with open("mycli_zsh_completion.zsh", "w") as zsh_file:
    zsh_file.write(zsh_script)
template_util.rm_empty_lines("mycli_zsh_completion.zsh")
