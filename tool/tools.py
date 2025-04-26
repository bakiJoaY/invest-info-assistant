from langchain_core.tools import tool
import akshare as ak
from vector_store.qdrant import get_qdrant_vector_store

@tool(response_format="content")
def retrieveHottestConcept():
    """通过akshare接口，获取今天最火的概念板块"""
    return '中国股市今天最热门的概念板块是'+ak.stock_board_concept_name_em().iloc[0]['板块名称']


@tool(response_format="content")
def retrieveConceptInfo(query: str):
    """寻找某个概念板块的背景、介绍信息"""
    qdrant_vector_store = get_qdrant_vector_store()
    result = qdrant_vector_store.similarity_search_with_score(f"请找一下{query}的详细信息", k=4)
    print('retrieveConceptInfo result:')
    print(result)
    return result