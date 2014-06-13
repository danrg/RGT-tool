/*
 jPaq - A fully customizable JavaScript/JScript library
 http://jpaq.org/

 Copyright (c) 2011 Christopher West
 Licensed under the MIT license.
 http://jpaq.org/license/

 Version: 1.0.6.0011
 Revised: April 6, 2011
*/
(function(){jPaq={toString:function(){return"jPaq - A fully customizable JavaScript/JScript library created by Christopher West."}};Array.prototype.forEach=Array.prototype.forEach||function(d,c){if(typeof d!="function")throw new TypeError;for(var a=0,e=this.length>>>0;a<e;a++)a in this&&d.call(c,this[a],a,this)};Array.prototype.reduce=Array.prototype.reduce||function(d,c){if(typeof d!="function")throw new TypeError;var a=this.length>>>0,e=arguments.length;if(a==0&&e==1)throw new TypeError;var b=0;
if(e<2){do{if(b in this){c=this[b++];break}if(++b>=a)throw new TypeError;}while(1)}for(;b<a;b++)b in this&&(c=d.call(void 0,c,this[b],b,this));return c}})();