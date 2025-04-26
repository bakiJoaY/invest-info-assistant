import akshare as ak


print(ak.stock_hot_rank_em())

def ak_stock_hot_rank_em():
    """ 通过akshare接口获取当天最热门的板块，返回数据为DataFrame """
    return ak.stock_hot_rank_em()