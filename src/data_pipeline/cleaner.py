"""数据清理、缺失值处理、数据变换逻辑"""

import re
import pandas as pd
import numpy as np


def load_raw_data(filepath: str) -> pd.DataFrame:
    """加载八爪鱼采集器导出的原始 CSV 数据"""
    df = pd.read_csv(filepath, encoding="utf-8")
    # 去除所有字段中的换行符和多余空白
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


def _rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """将八爪鱼默认列名映射为业务语义列名"""
    col_map = {
        df.columns[0]: "信息_链接",
        df.columns[1]: "岗位名称",
        df.columns[2]: "薪水",
        df.columns[3]: "技能关键词",
        df.columns[4]: "标签",
        df.columns[5]: "工作经验",
        df.columns[6]: "学历要求",
        df.columns[7]: "工作地点",
        df.columns[8]: "公司名称",
        df.columns[9]: "公司信息",
        df.columns[10]: "公司标签",
        df.columns[11]: "其它信息",
    }
    return df.rename(columns=col_map)


def _extract_salary(df: pd.DataFrame) -> pd.DataFrame:
    """从薪水字段提取数值信息：最低薪、最高薪、单位、薪数"""

    def parse(s):
        if pd.isna(s) or str(s).strip() == "":
            return np.nan, np.nan, np.nan, np.nan

        s = str(s).strip()

        # 提取月数 (如 13薪, 14薪)
        months_match = re.search(r"(\d+)\s*薪", s)
        months = float(months_match.group(1)) if months_match else 12.0

        # 提取单位：万 or 元
        unit = "万" if "万" in s else "元"

        # 提取数字范围
        nums = re.findall(r"[\d.]+", s)
        if len(nums) >= 2:
            lo, hi = float(nums[0]), float(nums[1])
        elif len(nums) == 1:
            lo = hi = float(nums[0])
        else:
            return np.nan, np.nan, np.nan, np.nan

        return lo, hi, unit, months

    parsed = df["薪水"].apply(parse).apply(pd.Series)
    parsed.columns = ["最低薪资", "最高薪资", "薪资单位", "年薪月数"]
    df = pd.concat([df, parsed], axis=1)

    # 统一换算为 元/月
    mask_w = df["薪资单位"] == "万"
    df.loc[mask_w, "最低薪资"] = df.loc[mask_w, "最低薪资"] * 10000
    df.loc[mask_w, "最高薪资"] = df.loc[mask_w, "最高薪资"] * 10000
    df["平均月薪"] = (df["最低薪资"] + df["最高薪资"]) / 2

    return df


def _parse_company_info(df: pd.DataFrame) -> pd.DataFrame:
    """将公司信息字段拆分为：公司类型、公司规模、所属行业"""
    type_map = {
        "民营": "民营",
        "国企": "国企",
        "股份制企业": "股份制",
        "上市公司": "上市公司",
        "合资": "合资",
        "外商独资": "外商独资",
        "其它": "其它",
    }

    def parse(info):
        if pd.isna(info):
            return np.nan, np.nan, np.nan
        parts = str(info).strip().split()
        ctype = np.nan
        csize = np.nan
        industry = np.nan
        for p in parts:
            if p in type_map:
                ctype = type_map[p]
            elif "人" in p:
                csize = p
            else:
                industry = p
        # 补充：有些企业类型的变体
        if pd.isna(ctype):
            for k, v in type_map.items():
                if k in str(info):
                    ctype = v
                    break
        return ctype, csize, industry

    parsed = df["公司信息"].apply(parse).apply(pd.Series)
    parsed.columns = ["公司类型", "公司规模", "所属行业"]
    return pd.concat([df, parsed], axis=1)


def _parse_location(df: pd.DataFrame) -> pd.DataFrame:
    """从工作地点字段拆分城市和区域"""

    def parse(loc):
        if pd.isna(loc):
            return np.nan, np.nan
        parts = str(loc).replace("·", " ").split()
        city = parts[0] if len(parts) > 0 else np.nan
        district = parts[1] if len(parts) > 1 else np.nan
        return city, district

    parsed = df["工作地点"].apply(parse).apply(pd.Series)
    parsed.columns = ["城市", "区域"]
    return pd.concat([df, parsed], axis=1)


def _standardize_experience(df: pd.DataFrame) -> pd.DataFrame:
    """标准化工作经验字段"""
    exp_order = ["经验不限", "1年以下", "1-3年", "3-5年", "5-10年", "10年以上"]
    df["工作经验"] = pd.Categorical(df["工作经验"], categories=exp_order, ordered=True)
    return df


def _standardize_education(df: pd.DataFrame) -> pd.DataFrame:
    """标准化学历要求字段"""
    edu_order = ["学历不限", "中专/中技", "大专", "本科", "硕士", "博士"]
    df["学历要求"] = pd.Categorical(df["学历要求"], categories=edu_order, ordered=True)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """执行完整数据清洗流程"""
    df = _rename_columns(df)
    df.replace("nan", pd.NA, inplace=True)
    df = _extract_salary(df)
    df = _parse_company_info(df)
    df = _parse_location(df)
    df = _standardize_experience(df)
    df = _standardize_education(df)
    # 去除薪资异常值：月薪低于500或高于20万的视为异常
    df = df[(df["平均月薪"] >= 500) & (df["平均月薪"] <= 200000)]
    return df


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """数据变换与规约 —— 当前返回完整清洗结果，后续可按需生成聚合表"""
    return df


def save_processed(df: pd.DataFrame, output_path: str):
    """保存清洗后的数据到 CSV"""
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"已保存清洗数据至: {output_path}")
    print(f"数据维度: {df.shape}")
