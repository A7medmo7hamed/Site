from flask import Flask,render_template,redirect,render_template_string,request,flash,url_for,abort,session,get_flashed_messages,make_response,Response
#from flask_recaptcha import ReCaptcha
import requests
import hashlib
import uuid
import base64

def num(Number):
			if (len(Number)==11):
				return (Number[1:11])
			else:
				return Number
def JSESSIONID(email,password):
			Ahmed=(f"{email}:{password}").strip()
			Code=base64.b64encode(Ahmed.encode('UTF-8')).decode('ascii')
			uid=uuid.uuid4()
			login=(requests.post("https://mab.etisalat.com.eg:11003/Saytar/rest/authentication/loginWithPlan",
headers={
"Content-Type": "text/xml",
"applicationName": "MAB",
"Accept": "text/xml",
"Host": "mab.etisalat.com.eg:11003",
"Connection": "Keep-Alive",
"Accept-Encoding": "gzip",
"User-Agent": "okhttp/3.12.8",
"ADRUM_1": "isMobile:true",
"ADRUM": "isAjax:true",
"Authorization": f"Basic {Code}",
},
data=f"<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><loginRequest><deviceId>{uid}</deviceId><firstLoginAttempt>true</firstLoginAttempt><modelType>SM-A025F</modelType><osVersion>11</osVersion><platform>Android</platform><udid>{uid}</udid></loginRequest>"))

			try:
				if login.status_code==200:
					Number=login.text.split("</postpaid><dial>")[1].split("</")[0]
					js=login.cookies["JSESSIONID"]
					JS=f"JSESSIONID={js}; path=/; HttpOnly"
					number=num(Number)
					return {"status":True,"dial":number,"JSESSIONID":JS,"udid":f"{uid}"}
				else:
					return {"status":False}
			except IndexError:
				return {"status":False}

server=Flask(__name__)
server.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@server.route("/")
def redir():
		return redirect('/home')
		
@server.route('/home')
def home():
	return (open("home.html","r").read()),200
	
@server.route('/Vodafone')
def vf():
	return (open("Vodafone.html","r").read()),200

@server.route('/Etisalat')
def et():
	return (open("Etisalat.html","r").read()),200

