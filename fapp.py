from flask import Flask,render_template,request,session,flash,redirect,url_for

import os
#import test
import importlib

from os.path import dirname, abspath

#from bs4 import BeautifulSoup as soup
#from urllib.request import urlopen as uReq 
#import json

#amazon
import urllib.request
from bs4 import BeautifulSoup
import json
import re

#flip
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq 

import datetime

import random

app=Flask(__name__)

@app.route('/')
def indexda():
        loadfolder=os.path.dirname(os.path.abspath(__file__))
        finalfolder=os.path.join(loadfolder,'test_images')

        for the_file in os.listdir(finalfolder):
                file_path = os.path.join(finalfolder, the_file)
                try:
                 if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                        print(e)  

        imgfolder=os.path.join(loadfolder,'images')
        for the_file in os.listdir(imgfolder):
                file_path = os.path.join(imgfolder, the_file)
                try:
                 if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                        print(e)  


        stafolder=os.path.join(loadfolder,'static/result_img')
        for the_file in os.listdir(stafolder):
                file_path = os.path.join(stafolder, the_file)
                try:
                 if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                        print(e) 
        
        


        return render_template('index2.html')

@app.route('/set')
def index():
    
    #reval=test.main()

    #curefilepath=os.path.dirname(os.path.abspath(__file__))

    #print(curefilepath)
    return render_template('home.html')
    # return a

@app.route('/detectresult',methods=['POST'])
def detectresult():
    curefilepath=os.path.dirname(os.path.abspath(__file__))
    
    productjson=os.path.join(curefilepath,'Products/')

    print(curefilepath)
    target=os.path.join(curefilepath,'images')
    # if not os.path.isdir(target):
    #     os.mkdir(target)
    for file in request.files.getlist('file'):
        #print(file)
        filename=file.filename
        destination="/".join([target,filename])
        print(destination)
        file.save(destination)
        session['picpath']=destination
    import test
    importlib.reload(test)
    reval=test.main()
    print("******",reval,"******")

    uperlist=[]
    
    for hj in reval:
            innerlist=[]
            innerlist.append (hj)
            innerlist.append(reval[hj])
            uperlist.append(innerlist)
    
    if reval!="":
         return render_template('inerresultpage.html',res=uperlist,picpath=session['picpath'])
    else:
         return render_template('inerresultpage.html',res=uperlist,picpath=session['picpath'])



@app.route('/nextcrop/<string:key>',methods=['GET','POST'])
def nextcrop(key):
        

            
    curefilepath=os.path.dirname(os.path.abspath(__file__))
    productjson=os.path.join(curefilepath,'Products/')
    fetchfile=key+".json"
    status=" "
    allpimgpath=os.path.join(productjson,'allimg.json')
    if os.path.exists(allpimgpath):
            pimglist=json.load(open(allpimgpath))


    json_url=os.path.join(productjson,fetchfile)
    if os.path.exists(json_url):
            modiedlist=[]
            jsondata=json.load(open(json_url))
            for iltr in jsondata:
                    proimgurl=random.choice(pimglist)
                    iltr['showimg']=proimgurl
                    modiedlist.append(iltr)

    else:
            modiedlist=["no data"]
            status="currently no data available for "+key
        

    if key!="":
         return render_template('detectionresult.html',res=key,picpath=session['picpath'],jdata=modiedlist,status=status)
    else:
         return render_template('detectionresult.html',res=key,picpath=session['picpath'],jdata=modiedlist,status=status)








    
@app.route('/back',methods=['POST'])
def back():
    #sys.exit()
    picpath=session['picpath']
    os.remove(picpath)
    return render_template('home.html')



@app.route('/show')
def show():
        curefilepath=os.path.dirname(os.path.abspath(__file__))
        json_url=os.path.join(curefilepath,"allinoneda.json")
        print('***************',json_url)
        if os.path.exists(json_url):
            jsondata=json.load(open(json_url))
            #print('jsondatanoooo')
        else:
            jsondata="[no data]"
            #print('____________________________bzzzzzzzzzzzzzzzzzzz')
        reval='just try'
        tryimg='just try'
        return render_template('detectionresult.html',res=reval,picpath=tryimg,jdata=jsondata)

    





