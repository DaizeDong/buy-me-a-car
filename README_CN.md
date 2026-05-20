# buy-me-a-car

16 个 Claude Code skill，把一个用车周末压缩成 2 小时决策：9 个网站并行抓库存、起草 counter-offer、生成买家级 dossier。

[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-orange?style=flat)](https://docs.anthropic.com/en/docs/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![All 50 States](https://img.shields.io/badge/Tax%20Data-50%E5%B7%9E%20%2B%20DC-green?style=flat)](skills/orchestrator/references/state_fees.md)
[![Roadmap](https://img.shields.io/badge/Roadmap-v0.2.2%20alpha-purple?style=flat)](ROADMAP.md)

[English](README.md) | [中文版](README_CN.md)

---

## 安装

```
/plugin install github:DaizeDong/buy-me-a-car
```

或者手动 clone：

```bash
git clone https://github.com/DaizeDong/buy-me-a-car.git ~/.claude/plugins/buy-me-a-car
```

Skill 在你说 `帮我买车`、`找辆车`、`回复 dealer`、`算 OTD`、`审 CARFAX` 等任意触发短语时自动激活。

---

## 60 秒导览

你说：

```
帮我这周买一辆紧凑型 SUV，预算 25k OTD，里程 60k 以下，ZIP <ZIP> 附近
```

自动跑起来：

1. 确认 9 项核心需求 + buyer-type router（cash / financing / trade-in / EV / pickup）
2. 并行 subagent 抓 **9 个网站**（Carfax、CarMax、Carvana、Cars.com、AutoTrader、Edmunds、TrueCar、CarGurus、Enterprise），按 VIN 去重
3. 通过 Playwright MCP 给 top 30 候选提交 lead form（自动绕 anti-bot）
4. **每 15 分钟 cron** 扫 Gmail，把 dealer 回信分进 4 桶（real / OOO / CRM / spam）
5. 用 **3-anchor 逻辑**起草纯 ASCII counter-offer（dealer 自家价差 + 区域 comp + 已锁竞品 OTD）
6. 抽取 dealer 附件 **CARFAX / 报价 PDF** 的红旗
7. 生成 **8 页 dossier**（HTML → headless-Chrome PDF，中英双模板）
8. 提车日 checklist 含逐字 **F&I 加项硬拒话术**

效果：相比冷启动走入 dealer 大堂，通常省 **$5-9k**。

---

## Skill 一览

总计 16 个：1 个宽触发 orchestrator + 15 个窄触发子 skill。子 skill 都能独立调用，orchestrator 在 9-phase 流程内部路由它们。

| 分组 | Skill |
|---|---|
| **调研 + 候选** | [orchestrator](#orchestrator) · [inbox-triage](#inbox-triage) · [quote-evidence-collector](#quote-evidence-collector) |
| **价格数学 + 文件** | [otd-calculator](#otd-calculator) · [state-fee-lookup](#state-fee-lookup) · [trade-in-valuator](#trade-in-valuator) |
| **谈判** | [dealer-reply-drafter](#dealer-reply-drafter) · [dossier-builder](#dossier-builder) |
| **决策 + 核查** | [lease-vs-cash-analyzer](#lease-vs-cash-analyzer) · [payment-method-decider](#payment-method-decider) · [ev-buyer-helper](#ev-buyer-helper) · [cpo-eligibility](#cpo-eligibility) · [carfax-pdf-review](#carfax-pdf-review) |
| **提车** | [insurance-shopper](#insurance-shopper) · [ppi-scheduler](#ppi-scheduler) · [close-day-checklist](#close-day-checklist) |

---

## 每个 skill 怎么用

每块 4 行：何时用、触发短语、示例输入、产出。

### orchestrator
- **何时用**：你想跑完整 9-phase 流程。
- **触发**：`buy me a car`、`帮我找车`、`买车`、`选车`
- **示例**：`帮我找一辆 2022-2024 款 Outback Premium，里程 60k 以下，离 <ZIP> 50 英里内，预算 32k OTD`
- **产出**：每个 phase 的 artifacts 输出到 `car_buying_<YEAR>/` 工作目录。

### otd-calculator
- **何时用**：sale price → OTD，或目标 OTD 反推最大 sale price。
- **触发**：`compute OTD`、`算 OTD`、`算总价`
- **示例**：`算下 NJ $30k sale + $499 doc 的 OTD`
- **产出**：50 州 + DC 的逐项 OTD 分解（税 / doc / title / reg / DMV）。

### state-fee-lookup
- **何时用**：拉某州 6 字段汇总（税率 / local / doc cap / title / reg / trade credit）。
- **触发**：`doc fee in NJ`、`state 税率`、`trade-in credit`
- **示例**：`看下 TX 的 doc fee 上限和 EV 附加费`
- **产出**：州级汇总 + "Does NOT have" 漏洞清单（用于侦测 dealer 报价里跑错州的费项）。

### cpo-eligibility
- **何时用**：付 CPO 溢价之前核实工厂认证资格 + 嵌入价值。
- **触发**：`is this car CPO`、`Subaru CPO`、`CPO 资格`
- **示例**：`查下 2021 款 Kia Telluride @ 55k 还能不能 CPO`
- **产出**：8 品牌资格矩阵裁定 + 嵌入价值 $1-3k + 假 CPO 红旗。

### carfax-pdf-review
- **何时用**：dealer 发了 CARFAX、保养记录或 F&I 报价 PDF。
- **触发**：`审 CARFAX`、`review PDF`、`F&I 加项`
- **示例**：`审下 dealer 刚发的 CARFAX`
- **产出**：结构化红旗报告（事故、保养缺失附 $ 区间、12 类可挑战 F&I 加项）。

### dealer-reply-drafter
- **何时用**：起一封外发邮件 —— counter / follow-up / walk-away。
- **触发**：`回复 dealer`、`起草 counter`、`对 dealer 报价 counter`
- **示例**：`帮我对这家 Honda dealer 的 $33k OTD 起草 counter，目标 $30.75k`
- **产出**：Gmail draft（保存不发送），~10 行，纯 ASCII，3 ask + 1 anchor + 1 walk-away。

### inbox-triage
- **何时用**：dealer 收件箱堆积，要把真回复和 CRM 噪音分开。
- **触发**：`看下邮箱`、`dealer 回复了吗`、`check inbox`
- **示例**：`triage 今天的 dealer 邮箱`
- **产出**：分桶计数（real / OOO / CRM / spam）+ Gmail 标签 + 交给 dealer-reply-drafter 的清单。

### dossier-builder
- **何时用**：试驾前打印一份买家级市场调研。
- **触发**：`生成 dossier`、`生成 PDF`、`build dossier`
- **示例**：`用中文模板生成 dossier PDF`
- **产出**：8 页 HTML + headless-Chrome PDF（中英），含市场均价 / OTD / CPO 嵌入价值 / dealer 内部 anchor 分析。

### ev-buyer-helper
- **何时用**：买电车 —— 联邦 §30D POS、§25E 二手、§45W 租赁、州级补贴叠加。
- **触发**：`EV 补贴`、`$7,500 POS`、`电车 credit`
- **示例**：`Ioniq 5 SEL 在 NJ 能不能拿 $7,500 POS`
- **产出**：补贴后净价 + dealer IRS 注册核实 + NACS/CCS1 转接头指引。

### payment-method-decider
- **何时用**：选 close-day 工具 —— cashier's check / 信用卡 / wire / lease cap reduction。
- **触发**：`支付方式`、`买车用刷卡还是支票`、`Visa for $30k car`
- **示例**：`$30k 是刷我 3% 返现 Visa 还是 cashier's check`
- **产出**：支付方式建议 + 信用卡返现 vs 刷卡手续费的盈亏平衡数学。

### lease-vs-cash-analyzer
- **何时用**：dealer 给了 lease 报价 —— 核实 MF / residual / acquisition / disposition。
- **触发**：`lease 还是 cash`、`money factor markup`、`租还是买`
- **示例**：`这台 Ioniq 5 SEL $575/mo 的 lease 报价靠谱吗`
- **产出**：月供拆解 + 按持有年限 LEASE / BUY / 持平的裁定。

### trade-in-valuator
- **何时用**：要置换 —— 4-anchor 估值 + lien 还款流程。
- **触发**：`评估置换车`、`valuate my trade`、`trade-in tax credit`
- **示例**：`我 2017 款 Civic 在 NJ 当 trade 值多少`
- **产出**：4-anchor 表（KBB Instant / Trade-in / Private / 批发）+ 置换 vs 单独卖的决策。

### quote-evidence-collector
- **何时用**：从 XHS / Reddit / FB 收 REAL dealer 报价截图，作为谈判 anchor。
- **触发**：`找证据图`、`搜集报价截图`、`find dealer evidence`
- **示例**：`找 <你所在州> 2024 Outback Premium 的 XHS 报价`
- **产出**：REAL 标记的压缩 `_FINAL_*.jpg`（1300px，100-300 KB），可直接手动 paperclip。

### insurance-shopper
- **何时用**：提车前上车险 —— 新司机、cash buyer、跨州移居。
- **触发**：`上保`、`保险报价`、`car insurance quote`、`new driver insurance`
- **示例**：`帮我新司机在 <你所在州> 上一辆 SUV 的车险`
- **产出**：NJM / Geico / Progressive 三家 6-month 报价对比 + 推荐 coverage + bind 步骤。

### ppi-scheduler
- **何时用**：要约 PPI 检车 —— 按地区匹配 mobile PPI 服务商。
- **触发**：`约 PPI`、`提车前检车`、`book PPI`
- **示例**：`明天约个 mobile PPI，给一家本地 dealer 的 2022 Outback`
- **产出**：预约（含 ID + 取消时限）+ 检后 PROCEED / COUNTER / WALK 决策矩阵。

### close-day-checklist
- **何时用**：明天要提车 —— 按 buyer 类型的 checklist + F&I 硬拒话术。
- **触发**：`提车清单`、`ready to close`、`F&I 加项硬拒`
- **示例**：`给我明天 cash + 置换买家的提车清单`
- **产出**：到店前 / 现场 / 离店后 checklist + 逐字 F&I 拒绝话术。

---

## 五条铁律

不可妥协。每条都源自某次具体丢钱事故：

1. **只谈 OTD** —— 绝不分开 sale price / tax / fee 单独谈，只盯 out-the-door 总价。
2. **纯 ASCII 邮件** —— 禁用 markdown、em-dash、智能引号。Dealer 客户端会把它们当字面字符显示。
3. **3-anchor 反砍** —— 每封回信必含 (a) dealer 自家内部价差、(b) 区域市场 comp、(c) 你已锁的竞品 OTD。
4. **15 分钟 cron 扫信** —— Gmail 由 cron 自动轮询，绝不让人工反复刷。
5. **walk-away 阈值** —— 超预算或对方拒绝合理还价 → 礼貌走人。维持选项胜过抢一单。

完整规则见 [`SKILL.md`](skills/orchestrator/SKILL.md)。

---

## 触发冲突路由

一句话能匹配多个 skill 时，**最窄、最具体**的触发胜出：

| 一句话 | 激活 | 不激活 |
|---|---|---|
| "帮我买车" / "help me buy a car" | `orchestrator` | 子 skill |
| "回复 dealer" / "draft reply to dealer" | `dealer-reply-drafter` | `orchestrator` |
| "算 OTD" / "compute OTD" | `otd-calculator` | `orchestrator` |
| "NJ 州税" / "doc fee in NJ" | `state-fee-lookup` | `otd-calculator` |
| "租还是买" / "lease or buy" | `lease-vs-cash-analyzer` | `payment-method-decider` |
| "刷卡买车" / "Visa for $30k car" | `payment-method-decider` | `lease-vs-cash-analyzer` |
| "找证据图" / "find quote screenshots" | `quote-evidence-collector` | `orchestrator` |
| "EV 补贴" / "$7,500 EV credit" | `ev-buyer-helper` | `payment-method-decider` |
| "约 PPI" / "book PPI" | `ppi-scheduler` | `orchestrator` |
| "审 CARFAX" / "review CARFAX" | `carfax-pdf-review` | `orchestrator` |
| "CPO 资格" / "is this car CPO" | `cpo-eligibility` | `carfax-pdf-review` |
| "生成 dossier" / "build dossier PDF" | `dossier-builder` | `orchestrator` |
| "看下邮箱" / "check inbox" | `inbox-triage` | `orchestrator` |
| "评估置换" / "valuate trade-in" | `trade-in-valuator` | `otd-calculator` |
| "上保" / "set up insurance" | `insurance-shopper` | `close-day-checklist` |
| "提车清单" / "ready to close" | `close-day-checklist` | `orchestrator` |

歧义时显式点名 skill：`用 dealer-reply-drafter 起草这封`。不确定调哪个？喊 `orchestrator`，它会在内部路由。

---

## 输出示例

![站点能力矩阵 + 候选去重](./examples/market_cn.png)

Phase 2 自动生成的两张表：上半是 9 个站点的能力矩阵 + 关键差异 + 推荐顺序，下半是按 VIN 去重的候选清单含 Deal Tag。两张都是 Markdown 表格 → Claude 渲染。

---

## 自检

安装后跑这几条，验证骨架是否齐全：

```bash
ls skills/   # 应看到 15 个目录
python skills/orchestrator/scripts/otd_calculator.py --state NJ --sale-price 25000
python skills/orchestrator/scripts/generate_dossier.py \
  --config skills/orchestrator/assets/dossier_config_template.yaml \
  --output /tmp/test.html
```

任一步失败 → 开 issue 贴 traceback。多半是 Python 依赖（PyYAML / Jinja2）或 Chrome headless 路径问题。

---

## 局限

- **单作者 alpha** —— 工作流基于一次真实购车 + 5 场情景压测，未经多市场对抗验证。
- **数据会漂移** —— 州费、CPO 条款、EV 补贴最后核对 2026-05-18，半年内可能有州法修订。
- **anti-bot 不稳定** —— CarGurus / Cars.com / AutoTrader / Edmunds / TrueCar 依赖 Playwright MCP，网站改版可能让 subagent 整组失败。
- **非税务 / 法律 / 财务建议** —— 所有计算仅供谈判参考，过户、贷款、保险请咨询持牌专业人士。

---

## Roadmap · 贡献 · License

[ROADMAP.md](ROADMAP.md) 记录 v0.3.0 / v1.0.0 计划（多作者数据、对抗性 dealer 测试、剩余州补全、更多品牌 CPO）。挑一个 → 开 issue → PR。

MIT —— Fork it, ship it, save someone money.

_last_verified: 2026-05-18_
