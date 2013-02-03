from jinja2 import Environment, FileSystemLoader

def build_html(content, fields, settings):
	#content = "{% extends template %}" # {% block content %}"+content+"{% endblock %}
	if "template" not in fields:
		fields['template'] = "base.html"
	f = fields.copy()
	f["content"] = content
	return render("{% extends template %}", f, settings)

def render(content, fields, settings):
	env = Environment(loader=FileSystemLoader(settings.get("theme")+"templates/"))
	
	if content == "":
		tpl = env.get_template(fields['template'])
	else:
		tpl = env.from_string(content)

	# Merge settings and fields to have it in the render context
	return tpl.render(**dict(settings.values.items()+fields.items()))