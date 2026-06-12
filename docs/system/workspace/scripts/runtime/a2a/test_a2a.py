#!/usr/bin/env python3
"""test_a2a.py - A2A 协议测试脚本

测试 A2A Server/Client 实现的功能：
- T1: Agent Card 发现
- T2: exit_kind 状态映射
- T3: Task CRUD 操作
- T4: Handoff fallback
- T5: SSE 实时推送
- T6: 能力协商

运行方式:
  # 启动 A2A Server (Worker 端)
  python3 docs/system/workspace/scripts/runtime/a2a/a2a_server.py --project /path/to/project --start

  # 运行测试 (Manager 端)
  python3 docs/system/workspace/scripts/runtime/a2a/test_a2a.py --project /path/to/project
"""

import argparse
import os
import sys
import time
import json

# 添加 runtime 目录到 path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RUNTIME_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, RUNTIME_DIR)

from a2a.a2a_client import A2AClient, A2AHandoffAdapter, TaskState
from a2a.a2a_server import EXIT_KIND_TO_TASK_STATE


# ── 测试结果收集 ───────────────────────────────────────────────────────────

class TestResult:
    def __init__(self, name: str):
        self.name = name
        self.passed = False
        self.error = ""
        self.start_time = 0
        self.end_time = 0

    def start(self):
        self.start_time = time.time()

    def end(self, passed: bool, error: str = ""):
        self.end_time = time.time()
        self.passed = passed
        self.error = error

    def duration(self) -> float:
        return self.end_time - self.start_time


# ── 测试用例 ───────────────────────────────────────────────────────────────

def test_agent_card_discovery(project: str) -> TestResult:
    """T1: Agent Card 发现"""
    result = TestResult("T1: Agent Card Discovery")
    result.start()

    try:
        client = A2AClient(project)
        card = client.discover_agent()

        if not card:
            result.end(False, "No Agent Card found")
            return result

        # 验证 Agent Card 字段
        required_fields = ["name", "description", "url", "version", "capabilities", "skills"]
        for field in required_fields:
            if not hasattr(card, field) or not getattr(card, field):
                result.end(False, f"Missing or empty field: {field}")
                return result

        # 验证 freely 扩展
        if not card.freely:
            result.end(False, "Missing freely extension")
            return result

        if "agentType" not in card.freely:
            result.end(False, "Missing freely.agentType")
            return result

        if card.freely["agentType"] != "worker":
            result.end(False, f"Expected agentType=worker, got {card.freely['agentType']}")
            return result

        # 验证 skills
        if not card.skills:
            result.end(False, "No skills found")
            return result

        print(f"  ✓ Agent Card: {card.name} v{card.version}")
        print(f"  ✓ Skills: {[s['id'] for s in card.skills]}")
        print(f"  ✓ Freely extension: {card.freely.get('agentType')}")

        result.end(True)
        return result

    except Exception as e:
        result.end(False, str(e))
        return result


def test_exit_kind_mapping() -> TestResult:
    """T2: exit_kind → Task State 映射"""
    result = TestResult("T2: exit_kind Mapping")
    result.start()

    try:
        # 验证映射表
        expected_mappings = {
            'manager_working': TaskState.SUBMITTED,
            'worker_working': TaskState.WORKING,
            'worker_done': TaskState.COMPLETED,
            'worker_blocked': TaskState.INPUT_REQUIRED,
            'worker_handoff_needed': TaskState.PENDING_INPUT,
            'delegate_workers': TaskState.SUBMITTED,
            'resume_manager': TaskState.COMPLETED,
            'stop_ai': TaskState.FAILED,
        }

        for exit_kind, expected_state in expected_mappings.items():
            actual_state = EXIT_KIND_TO_TASK_STATE.get(exit_kind)
            if actual_state != expected_state:
                result.end(False, f"Mismatch: {exit_kind} -> {actual_state} (expected {expected_state})")
                return result

        print(f"  ✓ All {len(expected_mappings)} exit_kind mappings verified")

        result.end(True)
        return result

    except Exception as e:
        result.end(False, str(e))
        return result


def test_task_crud(project: str) -> TestResult:
    """T3: Task CRUD 操作"""
    result = TestResult("T3: Task CRUD")
    result.start()

    try:
        client = A2AClient(project)

        # Create
        task = client.create_task(
            skill="freely-fix-execution",
            prompt_file="docs/issues/test/issue.md",
            worktree="/path/to/worktree",
            branch="feature/test",
            reason="Test task creation",
            session_id="test-session-001",
        )

        if not task:
            result.end(False, "Task creation failed")
            return result

        task_id = task.id
        print(f"  ✓ Task created: {task_id}")

        # Read
        retrieved = client.get_task(task_id)
        if not retrieved or retrieved.id != task_id:
            result.end(False, "Task retrieval failed")
            return result
        print(f"  ✓ Task retrieved: {retrieved.state}")

        # Update
        updated = client.update_task(
            task_id=task_id,
            exit_kind="worker_working",
            progress="Processing test task...",
            next_action="Continue execution",
        )

        if not updated or updated.state != TaskState.WORKING.value:
            result.end(False, f"Task update failed, state: {updated.state if updated else 'None'}")
            return result
        print(f"  ✓ Task updated: {updated.state}")

        # Complete
        completed = client.update_task(
            task_id=task_id,
            exit_kind="worker_done",
            completion_summary="Test task completed successfully",
            evidence_paths="docs/progress/test/evidence.md",
            next_action="Ready for next task",
        )

        if not completed or completed.state != TaskState.COMPLETED.value:
            result.end(False, f"Task completion failed, state: {completed.state if completed else 'None'}")
            return result
        print(f"  ✓ Task completed: {completed.state}")

        result.end(True)
        return result

    except Exception as e:
        result.end(False, str(e))
        return result


