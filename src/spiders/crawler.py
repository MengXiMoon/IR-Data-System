"""基于 Scrapling 的通用爬虫 —— 提取结构化数据并导出 CSV"""

import csv
from pathlib import Path
from scrapling import Fetcher


class CsvWriter:
    """CSV 写入器，支持逐行追加"""

    def __init__(self, filepath: str, fieldnames: list[str]):
        self.filepath = Path(filepath)
        self.fieldnames = fieldnames
        self._file = open(self.filepath, "w", newline="", encoding="utf-8-sig")
        self._writer = csv.DictWriter(self._file, fieldnames=fieldnames)
        self._writer.writeheader()

    def write_row(self, row: dict):
        self._writer.writerow(row)
        self._file.flush()

    def close(self):
        self._file.close()


def parse_items(page, container_sel: str, field_selectors: dict,
                join_sep: str = " / ") -> list[dict]:
    """在容器内提取字段。

    field_selectors 的 value 可以是:
      - str: 普通 CSS 选择器，多匹配自动拼接
      - (str, int): (选择器, 索引)，取第 N 个匹配（0-based）
      - (str, str): (选择器, 属性名)，取第一个匹配的 HTML 属性值
    """
    containers = page.css(container_sel)
    items = []

    for c in containers:
        item = {}
        for field, spec in field_selectors.items():
            if isinstance(spec, tuple):
                sel, arg = spec
                els = c.css(sel)
                if isinstance(arg, int):
                    item[field] = els[arg].text.strip() if arg < len(els) else ""
                else:
                    item[field] = els[0].attrib.get(arg, "") if els else ""
            else:
                els = c.css(spec)
                if not els:
                    item[field] = ""
                elif len(els) == 1:
                    item[field] = els[0].text.strip()
                else:
                    texts = [el.text.strip() for el in els if el.text.strip()]
                    item[field] = join_sep.join(texts)
        items.append(item)

    return items


def crawl_pages(base_url: str, container_sel: str, field_selectors: dict,
                cities: list[str] | None = None,
                city_names: dict[str, str] | None = None,
                city_field: str = "城市",
                start: int = 1, end: int = 5,
                csv_path: str = "output.csv") -> int:
    """多城市翻页爬取，结果追加写入同一个 CSV，返回总条数。

    base_url 中用 {city} 和 {page} 占位。
    city_names 将城市编码映射为中文名，如 {"530": "北京"}。"""
    total = 0
    writer = None
    f = Fetcher()
    city_list = cities or [""]
    name_map = city_names or {}
    all_fields = list(field_selectors.keys())

    for city_code in city_list:
        city_name = name_map.get(city_code, city_code)
        prev_links: set[str] = set()
        dup_break = False
        empty_streak = 0        # 连续空页计数

        for p in range(start, end + 1):
            url = base_url.format(city=city_code, page=p)
            items = []
            # 空页重试最多 3 次，排除网络抖动 / 临时反爬
            for attempt in range(1, 4):
                print(f"[{city_name} / 第 {p} 页] 正在抓取...", end="")
                if attempt > 1:
                    print(f" (重试 {attempt - 1}/3)", end="")
                print()
                page = f.get(url)
                items = parse_items(page, container_sel, field_selectors)
                print(f"  -> 提取到 {len(items)} 条")
                if items:
                    break

            if not items:
                empty_streak += 1
                print(f"  [{city_name}] 第 {p} 页无数据 (连续 {empty_streak} 页)")
                if empty_streak >= 3:
                    print(f"  [{city_name}] 连续 3 页无数据，切换到下一城市")
                    break
                continue
            empty_streak = 0

            # 用所有职位链接（唯一 URL）判断整页是否重复
            cur_links = {it.get("职位链接", "") for it in items}
            if cur_links and cur_links == prev_links:
                print(f"  [{city_name}] 第 {p} 页与上页完全重复，已到末页，切换到下一城市")
                dup_break = True
                break
            prev_links = cur_links

            if writer is None:
                writer = CsvWriter(csv_path, [city_field] + all_fields)

            for item in items:
                item[city_field] = city_name
                writer.write_row(item)
            total += len(items)

        if not dup_break and prev_links:
            print(f"  [{city_name}] 爬完 {end} 页，可能未到末页")

    if writer:
        writer.close()
    print(f"\n总计 {total} 条数据，已保存到 {csv_path}")
    return total


# ── 配置区 ──────────────────────────────────────────────
CONTAINER_SEL = ".joblist-box__iteminfo"

FIELD_SELECTORS = {
    "职位名称": ".jobinfo__name",
    "职位链接": (".jobinfo__name", "href"),
    "公司名称": ".companyinfo__name",
    "企业类型": (".companyinfo__tag .joblist-box__item-tag", 0),
    "公司人数": (".companyinfo__tag .joblist-box__item-tag", 1),
    "行业领域": (".companyinfo__tag .joblist-box__item-tag", 2),
    "技术要求": ".jobinfo__tag .joblist-box__item-tag",
    "薪资": ".jobinfo__salary",
    "地区": ".jobinfo__other-info-item span",
    "工作经验": (".jobinfo__other-info-item", 1),
    "学历要求": (".jobinfo__other-info-item", 2),
}

CITY_MAP = {
    "530": "北京", "538": "上海", "763": "广州", "765": "深圳",
    "531": "天津", "736": "武汉", "854": "西安", "801": "成都",
    "600": "大连", "613": "长春", "599": "沈阳", "635": "南京",
    "702": "济南", "703": "青岛", "653": "杭州", "639": "苏州",
    "636": "无锡", "654": "宁波", "551": "重庆", "719": "郑州",
    "749": "长沙", "681": "福州", "682": "厦门", "622": "哈尔滨",
}

BASE_URL = "https://www.zhaopin.com/sou/jl{city}/kw01L00O80EO062/p{page}"
START_PAGE = 1
END_PAGE = 26
CSV_PATH = "java.csv"


def main():
    total = crawl_pages(
        BASE_URL,
        CONTAINER_SEL,
        FIELD_SELECTORS,
        cities=list(CITY_MAP.keys()),
        city_names=CITY_MAP,
        start=START_PAGE,
        end=END_PAGE,
        csv_path=CSV_PATH,
    )
    print(f"完成，共 {total} 条")


if __name__ == "__main__":
    main()
