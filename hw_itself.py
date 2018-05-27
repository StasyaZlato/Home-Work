import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import networkx as nx
import matplotlib.pyplot as plt


def searching_for_cos(sem_pole):
    import gensim
    m = 'ruwikiruscorpora_upos_skipgram_300_2_2018.vec.gz'
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
    print('Модель загружена')
    variants = [(i, n) for i in sem_pole for n in sem_pole if i != n]
    for pair in variants:
        if pair[0] in model and pair[1] in model:
            nums = model.similarity(pair[0], pair[1])
            with open('new_file.txt', 'a', encoding='utf-8') as f:
                f.write(pair[0] + '\t' + pair[1] + '\t' + str(nums) + '\n')


'''Еще одна бессмысленная домашка, настолько загружающая оперативку и ноутбук в целом, 
и следующую переустановку винды оплачивать будете вы.'''


def making_graph(sem_pole):
    graph = nx.Graph()
    graph.add_nodes_from(sem_pole)
    data = data_for_graph(sem_pole)
    for i in data:
        graph.add_edge(i[0], i[1], weight=float(i[2]))
    # pos = nx.spring_layout(graph)
    labels = {i: i for i in sem_pole}
    nx.draw_circular(graph, node_color='#66CCCC', edge_color='#003333', labels=labels)
    plt.axis('off')
    nx.write_gexf(graph, 'graph_file.gexf')
    plt.show()
    return


def data_for_graph(sem_pole):
    with open('new_file.txt', 'r', encoding='utf-8') as f:
        data_plain = f.readlines()
    for i in range(len(data_plain)):
        data_plain[i] = data_plain[i].split('\t')
    data = []
    for data_el in data_plain:
        if float(data_el[2]) > 0.5 and data_el not in data and [data_el[1], data_el[0], data_el[2]] not in data:
            data.append(data_el)
    return data


def central_nodes(graph):
    deg = nx.degree_centrality(graph)
    list_sort = []
    for nodeid in sorted(deg, key=deg.get, reverse=True):
        list_sort.append(nodeid + '\t' + str(round(deg[nodeid], 3)) + '\t' + str(graph.degree(nodeid)))
    return 'Список узлов, сортированных по центральности\n' + '\n'.join(list_sort)


def radius(graph):
    components = list(nx.connected_component_subgraphs(graph))
    num = len(components)
    rads = []
    line = ''
    for i in components:
        # rads.append(nx.radius(i))
        line = line + 'Компонента связности №' + str(components.index(i)+1) + ' имеет радиус ' + str(nx.radius(i)) + '\n'
    return 'Всего в графе {} компонент связности. {}'.format(str(num), line)


def clustering_c(graph):
    coef = nx.average_clustering(graph)
    return 'Коэффициент кластеризации графа {}'.format(str(coef))


def taking_info():
    graph = nx.read_gexf('graph_file.gexf')
    with open('graph_info.txt', 'w', encoding='utf-8') as f:
        f.write(central_nodes(graph) + '\n\n')
        f.write(radius(graph))
        f.write(clustering_c(graph))




def main():
    sem_pole = ['красный_ADJ',
                'пурпурный_ADJ',
                'лиловый_ADJ',
                'розовый_ADJ',
                'малиновый_ADJ',
                'розоватый_ADJ',
                'алый_ADJ',
                'бордовый_ADJ',
                'багровый_ADJ',
                'фиолетовый_ADJ',
                'коралловый_ADJ',
                'лавандовый_ADJ']
    # searching_for_cos(sem_pole)
    # data_for_graph(sem_pole)
    making_graph(sem_pole)
    taking_info()


main()





