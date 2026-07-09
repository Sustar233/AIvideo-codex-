# -*- coding: utf-8 -*-
"""
銆婄惀鐝€涔嬪煄銆嬪墽鏈垎鏋愮粨鏋滆В鏋愬櫒
鐢ㄦ硶锛氬皢缃戦〉鐗?AI 鐨勮緭鍑哄叏鏂囪创鍒?stdin锛屾鑴氭湰瑙ｆ瀽鍚庤嚜鍔ㄦ洿鏂版暟鎹簱
"""

import json, os, sys, re
sys.stdout.reconfigure(encoding="utf-8")

DB = "剧本文件夹/database"

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

    # 1. 鍒嗛泦鍓ф儏
    sec1 = extract_section(text, "1\\.")
    m = re.search(r"\{.*\}", sec1, re.DOTALL)
    if m:
        try:
            ep_data = json.loads(m.group())
            eps = load_json(os.path.join(DB, "鍒嗛泦鍓ф儏.json"))
            eps["闆嗘暟"].append(ep_data)
            save_json(os.path.join(DB, "鍒嗛泦鍓ф儏.json"), eps)
            report.append(f"鍒嗛泦鍓ф儏: 绗瑊ep_data['ep']}闆嗗凡娣诲姞")
        except:
            report.append("鍒嗛泦鍓ф儏: 瑙ｆ瀽澶辫触")

    # 2. 鐜版湁瑙掕壊鏇存柊
    sec2 = extract_section(text, "2\\.")
    updates = {}
    for line in sec2.split("\n"):
        line = line.strip()
        if "锛? in line:
            name, desc = line.split("锛?, 1)
            updates[name] = desc
    if updates:
        chars = load_json(os.path.join(DB, "瑙掕壊.json"))
        for c in chars:
            key = f"绗瑊_get_ep(sec1)}闆嗚〃鐜?
            if c["name"] in updates:
                c[key] = updates[c["name"]]
        save_json(os.path.join(DB, "瑙掕壊.json"), chars)
        report.append(f"瑙掕壊鏇存柊: {list(updates.keys())}")

    # 3. 鏂拌鑹?    sec3 = extract_section(text, "3\\.")
    if sec3 and sec3 != "鏃?:
        chars = load_json(os.path.join(DB, "瑙掕壊.json"))
        added = 0
        for line in sec3.split("\n"):
            line = line.strip()
            if not line or "|" not in line:
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                new_char = {
                    "name": parts[0],
                    "鎬у埆": parts[1] if len(parts) > 1 else "",
                    "澶栬矊": parts[2] if len(parts) > 2 else "",
                    "韬唤": parts[3] if len(parts) > 3 else "",
                    "鎬ф牸": parts[4] if len(parts) > 4 else "",
                    "姝﹀櫒": parts[5] if len(parts) > 5 else "",
                    "鏈泦琛ㄧ幇": parts[6] if len(parts) > 6 else "",
                    "棣栨鍑虹幇": f"绗瑊_get_ep(sec1)}闆?,
                    "澶囨敞": parts[7] if len(parts) > 7 else ""
                }
                if not any(c["name"] == new_char["name"] for c in chars):
                    chars.append(new_char)
                    added += 1
        save_json(os.path.join(DB, "瑙掕壊.json"), chars)
        report.append(f"鏂板瑙掕壊: {added}")

    # 4. 鏂板満鏅?    sec4 = extract_section(text, "4\\.")
    if sec4 and sec4 != "鏃?:
        scens = load_json(os.path.join(DB, "鍦烘櫙.json"))
        added = 0
        for line in sec4.split("\n"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 2:
                new_scene = {
                    "name": parts[0],
                    "鎻忚堪": parts[1] if len(parts) > 1 else "",
                    "鏃堕棿": parts[2] if len(parts) > 2 else "",
                    "鍏夊奖": parts[3] if len(parts) > 3 else "",
                    "鍏抽敭閬撳叿": parts[4] if len(parts) > 4 else "",
                    "棣栨鍑虹幇": f"绗瑊_get_ep(sec1)}闆?
                }
                if not any(s["name"] == new_scene["name"] for s in scens):
                    scens.append(new_scene)
                    added += 1
        save_json(os.path.join(DB, "鍦烘櫙.json"), scens)
        report.append(f"鏂板鍦烘櫙: {added}")

    # 5. 鏂板嚩鍏?    sec5 = extract_section(text, "5\\.")
    if sec5 and sec5 != "鏃?:
        beasts = load_json(os.path.join(DB, "澶栨槦鍑跺吔.json"))
        added = 0
        for line in sec5.split("\n"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 2:
                new_beast = {
                    "name": parts[0],
                    "鎻忚堪": parts[1] if len(parts) > 1 else "",
                    "鐗规€?: parts[2] if len(parts) > 2 else "",
                    "鏈泦琛ㄧ幇": parts[3] if len(parts) > 3 else "",
                    "棣栨鍑虹幇": f"绗瑊_get_ep(sec1)}闆?
                }
                if not any(b["name"] == new_beast["name"] for b in beasts):
                    beasts.append(new_beast)
                    added += 1
        save_json(os.path.join(DB, "澶栨槦鍑跺吔.json"), beasts)
        report.append(f"鏂板鍑跺吔: {added}")

    # 6. 鏂伴亾鍏?    sec6 = extract_section(text, "6\\.")
    if sec6 and sec6 != "鏃?:
        props = load_json(os.path.join(DB, "鍏抽敭閬撳叿涓庡埗搴?json"))
        added = 0
        for line in sec6.split("\n"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                entry = {
                    "绫诲瀷": parts[1],
                    "鎻忚堪": parts[2],
                    "棣栨鍑虹幇": f"绗瑊_get_ep(sec1)}闆?
                }
                if len(parts) > 3 and parts[3]:
                    entry["鎸佹湁鑰?] = parts[3]
                if parts[0] not in props:
                    props[parts[0]] = entry
                    added += 1
        save_json(os.path.join(DB, "鍏抽敭閬撳叿涓庡埗搴?json"), props)
        report.append(f"鏂板閬撳叿/鍒跺害: {added}")

    # 7. 鍓ф儏姊楁
    sec7 = extract_section(text, "7\\.")
    if sec7 and sec7 != "鏃? and len(sec7) > 5:
        outline = load_json(os.path.join(DB, "鍓ф儏姊楁.json"))
        outline["鍏抽敭鍓ф儏鑺傜偣"].append(sec7.strip())
        save_json(os.path.join(DB, "鍓ф儏姊楁.json"), outline)
        report.append("鍓ф儏姊楁: 宸茶拷鍔?)

    # 8. 浜鸿鎻愮ず璇?(淇濆瓨鍒版枃浠?
    sec8 = extract_section(text, "8\\.")
    if sec8 and sec8 != "涓嶉渶瑕?:
        prompt_path = "剧本文件夹/人设提示词.md"
        with open(prompt_path, "w", encoding="utf-8") as f:
            f.write(f"# 浜鸿鎻愮ず璇?鈥?绗瑊_get_ep(sec1)}闆哱n")
            f.write("# 娉ㄦ剰锛氭鏂囦欢鍙繚鐣欐渶鏂版彁绀鸿瘝锛屾棫鐗堝凡瀛樺叆鐢ㄦ埛璧勪骇搴揬n\n")
            f.write(sec8)
        report.append("浜鸿鎻愮ず璇? 宸插啓鍏?)

    # 9. 淇濆瓨鍘熷鍓ф湰
    sec9 = extract_section(text, "9\\.")
    if sec9 and len(sec9) > 50:
        script_dir = "剧本文件夹"
        ep_num = _get_ep(sec1)
        fname = f"绗瑊ep_num}闆?txt"
        with open(os.path.join(script_dir, fname), "w", encoding="utf-8") as f:
            f.write(sec9.strip())
        report.append(f"鍓ф湰鏂囦欢: 宸蹭繚瀛樹负 {fname}")

    return report

def _get_ep(sec):
    m = re.search(r'"ep":\s*(\d+)', sec)
    if m:
        return m.group(1)
    m2 = re.search(r'绗?\d+)闆?, sec)
    if m2:
        return m2.group(1)
    return "?"

if __name__ == "__main__":
    text = sys.stdin.read()
    results = parse_answer(text)
    print("=== 瑙ｆ瀽缁撴灉 ===")
    for r in results:
        print(f"  [{chr(10003) if '澶辫触' not in r else chr(10007)}] {r}")
    print("=== 瀹屾垚 ===")
