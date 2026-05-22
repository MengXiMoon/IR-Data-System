"""可视化响应模块 — 生成各类分析图表"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.font_manager as fm
import seaborn as sns
import pandas as pd
import numpy as np
from wordcloud import WordCloud
from collections import Counter

# ---- 中文字体配置 ----
_FONT_NAME = None
_FONT_PATH = None


def _init_font():
    """探测可用的中文字体并全局配置"""
    global _FONT_NAME, _FONT_PATH
    if _FONT_NAME:
        return _FONT_NAME, _FONT_PATH

    # 按优先级探测字体
    candidates = [
        "Microsoft YaHei",
        "SimHei",
        "Noto Sans SC",
        "KaiTi",
        "FangSong",
        "STXihei",
    ]
    for name in candidates:
        for f in fm.fontManager.ttflist:
            if f.name == name:
                _FONT_NAME = f.name
                _FONT_PATH = f.fname
                break
        if _FONT_NAME:
            break

    if _FONT_NAME:
        plt.rcParams["font.sans-serif"] = [_FONT_NAME, "SimHei", "DejaVu Sans"]
        plt.rcParams["font.family"] = "sans-serif"
        plt.rcParams["axes.unicode_minus"] = False
    return _FONT_NAME, _FONT_PATH


_init_font()


def _font_props():
    """返回可在 matplotlib 中使用的字体属性"""
    return fm.FontProperties(fname=_FONT_PATH) if _FONT_PATH else None


# ==============================
# 薪资分析
# ==============================

def plot_salary_distribution(df: pd.DataFrame) -> plt.Figure:
    """薪资分布直方图 + 经验箱线图"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fp = _font_props()

    salaries = df["平均月薪"].dropna()
    ax = axes[0]
    ax.hist(salaries / 1000, bins=40, color="#4e79a7", edgecolor="white", alpha=0.85)
    ax.set_xlabel("月薪（千元）", fontproperties=fp, fontsize=12)
    ax.set_ylabel("岗位数量", fontproperties=fp, fontsize=12)
    ax.set_title("Python工程师薪资分布", fontproperties=fp, fontsize=14)
    median_val = salaries.median() / 1000
    ax.axvline(median_val, color="red", linestyle="--",
               label=f"中位数: {median_val:.1f}k")
    ax.legend(prop=fp)

    # 按经验分组的薪资箱线图
    ax = axes[1]
    exp_cat = ["1年以下", "1-3年", "3-5年", "5-10年", "10年以上"]
    box_data = []
    labels_present = []
    for e in exp_cat:
        vals = df[df["工作经验"] == e]["平均月薪"].dropna()
        if len(vals) > 0:
            box_data.append(vals.values)
            labels_present.append(e)
    bp = ax.boxplot(box_data, labels=labels_present, patch_artist=True, showfliers=False)
    for patch in bp["boxes"]:
        patch.set_facecolor("#59a14f")
    ax.set_xlabel("工作经验", fontproperties=fp, fontsize=12)
    ax.set_ylabel("月薪（元）", fontproperties=fp, fontsize=12)
    ax.set_title("不同经验级别薪资对比", fontproperties=fp, fontsize=14)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}k"))

    plt.tight_layout()
    return fig


def plot_year_end_bonus(df: pd.DataFrame) -> plt.Figure:
    """年终奖（年薪月数）分布"""
    fig, ax = plt.subplots(figsize=(8, 5))
    fp = _font_props()

    months = df["年薪月数"].dropna()
    counts = months.value_counts().sort_index()
    colors = ["#4e79a7" if m == 12 else "#f28e2b" for m in counts.index]
    ax.bar(counts.index.astype(str), counts.values, color=colors, edgecolor="white")
    ax.set_xlabel("年薪月数", fontproperties=fp, fontsize=12)
    ax.set_ylabel("岗位数量", fontproperties=fp, fontsize=12)
    ax.set_title("年终奖分布（12薪=无年终奖）", fontproperties=fp, fontsize=14)

    plt.tight_layout()
    return fig


# ==============================
# 企业分析
# ==============================

