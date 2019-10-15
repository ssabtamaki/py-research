import itertools
import networkx as nx
from .const import JSONFILES
from .text import (create_tweets_loading_file,
                   extract_text,
                   morphological_analysis)
from .datapolish.similarity import npmi
from .datapolish.graph import binarize_graph


def co_occurrence_network(jsonfiles: list, graph: nx.Graph) -> nx.Graph:
    '''
    共起ネットワークを作成
    '''
    tweets = create_tweets_loading_file(jsonfiles)
    all_words = set()
    for tweet in tweets:
        words = morphological_analysis(tweet)
        all_words.add(words)
    _add_node_and_edge(all_words, graph)
    _compute_npmi(graph)
    return graph


def _add_node_and_edge(all_words: list, graph: nx.Graph):
    '''
    Graphにnodeとedgeを付与
    param words: 1ツイートに含まれる単語
    '''
    for v in all_words:
        if v in graph.nodes():
            graph.nodes[v]['count'] += 1
        else:
            graph.add_node(v, count=1)
    for u, v in itertools.combinations(all_words, 2):
        if graph.has_edge(u, v):
            graph[u][v]['count'] += 1
        else:
            graph.add_edge(u, v, count=1)


def _compute_npmi(graph: nx.Graph):
    '''
    共起の強さを測るため、相互情報量を求める
    '''
    total_num_of_tweets = len(JSONFILES)
    for v in graph.nodes():
        graph.nodes[v]['probability'] = \
            graph.nodes[v]['count'] / total_num_of_tweets
    for u, v in graph.edges():
        graph[u][v]['probability'] = graph[u][v]['count'] / total_num_of_tweets
    # NPMI計算
    for u, v in graph.edges():
        graph[u][v]['npmi'] = npmi(
            graph[u][v]['probability'],
            graph.nodes[u]['probability'],
            graph.nodes[v]['probability']
        )


def _output_CON_to_A():
    graph = nx.Graph()
    graph = co_occurrence_network(JSONFILES, graph)
    # 以下でグラフを出力


if __name__ == '__main__':
    _create_graph_in_CON()