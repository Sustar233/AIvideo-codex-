# -*- coding: utf-8 -*-
"""
《琥珀之城》剧本分析结果解析器
用法：将网页版 AI 的输出全文贴到 stdin，此脚本解析后自动更新数据库
"""

import json, os, sys, re
sys.stdout.reconfigure(encoding="utf-8")

DB = "C:\\Users\\83763\\Desktop\\AIvideo\\剧本文件夹\\database"

def load_json(path):
    with open(path, "rb") as f:
        raw = f.read()
    while raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    return json.loads(raw.decode("utf-8"))

def save_json(path, data):
    txt = json.dumps(data, ensure_ascii=False, indent=2)
    with open(path, "wb") as f:
        f.write(txt.encode("utf-8"))

def extract_section(text, header):
    """Extract content between section headers"""
    pattern = rf"={70,}\s*##\s*{re.escape(header)}.*?\n(.*?)(?=\n={70,}|\Z)"
    m = re.search(pattern, text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return ""

def parse_answer(text):
    report = []

    # 1. 分集剧情
    sec1 = extract_section(text, "1\\.")
    m = re.search(r"\{.*\}", sec1, re.DOTALL)
    if m:
        try:
            ep_data = json.loads(m.group())
            eps = load_json(os.path.join(DB, "分集剧情.json"))
            eps["集数"].append(ep_data)
            save_json(os.path.join(DB, "分集剧情.json"), eps)
            report.append(f"分集剧情: 第{ep_data['ep']}集已添加")
        except:
            report.append("分集剧情: 解析失败")

    # 2. 现有角色更新
    sec2 = extract_section(text, "2\\.")
    updates = {}
    for line in sec2.split("\n"):
        line = line.strip()
        if "：" in line:
            name, desc = line.split("：", 1)
            updates[name] = desc
    if updates:
        chars = load_json(os.path.join(DB, "角色.json"))
        for c in chars:
            key = f"第{_get_ep(sec1)}集表现"
            if c["name"] in updates:
                c[key] = updates[c["name"]]
        save_json(os.path.join(DB, "角色.json"), chars)
        report.append(f"角色更新: {list(updates.keys())}")

    # 3. 新角色
    sec3 = extract_section(text, "3\\.")
    if sec3 and sec3 != "无":
        chars = load_json(os.path.join(DB, "角色.json"))
        added = 0
        for line in sec3.split("\n"):
            line = line.strip()
            if not line or "|" not in line:
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                new_char = {
                    "name": parts[0],
                    "性别": parts[1] if len(parts) > 1 else "",
                    "外貌": parts[2] if len(parts) > 2 else "",
                    "身份": parts[3] if len(parts) > 3 else "",
                    "性格": parts[4] if len(parts) > 4 else "",
                    "武器": parts[5] if len(parts) > 5 else "",
                    "本集表现": parts[6] if len(parts) > 6 else "",
                    "首次出现": f"第{_get_ep(sec1)}集",
                    "备注": parts[7] if len(parts) > 7 else ""
                }
                if not any(c["name"] == new_char["name"] for c in chars):
                    chars.append(new_char)
                    added += 1
        save_json(os.path.join(DB, "角色.json"), chars)
        report.append(f"新增角色: {added}")

    # 4. 新场景
    sec4 = extract_section(text, "4\\.")
    if sec4 and sec4 != "无":
        scens = load_json(os.path.join(DB, "场景.json"))
        added = 0
        for line in sec4.split("\n"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 2:
                new_scene = {
                    "name": parts[0],
                    "描述": parts[1] if len(parts) > 1 else "",
                    "时间": parts[2] if len(parts) > 2 else "",
                    "光影": parts[3] if len(parts) > 3 else "",
                    "关键道具": parts[4] if len(parts) > 4 else "",
                    "首次出现": f"第{_get_ep(sec1)}集"
                }
                if not any(s["name"] == new_scene["name"] for s in scens):
                    scens.append(new_scene)
                    added += 1
        save_json(os.path.join(DB, "场景.json"), scens)
        report.append(f"新增场景: {added}")

    # 5. 新凶兽
    sec5 = extract_section(text, "5\\.")
    if sec5 and sec5 != "无":
        beasts = load_json(os.path.join(DB, "外星凶兽.json"))
        added = 0
        for line in sec5.split("\n"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 2:
                new_beast = {
                    "name": parts[0],
                    "描述": parts[1] if len(parts) > 1 else "",
                    "特性": parts[2] if len(parts) > 2 else "",
                    "本集表现": parts[3] if len(parts) > 3 else "",
                    "首次出现": f"第{_get_ep(sec1)}集"
                }
                if not any(b["name"] == new_beast["name"] for b in beasts):
                    beasts.append(new_beast)
                    added += 1
        save_json(os.path.join(DB, "外星凶兽.json"), beasts)
        report.append(f"新增凶兽: {added}")

    # 6. 新道具
    sec6 = extract_section(text, "6\\.")
    if sec6 and sec6 != "无":
        props = load_json(os.path.join(DB, "关键道具与制度.json"))
        added = 0
        for line in sec6.split("\n"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                entry = {
                    "类型": parts[1],
                    "描述": parts[2],
                    "首次出现": f"第{_get_ep(sec1)}集"
                }
                if len(parts) > 3 and parts[3]:
                    entry["持有者"] = parts[3]
                if parts[0] not in props:
                    props[parts[0]] = entry
                    added += 1
        save_json(os.path.join(DB, "关键道具与制度.json"), props)
        report.append(f"新增道具/制度: {added}")

    # 7. 剧情梗概
    sec7 = extract_section(text, "7\\.")
    if sec7 and sec7 != "无" and len(sec7) > 5:
        outline = load_json(os.path.join(DB, "剧情梗概.json"))
        outline["关键剧情节点"].append(sec7.strip())
        save_json(os.path.join(DB, "剧情梗概.json"), outline)
        report.append("剧情梗概: 已追加")

    # 8. 人设提示词 (保存到文件)
    sec8 = extract_section(text, "8\\.")
    if sec8 and sec8 != "不需要":
        prompt_path = "C:\\Users\\83763\\Desktop\\AIvideo\\剧本文件夹\\人设提示词.md"
        with open(prompt_path, "w", encoding="utf-8") as f:
            f.write(f"# 人设提示词 — 第{_get_ep(sec1)}集\n")
            f.write("# 注意：此文件只保留最新提示词，旧版已存入用户资产库\n\n")
            f.write(sec8)
        report.append("人设提示词: 已写入")

    # 9. 保存原始剧本
    sec9 = extract_section(text, "9\\.")
    if sec9 and len(sec9) > 50:
        script_dir = "C:\\Users\\83763\\Desktop\\AIvideo\\剧本文件夹"
        ep_num = _get_ep(sec1)
        fname = f"第{ep_num}集.txt"
        with open(os.path.join(script_dir, fname), "w", encoding="utf-8") as f:
            f.write(sec9.strip())
        report.append(f"剧本文件: 已保存为 {fname}")

    return report

def _get_ep(sec):
    m = re.search(r'"ep":\s*(\d+)', sec)
    if m:
        return m.group(1)
    m2 = re.search(r'第(\d+)集', sec)
    if m2:
        return m2.group(1)
    return "?"

if __name__ == "__main__":
    text = sys.stdin.read()
    results = parse_answer(text)
    print("=== 解析结果 ===")
    for r in results:
        print(f"  [{chr(10003) if '失败' not in r else chr(10007)}] {r}")
    print("=== 完成 ===")