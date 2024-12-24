# gen_comp

一个基于help生成命令补全基本框架的工具，支持bash、zsh补全。

## 使用

实际上中help中解析出有用的信息是一件复杂的事情。面对各种各样的help文本，我们无法保证正确性。

目前我们无法正确的解析复杂的帮助文本，虽然代码里写了subcommands的逻辑，但是仍在实现中。现在仅支持选项。

实际上，本工具的定位是，在编写复杂的补全脚本时的辅助脚本，用于快速生成一个框架。避免重复性的工作。

我们这里提供一个简单的例子

```shell
python gen_comp.py -f help.txt
```

## todo

- [x] bash options
- [x] zsh options
- [ ] bash subcommands
- [ ] zsh subcommands
