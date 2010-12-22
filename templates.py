from string import Template

from models import User

base_template = Template("""<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Steam Engine | Documentation</title>

    <link href="css/style.css" rel="stylesheet" />
    <script src="//ajax.googleapis.com/ajax/libs/dojo/1.5/dojo/dojo.xd.js" 
            djConfig="isDebug:true,parseOnLoad:true"></script>
    <script type="text/javascript">
      dojo.require("dojox.widget.Toaster");
      dojo.require("dijit.form.Button");
    </script>
  </head>
  <body class="tundra docs" style="height: 495px;width:100%">

    <div style="margin: 20px" id="search">
      <a href="/">Overview</a>

      <form action="/search/" style="float:right">
        <span id="help_8" class="helpTooltip" style="opacity:0"></span>
        <input type="text" name="q" value="${q}" />
        <input type="submit" value="search" class="dijitButtonNode" />
      </form>
  
      $body
      
      <div id="toaster">
      </div>
   </div>

    <script src="js/steamengine/docs.js"></script>
    <script src="js/steamengine/enginedoc.js"></script>
    <script>
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

not_found_template = Template("""
  <h1>Page Not Found</h1>
  <p>
    The page you have requested does not exist on this server.  
  </p>
""")

def render(template, **kwargs):
    kwargs.update({
      'q': kwargs.get('q','')
      })
    return template.substitute(**kwargs)

def not_found():
    page = render(not_found_template)
    return render(base_template, title="Not Found", body=page)

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

    searchurl = "/search/?q=%s" % (query)  
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
    if User.is_staff():
        edit_link = '<a href="%sedit/" class="red">[edit]</a>' % (doc.url)
        doc.body = doc.body + edit_link
    t = render(doc_template, title=doc.title, body=doc.body)
    return render(base_template, title=doc.title, body=t)

def doc_body(dict):
    return render(doc_summary_template, title=dict['title'], body=dict['body'], url=dict['url'])
    
def docs(dict):
    items = []
    current_category = None
    for t in dict.get('docs'):
        if t.category != current_category:
            current_category = t.category
            items.append('</ul><h2>%s</h2><ul>' % current_category)
        if User.is_staff():
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
        }
        htmltitle = "Edit %s" % instance.title
    else:
        values = {
            'body' :'',
            'category':'',
            'title': '',
            'action': '/',
            'id': 'newForm',
            'clearFormOnSuccess': 'true',
            }
        htmltitle = "Add documentation"
    
    form = render(doc_form_template, **values)
    return render(base_template, title=htmltitle, body=form)