@server.route('/Vodafone/58GB',methods=["POST","GET"])
def _58GB():
	if request.method == "POST":
		print(request.base_url)
		numb=request.form['number']
		pas=request.form['password']
		try:
	
			token=requests.post("https://mobile.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token",
			headers={"Accept":"application/json, text/plain, */*","Connection":"keep-alive","x-dynatrace":"MT_3_17_998679495_45-0_a556db1b-4506-43f3-854a-1d2527767923_0_18957_273","x-agent-operatingsystem":"1630483957","clientId":"AnaVodafoneAndroid","x-agent-device":"RMX1911","x-agent-version":"2021.12.2","x-agent-build":"493","Content-Type":"application/x-www-form-urlencoded","Content-Length":"143","Host":"mobile.vodafone.com.eg","Accept-Encoding":"gzip","User-Agent":"okhttp/4.9.1"},
			data={
			"username":numb,#"01029160511",
			"password":pas,#"@Almadyy2000",
			"grant_type":"password",
			"client_secret":"a2ec6fff-0b7f-4aa4-a733-96ceae5c84c3",
			"client_id":"my-vodafone-app",
			}).json()['access_token']
			#print(token)
			try:
				id=requests.get(f"https://web.vodafone.com.eg/services/dxl/pim/product?relatedParty.id\u003d{numb}\u0026place.@referredType\u003dLocal\u0026@type\u003dMIProfile",
				 headers = {
			    "Host": "web.vodafone.com.eg",
			    "Connection": "keep-alive",
			    "msisdn": (numb),
			    "Accept-Language": "AR",
			    "Authorization": "Bearer "+token,
			    "Content-Type": "application/json",
			    "Accept": "application/json",
			    "x-dtreferer": "https://web.vodafone.com.eg/spa/myHome",
			    "clientId": "WebsiteConsumer",
			    #"x-dtpc": "22$359801315_733h11vHBNGFNCJMFSGONHETDKMKISFJRUMNPCJ-0e0",
			    #"User-Agent": "Mozilla/5.0 (Linux; Android 11; SM-A025F Build/RP1A.200720.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36",
			    "X-Requested-With": "mark.via.gp",
			    "Sec-Fetch-Site": "same-origin",
			    "Sec-Fetch-Mode": "cors",
			    "Sec-Fetch-Dest": "empty",
			    "Referer": "https://web.vodafone.com.eg/spa/myManagement/internet",
			    "Accept-Encoding": "gzip, deflate",})
				print(id.text)
				print(id.json()[2]['productOffering']['encProductId'])
				_id=(id.json()[2]['productOffering']['encProductId'])
				__id=(id.json()[1]['productOffering']['encProductId'])
				_order=(requests.post("https://web.vodafone.com.eg/services/dxl/pom/productOrder",
				headers = {
			    "Host": "web.vodafone.com.eg",
			    "Connection": "keep-alive",
			    "msisdn": (numb),
			    "Accept-Language": "AR",
			    "Authorization": "Bearer "+token,
			    "Content-Type": "application/json",
			    "Accept": "application/json",
			    "x-dtreferer": "https://web.vodafone.com.eg/spa/myHome",
			    "clientId": "WebsiteConsumer",
			    #"x-dtpc": "22$359801315_733h11vHBNGFNCJMFSGONHETDKMKISFJRUMNPCJ-0e0",
			    #"User-Agent": "Mozilla/5.0 (Linux; Android 11; SM-A025F Build/RP1A.200720.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36",
			    "X-Requested-With": "mark.via.gp",
			    "Sec-Fetch-Site": "same-origin",
			    "Sec-Fetch-Mode": "cors",
			    "Sec-Fetch-Dest": "empty",
			    "Referer": "https://web.vodafone.com.eg/spa/myManagement/internet",
			    "Accept-Encoding": "gzip, deflate",},
			    json={"channel":{"name":"MobileApp"},"orderItem":[{"action":"add","product":{"characteristic":[{"name":"ExecutionType","value":"Sync"},{"name":"LangId","value":"en"},{"name":"MigrationType","value":"Repurchase"}],"relatedParty":[{"id":numb,"name":"MSISDN","role":"Subscriber"}],"id":"Summer_Promo_4","@type":"MI","encProductId":__id}}],"@type":"MIProfile"}))
				print(_order.status_code)
				flash("تم اضافة 58 جيجا لخطك بنجاح")
				return render_template_string(open("main.html").read(),title="58GB | "+get_flashed_messages()[0],sub="darkred",alertcolor="green")
				print(_order.text)
				order=(requests.post("https://web.vodafone.com.eg/services/dxl/pom/productOrder",
				headers = {
			    "Host": "web.vodafone.com.eg",
			    "Connection": "keep-alive",
			    "msisdn": (numb),
			    "Accept-Language": "AR",
			    "Authorization": "Bearer "+token,
			    "Content-Type": "application/json",
			    "Accept": "application/json",
			    "x-dtreferer": "https://web.vodafone.com.eg/spa/myHome",
			    "clientId": "WebsiteConsumer",
			    #"x-dtpc": "22$359801315_733h11vHBNGFNCJMFSGONHETDKMKISFJRUMNPCJ-0e0",
			    #"User-Agent": "Mozilla/5.0 (Linux; Android 11; SM-A025F Build/RP1A.200720.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36",
			    "X-Requested-With": "mark.via.gp",
			    "Sec-Fetch-Site": "same-origin",
			    "Sec-Fetch-Mode": "cors",
			    "Sec-Fetch-Dest": "empty",
			    "Referer": "https://web.vodafone.com.eg/spa/myManagement/internet",
			    "Accept-Encoding": "gzip, deflate",},
			    json={"channel":{"name":"MobileApp"},"orderItem":[{"action":"add","product":{"characteristic":[{"name":"ExecutionType","value":"Sync"},{"name":"LangId","value":"en"},{"name":"MigrationType","value":"Repurchase"}],"relatedParty":[{"id":numb,"name":"MSISDN","role":"Subscriber"}],"id":"Summer_Promo_4","@type":"MI","encProductId":_id}}],"@type":"MIProfile"}))
				print(order.status_code)
				print(order.text)
			except :
				flash("غير متاحه لنظام خطك")
				return render_template_string(open("main.html").read(),title="58GB | "+get_flashed_messages()[0],sub="darkred",alertcolor="darkred")
		except KeyError :
			flash("خطأ في الرقم او الباسورد")
			return render_template_string(open("main.html").read(),title="58GB | "+get_flashed_messages()[0],sub="darkred",alertcolor="darkred")
			#pass
		
	
	return render_template_string(open('main.html').read(),title="Vodafone | 58GB ",sub="darkred")