@app.route('/admin',methods=['GET','POST'])
def admin():
    if request.method=='POST':
        userid = request.form['userid']
        pwd = request.form['pwd']
        if userid=='123' and pwd=='123':
            return render_template('adminhome.html')
        
    return render_template('login.html')









@app.route('/amzscrap',methods=['GET','POST'])
def amzscrap():
        curefilepath=os.path.dirname(os.path.abspath(__file__))
        target=os.path.join(curefilepath,'Products/')
        now = datetime.datetime.now()
        now=str(now)
        if request.method=='POST':
                brandname=request.form['brandname']
                amz_url = request.form['aurl']
                keywords=request.form['amzkeyword']

                keywordsplit=keywords.lower()
                brandnameinlist=keywordsplit.split(" ")
                brandnameinlist.append(" ")

                url=amz_url
                headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}
                requestvar = urllib.request.Request(url,headers=headers)
                html = urllib.request.urlopen(requestvar).read()
                soupa = BeautifulSoup(html,'html.parser')
                pagenav=soupa.find("ul",attrs={'class':'a-pagination'})
                allpagelink=[]
                allpagelink=pagenav.findAll("li",{"class": "a-normal"})
                firstlink=pagenav.findAll("li",{"class": "a-selected"})
                allpagelink.insert(0,firstlink[0])
                extracted_records = []
                imglinks=[]
                for li,pagenum in zip(allpagelink,range(len(allpagelink))):
                        filename = "AMALamazon"+str(pagenum)+".json"
                        pages_url = "http://www.amazon.in"+li.a.get('href')
                        #print(pages_url)
                        innerrequest = urllib.request.Request(pages_url,headers=headers)
                        html = urllib.request.urlopen(innerrequest).read()
                        innersoupa = BeautifulSoup(html,'html.parser')
                        main_table = innersoupa.find_all("div",attrs={'class':'a-section a-spacing-medium'})
                        for i in main_table:
                                try:

                                          
                                        links = i.find("a",class_="a-link-normal a-text-normal")
                                        title = links.text.strip()
                                        filtertitle=title.lower()
                                        url = links['href']
                                        if not url.startswith('http'):
                                                url = "https://www.amazon.in"+url
                                        prices = i.find("span",class_="a-price-whole")
                                        amount=prices.text
                                        image = i.a.img["src"]
                                        titsplit=title.split('(')
                                        productname=titsplit[0]
                                        if brandnameinlist[0] in filtertitle and brandnameinlist[1] in filtertitle:
                                                pass
                                        else:
                                             continue   
                                except Exception:
                                        print("some went wrong..")
                                        continue
                                record ={
                                        'product':title,
                                        'proname':productname,
                                        'price':amount,
                                        'url':url,
                                        'image':image,
                                        }
                                extracted_records.append(record)
                                imglinks.append(image)
                                print(record)
                
                datatarget=target+'amz'+keywords+'.json'

                imgtarget=target+'amzimg'+keywords+'.json'
                
                linktarget=target+'linkmanagment.json'

                brandtarget=target+brandname+'.json'

                brandflag=0
                if os.path.exists(brandtarget):
                        brandnamelist={
                                'site':'Amazon',
                                'Keyword':keywords,
                                'filename':'amz'+keywords+'.json',
                                'Scraptime':now,
                                'Link':amz_url,
                        }
                        forupdate=[]
                        jsonbrandname=json.load(open(brandtarget))
                        for qw in jsonbrandname:
                                if qw['Keyword']==keywords:

                                        updatedbrandnamelist={
                                                'site':'Amazon',
                                                'Keyword':keywords,
                                                'filename':'amz'+keywords+'.json',
                                                'Scraptime':now,
                                                'Link':amz_url,
                                                }
                                        forupdate.append(updatedbrandnamelist)
                                        brandflag=1
                                else:
                                       forupdate.append(qw) 

                        if brandflag==0:
                                jsonbrandname.append(brandnamelist)
                                with open(brandtarget, 'w') as outfile12:
                                        json.dump(jsonbrandname, outfile12, indent=4)
                        
                        if brandflag==1:
                                with open(brandtarget, 'w') as outfile14:
                                        json.dump(forupdate, outfile14, indent=4)
                                print("aa")



                        
                else:
                        brandnamelist=[{
                                'site':'Amazon',
                                'Keyword':keywords,
                                'filename':'amz'+keywords+'.json',
                                'Scraptime':now,
                                'Link':amz_url,
                        }]
                        with open(brandtarget, 'w') as outfile11:
                                json.dump(brandnamelist, outfile11, indent=4)

                

                flag=0
                if os.path.exists(linktarget):
                        linkman={
                                'site':'Amazon',
                                'Link':amz_url,
                                'Keyword':keywords,
                                'Scraptime':now,
                        }
                        jsonlink=json.load(open(linktarget))
                        for ij in jsonlink:
                                if ij['Keyword']==keywords:

                                        flag=1
                        if flag==0:

                                jsonlink.append(linkman)
                                with open(linktarget, 'w') as outfile2:
                                        json.dump(jsonlink, outfile2, indent=4)

                        
                        
                else:
                        linkman=[{
                                'site':'Amazon',
                                'Link':amz_url,
                                'Keyword':keywords,
                                'Scraptime':now,
                        }]
                        with open(linktarget, 'w') as outfile2:
                                json.dump(linkman, outfile2, indent=4)

                with open(datatarget, 'w') as outfile:
                        json.dump(extracted_records, outfile, indent=4)
                
                with open(imgtarget, 'w') as outfile3:
                        json.dump(imglinks, outfile3, indent=4)

                #return render_template('amzproductscrap.html',url=a
                return render_template('allproduct.html',alldata=extracted_records,res=keywords)
        return render_template('amzproductscrap.html')



