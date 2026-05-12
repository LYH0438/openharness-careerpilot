from __future__ import annotations

import re
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class SeniorityLevel(str, Enum):
    junior = "junior"
    mid = "mid"
    senior = "senior"
    unknown = "unknown"


class JDAnalysisInput(BaseModel):
    job_description: str = Field(..., min_length=1)
    target_role: Optional[str] = "Unknown Role"
    language: Optional[str] = "zh-CN"


class JDAnalysisOutput(BaseModel):
    role_summary: str
    seniority_level: SeniorityLevel
    core_skills: List[str]
    nice_to_have_skills: List[str]
    responsibilities: List[str]
    keywords_for_resume: List[str]
    interview_focus: List[str]
    risk_notes: List[str]


TECH_KEYWORDS = {
    "Python": ["python"],
    "FastAPI": ["fastapi"],
    "Django": ["django"],
    "Flask": ["flask"],
    "Java": ["java"],
    "Go": ["golang", " go "],
    "JavaScript": ["javascript", "js"],
    "TypeScript": ["typescript", "ts"],
    "React": ["react"],
    "Node.js": ["node.js", "nodejs", "node "],
    "PostgreSQL": ["postgresql", "postgres"],
    "MySQL": ["mysql"],
    "Redis": ["redis"],
    "MongoDB": ["mongodb"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes", "k8s"],
    "AWS": ["aws", "amazon web services"],
    "GCP": ["gcp", "google cloud"],
    "Azure": ["azure"],
    "CI/CD": ["ci/cd", "github actions", "jenkins", "gitlab ci"],
    "REST API": ["rest api", "restful", "api"],
    "GraphQL": ["graphql"],
    "Microservices": ["microservice", "microservices", "微服务"],
    "Distributed Systems": ["distributed system", "distributed systems", "分布式"],
    "LLM": ["llm", "large language model", "大语言模型"],
    "Agent": ["agent", "智能体"],
    "RAG": ["rag", "retrieval augmented generation"],
}


RESPONSIBILITY_PATTERNS = {
    "设计和维护后端服务": ["backend", "后端", "server-side", "service"],
    "开发和维护 API": ["api", "rest", "graphql"],
    "数据库设计与性能优化": ["database", "数据库", "postgres", "mysql", "query", "索引"],
    "构建可扩展系统": ["scalable", "scale", "可扩展", "distributed", "分布式"],
    "参与部署和 DevOps 流程": ["deploy", "deployment", "docker", "kubernetes", "ci/cd", "devops"],
    "与跨职能团队协作": ["collaborate", "cross-functional", "stakeholder", "协作"],
}


def _normalize_text(text: str) -> str:
    normalized = text.lower().replace("\n", " ")
    return f" {normalized} "


def _find_skills(text: str) -> List[str]:
    normalized = _normalize_text(text)
    found = []

    for skill, patterns in TECH_KEYWORDS.items():
        normalized_patterns = [pattern.lower() for pattern in patterns]
        if any(pattern in normalized for pattern in normalized_patterns):
            found.append(skill)

    return found


def _infer_seniority(text: str) -> SeniorityLevel:
    normalized = _normalize_text(text)

    senior_terms = [
        "senior",
        "lead",
        "principal",
        "staff",
        "5+ years",
        "6+ years",
        "7+ years",
        "8+ years",
        "资深",
        "专家",
    ]
    mid_terms = [
        "mid",
        "3+ years",
        "4+ years",
        "2+ years",
        "中级",
        "有经验",
    ]
    junior_terms = [
        "junior",
        "entry level",
        "new grad",
        "intern",
        "0-1 years",
        "实习",
        "初级",
        "应届",
    ]

    if any(term in normalized for term in senior_terms):
        return SeniorityLevel.senior
    if any(term in normalized for term in mid_terms):
        return SeniorityLevel.mid
    if any(term in normalized for term in junior_terms):
        return SeniorityLevel.junior

    return SeniorityLevel.unknown


def _extract_responsibilities(text: str) -> List[str]:
    normalized = _normalize_text(text)
    responsibilities = []

    for responsibility, patterns in RESPONSIBILITY_PATTERNS.items():
        if any(pattern in normalized for pattern in patterns):
            responsibilities.append(responsibility)

    if not responsibilities:
        responsibilities.append("根据岗位描述完成核心工程任务")

    return responsibilities


def _split_core_and_nice_to_have(skills: List[str], text: str) -> tuple[List[str], List[str]]:
    """
    Split skills into core and nice-to-have.

    Logic:
    - If a skill appears in a sentence/line marked as nice-to-have, treat it as nice.
    - If a skill also appears in a normal requirement sentence, treat it as core.
    - This avoids marking all previous skills as nice just because "nice to have"
      appears nearby later in the JD.
    """
    nice_markers = [
        "nice to have",
        "preferred",
        "plus",
        "bonus",
        "加分",
        "优先",
        "最好",
    ]

    reset_headers = [
        "requirements:",
        "requirement:",
        "required:",
        "must have:",
        "responsibilities:",
        "responsibility:",
        "what you will do:",
        "岗位职责",
        "任职要求",
    ]

    text_lower = text.lower()
    segments: list[tuple[str, bool]] = []
    in_nice_section = False

    for raw_line in text_lower.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if any(header in line for header in reset_headers):
            in_nice_section = False

        # Section header style:
        # Nice to have:
        # - Kubernetes
        # - AWS
        starts_nice_section = (
            line.endswith(":")
            and any(marker in line for marker in nice_markers)
        ) or bool(
            re.match(r"^(nice to have|preferred|plus|bonus|加分|优先|最好)\s*[:：]", line)
        )

        if starts_nice_section:
            in_nice_section = True

        sentence_parts = re.split(r"[.!?。！？；;]+", line)

        for part in sentence_parts:
            segment = part.strip(" -•\t")
            if not segment:
                continue

            segment_is_nice = in_nice_section or any(marker in segment for marker in nice_markers)
            segments.append((segment, segment_is_nice))

    core: List[str] = []
    nice_to_have: List[str] = []

    for skill in skills:
        skill_patterns = [pattern.lower() for pattern in TECH_KEYWORDS.get(skill, [skill.lower()])]

        found_in_core = False
        found_in_nice = False

        for segment, segment_is_nice in segments:
            padded_segment = f" {segment} "

            if any(pattern in padded_segment for pattern in skill_patterns):
                if segment_is_nice:
                    found_in_nice = True
                else:
                    found_in_core = True

        if found_in_nice and not found_in_core:
            nice_to_have.append(skill)
        else:
            core.append(skill)

    return core, nice_to_have


def _build_interview_focus(core_skills: List[str], responsibilities: List[str]) -> List[str]:
    focus = []

    if any(skill in core_skills for skill in ["REST API", "FastAPI", "Django", "Flask", "Node.js"]):
        focus.append("API 设计与后端服务实现")

    if any(skill in core_skills for skill in ["PostgreSQL", "MySQL", "Redis", "MongoDB"]):
        focus.append("数据库设计、索引和性能优化")

    if any(skill in core_skills for skill in ["Docker", "Kubernetes", "CI/CD", "AWS", "GCP", "Azure"]):
        focus.append("部署、云服务和 DevOps 基础")

    if "构建可扩展系统" in responsibilities or "Distributed Systems" in core_skills:
        focus.append("系统设计与可扩展架构")

    if any(skill in core_skills for skill in ["LLM", "Agent", "RAG"]):
        focus.append("LLM 应用、Agent 工作流和 RAG 设计")

    if not focus:
        focus.append("项目经验、技术基础和问题解决能力")

    return focus


def _build_risk_notes(core_skills: List[str], nice_to_have_skills: List[str], responsibilities: List[str]) -> List[str]:
    notes = []

    infra_skills = {"Docker", "Kubernetes", "AWS", "GCP", "Azure", "CI/CD"}
    if infra_skills.intersection(set(core_skills)):
        notes.append("岗位包含明显部署或基础设施要求，简历中需要补充上线、部署或 DevOps 经验。")

    if "Distributed Systems" in core_skills or "构建可扩展系统" in responsibilities:
        notes.append("岗位可能关注系统设计能力，需要准备高并发、缓存、数据库扩展等案例。")

    if {"LLM", "Agent", "RAG"}.intersection(set(core_skills + nice_to_have_skills)):
        notes.append("岗位涉及 AI Agent 或 LLM 应用，需要准备工具调用、上下文管理和输出稳定性相关讲法。")

    if not notes:
        notes.append("未发现明显高风险要求，但仍建议针对核心技能补充项目证据。")

    return notes


def analyze_jd(payload: JDAnalysisInput | dict) -> JDAnalysisOutput:
    if isinstance(payload, dict):
        payload = JDAnalysisInput(**payload)

    text = payload.job_description.strip()
    if not text:
        raise ValueError("job_description cannot be empty")

    skills = _find_skills(text)
    core_skills, nice_to_have_skills = _split_core_and_nice_to_have(skills, text)
    responsibilities = _extract_responsibilities(text)
    seniority_level = _infer_seniority(text)
    interview_focus = _build_interview_focus(core_skills, responsibilities)
    risk_notes = _build_risk_notes(core_skills, nice_to_have_skills, responsibilities)

    target_role = payload.target_role or "this role"

    role_summary = f"{target_role} role focused on {', '.join(core_skills[:4]) if core_skills else 'core engineering capabilities'}."

    keywords_for_resume = list(dict.fromkeys(core_skills + nice_to_have_skills + responsibilities))

    return JDAnalysisOutput(
        role_summary=role_summary,
        seniority_level=seniority_level,
        core_skills=core_skills,
        nice_to_have_skills=nice_to_have_skills,
        responsibilities=responsibilities,
        keywords_for_resume=keywords_for_resume,
        interview_focus=interview_focus,
        risk_notes=risk_notes,
    )


if __name__ == "__main__":
    from pathlib import Path

    sample_path = Path("examples/careerpilot/sample_jd_backend.md")
    jd_text = sample_path.read_text(encoding="utf-8")

    sample = {
        "target_role": "Backend Engineer",
        "language": "zh-CN",
        "job_description": jd_text,
    }

    result = analyze_jd(sample)
    print(result.model_dump_json(indent=2))