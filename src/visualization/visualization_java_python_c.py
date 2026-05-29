"""Java/Python/C/C++ 工程师招聘数据可视化

5个可视化角度:
  1. 薪资分布分析 —— 整体薪资直方图 + 不同经验级别薪资箱线图
  2. 城市地域分布 —— Top15城市岗位数量 + 热门城市区域分布
  3. 企业类型与规模 —— 企业类型饼图 + 企业规模柱状图
  4. 学历与经验要求 —— 学历分布 + 工作经验分布
  5. 技能需求热词 —— 技能关键词词云 + Top20技能频次
  6. 编程语言维度对比 —— Java/Python/C_C++岗位数量与薪资对比 (额外角度)
  7. 行业分布 —— 所属行业 Top12 饼图 (额外角度)
"""

import os
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

_FONT_NAME = None
_FONT_PATH = None

CHART_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data", "processed", "charts"
)


def _init_font():
    global _FONT_NAME, _FONT_PATH
    if _FONT_NAME:
        return _FONT_NAME, _FONT_PATH
    candidates = [
        "Microsoft YaHei", "SimHei", "Noto Sans SC",
        "KaiTi", "FangSong", "STXihei",
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


def _fp():
    return fm.FontProperties(fname=_FONT_PATH) if _FONT_PATH else None


_init_font()


def _save(fig, name):
    os.makedirs(CHART_DIR, exist_ok=True)
    path = os.path.join(CHART_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  已保存: {path}")


# ============================================================
# 角度1: 薪资分布分析
# ============================================================
def plot_salary_distribution(df: pd.DataFrame):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fp = _fp()

    salaries = df["平均月薪"].dropna()
    ax = axes[0]
    ax.hist(salaries / 1000, bins=40, color="#4e79a7", edgecolor="white", alpha=0.85)
    ax.set_xlabel("月薪（千元）", fontproperties=fp, fontsize=12)
    ax.set_ylabel("岗位数量", fontproperties=fp, fontsize=12)
    ax.set_title("Java/Python/C工程师薪资分布", fontproperties=fp, fontsize=14)
    median_val = salaries.median() / 1000
    mean_val = salaries.mean() / 1000
    ax.axvline(median_val, color="red", linestyle="--",
               label=f"中位数: {median_val:.1f}k")
    ax.axvline(mean_val, color="orange", linestyle=":",
               label=f"均值: {mean_val:.1f}k")
    ax.legend(prop=fp)

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
    palette = sns.color_palette("YlOrRd", len(box_data))
    for patch, color in zip(bp["boxes"], palette):
        patch.set_facecolor(color)
    ax.set_xlabel("工作经验", fontproperties=fp, fontsize=12)
    ax.set_ylabel("月薪（元）", fontproperties=fp, fontsize=12)
    ax.set_title("不同经验级别薪资对比", fontproperties=fp, fontsize=14)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}k"))

    plt.tight_layout()
    _save(fig, "salary_distribution.png")


# ============================================================
# 角度2: 城市地域分布
# ============================================================
def plot_company_region(df: pd.DataFrame, top_n: int = 15):
    fig, axes = plt.subplots(1, 2, figsize=(16, 5))
    fp = _fp()

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

    ax = axes[1]
    top_city = city_counts.index[0]
    top_city_data = df[df["城市"] == top_city]
    district_counts = top_city_data["区域"].value_counts().head(10)
    colors_pie = sns.color_palette("Set3", len(district_counts))
    wedges, texts, autotexts = ax.pie(
        district_counts.values, autopct="%1.1f%%", colors=colors_pie,
    )
    ax.legend(wedges, district_counts.index, title="区域",
              loc="center left", bbox_to_anchor=(1, 0.5), prop=fp)
    ax.set_title(f"{top_city}各区域岗位分布", fontproperties=fp, fontsize=14)

    plt.tight_layout()
    _save(fig, "company_region.png")


# ============================================================
# 角度3: 企业类型与规模
# ============================================================
def plot_company_type(df: pd.DataFrame):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fp = _fp()

    ax = axes[0]
    type_counts = df["公司类型"].value_counts()
    colors_t = sns.color_palette("Set2", len(type_counts))
    wedges, texts, autotexts = ax.pie(
        type_counts.values, autopct="%1.1f%%", colors=colors_t,
    )
    ax.legend(wedges, type_counts.index, title="企业类型",
              loc="center left", bbox_to_anchor=(1, 0.5), prop=fp)
    ax.set_title("企业类型分布", fontproperties=fp, fontsize=14)

    ax = axes[1]
    size_order = ["20人以下", "20-99人", "100-299人", "300-499人",
                  "500-999人", "1000-9999人", "10000人以上"]
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
    _save(fig, "company_type.png")


# ============================================================
# 角度4: 学历与经验要求
# ============================================================
def plot_education_requirements(df: pd.DataFrame):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fp = _fp()

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
    _save(fig, "education_requirements.png")


# ============================================================
# 角度5: 技能需求热词
# ============================================================
def plot_skill_wordcloud(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(14, 7))
    fp = _fp()

    skills_text = df["技能关键词"].dropna().str.cat(sep=" ")
    words = [w.strip() for w in skills_text.split()
             if len(w.strip()) > 1 and not w.strip().isdigit()]
    skills_text = " ".join(words)

    wc_kwargs = dict(
        width=1400, height=700, background_color="white",
        colormap="viridis", max_words=120, max_font_size=180,
        collocations=False,
    )
    if _FONT_PATH:
        wc_kwargs["font_path"] = _FONT_PATH

    wc = WordCloud(**wc_kwargs)
    wc.generate(skills_text)
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    ax.set_title("Java/Python/C工程师技能要求词云", fontproperties=fp, fontsize=20)

    plt.tight_layout()
    _save(fig, "skill_wordcloud.png")


def plot_top_skills(df: pd.DataFrame, top_n: int = 20):
    fig, ax = plt.subplots(figsize=(10, 8))
    fp = _fp()

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
    _save(fig, "top_skills.png")


# ============================================================
# 角度6: 编程语言维度对比
# ============================================================
def plot_language_comparison(df: pd.DataFrame):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fp = _fp()

    lang_order = ["Java", "Python", "C_C++", "多语言", "其他"]
    lang_labels = ["Java", "Python", "C/C++", "多语言", "其他"]

    ax = axes[0]
    lang_counts = df["语言类别"].value_counts()
    counts = [lang_counts.get(l, 0) for l in lang_order]
    colors = ["#f1ce63", "#4e79a7", "#e15759", "#76b7b2", "#af7aa1"]
    bars = ax.bar(range(len(lang_order)), counts, color=colors, edgecolor="white")
    ax.set_xticks(range(len(lang_order)))
    ax.set_xticklabels(lang_labels, fontproperties=fp, fontsize=11)
    ax.set_ylabel("岗位数量", fontproperties=fp, fontsize=12)
    ax.set_title("各语言岗位数量对比", fontproperties=fp, fontsize=14)
    for bar, val in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50,
                str(val), ha="center", fontproperties=fp, fontsize=10)

    ax = axes[1]
    avg_salaries = []
    for l in lang_order:
        avg = df[df["语言类别"] == l]["平均月薪"].mean()
        avg_salaries.append(avg if not pd.isna(avg) else 0)
    bars = ax.bar(range(len(lang_order)), [v / 1000 for v in avg_salaries],
                  color=colors, edgecolor="white")
    ax.set_xticks(range(len(lang_order)))
    ax.set_xticklabels(lang_labels, fontproperties=fp, fontsize=11)
    ax.set_ylabel("平均月薪（千元）", fontproperties=fp, fontsize=12)
    ax.set_title("各语言平均薪资对比", fontproperties=fp, fontsize=14)
    for bar, val in zip(bars, avg_salaries):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                f"{val/1000:.1f}k", ha="center", fontproperties=fp, fontsize=10)

    plt.tight_layout()
    _save(fig, "language_comparison.png")


