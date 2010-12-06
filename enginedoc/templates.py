from string import Template

from consts import MEDIAURL
from consts import PREFIXURL

from models import User

base_template = Template("""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8" />
	  <title>Steam Engine | Documentation</title>

    <link href="${mediaurl}css/style.css" rel="stylesheet" type="text/css" />
    <script src="//ajax.googleapis.com/ajax/libs/dojo/1.5/dojo/dojo.xd.js">
         type="text/javascript" djConfig="isDebug:true,parseOnLoad:true"></script>
    <script type="text/javascript">
      dojo.require("dojox.widget.Toaster");
      dojo.require("dijit.form.Button");
    </script>

  </head>
  <body class="tundra docs" style="height: 495px;width:100%">

    <div style="margin: 20px" id="search">
      <a href="$prefixurl">Overview</a>

      <form action="${prefixurl}search/" style="float:right">
        <span id="help_8" class="helpTooltip" style="opacity:0"></span>
        <input type="text" name="q" value="${q}" />
        <input type="submit" value="search" class="dijitButtonNode" />
      </form>
  
      $body
      
      <div id="toaster">
      </div>
   </div>

    <script type="text/javascript" src="${mediaurl}js/steamengine/docs.js"></script>
    <script type="text/javascript" src="${mediaurl}js/steamengine/enginedoc.js"></script>
    <script type="text/javascript">
      var isIframe = window.top !== this;

      dojo.query('a').onclick(function(e){
        // are we in an iframe?
        if(isIframe){
          e.preventDefault();
          if(dojo.isIE){
             parent.location.hash = '_help/' + this.pathname;
          }
          else{
             parent.location.hash = '_help' + this.pathname;
          }
        }
      });

      dojo.ready(function(){
        dojo.query('.helpTooltip').helpTooltip();
        var toaster = new dojox.widget.Toaster({
            id: 'dojoToaster',
            positionDirection: "bl-up",
            messageTopic : "message"
        },
        dojo.byId('toaster'));
      });
     </script>
  </body>
</html>
""")

doc_form_template = Template("""
<form id="$id" method="post" action="$action" class="aligned">
  <p>
    <label for="category">Category:</label>
    <input id="category" type="text" name="category" value="$category" />
  </p>

  <p>
    <label for="title">Title:</label>
    <input id="title" type="text" name="title" value="$title"/>
  </p>

  <p>
    <label for="body">Body:</label>
    <textarea name="body" cols="80" rows="20">$body</textarea>
  </p>

  <div>
    <button id="formButton" type="submit">Save</button>
    <a href="$prefixurl">Back</a>
  </div>

</form>

<script type="text/javascript">
dojo.addOnLoad(function(){
  ed.form({domId:'$id', clearOnSuccess: $clearFormOnSuccess});
});
</script>
""")

docs_template = Template("""
<a href="new/">Add</a>
<h1>Steam Engine Documentation</h1>
<ul>
  $items
</ul>
""")

doc_template = Template("""
<h1>$title</h1>
<div>$body</div>
""")

doc_summary_template = Template("""
<h1>$title</h1>
<div id="body" class="tundra">$body</div>
""")

search_template = Template("""
<div>
<h1>Search Results</h1>
<div id="search_info" style="float:right">
$search_info
</div>
<ul>
$results
</ul>
$search_links
</div>
""")

def render(template, **kwargs):
    kwargs.update({
            'mediaurl': MEDIAURL,
            'prefixurl': PREFIXURL,
            'q': kwargs.get('q','')
            })
    return template.substitute(**kwargs)

def search(dict):
    # from whoosh import highlight
    # from whoosh.analysis import StandardAnalyzer
    results = dict['results']
    count = results.total
    query = dict['q']

    # FIXME: move somewhere sensible
    def truncate_words(s, url, length):
        "Truncates a string after a certain number of words."
        words = s.split()
        if len(words) > length:
            words = words[:length]
            words.append('<br /><a href="%s">[more]</a>' % url)
        return u' '.join(words)

    items = []
    for r in results:
        r.update({'body': truncate_words(r['body'], r['url'], 30)})
        # body = highlight.highlight(
        #     r['body'],
        #     results.results.query.all_terms(), # <-- error :(
        #     StandardAnalyzer(),
        #     highlight.SimpleFragmenter(),
        #     highlight.HtmlFormatter())
        items.append('<li><h3><a href="%(url)s">%(category)s | %(title)s</a></h3><p>%(body)s</li>' % r)
    items = ''.join(items) if items else "<li>Your search didn't return any results</li>"

    if count == 1:
        search_info = "%s topic matches '<b>%s</b>'" % (count, query)
    else:
        search_info = "%s topics match '<b>%s</b>'" % (count, query)

    searchurl = "%ssearch/?q=%s" % (PREFIXURL, query)  
    links = []
    for p in range(results.pagecount):
        p = p + 1 # we index from 1
        if(p != results.pagenum):
            links.append('<li><a href="%s&page=%s">%s</a></li>' % (searchurl,p,p))
        else:
            links.append('<li>%s</li>' % p)
    links = '<ul id="nav">%s</ul>' % ("".join(links)) if len(links) > 1  else ''
    t = render(search_template, results=items, search_info=search_info,q=query, search_links=links)
    return render(base_template, title="Search Results", body=t, q=query)
    
def doc(dict):
    doc = dict['doc']
    user = User.get_current_user()
    if user and user.is_staff:
        edit_link = '<a href="%sedit/" class="red">[edit]</a>' % (doc.url)
        doc.body = doc.body + edit_link
    t = render(doc_template, title=doc.title, body=doc.body)
    return render(base_template, title=doc.title, body=t)

def doc_body(dict):
    return render(doc_summary_template, title=dict['title'], body=dict['body'], url=dict['url'])
    
def docs(dict):
    items = []
    current_category = None
    user = User.get_current_user()
    for t in dict.get('docs'):
        if t.category != current_category:
            current_category = t.category
            items.append('</ul><h2>%s</h2><ul>' % current_category)
        if user and user.is_staff:
            items.append('<li><a href="%s">%s</a> <a href="%sedit/" class="red">[edit]</a></li>' % (t.url, t.title, t.url))
        else:
            items.append('<li><a href="%s">%s</a></li>' % (t.url, t.title))
    docs = render(docs_template, items='\n'.join(items))
    return render(base_template, title="Documentation", body=docs)
        
def doc_form(dict):
    instance = dict['instance']
    referer = dict['request'].headers.get('referer')
    if(instance):
        values = {
        'body': instance.body,
        'category': instance.category,
        'title': instance.title,
        'action': instance.url,
        'id': 'form',
        'clearFormOnSuccess': 'false',
        'referer': referer,
        'prefixurl': PREFIXURL
        }
        htmltitle = "Edit %s" % instance.title
    else:
        values = {
            'body' :'',
            'category':'',
            'title': '',
            'action': PREFIXURL,
            'id': 'newForm',
            'clearFormOnSuccess': 'true',
            'prefixurl': PREFIXURL
            }
        htmltitle = "Add documentation"
    
    form = render(doc_form_template, **values)
    return render(base_template, title=htmltitle, body=form)
