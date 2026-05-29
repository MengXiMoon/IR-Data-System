"""Java/Python/C/C++ 工程师招聘数据清洗脚本

可视化角度设计（至少5个）:
  1. 薪资分布 —— 整体薪资直方图 + 不同经验级别薪资箱线图
  2. 城市地域分布 —— Top15城市岗位数量 + 热门城市区域分布
  3. 企业类型与规模 —— 企业类型饼图 + 企业规模柱状图
  4. 学历要求与经验要求 —— 学历分布 + 工作经验分布
  5. 技能需求热词 —— 技能关键词词云 + Top20技能频次
  6. 行业分布 —— 所属行业 Top12 饼图
  7. 薪资与学历交叉分析 —— 不同学历平均薪资柱状图
  8. 编程语言维度对比 —— Java/Python/C_C++ 岗位数/薪资对比
"""

import re
import pandas as pd
import numpy as np


LEGIT_COMPANY_TYPES = {
    "合资", "民营", "外商独资", "上市公司", "其它", "国企",
    "股份制企业", "事业单位", "港澳台公司", "社会团体",
    "代表处", "国家机关", "银行",
}

TYPE_NORMALIZE_MAP = {
    "股份制 企业": "股份制",
    "股份制企业": "股份制",
    "20人以下": np.nan,
    "20-99人": np.nan,
    "100-299人": np.nan,
    "300-499人": np.nan,
    "500-999人": np.nan,
    "1000-9999人": np.nan,
    "10000人以上": np.nan,
}

EXP_ORDER = ["经验不限", "1年以下", "1-3年", "3-5年", "5-10年", "10年以上"]
EDU_ORDER = ["学历不限", "初中及以下", "高中", "中专/中技", "大专", "本科", "硕士", "博士"]
SIZE_ORDER = [
    "20人以下", "20-99人", "100-299人", "300-499人",
    "500-999人", "1000-9999人", "10000人以上",
]


def load_raw_data(filepath: str) -> pd.DataFrame:
    """加载原始 CSV 数据并清理换行符和多余空白"""
    df = pd.read_csv(filepath, encoding="utf-8")
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.replace(r"[\n\r]+", " ", regex=True)
                .str.replace(r"\s+", " ", regex=True)
            )
    return df


