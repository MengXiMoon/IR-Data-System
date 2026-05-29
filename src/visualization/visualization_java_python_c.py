"""Java/Python/C/C++ 工程师招聘数据可视化

可视化角度（12个，涵盖多种图形类型）:
  1.  薪资分布直方图+KDE —— 直方图 + 核密度估计曲线
  2.  经验级别薪资箱线图 —— 箱线图 (Boxplot)
  3.  经验×学历薪资热力图 —— 热力图 (Heatmap)
  4.  城市×语言类别岗位数热力图 —— 热力图 (Heatmap)
  5.  语言类别薪资小提琴图 —— 小提琴图 (Violin Plot)
  6.  薪资范围散点图 —— 散点图 (Scatter Plot)
  7.  城市语言堆叠柱状图 —— 堆叠柱状图 (Stacked Bar)
  8.  学历分布环形图 —— 环形图 (Donut Chart)
  9.  技能需求词云 —— 词云图 (Word Cloud)
  10. Top20技能频次 —— 水平柱状图 (Horizontal Bar)
  11. 编程语言维度对比 —— 分组柱状图 (Grouped Bar)
  12. 行业分布环形图 —— 环形图 (Donut Chart)
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

EXP_ORDER = ["经验不限", "1年以下", "1-3年", "3-5年", "5-10年", "10年以上"]
EDU_ORDER = ["学历不限", "初中及以下", "高中", "中专/中技", "大专", "本科", "硕士", "博士"]
SIZE_ORDER = [
    "20人以下", "20-99人", "100-299人", "300-499人",
    "500-999人", "1000-9999人", "10000人以上",
]
LANG_ORDER = ["Java", "Python", "C_C++", "多语言", "其他"]
LANG_LABELS = ["Java", "Python", "C/C++", "多语言", "其他"]
LANG_COLORS = ["#f1ce63", "#4e79a7", "#e15759", "#76b7b2", "#af7aa1"]


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
# 角度1: 薪资分布直方图 + KDE
# ============================================================
def plot_salary_distribution(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(12, 6))
    fp = _fp()

    salaries = df["平均月薪"].dropna() / 1000
    ax.hist(salaries, bins=45, color="#4e79a7", edgecolor="white",
            alpha=0.7, density=True, label="频率分布")
    salaries.plot.kde(ax=ax, color="#e15759", linewidth=2.5, label="核密度估计")

    median_val = salaries.median()
    mean_val = salaries.mean()
    ax.axvline(median_val, color="red", linestyle="--", linewidth=1.5,
               label=f"中位数: {median_val:.1f}k")
    ax.axvline(mean_val, color="orange", linestyle=":", linewidth=1.5,
               label=f"均值: {mean_val:.1f}k")

    ax.set_xlabel("月薪（千元）", fontproperties=fp, fontsize=12)
    ax.set_ylabel("密度", fontproperties=fp, fontsize=12)
    ax.set_title("Java/Python/C工程师薪资分布（直方图+KDE）", fontproperties=fp, fontsize=15)
    ax.legend(prop=fp, fontsize=11)

    plt.tight_layout()
    _save(fig, "salary_distribution.png")


# ============================================================
# 角度2: 经验级别薪资箱线图
# ============================================================
def plot_salary_boxplot(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(12, 6))
    fp = _fp()

    exp_cat = [e for e in EXP_ORDER if e in df["工作经验"].values]
    box_data = [df[df["工作经验"] == e]["平均月薪"].dropna().values for e in exp_cat]

    bp = ax.boxplot(box_data, labels=exp_cat, patch_artist=True, showfliers=False,
                    widths=0.5, medianprops=dict(color="black", linewidth=2))
    palette = sns.color_palette("YlOrRd", len(box_data))
    for patch, color in zip(bp["boxes"], palette):
        patch.set_facecolor(color)
        patch.set_alpha(0.85)

    ax.set_xlabel("工作经验", fontproperties=fp, fontsize=12)
    ax.set_ylabel("月薪（元）", fontproperties=fp, fontsize=12)
    ax.set_title("不同经验级别薪资箱线图", fontproperties=fp, fontsize=15)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}k"))
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    _save(fig, "salary_boxplot.png")


# ============================================================
# 角度3: 经验×学历薪资热力图
# ============================================================
def plot_exp_edu_heatmap(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 7))
    fp = _fp()

    valid = df.dropna(subset=["工作经验", "学历要求", "平均月薪"])
    pivot = valid.groupby(["工作经验", "学历要求"])["平均月薪"].mean().reset_index()
    pivot_table = pivot.pivot(index="工作经验", columns="学历要求", values="平均月薪")

    exp_present = [e for e in EXP_ORDER if e in pivot_table.index]
    edu_present = [e for e in EDU_ORDER if e in pivot_table.columns]
    pivot_table = pivot_table.reindex(index=exp_present, columns=edu_present)

    sns.heatmap(
        pivot_table / 1000, annot=True, fmt=".1f", cmap="YlOrRd",
        linewidths=0.8, linecolor="white", ax=ax,
        cbar_kws={"label": "平均月薪（千元）"},
    )
    ax.set_xlabel("学历要求", fontproperties=fp, fontsize=12)
    ax.set_ylabel("工作经验", fontproperties=fp, fontsize=12)
    ax.set_title("经验×学历 平均薪资热力图（千元）", fontproperties=fp, fontsize=15)
    ax.set_yticklabels(ax.get_yticklabels(), fontproperties=fp, rotation=0)
    ax.set_xticklabels(ax.get_xticklabels(), fontproperties=fp, rotation=30, ha="right")

    plt.tight_layout()
    _save(fig, "exp_edu_salary_heatmap.png")


# ============================================================
# 角度4: 城市×语言类别岗位数热力图
# ============================================================
def plot_city_lang_heatmap(df: pd.DataFrame, top_n: int = 12):
    fig, ax = plt.subplots(figsize=(10, 8))
    fp = _fp()

    top_cities = df["城市"].value_counts().head(top_n).index.tolist()
    subset = df[df["城市"].isin(top_cities)]
    pivot = subset.groupby(["城市", "语言类别"]).size().reset_index(name="岗位数")
    pivot_table = pivot.pivot(index="城市", columns="语言类别", values="岗位数").fillna(0)

    city_order = [c for c in top_cities if c in pivot_table.index]
    lang_present = [l for l in LANG_ORDER if l in pivot_table.columns]
    pivot_table = pivot_table.reindex(index=city_order, columns=lang_present)

    sns.heatmap(
        pivot_table, annot=True, fmt=".0f", cmap="Blues",
        linewidths=0.8, linecolor="white", ax=ax,
        cbar_kws={"label": "岗位数量"},
    )
    ax.set_xlabel("语言类别", fontproperties=fp, fontsize=12)
    ax.set_ylabel("城市", fontproperties=fp, fontsize=12)
    ax.set_title("城市×语言类别 岗位数量热力图", fontproperties=fp, fontsize=15)
    ax.set_yticklabels(ax.get_yticklabels(), fontproperties=fp, rotation=0)
    lang_tick_labels = [LANG_LABELS[LANG_ORDER.index(l)] for l in lang_present]
    ax.set_xticklabels(lang_tick_labels, fontproperties=fp, rotation=0)

    plt.tight_layout()
    _save(fig, "city_lang_heatmap.png")


# ============================================================
# 角度5: 语言类别薪资小提琴图
# ============================================================
def plot_salary_violin(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(12, 6))
    fp = _fp()

    plot_df = df[df["语言类别"].isin(LANG_ORDER)].copy()
    plot_df["薪资千元"] = plot_df["平均月薪"] / 1000

    palette = dict(zip(LANG_ORDER, LANG_COLORS))
    sns.violinplot(
        data=plot_df, x="语言类别", y="薪资千元",
        order=LANG_ORDER, palette=palette, inner="box",
        cut=0, ax=ax, saturation=0.85,
    )

    ax.set_xticklabels(LANG_LABELS, fontproperties=fp, fontsize=11)
    ax.set_xlabel("语言类别", fontproperties=fp, fontsize=12)
    ax.set_ylabel("月薪（千元）", fontproperties=fp, fontsize=12)
    ax.set_title("各语言类别薪资分布小提琴图", fontproperties=fp, fontsize=15)
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    _save(fig, "salary_violin.png")


# ============================================================
# 角度6: 薪资范围散点图
# ============================================================
def plot_salary_scatter(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(12, 8))
    fp = _fp()

    valid = df.dropna(subset=["最低薪资", "最高薪资", "语言类别"])
    valid = valid[valid["语言类别"].isin(LANG_ORDER)]

    for lang, color, label in zip(LANG_ORDER, LANG_COLORS, LANG_LABELS):
        subset = valid[valid["语言类别"] == lang]
        ax.scatter(
            subset["最低薪资"] / 1000, subset["最高薪资"] / 1000,
            c=color, alpha=0.35, s=20, label=label, edgecolors="none",
        )

    max_val = max(valid["最高薪资"].max() / 1000, valid["最低薪资"].max() / 1000)
    ax.plot([0, max_val], [0, max_val], "k--", alpha=0.3, linewidth=1, label="最低=最高")

    ax.set_xlabel("最低月薪（千元）", fontproperties=fp, fontsize=12)
    ax.set_ylabel("最高月薪（千元）", fontproperties=fp, fontsize=12)
    ax.set_title("薪资范围散点图（最低 vs 最高月薪）", fontproperties=fp, fontsize=15)
    ax.legend(prop=fp, fontsize=10, markerscale=2)
    ax.grid(alpha=0.2)

    plt.tight_layout()
    _save(fig, "salary_scatter.png")


# ============================================================
# 角度7: 城市语言堆叠柱状图
# ============================================================
def plot_city_lang_stacked(df: pd.DataFrame, top_n: int = 10):
    fig, ax = plt.subplots(figsize=(14, 7))
    fp = _fp()

    top_cities = df["城市"].value_counts().head(top_n).index.tolist()
    subset = df[df["城市"].isin(top_cities)]

    pivot = subset.groupby(["城市", "语言类别"]).size().reset_index(name="岗位数")
    pivot_table = pivot.pivot(index="城市", columns="语言类别", values="岗位数").fillna(0)
    city_order = sorted(top_cities, key=lambda c: pivot_table.loc[c].sum() if c in pivot_table.index else 0)
    lang_present = [l for l in LANG_ORDER if l in pivot_table.columns]
    pivot_table = pivot_table.reindex(index=city_order, columns=lang_present)

    bottom = np.zeros(len(city_order))
    for lang, color, label in zip(lang_present, LANG_COLORS, LANG_LABELS):
        vals = pivot_table[lang].values
        ax.barh(range(len(city_order)), vals, left=bottom, color=color,
                label=label, edgecolor="white", linewidth=0.5)
        bottom += vals

    ax.set_yticks(range(len(city_order)))
    ax.set_yticklabels(city_order, fontproperties=fp)
    ax.set_xlabel("岗位数量", fontproperties=fp, fontsize=12)
    ax.set_title(f"Top{top_n}城市各语言岗位堆叠柱状图", fontproperties=fp, fontsize=15)
    ax.legend(prop=fp, fontsize=10, loc="lower right")

    plt.tight_layout()
    _save(fig, "city_lang_stacked.png")


# ============================================================
# 角度8: 学历分布环形图
# ============================================================
def plot_education_donut(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(9, 9))
    fp = _fp()

    edu_counts = df["学历要求"].value_counts()
    edu_present = [e for e in EDU_ORDER if e in edu_counts.index]
    counts = [edu_counts.get(e, 0) for e in edu_present]

    colors = sns.color_palette("Set2", len(edu_present))
    wedges, texts, autotexts = ax.pie(
        counts, labels=edu_present, autopct="%1.1f%%",
        colors=colors, pctdistance=0.8,
        wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2),
    )
    for t in texts:
        t.set_fontproperties(fp)
        t.set_fontsize(11)
    for t in autotexts:
        t.set_fontsize(9)

    ax.text(0, 0, f"共{sum(counts)}个\n岗位", ha="center", va="center",
            fontproperties=fp, fontsize=16, fontweight="bold")
    ax.set_title("学历要求分布环形图", fontproperties=fp, fontsize=15)

    plt.tight_layout()
    _save(fig, "education_donut.png")


# ============================================================
# 角度9: 技能需求词云
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


# ============================================================
# 角度10: Top20技能频次
# ============================================================
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
# 角度11: 编程语言维度对比（分组柱状图）
# ============================================================
def plot_language_comparison(df: pd.DataFrame):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fp = _fp()

    lang_counts = df["语言类别"].value_counts()
    counts = [lang_counts.get(l, 0) for l in LANG_ORDER]

    ax = axes[0]
    bars = ax.bar(range(len(LANG_ORDER)), counts, color=LANG_COLORS, edgecolor="white", width=0.6)
    ax.set_xticks(range(len(LANG_ORDER)))
    ax.set_xticklabels(LANG_LABELS, fontproperties=fp, fontsize=11)
    ax.set_ylabel("岗位数量", fontproperties=fp, fontsize=12)
    ax.set_title("各语言岗位数量对比", fontproperties=fp, fontsize=14)
    for bar, val in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50,
                str(val), ha="center", fontproperties=fp, fontsize=10)

    ax = axes[1]
    avg_salaries = []
    for l in LANG_ORDER:
        avg = df[df["语言类别"] == l]["平均月薪"].mean()
        avg_salaries.append(avg if not pd.isna(avg) else 0)
    bars = ax.bar(range(len(LANG_ORDER)), [v / 1000 for v in avg_salaries],
                  color=LANG_COLORS, edgecolor="white", width=0.6)
    ax.set_xticks(range(len(LANG_ORDER)))
    ax.set_xticklabels(LANG_LABELS, fontproperties=fp, fontsize=11)
    ax.set_ylabel("平均月薪（千元）", fontproperties=fp, fontsize=12)
    ax.set_title("各语言平均薪资对比", fontproperties=fp, fontsize=14)
    for bar, val in zip(bars, avg_salaries):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                f"{val/1000:.1f}k", ha="center", fontproperties=fp, fontsize=10)

    plt.tight_layout()
    _save(fig, "language_comparison.png")


# ============================================================
# 角度12: 行业分布环形图
# ============================================================
def plot_industry_donut(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 10))
    fp = _fp()

    industry_counts = df["所属行业"].dropna().value_counts().head(12)
    colors_i = sns.color_palette("viridis", len(industry_counts))

    wedges, texts, autotexts = ax.pie(
        industry_counts.values, labels=industry_counts.index, autopct="%1.1f%%",
        colors=colors_i, pctdistance=0.8,
        wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2),
    )
    for t in texts:
        t.set_fontproperties(fp)
        t.set_fontsize(10)
    for t in autotexts:
        t.set_fontsize(8)

    ax.text(0, 0, "行业\nTop12", ha="center", va="center",
            fontproperties=fp, fontsize=16, fontweight="bold")
    ax.set_title("所属行业分布环形图", fontproperties=fp, fontsize=15)

    plt.tight_layout()
    _save(fig, "industry_donut.png")


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

    print("[1/12] 薪资分布直方图+KDE")
    plot_salary_distribution(df)

    print("[2/12] 经验级别薪资箱线图")
    plot_salary_boxplot(df)

    print("[3/12] 经验×学历薪资热力图")
    plot_exp_edu_heatmap(df)

    print("[4/12] 城市×语言类别岗位数热力图")
    plot_city_lang_heatmap(df)

    print("[5/12] 语言类别薪资小提琴图")
    plot_salary_violin(df)

    print("[6/12] 薪资范围散点图")
    plot_salary_scatter(df)

    print("[7/12] 城市语言堆叠柱状图")
    plot_city_lang_stacked(df)

    print("[8/12] 学历分布环形图")
    plot_education_donut(df)

    print("[9/12] 技能需求词云")
    plot_skill_wordcloud(df)

    print("[10/12] Top20技能频次")
    plot_top_skills(df)

    print("[11/12] 编程语言维度对比")
    plot_language_comparison(df)

    print("[12/12] 行业分布环形图")
    plot_industry_donut(df)

    print()
    print("=" * 60)
    print(f"全部图表已保存至: {CHART_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    _PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    csv_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        _PROJECT_ROOT, "data", "processed", "智联招聘java_python_C工程师_cleaned.csv"
    )
    run_all(csv_path)
