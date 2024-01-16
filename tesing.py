import requests
requestadpr = requests.Session()

datas ="articleId="+str(123)+"&formLocale=es_ES&deletedAuthors=&moveAuthor=0&moveAuthorDir=&moveAuthorIndex=&authors%5B0%5D%5BauthorId%5D=12048&authors%5B0%5D%5Bseq%5D=1&primaryContact=0&authors%5B0%5D%5BfirstName%5D=Erbe&authors%5B0%5D%5BmiddleName%5D=&authors%5B0%5D%5BlastName%5D=sdf&authors%5B0%5D%5Bemail%5D=developer1575%40gmail.com&authors%5B0%5D%5Borcid%5D=&authors%5B0%5D%5Burl%5D=&authors%5B0%5D%5Baffiliation%5D%5Bes_ES%5D=&authors%5B0%5D%5Bcountry%5D=&authors%5B0%5D%5BcompetingInterests%5D%5Bes_ES%5D=&authors%5B0%5D%5Bbiography%5D%5Bes_ES%5D=&title%5Bes_ES%5D=sss&abstract%5Bes_ES%5D=&subject%5Bes_ES%5D=&language=es&sponsor%5Bes_ES%5D=&citations="

requestadpr.headers.update({"Content-Type":"application/x-www-form-urlencoded"})
paso3 = requestadpr.post(url="http://revpediatria.sld.cu/index.php/ped/author/saveSubmit/3",data=datas)
           