#flip
@app.route('/flipscrap',methods=['GET','POST'])
def flipscrap():
        curefilepath=os.path.dirname(os.path.abspath(__file__))
        target=os.path.join(curefilepath,'Products/')
        target1=os.path.join(curefilepath,'Products/')
        target2=os.path.join(curefilepath,'Products/')
        now = datetime.datetime.now()
        now=str(now)
        fordropdownlist=os.path.join(curefilepath,'Products/linkmanagment.json')
        if os.path.exists(fordropdownlist):
                passkeylist=[]
                dropdowndata=json.load(open(fordropdownlist))
                for ik in dropdowndata:
                        passkeylist.append(ik['Keyword'])

        else:
                passkeylist=[]


        if request.method=='POST':
                brandname=request.form['brandname']
                flip_url = request.form['aurl']
                keywords=request.form['flipkeyword']

                keywordsplit=keywords.lower()
                brandnameinlist=keywordsplit.split(" ")
                brandnameinlist.append(" ")

                forimglist=os.path.join(curefilepath,'Products/amzimg'+keywords+'.json')
                print("______",forimglist,"____")
                if os.path.exists(forimglist):
                        
                        imgcontainerlist=json.load(open(forimglist))
                else:
                        imgcontainerlist=['nopic','picno']


                my_url=flip_url
                uClient = uReq(my_url)
                page_html = uClient.read()
                uClient.close()
                page_soup = soup(page_html,"html.parser")
                containers = page_soup.findAll("div",{"class": "_2zg3yZ"})
                container = containers[0]
                links = container.findAll("a",{"class":"_2Xp0TH"})
                extracted_records=[]

                try:
                        for li,fnum in zip(links,range(len(links))):

                                filename = "product"+str(fnum)+".json"
                                print(filename)
                                pages_url="http://www.flipkart.com"+li['href']
                                uinnerClient = uReq(pages_url)
                                pageinner_html = uinnerClient.read()
                                uinnerClient.close()
                                pageinner_soup = soup(pageinner_html,"html.parser")
                                containers = pageinner_soup.findAll("div",{"class": "_3O0U0u"})
                                container = containers[0]
                                price = container.findAll("div",{"class": "col col-5-12 _2o7WAb"})
                                ratings = container.findAll("div",{"class":"niH0FQ"})
                                links = container.findAll("a",{"class":"_31qSD5"})
                                url=links[0]['href']
                                for container in containers:

                                        product_name = container.div.img["alt"]
                                        pname=product_name.replace(",","|")
                                        filtertitle=pname.lower()

                                        links = container.findAll("a",{"class":"_31qSD5"})
                                        url=links[0]['href']
                                        price_container = container.findAll("div",{"class": "col col-5-12 _2o7WAb"})
                                        price = price_container[0].text.strip()
                                        rm_rupee = price.split("₹")
                                        add_rs_price = "Rs"+rm_rupee[1]
                                        split_price = add_rs_price.split('E')
                                        final_price = split_price[0]
                                        last_price = final_price.replace("No Cost","")
                                        if not url.startswith('http'):
                                                url = "https://www.flipkart.com"+url
                                        imgurl=random.choice(imgcontainerlist)

                                        if brandnameinlist[0] in filtertitle and brandnameinlist[1] in filtertitle:
                                                pass
                                        else:
                                             continue

                                        fliprecord ={
                                                'product':product_name.replace(",","|"),
                                                'price':last_price,
                                                'url':url,
                                                'img':imgurl,
                                                }
                                        extracted_records.append(fliprecord)
                except(Exception):

                        print("data scrapped successfully")

                target=target+'flip'+keywords+'.json'

                linktarget=target1+'flipkartlinkmanagment.json'

                brandtarget=target2+'f'+brandname+'.json'
                brandflag=0
                if os.path.exists(brandtarget):
                        brandnamelist={
                                'site':'flipkart',
                                'Keyword':keywords,
                                'filename':'flip'+keywords+'.json',
                                'Scraptime':now,
                                'Link':url,
                        }
                        flipforupdate=[]
                        jsonbrandname=json.load(open(brandtarget))
                        for qw in jsonbrandname:
                                if qw['Keyword']==keywords:
                                        print("hahahhahahahah_____")
                                        updatedbrandnamelist={
                                                'site':'flipkart',
                                                'Keyword':keywords,
                                                'filename':'flip'+keywords+'.json',
                                                'Scraptime':now,
                                                'Link':url,
                                                }
                                        flipforupdate.append(updatedbrandnamelist)
                                        brandflag=1
                                else:
                                       flipforupdate.append(qw)
                        if brandflag==0:
                                jsonbrandname.append(brandnamelist)
                                with open(brandtarget, 'w') as outfile12:
                                        json.dump(jsonbrandname, outfile12, indent=4)
                        if brandflag==1:
                                with open(brandtarget, 'w') as outfile14:
                                        json.dump(flipforupdate, outfile14, indent=4)
                                        print("aa")
                        
                        

                                        
                else:
                        brandnamelist=[{
                                'site':'Flipkart',
                                'Keyword':keywords,
                                'filename':'flip'+keywords+'.json',
                                'Scraptime':now,
                                'Link':url,
                        }]
                        with open(brandtarget, 'w') as outfile21:
                                json.dump(brandnamelist, outfile21, indent=4)

                flag=0
                if os.path.exists(linktarget):

                        linkmangement={
                                'site':'Flipkart',
                                'Link':flip_url,
                                'Keyword':keywords,
                                'Scraptime':now,
                        }

                        jsonlink=json.load(open(linktarget))
                        for kl in jsonlink:
                                if kl['Keyword']==keywords:
                                        flag=1
                        if flag==0:
                                jsonlink.append(linkmangement)
                                with open(linktarget, 'w') as outfile2:
                                        json.dump(jsonlink, outfile2, indent=4)




                else:
                        linkmangement=[{
                                'site':'Flipkart',
                                'Link':flip_url,
                                'Keyword':keywords,
                                'Scraptime':now,
                        }]
                        with open(linktarget, 'w') as outfile5:
                                json.dump(linkmangement, outfile5, indent=4)


                with open(target, 'w') as outfile:
                        json.dump(extracted_records, outfile, indent=4)
                
    
                return render_template('flipkallproduct.html',alldata=extracted_records,res=keywords)    

        return render_template('flipkartroductscrap.html',passkeylist=passkeylist)







