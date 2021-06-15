#!/usr/bin/env python3

"""
Updated on Jun 14, 2020

By Johany A. Carmona C.
GitHub: https://github.com/JohanyCarmona/
Email: johany.carmona@pm.me; johany.carmona@tuta.io; johany.carmona@udea.edu.co

About: Legal Tradition Certificate PDF Scrapper
Info: Extract Main Data from a PDF file, then transform it to Data Object and finally load it to a JSON file.

Help: Execute from terminal using the following command.
Command: python3 cert.py [fileName]
"""

#System Library
from sys import argv
#REGEX Methods
from re import search, findall
#JSON Library
from json import dump
"""
pdfplumber Third Party Library
GitHub: https://github.com/jsvine/pdfplumber
Installation: pip install pdfplumber
"""
from pdfplumber import open as openPdf

"""
GENERAL REGEX PATTERNS
TIPs: If you want execute the script more restrictively,
      then use #Particular case comment lines to prevent invalid file extraction.
"""
#REGISTER_NUMBER_PATTERN = r'(?<=Nro Matrícula: )[0-9]+[-]?[0-9]*' #Particular case
REGISTER_NUMBER_PATTERN = r'(?<=Nro Matrícula: ).*' #General case

#PRINTOUT_DATE_PATTERN = r'(?<=Impreso el )([0]?[1-9]|([1-2][0-9]|[3][0-1])) de [A-Z][a-z]+ de ([0-1]?[0-9]{3}|(20[0-1][0-9]|202[0-1])) a las ([0-1][0-9]|[2][0-3])[:][0-5][0-9][:][0-5][0-9] (AM|PM)' #Particular case
PRINTOUT_DATE_PATTERN = r'(?<=Impreso el ).*' #General case

#REGISTRY_CIRCLES_PATTERN = r'(?<=CIRCULO REGISTRAL: )[0-9]+[ ]*[-]?[ ]*[A-Z]+[ ]*DEPTO:[ ]*([A-Z]+[ ]*)+MUNICIPIO:[ ]*([A-Z]+[ ]*)+VEREDA:([ ]*[A-Z]+)+' #Particular case
REGISTRY_CIRCLES_PATTERN = r'(?<=CIRCULO REGISTRAL: ).*' #General case

#CADASTRAL_CODE_PATTERN = r'(?<=CODIGO CATASTRAL: )[0-9]+[ ]*COD[ ]*CATASTRAL[ ]*[A-Z]+:([ ]*[A-Z]+)+' #Particular case
CADASTRAL_CODE_PATTERN = r'(?<=CODIGO CATASTRAL: ).*' #General case

#FOLIO_STATE_PATTERN = r'[A-Z]+(?=(\n)ESTADO DEL FOLIO:)' #Particular case
FOLIO_STATE_PATTERN = r'[a-z|A-Z]+(?=(\n)ESTADO DEL FOLIO:)' #General case

#PROPERTY_ADDRESS_PATTERN = r'(?<=Tipo Predio: )[A-Z]+(\n)1\)([ ]*([A-Z]+|[".]))+' #Particular case
PROPERTY_ADDRESS_PATTERN = r'(?<=Tipo Predio: ).*(\n).*\).*' #General case
PROPERTY_ADDRESS_KEYWORD = ' '

#PROPERTY_TYPE_PATTERN = r'(?<=Tipo Predio: )[A-Z]+' #Particular case
PROPERTY_TYPE_PATTERN = r'(?<=Tipo Predio: ).*' #General case

"""
RECORDS REGEX PATTERNS
"""
DOCUMENT_RECORD_PATTERN = r'(?<=Doc: ).*(?= VALOR ACTO:)' #Unique case

#RESIDE_RECORD_PATTERN = r'(?<=ANOTACION:)[ ]*Nro[ ]*[0-9]+.*Radicaci.n:[ ]*.*' #Particular case
RESIDE_RECORD_PATTERN = r'(?<=ANOTACION:).*' #General case
RESIDE_RECORD_KEYWORD = 'Radicación: '

