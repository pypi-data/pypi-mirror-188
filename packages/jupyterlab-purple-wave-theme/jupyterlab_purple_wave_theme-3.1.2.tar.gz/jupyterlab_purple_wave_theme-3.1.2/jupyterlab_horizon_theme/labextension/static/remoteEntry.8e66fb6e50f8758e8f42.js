var _JUPYTERLAB;(()=>{"use strict";var e,r,t,n,o,a,i,u,l,f,s,p,d,c,h,v={180:(e,r,t)=>{var n={"./index":()=>t.e(568).then((()=>()=>t(568))),"./extension":()=>t.e(568).then((()=>()=>t(568)))},o=(e,r)=>(t.R=r,r=t.o(n,e)?n[e]():Promise.resolve().then((()=>{throw new Error('Module "'+e+'" does not exist in container.')})),t.R=void 0,r),a=(e,r)=>{if(t.S){var n="default",o=t.S[n];if(o&&o!==e)throw new Error("Container initialization failed as it has already been initialized with a different share scope");return t.S[n]=e,t.I(n,r)}};t.d(r,{get:()=>o,init:()=>a})}},m={};function g(e){var r=m[e];if(void 0!==r)return r.exports;var t=m[e]={exports:{}};return v[e](t,t.exports,g),t.exports}g.m=v,g.c=m,g.n=e=>{var r=e&&e.__esModule?()=>e.default:()=>e;return g.d(r,{a:r}),r},g.d=(e,r)=>{for(var t in r)g.o(r,t)&&!g.o(e,t)&&Object.defineProperty(e,t,{enumerable:!0,get:r[t]})},g.f={},g.e=e=>Promise.all(Object.keys(g.f).reduce(((r,t)=>(g.f[t](e,r),r)),[])),g.u=e=>e+".9f0e86c070817b9e94e0.js?v=9f0e86c070817b9e94e0",g.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),g.o=(e,r)=>Object.prototype.hasOwnProperty.call(e,r),e={},r="@arnos-stuff/jupyterlab-purple-wave-theme:",g.l=(t,n,o,a)=>{if(e[t])e[t].push(n);else{var i,u;if(void 0!==o)for(var l=document.getElementsByTagName("script"),f=0;f<l.length;f++){var s=l[f];if(s.getAttribute("src")==t||s.getAttribute("data-webpack")==r+o){i=s;break}}i||(u=!0,(i=document.createElement("script")).charset="utf-8",i.timeout=120,g.nc&&i.setAttribute("nonce",g.nc),i.setAttribute("data-webpack",r+o),i.src=t),e[t]=[n];var p=(r,n)=>{i.onerror=i.onload=null,clearTimeout(d);var o=e[t];if(delete e[t],i.parentNode&&i.parentNode.removeChild(i),o&&o.forEach((e=>e(n))),r)return r(n)},d=setTimeout(p.bind(null,void 0,{type:"timeout",target:i}),12e4);i.onerror=p.bind(null,i.onerror),i.onload=p.bind(null,i.onload),u&&document.head.appendChild(i)}},g.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},(()=>{g.S={};var e={},r={};g.I=(t,n)=>{n||(n=[]);var o=r[t];if(o||(o=r[t]={}),!(n.indexOf(o)>=0)){if(n.push(o),e[t])return e[t];g.o(g.S,t)||(g.S[t]={});var a=g.S[t],i="@arnos-stuff/jupyterlab-purple-wave-theme",u=[];return"default"===t&&((e,r,t,n)=>{var o=a[e]=a[e]||{},u=o[r];(!u||!u.loaded&&(1!=!u.eager?n:i>u.from))&&(o[r]={get:()=>g.e(568).then((()=>()=>g(568))),from:i,eager:!1})})("@arnos-stuff/jupyterlab-purple-wave-theme","3.1.2"),e[t]=u.length?Promise.all(u).then((()=>e[t]=1)):1}}})(),(()=>{var e;g.g.importScripts&&(e=g.g.location+"");var r=g.g.document;if(!e&&r&&(r.currentScript&&(e=r.currentScript.src),!e)){var t=r.getElementsByTagName("script");t.length&&(e=t[t.length-1].src)}if(!e)throw new Error("Automatic publicPath is not supported in this browser");e=e.replace(/#.*$/,"").replace(/\?.*$/,"").replace(/\/[^\/]+$/,"/"),g.p=e})(),t=e=>{var r=e=>e.split(".").map((e=>+e==e?+e:e)),t=/^([^-+]+)?(?:-([^+]+))?(?:\+(.+))?$/.exec(e),n=t[1]?r(t[1]):[];return t[2]&&(n.length++,n.push.apply(n,r(t[2]))),t[3]&&(n.push([]),n.push.apply(n,r(t[3]))),n},n=(e,r)=>{e=t(e),r=t(r);for(var n=0;;){if(n>=e.length)return n<r.length&&"u"!=(typeof r[n])[0];var o=e[n],a=(typeof o)[0];if(n>=r.length)return"u"==a;var i=r[n],u=(typeof i)[0];if(a!=u)return"o"==a&&"n"==u||"s"==u||"u"==a;if("o"!=a&&"u"!=a&&o!=i)return o<i;n++}},o=e=>{var r=e[0],t="";if(1===e.length)return"*";if(r+.5){t+=0==r?">=":-1==r?"<":1==r?"^":2==r?"~":r>0?"=":"!=";for(var n=1,a=1;a<e.length;a++)n--,t+="u"==(typeof(u=e[a]))[0]?"-":(n>0?".":"")+(n=2,u);return t}var i=[];for(a=1;a<e.length;a++){var u=e[a];i.push(0===u?"not("+l()+")":1===u?"("+l()+" || "+l()+")":2===u?i.pop()+" "+i.pop():o(u))}return l();function l(){return i.pop().replace(/^\((.+)\)$/,"$1")}},a=(e,r)=>{if(0 in e){r=t(r);var n=e[0],o=n<0;o&&(n=-n-1);for(var i=0,u=1,l=!0;;u++,i++){var f,s,p=u<e.length?(typeof e[u])[0]:"";if(i>=r.length||"o"==(s=(typeof(f=r[i]))[0]))return!l||("u"==p?u>n&&!o:""==p!=o);if("u"==s){if(!l||"u"!=p)return!1}else if(l)if(p==s)if(u<=n){if(f!=e[u])return!1}else{if(o?f>e[u]:f<e[u])return!1;f!=e[u]&&(l=!1)}else if("s"!=p&&"n"!=p){if(o||u<=n)return!1;l=!1,u--}else{if(u<=n||s<p!=o)return!1;l=!1}else"s"!=p&&"n"!=p&&(l=!1,u--)}}var d=[],c=d.pop.bind(d);for(i=1;i<e.length;i++){var h=e[i];d.push(1==h?c()|c():2==h?c()&c():h?a(h,r):!c())}return!!c()},i=(e,r)=>{var t=g.S[e];if(!t||!g.o(t,r))throw new Error("Shared module "+r+" doesn't exist in shared scope "+e);return t},u=(e,r)=>{var t=e[r];return Object.keys(t).reduce(((e,r)=>!e||!t[e].loaded&&n(e,r)?r:e),0)},l=(e,r,t,n)=>"Unsatisfied version "+t+" from "+(t&&e[r][t].from)+" of shared singleton module "+r+" (required "+o(n)+")",f=(e,r,t,n)=>{var o=u(e,t);return a(n,o)||"undefined"!=typeof console&&console.warn&&console.warn(l(e,t,o,n)),s(e[t][o])},s=e=>(e.loaded=1,e.get()),p=(e=>function(r,t,n,o){var a=g.I(r);return a&&a.then?a.then(e.bind(e,r,g.S[r],t,n,o)):e(r,g.S[r],t,n)})(((e,r,t,n)=>(i(e,t),f(r,0,t,n)))),d={},c={859:()=>p("default","@jupyterlab/apputils",[1,3,5,3])},h={568:[859]},g.f.consumes=(e,r)=>{g.o(h,e)&&h[e].forEach((e=>{if(g.o(d,e))return r.push(d[e]);var t=r=>{d[e]=0,g.m[e]=t=>{delete g.c[e],t.exports=r()}},n=r=>{delete d[e],g.m[e]=t=>{throw delete g.c[e],r}};try{var o=c[e]();o.then?r.push(d[e]=o.then(t).catch(n)):t(o)}catch(e){n(e)}}))},(()=>{var e={882:0};g.f.j=(r,t)=>{var n=g.o(e,r)?e[r]:void 0;if(0!==n)if(n)t.push(n[2]);else{var o=new Promise(((t,o)=>n=e[r]=[t,o]));t.push(n[2]=o);var a=g.p+g.u(r),i=new Error;g.l(a,(t=>{if(g.o(e,r)&&(0!==(n=e[r])&&(e[r]=void 0),n)){var o=t&&("load"===t.type?"missing":t.type),a=t&&t.target&&t.target.src;i.message="Loading chunk "+r+" failed.\n("+o+": "+a+")",i.name="ChunkLoadError",i.type=o,i.request=a,n[1](i)}}),"chunk-"+r,r)}};var r=(r,t)=>{var n,o,[a,i,u]=t,l=0;if(a.some((r=>0!==e[r]))){for(n in i)g.o(i,n)&&(g.m[n]=i[n]);u&&u(g)}for(r&&r(t);l<a.length;l++)o=a[l],g.o(e,o)&&e[o]&&e[o][0](),e[o]=0},t=self.webpackChunk_arnos_stuff_jupyterlab_purple_wave_theme=self.webpackChunk_arnos_stuff_jupyterlab_purple_wave_theme||[];t.forEach(r.bind(null,0)),t.push=r.bind(null,t.push.bind(t))})();var b=g(180);(_JUPYTERLAB=void 0===_JUPYTERLAB?{}:_JUPYTERLAB)["@arnos-stuff/jupyterlab-purple-wave-theme"]=b})();