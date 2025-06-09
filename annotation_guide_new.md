# HKU校园建筑数据标注指南

## 1. 数据标注原则

### 1.1 准确性
- 所有建筑信息必须准确无误
- 历史年份、建筑师名称等需要查证
- 不确定的信息不要编造

### 1.2 双语一致性
- 中英文描述应该传达相同的信息
- 专有名词保持官方译名
- 注意语言风格的自然性

### 1.3 多样性
- 问题类型要多样化
- 回答长度要有变化
- 涵盖不同难度级别

## 2. 标注类别

### 2.1 建筑识别类
```json
{
  "en": {
    "q": "What building is shown in this image?",
    "a": "This is the Run Run Shaw Tower at the University of Hong Kong."
  },
  "cn": {
    "q": "这是什么建筑？",
    "a": "这是香港大学的邵逸夫楼。"
  }
}
```

### 2.2 历史背景类
```json
{
  "en": {
    "q": "Can you tell me about the history of this building?",
    "a": "The Main Building was completed in 1912 and is the oldest building at HKU. It was designed by Leigh & Orange in the Edwardian Baroque style."
  },
  "cn": {
    "q": "能介绍一下这座建筑的历史吗？",
    "a": "本部大楼于1912年落成，是港大最古老的建筑。由Leigh & Orange建筑事务所设计，采用爱德华巴洛克风格。"
  }
}
```

### 2.3 建筑特征类
```json
{
  "en": {
    "q": "What are the distinctive architectural features of this building?",
    "a": "The building features a prominent clock tower, arched windows, red brick facade, and classical columns at the entrance."
  },
  "cn": {
    "q": "这座建筑有什么特色？",
    "a": "这座建筑的特色包括醒目的钟楼、拱形窗户、红砖外墙以及入口处的古典柱廊。"
  }
}
```

### 2.4 功能用途类
```json
{
  "en": {
    "q": "What is this building used for?",
    "a": "The Kadoorie Biological Sciences Building houses laboratories, lecture theaters, and research facilities for the Faculty of Science."
  },
  "cn": {
    "q": "这座建筑的用途是什么？",
    "a": "嘉道理生物科学大楼设有实验室、演讲厅和理学院的研究设施。"
  }
}
```

### 2.5 位置导航类
```json
{
  "en": {
    "q": "How do I get to this building from the main entrance?",
    "a": "From the main entrance, walk straight along the main road for about 5 minutes. The building will be on your right, next to the library."
  },
  "cn": {
    "q": "从正门怎么走到这里？",
    "a": "从正门直走约5分钟，建筑就在您的右手边，紧邻图书馆。"
  }
}
```

### 2.6 实用信息类
```json
{
  "en": {
    "q": "What facilities are available in this building?",
    "a": "The building has study rooms, computer labs, a cafeteria on the ground floor, and student service center on the second floor."
  },
  "cn": {
    "q": "这栋楼里有什么设施？",
    "a": "这栋楼设有自习室、电脑室、一楼有餐厅，二楼有学生服务中心。"
  }
}
```

## 3. 多轮对话示例

```json
{
  "id": "hku_multi_example",
  "image": "centennial_campus_001.jpg",
  "conversations": [
    {
      "from": "human",
      "value": "<image>\nWhat modern building is this?"
    },
    {
      "from": "gpt",
      "value": "This is the Centennial Campus of HKU, a modern extension of the university completed in 2012."
    },
    {
      "from": "human",
      "value": "Why is it called Centennial Campus?"
    },
    {
      "from": "gpt",
      "value": "It's called Centennial Campus because it was built to commemorate the 100th anniversary of the University of Hong Kong, which was founded in 1911."
    },
    {
      "from": "human",
      "value": "What faculties are located here?"
    },
    {
      "from": "gpt",
      "value": "The Centennial Campus houses several faculties including the Faculty of Law, Faculty of Social Sciences, and the Faculty of Arts. It also contains state-of-the-art teaching facilities, libraries, and student amenities."
    }
  ]
}
```

## 4. 标注注意事项

### 4.1 避免的错误
- ❌ 编造不存在的设施或服务
- ❌ 提供过时的信息（如已关闭的餐厅）
- ❌ 混淆不同建筑的信息
- ❌ 使用过于学术或生硬的语言

### 4.2 推荐做法
- ✅ 使用官方名称和术语
- ✅ 提供实用的导览信息
- ✅ 回答自然、友好、专业
- ✅ 适当加入有趣的历史故事或趣闻

### 4.3 数据平衡
- 每座建筑至少20个不同的问答对
- 中英文问答数量平衡
- 简单问题和复杂问题比例约为 3:2:1（简单:中等:复杂）
- 包含5-10%的多轮对话

## 5. 质量检查清单

在完成标注后，请检查：
- [ ] 所有事实信息是否准确
- [ ] 中英文是否表达一致
- [ ] 是否涵盖了各种问题类型
- [ ] 语言是否自然流畅
- [ ] 是否有拼写或语法错误
- [ ] 图片文件名是否正确对应