
if __name__ == '__main__':

import pandas as pd


def largest_orders(orders: pd.DataFrame) -> pd.DataFrame:
    order_counts = orders.groupby('customer_number').size().reset_index(name='order_count')

    max_orders = order_counts['order_count'].max()
    result = order_counts[order_counts['order_count'] == max_orders][['customer_number']]

    return result

-----------------------------------------------------------------------------------------------------------------------

import pandas as pd


def actors_and_directors(actor_director: pd.DataFrame) -> pd.DataFrame:
    pair_counts = actor_director.groupby(['actor_id', 'director_id']).size().reset_index(name='count')

    result = pair_counts[pair_counts['count'] >= 3][['actor_id', 'director_id']]

    return result