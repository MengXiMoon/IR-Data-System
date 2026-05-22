"""定制化求职建议的提示词模板（Prompt Engineering）"""

SYSTEM_PROMPT = """你是一位专业的求职顾问 AI，帮助用户分析招聘信息并提供求职建议。"""

JOB_ADVICE_PROMPT = """根据以下招聘数据，为用户提供个性化的求职建议：

用户背景：{user_background}
岗位信息：{job_info}

请从以下维度给出建议：
1. 技能匹配度分析
2. 薪资竞争力评估
3. 职业发展建议
"""
