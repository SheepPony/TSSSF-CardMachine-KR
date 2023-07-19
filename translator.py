import csv

def unwhite(s):
	return s.replace(" ","").replace("\n","").replace("\t","").replace(".","").replace("-","").replace('"','').lower()
	
def unescape(s):
	return s.replace("\\n","\n")
def escape(s):
	return repr(s)[1:-1]


with open("TranslationData/mapping.csv","r",encoding="utf-8") as f:
	csv_rows=list(csv.reader(f))
csv_rows=csv_rows[2:]

keyword_mappings=dict()
for row in csv_rows:
	k=row[1]
	v=row[3]
	keyword_mappings[k]=v
	
def apply_mappings(s):
	for k in keyword_mappings:
		v=keyword_mappings[k]
		s=s.replace(k,v)
	return s

def parse_csv(filepath,is_goal=False):
	res=dict()
	with open(filepath,"r",encoding="utf-8") as f:
		csv_rows=list(csv.reader(f))

	csv_rows=csv_rows[2:]
	i=0
	while i<len(csv_rows):
		if csv_rows[i][1].strip(): # Number column NOT empty!
			key=unwhite(csv_rows[i][2])
			dat=dict()
			if is_goal:
				tagkeys=("name","body","flavor")
			else:
				tagkeys=("name","keyword","body","flavor")
			
			taglines=[]
			for j in range(4):
				try:
					row=csv_rows[i+j]
				except IndexError:
					break
					
				cell=row[3].strip()
				if (j!=0) and (row[1].strip()): # next entry!
					break
				if cell:
					
					taglines.append(cell)
			if not taglines[-1]:
				del taglines[-1]
				
			tagkeys={
				1:("name",),
				2:("name","flavor"),
				3:("name","body","flavor"),
				4:("name","keyword","body","flavor")}[len(taglines)]
			for j in range(len(taglines)):
				dat[tagkeys[j]]=taglines[j]
			'''
			for j in range(len(tagkeys)):
				tagkey=tagkeys[j]
				try:
					row=csv_rows[i+j]
				except IndexError:
					break
					
				cell=row[3]
				#print(row,tagkey,cell)
				if (j!=0) and (row[1].strip()): # next entry!
					break
				if cell:
					dat[tagkey]=cell
			'''
			#print("Add Transl. Entry:",key)
			if key in res:
				print("DUPLICATE ENTRY!",key)
			res[key]=dat
		i+=1
	print(F"{filepath} parsed: {len(res)} entries")
	return res


translation_data=dict()
translation_data.update(parse_csv("TranslationData/pony.csv"))
translation_data.update(parse_csv("TranslationData/goal.csv",is_goal=True))
translation_data.update(parse_csv("TranslationData/ship.csv"))

TYPE, PICTURE, SYMBOLS, TITLE, KEYWORDS, BODY, FLAVOR, EXPANSION, CLIENT = range(9)


with open("TSSSF/Core 1.1.5/cards.pon","r",encoding="utf-8") as f:
	orig_pon=f.read()

orig_lines=orig_pon.split("\n")
translated_lines=[]

print("Translating...")
for orig_line in orig_lines:
	orig_tags=orig_line.split('`')
	#print(orig_tags)
	
	if len(orig_tags)<6:
		continue
	title=orig_tags[3]
	keyword=orig_tags[4]
	body=orig_tags[5]
	flavor=orig_tags[6]
	
	key=unwhite(unescape(title))
	#print("Finding",key)
	if key in translation_data:
		
		dat=translation_data[key]
		if "name" in dat:
			title=escape(dat["name"])
		if "keyword" in dat:
			keyword=escape(dat["keyword"])
		if "body" in dat:
			body=apply_mappings(escape(dat["body"]))
		if "flavor" in dat:
			flavor=escape(dat["flavor"])
		
		#print("  Trans data found:",dat)
	else:
		print(" ### No trans data found!",key)
	
	translated_tags=orig_tags[:3]+[title,keyword,body,flavor]+orig_tags[7:]
	#print(translated_tags)
	
	translated_lines.append('`'.join(translated_tags))
print(F"Translated {len(translated_lines)} entries.")


with open("TSSSF/Core 1.1.5/cardsKR.pon","w",encoding="utf-8") as f:
	f.write("\n".join(translated_lines))
