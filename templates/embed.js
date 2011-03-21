// Requires the user to include dojo at the moment!!

dojo.require('dijit.Dialog');
dojo.require('dijit.TooltipDialog');
dojo.require('dijit.form.DropDownButton');
dojo.require('dojo.io.script');

dojo.ready(function(){
  
  function loadStylesheet(){
    var link = dojo.create("link", {
      type: "text/css",
      rel: "stylesheet",
      href: "//{{host}}/static/css/embed.css"
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
      baseClass:"irigo-tooltip-base",
      iconClass:"irigo-tooltip-base-icon",
      onClick: function(e){
        e.preventDefault();
        e.stopPropagation();
        var dfd = getTopic(topic_url);
        dfd.then(function(js){
          dialog.set('content', '<p>' + js.excerpt + ' (<a href="' + topic_url + '" target="_blank">more</a>)</p>');
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
      baseClass:"irigo-tooltip-base",
      iconClass:"irigo-tooltip-base-icon",
      onClick: function(e){
        var dfd = getTopic(topic_url);
        dfd.then(function(js){
          dialog.set('title', js.name);
          dialog.set('content', '<p>' + js.excerpt + '</p><p style="float:right"><a href="' + topic_url + '">more</a></p>');
        });
        dialog.show();
      }
    });
    // replacing the a tag!
    dojo.place(button.domNode, node, 'replace');
  }

  function text(node, args){
    node = dojo.byId(node);

    var topic_url = node.href;

    var dfd = getTopic(topic_url);
    dfd.then(function(js){
      var wrapper = dojo.create('div', { 
        innerHTML: '<h3>' + js.name + '</h3><p>' + js.excerpt + '</p>'
      });
      // replacing the a tag!
      dojo.place(wrapper, node, 'replace');
    });
  }
  
  loadStylesheet();
  
  dojo.extend(dojo.NodeList, {
    irigoTooltip: dojo.NodeList._adaptAsForEach(tooltip),
    irigoDialog: dojo.NodeList._adaptAsForEach(dialog),
    irigoText: dojo.NodeList._adaptAsForEach(text)
  });

  IRIGO = {
    getTopic: getTopic
  };

});

