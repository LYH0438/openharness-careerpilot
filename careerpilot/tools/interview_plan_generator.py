from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class InterviewPlanInput(BaseModel):
    jd_analysis: dict[str, Any]
    resume_match: dict[str, Any]
    available_days: int = Field(default=3, ge=1, le=14)
    daily_hours: float = Field(default=2.0, ge=0.5, le=8.0)
    target_role: str = "Backend Engineer"
    language: str = "zh-CN"


class InterviewDay(BaseModel):
    day: int
    title: str
    focus: list[str]
    tasks: list[str]
    deliverables: list[str]
    estimated_hours: float


class InterviewPlanOutput(BaseModel):
    target_role: str
    available_days: int
    daily_hours: float
    priority_topics: list[str]
    daily_plan: list[InterviewDay]
    final_checklist: list[str]
    human_review_notice: str


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, (tuple, set)):
        return [str(item).strip() for item in value if str(item).strip()]
    return [str(value).strip()] if str(value).strip() else []


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []

    for item in items:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            result.append(item)

    return result


def _topic_contains(topic: str, keywords: list[str]) -> bool:
    lowered = topic.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def _build_priority_topics(
    jd_analysis: dict[str, Any],
    resume_match: dict[str, Any],
) -> list[str]:
    topics: list[str] = []

    topics.extend(_as_list(resume_match.get("interview_preparation_topics")))
    topics.extend(_as_list(resume_match.get("missing_skills")))
    topics.extend(_as_list(jd_analysis.get("interview_focus")))
    topics.extend(_as_list(jd_analysis.get("core_skills"))[:4])
    topics.extend(_as_list(resume_match.get("resume_keywords_to_add"))[:4])

    weak_evidence = _as_list(resume_match.get("weak_evidence"))
    if weak_evidence:
        topics.append("补强薄弱证据与量化结果")

    topics = _dedupe(topics)

    if not topics:
        return ["项目经历复盘", "核心技术基础", "模拟面试"]

    return topics


def _build_topic_day(topic: str, day: int, daily_hours: float) -> InterviewDay:
    if _topic_contains(topic, ["api", "rest", "fastapi", "django", "flask", "backend", "后端"]):
        title = "Backend API Fundamentals"
        tasks = [
            "复习 REST API 设计、认证授权、错误处理、分页和幂等性。",
            "整理一个你在项目中设计或维护 API 的案例，说明输入、输出、边界和失败处理。",
            "准备 2 个英文回答：API design trade-off 和 backend service ownership。",
        ]
        deliverables = [
            "2 个 API 设计面试回答",
            "1 个后端服务 STAR 项目故事",
        ]

    elif _topic_contains(topic, ["database", "postgres", "mysql", "redis", "索引", "数据库", "query"]):
        title = "Database and Performance"
        tasks = [
            "复习索引、事务、慢查询、连接池和缓存的基础概念。",
            "把项目中的数据库使用场景改写成一个性能优化或数据建模故事。",
            "准备解释：什么时候加索引、什么时候用缓存、如何排查慢查询。",
        ]
        deliverables = [
            "1 个数据库优化 STAR 故事",
            "3 个数据库高频问题的要点答案",
        ]

    elif _topic_contains(topic, ["docker", "kubernetes", "k8s", "aws", "gcp", "azure", "ci/cd", "devops", "部署"]):
        title = "Deployment, Cloud, and DevOps"
        tasks = [
            "复习 Docker 镜像、容器运行、环境变量、日志和基础部署流程。",
            "整理你项目中可诚实描述的部署、测试或 CI/CD 经验。",
            "准备说明你如何让一个服务从本地脚本变成可运行 demo。",
        ]
        deliverables = [
            "1 个部署或 CI/CD 项目回答",
            "1 份可加入简历的 DevOps 证据 bullet 草稿",
        ]

    elif _topic_contains(topic, ["system design", "distributed", "scalable", "系统设计", "分布式", "可扩展"]):
        title = "System Design and Scalability"
        tasks = [
            "复习容量估算、API 边界、数据存储、缓存、异步任务和故障处理。",
            "用 CareerPilot demo 画出一个简单系统设计讲法：输入、工具、报告、memory。",
            "准备回答：如何从单脚本演进到多 Agent 或 RAG 系统。",
        ]
        deliverables = [
            "1 个系统设计口述大纲",
            "1 张文字版架构图或流程图",
        ]

    elif _topic_contains(topic, ["llm", "agent", "rag", "tool calling", "智能体", "工具调用"]):
        title = "LLM Agent Workflow"
        tasks = [
            "复习 tool-use、skill、memory、structured output 和 human review 的边界。",
            "准备解释 CareerPilot 为什么不是普通 prompt，而是工具化 workflow。",
            "整理输出稳定性方案：Pydantic schema、规则解析、测试和人工审核。",
        ]
        deliverables = [
            "1 个 Agent 架构讲解回答",
            "1 个 Tool schema 设计回答",
        ]

    elif _topic_contains(topic, ["量化", "metric", "evidence", "证据", "impact", "薄弱"]):
        title = "Resume Evidence and STAR Stories"
        tasks = [
            "检查简历中没有数字或结果的 bullet，补充真实可验证的影响。",
            "为核心项目准备 Problem、Action、Result 三段式讲法。",
            "把缺失技能转化为不夸大的学习计划或项目证据表达。",
        ]
        deliverables = [
            "2 条带结果的简历 bullet 草稿",
            "1 个项目 STAR 故事",
        ]

    else:
        title = f"Role Requirement Deep Dive: {topic}"
        tasks = [
            f"复习 JD 中与 `{topic}` 相关的基础概念、常见问题和项目使用场景。",
            "把该主题映射到你的简历证据：项目、课程、工具或真实经历。",
            "准备一个 60-90 秒回答，说明你如何学习或实践过该主题。",
        ]
        deliverables = [
            f"1 个围绕 `{topic}` 的面试回答",
            "1 条可人工审核的简历补充建议",
        ]

    return InterviewDay(
        day=day,
        title=title,
        focus=[topic],
        tasks=tasks,
        deliverables=deliverables,
        estimated_hours=daily_hours,
    )


