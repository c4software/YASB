from docutils.core import publish_parts, publish_doctree
from docutils.nodes import docinfo

import Yasb.htmlbuilder

def run(text, settings={}):
	# Extraction des champs, et transformation du rst en html
	rst = publish_parts(text, writer_name="html")
	fields = extract_fields(text)
	fields['title'] = rst['title']
	rst['body'] = body_as_template(rst['body'], fields, settings)
	return rst['body'], fields

def body_as_template(content, fields, settings):
	return Yasb.htmlbuilder.render(content, fields, settings)

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
