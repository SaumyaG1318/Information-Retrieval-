#!/bin/bash

# Read the JSON file containing the queries
json_file="../s2/s2_query.json"

# Extract the queries using jq and loop over them
jq -c '.queries[]' "$json_file" | while IFS= read -r query; do
    # Extract the query text from the JSON object
    query_text=$(echo "$query" | jq -r '.query')

    # Search for the query text in the JSON file
    matching_docs=$(jq --arg query_text "$query_text" '.all_papers[] | select(.title[0] | test($query_text)) | .docno' ../s2/s2_doc.json)

    # Print the query text and corresponding docnos
    echo "Query: $query_text"
    echo "$matching_docs"
done

