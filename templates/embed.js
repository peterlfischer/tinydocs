!window.dojo && document.write('<script src="//ajax.googleapis.com/ajax/libs/dojo/1.5/dojo/dojo.xd.js"><\/script>');

dojo.ready(function(){

  dojo.require('dijit.form.DropDownButton');
  dojo.require('dijit.TooltipDialog');
  dojo.require('dojo.io.script');
  
  function loadStylesheet(){
    var link = dojo.create("link", {
      type: "text/css",
      rel: "stylesheet",
      href: "{{HOST}}/static/css/embed.css"
    });
    dojo.doc.getElementsByTagName("head")[0].appendChild(link);
  }

  function getTopic(url){
    var args = {
      url: url + '/jsonp',
      callbackParamName: 'callback'
    };
    return dojo.io.script.get(args);
  }
  
  function tooltip(node, args){
    node = dojo.byId(node);
  
    var topic_url = node.href;
  
    var dialog = new dijit.TooltipDialog({
      style:"width:200px"
    });
    
    var button = new dijit.form.DropDownButton({
      dropDown: dialog,
      baseClass:"irigo-tooltip",
      iconClass:"irigo-tooltip-icon",
      onClick: function(e){
        var dfd = getTopic(topic_url);
        dfd.then(function(js){
          dialog.set('content', '<h3>' + js.name + '</h3><p>' + js.body + '</p>');
        });
      }
    }); 
    // replacing the a tag!
    dojo.place(button.domNode, node, 'replace');
  }

  function dialog(node, args){
    node = dojo.byId(node);

    var topic_url = node.href;

    var dialog = new dijit.Dialog({
      style:"width:200px"
    });

    var button = new dijit.form.DropDownButton({
      baseClass:"irigo-tooltip",
      iconClass:"irigo-tooltip-icon",
      onClick: function(e){
        var dfd = getTopic(topic_url);
        dfd.then(function(js){
          dialog.set('content', '<h3>' + js.name + '</h3><p>' + js.body + '</p>');
        });
        dialog.show();
      }
    });
    // replacing the a tag!
    dojo.place(button.domNode, node, 'replace');
  }
  
  loadStylesheet();
  
  dojo.extend(dojo.NodeList, {
    irigoTooltip: dojo.NodeList._adaptAsForEach(tooltip),
    irigoDialog: dojo.NodeList._adaptAsForEach(dialog)
  });

  IRIGO = {
    getTopic: getTopic
  };

});
