import argparse
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import numpy as np
import os

from img2vec_keras import Img2Vec
docs=[]
img2vec = Img2Vec()
# for img_path in sorted(Path("./images").glob("*.jpg")):
#     print(img_path)
#
#     docs[img_path]=img2vec.get_vec(img_path).tolist()
#     print(type(img2vec.get_vec(img_path).tolist()))
#     print(type(img_path))
# print(docs)


# rootdir = '/home/jainal09/adarsh/bertsearch'

client = Elasticsearch()

def main(args):

    docs = []

    # docs = load_dataset(args.data
    root = "./images"
    print('below root')
    for subdir, dirs, files in os.walk(root):
        print('in for')
        for file in files:
            dic = {
                '_op_type': 'index',
                '_index': args.index_name,
                "title": file,
                "text_vector": img2vec.get_vec(os.path.join(subdir, file)).tolist()

            }
            docs.append(dic)

    print(docs)
    bulk(client, docs)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creating elasticsearch documents.')
    # parser.add_argument('--data', help='data for creating documents.')
    # parser.add_argument('--save', default='documents.jsonl', help='created documents.')
    parser.add_argument('--index_name', default='jobsearch', help='Elasticsearch index name.')
    args = parser.parse_args()
    main(args)
    print('hi')


# python3 index_image.py --index_name=jobsearch
