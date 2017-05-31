"""
Descryption: scrapes hostnet.nl DNS records html page of a zone/domain and exports the result as a AWS route 53 formated DNS zone file
Input: hostnet.nl domain records configuration (.HTML saved page)
Output:  Domain.txt file (AWS Route 53 format)

Written by: jorge gil
"""
from lxml import html
from Record import Record
import sys, os.path


domainXpath= "//form[@id = 'dns-form']"
subdomainsXpath="//div[@class='dns-record default-row resetable undoable']"
#AWS Zone file header
origin = "$ORIGIN "
ttl ="$TTL 300"

def main():
    #takes a filename as one argument
    if(len(sys.argv) < 2):
        print("No argument received.\n Use HTML file as an argument")
        sys.exit(0)

    #Check if file exists
    if os.path.isfile(sys.argv[1]):
        htmlFileName = sys.argv[1]
    else:
        print("not a valid file")
        sys.exit(0)

    #read file contents
    with open(htmlFileName,"r") as f:
        page=f.read()

    tree = html.fromstring(page)

    #get records form content
    dnsForm = tree.xpath(domainXpath)[0]

    #get Domain
    domainName = dnsForm.attrib['data-domain']

    #get records list
    subdomains = tree.xpath(subdomainsXpath)

    #build filename
    fileName = domainName + ".txt"

    #create file
    f = open(fileName, 'w')

    #write header into file
    #Domain and TTL
    f.write(origin + domainName + "\n")
    f.write(ttl + "\n")

    #go trough all records found
    for sub in subdomains:
        #creates a Record Object
        myRecord = Record(sub,domainName)

        #Print to console status and write to file all entries
        print("Writing " + myRecord.recordName + " to file...")
        f.write(myRecord.getAWSRecordOutput() + "\n")

    #close file
    f.close()

if __name__ == "__main__":
    main()