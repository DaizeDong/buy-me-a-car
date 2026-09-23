# buy-me-a-car

这套工具包含 16 个技能，帮助买家查车源、比较书面报价、准备经销商回信，并整理购车决策档案。
一般购车请求默认交付市场比较、买方研究 HTML 和 PDF。助手复用已知需求并准备报告输入，
用户不必另说“展开写”“生成 PDF”，也不必自己填写 JSON 模板。
公开仓库只存工具和可重新生成的合成示例；真实购车记录必须放在已验证为私有的伴生 Git 仓库。

[English](README.md) · [主技能](skills/orchestrator/SKILL.md) · [后续工作](ROADMAP.md)

## 已实现的能力

- OTD（落地总价）使用十进制金额计算，按已核实的州规则检查适用范围。规则未知、过期或交易类型不支持时拒绝计算。
- 经销商回信由已批准的问题、报价证据和对外报价生成。内部最高预算单独保存。
- 邮件导入保留账号、消息和游标标识；草稿导出记录操作状态和回执，执行结果不确定时禁止直接重放。
- 买方研究报告覆盖需求、检索范围、车型取舍、车源、成本、用途适配、冬季使用、持有成本、推荐、下一步和来源。没有书面报价时照常交付，未知费用保留未知。
- 报告检查证据日期和文件哈希，转义插入文本并验证 PDF。研究报告当前支持中文；经销商提案保留完整书面报价要求，支持英文、中文和西班牙文。
- 安装器注册全部 16 个技能，提前检查名称冲突，支持 Windows 目录联接。
- 真实输入和输出统一通过私有目录解析器；找不到私有仓、可见性不明或路径越界时停止写入。

车源搜索需要当前会话提供搜索或浏览器工具。Gmail、后台定时运行、发信和预约还需要实际可用的集成与对应授权。
本仓库不自带这些外部服务。合成示例和本地测试不能证明真实购车节省了多少钱。
具体交付流程见[默认报告工作流](skills/orchestrator/references/report_delivery.md)。存档证明采集到了什么，不证明车辆仍在售或卖方陈述属实。

## 安装

需要 Python 3.10 以上、Git 和完整子模块。PDF 推荐使用 Chrome 或 Edge。

```sh
git clone --recurse-submodules https://github.com/DaizeDong/buy-me-a-car.git
cd buy-me-a-car
python -m pip install -r requirements.txt
git config core.hooksPath .githooks
python tools/install.py
python tools/install.py --apply
python tools/doctor.py
```

安装器默认先预览，`--apply` 才创建链接，默认目录为 `~/.agents/skills`。
其他宿主可使用 `--target <技能目录>`。遇到已有的无关技能会拒绝覆盖。
安装后启动新会话，让宿主重新发现技能。Claude 插件宿主也可把本仓库作为本地插件加载。

已有仓库缺少子模块时，运行 `git submodule update --init --recursive`。不要绕过安全钩子。

## 真实数据初始化

在公开仓库之外建立或克隆一个**私有 GitHub 伴生仓库**，创建其中的 `data` 目录。
把 `BUY_ME_A_CAR_CONFIG` 设置为伴生仓根目录，并完成 GitHub CLI 的认证，然后运行：

```sh
python tools/runtime_paths.py --write
```

输出会标明核实过的私有仓与 DATA 路径。公开仓、未知可见性、未初始化目录和没有版本管理的散目录均不能接收真实记录。
只读检查可以报告“未初始化”；写操作必须失败并给出初始化指引。

买家需求、网页截图、报价、邮件状态、PDF、反馈和模型评测回执，都保存在私有伴生仓，并沿用它的版本管理与备份流程。
不要在公开模板或被 gitignore 忽略的仓内目录填写真实内容。

```sh
python tools/runtime_paths.py cycles/example/criteria.md --write
```

这里的相对路径以私有 DATA 为根。先解析路径，再复制空白模板并填写。
浏览器和抓取命令也应在已验证的私有周期目录执行。

## 使用与验收

完整购车流程从[主技能](skills/orchestrator/SKILL.md)开始；单项任务直接用对应技能。
全部技能和命令示例见[英文说明](README.md#skills-and-routing)。

合成的 Maryland 普通经销商购车算例：

```sh
python skills/orchestrator/scripts/otd_calculator.py --state MD --sales 30000 --doc 800 --title 200 --reg 120.50 --forward --json
python skills/orchestrator/scripts/otd_calculator.py --list-states
python skills/orchestrator/scripts/check_freshness.py --report-only
```

示例费用只是测试输入。实际费用必须按注册地、日期、车辆和交易类型核实。
州数据表覆盖全部州与 DC，不等于全部州都支持完整计算。

```sh
python tools/make_fixtures.py --check
python tools/check_repository.py
python skills/orchestrator/scripts/render_state_data.py --check
python -m unittest discover -s eval -p "test_*.py" -v
python eval/test_rubric.py
```

离线检查验证程序规则。另行运行 `python eval/test_rubric.py --llm` 才会通过本机 `llmcall` 实际调用模型并独立复核，
完整输入与回执写入私有 DATA。超时、不可用或失败不能算通过，结果不确定的调用不能自动重放。

`python eval/run_scenarios.py --llm` 会测试“阿拉斯加买皮卡”及税费、拖挂能力追问的实际中文回答，
并另行调用模型评审。测试范围与结果说明见[评测文档](eval/README.md)。

PDF 的 demo 模式只接受生成器产出的合成配置；真实档案必须用
[live 模式](skills/dossier-builder/SKILL.md)，提供完整报价与实际证据。
每次都要逐页查看最终 PDF，页数由内容决定。

## 当前边界

本地验证无法代替真实发信、经销商确认、税务机关认定或实际成交。
车源、补贴、保修和税费规则都可能变化，需要当前证据。

三种语言的档案模板只翻译固定标签，不会自动翻译任意输入段落。
经销商回信渲染器当前只支持 ASCII 英文。[九个场景](examples/README.md)都是合成输入和预期行为，不是成交记录。

MIT，见 [LICENSE](LICENSE) 和 [CHANGELOG.md](CHANGELOG.md)。
