import{c as q,o as _,e as L,ay as Se,r as se,w as R,az as we,aA as X,ar as xe,bg as je,bh as qe,bi as Ye,R as Ue,bj as O,bk as k,af as Z,bl as Ge,bm as He,bn as ge,M as ve,bo as Ke,ae as Me,bp as We,S as me,bq as W,br as Je,g as s,b8 as _e,b9 as Xe,bs as Qe,bb as Ze,bt as et,bu as tt,bv as ye,bw as at,bx as nt,b7 as lt,by as rt,bz as ot,F as fe,bA as st,bB as it,ap as le,I as ut,E as dt,bC as ct,bD as vt,a as ee,L as te,d as P,bE as mt,al as he,f as D,t as z,bF as ft,i as b,bG as ht,bH as pt,v as bt,j as J,D as re,av as gt,p as Te,q as Ve,H as _t,bI as yt,_ as Ie,bJ as kt,bK as Ct,z as St,A as wt,b0 as Mt,bL as Tt,a_ as Vt,a$ as It,bM as Ft,b as ke,J as Nt,aV as Bt,aY as Rt,k as Lt,aw as Pt,C as Dt}from"./admin-2062d25c.js";const $t={name:"PaginationToolbar"};function zt(e,a,l,m,r,i){return _(),L(xe,{class:"paginationToolbar codexToolbar",density:"compact",transform:"center bottom"},Se({_:2},[se(e.$slots,(h,t)=>({name:t,fn:R(o=>[we(e.$slots,t,X({props:h},o),void 0,!0)])}))]),1024)}const tn=q($t,[["render",zt],["__scopeId","data-v-cfa8cce0"]]);const pe=Symbol.for("vuetify:v-slider");function Et(e,a,l){const m=l==="vertical",r=a.getBoundingClientRect(),i="touches"in e?e.touches[0]:e;return m?i.clientY-(r.top+r.height/2):i.clientX-(r.left+r.width/2)}function At(e,a){return"touches"in e&&e.touches.length?e.touches[0][a]:"changedTouches"in e&&e.changedTouches.length?e.changedTouches[0][a]:e[a]}const Ot=je({disabled:Boolean,error:Boolean,readonly:Boolean,max:{type:[Number,String],default:100},min:{type:[Number,String],default:0},step:{type:[Number,String],default:0},thumbColor:String,thumbLabel:{type:[Boolean,String],default:void 0,validator:e=>typeof e=="boolean"||e==="always"},thumbSize:{type:[Number,String],default:20},showTicks:{type:[Boolean,String],default:!1,validator:e=>typeof e=="boolean"||e==="always"},ticks:{type:[Array,Object]},tickSize:{type:[Number,String],default:2},color:String,trackColor:String,trackFillColor:String,trackSize:{type:[Number,String],default:4},direction:{type:String,default:"horizontal",validator:e=>["vertical","horizontal"].includes(e)},reverse:Boolean,...qe(),...Ye({elevation:2})},"slider"),xt=e=>{let{props:a,handleSliderMouseUp:l,handleMouseMove:m,getActiveThumb:r}=e;const{isRtl:i}=Ue(),h=O(a,"reverse"),t=k(()=>{let u=i.value?"rtl":"ltr";return a.reverse&&(u=u==="rtl"?"ltr":"rtl"),u}),o=k(()=>parseFloat(a.min)),n=k(()=>parseFloat(a.max)),c=k(()=>a.step>0?parseFloat(a.step):0),p=k(()=>{const u=c.value.toString().trim();return u.includes(".")?u.length-u.indexOf(".")-1:0}),f=k(()=>parseInt(a.thumbSize,10)),y=k(()=>parseInt(a.tickSize,10)),d=k(()=>parseInt(a.trackSize,10)),v=k(()=>(n.value-o.value)/c.value),g=O(a,"disabled"),w=k(()=>a.direction==="vertical"),I=k(()=>a.error||a.disabled?void 0:a.thumbColor??a.color),C=k(()=>a.error||a.disabled?void 0:a.trackColor??a.color),Y=k(()=>a.error||a.disabled?void 0:a.trackFillColor??a.color),$=Z(!1),M=Z(0),B=Z(),V=Z();function E(u){if(c.value<=0)return u;const T=ge(u,o.value,n.value),K=o.value%c.value,ue=Math.round((T-K)/c.value)*c.value+K;return parseFloat(Math.min(ue,n.value).toFixed(p.value))}function x(u){var T;const K=a.direction==="vertical",ue=K?"top":"left",$e=K?"height":"width",ze=K?"clientY":"clientX",{[ue]:Ee,[$e]:Ae}=(T=B.value)==null?void 0:T.$el.getBoundingClientRect(),Oe=At(u,ze);let de=Math.min(Math.max((Oe-Ee-M.value)/Ae,0),1)||0;return(K||t.value==="rtl")&&(de=1-de),E(o.value+de*(n.value-o.value))}let A=!1;const F=u=>{A||(M.value=0,l(x(u))),$.value=!1,A=!1,M.value=0},Q=u=>{V.value=r(u),V.value&&(V.value.focus(),$.value=!0,V.value.contains(u.target)?(A=!0,M.value=Et(u,V.value,a.direction)):(M.value=0,m(x(u))))},j={passive:!0,capture:!0};function U(u){A=!0,m(x(u))}function S(u){u.stopPropagation(),u.preventDefault(),F(u),window.removeEventListener("mousemove",U,j),window.removeEventListener("mouseup",S)}function N(u){var T;F(u),window.removeEventListener("touchmove",U,j),(T=u.target)==null||T.removeEventListener("touchend",N)}function G(u){var T;Q(u),window.addEventListener("touchmove",U,j),(T=u.target)==null||T.addEventListener("touchend",N,{passive:!1})}function ae(u){u.preventDefault(),Q(u),window.addEventListener("mousemove",U,j),window.addEventListener("mouseup",S,{passive:!1})}const H=u=>{const T=(u-o.value)/(n.value-o.value)*100;return ge(isNaN(T)?0:T,0,100)},ne=k(()=>a.ticks?Array.isArray(a.ticks)?a.ticks.map(u=>({value:u,position:H(u),label:u.toString()})):Object.keys(a.ticks).map(u=>({value:parseFloat(u),position:H(parseFloat(u)),label:a.ticks[u]})):v.value!==1/0?Ge(v.value+1).map(u=>{const T=o.value+u*c.value;return{value:T,position:H(T)}}):[]),ie=k(()=>ne.value.some(u=>{let{label:T}=u;return!!T})),be={activeThumbRef:V,color:O(a,"color"),decimals:p,disabled:g,direction:O(a,"direction"),elevation:O(a,"elevation"),hasLabels:ie,horizontalDirection:t,isReversed:h,min:o,max:n,mousePressed:$,numTicks:v,onSliderMousedown:ae,onSliderTouchstart:G,parsedTicks:ne,parseMouseMove:x,position:H,readonly:O(a,"readonly"),rounded:O(a,"rounded"),roundValue:E,showTicks:O(a,"showTicks"),startOffset:M,step:c,thumbSize:f,thumbColor:I,thumbLabel:O(a,"thumbLabel"),ticks:O(a,"ticks"),tickSize:y,trackColor:C,trackContainerRef:B,trackFillColor:Y,trackSize:d,vertical:w};return He(pe,be),be},jt=ve({name:"VSliderThumb",directives:{Ripple:Ke},props:{focused:Boolean,max:{type:Number,required:!0},min:{type:Number,required:!0},modelValue:{type:Number,required:!0},position:{type:Number,required:!0},ripple:{type:Boolean,default:!0}},emits:{"update:modelValue":e=>!0},setup(e,a){let{slots:l,emit:m}=a;const r=Me(pe);if(!r)throw new Error("[Vuetify] v-slider-thumb must be used inside v-slider or v-range-slider");const{thumbColor:i,step:h,vertical:t,disabled:o,thumbSize:n,thumbLabel:c,direction:p,readonly:f,elevation:y,isReversed:d,horizontalDirection:v,mousePressed:g,decimals:w}=r,{textColorClasses:I,textColorStyles:C}=We(i),{pageup:Y,pagedown:$,end:M,home:B,left:V,right:E,down:x,up:A}=et,F=[Y,$,M,B,V,E,x,A],Q=k(()=>h.value?[1,2,3]:[1,5,10]);function j(S,N){if(!F.includes(S.key))return;S.preventDefault();const G=h.value||.1,ae=(e.max-e.min)/G;if([V,E,x,A].includes(S.key)){const ne=(v.value==="rtl"?[V,A]:[E,A]).includes(S.key)?1:-1,ie=S.shiftKey?2:S.ctrlKey?1:0;N=N+ne*G*Q.value[ie]}else if(S.key===B)N=e.min;else if(S.key===M)N=e.max;else{const H=S.key===$?1:-1;N=N-H*G*(ae>100?ae/10:10)}return Math.max(e.min,Math.min(e.max,N))}function U(S){const N=j(S,e.modelValue);N!=null&&m("update:modelValue",N)}return me(()=>{var S;const N=W(t.value||d.value?100-e.position:e.position,"%"),{elevationClasses:G}=Je(k(()=>o.value?void 0:y.value));return s("div",{class:["v-slider-thumb",{"v-slider-thumb--focused":e.focused,"v-slider-thumb--pressed":e.focused&&g.value}],style:{"--v-slider-thumb-position":N,"--v-slider-thumb-size":W(n.value)},role:"slider",tabindex:o.value?-1:0,"aria-valuemin":e.min,"aria-valuemax":e.max,"aria-valuenow":e.modelValue,"aria-readonly":f.value,"aria-orientation":p.value,onKeydown:f.value?void 0:U},[s("div",{class:["v-slider-thumb__surface",I.value,G.value],style:{...C.value}},null),_e(s("div",{class:["v-slider-thumb__ripple",I.value],style:C.value},null),[[Xe("ripple"),e.ripple,null,{circle:!0,center:!0}]]),s(Qe,{origin:"bottom center"},{default:()=>[_e(s("div",{class:"v-slider-thumb__label-container"},[s("div",{class:["v-slider-thumb__label"]},[s("div",null,[((S=l["thumb-label"])==null?void 0:S.call(l,{modelValue:e.modelValue}))??e.modelValue.toFixed(h.value?w.value:1)])])]),[[Ze,c.value&&e.focused||c.value==="always"]])]})])}),{}}});const qt=ve({name:"VSliderTrack",props:{start:{type:Number,required:!0},stop:{type:Number,required:!0}},emits:{},setup(e,a){let{slots:l}=a;const m=Me(pe);if(!m)throw new Error("[Vuetify] v-slider-track must be inside v-slider or v-range-slider");const{color:r,horizontalDirection:i,parsedTicks:h,rounded:t,showTicks:o,tickSize:n,trackColor:c,trackFillColor:p,trackSize:f,vertical:y,min:d,max:v}=m,{roundedClasses:g}=tt(t),{backgroundColorClasses:w,backgroundColorStyles:I}=ye(p),{backgroundColorClasses:C,backgroundColorStyles:Y}=ye(c),$=k(()=>`inset-${y.value?"block-end":"inline-start"}`),M=k(()=>y.value?"height":"width"),B=k(()=>({[$.value]:"0%",[M.value]:"100%"})),V=k(()=>e.stop-e.start),E=k(()=>({[$.value]:W(e.start,"%"),[M.value]:W(V.value,"%")})),x=k(()=>(y.value?h.value.slice().reverse():h.value).map((F,Q)=>{var j;const U=y.value?"bottom":"margin-inline-start",S=F.value!==d.value&&F.value!==v.value?W(F.position,"%"):void 0;return s("div",{key:F.value,class:["v-slider-track__tick",{"v-slider-track__tick--filled":F.position>=e.start&&F.position<=e.stop,"v-slider-track__tick--first":F.value===d.value,"v-slider-track__tick--last":F.value===v.value}],style:{[U]:S}},[(F.label||l["tick-label"])&&s("div",{class:"v-slider-track__tick-label"},[((j=l["tick-label"])==null?void 0:j.call(l,{tick:F,index:Q}))??F.label])])}));return me(()=>s("div",{class:["v-slider-track",g.value],style:{"--v-slider-track-size":W(f.value),"--v-slider-tick-size":W(n.value),direction:y.value?void 0:i.value}},[s("div",{class:["v-slider-track__background",C.value,{"v-slider-track__background--opacity":!!r.value||!p.value}],style:{...B.value,...Y.value}},null),s("div",{class:["v-slider-track__fill",w.value],style:{...E.value,...I.value}},null),o.value&&s("div",{class:["v-slider-track__ticks",{"v-slider-track__ticks--always-show":o.value==="always"}]},[x.value])])),{}}}),Yt=ve({name:"VSlider",props:{...at(),...Ot(),...nt(),modelValue:{type:[Number,String],default:0}},emits:{"update:focused":e=>!0,"update:modelValue":e=>!0},setup(e,a){let{slots:l}=a;const m=Z(),{min:r,max:i,mousePressed:h,roundValue:t,onSliderMousedown:o,onSliderTouchstart:n,trackContainerRef:c,position:p,hasLabels:f,readonly:y}=xt({props:e,handleSliderMouseUp:C=>d.value=t(C),handleMouseMove:C=>d.value=t(C),getActiveThumb:()=>{var C;return(C=m.value)==null?void 0:C.$el}}),d=lt(e,"modelValue",void 0,C=>{const Y=typeof C=="string"?parseFloat(C):C??r.value;return t(Y)}),{isFocused:v,focus:g,blur:w}=rt(e),I=k(()=>p(d.value));return me(()=>{const[C,Y]=ot(e),$=!!(e.label||l.label||l.prepend);return s(it,X({class:["v-slider",{"v-slider--has-labels":!!l["tick-label"]||f.value,"v-slider--focused":v.value,"v-slider--pressed":h.value,"v-slider--disabled":e.disabled}]},C,{focused:v.value}),{...l,prepend:$?M=>{var B,V;return s(fe,null,[((B=l.label)==null?void 0:B.call(l,M))??e.label?s(st,{id:M.id,class:"v-slider__label",text:e.label},null):void 0,(V=l.prepend)==null?void 0:V.call(l,M)])}:void 0,default:M=>{let{id:B,messagesId:V}=M;return s("div",{class:"v-slider__container",onMousedown:y.value?void 0:o,onTouchstartPassive:y.value?void 0:n},[s("input",{id:B.value,name:e.name||B.value,disabled:e.disabled,readonly:e.readonly,tabindex:"-1",value:d.value},null),s(qt,{ref:c,start:0,stop:I.value},{"tick-label":l["tick-label"]}),s(jt,{ref:m,"aria-describedby":V.value,focused:v.value,min:r.value,max:i.value,modelValue:d.value,"onUpdate:modelValue":E=>d.value=E,position:I.value,elevation:e.elevation,onFocus:g,onBlur:w},{"thumb-label":l["thumb-label"]})])}})}),{}}}),Ut={name:"PaginationSlider"};function Gt(e,a,l,m,r,i){return _(),L(Yt,X({"thumb-size":"36",class:"paginationSlider",density:"compact","hide-details":"auto",rounded:!0,"show-ticks":"always",step:1,"thumb-label":"always"},e.$attrs),null,16)}const an=q(Ut,[["render",Gt],["__scopeId","data-v-825b160e"]]);const Ht={name:"PaginationNavButton"};function Kt(e,a,l,m,r,i){return _(),L(le,X({class:"paginationNavButton",height:"100%"},e.$attrs),Se({_:2},[se(e.$slots,(h,t)=>({name:t,fn:R(o=>[we(e.$slots,t,X({props:h},o),void 0,!0)])}))]),1040)}const nn=q(Ht,[["render",Kt],["__scopeId","data-v-852fad11"]]),Fe=ut.browser.vuetifyNullCode,Ne="None",Wt={value:Fe,title:Ne},Jt=function(e,a){let l;return e===void 0?l=e:e instanceof Object?(l={value:e.pk,title:e.name},e.pk===null||e.name===void 0?l.value=Fe:a||(l.value=+e.pk),(l.title===null||l.value===void 0)&&(l.title=Ne)):e===null?l=Wt:l={value:e,title:e.toString()},l},Xt=function(e,a){return e.title<a.title?-1:e.title>a.title?1:0},Qt=function(e,a){return Number.parseFloat(e.title)-Number.parseFloat(a.title)},Zt=function(e,a,l=!1,m=!1){const r=e||[],i=a&&a.toLowerCase();let h=[];for(const o of r){const n=Jt(o,m);n&&(!i||n.title&&n.title.toLowerCase().includes(i))&&h.push(n)}const t=l?Qt:Xt;return h.sort(t)};const ea={name:"PlaceholderLoading",props:{indeterminate:{type:Boolean,default:!0}}};function ta(e,a,l,m,r,i){return _(),L(dt,X({"aria-label":"loading",class:"codexProgressCircular",indeterminate:l.indeterminate},e.$attrs),null,16,["indeterminate"])}const Be=q(ea,[["render",ta],["__scopeId","data-v-7bb4cf22"]]);var oe={},aa={get exports(){return oe},set exports(e){oe=e}};(function(e,a){(function(){var l=this,m=l.humanize,r={};e.exports&&(a=e.exports=r),a.humanize=r,r.noConflict=function(){return l.humanize=m,this},r.pad=function(t,o,n,c){if(t+="",n?n.length>1&&(n=n.charAt(0)):n=" ",c=c===void 0?"left":"right",c==="right")for(;t.length<o;)t=t+n;else for(;t.length<o;)t=n+t;return t},r.time=function(){return new Date().getTime()/1e3};var i=[0,0,31,59,90,120,151,181,212,243,273,304,334],h=[0,0,31,60,91,121,152,182,213,244,274,305,335];r.date=function(t,o){var n=o===void 0?new Date:o instanceof Date?new Date(o):new Date(o*1e3),c=/\\?([a-z])/gi,p=function(v,g){return d[v]?d[v]():g},f=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],y=["January","February","March","April","May","June","July","August","September","October","November","December"],d={d:function(){return r.pad(d.j(),2,"0")},D:function(){return d.l().slice(0,3)},j:function(){return n.getDate()},l:function(){return f[d.w()]},N:function(){return d.w()||7},S:function(){var v=d.j();return v>4&&v<21?"th":{1:"st",2:"nd",3:"rd"}[v%10]||"th"},w:function(){return n.getDay()},z:function(){return(d.L()?h[d.n()]:i[d.n()])+d.j()-1},W:function(){var v=d.z()-d.N()+1.5;return r.pad(1+Math.floor(Math.abs(v)/7)+(v%7>3.5?1:0),2,"0")},F:function(){return y[n.getMonth()]},m:function(){return r.pad(d.n(),2,"0")},M:function(){return d.F().slice(0,3)},n:function(){return n.getMonth()+1},t:function(){return new Date(d.Y(),d.n(),0).getDate()},L:function(){return new Date(d.Y(),1,29).getMonth()===1?1:0},o:function(){var v=d.n(),g=d.W();return d.Y()+(v===12&&g<9?-1:v===1&&g>9)},Y:function(){return n.getFullYear()},y:function(){return String(d.Y()).slice(-2)},a:function(){return n.getHours()>11?"pm":"am"},A:function(){return d.a().toUpperCase()},B:function(){var v=n.getTime()/1e3,g=v%86400+3600;g<0&&(g+=86400);var w=g/86.4%1e3;return v<0?Math.ceil(w):Math.floor(w)},g:function(){return d.G()%12||12},G:function(){return n.getHours()},h:function(){return r.pad(d.g(),2,"0")},H:function(){return r.pad(d.G(),2,"0")},i:function(){return r.pad(n.getMinutes(),2,"0")},s:function(){return r.pad(n.getSeconds(),2,"0")},u:function(){return r.pad(n.getMilliseconds()*1e3,6,"0")},O:function(){var v=n.getTimezoneOffset(),g=Math.abs(v);return(v>0?"-":"+")+r.pad(Math.floor(g/60)*100+g%60,4,"0")},P:function(){var v=d.O();return v.substr(0,3)+":"+v.substr(3,2)},Z:function(){return-n.getTimezoneOffset()*60},c:function(){return"Y-m-d\\TH:i:sP".replace(c,p)},r:function(){return"D, d M Y H:i:s O".replace(c,p)},U:function(){return n.getTime()/1e3||0}};return t.replace(c,p)},r.numberFormat=function(t,o,n,c){o=isNaN(o)?2:Math.abs(o),n=n===void 0?".":n,c=c===void 0?",":c;var p=t<0?"-":"";t=Math.abs(+t||0);var f=parseInt(t.toFixed(o),10)+"",y=f.length>3?f.length%3:0;return p+(y?f.substr(0,y)+c:"")+f.substr(y).replace(/(\d{3})(?=\d)/g,"$1"+c)+(o?n+Math.abs(t-f).toFixed(o).slice(2):"")},r.naturalDay=function(t,o){t=t===void 0?r.time():t,o=o===void 0?"Y-m-d":o;var n=86400,c=new Date,p=new Date(c.getFullYear(),c.getMonth(),c.getDate()).getTime()/1e3;return t<p&&t>=p-n?"yesterday":t>=p&&t<p+n?"today":t>=p+n&&t<p+2*n?"tomorrow":r.date(o,t)},r.relativeTime=function(t){t=t===void 0?r.time():t;var o=r.time(),n=o-t;if(n<2&&n>-2)return(n>=0?"just ":"")+"now";if(n<60&&n>-60)return n>=0?Math.floor(n)+" seconds ago":"in "+Math.floor(-n)+" seconds";if(n<120&&n>-120)return n>=0?"about a minute ago":"in about a minute";if(n<3600&&n>-3600)return n>=0?Math.floor(n/60)+" minutes ago":"in "+Math.floor(-n/60)+" minutes";if(n<7200&&n>-7200)return n>=0?"about an hour ago":"in about an hour";if(n<86400&&n>-86400)return n>=0?Math.floor(n/3600)+" hours ago":"in "+Math.floor(-n/3600)+" hours";var c=2*86400;if(n<c&&n>-c)return n>=0?"1 day ago":"in 1 day";var p=29*86400;if(n<p&&n>-p)return n>=0?Math.floor(n/86400)+" days ago":"in "+Math.floor(-n/86400)+" days";var f=60*86400;if(n<f&&n>-f)return n>=0?"about a month ago":"in about a month";var y=parseInt(r.date("Y",o),10),d=parseInt(r.date("Y",t),10),v=y*12+parseInt(r.date("n",o),10),g=d*12+parseInt(r.date("n",t),10),w=v-g;if(w<12&&w>-12)return w>=0?w+" months ago":"in "+-w+" months";var I=y-d;return I<2&&I>-2?I>=0?"a year ago":"in a year":I>=0?I+" years ago":"in "+-I+" years"},r.ordinal=function(t){t=parseInt(t,10),t=isNaN(t)?0:t;var o=t<0?"-":"";t=Math.abs(t);var n=t%100;return o+t+(n>4&&n<21?"th":{1:"st",2:"nd",3:"rd"}[t%10]||"th")},r.filesize=function(t,o,n,c,p,f){return o=o===void 0?1024:o,t<=0?"0 bytes":(t<o&&n===void 0&&(n=0),f===void 0&&(f=" "),r.intword(t,["bytes","KB","MB","GB","TB","PB"],o,n,c,p,f))},r.intword=function(t,o,n,c,p,f,y){var d,v;o=o||["","K","M","B","T"],v=o.length-1,n=n||1e3,c=isNaN(c)?2:Math.abs(c),p=p||".",f=f||",",y=y||"";for(var g=0;g<o.length;g++)if(t<Math.pow(n,g+1)){v=g;break}d=t/Math.pow(n,v);var w=o[v]?y+o[v]:"";return r.numberFormat(d,c,p,f)+w},r.linebreaks=function(t){return t=t.replace(/^([\n|\r]*)/,""),t=t.replace(/([\n|\r]*)$/,""),t=t.replace(/(\r\n|\n|\r)/g,`
`),t=t.replace(/(\n{2,})/g,"</p><p>"),t=t.replace(/\n/g,"<br />"),"<p>"+t+"</p>"},r.nl2br=function(t){return t.replace(/(\r\n|\n|\r)/g,"<br />")},r.truncatechars=function(t,o){return t.length<=o?t:t.substr(0,o)+"…"},r.truncatewords=function(t,o){var n=t.split(" ");return n.length<o?t:n.slice(0,o).join(" ")+"…"}}).call(ct)})(aa,oe);const ce=oe,na=(e,a)=>e?`${vt(e)}/cover.webp?${a}`:window.CODEX.MISSING_COVER;const la={name:"BookCover",props:{group:{type:String,required:!0},childCount:{type:Number,default:1},finished:{type:Boolean},coverPk:{type:Number,required:!0}},data(){return{showPlaceholder:!1}},computed:{...ee(te,{coverSrc:function(e){return na(this.coverPk,e.page.coversTimestamp)}})},mounted:function(){this.delayPlaceholder()},methods:{delayPlaceholder:function(){setTimeout(()=>{this.showPlaceholder=!0},2e3)}}},ra={class:"bookCover"},oa={key:1,class:"childCount"};function sa(e,a,l,m,r,i){return _(),P("div",ra,[s(mt,{src:e.coverSrc,class:"coverImg"},null,8,["src"]),l.finished!==!0?(_(),P("div",{key:0,class:he({unreadFlag:!0,mixedreadFlag:l.finished===null})},null,2)):D("",!0),l.group!=="c"?(_(),P("span",oa,z(l.childCount),1)):D("",!0)])}const Re=q(la,[["render",sa],["__scopeId","data-v-9acb5f6a"]]);const ia={name:"MetadataTags",props:{label:{type:String,required:!0},items:{type:Array,default(){return[]}},values:{type:Array,default(){return[]}}},data(){return{mdiFilter:ft}},computed:{...ee(te,{filterValues:function(e){return e.settings.filters[this.label.toLowerCase()]}}),model(){return Zt(this.values)}},methods:{chipColor:function(e){return this.filterValues&&this.filterValues.includes(e)?this.$vuetify.theme.current.colors["primary-darken-1"]:""}}},ua={key:0,class:"tags"},da={class:"label"};function ca(e,a,l,m,r,i){return i.model&&i.model.length>0?(_(),P("div",ua,[s(pt,{value:i.model,multiple:"",class:"chipGroup"},{default:R(()=>[b("div",da,z(l.label),1),(_(!0),P(fe,null,se(i.model,h=>(_(),L(ht,{key:`${l.label}/${h.value}`,color:i.chipColor(h.value),value:h.value,text:h.title},null,8,["color","value","text"]))),128))]),_:1},8,["value"])])):D("",!0)}const Le=q(ia,[["render",ca],["__scopeId","data-v-80903885"]]);const va={name:"MetadataTextBox",props:{label:{type:String,required:!0},value:{type:[Object,String,Number,Boolean],default:void 0},link:{type:Boolean,default:!1},highlight:{type:Boolean,default:!1}},data(){return{mdiOpenInNew:bt}},computed:{computedValue:function(){return this.value!=null&&this.value instanceof Object?this.value.name:this.value}}},ma={class:"textLabel"},fa=["href"],ha={key:1,class:"textContent"};function pa(e,a,l,m,r,i){return i.computedValue?(_(),P("div",{key:0,class:he(["text",{highlight:l.highlight}])},[b("div",ma,z(l.label),1),l.link?(_(),P("a",{key:0,href:i.computedValue,target:"_blank"},[J(z(i.computedValue)+" ",1),s(re,{size:"small"},{default:R(()=>[J(z(r.mdiOpenInNew),1)]),_:1})],8,fa)):(_(),P("div",ha,z(i.computedValue),1))],2)):D("",!0)}const Pe=q(va,[["render",pa],["__scopeId","data-v-48a2f357"]]);const ba={name:"MetadataCreditsTable",props:{value:{type:Array,default:void 0}},data(){return{}},computed:{sortedCredits:function(){return this.value?[...this.value].sort(this.creditsCompare):[]},...ee(te,{filteredCreators(e){return e.settings.filters.creators}})},methods:{roleName:function(e){return e==="CoverArtist"?"Cover Artist":e},creditSortable:function(e){const a=e.person.name.split(" ");let l=[];return a&&(l.push(a.slice(-1)),a.length>1&&l.push(a.slice(0,-1))),l.push(e.role.name),l.join(" ")},creditsCompare:function(e,a){const l=this.creditSortable(e),m=this.creditSortable(a);return l<m?-1:l>m?1:0},isFilteredCreator(e){return this.filteredCreators&&this.filteredCreators.includes(e)}}},De=e=>(Te("data-v-d709751f"),e=e(),Ve(),e),ga=De(()=>b("h2",null,"Credits",-1)),_a={class:"highlight-table"},ya=De(()=>b("thead",null,[b("tr",null,[b("th",{class:"text-left"},"Role"),b("th",{class:"text-left"},"Creator")])],-1)),ka={class:"highlight"};function Ca(e,a,l,m,r,i){return i.sortedCredits&&i.sortedCredits.length>0?(_(),L(gt,{key:0,id:"creditsTable"},{default:R(()=>[ga,b("table",_a,[ya,b("tbody",null,[(_(!0),P(fe,null,se(i.sortedCredits,h=>(_(),P("tr",{key:h.pk},[b("td",null,z(i.roleName(h.role.name)),1),b("td",{class:he({filteredOn:i.isFilteredCreator(h.person.pk)})},[b("span",ka,z(h.person.name),1)],2)]))),128))])])]),_:1})):D("",!0)}const Sa=q(ba,[["render",Ca],["__scopeId","data-v-d709751f"]]),wa=({pk:e,page:a,readLtr:l,pageCount:m})=>{if(m){if(a)a=Number(a);else if(l)a=0;else{const r=Number(m)-1;a=Math.max(r,0)}return{name:"reader",params:{pk:e,page:a}}}},Ce=_t("metadata",{state:()=>({md:void 0}),actions:{async loadMetadata({group:e,pk:a}){const l=te();await yt.getMetadata({group:e,pk:a},l.settings).then(m=>(this.md=m.data,!0)).catch(m=>{console.error(m),this.clearMetadata()})},clearMetadata(){this.md=void 0}}});const Ma=1160,Ta=.05,Va=250,Ia={comic:"Comic Archive",pdf:"PDF"},Fa={name:"MetadataButton",components:{BookCover:Re,CloseButton:Ie,MetadataCreditsTable:Sa,MetadataTags:Le,MetadataText:Pe,PlaceholderLoading:Be},props:{group:{type:String,required:!0},pk:{type:Number,required:!0},children:{type:Number,default:1}},data(){return{mdiDownload:kt,mdiTagOutline:Ct,dialog:!1,progress:0}},computed:{...St(wt,["isUserAdmin"]),...ee(Ce,{md:e=>e.md,downloadFileName:e=>{const a=e.md;return e.md.path?a.path.split("/").at(-1):Mt({seriesName:a.series.name,volumeName:a.volume.name,issue:a.issue,issueSuffix:a.issueSuffix})+".cbz"}}),...ee(te,{q:e=>e.settings.q}),downloadURL:function(){return Tt(this.pk)},isReadButtonShown:function(){return this.group==="c"&&this.$route.name!="reader"},isReadButtonEnabled:function(){return this.$route.name==="browser"&&Boolean(this.readerRoute)},readButtonIcon:function(){return this.isReadButtonEnabled?Vt:It},readerRoute:function(){return wa(this.md)},formattedIssue:function(){if(!((this.md.issue===null||this.md.issue===void 0)&&!this.md.issueSuffix))return Ft({issue:this.md.issue,issueSuffix:this.md.issueSuffix})},ltrText:function(){return this.md.readLtr?"Left to Right":"Right to Left"},pages:function(){let e="";if(this.md.page){const l=ce.numberFormat(this.md.page,0);e+=`Read ${l} of `}const a=ce.numberFormat(this.md.pageCount,0);return e+=`${a} pages`,this.md.progress>0&&(e+=` (${Math.round(this.md.progress)}%)`),e},size:function(){return ce.filesize(this.md.size)},fileFormat:function(){return Ia[this.md.fileFormat]||this.md.fileFormat}},watch:{dialog:function(e){e?this.dialogOpened():this.clearMetadata()}},mounted(){window.addEventListener("keyup",this._keyListener)},unmounted(){window.removeEventListener("keyup",this._keyListener)},methods:{...ke(Ce,["clearMetadata","loadMetadata"]),...ke(Nt,["downloadIOSPWAFix"]),dialogOpened:function(){this.loadMetadata({group:this.group,pk:this.pk}),this.startProgress()},startProgress:function(){this.startTime=Date.now(),this.estimatedMS=Math.max(Ta,this.children/Ma)*1e3,this.updateProgress()},updateProgress:function(){const e=Date.now()-this.startTime;this.progress=e/this.estimatedMS*100,!(this.progress>=100||this.md)&&setTimeout(()=>{this.updateProgress()},Va)},formatDateTime:function(e){const a=new Date(e);return Bt.format(a).replace(",","")},download(){this.downloadIOSPWAFix(this.downloadURL,this.downloadFileName)},_keyListener(e){e.stopImmediatePropagation(),e.key==="Escape"&&(this.dialog=!1)}}},Na=e=>(Te("data-v-fdc382c4"),e=e(),Ve(),e),Ba={key:0,id:"metadataContainer"},Ra={id:"metadataHeader"},La={id:"metadataBookCoverWrapper"},Pa={class:"headerHalfRow"},Da={class:"headerQuarterRow"},$a={class:"mdSection"},za={key:0,class:"inlineRow"},Ea={id:"metadataBody"},Aa={class:"mdSection"},Oa={class:"thirdRow"},xa={class:"mdSection"},ja={class:"quarterRow"},qa={class:"lastSmallRow"},Ya={class:"halfRow mdSection"},Ua={class:"mdSection"},Ga={class:"mdSection"},Ha={class:"mdSection"},Ka={class:"mdSection"},Wa={id:"footerLinks"},Ja={id:"bottomRightButtons"},Xa={key:1,id:"placeholderContainer"},Qa=Na(()=>b("div",{id:"placeholderTitle"},"Tags Loading",-1));function Za(e,a,l,m,r,i){const h=Ie,t=Pe,o=Re,n=Le,c=Dt("MetadataCreditsTable"),p=Be;return _(),L(Pt,{modelValue:r.dialog,"onUpdate:modelValue":a[4]||(a[4]=f=>r.dialog=f),fullscreen:"",transition:"dialog-bottom-transition"},{activator:R(({props:f})=>[s(le,X({"aria-label":"tags",class:"tagButton cardControlButton",icon:"",title:"Tags",variant:"text"},f,{onClick:a[0]||(a[0]=Rt(()=>{},["prevent"]))}),{default:R(()=>[s(re,null,{default:R(()=>[J(z(r.mdiTagOutline),1)]),_:1})]),_:2},1040)]),default:R(()=>[e.md?(_(),P("div",Ba,[b("header",Ra,[s(h,{class:"closeButton",title:"Close Metadata (esc)",size:"x-large",onClick:a[1]||(a[1]=f=>r.dialog=!1)}),e.q?(_(),L(t,{key:0,id:"search",value:e.q,label:"Search Query",highlight:!0},null,8,["value"])):D("",!0),b("div",La,[s(o,{id:"bookCover","cover-pk":e.md.coverPk,group:l.group,"child-count":e.md.childCount,finished:e.md.finished},null,8,["cover-pk","group","child-count","finished"]),s(Lt,{class:"bookCoverProgress","model-value":e.md.progress,rounded:"","background-color":"inherit",height:"2","aria-label":"% read"},null,8,["model-value"])]),b("div",Pa,[s(t,{id:"publisher",value:e.md.publisher,label:"Publisher",highlight:e.md.group==="p"},null,8,["value","highlight"]),s(t,{id:"imprint",value:e.md.imprint,label:"Imprint",highlight:e.md.group==="i"},null,8,["value","highlight"])]),s(t,{id:"series",value:e.md.series,label:"Series",highlight:e.md.group==="s"},null,8,["value","highlight"]),b("div",Da,[s(t,{id:"volume",value:e.md.volume,label:"Volume",highlight:e.md.group==="v"},null,8,["value","highlight"]),s(t,{value:e.md.volumeCount,label:"Volume Count"},null,8,["value"]),s(t,{id:"issue",value:i.formattedIssue,label:"Issue",highlight:e.md.group==="c"},null,8,["value","highlight"]),s(t,{value:e.md.issueCount,label:"Issue Count"},null,8,["value"])]),b("section",$a,[s(t,{value:e.md.name,label:"Title"},null,8,["value"]),e.md.year||e.md.month||e.md.day?(_(),P("div",za,[s(t,{value:e.md.year,label:"Year",class:"datePicker",type:"number"},null,8,["value"]),s(t,{value:e.md.month,label:"Month",class:"datePicker"},null,8,["value"]),s(t,{value:e.md.day,label:"Day",class:"datePicker"},null,8,["value"])])):D("",!0),s(t,{value:e.md.format,label:"Format"},null,8,["value"])])]),b("div",Ea,[b("section",Aa,[b("div",Oa,[s(t,{value:i.pages,label:"Pages"},null,8,["value"]),s(t,{value:e.md.finished,label:"Finished"},null,8,["value"]),s(t,{value:i.ltrText,label:"Reading Direction"},null,8,["value"])])]),b("section",xa,[b("div",ja,[e.md.createdAt?(_(),L(t,{key:0,value:i.formatDateTime(e.md.createdAt),label:"Created at",class:"mtime"},null,8,["value"])):D("",!0),e.md.updatedAt?(_(),L(t,{key:1,value:i.formatDateTime(e.md.updatedAt),label:"Updated at",class:"mtime"},null,8,["value"])):D("",!0),s(t,{value:i.size,label:"Size"},null,8,["value"]),s(t,{value:i.fileFormat,label:"File Type"},null,8,["value"])]),b("div",qa,[s(t,{value:e.md.path,label:"Path"},null,8,["value"])])]),b("section",Ya,[s(t,{value:e.md.country,label:"Country"},null,8,["value"]),s(t,{value:e.md.language,label:"Language"},null,8,["value"])]),b("section",Ua,[s(t,{value:e.md.communityRating,label:"Community Rating"},null,8,["value"]),s(t,{value:e.md.criticalRating,label:"Critical Rating"},null,8,["value"]),s(t,{value:e.md.ageRating,label:"Age Rating"},null,8,["value"])]),b("section",Ga,[s(n,{values:e.md.genres,label:"Genres"},null,8,["values"]),s(n,{values:e.md.tags,label:"Tags"},null,8,["values"]),s(n,{values:e.md.teams,label:"Teams"},null,8,["values"]),s(n,{values:e.md.characters,label:"Characters"},null,8,["values"]),s(n,{values:e.md.locations,label:"Locations"},null,8,["values"]),s(n,{values:e.md.storyArcs,label:"Story Arcs"},null,8,["values"]),s(n,{values:e.md.seriesGroups,label:"Series Groups"},null,8,["values"])]),b("section",Ha,[s(t,{value:e.md.web,label:"Web Link",link:!0},null,8,["value"]),s(t,{value:e.md.summary,label:"Summary"},null,8,["value"]),s(t,{value:e.md.comments,label:"Comments"},null,8,["value"]),s(t,{value:e.md.notes,label:"Notes"},null,8,["value"]),s(t,{value:e.md.scanInfo,label:"Scan"},null,8,["value"])]),b("section",Ka,[s(c,{value:e.md.credits},null,8,["value"])])]),b("footer",Wa,[l.group==="c"?(_(),L(le,{key:0,id:"downloadButton",title:"Download Comic Archive",onClick:i.download},{default:R(()=>[l.group==="c"?(_(),L(re,{key:0},{default:R(()=>[J(z(r.mdiDownload),1)]),_:1})):D("",!0),J(" Download ")]),_:1},8,["onClick"])):D("",!0),i.isReadButtonShown?(_(),L(le,{key:1,to:i.readerRoute,title:"Read Comic",disabled:!i.isReadButtonEnabled},{default:R(()=>[s(re,null,{default:R(()=>[J(z(i.readButtonIcon),1)]),_:1}),J(" Read ")]),_:1},8,["to","disabled"])):D("",!0),b("span",Ja,[s(h,{class:"closeButton",title:"Close Metadata (esc)",size:"x-large",onClick:a[2]||(a[2]=f=>r.dialog=!1)})])])])):(_(),P("div",Xa,[s(h,{class:"closeButton",title:"Close Metadata (esc)",onClick:a[3]||(a[3]=f=>r.dialog=!1)}),Qa,s(p,{"model-value":r.progress,indeterminate:r.progress>=100,class:"placeholder"},null,8,["model-value","indeterminate"])]))]),_:1},8,["modelValue"])}const ln=q(Fa,[["render",Za],["__scopeId","data-v-fdc382c4"]]);export{Be as P,nn as _,an as a,tn as b,ln as c,Re as d,wa as g,ce as h,Zt as t};
