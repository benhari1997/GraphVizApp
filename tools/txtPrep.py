import networkx as nx
from nltk.corpus import stopwords
from tqdm import tqdm

def load_file(filename):
    """
    loads file as list of words
    """
    with open(filename,'r') as f:
        text = f.readlines()
    return text

def preprocess(line):
    """
    preprocesses each text's line
    """
    stop_words = set(stopwords.words('english'))
    line = [item.lower() for item in line if not item.lower() in stop_words]
    return line

def create_graph_from_text(text_path):
    """
    returns a networkx graph after preprocessing it.
    """
    text = load_file(text_path)
    word_list = []
    G = nx.Graph()
    pbar = tqdm(total=len(text))
    for line in text:
        line = (line.strip()).split()
        line = preprocess(line)
        for i, word in enumerate(line):
            if i != len(line)-1:
                word_a = word
                word_b = line[i+1]
                if word_a not in word_list:
                    word_list.append(word_a)
                if word_b not in word_list:
                    word_list.append(word_b)
                if G.has_edge(word_a,word_b):
                    G[word_a][word_b]['weight'] += 1
                else:
                    G.add_edge(word_a,word_b, weight = 1)
        pbar.update(1)
    pbar.close()
    return G



