import os
from yaml_add_header import add_yaml_header

if __name__ == "__main__":
    print("==== 批量MD文件YAML补全工具【当前目录】 ====")
    # 直接取脚本运行的当前目录
    folder = os.getcwd()
    print(f"当前处理目录：{folder}")

    file_list = [f for f in os.listdir(folder) if f.lower().endswith(".md") and os.path.isfile(os.path.join(folder, f))]
    if len(file_list) == 0:
        print("当前文件夹下没有找到md文件，程序退出。")
        exit(0)

    print(f"共找到 {len(file_list)} 个md文件\n")

    mode = input("请选择处理模式：\n[A]全部文件共用一套分类标签(只输入一次)\n[B]每个文件单独输入分类标签\n请输入A/B：").strip().upper()

    if mode == "A":
        # 全局统一一套cat/tag
        default_cat = "计算机"
        use_default_cat = input(f"分类category，默认值【{default_cat}】，是否使用默认？(y/n): ").strip().lower()
        if use_default_cat == "y":
            cat_val = default_cat
        else:
            cat_val = input("请输入自定义category分类：").strip()
            if not cat_val:
                print("分类不能为空，程序退出")
                exit(1)

        tag_val = input("请输入post_tag标签（必填，无默认）：").strip()
        if not tag_val:
            print("tag不能为空，程序退出")
            exit(1)

        print(f"\n>>> 全局设置：category={cat_val}, tag={tag_val}，开始批量处理\n")
        for filename in file_list:
            full_path = os.path.join(folder, filename)
            print(f"处理文件：{filename}")
            add_yaml_header(full_path, cat_val, tag_val)

    elif mode == "B":
        # 逐个文件输入
        for filename in file_list:
            full_path = os.path.join(folder, filename)
            print(f"\n>>> 当前处理文件：{filename}")

            default_cat = "计算机"
            use_default_cat = input(f"分类category，默认值【{default_cat}】，是否使用默认？(y/n): ").strip().lower()
            if use_default_cat == "y":
                cat_val = default_cat
            else:
                cat_val = input("请输入自定义category分类：").strip()
                if not cat_val:
                    print("分类为空，跳过该文件")
                    continue

            tag_val = input("请输入post_tag标签（必填，无默认）：").strip()
            if not tag_val:
                print("tag为空，跳过该文件")
                continue

            add_yaml_header(full_path, cat_val, tag_val)
    else:
        print("输入无效，程序退出")
        exit(1)

    print("\n==== 全部任务处理完成 ====")
