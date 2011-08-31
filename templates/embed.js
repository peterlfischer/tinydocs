// Requires the user to include dojo at the moment!!

dojo.require('dijit.Dialog');
dojo.require('dijit.TooltipDialog');
dojo.require('dijit.form.DropDownButton');
dojo.require('dojo.io.script');

dojo.ready(function(){

  var hasTundra = dojo.hasClass(dojo.body(), 'tundra');

  function addStyle(){
    if(!hasTundra){
      dojo.addClass(dojo.body(), 'tundra');
    }
  }

  function removeStyle(){
    if(!hasTundra){
      dojo.removeClass(dojo.body(), 'tundra');
    }
  }

  function loadStylesheet(){
    var head = dojo.doc.getElementsByTagName("head")[0];

    var embedCss = dojo.create("link", {
      type: "text/css",
      rel: "stylesheet",
      href: "//{{host}}/static/css/embed.css"
    });
    // add tundra css if not there!
    // FIXME: copy paste the relevant parts from that stylesheet into embed.css
    // and rename tundra.
    if(!hasTundra){
      var tundraCss = dojo.create("link", {
        type: "text/css",
        rel: "stylesheet",
        href: "//ajax.googleapis.com/ajax/libs/dojo/1.6/dijit/themes/tundra/tundra.css"
      });
      head.appendChild(tundraCss);
    }
    head.appendChild(embedCss);
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
      style:"width:300px"
    });
    
    var button = new dijit.form.DropDownButton({
      dropDown: dialog,
      baseClass:"irigo-tooltip-base",
      iconClass:"irigo-tooltip-base-icon",
      onOpen: function(){
        addStyle();
      },
      onClose: function(){
        removeStyle();
      },
      onClick: function(e){
        if(dialog.get('content') == ''){
          var dfd = getTopic(topic_url);
          dfd.then(function(js){
            dialog.set('content', '<p>' + js.excerpt + ' (<a href="' + topic_url + '" target="_blank">more</a>)</p>');
          });
        }
        // else, we've already loaded the content.
        dojo.stopEvent(e);
        return false;
      }
    }); 
    // replacing the a tag!
    dojo.place(button.domNode, node, 'replace');
  }

  function dialog(node, args){
    node = dojo.byId(node);

    var topic_url = node.href;

    var dialog = new dijit.Dialog({
      style:"width:300px"
    });

    var button = new dijit.form.DropDownButton({
      baseClass:"irigo-tooltip-base",
      iconClass:"irigo-tooltip-base-icon",
      onOpen: function(){
        addClass();
      },
      onClose: function(){
        removeClass();
      },
      onClick: function(e){
        if(dialog.get('content') == ''){
          var dfd = getTopic(topic_url);
          dfd.then(function(js){
            dialog.set('title', js.name);
            dialog.set('content', '<p>' + js.excerpt + '</p><p style="float:right"><a href="' + topic_url + '" target="_blank">more</a></p>');
          });
        }
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

