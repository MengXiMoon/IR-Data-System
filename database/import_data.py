"""将清洗后的 CSV 数据导入 MySQL"""

import getpass
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
}


def import_csv_to_mysql(csv_path: str):
    """读取 CSV 并逐行插入 MySQL"""
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    df = df.where(pd.notna(df), None)  # NaN → None → SQL NULL

    # 重命名列
    df.rename(columns=COLUMN_MAP, inplace=True)
    columns = list(COLUMN_MAP.values())
    df = df[columns]

    conn = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password=getpass.getpass("MySQL root 密码: "),
        database="recruitment_ai",
        charset="utf8mb4",
    )
    cursor = conn.cursor()

    placeholders = ", ".join(["%s"] * len(columns))
    sql = f"INSERT INTO job_listing ({', '.join(columns)}) VALUES ({placeholders})"

    rows = [tuple(row) for row in df.itertuples(index=False)]
    cursor.executemany(sql, rows)
    conn.commit()

    print(f"导入完成: {cursor.rowcount} 条记录")
    cursor.close()
    conn.close()


if __name__ == "__main__":
    csv_path = "../data/processed/智联招聘python工程师_cleaned.csv"
    import_csv_to_mysql(csv_path)
