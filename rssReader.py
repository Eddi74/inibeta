import re
import urllib
from bs4 import BeautifulSoup

#inserisco le url dei feed di riferimento

urldiv = 'http://www.forumfree.it/rss.php?a=817354&type=html&colorlink=989E94&n=30'

html_docdiv = urllib.urlopen(urldiv).read()
soup = BeautifulSoup(html_docdiv, 'html.parser')
tag_div = soup('div')
xtag_div = len(tag_div)


urlp = 'http://www.forumfree.it/rssreader.php?feed=http://www.forumfree.it/rss.php?a=817354&type=html&colorlink=989E94&n=30'

html_docp = urllib.urlopen(urlp).read()
soup = BeautifulSoup(html_docp, 'html.parser')
tag_p = soup('p')
xtag_p = len(tag_p)


#primo controllo che le url dei feed di riferimento siano sincronizzate

if xtag_div == xtag_p:
    pass
else:
    print 'Le origini dei commenti non sono sincronizzate.'
    print 'Fare ripartire il parser.'
    quit()
    
#parsing della prima url

xtag_div_count = 0
divs_list = []

for tag_div_entries in tag_div:
    
        xtag_div_count = xtag_div_count + 1 
        url_a = tag_div_entries.find_all('a')
       
        div_dict = {}
        href_list = []
        id_numbers_list = []
        strings_list = []
        
        for links in url_a:
            
            url_href= links.get('href')
            href_list.append(str(url_href))
            id_numbers = re.findall(r'\d+',str(url_href))
            id_numbers_list.append(int(id_numbers[0]))
            names = re.findall('>(.*?)<',str(links))
            for name in names:
                strings_list.append(str(name))
                
        topic_link_pulito = re.findall('(.*?)\d+',str(href_list[0]))   
        topic_link_prmes = topic_link_pulito[0]+str(id_numbers_list[0])
           
        date_hour_ms = re.findall('il: (.*?)br',str(tag_div_entries))
        date_ms =  re.findall('(.*?),',str(date_hour_ms[0]))
        hour_ms =  re.findall(', (.*?)<',str(date_hour_ms[0]))
        data_date_ms =  re.findall(r'\d+',str(date_ms[0]))
        
        date_american = str(data_date_ms[2])+'/'+str(data_date_ms[1])+'/'+str(data_date_ms[0])
        
        div_dict.update(topic_link=href_list[0], topic_link_primomess=topic_link_prmes, profilo_link=href_list[1], topic_id=id_numbers_list[0], profilo_id=id_numbers_list[1], profilo_name=strings_list[3], topic_title=strings_list[1], topic_date=date_american, topic_hour=hour_ms[0])
            
        divs_list.append(div_dict)

#parsing della seconda url

xtag_p_count = 0
ps_list = []

for tag_p_entries in tag_p:
        
        xtag_p_count = xtag_p_count + 1
        urlp_a = tag_p_entries.find_all('a')
        
        p_dict = {}
        href_list = []
        id_numbers_list = []
        strings_list = []
        
        for links in urlp_a:
            
            url_href= links.get('href')
            href_list.append(str(url_href))
            id_numbers = re.findall(r'\d+',str(url_href))
            id_numbers_list.append(int(id_numbers[0]))
        
        image_link_p = re.findall('src="(.*?)">',str(tag_p_entries))
        
        if len(image_link_p) == 0:
            image_link_p.append('')
            
        names_p = re.findall('op">(.*?)</a',str(tag_p_entries))
        name_title_p= re.findall('>(.*?)<',str(names_p[0]))                        
        
        p_dict.update(topic_id_p=id_numbers_list[0], image_link=image_link_p[0], section_id=id_numbers_list[2], section_link=href_list[2],   section_name=names_p[2], profilo_name_p=names_p[1], profilo_id_p=id_numbers_list[1], topic_title_p=name_title_p[0])
            
        ps_list.append(p_dict)

#secondo e definitivo controllo che le url dei feed di riferimento siano sincronizzate

count=0 

while count < xtag_div: 
        
        if ps_list[count].get('topic_id_p') == divs_list[count].get('topic_id') and ps_list[count].get('profilo_id_p') == divs_list[count].get('profilo_id'):
            pass

        else:  
            print 'Le origini dei commenti non sono sincronizzate. errore al messaggio: ', count
            print
            print ps_list[count]
            print
            print divs_list[count]
            print
            print 'Fare ripartire il parser.'
            quit()
        
        count = count + 1

#unione dei dati delle due url in divs_list

count=0 

for key  in   ps_list:
        image_url = ps_list[count].get('image_link')
        section = ps_list[count].get('section_name')
        sectionid = ps_list[count].get('section_id')
        sectionlink = ps_list[count].get('section_link')
        divs_list[count].update(image_link=image_url, sezione_name=section, sezione_id=sectionid, sezione_link=sectionlink)
        count=count+1
        
#export jason       

import json
j = json.dumps(divs_list, indent=4)

file = open("../rssJason.json", "w")

file.write(j)

file.close()

#export html

count=0 
divantetotal= []

for value in divs_list:
    
    username = str(divs_list[count].get('profilo_name'))
    profilolink = str(divs_list[count].get('profilo_link'))
    titolotopic = str(divs_list[count].get('topic_title'))
    linktopic = str(divs_list[count].get('topic_link'))
    linktopicprimome = str(divs_list[count].get('topic_link_primomess'))
    nomesezione = str(divs_list[count].get('sezione_name')) 
    sezionelink = str(divs_list[count].get('sezione_link'))
    datatopic = str(divs_list[count].get('topic_date')) 
    linkimmagine = str(divs_list[count].get('image_link'))
    count = count + 1
    

    divanteprima = '''
    <div class="anteprima"> 
        
        <a href="'''+sezionelink+'''">
           <h3 class="nomesezione"> '''+nomesezione+'''</h3>   
        </a>
        
        <div class="imagecontainer">
            <a href="'''+linktopicprimome+'''">
              <img  class="immaginetopic" src="'''+linkimmagine+'''"></img>
            </a>
        </div>
        
        <div class="dummy_informazioni"></div>
        
        <div class="informazioni">
           <a href="'''+linktopic+'''">
              <h3 class="titolotopic">  '''+titolotopic+'''</h3>
           </a>
           <p class="usercomm">ultimo commento di: </p>
           <a href="'''+profilolink+'''">
               <h3 class="username"> '''+username+'''</h3>   
           </a>
           <p class="datecommnt">il: '''+datatopic+'''</p>
        </div>
        
    </div> '''
    
    divantetotal.append(divanteprima)
    
spazio=""
anteprima_nuovi_commenti = spazio.join(divantetotal)

mess= '''
<!DOCTYPE html>
<html>
    <head>
      <link href="css/ucstile.css" rel="stylesheet" type="text/css">
      <meta charset="UTF-8"> 
      <title>Anteprima Ultimi Commenti</title>
    </head>
    
<body>

<div class="bodycontainer">

  <div class="anteprimacont">
'''+anteprima_nuovi_commenti+'''
  </div>
  
</div>

</body>
</html>'''

file = open("../anteprima.html","w")

file.write(mess)

file.close()

    
    
    
    

   
    
        


    

