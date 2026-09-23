# buy-me-a-car

用 16 个技能完成美国购车研究，从第一句话推进到候选车比较、买方报告和交车清单。

[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-orange?style=flat)](https://docs.anthropic.com/en/docs/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/Skills-16-green?style=flat)](#orchestrator)
[![Languages](https://img.shields.io/badge/Languages-EN%20%2F%20CN-blue?style=flat)](#语言)
[![Roadmap](https://img.shields.io/badge/Roadmap-v0.2.2%20alpha-purple?style=flat)](ROADMAP.md)

[English](README.md) | [中文版](README_CN.md)

---

## ⭐ 先读这里，设计理念

一次有用的购车判断，需要可比的成本、车辆证据和能执行的下一步。广告低价、不完整的报价或一长串搜索结果，都不足以单独支持决定。这套流程遵循五条原则：

1. **比较完整成本。** 先确认预算指车价还是落地总价（OTD），分别列出有依据的税费、杂费和运输成本，未知金额明确保留。
2. **把研究交付完整。** 复用已知需求，集中询问会影响判断的缺失信息，并直接把研究整理成比较表和 HTML/PDF 报告。
3. **由买家控制行动。** 内部最高预算与获准对外提出的价格分开。草稿必须有证据，联系卖方、预约和其他对外承诺需要相应授权。
4. **让证据可追溯。** 保存来源日期、原始材料、访问受阻情况和相互冲突的记录。采集到车源只说明当时看到了什么，不保证现在仍在售。
5. **把购车记录留在私有仓。** 公开仓库是一件未初始化的工具。真实需求、报价和报告属于买家已验证为私有的伴生 Git 仓库。

完整操作规则见[主技能](skills/orchestrator/SKILL.md)和[默认报告工作流](skills/orchestrator/references/report_delivery.md)。

## 它是什么（不是什么）

一个主技能协调美国购车流程，15 个专项技能处理落地价计算、车辆历史审阅、置换估值、租赁比较、回信草稿和签约检查等任务。单个问题可以直接用专项技能，完整买车过程由主技能衔接。

一般购车请求默认包含市场比较和买方研究 HTML/PDF。没有经销商书面报价时，研究仍可继续。对外经销商提案另有更严格的完整报价要求。

这是一套助手技能包，使用宿主提供的搜索、浏览器和邮箱工具；它不安装 Gmail 接入、后台定时器或预约服务。外部行动能否执行，取决于实际集成和已有授权。

## 安装

需要 Python 3.10 以上、Git 和完整子模块。通过下面的命令安装 YAML/PDF 依赖，使用 Chromium 或 Edge 渲染 PDF。验证私有存储还需要 GitHub CLI（`gh`）。

```sh
git clone --recurse-submodules https://github.com/DaizeDong/buy-me-a-car.git
cd buy-me-a-car
python -m pip install -r requirements.txt
git config core.hooksPath .githooks
python tools/install.py
python tools/install.py --apply
python tools/doctor.py
```

安装器先预览，`--apply` 才把全部 16 个技能注册到 `~/.agents/skills`。其他宿主可用 `--target <skill-directory>` 指定目录。遇到已有的无关技能会报告冲突，保留原内容。安装后启动新会话。Claude 插件宿主也可通过 `.claude-plugin/plugin.json` 把仓库作为本地插件加载。

已有克隆缺少子模块时，运行 `git submodule update --init --recursive`。缺少安全守卫应明确失败，不要绕过钩子。

## 配置

在公开工作树之外创建或克隆一个**私有 GitHub 伴生仓库**，建立其中的 `data` 目录，并完成 `gh` 认证。将 `BUY_ME_A_CAR_CONFIG` 设为该伴生仓的根目录：

```powershell
$env:BUY_ME_A_CAR_CONFIG = "<private-companion-root>"
```

POSIX shell 使用 `export BUY_ME_A_CAR_CONFIG="<private-companion-root>"`。然后验证目标目录：

```sh
python tools/runtime_paths.py --write
```

解析器会标明已验证的私有仓和 DATA 路径。公开仓、可见性未知、目录缺失或未纳入版本管理的目标均被拒绝。可选读取可以报告 `UNINITIALIZED`，写入必须先证明存储位置私有。

真实需求、采集材料、报价、邮件状态、PDF、反馈和评测回执，都保存在这个私有 Git 仓库中，沿用其版本管理与备份流程。没有退回公开工作树的备用路径。复制空白模板或填写记录前，先解析目标位置：

```sh
python tools/runtime_paths.py cycles/example/criteria.md --write
```

该路径以私有 DATA 为根。浏览器与抓取命令也应在已验证的私有购车目录执行。

## 60 秒上手

安装并配置私有存储后，说明你想买什么车，以及目前知道的条件即可。下面的启动例句来自[生成的合成路由样例](eval/fixtures/routing_prompts.json)，保留英文原文：

> Help me buy a used compact SUV, ZIP 10001, budget $30000 OTD, cash, within two months.

之后，流程会：

1. **复用你已提供的信息。** 集中补问会影响判断的缺失条件，例如注册地、预算是否为落地总价、座位与载物需求、付款方式和时间安排。不依赖答案的研究继续进行。
2. **比较实际证据。** 检索合适的来源，记录访问情况，按已知 VIN 去重，并检查车辆用途适配和可比成本。
3. **交付购车报告。** 在初步选车阶段准备报告输入，生成比较表、HTML 和 PDF。你不必自己填 JSON 模板，也不必再说一次“写详细点”。
4. **沿用同一套条件继续。** 新报价、检查结果和买家决定更新到同一个私有购车记录中。已获准使用的假设仍标为假设，但不会被当作尚未回答的问题反复确认。

私有研究交付包括：

| 私有 DATA 中的文件 | 帮助你判断什么 |
|---|---|
| `master_comparison.md` | 比较候选车、来源、已知成本和未解决的证据问题。 |
| `buyer_research.html` | 查看需求、检索范围、车型取舍、车源、用途适配、运输、持有风险和推荐。 |
| `buyer_research.pdf` | 阅读或打印经过检查的报告，包含下一步和来源。 |

当前研究渲染器输出中文报告。缺少报价和未知成本会明确列出，不妨碍初次研究报告交付。联系卖方、预约和作出承诺，需要相应授权与可用集成。详见[交付工作流](skills/orchestrator/references/report_delivery.md)。

## 技能一览

共 16 个技能：一个主技能和 15 个专项技能。每个专项技能也可独立使用。

| 阶段 | 技能 |
|---|---|
| 研究与证据 | [orchestrator](#orchestrator), [quote-evidence-collector](#quote-evidence-collector) |
| 成本与方案比较 | [otd-calculator](#otd-calculator), [state-fee-lookup](#state-fee-lookup), [lease-vs-cash-analyzer](#lease-vs-cash-analyzer), [trade-in-valuator](#trade-in-valuator) |
| 车辆核查 | [carfax-pdf-review](#carfax-pdf-review), [cpo-eligibility](#cpo-eligibility), [ev-buyer-helper](#ev-buyer-helper) |
| 回信与报告 | [dealer-reply-drafter](#dealer-reply-drafter), [inbox-triage](#inbox-triage), [dossier-builder](#dossier-builder) |
| 付款与提车 | [payment-method-decider](#payment-method-decider), [insurance-shopper](#insurance-shopper), [ppi-scheduler](#ppi-scheduler), [close-day-checklist](#close-day-checklist) |

## 如何调用每个技能

这些是预期的路由提示，不保证每个宿主模型都能正确识别所有改写。下列例句直接取自[生成的合成路由样例](eval/fixtures/routing_prompts.json)，保留英文原文，不是真实买家记录。

### orchestrator

- **适用场景**: 规划从需求、车源研究、比较到交车的完整购车流程。
- **触发词**: buy me a car / 帮我买车
- **合成例句（英文原文）**: Help me buy a used compact SUV, ZIP 10001, budget $30000 OTD, cash, within two months.
- **输出**: 私有购车记录、市场比较和买方研究 HTML/PDF；后续行动按买家授权推进。
- **完整说明**: [SKILL.md](skills/orchestrator/SKILL.md)

### otd-calculator

- **适用场景**: 由车价计算落地总价，或由目标总价反推车价。
- **触发词**: compute OTD / 算落地价
- **合成例句（英文原文）**: Compute OTD from a $30000 sale, explicit fees, and a confirmed registering state.
- **输出**: 按受支持且证据未过期的注册地、交易类型逐项计算；不支持时明确拒绝。
- **完整说明**: [SKILL.md](skills/otd-calculator/SKILL.md)

### state-fee-lookup

- **适用场景**: 在计算前核实州税、费用和置换抵税规则。
- **触发词**: state fee lookup / 查州税费
- **合成例句（英文原文）**: Look up the current state fee rules and tell me which fields still need official verification.
- **输出**: 带日期的规则证据、适用范围，以及仍需官方核实的字段。
- **完整说明**: [SKILL.md](skills/state-fee-lookup/SKILL.md)

### quote-evidence-collector

- **适用场景**: 把车源页面与书面报价整理成可追溯证据。
- **触发词**: collect quote evidence / 整理报价证据
- **合成例句（英文原文）**: Collect quote evidence from these source links and retain dates and original artifacts.
- **输出**: 私有目录中的来源日期、原始材料和未解决的差异。
- **完整说明**: [SKILL.md](skills/quote-evidence-collector/SKILL.md)

### dealer-reply-drafter

- **适用场景**: 根据已批准的问题和有证据的报价准备经销商回信。
- **触发词**: draft a counter / 起草还价邮件
- **合成例句（英文原文）**: Draft a counter to this dealer email using only my approved offer and documented competing quote.
- **输出**: 包含已授权对外报价的 ASCII 英文草稿，内部最高预算不写入外发内容。
- **完整说明**: [SKILL.md](skills/dealer-reply-drafter/SKILL.md)

### inbox-triage

- **适用场景**: 分类经销商回信并记录处理状态，避免重复执行。
- **触发词**: triage dealer replies / 整理经销商邮件
- **合成例句（英文原文）**: Triage dealer replies, identify out-of-office messages, and record processed message IDs.
- **输出**: 消息分类、稳定标识、游标和操作回执；读取邮箱需要宿主提供可用集成。
- **完整说明**: [SKILL.md](skills/inbox-triage/SKILL.md)

### dossier-builder

- **适用场景**: 生成买方研究报告，或有完整依据的对外经销商提案。
- **触发词**: build a dossier / 生成购车报告
- **合成例句（英文原文）**: Build a private decision dossier from my verified quotes and inspection evidence.
- **输出**: 经过检查的 HTML/PDF。研究允许缺少报价、费用保持未知；对外提案要求完整报价。
- **完整说明**: [SKILL.md](skills/dossier-builder/SKILL.md)

### carfax-pdf-review

- **适用场景**: 审阅车辆历史报告或经销商附带的 PDF。
- **触发词**: review CARFAX / 看车辆历史报告
- **合成例句（英文原文）**: Review this CARFAX PDF for accident entries and gaps in service records.
- **输出**: 带文档依据的事故、产权和保养记录发现，以及需要追问的问题。
- **完整说明**: [SKILL.md](skills/carfax-pdf-review/SKILL.md)

### cpo-eligibility

- **适用场景**: 核实原厂认证二手车资格及保修范围。
- **触发词**: check CPO / 核实原厂认证
- **合成例句（英文原文）**: Check factory CPO eligibility and current coverage for this used vehicle.
- **输出**: 依据当前厂商条款及具体车辆核查认证资格与保修。
- **完整说明**: [SKILL.md](skills/cpo-eligibility/SKILL.md)

### ev-buyer-helper

- **适用场景**: 评估纯电或插混车辆的充电、电池和补贴适用性。
- **触发词**: EV purchase advice / 电动车购车建议
- **合成例句（英文原文）**: Help me check current EV purchase incentives and whether I can charge at home.
- **输出**: 充电和电池检查、带日期的补贴资格，以及未确认的购车条件。
- **完整说明**: [SKILL.md](skills/ev-buyer-helper/SKILL.md)

### lease-vs-cash-analyzer

- **适用场景**: 把书面租赁方案与现金购车放在同一口径比较。
- **触发词**: lease vs cash / 租赁还是现金买
- **合成例句（英文原文）**: Compare lease vs cash purchase using the quoted money factor and residual.
- **输出**: 列明期限、里程、残值和货币因子的可比成本计算。
- **完整说明**: [SKILL.md](skills/lease-vs-cash-analyzer/SKILL.md)

### trade-in-valuator

- **适用场景**: 把置换车辆价值与贷款余额、新车交易条件分开。
- **触发词**: value my trade-in / 估算置换价
- **合成例句（英文原文）**: Value my trade-in separately from its lien payoff and purchase tax treatment.
- **输出**: 估值依据、贷款结清处理，以及经核实适用的抵税影响。
- **完整说明**: [SKILL.md](skills/trade-in-valuator/SKILL.md)

### payment-method-decider

- **适用场景**: 选择适合实际交易、卖方接受的付款方式。
- **触发词**: choose payment method / 选付款方式
- **合成例句（英文原文）**: Choose payment method: cashier check or credit card with a 3 percent surcharge.
- **输出**: 覆盖限额、手续费、时点和收款方核实的付款安排。
- **完整说明**: [SKILL.md](skills/payment-method-decider/SKILL.md)

### insurance-shopper

- **适用场景**: 比较保险并确认提车前的承保状态。
- **触发词**: shop car insurance / 比较车险
- **合成例句（英文原文）**: Shop car insurance and confirm the coverage binder required before collection.
- **输出**: 可比的承保问题与保险凭证清单；实际投保需要授权并由保险方办理。
- **完整说明**: [SKILL.md](skills/insurance-shopper/SKILL.md)

### ppi-scheduler

- **适用场景**: 规划独立第三方购前检查。
- **触发词**: book pre-purchase inspection / 安排购前检查
- **合成例句（英文原文）**: Plan how to book pre-purchase inspection with an independent mechanic.
- **输出**: 维修师选项、检查范围、预约准备，以及已授权操作的回执记录。
- **完整说明**: [SKILL.md](skills/ppi-scheduler/SKILL.md)

### close-day-checklist

- **适用场景**: 签字前检查合同、付款和交车事项。
- **触发词**: close day checklist / 签约交车清单
- **合成例句（英文原文）**: Give me the close day checklist before I sign the purchase contract.
- **输出**: 按购车类型组织的清单、拒绝附加项目的话术、停止条件和交接文件。
- **完整说明**: [SKILL.md](skills/close-day-checklist/SKILL.md)

## 触发路由

请求跨越多个任务时，由主技能协调专项技能。入口取决于你需要的输出。

| 请求 | 入口 |
|---|---|
| 找车并帮我选 | [orchestrator](#orchestrator)，默认包含研究报告交付 |
| 算落地价或核实税费规则 | [otd-calculator](#otd-calculator) 与 [state-fee-lookup](#state-fee-lookup) |
| 审阅车辆历史文件 | [carfax-pdf-review](#carfax-pdf-review) |
| 根据已有证据回复经销商 | [dealer-reply-drafter](#dealer-reply-drafter) |
| 制作研究报告或有依据的经销商提案 | [dossier-builder](#dossier-builder)，按对应文档要求处理 |
| 规划购前检查或准备签约 | [ppi-scheduler](#ppi-scheduler) 或 [close-day-checklist](#close-day-checklist) |

## 示例输出

[九个完整场景](examples/README.md)包含由生成器产出的虚构输入和预期行为，用于说明工具应如何响应，不是实测购车结果。

要查看样本文档，把下面的 `<temporary-directory>` 替换为公开仓库之外的实际系统临时目录：

```sh
python skills/orchestrator/scripts/generate_research_report.py --mode demo --config skills/orchestrator/assets/research_report_config_template.json --output <temporary-directory>/research.html --to-pdf <temporary-directory>/research.pdf
python skills/orchestrator/scripts/generate_dossier.py --mode demo --config skills/orchestrator/assets/dossier_config_template.yaml --output <temporary-directory>/proposal.html --to-pdf <temporary-directory>/proposal.pdf
```

Demo 模式只接受生成器产出的原始合成配置。真实输入使用 [live 模式](skills/dossier-builder/SKILL.md)、私有来源材料，以及对应文档类型要求的证据。买方研究允许没有书面报价；对外经销商提案要求完整书面报价。每次都要逐页检查 PDF，篇幅由证据决定。

下面是使用明确演示费用的 Maryland 普通经销商合成算例：

```sh
python skills/orchestrator/scripts/otd_calculator.py --state MD --sales 30000 --doc 800 --title 200 --reg 120.50 --forward --json
python skills/orchestrator/scripts/otd_calculator.py --list-states
python skills/orchestrator/scripts/check_freshness.py --report-only
```

这些费用只是演示输入，不是个性化报价。支持的计算方案会随证据过期而失效。`--estimate` 只在明确要求时进行通用代数估算，不能证明税费适用于实际注册地。

## 验证

在仓库根目录运行确定性检查：

```sh
python tools/make_fixtures.py --check
python tools/check_repository.py
python skills/orchestrator/scripts/render_state_data.py --check
python -m unittest discover -s eval -p "test_*.py" -v
python eval/test_rubric.py
```

离线检查验证程序规则。另行运行 `python eval/test_rubric.py --llm`，才会通过已安装的 `llmcall` 默认配置执行模型任务并独立复核，输入和回执保存在私有 DATA。失败、不可用和超时都明确报告；结果不确定的行动要先核对，再决定是否重试。

`python eval/run_scenarios.py --llm` 测试生成的阿拉斯加皮卡请求及税费、拖挂能力追问，并由另一个评审复核。范围和结果解读见[评测指南](eval/README.md)。

功能 CI 覆盖 Windows 和 Linux；另有隐私与数据、文风和加载预算检查。离线样例不验证真实发送、税务机关受理或谈判成功。

## 局限

- 州数据表覆盖全部州和 DC，并明确保留未知字段。经核实支持的计算范围更窄，还取决于具体注册地和交易类型。
- 车源、补贴、保修和税费需要当前证据。来源日期与哈希证明采集到了什么，不证明卖方陈述属实或车辆仍在售。
- 搜索和浏览器访问、Gmail、定时运行、发送和预约都取决于宿主能力及授权。本地测试通过不能使缺失的集成变得可用。
- 当前经销商邮件渲染器支持 ASCII 英文。文档语言支持见下表；固定标签不会自动翻译任意输入段落。
- 合成场景不能证明购车节省或真实成交效果。没有固定响应时间、站点覆盖或页数保证。

## 语言

英文版（`README.md`，权威版）与中文版（`README_CN.md`）按相同结构对应。

| 使用位置 | 当前支持 |
|---|---|
| 购车对话与路由提示 | 英文、中文和西班牙文；实际路由取决于宿主模型。 |
| 买方研究渲染器 | 中文。 |
| 经销商提案版式 | 英文、中文和西班牙文固定标签；输入正文需要单独翻译并结合语境检查。 |
| 经销商邮件渲染器 | ASCII 英文。 |

## Roadmap · 贡献 · 许可

后续工作见 [ROADMAP.md](ROADMAP.md)，改动记录见 [CHANGELOG.md](CHANGELOG.md)。贡献请附上可复现的合成用例、适用时的当前来源，以及相关验证结果。提交 [issue](https://github.com/DaizeDong/buy-me-a-car/issues) 或 [pull request](https://github.com/DaizeDong/buy-me-a-car/pulls) 时，不要附带私有购车记录。

采用 [MIT 许可](LICENSE)。