@app.route('/allproduct',methods=['GET','POST'])
def allproduct():
        return render_template('allproduct.html')


@app.route('/finalpageamz/<string:key>',methods=['GET','POST'])
def finalpageamz(key):
        filename=key
        curefilepath=os.path.dirname(os.path.abspath(__file__))
        target=os.path.join(curefilepath,'Products/amz'+filename+'.json')
        if os.path.exists(target):
                jsondata=json.load(open(target))
        else:
                jsondata=[]
        return render_template('finalpageamz.html',finalamzdata=jsondata,brand=key)

@app.route('/finalpageflipkart/<string:key>',methods=['GET','POST'])
def finalpageflipkart(key):
        filename=key
        curefilepath=os.path.dirname(os.path.abspath(__file__))
        target=os.path.join(curefilepath,'Products/flip'+filename+'.json')
        if os.path.exists(target):
                jsondata=json.load(open(target))
        else:
                jsondata=[]
        return render_template('finalpageflipkart.html',finalamzdata=jsondata,brand=key)




@app.route('/amzscraplinks',methods=['GET','POST'])
def amzscraplinks():
        curefilepath=os.path.dirname(os.path.abspath(__file__))
        target=os.path.join(curefilepath,'Products/linkmanagment.json')
        if os.path.exists(target):
            jsondata=json.load(open(target))
            return render_template('amzscraplinks.html',linkdata=jsondata)

        return render_template('amzscraplinks.html')


