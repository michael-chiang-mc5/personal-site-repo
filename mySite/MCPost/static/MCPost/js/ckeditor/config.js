/**
 * @license Copyright (c) 2003-2015, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

 /*
  * Note: to set css of ckeditor iframe, edit ckeditor/contents.css
  */

CKEDITOR.editorConfig = function( config ) {
 	config.toolbarGroups = [
 		{ name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
 		{ name: 'insert', groups: [ 'insert' ] },
 		{ name: 'links', groups: [ 'links' ] },
 		{ name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi', 'paragraph' ] },
 		{ name: 'styles', groups: [ 'styles' ] },
 		{ name: 'editing', groups: [ 'find', 'selection', 'spellchecker', 'editing' ] },
 		{ name: 'forms', groups: [ 'forms' ] },
 		{ name: 'clipboard', groups: [ 'clipboard', 'undo' ] },
 		{ name: 'colors', groups: [ 'colors' ] },
 		{ name: 'tools', groups: [ 'tools' ] },
 		{ name: 'others', groups: [ 'others' ] },
 		{ name: 'about', groups: [ 'about' ] },
 		{ name: 'document', groups: [ 'mode', 'document', 'doctools' ] }
 	];
 	config.removeButtons = 'Source,Save,NewPage,Preview,Print,Templates,Cut,Copy,Paste,PasteText,PasteFromWord,Redo,Undo,Find,Replace,SelectAll,Form,Checkbox,Radio,TextField,Textarea,Select,Button,ImageButton,HiddenField,RemoveFormat,Anchor,Unlink,Flash,PageBreak,Iframe,Font,FontSize,TextColor,BGColor,Maximize,ShowBlocks,About,BulletedList,Outdent,Indent,CreateDiv,JustifyBlock,BidiLtr,BidiRtl,Language,Scayt,Smiley'
  config.removeDialogTabs = 'image:Link;image:advanced;table:advanced;link:target;link:advanced';
  config.hideDialogFields="image:info:txtAlt;image:info:txtHeight;image:info:txtWidth;image:info:ratioLock;" +
                          "image:info:txtBorder;image:info:txtHSpace;image:info:txtVSpace;image:info:cmbAlign;image:info:htmlPreview;" +
                          "table:info:selHeaders;table:info:txtCellSpace;table:info:txtBorder;table:info:txtCellPad;table:info:cmbAlign;table:info:txtSummary;table:info:txtHeight;" +
                          "link:info:linkType;link:info:protocol"
  config.specialChars = [ 'α','β','ξ','δ','ε','φ','γ','η','ι','σ','κ','λ','μ','ν','ο','π','θ','ρ','σ','τ','υ','ϝ','ω','χ','ψ','ζ'  ];

  config.extraPlugins = 'mathjax,confighelper'; // put 'mathjax,devtools' if you want to know editor IDs
  config.mathJaxLib = 'http://cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML';

};




CKEDITOR.on( 'dialogDefinition', function( ev ) {
    // Take the dialog name and its definition from the event data.
    var dialogName = ev.data.name;
    var dialogDefinition = ev.data.definition;

    // Set default values
    if ( dialogName == 'table' ) {
        var infoTab = dialogDefinition.getContents( 'info' );
        var field = infoTab.get( 'txtWidth' );
        field[ 'default' ] = '50%';
    }
});
