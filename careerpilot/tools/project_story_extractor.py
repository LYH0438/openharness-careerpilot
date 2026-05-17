from __future__ import annotations

import re
from typing import List, Literal

from pydantic import BaseModel, Field


class InterviewStory(BaseModel):
    problem: str
    solution: str
    impact: str


class ProjectStoryInput(BaseModel):
    project_text: str = Field(..., min_length=1)
    target_role: str = "AI Agent Engineer"
    style: Literal["resume", "interview", "resume_and_interview"] = "resume_and_interview"


class ProjectStoryOutput(BaseModel):
    one_liner: str
    tech_stack: List[str]
    architecture_highlights: List[str]
    resume_bullets_cn: List[str]
    resume_bullets_en: List[str]
    interview_story: InterviewStory
    possible_interview_questions: List[str]


KNOWN_TECH = [
    "Python",
    "Pydantic",
    "pytest",
    "OpenHarness",
    "LLM",
    "Tool Calling",
    "CLI",
    "JSON",
    "Markdown",
    "FastAPI",
    "PostgreSQL",
    "Docker",
    "RAG",
    "MCP",
    "Agent",
    "Memory",
    "Skill",
]


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def _detect_tech_stack(text: str) -> List[str]:
    lowered = text.lower()
    found = []

    aliases = {
        "python": "Python",
        "pydantic": "Pydantic",
        "pytest": "pytest",
        "openharness": "OpenHarness",
        "llm": "LLM",
        "tool calling": "Tool Calling",
        "tool-use": "Tool Calling",
        "cli": "CLI",
        "json": "JSON",
        "markdown": "Markdown",
        "fastapi": "FastAPI",
        "postgresql": "PostgreSQL",
        "docker": "Docker",
        "rag": "RAG",
        "mcp": "MCP",
        "agent": "Agent",
        "memory": "Memory",
        "skill": "Skill",
    }

    for key, value in aliases.items():
        if key in lowered and value not in found:
            found.append(value)

    if not found:
        found = ["Python", "Markdown", "LLM"]

    return found[:8]


def _detect_architecture_highlights(text: str) -> List[str]:
    lowered = text.lower()
    highlights = []

    if "tool" in lowered:
        highlights.append("自定义 Tool 抽象，用于封装 JD 分析、简历匹配和项目经历提炼能力")
    if "skill" in lowered:
        highlights.append("Skill 驱动的领域工作流，将求职流程拆分为可复用步骤")
    if "memory" in lowered or "json" in lowered:
        highlights.append("本地 Memory 记录投递状态、用户画像和结构化分析结果")
    if "cli" in lowered or "demo" in lowered:
        highlights.append("CLI / demo script 支持端到端求职流程演示")
    if "test" in lowered or "pytest" in lowered:
        highlights.append("使用测试覆盖核心工具逻辑，提升输出稳定性")

    if not highlights:
        highlights = [
            "模块化工具设计，便于扩展新的求职自动化能力",
            "结构化输出设计，便于测试、复用和后续工作流编排",
        ]

    return highlights[:5]


def _build_one_liner(text: str, target_role: str) -> str:
    lowered = text.lower()

    if "openharness" in lowered:
        return f"基于 OpenHarness 构建的面向 {target_role} 求职流程智能体"

    if "resume" in lowered or "job" in lowered or "career" in lowered:
        return f"面向 {target_role} 求职场景的个人智能体项目"

    return f"面向 {target_role} 的项目经历提炼与面试表达生成工具"


def _build_resume_bullets_cn(
    tech_stack: List[str],
    architecture_highlights: List[str],
    target_role: str,
) -> List[str]:
    main_tech = "、".join(tech_stack[:4])

    return [
        f"基于 {main_tech} 构建面向 {target_role} 的项目经历提炼工具，将项目 README/说明文档转化为中英文简历 bullet、面试故事和潜在面试问题。",
        f"设计结构化输出 schema，覆盖项目一句话总结、技术栈、架构亮点、简历表述和 STAR 面试故事，提升项目包装的一致性与可测试性。",
        f"通过规则化关键词识别和模板化生成逻辑，降低生成结果不稳定风险，使输出能够直接进入端到端 demo 和单元测试流程。",
    ]


def _build_resume_bullets_en(
    tech_stack: List[str],
    architecture_highlights: List[str],
    target_role: str,
) -> List[str]:
    main_tech = ", ".join(tech_stack[:4])

    return [
        f"Built a project story extraction tool for {target_role} workflows using {main_tech}, converting README-style project descriptions into resume bullets, interview stories, and likely interview questions.",
        "Designed a structured output schema covering project summary, tech stack, architecture highlights, bilingual resume bullets, and STAR-style interview narratives.",
        "Implemented deterministic keyword extraction and template-based generation to improve output stability, testability, and demo reliability.",
    ]


def _build_interview_story(target_role: str) -> InterviewStory:
    return InterviewStory(
        problem="求职过程中，项目经历往往需要针对不同岗位重新组织表达，手动改写耗时且容易遗漏技术亮点。",
        solution=f"围绕 {target_role} 场景设计 Project Story Extractor，将项目说明结构化解析为技术栈、架构亮点、简历 bullet 和面试故事。",
        impact="在 demo 场景中，可以把项目材料快速转化为可复用的简历和面试表达，减少重复整理成本，并提升输出一致性。",
    )


def _build_questions(tech_stack: List[str]) -> List[str]:
    questions = [
        "你为什么要把项目经历提炼单独做成一个 Tool？",
        "这个工具和普通 prompt 生成简历 bullet 有什么区别？",
        "你如何保证输出字段稳定，方便后续测试和 workflow 编排？",
    ]

    if "OpenHarness" in tech_stack:
        questions.append("你在这个项目里具体使用了 OpenHarness 的哪些能力？")
    if "Pydantic" in tech_stack:
        questions.append("为什么使用 Pydantic 定义输入输出 schema？")
    if "Agent" in tech_stack or "Tool Calling" in tech_stack:
        questions.append("Tool schema 设计时，你如何划分输入、输出和异常情况？")

    return questions[:6]


def extract_project_story(
    project_text: str,
    target_role: str = "AI Agent Engineer",
    style: Literal["resume", "interview", "resume_and_interview"] = "resume_and_interview",
) -> ProjectStoryOutput:
    input_data = ProjectStoryInput(
        project_text=project_text,
        target_role=target_role,
        style=style,
    )

    text = _normalize_text(input_data.project_text)
    tech_stack = _detect_tech_stack(text)
    architecture_highlights = _detect_architecture_highlights(text)

    return ProjectStoryOutput(
        one_liner=_build_one_liner(text, input_data.target_role),
        tech_stack=tech_stack,
        architecture_highlights=architecture_highlights,
        resume_bullets_cn=_build_resume_bullets_cn(
            tech_stack,
            architecture_highlights,
            input_data.target_role,
        ),
        resume_bullets_en=_build_resume_bullets_en(
            tech_stack,
            architecture_highlights,
            input_data.target_role,
        ),
        interview_story=_build_interview_story(input_data.target_role),
        possible_interview_questions=_build_questions(tech_stack),
    )


if __name__ == "__main__":
    sample_text = """
    CareerPilot Agent is a personalized job-search agent built on OpenHarness.
    It extends tools, skills, memory, CLI workflows, JSON outputs, and pytest tests.
    """

    result = extract_project_story(
        project_text=sample_text,
        target_role="AI Agent Engineer",
    )

    if hasattr(result, "model_dump_json"):
        print(result.model_dump_json(indent=2, ensure_ascii=False))
    else:
        print(result.json(indent=2, ensure_ascii=False))