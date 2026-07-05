# 生图模型规格说明

## GPT Image 2 (DALL·E 3)

### 特性
- 最佳输入：自然语言描述
- 支持长度：最多 ~400 tokens
- 优势：理解复杂语义、场景还原强
- 劣势：风格化可控性较弱

### 提示词建议
```
1. 用完整句子描述，而非关键词堆砌
2. 优先描述主体，再展开细节
3. 避免过多技术参数
4. 使用"high quality""detailed"等简单质量词
```

**模板格式**:
```
A [age] [gender] who is [appearance details]. 
They are wearing [clothing description]. 
The setting is [scene description]. 
[Lighting and atmosphere]. High quality, detailed artwork.
```

---

## Seedream 4.5 (Kling AI)

### 特性
- 最佳输入：关键词 + 自然语言混合
- 支持长度：~600 tokens
- 优势：亚洲人脸优化、风格多样
- 劣势：英文理解略逊

### 提示词建议
```
1. 关键特征用英文关键词
2. 复杂描述用自然语言
3. 可以加入中文注释（部分支持）
4. 明确指定风格标签
```

**模板格式**:
```
[keyword1], [keyword2], [keyword3], 
[detailed description in sentences], 
style: [style_tag], quality: [quality_tag]
```

### 常用风格标签
```
photorealistic      # 写实
anime               # 动漫
watercolor          # 水彩
oil painting        # 油画
digital art         # 数字艺术
illustration        # 插画
```

---

## 通用参数建议

### 分辨率
- 人设图推荐：1024x1024 或 768x1024 (竖版更适合人物)

### 采样步数
- SDXL 系：30-40 steps
- DALL·E 3：自动
- Midjourney: --s 250-500 (stylize)

### CFG Scale
- 写实风格：5-7
- 艺术风格：7-10

---

## 负面提示词通用库

```
ugly, deformed, noisy, blurry, distorted, 
out of focus, bad anatomy, extra limbs, 
disfigured, poorly drawn hands, poorly drawn faces, 
mutation, mutated, extra fingers, wrong number of fingers, 
bad proportions, missing limbs, floating limbs, 
disconnected limbs, malformed hands, long neck, 
long body, cloned face, long face, fused fingers, 
too many fingers, long neck, ugly, bad hands, 
missing fingers, extra digit, third hand, 
conjoined fingers, too many arms, extra leg, 
malformed feet, extra foot, poorly drawn feet, 
extra toe, too many toes, watermark, signature, 
text, error, username, cropping, worst quality, 
low quality, jpeg artifacts, out of frame, 
mutated, extra limb, ugly, disgusting, poorly drawn, 
amputation, bad anatomy, disfigured, deformed, 
cross-eyed, blurred, duplicate, morbid, 
fleshy colors, 3d, cgi, render
```
