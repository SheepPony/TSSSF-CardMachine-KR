import csv

def unwhite(s):
	return s.replace(" ","").replace("\n","").replace("\t","").replace("…","").replace(".","").replace("-","").replace('"','').lower()
	
def unescape(s):
	return s.replace("\\n","\n").replace("\'","'")
def escape(s):
	#return repr(s)[1:-1]
	return s.replace("\n","\\n")


with open("TranslationData/mapping_v2.csv","r",encoding="utf-8") as f:
	csv_rows=list(csv.reader(f))
csv_rows=csv_rows[1:]

keyword_mappings=dict()
for row in csv_rows:
	k=row[1]
	v=row[3]
	keyword_mappings[k]=v
print(F"Loaded {len(keyword_mappings)} mappings.")
	
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
	print(F"{filepath} parsed (V1): {len(res)} entries")
	return res
	
def parse_csv_v2(filepath,*,parse_end=None,prune_empty=False):
	res=dict()
	with open(filepath,"r",encoding="utf-8") as f:
		csv_rows=list(csv.reader(f))
	
	if parse_end:
		csv_rows=csv_rows[:parse_end]
	csv_rows=csv_rows[1:]
	for row in csv_rows:
		key=unwhite(row[1]) # EN Name
		if prune_empty:
			if not row[6].strip():
				print("Skipping empty row:")
				print("   ",filepath)
				print("   ",key)
				continue
		dat={
			"name":row[6],
			"keyword":row[7],
			"body":row[8],
			"flavor":row[9]+" - "+row[10]}
		res[key]=dat
	print(F"{filepath} parsed (V2): {len(res)} entries")
	return res

translation_data=dict()
#translation_data.update(parse_csv("TranslationData/pony.csv"))
translation_data.update(parse_csv_v2("TranslationData/pony_v2.csv"))
translation_data.update(parse_csv_v2("TranslationData/goal_v2.csv"))
translation_data.update(parse_csv_v2("TranslationData/ship_v2.csv"))
#translation_data.update(parse_csv("TranslationData/ECship.csv",is_goal=False))
#translation_data.update(parse_csv("TranslationData/ECgoal.csv",is_goal=True))
translation_data.update(parse_csv_v2("TranslationData/ECgoal_v2.csv"))#,prune_empty=True))
translation_data.update(parse_csv_v2("TranslationData/ECship_v2.csv"))#,prune_empty=True))

TYPE, PICTURE, SYMBOLS, TITLE, KEYWORDS, BODY, FLAVOR, EXPANSION, CLIENT = range(9)

def translate(ponE,ponK):
	print(ponE,"to",ponK)
	with open(ponE,"r",encoding="utf-8") as f:
		orig_pon=f.read()

	orig_lines=orig_pon.split("\n")
	translated_lines=[]

	print("Translating...")
	for orig_line in orig_lines:
		orig_tags=orig_line.split('`')
		#print(orig_tags)
		
		if len(orig_tags)<6:
			translated_lines.append(orig_line)
			print("Copying line",repr(orig_line))
			continue
		kind=orig_tags[0]
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
				if kind.lower()=="goal":
					body="다음 상황에서 이 목표가 달성됩니다:\\n"+body
					
			if "flavor" in dat:
				flavor=escape(dat["flavor"])
			
			#print("  Trans data found:",dat)
		else:
			print(" ### No trans data found!",key)
		
		translated_tags=orig_tags[:3]+[title,keyword,body,flavor]+orig_tags[7:]
		#print(translated_tags)
		
		translated_lines.append('`'.join(translated_tags))
	print(F"Translated {len(translated_lines)} entries.")


	with open(ponK,"w",encoding="utf-8") as f:
		f.write("\n".join(translated_lines))

translate("TSSSF/Core 1.1.5/cards.pon","TSSSF/Core 1.1.5/cardsKR.pon")
translate("TSSSF/Extra Credit 1.0.1/cards.pon","TSSSF/Extra Credit 1.0.1/cardsKR.pon")
