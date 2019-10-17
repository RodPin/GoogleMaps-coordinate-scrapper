import unittest
import collections
from selenium import webdriver
from DriverConfig import DriverConfig
from time import sleep
from selenium.webdriver.common.keys import Keys

chrome_options = DriverConfig.get_options()
driver = webdriver.Chrome(options=chrome_options, executable_path=DriverConfig.get_system_driver())

driver.get("https://www.google.com.br/maps")

#Adjusts between the center of screen and the marker, according to the zoom
ZoomAdjust = {
    '4':[0.0, 0.0],
    '6':[0.0 ,0.0],
    '9':[0.0, 0.0],
    '10':[0.0, 0.0],
    '11':[0.0, 0.0],
    '12':[0.0, 0.0],
    '14':[0.0, 0.0],
    # '15':[0.0000004,0.0021883],
    '15':[0.0,0.0],
    '16':[0.0, 0.0],
    '17':[0.0000001,0.0021892],
    '18':[0.0,0.0],
    '19':[0.0,0.0]
}

def searchOnMaps(endereco):
    digitarEndereco = driver.find_element_by_id("searchboxinput")
    digitarEndereco.clear()
    digitarEndereco.send_keys(endereco)
    digitarEndereco.send_keys(Keys.ENTER)
    sleep(4)
    #If google find more than one result,our program will click at the first one
    elements = driver.find_elements_by_class_name('section-result')
    if elements is not None and len(elements) > 0:
        elements[0].click()
        sleep(3)
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
    zoom=arrayLatLongZoom[2][:-1]
    
    if zoom in ZoomAdjust and int(zoom) == 17:
        latitude=float(latitude)-float(ZoomAdjust[zoom][0])
        longitude=float(longitude) + float(ZoomAdjust[zoom][1])
        print('LatitudeLongitude: '+ str(latitude)+' '+ str(longitude)+ '     Zoom: '+zoom)
        return [str(latitude),str(longitude),zoom]
    else:
        print('LatitudeLongitude: '+ str(latitude)+' '+ str(longitude) + '    Zoom:'+zoom)
        return ['ERRO','erro',zoom]

if __name__ == '__main__':
    #Here you choose your file name
    filepath="./address.txt"
    f = open(filepath,"r")
    content = f.readlines()
    f.close()
    organs = {}
    addresses = set()
    address=''
    for line in content:
        if filepath[-4:]=='.csv':
            data = line.split(';')
            # Creating the adress from a csv file, edit here in your way
            address = " , ".join([data[2] + ' ' + data[3], data[4], data[5], data[7], data[8]])
        else:
            address=line
        addresses.add(address)
        if address in organs:
            organs[address] += [line]
        else:
            organs[address] = [line]
    coordinates = []
    zoom_count = {}
    new_lines = ""
    for address in addresses:
        lat_lon = searchOnMaps(address)
        coordinates.append(lat_lon)
        if lat_lon[-1] in zoom_count:
            zoom_count[lat_lon[-1]] += 1
        else:
            zoom_count[lat_lon[-1]] = 1
        for i in range(len(organs[address])):
            address_list = organs[address] 
            string = address_list[i]
            if filepath[-4:]=='.csv':
                address_list[i] = string.rstrip('\n')[:-1] + lat_lon[0] + ";" + lat_lon[1]
            else:
                address_list[i] = string.rstrip('\n')+';'+ lat_lon[0] + ";" + lat_lon[1]
            organs[address] = address_list
            new_lines += organs[address][i] + '\n'
    new_file = open('./adress_lat_lon.txt', 'w')
    new_file.write(new_lines)
    new_file.close()             
    print(zoom_count)
    driver.quit()