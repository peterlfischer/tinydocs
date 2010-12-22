/*global
dojo:false,
dijit:false,
dojox:false
 */
dojo.require('dojox.dtl.filter.strings');
dojo.require("dijit.TooltipDialog");
dojo.require("dijit.form.Button");

var help = {};

help.uriprefix = "/steamengine/docs/"; 
help.urisuffix = "/body/";

/**
 * Adds tooltip to any node.
 * 
 * The node must have the following format:
 * <node id="help_{id}"></node>
 * Where the id is the id in the docs db. 
 */
help.helpTooltip = function(node, args){
  var opts = dojo.mixin({ iconClass: 'tooltipIcon' }, args || {});
  
  node = dojo.byId(node);

  // url to doc
  var doc_id = node.id.substr(5); // help_{id}
  var href =  help.uriprefix + doc_id + help.urisuffix;
  node.innerHTML = "";
  node.className = node.className + "-processed";

  var dialog = new dijit.TooltipDialog({ 
    href: href,       
    style: "width:400px;",
    // handles truncation of downloaded help text.
    onDownloadEnd: function(e){
      var node = dojo.byId('body');
      var html = node.innerHTML;
      var truncated = dojox.dtl.filter.strings.truncatewords_html(html, 30);
      var i = truncated.lastIndexOf('...'); 
      if(i != -1){ 
        truncated = truncated.substr(0, i); // remove the trailing .
        var summary = dojo.create('div', { innerHTML: truncated});
        var expandLink = dojo.create('a', { innerHTML: "(more)", href: "#", title: "more" });
        expandLink.onclick = function(){
          dojo.byId('body').innerHTML = html;
        };
        node.innerHTML = "";
        node.appendChild(summary);
        node.appendChild(expandLink);
      }
    },

    onClick: function(e){
      e.stopPropagation();
      e.preventDefault();
    },
                                         
    onBlur: function(){
      dijit.popup.close(this);
    } 

  });
  
  // not using dropdownbutton because:
  // * can't stop the onclick event from propagating
  // * the popup is placed at the wrong position when inside data grids.
  var helpButton = new dijit.form.Button(
    {
      baseClass: "tooltip",
      iconClass: opts.iconClass,
      
      onClick: function(e){
        dijit.popup.open(
          {
            popup: dialog,
            around: this.domNode,
            orient: {'BR':'TR', 'BL':'TL', 'TR':'BR', 'TL':'BL'},
            onCancel: function(){
              dijit.popup.close(dialog);
          },
            onClose: function(){
              dijit.popup.close(dialog);
          }
        });
        // this stopped working in dojo 1.5
        e.stopPropagation();
        e.preventDefault();
      }
    });

  helpButton.placeAt(node);
  dojo.fadeIn({ node: node }).play();
};

help.helpTooltipSmall = function(node, args){
  var opts = dojo.mixin({}, args || {});
  opts.iconClass = 'tooltipIconSmall';
  help.helpTooltip(node, opts);
};

help.helpText = function(node, args){
  node = dojo.byId(node);
  var doc_id = node.id.substr(5); 
  var url =  help.uriprefix + doc_id + help.urisuffix;
  node.innerHTML = "";      
  node.className = node.className + '-processed';
  function onLoad(response){
    dojo.place('<div>' + response + '</div>', node);
    // parse the response allowing dojo attributes in html
    dojo.parser.parse(node);
  }
  dojo.xhrGet({url: url, load: onLoad});
};
    
/**
 * Extend the dojo.NodeList with helpTooltip.
 * Means that the following is possible:
 * dojo.query('.help').helpTooltip();
 */
dojo.extend(dojo.NodeList, {
  helpTooltip: dojo.NodeList._adaptAsForEach(help.helpTooltip)
});

dojo.extend(dojo.NodeList, {
  helpTooltipSmall: dojo.NodeList._adaptAsForEach(help.helpTooltipSmall)
});

dojo.extend(dojo.NodeList, {
  helpText: dojo.NodeList._adaptAsForEach(help.helpText)
});