#SPECIFICATION_RECORD_PATTERN = r'(?<=ESPECIFICACION: ).*[:]?[ ]*[0-9]+.*' #Particular case
SPECIFICATION_RECORD_PATTERN = r'(?<=ESPECIFICACION: ).*[:]?[ ]*.*' #General case
SPECIFICATION_KEYWORD = ': '

#PDF REGEX PATTERN
PDF_FORMAT_PATTERN = r'.*(?=.pdf)'
JSON_FORMAT = '.json'

#Legal Tradition Certificate
class Cert():
    
    def __init__(self, fileName):
        
        #READ
        content = self.__readPDF(fileName)
        
        #GENERAL
        self.registerNumber = search(REGISTER_NUMBER_PATTERN, content).group(0)
        self.printoutDate = search(PRINTOUT_DATE_PATTERN, content).group(0)
        self.registryCircles = search(REGISTRY_CIRCLES_PATTERN, content).group(0)
        self.cadastralCode = search(CADASTRAL_CODE_PATTERN, content).group(0)
        self.folioState = search(FOLIO_STATE_PATTERN, content).group(0)
        self.propertyAddress = self.__searchComplex(PROPERTY_ADDRESS_PATTERN, PROPERTY_ADDRESS_KEYWORD, content)
        self.propertyType = search(PROPERTY_TYPE_PATTERN, content).group(0)
        
        #RECORDS
        self.records = {}
        self.records['documentRecords'] = findall(DOCUMENT_RECORD_PATTERN, content)
        self.records['resideRecords'] = self.__findAllComplex(RESIDE_RECORD_PATTERN, RESIDE_RECORD_KEYWORD, content)
        self.records['specificationRecords'] = self.__findAllComplex(SPECIFICATION_RECORD_PATTERN, SPECIFICATION_KEYWORD, content)
        
        #WRITE
        self.__writeJSON(fileName)
    
    def __readPDF(self, fileName):
        content = ""
        with openPdf(fileName) as pdf:
            for page in pdf.pages:
                content = content + page.extract_text()
            pdf.close()
        return content
    
    #Find matched pattern and filter waste from data.
    def __searchComplex(self, pattern, keyword, content):
        data = search(pattern, content).group(0)
        _, _, data = data.partition(keyword)
        return data
        
    #Find all matched patterns and filter waste from data.   
    def __findAllComplex(self,pattern, keyword, content):
        #Find Matched Patterns
        dataRecords = findall(pattern, content)
        del content
        
        _dataRecords = []
        #Filter waste from data
        for dataRecord in dataRecords:
            _, _, dataRecord = dataRecord.partition(keyword)
            _dataRecords.append(dataRecord)
        del dataRecords
        
        return _dataRecords
    
    def __generateJSON(self):
        records = {
                    "Documento anotación" : self.records['documentRecords'],
                    "Radicación anotación" : self.records['resideRecords'],
                    "Especificación anotación" : self.records['specificationRecords']
        }
        
        output = {
                    "Número matrícula" : self.registerNumber,
                    "Fecha impresión" : self.printoutDate,
                    "Círculo registral" : self.registryCircles,
                    "Código catastral" : self.cadastralCode,
                    "Estado folio" : self.folioState,
                    "Dirección inmueble" : self.propertyAddress,
                    "Tipo predio" : self.propertyType,
                    "Anotaciones" : records
        }
        return output 
        
    def __writeJSON(self,fileName):
        fileName = search(PDF_FORMAT_PATTERN, fileName).group(0)
        fileName = fileName+JSON_FORMAT

        with open(fileName,'w') as file:
            dump(self.__generateJSON(), file)
        print()
        print("'%s' successfully created"%(fileName))
        
fileName = argv[1]
cert = Cert(fileName)
