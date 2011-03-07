dojo.require('dojox.dtl.filter.strings');
dojo.require("dijit.TooltipDialog");
dojo.require("dijit.form.Button");

// dojo.ready(function(node, args){

//   node = dojo.byId(node);

//   var getDialog = function(node, args){
//     console.log('getDialog', node,args);
    
//     var opts = dojo.mixin({ iconClass: 'tooltipIcon' }, args || {});
//     node = dojo.byId(node);
      
//     // url to doc
//     var href =  node.href;
//     node.innerHTML = "";
//     node.className = node.className + "-processed";
    
//     var dialog = new dijit.TooltipDialog({ 
//       href: href,       
//       style: "width:400px;height:200px",
//       // handles truncation of downloaded help text.
//       onDownloadEnd: function(e){
//         var node = dojo.byId('body');
//         var html = node.innerHTML;
//         var truncated = dojox.dtl.filter.strings.truncatewords_html(html, 30);
//         var i = truncated.lastIndexOf('...'); 
//         if(i != -1){ 
//           truncated = truncated.substr(0, i); // remove the trailing .
//           var summary = dojo.create('div', { innerHTML: truncated});
//           var expandLink = dojo.create('a', { innerHTML: "(more)", href: "#", title: "more" });
//           expandLink.onclick = function(){
//             dojo.byId('body').innerHTML = html;
//           };
//           node.innerHTML = "";
//           node.appendChild(summary);
//           node.appendChild(expandLink);
//         }
//       },
    
//       onClick: function(e){
//         e.stopPropagation();
//         e.preventDefault();
//       },
                                           
//       onBlur: function(){
//         dijit.popup.close(this);
//       } 
//     });
//     return dialog;
//   };

//   // not using dropdownbutton because:
//   // * can't stop the onclick event from propagating
//   // * the popup is placed at the wrong position when inside data grids.
//   var tooltipButton = function(node, args){
//     return new dijit.form.Button({
//       label: "help",                                   
//       baseClass: "tooltip",
//       // iconClass: opts.iconClass,
      
//       onClick: function(e){
        
//         dijit.popup.open({
//           popup: getDialog(node, args),
//           around: node,
//           orient: {'BR':'TR', 'BL':'TL', 'TR':'BR', 'TL':'BL'},
//           onCancel: function(){
//             dijit.popup.close(this.popup);
//           },
//           onClose: function(){
//             dijit.popup.close(this.popup);
//           }
//         });
//         // this stopped working in dojo 1.5
//         e.stopPropagation();
//         e.preventDefault();
//       }
//     });
//   };


//   var doc = {

//     server:'/',

//     body_suffix: '/body',

//     show: function(node, args){
//       node = dojo.byId(node);
//       var dialog = new dijit.TooltipDialog({content: 'fdasf dafasd'}, node);

//       var button = new dijit.form.DropDownButton({
//         label: "show tooltip dialog",
//         dropDown: dialog
//       });
//       button.appendTo(node);
//       // tooltipButton(node, args).placeAt(node);
//       // dojo.fadeIn({ node: node }).play();
//     }
//   };

//   var helpTooltip = function(node, args){
//     doc.show(node, args);
//   };

//   dojo.extend(dojo.NodeList, {
//     helpTooltip: dojo.NodeList._adaptAsForEach(helpTooltip)
//   });
 
//   console.log(dojo.query('[caboType=docs]'));
             
//   dojo.query('[caboType=docs]').helpTooltip();
// });



dojo.require("dijit.form.DropDownButton");
dojo.require("dijit.TooltipDialog");
dojo.require("dijit.form.TextBox");
dojo.require("dijit.form.Button");

dojo.addOnLoad(function() {
  var dialog = new dijit.TooltipDialog({
    content: '<div><label for="name">Name:</label> <input dojoType="dijit.form.TextBox" id="name" name="name"><br>' + '<label for="hobby">Hobby:</label> <input dojoType="dijit.form.TextBox" id="hobby" name="hobby"><br>' + '<button dojoType="dijit.form.Button" type="submit">Save</button></div>'
   });

   var button = new dijit.form.DropDownButton({
       label: "show tooltip dialog",
       dropDown: dialog
   });
   dojo.byId("help").appendChild(button.domNode);
});