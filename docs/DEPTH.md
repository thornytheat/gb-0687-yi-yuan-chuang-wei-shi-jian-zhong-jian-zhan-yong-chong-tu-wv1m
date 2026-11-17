# 深度登记 医院床位事件重建与占用冲突

- 规模：中型
- 核心规则：按患者事件时间构造半开占床区间，转床同刻先出后入，缺失出院保留开放段，重叠转移隔离
- 使用者与工作流：医院运营数据员；合并入出转床事件，计算病区每日占床时长并定位双占

## 功能模块

| 模块 | 使用者动作 | 入口 | 核心文件 | 测试 |
|---|---|---|---|---|
| M1 事件接收 | 接收带行号事件 | `/api/m1` | `app/modules/m1_receive/rules.py` `app/modules/m1_receive/service.py` | `tests/test_m1_receive.py` |
| M2 病区映射 | 匹配床位病区与时区 | `/api/m2` | `app/modules/m2_mapping/rules.py` `app/modules/m2_mapping/service.py` | `tests/test_m2_mapping.py` |
| M3 住院分段 | 回放入出转院事件 | `/api/m3` | `app/modules/m3_episodes/rules.py` `app/modules/m3_episodes/service.py` | `tests/test_m3_episodes.py` |
| M4 转床裁决 | 定位床位双占交集 | `/api/m4` | `app/modules/m4_conflicts/rules.py` `app/modules/m4_conflicts/service.py` | `tests/test_m4_conflicts.py` |
| M5 占床日历 | 按当地午夜切分占床 | `/api/m5` | `app/modules/m5_calendar/rules.py` `app/modules/m5_calendar/service.py` | `tests/test_m5_calendar.py` |
| M6 病区对账 | 核对分段与日历分钟 | `/api/m6` | `app/modules/m6_reconcile/rules.py` `app/modules/m6_reconcile/service.py` | `tests/test_m6_reconcile.py` |
| M7 补传重算 | 标记迟到并复核补传 | `/api/m7` | `app/modules/m7_replay/rules.py` `app/modules/m7_replay/service.py` | `tests/test_m7_replay.py` |

## 陷阱登记

| TRAP | 现象 | 朴素实现会怎样 | 本项目处理 | 处理位置 | 测试 |
|---|---|---|---|---|---|
| TRAP-02 | BOM | 覆盖或重复计数 | 显式检查保留证据 | `app/modules/m1_receive/rules.py` | `tests/test_m1_receive.py::test_bom_header` |
| TRAP-05 | 短行 | 覆盖或重复计数 | 显式检查保留证据 | `app/modules/m1_receive/rules.py` | `tests/test_m1_receive.py::test_real_bad_width` |
| TRAP-08 | 患者号前导零 | 覆盖或重复计数 | 显式检查保留证据 | `app/modules/m1_receive/rules.py` | `tests/test_m1_receive.py::test_key_preserved` |
| TRAP-11 | 偏移混用 | 覆盖或重复计数 | 显式检查保留证据 | `app/modules/m2_mapping/rules.py` | `tests/test_m2_mapping.py::test_timezone_equivalence` |
| TRAP-13 | 迟到补传 | 覆盖或重复计数 | 显式检查保留证据 | `app/modules/m7_replay/rules.py` | `tests/test_m7_replay.py::test_late_replayed` |
| TRAP-14 | 同版事件矛盾 | 覆盖或重复计数 | 显式检查保留证据 | `app/modules/m3_episodes/rules.py` | `tests/test_m3_episodes.py::test_same_version_conflict` |
| TRAP-23 | 相接转床端点 | 覆盖或重复计数 | 显式检查保留证据 | `app/modules/m4_conflicts/rules.py` | `tests/test_m4_conflicts.py::test_touching_not_overlap` |
| TRAP-26 | 旧版复核 | 覆盖或重复计数 | 显式检查保留证据 | `app/store.py` | `tests/test_m7_replay.py::test_optimistic_lock` |

## 对账规则

输入逻辑行数 = 采信行数 + 隔离行数；空行单列。每条重复、冲突、超限、缺失均保留原始行号与原因码。计算阶段的输出数量可聚合，原始采信records始终保留，业务平衡另按模块给出的重量、时长、电量或座席数量核对。
相同输入摘要、规则版本、参数产生相同批次ID。运行原子插入SQLite；复核使用整数版本乐观锁。

## 已知不覆盖

床位目录固定为两病区各四床，时间使用明确偏移。未做医嘱、收费与患者隐私字段。双占保留证据待人工复核，不自行删除患者。
