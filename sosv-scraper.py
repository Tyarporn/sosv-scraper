from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv

'''
TO DO! 
- Run the code to see if it works
'''


class Company:
    def __init__(self, name, founder, linkedin, website, description, location):
        self.name = name
        self.founder = founder
        self.linkedin = linkedin
        self.website = website
        self.description = description
        self.location = location


# you have to download a web driver for this to work (I used chrome)
'''put your driver path here!!'''
driver_path = "/Users/tyarpornsuksant/Downloads/chromedriver"
driver = webdriver.Chrome(driver_path)

names = []
founders = []
linkedins = []
websites = []
descriptions = []
locations = []
hrefs = []
company_hrefs = []
page_number = 1
max_pages = 6

# program = 'Chinaccelerator'
# program = 'HAX'
# program = 'MOX'
# program = 'dlab'
# program = 'Food-X'
# program = 'IndieBio'
# program = 'RebelBio'

programs = ['Chinaccelerator', 'HAX', 'MOX', 'dlab', 'Food-X', 'IndieBio', 'RebelBio']

for program in programs:
    while page_number <= max_pages:
        # directory_url = "https://sosv.com/portfolio/?program=HAX&stage=Accelerator%2CPre-seed%2CSeed&page=" + str(page_number)
        directory_url = "https://sosv.com/portfolio/?program=" + program + "&stage=Program%2CPre-seed%2CSeed&page=" + str(
            page_number)
        driver.get(directory_url)
        time.sleep(3)  # for page to load
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        # print(soup)
        titles_raw = soup.find_all('p', class_="card-title sosv-h2")
        descriptions_raw = soup.find_all('p', class_="card-text sosv-text")
        location_raw = soup.find_all('footer', class_="sosv-location-text")
        hrefs = soup.find_all('a', class_="card-body p-3 d-flex flex-column justify-content-between")
        for t in titles_raw:
            try:
                names.append(t.text)
            except:
                print("name for " + t + " not found")
                names.append(" ")
        for d in descriptions_raw:
            try:
                descriptions.append(d.text)
            except:
                print("description for " + d + " not found")
                descriptions.append(" ")
        for l in location_raw:
            try:
                locations.append(l.text)
            except:
                print("location for " + l + " not found")
                locations.append(" ")
        for h in hrefs:
            try:
                company_hrefs.append(h['href'])
            except:
                print("href not found")
                company_hrefs.append("xxxxx")
        page_number += 1

    iso_url = "https://sosv.com"
    for link in company_hrefs:
        iso_com_url = iso_url + link
        driver.get(iso_com_url)
        iso_src = driver.page_source
        iso_soup = BeautifulSoup(iso_src, 'html.parser')
        try:
            websites_links_raw = iso_soup.find_all('a', class_="sosv-link-dark mb-3")
            weblinks = []
            wn = 1
            for w in websites_links_raw:
                if w['href'][0] == "h":
                    websites.append(w['href'])
                    break
                else:
                    wn += 1
            if wn == len(websites_links_raw) + 1:
                print("website not found")
                websites.append(" ")
        except:
            print("website for " + link + " not found")
            websites.append(" ")
        company_ppl = iso_soup.find('div', class_="company-people col")
        try:
            founder = company_ppl.find('p', class_="sosv-text mb-1")
            striped = founder.text.strip()
            n = striped.find("\n")
            striped_striped = striped[0:n]
            founders.append(striped_striped)
        except:
            print("founder for " + link + " not found")
            founders.append(" ")
        try:
            linkedin = company_ppl.find('a', {'title': 'LinkedIn'})['href']
            linkedins.append(linkedin)
        except:
            print("linkedin for " + link + " not found")
            linkedins.append(" ")

    print(str(len(names)) + "names")
    print(str(len(founders)) + "founders")
    print(str(len(linkedins)) + "linkedins")
    print(str(len(websites)) + "websites")
    print(str(len(descriptions)) + "descriptions")
    print(str(len(locations)) + "locations")

    print(names)
    print(websites)

    companies = []
    for r in range(len(names)):
        companies.append(Company(names[r], founders[r], linkedins[r], websites[r], descriptions[r], locations[r]))

    with open(program + 'info.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["title", "founders", "linkedin", "website", "description", "location"])
        for company in companies:
            try:
                writer.writerow([company.name, company.founder, company.linkedin, company.website, company.description,
                                 company.location])
                print(company.name + " was recorded")
            except:
                print("There was something wrong with " + company.name + ". It could not be recorded")
