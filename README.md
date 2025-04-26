# 0.参考文档
- **基于大型语言模型的检索增强生成综述**<br>
该文章发布于25.03.13。
在1.2节开头列出了目前主流的研究问题与解决方案。
在1.6节列出了主流的RAG应用框架。
- **A Survey on the Optimization of Large Language  Model-based Agents**<br>
https://github.com/YoungDubbyDu/LLM-Agent-Optimization<br>
该文章发布于25.03，整理了主流的agent技术，特别在第4节提到了无参的agent技术，其中包括rag。该综述涉及到的文章都已由作者整理到了github上，可以参考。
- **LLM Powered Autonomous Agents**<br>
https://lilianweng.github.io/posts/2023-06-23-agent/<br>
LilianWen的博客，这篇文章从三个方面：Plan、Memory、Tools的三个角度来分析Agent技术
- **Prompt Engineering**<br>
https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/<br>
LilianWen的博客，主要关注提示词工程，特别是in-context learning<br>
- **Creating Large Language Model Applications Utilizing LangChain: A  Primer on Developing LLM Apps Fast**<br>
https://github.com/research-outcome/llm-langchain-examples<br>
这篇文章对langchain中的基本组件的功能进行了阐述<br>

# 1.依赖
langchain
langgraph
langserve
python(3.10)
qdrant
akshare
uvicorn
fastapi<br>

本项目使用通义千问作为模型服务，具体如下：<br>
- chat_model: ChatTongyi<br>
https://python.langchain.com/docs/integrations/chat/tongyi/<br>
- embedding: DashScope<br>
https://python.langchain.com/docs/integrations/text_embedding/dashscope/<br>

通义千问相关的模型使用指导可参照下面的链接：<br>
https://bailian.console.aliyun.com/console?tab=api#/api/?type=model&url=https%3A%2F%2Fhelp.aliyun.com%2Fdocument_detail%2F2712515.html

# 2.使用
`python -m web.serve`<br>
访问：localhost:8080/runApp/playground