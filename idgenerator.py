import argparse
import csv
import requests
import json


URIGEN_URL = "http://garfield.ebi.ac.uk:8180/urigen/api/uris?restApiKey="
ONTOLOGY_ID = 2



def processFile(input, output, api_key):
    # print(input)

    with open(input) as tsvin, open(output, 'w') as tsvout:
        tsread = csv.reader(tsvin, delimiter='|')
        tsvout = csv.writer(tsvout, delimiter='\t')

        url = URIGEN_URL + api_key

        for row in tsread:
            # print(row)
            # print(row[0])

            if row[0] == '':
                label = row[1]

                payload = {"preferencesId": ONTOLOGY_ID, "label": label}

                r = requests.post(url, json=payload)

                if r.ok:
                    data = json.loads(r.content)

                    id = data["generatedUri"]

                    id = id.replace("http://www.ebi.ac.uk/efo/", "efo:")

                    row[0] = id

            tsvout.writerow(row)





if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="input",
                      help="path to input file", metavar="FILE")
    parser.add_argument("-o", "--output", dest="output",
                      help="path to output file", metavar="FILE")
    parser.add_argument("-a", "--apikey", dest="api_key",
                      help="your urigen API key")
    args = parser.parse_args()

    if not args.input:
        print("You must supply an input file")
        exit(2)
    if not args.output:
        print("You must supply an output file")
        exit(2)

    if not args.api_key:
        print("You must supply your Urigen API key")
        exit(2)
    processFile(args.input, args.output, args.api_key)