@server.route("/Etisalat/GIFT",methods=["POST","GET"])
def Gift():
	if request.method == 'POST':
		#print(request.form)
		username=request.form['email']
		password=request.form['password']
		try:
			import uuid
			import base64
			from os import system
		except:
			system("pip install requests")
			system("pip install base64")
			system("pip install uuid")

#		def num(Number):
#			if (len(Number)==11):
#				return (Number[1:11])
#			else:
#				return Number
#		def JSESSIONID(email,password):
#			Ahmed=(f"{email}:{password}").strip()
#			Code=base64.b64encode(Ahmed.encode('UTF-8')).decode('ascii')
#			uid=uuid.uuid4()
#			login=(requests.post("https://mab.etisalat.com.eg:11003/Saytar/rest/authentication/loginWithPlan",
#headers={
#"Content-Type": "text/xml",
#"applicationName": "MAB",
#"Accept": "text/xml",
#"Host": "mab.etisalat.com.eg:11003",
#"Connection": "Keep-Alive",
#"Accept-Encoding": "gzip",
#"User-Agent": "okhttp/3.12.8",
#"ADRUM_1": "isMobile:true",
#"ADRUM": "isAjax:true",
#"Authorization": f"Basic {Code}",
#},
#data=f"<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><loginRequest><deviceId>{uid}</deviceId><firstLoginAttempt>true</firstLoginAttempt><modelType>SM-A025F</modelType><osVersion>11</osVersion><platform>Android</platform><udid>{uid}</udid></loginRequest>"))


#			if login.status_code==200:
#				Number=login.text.split("</postpaid><dial>")[1].split("</")[0]
#				js=login.cookies["JSESSIONID"]
#				JS=f"JSESSIONID={js}; path=/; HttpOnly"
#				number=num(Number)
#				return {"status":True,"dial":number,"JSESSIONID":JS,"udid":f"{uid}"}
#			else:
#				return {"status":False}

		Login=JSESSIONID(username,password)
		if Login["status"]==True:
			number=Login["dial"]
			JS=Login["JSESSIONID"]
			day=requests.get("https://mab.etisalat.com.eg:11003/Saytar/rest/dailyTipsWS/dailyTipGiftV3?req=<dailyTipRequest><subscriberNumber>"+number+"</subscriberNumber><language>1</language></dailyTipRequest>",
headers={
"Content-Type": "text/xml",
"applicationName": "MAB",
"Accept": "text/xml",
"Cookie": JS,
"Host": "mab.etisalat.com.eg:11003",
"Connection": "Keep-Alive",
"Accept-Encoding": "gzip",
"User-Agent": "okhttp/3.12.8",
"ADRUM_1": "isMobile:true",
"ADRUM": "isAjax:true"
}).text

