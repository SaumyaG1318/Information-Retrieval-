import sys
import os
import json
sys.path.append('../')
from main import load_index_in_memory as load, and_query, intersection


def queries(postings):
	f = open('../s2/s2_query.json', encoding="utf-8")
	json_file = json.load(f)
	
	for json_object in json_file['queries']:
		qid = json_object['qid']
		query = json_object['query'].split(" ")
		
		
		if query[0] in postings:
			result = postings[query[0]]
			for q in query[1:]:
				l1 = result
				l2 = q 
				result =  intersection(l1, l2)
					
			print("qid:", qid, result)
		else:
			print("qid:", qid,  '[]')


if __name__ == '__main__':
    postings = {}
    doc_freq = {}
    
    postings, doc_freq = load('../s2/')
    queries(postings)