@app.route('/amzbrandlist',methods=['GET','POST'])
def amzbrandlist():
        return render_template('amzbrandlist.html')


@app.route('/flipbrandlist',methods=['GET','POST'])
def flipbrandlist():
        return render_template('flipbrandlist.html')



@app.route('/amzbrandlistingresult/<string:key>',methods=['GET','POST'])
def amzbrandlistingresult(key):
        #print("***",key,"*****")
        curefilepath=os.path.dirname(os.path.abspath(__file__))
        target=os.path.join(curefilepath,'Products/'+key+'.json')
        if os.path.exists(target):
            jsondata=json.load(open(target))
            return render_template('amzbrandlistingresult.html',brandlist=jsondata,brandname=key)
        return render_template('amzbrandlistingresult.html')



@app.route('/flipbrandlistingresult/<string:key>',methods=['GET','POST'])
def flipbrandlistingresult(key):
        #print("***",key,"*****")
        curefilepath=os.path.dirname(os.path.abspath(__file__))
        target=os.path.join(curefilepath,'Products/f'+key+'.json')
        if os.path.exists(target):
            jsondata=json.load(open(target))
            return render_template('flipbrandlistingresult.html',brandlist=jsondata,brandname=key)
        return render_template('flipbrandlistingresult.html')




@app.route('/flipkartscraplinks',methods=['GET','POST'])
def flipkartscraplinks():
        curefilepath=os.path.dirname(os.path.abspath(__file__))
        target=os.path.join(curefilepath,'Products/flipkartlinkmanagment.json')
        if os.path.exists(target):
            jsondata=json.load(open(target))
            return render_template('flipscraplinks.html',linkdata=jsondata)

        return render_template('flipscraplinks.html')




