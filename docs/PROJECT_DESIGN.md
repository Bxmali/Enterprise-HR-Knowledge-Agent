# 项目实现说明

## 为什么 MySQL + 向量数据库同时使用？

MySQL 适合精确查询：
- 员工姓名
- 部门
- 薪资
- 绩效分数

向量数据库适合语义查询：
- 简历内容
- 绩效评语
- 培训记录
- 员工手册

## 为什么要 Small-to-Big？

小块检索精准，大块回答完整。

系统将文档切成 Parent Chunk 和 Child Chunk：

- Child Chunk 存向量库，用于召回
- Parent Chunk 存 docstore，用于回答

## 为什么需要记忆系统？

短期记忆用于多轮对话。
长期记忆用于保存重要历史。
用户画像用于记录用户长期偏好。

## 为什么默认 Chroma，兼容 Qdrant？

Chroma 类似 SQLite，适合本地学习。
Qdrant 类似 MySQL，是服务型向量数据库，适合企业部署。
