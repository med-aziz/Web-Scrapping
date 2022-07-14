from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import csv
from tkinter import *
from tkinter import filedialog
from win32api import GetSystemMetrics

# Making application screen
root = Tk()                 

def window(mainscreen):
    mainscreen.update_idletasks()
    # change screen title
    mainscreen.title("NewEgg Product Manager")
    # Change window pop-up Position
    mainscreen.geometry('+0+0')
    # Changing window icon
    #mainscreen.icon()


window(root)



class NewEggScrapper:
    def __init__(self,master):
        self.master = master
        self.fileName = ""
        self.link = ""
        self.path = ""
        self.itemsPossibleSpecs = []
        self.itemsPossibleSpecs.append("Name")
        self.itemsPossibleSpecs.append("Characteristics")
        #self.fillCsvWithData("D://Python Repertory//Web Scrapping 101//")
        # making canvas
        #self.canvas = Canvas(master, height= GetSystemMetrics(1), width= GetSystemMetrics(0), bg='#AE7F51')
        self.canvas = Canvas(master, height= GetSystemMetrics(1), width= GetSystemMetrics(0), bg='#AE7F51')
        self.canvas.pack()
        # making frame
        self.frame = Frame(master, bg= '#AEAE51')
        #relheight, relwidth − Height and width as a float between 0.0 and 1.0, as a fraction of the height and width of the parent widget.
        #relx, rely − Horizontal and vertical offset as a float between 0.0 and 1.0, as a fraction of the height and width of the parent widget.
        self.frame.place(relwidth= 0.8, relheight= 0.8, relx= 0.1, rely= 0.1)
        # Making newEgg Category link Label
        self.link = Label(self.frame, text= "Newegg Category Link:", bg='#AE5151', fg= 'white')
        self.link.config(font=('TkDefaultFont', 10)) 
        self.link.grid(row=0, column=0, sticky=E, padx=10,pady=10)
        # Making newEgg Category link field
        self.linkField = Entry(self.frame)
        self.linkField.grid(row=1, column=0, pady=10)
        # Making LookforData Button
        self.searchDataButton = Button(self.frame, text='Search For Data', bg='#FF0E00', fg= 'white', command= self.fillCsvWithData)
        self.searchDataButton.grid(row=4, column=0, padx=10, pady=10)
        # Making Choose file Path Button
        self.chooseFilePathButton = Button(self.frame, text='Choose File Path', bg='#AE5151', fg= 'white', command= self.choosePath)
        self.chooseFilePathButton.grid(row=5, column=0, pady=10, padx=10)
        # Making fileName label
        self.fileN= Label(self.frame, text= "File Name: ", bg='#AE5151', fg= 'white')
        self.fileN.config(font=('TkDefaultFont', 10))
        self.fileN.grid(row=2, column=0, pady=10, padx=10) 
        # Making file Name Entry:
        self.fileNameField = Entry(self.frame)
        self.fileNameField.grid(row=3, column=0, pady=10)
    def choosePath(self):
        fileFolder = filedialog.askdirectory()
        self.path = fileFolder.replace("/", "//")
        try:
            self.pathLabel = Label()
            self.pathLabel.destroy()
        except:
            pass
        self.pathLabel = Label(self.frame, text= self.path, bg='#AE5151', fg= 'white')
        self.pathLabel.config(font=('TkDefaultFont', 10))
        self.pathLabel.grid(row=5, column=1, pady=10)
    def getLink(self):
        self.link = self.linkField.get()
        return self.link
    def getFileName(self):
        self.fileName = self.fileNameField.get()
        return self.fileName
    def getSoup(self, link):
        # getting a link and returning soup
        uClient = uReq(link)
        page = uClient.read()
        uClient.close()
        return soup(page, 'lxml')
    def getItemContainers(self, soup_page):
        item_containers = soup_page.findAll('div', class_='item-container')
        return item_containers
    def getItemPageData(self, item_container):
        itemPageLink =item_container.a["href"]
        return self.getSoup(itemPageLink)
    def getItemCharacteristics(self, itemDataPage):
        itemCharac = ""
        itemCharacList = itemDataPage.findAll('div', class_= 'product-bullets')[0]
        itemCharacData = itemCharacList.ul.findAll('li')
        for item in itemCharacData:
            itemCharac = itemCharac + item.text.strip()
        return (itemCharac.replace(",","|")).replace("\n", "||")
    def getItemSpecs(self, itemDataPage):
        #Creating a spec table in the form of [spec_name, spec_info, spec_name, spec_info, ........]
        specs = []
        itemSpecsTables = itemDataPage.findAll('table', class_= 'table-horizontal')
        specs.append("Name")
        specs.append((itemDataPage.find('h1' , class_='product-title')).text.strip())
        specs.append("Characteristics")
        specs.append(self.getItemCharacteristics(itemDataPage))
        for table in itemSpecsTables:
            for specPart in table.findAll('tr'):
                specs.append(specPart.th.text.strip())
                specs.append(specPart.td.text.strip())
                specName = specPart.th.text.strip()
                if not(specName in self.itemsPossibleSpecs):
                    self.itemsPossibleSpecs.append(specName)
        return specs
    def fillCsvWithData(self):
        allIemsData = []
        item_containers = self.getItemContainers(self.getSoup(self.getLink()))
        path_to_use = self.path + "//" + self.getFileName() + ".csv"
        csvFile = open(path_to_use, 'w')
        csvWriter = csv.writer(csvFile, lineterminator = '\n')
        i = 0
        for item in item_containers:
            itemPage = self.getItemPageData(item)
            itemSpecs = self.getItemSpecs(itemPage)
            allIemsData.append(itemSpecs)
            i+= 1
            if i == 9:
                break
        csvWriter.writerow(self.itemsPossibleSpecs)
        for itemdata in allIemsData:
            toWrite = []
            for possibleSpec in self.itemsPossibleSpecs:
                if (possibleSpec in itemdata):
                    index = itemdata.index(possibleSpec)
                    toWrite.append(itemdata[index+1])
                else:
                    toWrite.append("Unknown")
            csvWriter.writerow(toWrite)
        csvFile.close()
        print(allIemsData[0])
        

g = NewEggScrapper(root)

#ScrappyUi(root, NewEggScrapper())
root.mainloop()