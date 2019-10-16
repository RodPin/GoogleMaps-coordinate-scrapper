import unittest
import collections
from selenium import webdriver
from DriverConfig import DriverConfig
from time import sleep
from selenium.webdriver.common.keys import Keys

chrome_options = DriverConfig.get_options()
driver = webdriver.Chrome(options=chrome_options, executable_path=DriverConfig.get_system_driver())

driver.get("https://www.google.com.br/maps")
def searchOnMaps(endereco):
    digitarEndereco = driver.find_element_by_id("searchboxinput")
    digitarEndereco.clear()
    digitarEndereco.send_keys(endereco)
    digitarEndereco.send_keys(Keys.ENTER)
    sleep(4)
    # clickar=driver.find_element_by_class_name("section-result-header")
    # if clickar:
    #     clickar.click()
    # sleep(2)
    url = driver.current_url

    def find_between( s, first, last ):
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return s[start:end]
        except ValueError:
            return ""

    latLongZoom= find_between(url,'@','/')
    arrayLatLongZoom=latLongZoom.split(",")
    latitude=arrayLatLongZoom[0]
    longitude=arrayLatLongZoom[1]
    # print(float(latitude)-float(0.0001271))
    # print(float(longitude) + float(0.0021159))
    
    if arrayLatLongZoom[2][1]!='z':
        zoom=arrayLatLongZoom[2][0]+arrayLatLongZoom[2][1]
      
    else:
        zoom=arrayLatLongZoom[2][0]

    if int(zoom)>15:
        latitude=float(latitude)-float(0.0001271)
        longitude=float(longitude) + float(0.0021159)
        print('LatitudeLongitude: '+ str(latitude)+' '+ str(longitude)+ '     Zoom: '+zoom)
        return [str(latitude),str(longitude),zoom]
    else:
        print('LatitudeLongitude: '+ str(latitude)+' '+ str(longitude) + '    Zoom:'+zoom)
        return ['ERRO','erro',zoom]

# sleep(10)
# driver.quit()
latLong=[]
ocurrencyArray=[]
def treatList(i,count):
    ## SEARCH ON MAP
    ocurrencyArray

    endereco=f[i][8]+' '+f[i][3]+' '+f[i][4]+' '+f[i][5]
    latLong=searchOnMaps(endereco) 
    if count>0:
        for x in range(count+1):
            # f[i-x][9]=str(count) ##USE RESULTS
            # f[i-x][10]=str(count) ##USE RESULTS
            f[i-x][9]=latLong[0]
            f[i-x][10]=latLong[1]
            ocurrencyArray.append(latLong[2])

    else:
        f[i][9]=latLong[0]
        f[i][10]=latLong[1]
        ocurrencyArray.append(latLong[2])




f= open("./adress","r").readlines()

# lat='5.3171555'
# longs='-41.5828389'   
# print(f[1])
# f[1]=f[1].split(',')
# f[1][9]=lat   
# f[1][10]=longs
pool=4
for x in range(pool):
    f[x]=f[x].split(';')

count=0

for i in range(pool):
    if f[i][3] == f[i+1][3] and f[i][2] == f[i+1][2] and f[i][4] == f[i+1][4] and f[i][5] == f[i+1][5] and f[i][8] == f[i+1][8]:
        count=count+1
    else:
        #Pesquisa coordenadas
        #i, contador,
        # print(f[i][3])
        treatList(i,count)
        count=0
    
errorCount=0
for i in range(pool):
    if f[i][10]=='erro':
        errorCount=errorCount+1
    virgula=','
    f[i]=virgula.join(f[i])
    # print(f[i])
print('ERRORS:')
print(errorCount)
print('ZOOMS:')
print(collections.Counter(ocurrencyArray))