# ============================================================
# 角度7: 行业分布
# ============================================================
def plot_industry_distribution(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 7))
    fp = _fp()

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
    _save(fig, "industry_distribution.png")


# ============================================================
# 主入口
# ============================================================
def run_all(csv_path: str):
    print("=" * 60)
    print("Java/Python/C/C++ 工程师招聘数据可视化")
    print("=" * 60)

    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    print(f"加载数据: {csv_path}")
    print(f"维度: {df.shape}")
    print()

    print("[1/7] 薪资分布分析")
    plot_salary_distribution(df)

    print("[2/7] 城市地域分布")
    plot_company_region(df)

    print("[3/7] 企业类型与规模")
    plot_company_type(df)

    print("[4/7] 学历与经验要求")
    plot_education_requirements(df)

    print("[5/7] 技能需求热词")
    plot_skill_wordcloud(df)
    plot_top_skills(df)

    print("[6/7] 编程语言维度对比")
    plot_language_comparison(df)

    print("[7/7] 行业分布")
    plot_industry_distribution(df)

    print()
    print("=" * 60)
    print(f"全部图表已保存至: {CHART_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    csv_path = sys.argv[1] if len(sys.argv) > 1 else (
        r"e:\code\program\IR-Data-System\data\processed\智联招聘java_python_C工程师_cleaned.csv"
    )
    run_all(csv_path)