@app.route('/linkwiselist/<string:key>')
def linkwiselist(key):
        curefilepath=os.path.dirname(os.path.abspath(__file__))
        target=os.path.join(curefilepath,'Products/')
        datatarget=target+'amz'+key+'.json'
        if os.path.exists(datatarget):
                jsondata=json.load(open(datatarget))
        
        return render_template('allproduct.html',alldata=jsondata,res=key)




@app.route('/updateamz/<string:key>',methods=['GET','POST'])
def updateamz(key):
        key=key.split(",")
        curefilepath=os.path.dirname(os.path.abspath(__file__))
        target=os.path.join(curefilepath,'Products/linkmanagment.json')
        if os.path.exists(target):
                editdata=[]
                jsondata=json.load(open(target))
                for i in jsondata:
                        if i["Keyword"]== key[0]:
                                editdata.append(key[0])
                                editdata.append(i['Link'])


                                


                
        return render_template('editamzscraplinks.html',editdata=editdata,brandname=key[1])




@app.route('/fliplinkwiselist/<string:key>')
def fliplinkwiselist(key):
        curefilepath=os.path.dirname(os.path.abspath(__file__))
        target=os.path.join(curefilepath,'Products/')
        datatarget=target+'flip'+key+'.json'
        if os.path.exists(datatarget):
                jsondata=json.load(open(datatarget))
        
        return render_template('flipkallproduct.html',alldata=jsondata,res=key)





@app.route('/updateflipkart/<string:key>',methods=['GET','POST'])
def updateflipkart(key):
        key=key.split(",")
        curefilepath=os.path.dirname(os.path.abspath(__file__))
        target=os.path.join(curefilepath,'Products/flipkartlinkmanagment.json')
        if os.path.exists(target):
                editdata=[]
                jsondata=json.load(open(target))
                for i in jsondata:
                        if i["Keyword"]== key[0]:
                                editdata.append(key[0])
                                editdata.append(i['Link'])

        return render_template('editflipkartscraplinks.html',editdata=editdata,brandname=key[1])





# @app.route('/webscraping',methods=['GET','POST'])
# def webscraping():
#         if request.method=='POST':

#                 my_url = request.form['surl']
#                 headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}
#                 uClient = uReq(my_url)
#                 page_html = uClient.read()
#                 uClient.close()
#                 page_soup = soup(page_html,"html.parser")
#                 containers = page_soup.findAll("div",{"class": "a-section a-spacing-medium"})
#                 container = containers[0]
#                 title =container.find_all("a",class_="a-link-normal a-text-normal")
#                 prices =container.find_all("span",class_="a-offscreen")
#                 extracted_records = []
#                 for container in containers:
#                         try:
#                                 product_name = container.find_all("a",class_="a-link-normal a-text-normal")
#                                 product=product_name[0].text.strip()
#                                 url=product_name[0]['href']
#                                 image = container.a.img["src"]
#                                 price_container = container.find_all("span",class_="a-offscreen")
#                                 price=price_container[0].text
#                                 #rm_rupee = price.split("₹")
#                                 #add_rs_price =rm_rupee[1].split(",")
#                                 #prices=add_rs_price[0]+add_rs_price[1]
#                                 prices=price.replace('₹','',2)
#                         except Exception:
#                                 price='noprice'
                                
#                         if not url.startswith('http'):
#                                 url = "https://www.amazon.in"+url
#                         record = {
#                                 'product':product,
#                                 'price':prices,
#                                 'url':url,
#                                 'image':image,
#                                 }
#                         extracted_records.append(record)
#                 with open('AmzonData.json', 'w') as outfile:
#                         json.dump(extracted_records, outfile, indent=4)
#         return render_template('webscraping.html')   


@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
        return render_template('demo.html')


if __name__=='__main__':
     
     app.run(host='0.0.0.0', port=8000, debug=False)

     app.secret_key = 'myappsecretkey'
     app.run(debug=True)