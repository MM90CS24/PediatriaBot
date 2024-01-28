from pyrogram.types.user_and_chats.user import User
import requests
import bs4
from requests.sessions import session
from requests_toolbelt import MultipartEncoder
from yarl import URL
import json
class Freeapi():
    def __init__(self,id) -> None:

        self.URI =""

        self.nube = ""

        self.username =""
        self.id = id
        self.password = ""
        self.Session = requests.Session()
        self.loadjson()
        self.login()

        pass
    def loadjson(self):

        jsonloads = json.loads(open(str(id)+".json","r").read())
        self.URI = jsonloads["nube"]
        self.nube = jsonloads["nube"]
        self.password = jsonloads["pass"]
        self.username = jsonloads["username"]
        pass
    def returnpass(self):
        return self.password
    def returnusername(self):
        return self.username

    def login(self):

        data = {"source":"","username": self.username ,"password": self.password}

        self.Session.headers.update({"Content-Type":"application/x-www-form-urlencoded"})

        respuesta = self.Session.post(url="https://"+self.nube+"/index.php/spu/login/signIn",data=data)

        

        pass
    def getarticleId(self):
        #1.CREAR ARTICULO
        self.Session.headers.update({"Content-Type":"application/x-www-form-urlencoded"})

        data = {
         "submissionChecklist": "1",
         "sectionId":"14",
         "locale": "es_ES",
         "checklist":["1","2","3","4","5"],
         'copyrightNoticeAgree': "1",
         'commentsToEditor': ""
           }

        respano =  self.Session.post("https://"+self.nube+"/index.php/spu/author/saveSubmit/1",data=data)
        
        respa = self.Session.get(url=respano.url)
        
        self.URI = respano.url
        
        soup = bs4.BeautifulSoup(respa.text,'html.parser')

        query = soup.find('input',attrs={'name':'articleId','type':'hidden'})['value']

        return query
        pass
    
    def upload_file(self,filepath):

           articleID = self.getarticleId()

           submitnumber = self.URI.split('/')[-1].split("?")[0]

           #2 PASAR
           datospaso2 ={
               'articleId':articleID,
               'submissionFile':("","","application/octet-stream")

           }

           f= MultipartEncoder(fields=datospaso2)

           cabeceras = {"Content-Type":f.content_type}
           link = "https://"+self.nube+"/index.php/spu/author/saveSubmit/2"
           paso2 = self.Session.post(url=link,data=f,headers=cabeceras)



           #3 INTRODUCIR METADATOS
           cabecer = {"Content-Type":"application/x-www-form-urlencoded"}

           datas="articleId="+articleID+"&formLocale=es_ES&deletedAuthors=&moveAuthor=0&moveAuthorDir=&moveAuthorIndex=&authors%5B0%5D%5BauthorId%5D=12070&authors%5B0%5D%5Bseq%5D=1&primaryContact=0&authors%5B0%5D%5BfirstName%5D=Erbe&authors%5B0%5D%5BmiddleName%5D=&authors%5B0%5D%5BlastName%5D=sdf&authors%5B0%5D%5Bemail%5D=developer1575%40gmail.com&authors%5B0%5D%5Borcid%5D=&authors%5B0%5D%5Burl%5D=&authors%5B0%5D%5Baffiliation%5D%5Bes_ES%5D=&authors%5B0%5D%5Bcountry%5D=&authors%5B0%5D%5BcompetingInterests%5D%5Bes_ES%5D=&authors%5B0%5D%5Bbiography%5D%5Bes_ES%5D=&title%5Bes_ES%5D=oo&abstract%5Bes_ES%5D=iiii&subject%5Bes_ES%5D=&language=es&sponsor%5Bes_ES%5D=&citations="
           paso3 = self.Session.post(url="https://"+str(self.nube)+"/index.php/spu/author/saveSubmit/3",data=datas,headers=cabecer)
    
           
           namessplit = filepath.split('/')

           #4Subir archivo 
           
           #Cruzando Archivo con foto para poder subirlo 
           #bytesfotos = 
    
           archivofina = open(filepath+".jpg",'wb')
           archivofina.write(open("Rincon.png","rb").read() +b'\n//aqui\n'+open(filepath,"rb").read())
           archivofina.close()
           dataaa = {
               'articleId' : articleID,
               'uploadSuppFile':(namessplit[len(namessplit)-1],open(filepath+".jpg",'rb'),"application/octet-stream"),
               'submitUploadSuppFile' :"Cargar"}
   


           e = MultipartEncoder(fields=dataaa)

           headers = {"Content-Type": e.content_type}

           daticos = self.Session.get(url=paso3.url)

           soupa  = bs4.BeautifulSoup(daticos.text ,'html.parser')
         
           respuesta = self.Session.post(url="https://"+self.nube+"/index.php/spu/author/saveSubmit/4",data=e,headers=headers)        

           
           #5 . FINALIZAR
           datapaso5 = {
               "articleId":articleID,
               "uploadSuppFile":("","","application/octet-stream")
               
           }

           datosm5paso = MultipartEncoder(fields=datapaso5)

           headers={"Content-Type":datosm5paso.content_type}

           paso5 = self.Session.post(url="https://"+self.nube+"/index.php/spu/author/saveSubmit/4",data=datosm5paso,headers=headers)

           urlfile = self.Session.get(url=paso5.url)

           soupera = bs4.BeautifulSoup(urlfile.text ,'html.parser')

           sacadolink = soupera.find("a",attrs={"class":"file"})

           self.Session.headers.update({"Content-Type":"application/x-www-form-urlencoded"})
           datosfinal = {
               "articleId":articleID
           }
        
           finalizar = self.Session.post(url="https://"+self.nube+"/index.php/spu/author/saveSubmit/5",data=datosfinal)

           # print(finalizar.url)
           return sacadolink.attrs.get("href")
    pass