def _fix_shifted_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    修复列偏移问题:
    部分行中，企业类型列存的是公司人数，公司人数列存的是行业领域，行业领域为 NaN。
    通过检测 企业类型 是否包含 "人" 来识别偏移行，将其数据归位。
    """
    shifted_mask = (
        df["企业类型"].apply(lambda x: "人" in str(x) if pd.notna(x) else False)
    )

    fixed_count = shifted_mask.sum()
    if fixed_count > 0:
        df.loc[shifted_mask, "行业领域"] = df.loc[shifted_mask, "公司人数"]
        df.loc[shifted_mask, "公司人数"] = df.loc[shifted_mask, "企业类型"]
        df.loc[shifted_mask, "企业类型"] = np.nan
        print(f"  修复列偏移行数: {fixed_count}")

    return df


def _clean_company_type(df: pd.DataFrame) -> pd.DataFrame:
    """清洗企业类型字段 —— 只保留合法类型值，其余置 NaN"""
    df["企业类型"] = df["企业类型"].replace(TYPE_NORMALIZE_MAP)
    df["企业类型"] = df["企业类型"].replace("nan", np.nan)

    def is_valid(t):
        if pd.isna(t):
            return True
        return str(t) in LEGIT_COMPANY_TYPES.union({"股份制"})

    df.loc[~df["企业类型"].apply(is_valid), "企业类型"] = np.nan
    return df


def _clean_company_size(df: pd.DataFrame) -> pd.DataFrame:
    """清洗公司人数字段 —— 只保留含'人'的有效值"""
    df["公司人数"] = df["公司人数"].apply(
        lambda x: x if pd.notna(x) and isinstance(x, str) and "人" in x else np.nan
    )
    return df


def _extract_salary(df: pd.DataFrame) -> pd.DataFrame:
    """从薪资字段提取数值信息"""

    def parse(s):
        if pd.isna(s) or str(s).strip() in ("", "nan", "面议"):
            return np.nan, np.nan, np.nan, np.nan

        s = str(s).strip()

        months_match = re.search(r"(\d+)\s*薪", s)
        months = float(months_match.group(1)) if months_match else 12.0

        unit = "万" if "万" in s else "元"

        nums = re.findall(r"[\d.]+", s)
        if len(nums) >= 2:
            lo, hi = float(nums[0]), float(nums[1])
        elif len(nums) == 1:
            lo = hi = float(nums[0])
        else:
            return np.nan, np.nan, np.nan, np.nan

        return lo, hi, unit, months

    parsed = df["薪资"].apply(parse).apply(pd.Series)
    parsed.columns = ["最低薪资", "最高薪资", "薪资单位", "年薪月数"]
    df = pd.concat([df, parsed], axis=1)

    mask_w = df["薪资单位"] == "万"
    df.loc[mask_w, "最低薪资"] = df.loc[mask_w, "最低薪资"] * 10000
    df.loc[mask_w, "最高薪资"] = df.loc[mask_w, "最高薪资"] * 10000
    df["平均月薪"] = (df["最低薪资"] + df["最高薪资"]) / 2

    return df


def _parse_location(df: pd.DataFrame) -> pd.DataFrame:
    """从地区字段拆分城市和区域"""
    def parse(loc):
        if pd.isna(loc) or str(loc).strip() == "nan":
            return np.nan, np.nan
        parts = str(loc).replace("\u00b7", " ").split()
        city = parts[0] if len(parts) > 0 else np.nan
        district = parts[1] if len(parts) > 1 else np.nan
        return city, district

    parsed = df["地区"].apply(parse).apply(pd.Series)
    parsed.columns = ["解析城市", "解析区域"]
    df = pd.concat([df, parsed], axis=1)

    df["城市"] = df["城市"].fillna(df["解析城市"])
    df["区域"] = df["解析区域"]
    df.drop(columns=["解析城市", "解析区域"], inplace=True)

    return df


def _extract_tag(df: pd.DataFrame) -> pd.DataFrame:
    """从技术要求中提取第一个有意义的词作为标签"""
    NOISE_WORDS = {
        "不限语言和经验", "不限", "经验不限", "开发经验",
        "岗位职责", "任职要求", "技术要求", "职位描述",
        "周末双休", "五险一金", "六险一金", "年终奖", "双休",
    }

    def first_tag(s):
        if pd.isna(s) or str(s).strip() in ("", "nan"):
            return np.nan
        parts = str(s).strip().split()
        for p in parts:
            p_clean = p.strip("/,").strip("()[]{}（）")
            if (
                len(p_clean) > 1
                and not p_clean.isdigit()
                and p_clean not in NOISE_WORDS
                and p_clean != "经验"
            ):
                return p_clean
        return np.nan

    df["标签"] = df["技术要求"].apply(first_tag)
    return df


def _categorize_language(df: pd.DataFrame) -> pd.DataFrame:
    """根据职位名称和技术要求，将岗位归类为 Java / Python / C_C++ / 其他"""

    def classify(row):
        name = str(row["职位名称"]) if pd.notna(row["职位名称"]) else ""
        skills = str(row["技术要求"]) if pd.notna(row["技术要求"]) else ""
        combined = (name + " " + skills).lower()

        has_java = bool(re.search(r"\bjava\b", combined, re.IGNORECASE))
        has_python = bool(re.search(r"\bpython\b", combined, re.IGNORECASE))
        has_c = bool(re.search(
            r"\bc\+\+|\bc/c\+\+|\bcnn\b|\bc语言\b|\bc\b",
            combined, re.IGNORECASE
        ))

        langs = []
        if has_java:
            langs.append("Java")
        if has_python:
            langs.append("Python")
        if has_c:
            langs.append("C_C++")

        if len(langs) == 0:
            return "其他"
        elif len(langs) == 1:
            return langs[0]
        else:
            return "多语言"

    df["语言类别"] = df.apply(classify, axis=1)
    return df


def _standardize_experience(df: pd.DataFrame) -> pd.DataFrame:
    df["工作经验"] = pd.Categorical(
        df["工作经验"], categories=EXP_ORDER, ordered=True
    )
    return df


def _standardize_education(df: pd.DataFrame) -> pd.DataFrame:
    df["学历要求"] = pd.Categorical(
        df["学历要求"], categories=EDU_ORDER, ordered=True
    )
    return df


def _build_output_columns(df: pd.DataFrame) -> pd.DataFrame:
    """映射为与项目现有清洗结果一致的列结构"""
    df["信息_链接"] = df["职位链接"]
    df["岗位名称"] = df["职位名称"]
    df["薪水"] = df["薪资"]
    df["技能关键词"] = df["技术要求"]
    df["工作地点"] = df["地区"]
    df["公司名称"] = df["公司名称"]
    df["公司类型"] = df["企业类型"]
    df["公司规模"] = df["公司人数"]
    df["所属行业"] = df["行业领域"]

    output_cols = [
        "信息_链接", "岗位名称", "薪水", "技能关键词", "标签",
        "工作经验", "学历要求", "工作地点", "公司名称",
        "公司信息", "公司标签", "其它信息",
        "最低薪资", "最高薪资", "薪资单位", "年薪月数", "平均月薪",
        "公司类型", "公司规模", "所属行业",
        "城市", "区域",
        "语言类别",
    ]

    missing_cols = [c for c in output_cols if c not in df.columns]
    for c in missing_cols:
        df[c] = np.nan

    return df[output_cols]


def _deduplicate_by_url(df: pd.DataFrame) -> pd.DataFrame:
    """根据职位链接（URL）去重 —— 相同URL视为同一岗位，保留首次出现的记录"""
    before = len(df)
    df = df.drop_duplicates(subset=["职位链接"], keep="first")
    after = len(df)
    removed = before - after
    if removed > 0:
        print(f"  基于职位链接去重，删除重复行: {removed} 行")
    else:
        print(f"  未发现基于职位链接的重复数据")
    return df


def clean_data(filepath: str) -> pd.DataFrame:
    """执行完整数据清洗流程"""
    print("=" * 60)
    print("Java/Python/C/C++ 工程师招聘数据清洗")
    print("=" * 60)

    print(f"\n[1/9] 加载原始数据: {filepath}")
    df = load_raw_data(filepath)
    print(f"  原始维度: {df.shape}")

    print("\n[2/9] 基于职位链接(URL)去重")
    df = _deduplicate_by_url(df)

    print("\n[3/9] 修复列偏移")
    df = _fix_shifted_rows(df)

    print("\n[4/9] 清洗企业类型与公司规模")
    df = _clean_company_type(df)
    df = _clean_company_size(df)

    print("\n[5/9] 解析薪资 (含面议过滤)")
    before = len(df)
    df = _extract_salary(df)
    df = df[(df["平均月薪"] >= 500) & (df["平均月薪"] <= 200000)]
    after = len(df)
    print(f"  薪资过滤掉: {before - after} 行 (含面议/异常值)")

    print("\n[6/9] 解析地区 -> 城市/区域")
    df = _parse_location(df)

    print("\n[7/9] 提取标签 + 编程语言归类")
    df = _extract_tag(df)
    df = _categorize_language(df)

    print("\n[8/9] 标准化工作经验与学历要求")
    df = _standardize_experience(df)
    df = _standardize_education(df)

    print("\n[9/9] 构建输出列")
    df = _build_output_columns(df)
    print(f"  最终维度: {df.shape}")

    print("\n" + "=" * 60)
    print("数据清洗完成!")
    print("=" * 60)
    _print_summary(df)

    return df


def _print_summary(df: pd.DataFrame):
    """输出数据概览"""
    print(f"\n--- 数据概览 ---")
    print(f"  总岗位数: {len(df)}")
    print(f"  有效薪资岗位数: {df['平均月薪'].notna().sum()}")
    print(f"  平均月薪: {df['平均月薪'].mean():.0f} 元")
    print(f"  薪资中位数: {df['平均月薪'].median():.0f} 元")
    print(f"  涉及城市数: {df['城市'].nunique()}")

    print(f"\n  语言类别分布:")
    for lang, cnt in df["语言类别"].value_counts().items():
        avg_sal = df[df["语言类别"] == lang]["平均月薪"].mean()
        print(f"    {lang}: {cnt} 岗位, 平均月薪 {avg_sal:.0f} 元")

    print(f"\n  工作经验分布:")
    for exp in EXP_ORDER:
        cnt = (df["工作经验"] == exp).sum()
        if cnt > 0:
            print(f"    {exp}: {cnt}")

    print(f"\n  学历要求分布:")
    for edu in EDU_ORDER:
        cnt = (df["学历要求"] == edu).sum()
        if cnt > 0:
            print(f"    {edu}: {cnt}")


def save_processed(df: pd.DataFrame, output_path: str):
    """保存清洗结果"""
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"\n已保存: {output_path}")
    print(f"维度: {df.shape}")


if __name__ == "__main__":
    import sys

    input_path = sys.argv[1] if len(sys.argv) > 1 else (
        r"e:\ExploreDownloads\福州大学至诚学院\智能应用开发课程设计\IR-Data-System\data\raw\智联招聘java、python、C工程师.csv"
    )
    output_path = sys.argv[2] if len(sys.argv) > 2 else (
        r"e:\ExploreDownloads\福州大学至诚学院\智能应用开发课程设计\IR-Data-System\data\processed\智联招聘java_python_C工程师_cleaned.csv"
    )

    result = clean_data(input_path)
    save_processed(result, output_path)
