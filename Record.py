import re

class Record:
    def __init__(self, record, domainName):
        self.domainName = domainName
        self.recordName = record.attrib['data-name']+'.'
        self.recordData = record.attrib['data-data']
        self.recordServiceName = record.attrib['data-service']
        self.recordProtocol = record.attrib['data-protocol']
        self.recordPriority = record.attrib['data-priority']
        self.recordWeigth = record.attrib['data-weight']
        self.recordPort = record.attrib['data-port']
        self.recordType = (list(record.getchildren()[0])[1]).attrib['data-type']


    def getAWSRecordOutput(self):
        '''
        Function that outputs the string of a record in aws format
        Three columns with DNS Entry name + entry type + values separated by spaces

        NO SOA RECORDS

        example (site)
        record1.org.     A   10.0.0.1
        record2.org.    CNAME   record.org.

        example (mail)
        record.org      MX  (10)    mail.record.org.
        redord.org      MX  (20)    mail2.record.org.



        :return string of a record formated in AWS format
        '''

        #build MX record - priority is between brackets
        if self.recordType == "MX":
            line = self.recordName + "\t" + self.recordType + "(" + self.recordPriority + ")\t" + self.recordData + "."
            return line
        # build SRV record - domain need to be removed from record Data
        elif self.recordType == "SRV":
            self.recordData = re.sub("."+self.domainName,'',self.recordData)
            line = self.recordServiceName+"."+self.recordProtocol+"."+self.recordName + "\t" + self.recordType + "\t" + self.recordPriority + " " + self.recordWeigth + " " + self.recordPort + "\t" + self.recordData
            return line
        # build CNAME record - need an '.' to be appended at the end
        elif self.recordType == "CNAME":
            line = self.recordName + "\t" + self.recordType + "\t" + self.recordData + "."
            return line
        # build TXT record - record Data needs to be between quotation marks "
        elif self.recordType == "TXT":
            line = self.recordName + "\t" + self.recordType + "\t \"" + self.recordData + "\""
            return line
        # build default record
        else:
            line = self.recordName + "\t" + self.recordType + "\t" + self.recordData
            return line