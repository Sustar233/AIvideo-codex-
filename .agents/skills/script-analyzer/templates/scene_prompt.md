# 场景提示词模板

生成场景生图提示词时，按以下结构组织：

## 必含要素（中英文对照格式）

| 字段 | 说明 | 示例 |
|------|------|------|
| **场景名称** | 中文命名 + 英文标识 | 琥珀之城中心广场 (Amber City Central Plaza) |
| **空间类型** | 室内/室外/城市/荒野/建筑内部等 | outdoor urban plaza |
| **环境描述** | 地形、建筑风格、植被、天气 | cobblestone streets, amber-glowing towers, clear sky with floating dust particles |
| **时间/光影** | 白天/黄昏/夜晚，光源方向与色温 | golden hour, warm sunlight streaming through amber barrier |
| **关键道具** | 该场景中必须出现的道具或标志性物品 | giant amber barrier pillars embedded in ground |
| **氛围关键词** | 整体情绪基调 | awe-inspiring, peaceful but with underlying tension |
| **构图模式** | 由用户选择：四宫格 / 俯视图 / 九宫格 / 全景图 | panoramic wide shot |

## 输出格式

每次为场景生成提示词时，按以下三段式输出：

```
【场景名】- [构图模式]

版本（标准版）：
> prompt: [英文+中文描述]

负面提示词：
[从 style_guide.md 复制负面列表]
```

## 注意事项

- 同一场景在不同集数若发生变化（如被破坏、季节更替），标注变化点
- 如果剧本未明确时间/光影，根据剧情氛围合理推断并标注"推断"
- 新场景需在输出末尾附上 JSON 片段，格式与 `场景.json` 一致，方便直接追加
- 对于有奇幻元素的世界观（如屏障、荧光效果），在风格中保持一致性