def plot_company_region(df: pd.DataFrame, top_n: int = 15) -> plt.Figure:
    """企业地域分布（城市 + 区域饼图）"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 5))
    fp = _font_props()

    # 城市分布
    ax = axes[0]
    city_counts = df["城市"].value_counts().head(top_n)
    colors_sorted = ["#e15759" if i == 0 else "#76b7b2" for i in range(len(city_counts))]
    bars = ax.barh(range(len(city_counts)), city_counts.values, color=colors_sorted)
    ax.set_yticks(range(len(city_counts)))
    ax.set_yticklabels(city_counts.index, fontproperties=fp)
    ax.set_xlabel("岗位数量", fontproperties=fp, fontsize=12)
    ax.set_title("企业城市分布 Top15", fontproperties=fp, fontsize=14)
    ax.invert_yaxis()
    for bar, val in zip(bars, city_counts.values):
        ax.text(bar.get_width() + 5, bar.get_y() + 0.35, str(val),
                fontproperties=fp, va="center")

    # 区域分布 - 取岗位数量最多的城市
    ax = axes[1]
    top_city = city_counts.index[0]
    top_city_data = df[df["城市"] == top_city]
    district_counts = top_city_data["区域"].value_counts().head(10)
    colors_pie = sns.color_palette("Set3", len(district_counts))
    wedges, texts, autotexts = ax.pie(
        district_counts.values, autopct="%1.1f%%",
        colors=colors_pie,
    )
    ax.legend(wedges, district_counts.index, title="区域",
              loc="center left", bbox_to_anchor=(1, 0.5), prop=fp)
    ax.set_title(f"{top_city}各区域岗位分布", fontproperties=fp, fontsize=14)

    plt.tight_layout()
    return fig


def plot_company_type(df: pd.DataFrame) -> plt.Figure:
    """企业类型与规模分布"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fp = _font_props()

    # 企业类型饼图
    ax = axes[0]
    type_counts = df["公司类型"].value_counts()
    colors_t = sns.color_palette("Set2", len(type_counts))
    wedges, texts, autotexts = ax.pie(
        type_counts.values, autopct="%1.1f%%",
        colors=colors_t,
    )
    ax.legend(wedges, type_counts.index, title="企业类型",
              loc="center left", bbox_to_anchor=(1, 0.5), prop=fp)
    ax.set_title("企业类型分布", fontproperties=fp, fontsize=14)

    # 企业规模柱状图
    ax = axes[1]
    size_order = ["20-99人", "100-299人", "300-499人", "500-999人",
                  "1000-9999人", "10000人以上"]
    size_counts = df["公司规模"].value_counts()
    available = [s for s in size_order if s in size_counts.index]
    counts = [size_counts.get(s, 0) for s in available]
    ax.barh(range(len(available)), counts,
            color=sns.color_palette("viridis", len(available)))
    ax.set_yticks(range(len(available)))
    ax.set_yticklabels(available, fontproperties=fp)
    ax.set_xlabel("岗位数量", fontproperties=fp, fontsize=12)
    ax.set_title("企业规模分布", fontproperties=fp, fontsize=14)
    ax.invert_yaxis()

    plt.tight_layout()
    return fig


# ==============================
# 岗位需求（词云）
# ==============================

def plot_skill_wordcloud(df: pd.DataFrame) -> plt.Figure:
    """技能关键词词云"""
    fig, ax = plt.subplots(figsize=(14, 7))
    fp = _font_props()

    skills_text = df["技能关键词"].dropna().str.cat(sep=" ")
    # 清理：只保留有意义的词
    words = [w.strip() for w in skills_text.split()
             if len(w.strip()) > 1 and not w.strip().isdigit()]
    skills_text = " ".join(words)

    wc_kwargs = dict(
        width=1400,
        height=700,
        background_color="white",
        colormap="viridis",
        max_words=120,
        max_font_size=180,
        collocations=False,
    )
    if _FONT_PATH:
        wc_kwargs["font_path"] = _FONT_PATH

    wc = WordCloud(**wc_kwargs)
    wc.generate(skills_text)
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    ax.set_title("Python工程师技能要求词云", fontproperties=fp, fontsize=20)

    plt.tight_layout()
    return fig