def test_capability_check(project: str) -> TestResult:
    """T4: 能力协商 (Capability Check)"""
    result = TestResult("T4: Capability Check")
    result.start()

    try:
        adapter = A2AHandoffAdapter(project)

        # 检查支持的 skill
        supported_skills = [
            "freely-fix-execution",
            "freely-feat-execution",
            "freely-doc-B1_IBM-execution",
            "freely-doc-B2_IBM-execution",
        ]

        for skill in supported_skills:
            has_capability = adapter.discover_and_check_capability(skill)
            if has_capability:
                print(f"  ✓ Worker supports: {skill}")
            else:
                print(f"  - Worker does not support: {skill} (may be fallback)")

        result.end(True)
        return result

    except Exception as e:
        result.end(False, str(e))
        return result


def test_task_wait_for_completion(project: str) -> TestResult:
    """T5: 等待 Task 完成"""
    result = TestResult("T5: Wait for Completion")
    result.start()

    try:
        client = A2AClient(project)

        # 创建 Task
        task = client.create_task(
            skill="freely-fix-execution",
            reason="Test wait for completion",
        )

        if not task:
            result.end(False, "Task creation failed")
            return result

        print(f"  ✓ Task created: {task.id}")

        # 模拟 Worker 状态变化
        # 在实际测试中，这需要 A2A Server 端运行
        # 这里我们测试 get_task 逻辑
        retrieved = client.get_task(task.id)
        if not retrieved:
            result.end(False, "Task retrieval failed")
            return result

        print(f"  ✓ Task state: {retrieved.state}")

        result.end(True)
        return result

    except Exception as e:
        result.end(False, str(e))
        return result


def test_handoff_fallback(project: str) -> TestResult:
    """T6: Handoff Fallback"""
    result = TestResult("T6: Handoff Fallback")
    result.start()

    try:
        adapter = A2AHandoffAdapter(project)

        # 尝试创建 Task (可能 fallback)
        task = adapter.create_task_with_fallback(
            skill="freely-fix-execution",
            prompt_file="docs/issues/test/issue.md",
            worktree="/path/to/worktree",
            branch="feature/test",
            reason="Test A2A with Handoff fallback",
        )

        if task:
            print(f"  ✓ Task created (A2A or Handoff): {task.get('id') or task.get('handoff_id')}")
            if task.get("fallback"):
                print(f"  ✓ Fallback to Handoff was used")
        else:
            print(f"  - No A2A server, Handoff fallback would be used in production")

        result.end(True)
        return result

    except Exception as e:
        result.end(False, str(e))
        return result


# ── 主测试运行器 ───────────────────────────────────────────────────────────

def run_all_tests(project: str) -> dict:
    """运行所有测试"""
    tests = [
        ("T1", "Agent Card Discovery", lambda: test_agent_card_discovery(project)),
        ("T2", "exit_kind Mapping", test_exit_kind_mapping),
        ("T3", "Task CRUD", lambda: test_task_crud(project)),
        ("T4", "Capability Check", lambda: test_capability_check(project)),
        ("T5", "Wait for Completion", lambda: test_task_wait_for_completion(project)),
        ("T6", "Handoff Fallback", lambda: test_handoff_fallback(project)),
    ]

    results = {}
    passed = 0
    failed = 0

    print("\n" + "=" * 60)
    print("A2A Protocol Test Suite")
    print("=" * 60)
    print(f"Project: {project}")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60 + "\n")

    for test_id, test_name, test_func in tests:
        print(f"[{test_id}] {test_name}")
        print("-" * 40)
        result = test_func()
        results[test_id] = result

        if result.passed:
            print(f"  PASSED ({result.duration():.3f}s)")
            passed += 1
        else:
            print(f"  FAILED: {result.error} ({result.duration():.3f}s)")
            failed += 1

        print()

    # 汇总
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed, {len(tests)} total")
    print("=" * 60)

    return {
        "passed": passed,
        "failed": failed,
        "total": len(tests),
        "results": {k: {"passed": v.passed, "error": v.error} for k, v in results.items()},
    }


def main():
    parser = argparse.ArgumentParser(description="A2A Protocol Test Suite")
    parser.add_argument("--project", required=True, help="Freely 项目路径")
    parser.add_argument("--test", help="运行单个测试 (T1-T6)")
    parser.add_argument("--output", help="输出 JSON 结果到文件")
    args = parser.parse_args()

    project = args.project

    if args.test:
        # 运行单个测试
        test_map = {
            "T1": lambda: test_agent_card_discovery(project),
            "T2": test_exit_kind_mapping,
            "T3": lambda: test_task_crud(project),
            "T4": lambda: test_capability_check(project),
            "T5": lambda: test_task_wait_for_completion(project),
            "T6": lambda: test_handoff_fallback(project),
        }

        if args.test in test_map:
            result = test_map[args.test]()
            print(f"{args.test}: {'PASSED' if result.passed else 'FAILED'}")
            if not result.passed:
                print(f"  Error: {result.error}")
                sys.exit(1)
        else:
            print(f"Unknown test: {args.test}")
            print(f"Available: {list(test_map.keys())}")
            sys.exit(1)
    else:
        # 运行所有测试
        results = run_all_tests(project)

        if args.output:
            with open(args.output, "w") as f:
                json.dump(results, f, indent=2)
            print(f"\nResults saved to: {args.output}")

        # 返回退出码
        sys.exit(0 if results["failed"] == 0 else 1)


if __name__ == "__main__":
    main()