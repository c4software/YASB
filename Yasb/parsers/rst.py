from docutils.core import publish_parts, publish_doctree
from docutils.nodes import docinfo

def run(text):
	# Extraction des champs, et transformation du rst en html
	rst = publish_parts(text, writer_name="html")
	fields = extract_fields(text)
	fields['title'] = rst['title']
	return rst['body'], fields

def extract_fields(text):
	doctree = publish_doctree(text)
	fields = {}
	for docinfos in doctree.traverse(docinfo):
		for element in docinfos.children:
			if element.tagname == 'field':  # custom fields (e.g. summary)
					name_elem, body_elem = element.children
					name = name_elem.astext()
					value = body_elem.astext()
			else:  # standard fields (e.g. address)
					name = element.tagname
					value = element.astext()
			fields[name]=value

	return fields