def plot_top_skills(df: pd.DataFrame, top_n: int = 20) -> plt.Figure:
    """TOP N 技能频次柱状图"""
    fig, ax = plt.subplots(figsize=(10, 8))
    fp = _font_props()

    skills_text = df["技能关键词"].dropna().str.cat(sep=" ")
    words = [w.strip() for w in skills_text.split()
             if len(w.strip()) > 1 and not w.strip().isdigit()]
    word_counts = Counter(words)
    top = word_counts.most_common(top_n)

    labels, values = zip(*top)
    colors = ["#e15759" if i < 3 else "#4e79a7" for i in range(len(labels))]
    bars = ax.barh(range(len(labels)), values, color=colors)
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontproperties=fp)
    ax.set_xlabel("出现次数", fontproperties=fp, fontsize=12)
    ax.set_title("技能关键词 Top 20", fontproperties=fp, fontsize=14)
    ax.invert_yaxis()
    for i, v in enumerate(values):
        ax.text(v + 2, i, str(v), va="center", fontproperties=fp)

    plt.tight_layout()
    return fig


# ==============================
# 学历与经验分布
# ==============================

def plot_education_requirements(df: pd.DataFrame) -> plt.Figure:
    """学历与工作经验分布"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fp = _font_props()

    # 学历分布
    ax = axes[0]
    edu_counts = df["学历要求"].value_counts()
    colors_edu = sns.color_palette("Set3", len(edu_counts))
    bars = ax.bar(range(len(edu_counts)), edu_counts.values,
                  color=colors_edu, edgecolor="white")
    ax.set_xticks(range(len(edu_counts)))
    ax.set_xticklabels(edu_counts.index.astype(str), fontproperties=fp, rotation=20)
    ax.set_ylabel("岗位数量", fontproperties=fp, fontsize=12)
    ax.set_title("学历要求分布", fontproperties=fp, fontsize=14)
    for bar, val in zip(bars, edu_counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5, str(val),
                ha="center", fontproperties=fp, fontsize=10)

    # 经验分布
    ax = axes[1]
    exp_counts = df["工作经验"].value_counts()
    colors_exp = sns.color_palette("Set2", len(exp_counts))
    bars = ax.bar(range(len(exp_counts)), exp_counts.values,
                  color=colors_exp, edgecolor="white")
    ax.set_xticks(range(len(exp_counts)))
    ax.set_xticklabels(exp_counts.index.astype(str), fontproperties=fp, rotation=20)
    ax.set_ylabel("岗位数量", fontproperties=fp, fontsize=12)
    ax.set_title("工作经验要求分布", fontproperties=fp, fontsize=14)
    for bar, val in zip(bars, exp_counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5, str(val),
                ha="center", fontproperties=fp, fontsize=10)

    plt.tight_layout()
    return fig


# ==============================
# 行业分析
# ==============================

def plot_industry_distribution(df: pd.DataFrame) -> plt.Figure:
    """行业分布饼图"""
    fig, ax = plt.subplots(figsize=(10, 7))
    fp = _font_props()

    industry_counts = df["所属行业"].dropna().value_counts().head(12)
    colors_i = sns.color_palette("viridis", len(industry_counts))
    wedges, texts, autotexts = ax.pie(
        industry_counts.values, autopct="%1.1f%%",
        colors=colors_i, pctdistance=0.85,
    )
    ax.legend(wedges, industry_counts.index, title="行业",
              loc="center left", bbox_to_anchor=(1, 0.5), prop=fp)
    ax.set_title("所属行业分布 Top 12", fontproperties=fp, fontsize=14)

    plt.tight_layout()
    return fig


# ==============================
# 薪资交叉分析
# ==============================

def plot_salary_by_education(df: pd.DataFrame) -> plt.Figure:
    """不同学历的薪资水平对比"""
    fig, ax = plt.subplots(figsize=(10, 5))
    fp = _font_props()

    avg_salaries = df.groupby("学历要求")["平均月薪"].mean()
    labels = list(avg_salaries.index.astype(str))
    vals = avg_salaries.values

    colors = sns.color_palette("RdYlGn", len(labels))
    bars = ax.bar(range(len(labels)), [v / 1000 for v in vals],
                  color=colors, edgecolor="white")
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, fontproperties=fp)
    ax.set_ylabel("平均月薪（千元）", fontproperties=fp, fontsize=12)
    ax.set_title("不同学历平均薪资对比", fontproperties=fp, fontsize=14)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f"{val/1000:.1f}k", ha="center", fontproperties=fp, fontsize=11)

    plt.tight_layout()
    return fig
