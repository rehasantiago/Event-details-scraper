import requests,csv,datetime,os,ast,sys


class Scraper:

	def __init__(self,agent):
		self.agent= agent	# file name 
    


	def getRequest(self,**kwargs):
		ten_useragent = "Mozilla/5.0 (compatible; name_of_your_bot/1.0)"#name your bot
		if len(kwargs) > 1 and "flag" in kwargs.keys() and kwargs["flag"]:
			from selenium import webdriver
			profile = webdriver.FirefoxProfile()
			profile.set_preference("general.useragent.override",ten_useragent)
			try:
				if "cap" not in kwargs.keys():
					driver = webdriver.Firefox(profile)
				elif "cap" in kwargs.keys() and "exec_path" in kwargs.keys():
					driver = webdriver.Firefox(capabilities=kwargs["cap"],executable_path=kwargs["exec_path"], firefox_profile=profile)
				elif "cap" in kwargs.keys() and "exec_path" not in kwargs.keys():
					driver = webdriver.Firefox(capabilities=kwargs["cap"], firefox_profile=profile)
				else:
					return {"status":{"code":0,"message":"Error: parameter missing"},"data":[]}	
				driver.get(kwargs["url"])
				return {"status":{"code":1,"message":[]},"data":driver}
			except Exception as e :
				return {"status":{"code":0,"message":"Error: "+str(e)},"data":[]}
		else:
			if "url" in kwargs.keys():
				headers = requests.utils.default_headers()
				headers.update({'User-Agent': ten_useragent})
				try:
					response = requests.get(kwargs["url"], headers=headers)
					return {"status":{"code":1,"message":[]},"data":response}
				except requests.exceptions.RequestException as e:
					return {"status":{"code":0,"message":"Error: "+str(e)},"data":[]}
			else:
				return {"status":{"code":0,"message":"Error: 'url' key is missing"},"data":[]}
	


	def saveData(self,data):
		if len(data)>0 :
			column = Columns(records={"maindate_flag":0,"positon":0},event_name={"maindate_flag":1,"positon":1},event_url={"maindate_flag":1,"positon":2},event_date={"maindate_flag":1,"positon":3},event_start={"maindate_flag":0,"positon":4},event_end={"maindate_flag":0,"positon":5},event_location={"maindate_flag":1,"positon":6},event_venue={"maindate_flag":0,"positon":7},event_city={"maindate_flag":0,"positon":8},event_country={"maindate_flag":0,"positon":9},event_contact_email={"maindate_flag":1,"positon":10},event_punchline={"maindate_flag":1,"positon":11},event_edition={"maindate_flag":0,"positon":12},fk_category_1={"maindate_flag":-1,"positon":13},fk_category_2={"maindate_flag":-1,"positon":14},fk_venue_id={"maindate_flag":-1,"positon":15},fk_city_id={"maindate_flag":-1,"positon":16},fk_country_id={"maindate_flag":-1,"positon":17},fk_event_id={"maindate_flag":-1,"positon":18},fk_event_type={"maindate_flag":-1,"positon":19})

			data = self._processData(data,column)
			################ Process Data ################
			if data["status"]["code"] :
				# filename = "/var/www/bot.10times.com/web/data-files/rawdata_"+os.path.splitext(os.path.basename(self.agent))[0]+"_"+datetime.datetime.now().strftime("%Y-%m-%d")+".csv"
				filename = "rawdata_"+os.path.splitext(self.agent)[0]+"_"+datetime.datetime.now().strftime("%Y-%m-%d")+".csv"
				path= sys.path[0]+"/"
				try:
					with open(str(path)+filename, 'a') as csvfile:
						writer = csv.writer(csvfile)
						writer.writerow(column.getHeaderByOrder())
						for row in data["data"]:
							writer.writerow(row)
					return {"status":{"code":1,"message":[]},"data":{"filename": path+filename}}
				except IOError as a:
					return {"status":{"code":0,"message":"Error: File does not appear to exist."},"data":[]}
			else:
				return data


	##################  			Creating CSV File 			####################

	def _processData(self,data,columnObj):
		maindate_columns = columnObj.getColumnsList(1)
		if(len(data[0].keys()) >= len(maindate_columns)):
			if (len(list(set(maindate_columns) - set(data[0].keys()))) ==0):
				final_data=[]
				count =0 
				for row in data:
					temp = []
					count =count+1
					for keys in columnObj.getHeaderByOrder():
						if keys in data[0].keys():
							temp.append(row[keys])
						elif keys=="records":
							temp.append(count)
						else:
							temp.append("")
					final_data.append(temp)
				return {"status":{"code":1,"message":[]},"data":final_data}
			else:
				return {"status":{"code":0,"message":"Error: Column Keys mismatch. Missing: "+str(list(set(maindate_columns) - set(data[0].keys())))},"data":[]}
		else:
			return {"status":{"code":0,"message":"Error: Columns count mismatch."},"data":[]}
		



class Columns:

	def __init__(self,**kwargs):
		self.columns = kwargs

	#gives header in order list my maindate flag 1 = manadatory ,0 = optional and -1 neglected
	def getColumnsDict(self,index):
		return ({k: v for k, v in self.columns.items() if v['maindate_flag'] == index})

	#gives header in order list my maindate flag 1 = manadatory ,0 = optional and -1 neglected
	def getColumnsList(self,index):
		columns_list =[]
		alist =(sorted(self.columns.items(),key=lambda x:int(x[1]['positon']),reverse=False))
		for k,v in alist:
			if v["maindate_flag"]==index:
				columns_list.append(k)
		return columns_list

	#gives header in order list	
	def getHeaderByOrder(self):
		columns_list =[]
		alist =(sorted(self.columns.items(),key=lambda x:int(x[1]['positon']),reverse=False))
		for k,v in alist:
			columns_list.append(k)
		return columns_list