#print(day)
			dayNum=(day.split("TRUE</todayGift></dailyTip></dailyTips><dayNum>")[1].split("</")[0])

			MB=(day.split(f"GIFT_ID</name><value>{dayNum}</value></param><param><name>VALIDITY</name><value>1</value></param><param><name>AMOUNT</name><value>")[1].split("</")[0])



			res=(requests.post("https://mab.etisalat.com.eg:11003/Saytar/rest/dailyTipsWS/submitOrder",
headers={
"Content-Type": "text/xml",
"applicationName": "MAB",
"Accept": "text/xml",
"Cookie": JS,
"Host": "mab.etisalat.com.eg:11003",
"Connection": "Keep-Alive",
"Accept-Encoding": "gzip",
"User-Agent": "okhttp/3.12.8",
"ADRUM_1": "isMobile:true",
"ADRUM": "isAjax:true"
},
data="<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><dailyTipsSubmitRequest><operationId>REDEEM</operationId><params><param><name>GIFT_ID</name><value>"+dayNum+"</value></param><param><name>CATEGORY</name><value>DAILY_TIPS_NEW</value></param></params><productId>DAILY_TIPS_GIFT</productId><subscriberNumber>"+number+"</subscriberNumber></dailyTipsSubmitRequest>"
))

			date=res.headers["Date"][4:16]

			m=({"result":{"Day":dayNum,"Status":"Complete","MB":f"{MB}","Dial":number,"ExpireDate":date}})
			#toast(m)
			flash(f"• تم اضافة  {m['result']['MB']}  ميجا - ليوم {m['result']['Day']} - تاريخ الانتهاء  {m['result']['ExpireDate']} •")
			lon="green"
			import uuid
			uid=uuid.uuid4()
			print(requests.post("https://mab.etisalat.com.eg:11003/Saytar/rest/quickAccess/logoutQuickAccess",
headers={
"Content-Type": "text/xml; charset=UTF-8",
"Content-Length": "181",
"applicationName": "MAB",
"Accept": "text/xml",
"Cookie":JS,
"Host": "mab.etisalat.com.eg:11003",
"Connection": "Keep-Alive",
"Accept-Encoding": "gzip",
"User-Agent": "okhttp/3.12.8",
"ADRUM_1": "isMobile:true",
"ADRUM": "isAjax:true"},
data=f"<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><logoutQuickAccessRequest><dial>{number}</dial><udid>{uid}</udid></logoutQuickAccessRequest>").text)
		else:
			if Login["status"]==False:
				flash("Error Username or Password")
				lon="red"
		return render_template_string(open("et.html").read(),title="Gift Etisalat | "+get_flashed_messages()[0],sub="darkgreen",alertcolor=lon)
	return render_template_string(open("et.html").read(),title="Gift Etisalat",sub="darkgreen")
@server.route('/Orange')
def _or():
	return (open("Orange.html","r").read()),200



@server.route("/Etisalat/4G",methods=["GET","POST"])
def _4G():
	if request.method == "POST":
		email = request.form['email']
		password = request.form["password"]
		Login = JSESSIONID(email,password)
		print(Login)
		if Login["status"] ==True:
			num=Login['dial']
			js=Login["JSESSIONID"]
			print(requests.post("https://mab.etisalat.com.eg:11003/Saytar/rest/rtim/rtimSubmitOrder",
			headers={
			"Content-Type": "text/xml; charset=UTF-8",
			"Content-Length": "331",
			"applicationName": "MAB",
			"Accept": "text/xml",
			"Cookie":js,
			"Host": "mab.etisalat.com.eg:11003",
			"Connection": "Keep-Alive",
			"Accept-Encoding": "gzip",
			"User-Agent": "okhttp/3.12.8",
			"ADRUM_1": "isMobile:true",
			"ADRUM": "isAjax:true"
			},
			data=f"<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><rtimSubmitOrder><extraProductId>20885</extraProductId><offerId>20885</offerId><operationId>ACTIVATE</operationId><productId>4G_USE_AND_GET_MI_DOUBLE=Offer_ID:20885;isRTIM:Y</productId><rtimFlag>true</rtimFlag><subscriberNumber>{num}</subscriberNumber></rtimSubmitOrder>").text)
			flash("تم تفعيل العرض بنجاح انتظر رساله من الشركة .")
			return render_template_string(open("et.html").read(),sub="green",title=f"Etisalat 4G | "+get_flashed_messages()[0],alertcolor="green")
		else:
			flash("حدث خطاء !")
			return render_template_string(open("et.html").read(),sub="green",title=f"Etisalat 4G | "+get_flashed_messages()[0],alertcolor="red")
	else:pass
	return render_template_string(open("et.html").read(),sub="green",title="Etisalat 4G")

