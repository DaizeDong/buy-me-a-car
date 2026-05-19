# buy-me-a-car 🚗💸

[English](README.md) | [中文版](README_CN.md)

> **Alpha 版本 v0.2.0** —— 这是一位作者的购车 playbook，背后有 5 场情景压测 + 约 80 条根因归因的迭代。尚未经过生产级验证；子 skill 内容（州费、CPO 条款、EV 补贴）最后核对日期 2026-05-18，可能随时漂移。真实购车前请自行核对。不构成税务、法律或财务建议。

> 🛒 **让 Claude Code 帮你买车。** 9 个网站平行抓库存、群发 30+ dealer 邮件、cron 监控收件箱、起草砍价回复、生成专业 OTD 提案 PDF —— 全自动。
>
> 🪶 **零依赖，零锁定。** 纯 Markdown skill + Python 脚本 + HTML 模板。换成 Codex、Cursor、Trae、自己的 agent 一样能跑。Fork 它、改它、为你的市场适配它。
>
> _💡 这不是平台，是工作流。买完你的车，把它带去下一个朋友的购车任务。🌱_

[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-orange?style=flat)](https://docs.anthropic.com/en/docs/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![All 50 States](https://img.shields.io/badge/Tax%20Data-50%E5%B7%9E%20%2B%20DC-green?style=flat)](skills/orchestrator/references/state_fees.md)
[![Roadmap](https://img.shields.io/badge/Roadmap-v0.2.0%20alpha-purple?style=flat)](ROADMAP.md)

---

## 🎯 干什么（三种模式，同一个 skill）

**Quick mode** —— 一句话启动全流程：

```
帮我这周买一辆紧凑型 SUV，预算 25k OTD，里程 60k 以下，ZIP <ZIP> 附近
```

Claude 自动 confirm 需求 → 9 个 subagent 并行抓 Carfax / CarMax / Carvana / Cars.com / AutoTrader / Edmunds / TrueCar / CarGurus / Enterprise → 汇总 top 30 候选 → 群发 lead form → 设 cron 每 15 分钟扫 Gmail。

**砍价 mode** —— Dealer 给了 OTD？锚定 + 反击：

```
dealer 报 32,200 OTD，目标 30k，帮我起草反砍信
```

Claude 用 3 种 anchor 起草纯 ASCII 回信：(1) Dealer 自家库存内部价差、(2) 区域市场 comp（AutoTrader / KBB / CarGurus）、(3) 已锁的竞品 OTD。

**Dossier mode** —— 试驾前打印一份专业市场调研：

```bash
cp assets/dossier_config_template.yaml my_offer.yaml
$EDITOR my_offer.yaml   # 填买方 + 目标车 + 竞品 OTD + 数据来源

python scripts/generate_dossier.py \
  --config my_offer.yaml \
  --output my_offer.html \
  --to-pdf my_offer.pdf
```

8 页 PDF（中英双模板），含市场均价、配置对比、CPO 嵌入价值、内部价差分析、报价结构、交易条件 —— 买方水准、可直接发给 dealer。

---

## 📊 覆盖范围

- **15 个 skill**：1 个 `orchestrator`（宽触发、9-phase 全流程）+ 14 个窄触发子 skill。
- **22 个州的 fee 细节** + 全 **50 州 + DC** 销售税兜底（剩余州走通用税率公式）。
- **8 个品牌的 CPO 计划**：Subaru / Honda / Toyota / Mazda / Hyundai / Kia / Nissan / Ford —— 嵌入价值、保修长度、check 清单。
- **3 个独立 PDF 审核 checklist**：CARFAX、dealer 报价、service record。
- **中英双模板** dossier（80+ YAML placeholder，HTML → Chrome headless → PDF）。

---

## 🖼️ 例图：站点能力矩阵 + 候选去重

下图是 Phase 2 多站抓库存后 Claude 自动生成的两张表：上半是 9 个站点（Carfax / CarGurus / Carvana / Cars.com / AutoTrader / Edmunds / TrueCar / CarMax / Enterprise / Hertz / EchoPark）的容量 + 关键差异 + 推荐顺序，下半是按 VIN 去重后的候选清单含 Deal Tag。两张表都是 Markdown 表格 → Claude 渲染。

![站点能力矩阵 + 候选去重](examples/market.png)

---

## 🚀 快速开始

```
/plugin install github:DaizeDong/buy-me-a-car
```

或手动 clone：

```bash
git clone https://github.com/DaizeDong/buy-me-a-car.git ~/.claude/plugins/buy-me-a-car
```

Skill 在你说 "帮我买车 / 找辆车 / help me buy a car / research used cars" 等任意触发短语时自动激活。

---

## 触发冲突（哪个子 skill 会激活？）

当一句话能匹配多个 skill 时，**最窄、最具体**的触发胜出。常见情况：

| EN | 中文 | Activates | Not |
|---|---|---|---|
| "help me buy a car" | 帮我买车 | `orchestrator`（全流程） | sub-skills |
| "draft reply to dealer" | 回复 dealer | `dealer-reply-drafter` | orchestrator |
| "compute OTD" | 算总价 | `otd-calculator` | orchestrator |
| "doc fee in NJ" | NJ 州税 | `state-fee-lookup` | otd-calculator |
| "lease or buy" | lease 还是 cash | `lease-vs-cash-analyzer` | payment-method-decider |
| "Visa for $30k car" | 刷卡买车 | `payment-method-decider` | lease-vs-cash-analyzer |
| "find quote screenshots" | 找证据图 | `quote-evidence-collector` | orchestrator |
| "$7,500 EV credit" | EV 补贴 | `ev-buyer-helper` | payment-method-decider |
| "book PPI" | 预约检车 | `ppi-scheduler` | orchestrator |
| "review this CARFAX" | 看 CARFAX | `carfax-pdf-review` | orchestrator |
| "is this car CPO" | Honda Certified | `cpo-eligibility` | carfax-pdf-review |
| "build dossier PDF" | 生成 PDF | `dossier-builder` | orchestrator |
| "check inbox" | 看下邮箱 | `inbox-triage` | orchestrator |
| "valuate trade-in" | 评估置换 | `trade-in-valuator` | otd-calculator |
| "ready to close" | 提车清单 | `close-day-checklist` | orchestrator |

如果歧义，用户可显式点名 skill：例如 "用 `dealer-reply-drafter` 起草这封"。

不确定调哪个？直接喊 `orchestrator` —— 它会在内部路由。

---

## ⚖️ 关键铁律

工作流里若干**不可妥协**的纪律，违反通常意味着钱包失血：

- **OTD 一刀切**：只谈 out-the-door 总价，绝不拆开 sale price / tax / fee 让 dealer 牵着鼻子走。
- **纯 ASCII 邮件**：所有 dealer 回信禁用 markdown、em-dash、智能引号，统一 7-bit ASCII，避免被 Outlook / Gmail 渲染破坏。
- **3-anchor 砍价**：每次反砍必须给出 dealer 自家价差 + 区域 comp + 已锁竞品 OTD，三者缺一不可。
- **15-min cron 扫信**：收件箱由 cron 轮询，跳过 auto-responder，重复 thread 去重，绝不让人工反复刷。
- **walk-away 阈值**：超过预算或对方拒绝合理还价，直接礼貌走人；维持选项胜过抢一单。

完整规则见 [`SKILL.md`](skills/orchestrator/SKILL.md)。

---

## ✅ 自检

安装后跑这几条，验证骨架是否齐全：

```bash
ls skills/   # 应看到 15 个目录
python scripts/otd_calculator.py --state NJ --sale-price 25000   # 应输出 OTD 数字
python scripts/generate_dossier.py --config assets/dossier_config_template.yaml --output /tmp/test.html
```

任一步失败 → 开 issue 贴 traceback；多半是 Python 依赖（PyYAML / Jinja2）或 Chrome headless 路径。

---

## ⚠️ 局限

- **单作者 alpha**：所有决策建议基于一次购车流程 + 5 场情景压测，**未经多市场对抗验证**。
- **数据会漂移**：州费、CPO 条款、EV 补贴最后核对 **2026-05-18**；半年内大概率有州法修订。
- **anti-bot 不稳定**：CarGurus / Cars.com / AutoTrader / Edmunds / TrueCar 依赖 Playwright MCP，网站改版可能让 subagent 整组失败。
- **非税务 / 法律建议**：所有计算仅供谈判参考；过户、贷款、保险请咨询持牌专业人士。

---

## 🤝 贡献 & License

[ROADMAP.md](ROADMAP.md) 记录 v0.2.0 已发版本与 v0.3.0 / v1.0.0 计划（多作者数据、对抗性 dealer 测试、剩余州补全、更多品牌 CPO）。挑一个 → 开 issue → PR。

MIT — fork it, ship it, save someone money.

_last_verified: 2026-05-18_
