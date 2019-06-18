"""
(Intern Project West Pod Summer 2019)
Authors: Thomas McLaughlin               |    Spencer DeRecat                   |    Benjamin Rice
Email : thomas.mclaughlin@tanium.com    |    Spencer.derecat@tanium.com        |    benjamin.rice@tanium.com
Date  : June 12 2019
Description:
formats data from xml into excel file
"""
#imports
import xlsxwriter
import xmlmethods

#helper functions to get rid of duplicates in dictionaries/lists.
def consolidatedictionary(input_raw):
    result = {}
    for key, value in input_raw.items():
        if key not in result.keys():
            result[key] = value
    return result
def consolidatedlist(input):
    return list(set(input))

#open workbook make a blank worksheet
workbook = xlsxwriter.Workbook("xmldata.xlsx")
worksheet = workbook.add_worksheet()
#create xml scraper to find relevant data to populate excel file with
xmlparser = xmlmethods.Xmlmethods('manifest.xml')

#setting up rows and cols. Headers for data.
toprow = ['name', 'count', 'delim', 'Issues', '-', '-', 'OS Support', '-', '-', 'Issues', 'description', 'Issues', 'result type', 'Issues', '-', '-', 'code length (by OS)', '-', '-', 'Issues', 'hash', 'Issues', '-', '-', 'Sensor Type (by OS)', '-', '-', 'Issues']
nextrow = ['-', '-', '-', '-', 'Win', 'Linux', 'Mac', 'Solaris', 'AIX', '-', '-', '-', '-', '-', 'Win', 'Linux', 'Mac', 'Solaris', 'AIX', '-', '-', '-', 'Win', 'Linux', 'Mac', 'Solaris', 'AIX', '-']
for i in range(28):
    worksheet.write(0, i, toprow[i])
    worksheet.write(1, i, nextrow[i])

#create a blank dictionary to put all of the data in. Key = sensor name. Value = list of values to populate cols with
#populating dictionary...
data_to_enter = {}
names = xmlparser.getnames()
for name, value in names.items():
    data_to_enter[name] = [value]

#load up xml parser atirbutes with all useful xml data
xmlparser.getsensortypes()
xmlparser.gethash()
xmlparser.getdelimeters()
xmlparser.getossupport()
xmlparser.getdescriptions()
xmlparser.getresulttype()
xmlparser.getsensorlength()

#put all that juicy data into the dictionary
for name, value in xmlparser.founddelims.items():
    data_to_enter[name].append(value)
for name, value in xmlparser.foundossupport.items():
    data_to_enter[name].append(value)
for name, value in xmlparser.founddescriptions.items():
    data_to_enter[name].append(value)
for name, value in xmlparser.foundresulttypes.items():
    data_to_enter[name].append(value)
for name, value in xmlparser.foundsensorlengths.items():
    data_to_enter[name].append(value)
for name, value in xmlparser.foundhashes.items():
    data_to_enter[name].append(value)
for name, value in xmlparser.foundsensortypes.items():
    data_to_enter[name].append(value)
print(data_to_enter['Computer Name'])

#putting values from dictionary into excel file, each sensor key corresponds to a length 8 list values with all of the useful information
#in the list there is the following information:
#at index 0: the number of occurances of the sensor in manifest.xml
#at index 1: the delimeter(s) used for the sensor
#at index 2: A list of lists that give OS support offered for each sensor, a sensor with consistently reported OS support in manifest.xml will only have one list
#at index 3: the description(s) of the sensor
#at index 4: the result type(s) of the sensor
#at index 5: A list of lists that gives code length (by character) for each sensor per OS - inconsistent code lengths across manifest.xml result in multiple lists
#at index 6: the hash value(s) of the sensor
#at index 7: A list of lists that gives sensor type per OS - inconsistent sensor types result in multiple lists
#indices 2, 5, 7 all take 5 cols in the excel file making for 20 cols for data + 1 col for sensor name
count = 2
for name, value in data_to_enter.items():
    worksheet.write(count, 0, name)
    for i in range(8):
        if i != 0:
            if len(value[i]) > 1:
                if i == 1:
                    worksheet.write(count, 3, 'conflict')
                if i == 2:
                    worksheet.write(count, 9, 'conflict')
                if i == 3:
                    worksheet.write(count, 11, 'conflict')
                if i == 4:
                    worksheet.write(count, 13, 'conflict')
                if i == 5:
                    worksheet.write(count, 19, 'conflict')
                if i == 6:
                    worksheet.write(count, 21, 'conflict')
                if i == 7:
                    worksheet.write(count, 27, 'conflict')
        if i == 0:  #how many occurances, always one value
            worksheet.write(count, 1, value[0])
        elif i == 2 or i == 5 or i == 7:  #iterating through the list elements
            counts = [[], [], [], [], []]
            for elem in value[i]:
                for index in range(len(elem)):
                    if i == 2:
                        counts[index].append(elem[index])
                        worksheet.write(count, index + 4, str(counts[index]) + '  ')
                    if i == 5:
                        counts[index].append(elem[index])
                        worksheet.write(count, index + 14, str(counts[index]) + '  ')
                    if i == 7:
                        counts[index].append(elem[index])
                        worksheet.write(count, index + 22, str(counts[index]) + '  ')
        else:  #all other elements
            if i == 1:
                worksheet.write(count, 2, str(value[i]) + '  ') #delim
            elif i == 3:
                worksheet.write(count, 10, str(value[i]) + '  ') #descrip
            elif i == 4:
                worksheet.write(count, 12, str(value[i]) + '  ') #rtype
            elif i ==6:
                worksheet.write(count, 20, str(value[i]) + '  ') #hash





    count += 1
workbook.close() #closing workbook
print("done")







