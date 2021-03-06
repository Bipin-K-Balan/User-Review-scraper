from flask import Flask, render_template, request,jsonify
# from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as ureq
import csv

class Scrapper():
    def __init__(self,keyword):

        self.keyword = keyword
    
    def scrape(self):

        filename = self.keyword+".csv"
        r =[]
        with open(filename, 'w',encoding="utf-8") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["ratings","headings","reviews"])


            for i in range(1,2):
                url = 'https://www.flipkart.com/search?q='+self.keyword+"&page="+str(i)
                uclient = ureq(url)
                page_a = uclient.read()
                uclient.close()

                html_a = bs(page_a,'html.parser')
                links_a = html_a.findAll('a',{"class":"_1fQZEK"})

                link_list = []
                for i in range(len(links_a)):
                    link_list.append(links_a[i]['href'])

                for i in range(len(link_list)):
                    pdctlink = 'https://www.flipkart.com'+link_list[i]
                    uclients = ureq(pdctlink)
                    page_b = uclients.read()
                    uclients.close()
                    html_b = bs(page_b,'html.parser')
                    links_b = html_b.findAll('a',href=True)
                    l1 = [links_b[i]['href'] for i in range(len(links_b)) if "/product-reviews/" in links_b[i]['href']]

                    for i in range(1,2):
                        reviewlink= 'https://www.flipkart.com'+l1[0]+"&page="+str(i)
                        uclientss = ureq(reviewlink)
                        page_c = uclientss.read()
                        uclientss.close()
                        html_c = bs(page_c,'html.parser')

                        rating = html_c.findAll('div',{'class':'_3LWZlK _1BLPMq'})
                        heading = html_c.findAll('p',{'class':'_2-N8zT'})
                        review = html_c.findAll('div',{'class':'t-ZTKy'})

                        
                        
                        for i in range(len(rating)):
                            csvwriter.writerow([rating[i].text,heading[i].text,review[i].text])
                            my_dict = {"Rating":rating[i].text,"Title":heading[i].text, "Review": review[i].text}
                            r.append(my_dict)

        return r