import csv

# Some string manipulation functions
def unwhite(s):
	return s.replace(" ","").replace("\n","").replace("\t","").replace("…","").replace(".","").replace("-","").replace('"','').lower()
def unescape(s):
	return s.replace("\\n","\n").replace("\'","'")
def escape(s):
	return s.replace("\n","\\n")

## Keyword Mappings
# Read CSV
# CSV Columns: NUMBER KEYWORD EN_TEXT KR_TEXT
with open("TranslationData/mapping_v2.csv","r",encoding="utf-8") as f:
	csv_rows=list(csv.reader(f))

# Skip header
csv_rows=csv_rows[1:]

# Load CSV into a dict
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


## Translation Database Parse
ficname_map=dict()
def parse_csv_v2(filepath):
	'''
	Parses Translation data CSV.
	CSV Rows: EN_NAME EN_KEYWORD EN_TEXT EN_FLAVOR EN_FICNAME 
	          KR_NAME KR_KEYWORD KR_TEXT KR_FLAVOR KR_FICNAME
	Result is a dict, mapping the card name into the translation data.
	'''
	
	# Read CSV
	res=dict()
	with open(filepath,"r",encoding="utf-8") as f:
		csv_rows=list(csv.reader(f))
	
	# Skip header
	csv_rows=csv_rows[1:]
	
	for row in csv_rows:
		
		key=unwhite(row[1]) # EN Name
		
		ficnameE=row[5]
		ficnameK=row[10]
		
		# Check if ficname is consistently translated
		if ficnameE in ficname_map:
			if ficname_map[ficnameE] != ficnameK:
				print("Ficname mismatch:",ficnameE)
				print(ficnameK,"!=",ficname_map[ficnameE])
				0/0
		ficname_map[ficnameE] = ficnameK
		
		flavorK=row[9]
		
		if ficnameK:
			# Insert line break hint
			# I'm using U+EB44, a Private Use Area code point.
			flavor_composite=flavorK+"\uEB44 - "+ficnameK 
		else:
			flavor_composite=flavorK
		
		dat={
			"name":row[6],
			"keyword":row[7],
			"body":row[8],
			"flavor":flavor_composite} 
		res[key]=dat
	
	print(F"{filepath} parsed (V2): {len(res)} entries")
	return res

# Gather all translation data
translation_data=dict()
translation_data.update(parse_csv_v2("TranslationData/pony_v2.csv"))
translation_data.update(parse_csv_v2("TranslationData/goal_v2.csv"))
translation_data.update(parse_csv_v2("TranslationData/ship_v2.csv"))
translation_data.update(parse_csv_v2("TranslationData/ECgoal_v2.csv"))
translation_data.update(parse_csv_v2("TranslationData/ECship_v2.csv"))


def translate(ponE,ponK):
	'''
	Actually translate the .pon files,
	given the filepaths.
	'''
	print("Translating",ponE,"to",ponK)
	
	# Read original .pon
	with open(ponE,"r",encoding="utf-8") as f:
		orig_pon=f.read()
	orig_lines=orig_pon.split("\n")
	
	
	print("Translating...")
	translated_lines=[]
	
	for orig_line in orig_lines:
		# Parse line
		orig_tags=orig_line.split('`')
		if len(orig_tags)<6:
			# If line is too short, it's probably a special card.
			# Copy the line as-is.
			translated_lines.append(orig_line)
			print("Copying line",repr(orig_line))
			continue
		kind=orig_tags[0]
		title=orig_tags[3]
		keyword=orig_tags[4]
		body=orig_tags[5]
		flavor=orig_tags[6]
		
		# The key for the translation data is the card's title without whitespaces.
		# THIS ASSUMES ALL CARD NAMES ARE UNIQUE!
		key=unwhite(unescape(title))
		
		if key in translation_data:
			
			# Apply translations
			dat=translation_data[key]
			if "name" in dat:
				title=escape(dat["name"])
			if "keyword" in dat:
				keyword=escape(dat["keyword"])
			if "body" in dat:
				# Need to add the goal text
				body=apply_mappings(escape(dat["body"]))
				if kind.lower()=="goal":
					body="다음 상황에서 이 목표가 달성됩니다:\\n"+body
			if "flavor" in dat:
				flavor=escape(dat["flavor"])
		else:
			print(" ### No trans data found!",key)
		
		# For other data, copy as-is.
		translated_tags=orig_tags[:3]+[title,keyword,body,flavor]+orig_tags[7:]
		
		translated_lines.append('`'.join(translated_tags))
	
	print(F"Translated {len(translated_lines)} entries.")
	
	# Write out the translated .pon file.
	with open(ponK,"w",encoding="utf-8") as f:
		f.write("\n".join(translated_lines))

# All the translation targets.
translate("TSSSF/Core 1.1.5/cards.pon","TSSSF/Core 1.1.5/cardsKR.pon")
translate("TSSSF/Extra Credit 1.0.1/cards.pon","TSSSF/Extra Credit 1.0.1/cardsKR.pon")
