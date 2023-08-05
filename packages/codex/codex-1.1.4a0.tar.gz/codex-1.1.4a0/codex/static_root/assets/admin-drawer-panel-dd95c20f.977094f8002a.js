import{_ as A,m as B,a as T,u as m,b as h,c as v,o as a,d as u,e as p,V as L,f as c,g as n,w as s,h as C,F as I,r as $,i as g,j as l,t as d,k as V,l as S,n as k,p as O,q as P,s as w,v as F,x as M,y as N,z as j,A as x,B as z,C as D,D as f,E}from"./admin-2062d25c.js";const U={name:"AdminStatusList",components:{CloseButton:A},data(){return{mdiCloseCircleOutline:B}},computed:{...T(m,{librarianStatuses:e=>e.librarianStatuses,show:e=>e.librarianStatuses.length>0})},created(){this.load()},methods:{...h(m,["loadTable","librarianTask"]),indeterminate:e=>!e.preactive&&+e.total==0,progress(e){return e.preactive||+e.total==0?0:100*+e.complete/+e.total},load(){this.loadTable("LibrarianStatus")},clear(){this.librarianTask("librarian_clear_status","")}}},q=e=>(O("data-v-24483090"),e=e(),P(),e),G={key:0},R=q(()=>g("h4",null,"Librarian Tasks",-1)),W={nav:"",class:"statusItem"},H={class:"statusItemTitle"},J={key:0};function K(e,r,i,y,_,o){const b=A;return a(),u(I,null,[e.show?(a(),p(L,{key:0})):c("",!0),n(k,{onClick:o.load},{default:s(()=>[n(C,null,{default:s(()=>[e.show?(a(),u("div",G,[n(b,{id:"clearButton",title:"Clear Librarian Statuses",size:"small",onClick:o.clear},null,8,["onClick"]),R,(a(!0),u(I,null,$(e.librarianStatuses,t=>(a(),p(C,{key:`${t.type} ${t.name}`},{default:s(()=>[g("div",W,[g("div",H,[l(d(t.type)+" "+d(t.name)+" ",1),+t.total?(a(),u("span",J,d(t.complete)+"/"+d(t.total),1)):c("",!0)]),n(V,{indeterminate:o.indeterminate(t),"model-value":o.progress(t),bottom:""},null,8,["indeterminate","model-value"])])]),_:2},1024))),128))])):(a(),p(S,{key:1,id:"noTasksRunning"},{default:s(()=>[l(" No librarian tasks running ")]),_:1}))]),_:1})]),_:1},8,["onClick"])],64)}const Q=v(U,[["render",K],["__scopeId","data-v-24483090"]]);const X={name:"AdminMenu",components:{AdminStatusList:Q},props:{menu:{type:Boolean,default:!0}},data(){return{mdiBookAlert:w,mdiOpenInNew:F,mdiDatabaseClockOutline:M,mdiCogOutline:N}},computed:{...j(x,["isUserAdmin"]),...z(m,["unseenFailedImports"])},methods:{...h(m,["clearFailedImports","librarianTask"])}},Y={key:0},Z={key:0};function ee(e,r,i,y,_,o){const b=D("AdminStatusList");return e.isUserAdmin?(a(),u("div",Y,[i.menu?(a(),u("div",Z,[n(k,{onClick:r[0]||(r[0]=t=>e.librarianTask("poll"))},{default:s(()=>[n(S,null,{default:s(()=>[n(f,null,{default:s(()=>[l(d(_.mdiDatabaseClockOutline),1)]),_:1}),l("Poll All Libraries")]),_:1})]),_:1}),n(k,{to:{name:"admin"},onClick:r[1]||(r[1]=t=>e.unseenFailedImports=!1)},{default:s(()=>[n(S,null,{default:s(()=>[n(f,null,{default:s(()=>[l(d(_.mdiCogOutline),1)]),_:1}),l("Admin Panel "),e.unseenFailedImports?(a(),p(f,{key:0,id:"failedImportsIcon",title:"New Failed Imports"},{default:s(()=>[l(d(_.mdiBookAlert),1)]),_:1})):c("",!0)]),_:1})]),_:1})])):c("",!0),n(b)])):c("",!0)}const te=v(X,[["render",ee],["__scopeId","data-v-9516956e"]]),ie=Object.freeze(Object.defineProperty({__proto__:null,default:te},Symbol.toStringTag,{value:"Module"}));const ae={name:"AdminSettingsButtonProgress",computed:{...T(m,["librarianStatuses"]),progressEnabled:function(){return this.librarianStatuses.length>0},progress:function(){let e=0,r=0;if(!(!this.librarianStatuses||this.librarianStatuses.length===0)){for(const i of this.librarianStatuses){if(i.total===null||i.total===void 0||i.complete===void 0)return;e+=+i.complete,r+=+i.total}if(!(r<=0))return 100*e/r}}},created(){this.loadTable("LibrarianStatus")},methods:{...h(m,["loadTable"])}};function ne(e,r,i,y,_,o){return o.progressEnabled?(a(),p(E,{key:0,indeterminate:o.progress==null,"model-value":o.progress,class:"progress",size:"36","aria-label":"`Librarian tasks in progress ${Math.round(progress)}%`"},null,8,["indeterminate","model-value"])):c("",!0)}const se=v(ae,[["render",ne],["__scopeId","data-v-8db54809"]]),oe=Object.freeze(Object.defineProperty({__proto__:null,default:se},Symbol.toStringTag,{value:"Module"}));export{ie as a,oe as b};
