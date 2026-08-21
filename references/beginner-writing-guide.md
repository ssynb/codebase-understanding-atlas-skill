# Beginner-Readable Chinese Writing Guide

Use this guide when the atlas language is Chinese. The goal is not literary translation; it is to let a reader with little repository knowledge understand what happens and why.

## Keep code names, translate meaning

Good:

> `SessionStore（会话存储）`读取已经保存的对话事件，按时间顺序还原用户看到的历史。

Bad:

> SessionStore handles session persistence and event projection.

The identifier remains searchable. The action and result are Chinese.

## Browser-row description

Use 1–3 short sentences. State the narrow file action, not the entire parent module.

Production code:

> 接收已经通过权限检查的任务，写入待执行队列，并返回可查询的任务编号。

Configuration:

> 规定浏览器测试使用的入口、超时时间和运行环境；测试命令启动时读取它。

Test:

> 验证重复提交同一请求时只创建一条任务记录，防止重试造成重复执行。

Documentation:

> 向插件作者说明注册工具所需的字段、调用顺序和失败处理规则。

Asset:

> 登录空状态使用的插图，由登录页面在用户尚未绑定账号时显示。

Avoid:

- “处理相关逻辑”
- “提供工具函数”
- “负责对应模块能力”
- a translated filename with no action or result
- a Chinese prefix followed by a copied English paragraph

## Structured purpose

`summary` answers why the file exists:

> 把外部请求转换成领域命令，避免路由层直接修改业务状态。

`when` answers the exact usage moment:

> 用户点击提交后，HTTP 路由完成身份校验并调用这个文件。

`effect` answers input and result:

> 接收已认证账号和表单字段；成功时返回新记录编号，失败时返回稳定错误类别。

Do not repeat the same sentence three times with different prefixes.

## Main functions, types, and variables

First identify the syntactic kind from source. Then explain behavior.

Function:

> `reserveSlot`（函数）— 在启动外部任务前原子占用一个并发名额；没有空位时返回可重试错误。

Type:

> `TaskView`（类型）— 接口返回给调用方的任务摘要，只包含状态、创建时间和可公开结果。

Variable:

> `retryableCodes`（变量）— 保存允许自动重试的错误码集合，避免把权限拒绝误当成临时故障。

Do not guess private helper semantics from a short name alone. If no declaration is reliable, leave `symbolDetails` empty; the drawer will explain that low-confidence helpers were omitted. If declarations were confidently detected, explain at least the main one.

## Directly touched tables

A table entry has four facts:

- `name` — exact schema identifier
- `display` — short Chinese fact name
- `access` — 读取、写入、读写、定义或迁移
- `purpose` — why this file touches it

Example:

```json
{
  "name": "task_run",
  "display": "任务运行记录",
  "access": "读写",
  "purpose": "创建任务时冻结输入，任务结束后写回状态和最终结果。"
}
```

Only include direct SQL, ORM, generated query, migration, or explicit storage contract evidence. A parent module using a table does not mean every child file touches it.

## Routes and tests

Keep route methods, URL paths, and exact test identifiers searchable, but explain their meaning in Chinese.

Route:

> `POST /tasks` — 用户提交新任务；成功后返回任务编号和初始状态。

Test:

> `rejects_duplicate_request` — 验证客户端重试同一请求时不会创建第二条任务记录。

Do not show an unexplained wall of English test names.

## Source design notes

Translate or summarize useful source comments into concise Chinese:

Source meaning:

> The lock must cover both duplicate checks because retries can race.

Visible note:

> 两个重复检查必须放在同一把锁内，否则并发重试可能同时通过并创建两条记录。

Do not display raw English comments. Do not turn ordinary line comments into grand architecture claims. Keep `designNotes` empty when the source contains no additional design rationale.

## Capability roles

Explain the file-specific step:

Good:

> 在“恢复会话”中读取指定会话的事件，并返回下一页游标；它不负责保存新消息。

Bad:

> 支持恢复会话功能。

Use only these Chinese relation values:

- 直接参与
- 支撑
- 验证
- 说明
- 不直接参与

## Concision check

Before accepting prose, remove:

- repeated parent-module introductions
- lists already shown in another section
- empty phrases such as “主要用于”“相关能力”“对应逻辑”
- untranslated prose
- implementation trivia that does not change a reader's understanding

A beginner-friendly explanation is concrete, not long. Prefer one precise sentence over five vague sentences.
