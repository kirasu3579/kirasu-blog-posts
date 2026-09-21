from datetime import datetime
import re
import os


def add_yaml_header(file_path: str, category: str, tag: str):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    stripped = content.lstrip()
    if stripped.startswith("---"):
        print(f"【跳过】{file_path} 已经存在YAML头部，无需处理")
        return

    # 提取文章标题
    title_match = re.search(r'^#{1,3}\s+(.*?)(\n|$)', content, flags=re.MULTILINE)
    if title_match:
        article_title = title_match.group(1).strip()
    else:
        article_title = os.path.splitext(os.path.basename(file_path))[0]

    now_date = datetime.now().strftime("%Y-%m-%d")

    yaml_header = f"""---
title: "{article_title}"
date: {now_date}
post_status: publish
comment_status: open
taxonomy:
  category:
    - {category}
  post_tag:
    - {tag}
---

"""
    new_content = yaml_header + content

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"【成功】已添加YAML头部")
    print(f"title: {article_title} | category: {category} | tag: {tag}\n")


if __name__ == "__main__":
    print("==== Markdown博客YAML头部自动补全工具 ====")
    md_path = input("请输入md文件完整路径（直接拖入文件也可以）：").strip()

    # 校验文件
    if not os.path.isfile(md_path):
        print("错误：文件不存在！")
        exit(1)
    if not md_path.lower().endswith(".md"):
        print("错误：不是md文件！")
        exit(1)

    # category交互：默认计算机，询问是否使用默认
    default_cat = "计算机"
    use_default_cat = input(f"分类category，默认值【{default_cat}】，是否使用默认？(y/n): ").strip().lower()
    if use_default_cat == "y":
        cat_val = default_cat
    else:
        cat_val = input("请输入自定义category分类：").strip()
        if not cat_val:
            print("分类不能为空！")
            exit(1)

    # tag：必须手动录入，无默认
    tag_val = input("请输入post_tag标签（必填，无默认）：").strip()
    if not tag_val:
        print("标签tag不能为空！")
        exit(1)

    add_yaml_header(md_path, category=cat_val, tag=tag_val)