@server.route("/Etisalat/1500UNITS",methods=["POST","GET"])
def _1500():
	if request.method == "POST":
		email = request.form['email']
		password = request.form["password"]
		Login = JSESSIONID(email,password)
		print(Login)
		if Login["status"] ==True:
			num=Login['dial']
			js=Login["JSESSIONID"]
			req=requests.post("https://mab.etisalat.com.eg:11003/Saytar/rest/downloadAndGet/submitOrder",
			headers={
			"Content-Type": "text/xml; charset=UTF-8",
			"Content-Length": "615",
			"applicationName": "MAB",
			"Accept": "text/xml",
			"Cookie":js,
			"Host": "mab.etisalat.com.eg:11003",
			"Connection": "Keep-Alive",
			"Accept-Encoding": "gzip",
			"User-Agent": "okhttp/3.12.8",
			"ADRUM_1": "isMobile:true",
			"ADRUM": "isAjax:true"
			},
			data=f"<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><downloadAndGetSubmitOrderRequest><Parameters><Parameter><name>GIFT_ID</name><value>DIGITAL_STREAMING_GIFT</value></Parameter><Parameter><name>VALIDITY</name><value>2</value></Parameter><Parameter><name>AMOUNT</name><value>1500</value></Parameter><Parameter><name>VERSION_NUMBER</name><value>v25.9.0</value></Parameter><Parameter><name>SERVICE_CLASS_GROUP</name><value>AHLAN_15PT</value></Parameter></Parameters><dial>{num}</dial><operationId>REDEEM</operationId><productId>DOWNLOAD_AND_PICK_STREAMING</productId></downloadAndGetSubmitOrderRequest>").text
			if "<submitResponse><fault><errorCode>SE_SDP_1</errorCode><message>WSMethod[downloadAndGetGiftSubmitOrder] STATUS[failed]</message><retry>true</retry></fault><status>false</status></submitResponse" in req:
				flash("هذا العرض غير متاح لنظام خطك ")
				return render_template_string(open("et.html").read(),sub="green",title=f"Etisalat 1500 Units | "+get_flashed_messages()[0],alertcolor="red")
			else:
				flash("تم اضافة 1500 وحدة بنجاح ")
				return render_template_string(open("et.html").read(),sub="green",title=f"Etisalat 1500 Units | "+get_flashed_messages()[0],alertcolor="green")
		else:
			flash("حدث خطاء ")
			return render_template_string(open("et.html").read(),sub="green",title=f"Etisalat 4G | "+get_flashed_messages()[0],alertcolor="red")
	else:pass
	return render_template_string(open("et.html").read(),sub="green",title="Etisalat 1500 Units ")