def _build_mock_day(
    day: int,
    daily_hours: float,
    priority_topics: list[str],
) -> InterviewDay:
    return InterviewDay(
        day=day,
        title="Mock Interview and Final Review",
        focus=priority_topics[:4],
        tasks=[
            "进行一轮 30-45 分钟模拟面试：自我介绍、项目深挖、技术基础、行为问题。",
            "检查每个高优先级主题是否都有一个真实项目证据或诚实的学习计划。",
            "复盘回答中过度夸大、缺少数字、缺少技术细节的地方。",
        ],
        deliverables=[
            "1 份 2 分钟英文自我介绍",
            "3 个项目深挖答案",
            "1 份最后修改清单",
        ],
        estimated_hours=daily_hours,
    )


def generate_interview_plan(
    payload: InterviewPlanInput | dict[str, Any],
) -> InterviewPlanOutput:
    data = payload if isinstance(payload, InterviewPlanInput) else InterviewPlanInput(**payload)
    priority_topics = _build_priority_topics(data.jd_analysis, data.resume_match)

    daily_plan: list[InterviewDay] = []

    for day in range(1, data.available_days + 1):
        if day == data.available_days:
            daily_plan.append(_build_mock_day(day, data.daily_hours, priority_topics))
            continue

        topic = priority_topics[(day - 1) % len(priority_topics)]
        daily_plan.append(_build_topic_day(topic, day, data.daily_hours))

    final_checklist = [
        "每个 JD 核心技能至少对应一个简历或项目证据。",
        "每个缺失技能都有诚实表述：补项目证据、写 familiar，或放入学习计划。",
        "至少准备 3 个 STAR 项目故事：后端实现、问题排查、结果影响。",
        "所有简历修改都需要人工审核，不能编造经历或夸大熟练度。",
    ]

    return InterviewPlanOutput(
        target_role=data.target_role,
        available_days=data.available_days,
        daily_hours=data.daily_hours,
        priority_topics=priority_topics,
        daily_plan=daily_plan,
        final_checklist=final_checklist,
        human_review_notice=(
            "This interview plan is generated for preparation purposes. "
            "Verify every resume claim and project story before using it in real applications."
        ),
    )


def format_interview_plan_markdown(
    plan: InterviewPlanOutput | dict[str, Any],
) -> str:
    if isinstance(plan, dict):
        plan = InterviewPlanOutput(**plan)

    lines: list[str] = [
        "# Interview Preparation Plan",
        "",
        f"Target role: **{plan.target_role}**",
        f"Schedule: **{plan.available_days} days × {plan.daily_hours:g} hours/day**",
        "",
        "## Priority Topics",
    ]

    lines.extend(f"- {topic}" for topic in plan.priority_topics)
    lines.append("")

    for item in plan.daily_plan:
        lines.append(f"## Day {item.day}: {item.title}")
        lines.append("")
        lines.append("Focus:")
        lines.extend(f"- {topic}" for topic in item.focus)
        lines.append("")
        lines.append("Tasks:")
        lines.extend(f"- {task}" for task in item.tasks)
        lines.append("")
        lines.append("Deliverables:")
        lines.extend(f"- {deliverable}" for deliverable in item.deliverables)
        lines.append("")

    lines.append("## Final Checklist")
    lines.extend(f"- {item}" for item in plan.final_checklist)
    lines.append("")
    lines.append(f"> Human review required: {plan.human_review_notice}")

    return "\n".join(lines).strip()


if __name__ == "__main__":
    sample = InterviewPlanInput(
        target_role="Backend Engineer",
        available_days=3,
        daily_hours=2,
        jd_analysis={
            "core_skills": ["Python", "FastAPI", "PostgreSQL"],
            "interview_focus": ["API 设计与后端服务实现", "数据库设计、索引和性能优化"],
        },
        resume_match={
            "missing_skills": ["Kubernetes", "CI/CD"],
            "weak_evidence": ["Resume lacks quantified impact."],
            "interview_preparation_topics": ["system design", "database optimization"],
        },
    )

    result = generate_interview_plan(sample)
    print(format_interview_plan_markdown(result))
