def strip_indents(text):
   # textwrap.dedent() / inspect.cleandoc() won't work here as i like to add extra indentation to my multiline strings
   return "\n".join([t.strip() for t in text.splitlines()])