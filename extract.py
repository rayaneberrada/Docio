# coding: utf-8
import xml.etree.ElementTree as ET
import pymysql.cursors
import argparse
import json

connection = pymysql.connect(host='localhost',
                             user='rayane',
                             password='i77EWEsN',
                             db='dictionnary',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

parser = argparse.ArgumentParser()
parser.add_argument("file_name")
parser.add_argument("-s", const=True, nargs='?')
parser.add_argument("-n")
args = parser.parse_args()

insert_word = ("INSERT INTO mot (orthographe, nature_grammaticale, genre, etymologie) VALUES (%s, %s, %s, %s)")
get_word = ("SELECT MAX(id) FROM mot")
insert_defs = ("INSERT INTO definition(description, mot_id) VALUES (%s, %s)")
get_def = ("SELECT id FROM definition WHERE description=%s")
get_label = ("SELECT id FROM unite_terminologique WHERE nom=%s")
insert_label = ("INSERT INTO unite_terminologique (nom, description) VALUES (%s, %s)")
link_label_def = ("INSERT INTO terme_definition (definition_id, terme_id) VALUES (%s, %s)")
get_word_syn_ant = ("SELECT mot_id FROM definition WHERE description=%s")
cursor = connection.cursor()

print(args)

if args.n:
	previous = None
	word = {}
	for event, elem in ET.iterparse(args.file_name):
		if 'title' in elem.tag:
			if word:
				if not "lemma" in word and "etymology" in word:
					grammar = "Préfixe" if word["title"][-1] == "-" else "Unknown"
					gender = word["gender"] if "gender" in word else None
					try:
						cursor.execute(insert_word, (word["title"], grammar, gender, word["etymology"]))
						connection.commit()
					except:
						print(word)
				word = {}
			word["title"] = elem.text

		if "text" in elem.tag:
			for textchild in elem:
				if "etymology" in textchild.tag:
					for etymchilds in textchild:
						if etymchilds.tag == "etym":
							for etymchild in etymchilds:
								if etymchild.tag == "txt":
									word["etymology"] = etymchild.text if "etymology" not in word else word["etymology"] + " " + etymchild.text

				if textchild.tag == "pos":
					if "locution" in textchild.attrib:
						if textchild.attrib["locution"] == "1": word["locution"] = 1

					if textchild.attrib["lemma"] == "0": word["lemma"] = 0
					if textchild.attrib["lemma"] == "1":
						word["lemma"] = 1
						word["grammar"] = textchild.attrib['type']
						try:
							word["gender"] = textchild.attrib['gender']
						except:
							pass

						for definitionschild in textchild:
							if "definitions" in definitionschild.tag:
								definitions = []
								for definitionchild in definitionschild:
									if "definition" in definitionchild.tag:
										definition = {}
										labels = []
										for data in definitionchild:
											if data.tag in "gloss":
												for subdata in data:
													if subdata.tag == "labels":
														for label in subdata:
															labels.append(label.attrib['value'])
														definition["label"] = labels
													if subdata.tag == "txt":
														definition["description"] = subdata.text
										definitions.append(definition)
								word["definitions"] = definitions
						grammar = word["grammar"] if word["grammar"] else "Unknown"
						gender = word["gender"] if "gender" in word else None
						etymology = word["etymology"] if "etymology" in word else "Unknown"

						cursor.execute(insert_word, (word["title"], grammar, gender, etymology))

						cursor.execute(get_word)
						word_id = cursor.fetchone()['MAX(id)']
						print(word_id)
						#Pour chaque définition dans la liste des définitions:
						for definition in word["definitions"]:
							if definition:
								cursor.execute(insert_defs, (definition["description"], word_id))
							else:
								continue
							cursor.execute(get_def, definition["description"])
							def_id = cursor.fetchone()['id']
							if "label" in definition:
								for label in definition["label"]:
									exist = cursor.execute(get_label, label)
									if not exist:
										cursor.execute(insert_label, (label, None))
									cursor.execute(get_label, label)
									label_id = cursor.fetchone()['id']
									cursor.execute(link_label_def, (def_id ,label_id))
						connection.commit()
					"""
					if "lemma" and word["title"] == previous:
						print("value:"+str(len(word)))
						print(word)
						pass
					previous = word["title"]
					display words with multiple pos values
					"""

if args.s:
	word = {}
	for event, elem in ET.iterparse(args.file_name):
		if 'title' in elem.tag:
			if word:
				word = {}
			word["title"] = elem.text

		if "text" in elem.tag:
			for textchild in elem:
				if textchild.tag == "pos":
					if textchild.attrib["lemma"] == "1":
						for definitionschild in textchild:
							if "definitions" in definitionschild.tag:
								for definitionchild in definitionschild:
									if "definition" in definitionchild.tag:
										definition = {}
										labels = []
										for data in definitionchild:
											if data.tag in "gloss":
												for subdata in data:
													if subdata.tag == "txt":
														definition = subdata.text
						synonym = []
						antonym = []
						for poschild in textchild:
							if poschild.tag == "subsection":
								for subsectionchild in poschild:
									if "type" in subsectionchild.attrib:
										cursor.execute(get_word_syn_ant, definition)
										word["word_id"] = cursor.fetchone()['mot_id']
										if subsectionchild.attrib["type"] == "synonym":
											synonym.append(subsectionchild.text)
										if subsectionchild.attrib["type"] == "antonym":
											antonym.append(subsectionchild.text)
						word["synonym"] = synonym
						word["antonym"] = antonym

						if word["synonym"] or word["antonym"]:
							print(word)


"""
	grammar = word["grammar"] if "grammar" in word else "Unknown"
	gender = word["gender"] if "gender" in word else "Unknown"
	etymology = word["etymology"] if "etymology" in word else "Unknown"
	cursor.execute(insert_word, (word["title"], grammar, gender, etymology))
	for definition in word["definitions"]:
		cursor.execute(insert_defs, ())
"""
	#Ajouter dernier élément en db à la fin

#cas de l'etmology divisée quand sur plusieurs lignes (voir fondue fribourgeoise )
# vérifier que descritpion et titre sont non nul
# Titre / Genre / définitions et Labels / nature grammaticale / etymology / Locution / lemme
"""
		if int(elem.attrib['pageid']) != previous + 1:
			print("len: " + str(len(dictionnaire)) + " previous/id: " + str(previous) + "/" + elem.attrib['pageid'])
			raise NameError("Error at: " + str(previous))
		previous += 1
"""
#with open("dictionnaire.py", "w") as f:
#	f.write(json.dumps(dictionnaire))