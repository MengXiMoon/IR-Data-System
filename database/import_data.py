"""将清洗后的 CSV 数据导入 MySQL"""

import os
import pandas as pd
import pymysql

# 列名映射: CSV列名 → job_listing 字段名
COLUMN_MAP = {
    "信息_链接": "source_url",
    "岗位名称": "job_title",
    "薪水": "salary_raw",
    "技能关键词": "skills_raw",
    "标签": "tag",
    "工作经验": "experience",
    "学历要求": "education",
    "工作地点": "work_location",
    "公司名称": "company_name",
    "公司信息": "company_info",
    "公司标签": "company_tag",
    "其它信息": "extra_info",
    "最低薪资": "salary_min",
    "最高薪资": "salary_max",
    "薪资单位": "salary_unit",
    "年薪月数": "salary_months",
    "平均月薪": "salary_avg",
    "公司类型": "company_type",
    "公司规模": "company_size",
    "所属行业": "industry",
    "城市": "city",
    "区域": "district",
    "数据来源": "source",
}


def import_csv_to_mysql(csv_path: str):
    """读取 CSV 并逐行插入 MySQL"""
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    # 重命名列
    df.rename(columns=COLUMN_MAP, inplace=True)
    # 只保留 CSV 中实际存在的列
    columns = [v for k, v in COLUMN_MAP.items() if v in df.columns]
    df = df[columns]

    conn = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password=os.environ.get("DB_PASSWORD", "123456"),
        database="recruitment_ai",
        charset="utf8mb4",
    )
    cursor = conn.cursor()

    placeholders = ", ".join(["%s"] * len(columns))
    sql = f"INSERT INTO job_listing ({', '.join(columns)}) VALUES ({placeholders})"

    # 构建行列表，处理 NaN → None
    rows = []
    for row in df.itertuples(index=False):
        clean = []
        for v in row:
            if pd.isna(v):
                clean.append(None)
            else:
                clean.append(v)
        rows.append(tuple(clean))
    cursor.executemany(sql, rows)
    conn.commit()

    print(f"导入完成: {cursor.rowcount} 条记录")
    cursor.close()
    conn.close()


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    csv_path = os.path.join(project_root, "data", "processed", "智联招聘java_python_C工程师_cleaned.csv")
    import_csv_to_mysql(csv_path)