@server.route("/Orange/500MB",methods=["GET","POST"])
def Orange_Promo():
    import hashlib
    def htv():
    	re=requests.post(url ="https://services.orange.eg/GetToken.svc/GenerateToken",headers={'Content-Type':'application/json','charset':'UTF-8','Content-Length':'78','Host':'services.orange.eg','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Encoding':'Identity, identity','User-Agent':'okhttp/3.12.0'},data= '{"channel":{"ChannelName":"MobinilAndMe","Password":"ig3yh*mk5l42@oj7QAR8yF"}}')
    	ctv=re.json()["GenerateTokenResult"]["Token"]
    	hash_string = ctv+',{.c][o^uecnlkijh*.iomv:QzCFRcd;drof/zx}w;ls.e85T^#ASwa?=(lk'
    	htv=hashlib.sha256(hash_string.encode()).hexdigest()
    	data={'htv':htv.upper(),'ctv':ctv}
    	return (data)
    if request.method == 'POST':
        
        number=request.form['number']
        password=request.form['password']
        
        rq=requests.post(url ="https://services.orange.eg/GetToken.svc/GenerateToken",headers={'Content-Type':'application/json','charset':'UTF-8','Content-Length':'78','Host':'services.orange.eg','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Encoding':'Identity, identity','User-Agent':'okhttp/3.12.0'},data= '{"channel":{"ChannelName":"MobinilAndMe","Password":"ig3yh*mk5l42@oj7QAR8yF"}}')
        ctv=rq.json()["GenerateTokenResult"]["Token"]
        
        hash_string = ctv+',{.c][o^uecnlkijh*.iomv:QzCFRcd;drof/zx}w;ls.e85T^#ASwa?=(lk'
        
        htv=hashlib.sha256(hash_string.encode()).hexdigest().upper()

    
        urrrlll="https://services.orange.eg/SignIn.svc/SignInUser"
        hd={
            "_ctv":ctv,
            "_htv":htv,
            "Content-Type":"application/json; charset=UTF-8",
            "Content-Length":"168",
            "Host":"services.orange.eg",
            "Connection":"Keep-Alive",
            "Accept-Encoding":"gzip",
            "User-Agent":"okhttp/3.14.9"
        }
        data2='{"appVersion": "6.0.1","channel":{"ChannelName":"MobinilAndMe", "Password": "ig3yh*mk5l42@oj7QAR8yF"},"dialNumber":"' + str(number) + '","isAndroid": "true","password":"' + str(password) + '"}'
        try:
        	rew=requests.post(urrrlll, headers=hd, data=data2)
        	userid=rew.json()["SignInUserResult"]["UserData"]["UserID"]
        	url = "https://services.orange.eg/APIs/Promotions/api/CAF/Redeem"
        	headers = {
            "_ctv":ctv,
            "_htv":htv,
            'UserId':userid,
            "Content-Type": "application/json; charset=UTF-8",
            "Host": "services.orange.eg",
            "Connection": "Keep-Alive",
            "User-Agent": "okhttp/3.12.9"
        }

        	json ={'Language':'ar','OSVersion':'Android7.0','PromoCode':'رمضان كريم','dial':str(number),'password':str(password),'Channelname':'MobinilAndMe','ChannelPassword':'ig3yh*mk5l42@oj7QAR8yF'}
        	lol=requests.post(url, headers=headers, json=json).json()
        	if lol["ErrorDescription"]=="Success":
        		result="تم اضافة 524 ميجا بنجاح"
        		_lon="green"
        		flash(result)
#        		return render_template_string(open('main.html').read(),title="500MB Orange | "+result,alertcolor=_lon)
        	
        	else:
        		result="انت استخدمت البرومو كود النهاردة شكراً :)"
        		_lon="orange"
        		flash(result)
#        		return render_template_string(open('main.html').read(),title="500MB Orange | "+result,alertcolor=_lon,sub="darkorange")
        except TypeError:
        	result="الرقم غلط او الباسورد !"
        	_lon="red"#"tomato"
        	flash(result)
        return render_template_string(open('main.html').read(),title="500MB Orange | "+result,alertcolor=_lon,sub="darkorange")

        #flash(result)
    return render_template_string(open('main.html').read(),title="500MB Orange",sub="darkorange")

	

if __name__ == '__main__':
    server.run(debug=True, host="0.0.0.0", port=8080)