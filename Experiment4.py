import shutil
import os
import json
import time
import hashlib
import numpy as np
import re
import cProfile
from memory_profiler import profile

class PermutermIndex:
    def __init__(self, terms):
        self.permuterm_index = {}
        self.construct_permuterm_index(terms)

    def construct_permuterm_index(self, terms):
        for term in terms:
            term_with_delimiter = term + '$'  # Using $ as a delimiter
            rotations = [term_with_delimiter[i:] + term_with_delimiter[:i] for i in range(len(term_with_delimiter))]
            for rotation in rotations:
                self.permuterm_index.setdefault(rotation, []).append(term)

    def prefix_search(self, wildcard_query):
        # Append $ to the end of the query and remove the *
        query = wildcard_query.replace('*', '') + '$'
        # Rotate the query until the $ is at the front (which would mean the * is at the end)
        while query[-1] != '$':
            query = query[-1] + query[:-1]
        # Now the query is rotated such that the original position of the wildcard is at the end, just before the $
        # Remove the $ for searching
        query = query[:-1]
        results = set()
        for key in self.permuterm_index.keys():
            if key.startswith(query):
                results.update(self.permuterm_index[key])
        return list(results)

class TreeBasedIndex:
    def __init__(self, terms):
        self.forward_index = {}
        self.backward_index = {}
        self.construct_tree_based_index(terms)

    def construct_tree_based_index(self, terms):
        for term in terms:
            for i in range(len(term)):
                prefix = term[:i + 1]
                suffix = term[i:]
                self.forward_index.setdefault(prefix, set()).add(term)
                self.backward_index.setdefault(suffix[::-1], set()).add(term)

    def wildcard_search(self, wildcard_query):
        results = set()

        if wildcard_query[0] == '*' and wildcard_query[-1] != '*':
            reversed_query = wildcard_query[::-1]
            results.update(term for term in self.backward_index if term.endswith(reversed_query))

        elif wildcard_query[0] != '*' and wildcard_query[-1] == '*':
            prefix = wildcard_query[:-1]
            results.update(term for term in self.forward_index if term.startswith(prefix))

        elif wildcard_query[0] != '*' and '*' in wildcard_query:
            parts = wildcard_query.split('*')
            forward_results = self.forward_index.get(parts[0] + parts[1], set())
            backward_results = self.backward_index.get(parts[1][::-1] + parts[0][::-1], set())
            results.update(forward_results.intersection(backward_results))

        return list(results)

def Wildcard_querying(corpus, wildcard_queries):
    # Permuterm Indexes
    permuterm_index = PermutermIndex(corpus)
    print("\nPermuterm Indexes:")
    for query in wildcard_queries:
        results = permuterm_index.prefix_search(query)
        print(f"Results for wildcard query '{query}': {results}")

    # Tree-based Indexes
    tree_based_index = TreeBasedIndex(corpus)
    print("\nTree-based Indexes:")
    for query in wildcard_queries:
        results = tree_based_index.wildcard_search(query)
        print(f"Results for wildcard query '{query}': {results}")

# Code starts here
if __name__ == '__main__':

    #Only Exp-4 main part here
    
    f2 = open("s2/" + "/s2_wildcard.json", encoding="utf-8")
    Wildcards = json.load(f2)["queries"]
    wildcard_queries = [query["query"] for query in Wildcards]

    corpus = []
    for paper in json_file['all_papers']:
        doc_no = paper['docno']
        title = paper['title'][0]
        abstract = paper['paperAbstract'][0]
        
        title_tokens = title.lower().split()
        abstract_tokens = abstract.lower().split()
        all_tokens = title_tokens + abstract_tokens
        corpus += all_tokens
    
    with cProfile.Profile() as pr:
        Wildcard_querying(corpus, wildcard_queries)
    
    pr.print_stats()
    #Someone pls implement the memory profiler. 
    f.close()
    f1.close()
    f2.close()
