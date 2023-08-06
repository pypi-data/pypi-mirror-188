/*! For license information please see fe724bbd.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[84695],{22814:(e,t,n)=>{n.d(t,{oT:()=>i,iI:()=>r,W2:()=>o,TZ:()=>a});location.protocol,location.host;const i=e=>e.map((e=>{if("string"!==e.type)return e;switch(e.name){case"username":return{...e,autocomplete:"username"};case"password":return{...e,autocomplete:"current-password"};case"code":return{...e,autocomplete:"one-time-code"};default:return e}})),r=(e,t)=>e.callWS({type:"auth/sign_path",path:t}),o=async(e,t,n,i)=>e.callWS({type:"config/auth_provider/homeassistant/create",user_id:t,username:n,password:i}),a=async(e,t,n)=>e.callWS({type:"config/auth_provider/homeassistant/admin_change_password",user_id:t,password:n})},9893:(e,t,n)=>{n.d(t,{Qo:()=>i,kb:()=>o,cs:()=>a});const i="custom:",r=window;"customCards"in r||(r.customCards=[]);const o=r.customCards,a=e=>o.find((t=>t.type===e))},2852:(e,t,n)=>{n.d(t,{t:()=>s});var i=n(37500),r=n(73728),o=n(5986),a=n(52871);const s=(e,t)=>(0,a.w)(e,t,{loadDevicesAndAreas:!0,createFlow:async(e,t)=>{const[n]=await Promise.all([(0,r.Ky)(e,t),e.loadBackendTranslation("config",t),e.loadBackendTranslation("selector",t),e.loadBackendTranslation("title",t)]);return n},fetchFlow:async(e,t)=>{const n=await(0,r.D4)(e,t);return await e.loadBackendTranslation("config",n.handler),await e.loadBackendTranslation("selector",n.handler),n},handleFlowStep:r.XO,deleteFlow:r.oi,renderAbortDescription(e,t){const n=e.localize(`component.${t.handler}.config.abort.${t.reason}`,t.description_placeholders);return n?i.dy`
            <ha-markdown allowsvg breaks .content=${n}></ha-markdown>
          `:""},renderShowFormStepHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`),renderShowFormStepDescription(e,t){const n=e.localize(`component.${t.handler}.config.step.${t.step_id}.description`,t.description_placeholders);return n?i.dy`
            <ha-markdown allowsvg breaks .content=${n}></ha-markdown>
          `:""},renderShowFormStepFieldLabel:(e,t,n)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.data.${n.name}`),renderShowFormStepFieldHelper(e,t,n){const r=e.localize(`component.${t.handler}.config.step.${t.step_id}.data_description.${n.name}`,t.description_placeholders);return r?i.dy`<ha-markdown breaks .content=${r}></ha-markdown>`:""},renderShowFormStepFieldError:(e,t,n)=>e.localize(`component.${t.handler}.config.error.${n}`,t.description_placeholders)||n,renderShowFormStepFieldLocalizeValue:(e,t,n)=>e.localize(`component.${t.handler}.selector.${n}`),renderExternalStepHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize("ui.panel.config.integrations.config_flow.external_step.open_site"),renderExternalStepDescription(e,t){const n=e.localize(`component.${t.handler}.config.${t.step_id}.description`,t.description_placeholders);return i.dy`
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.external_step.description")}
        </p>
        ${n?i.dy`
              <ha-markdown
                allowsvg
                breaks
                .content=${n}
              ></ha-markdown>
            `:""}
      `},renderCreateEntryDescription(e,t){const n=e.localize(`component.${t.handler}.config.create_entry.${t.description||"default"}`,t.description_placeholders);return i.dy`
        ${n?i.dy`
              <ha-markdown
                allowsvg
                breaks
                .content=${n}
              ></ha-markdown>
            `:""}
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.created_config","name",t.title)}
        </p>
      `},renderShowFormProgressHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`),renderShowFormProgressDescription(e,t){const n=e.localize(`component.${t.handler}.config.progress.${t.progress_action}`,t.description_placeholders);return n?i.dy`
            <ha-markdown allowsvg breaks .content=${n}></ha-markdown>
          `:""},renderMenuHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`),renderMenuDescription(e,t){const n=e.localize(`component.${t.handler}.config.step.${t.step_id}.description`,t.description_placeholders);return n?i.dy`
            <ha-markdown allowsvg breaks .content=${n}></ha-markdown>
          `:""},renderMenuOption:(e,t,n)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.menu_options.${n}`,t.description_placeholders),renderLoadingDescription(e,t,n,i){if("loading_flow"!==t&&"loading_step"!==t)return"";const r=(null==i?void 0:i.handler)||n;return e.localize(`ui.panel.config.integrations.config_flow.loading.${t}`,{integration:r?(0,o.Lh)(e.localize,r):e.localize("ui.panel.config.integrations.config_flow.loading.fallback_title")})}})},52871:(e,t,n)=>{n.d(t,{w:()=>o});var i=n(47181);const r=()=>Promise.all([n.e(98985),n.e(41985),n.e(85084),n.e(51882),n.e(45507),n.e(51644),n.e(68200),n.e(49842),n.e(1548),n.e(49075),n.e(7265),n.e(77576),n.e(29925),n.e(12545),n.e(26272),n.e(67681),n.e(4940),n.e(68101),n.e(48194),n.e(15483)]).then(n.bind(n,93990)),o=(e,t,n)=>{(0,i.B)(e,"show-dialog",{dialogTag:"dialog-data-entry-flow",dialogImport:r,dialogParams:{...t,flowConfig:n,dialogParentElement:e}})}},26765:(e,t,n)=>{n.d(t,{Ys:()=>a,g7:()=>s,D9:()=>l});var i=n(47181);const r=()=>Promise.all([n.e(85084),n.e(1281)]).then(n.bind(n,1281)),o=(e,t,n)=>new Promise((o=>{const a=t.cancel,s=t.confirm;(0,i.B)(e,"show-dialog",{dialogTag:"dialog-box",dialogImport:r,dialogParams:{...t,...n,cancel:()=>{o(!(null==n||!n.prompt)&&null),a&&a()},confirm:e=>{o(null==n||!n.prompt||e),s&&s(e)}}})})),a=(e,t)=>o(e,t),s=(e,t)=>o(e,t,{confirmation:!0}),l=(e,t)=>o(e,t,{prompt:!0})},51444:(e,t,n)=>{n.d(t,{_:()=>o});var i=n(47181);const r=()=>Promise.all([n.e(98985),n.e(85084),n.e(39928)]).then(n.bind(n,39928)),o=e=>{(0,i.B)(e,"show-dialog",{dialogTag:"ha-voice-command-dialog",dialogImport:r,dialogParams:{}})}},27849:(e,t,n)=>{n(39841);var i=n(50856);n(28426);class r extends(customElements.get("app-header-layout")){static get template(){return i.d`
      <style>
        :host {
          display: block;
          /**
         * Force app-header-layout to have its own stacking context so that its parent can
         * control the stacking of it relative to other elements (e.g. app-drawer-layout).
         * This could be done using \`isolation: isolate\`, but that's not well supported
         * across browsers.
         */
          position: relative;
          z-index: 0;
        }

        #wrapper ::slotted([slot="header"]) {
          @apply --layout-fixed-top;
          z-index: 1;
        }

        #wrapper.initializing ::slotted([slot="header"]) {
          position: relative;
        }

        :host([has-scrolling-region]) {
          height: 100%;
        }

        :host([has-scrolling-region]) #wrapper ::slotted([slot="header"]) {
          position: absolute;
        }

        :host([has-scrolling-region])
          #wrapper.initializing
          ::slotted([slot="header"]) {
          position: relative;
        }

        :host([has-scrolling-region]) #wrapper #contentContainer {
          @apply --layout-fit;
          overflow-y: auto;
          -webkit-overflow-scrolling: touch;
        }

        :host([has-scrolling-region]) #wrapper.initializing #contentContainer {
          position: relative;
        }

        #contentContainer {
          /* Create a stacking context here so that all children appear below the header. */
          position: relative;
          z-index: 0;
          /* Using 'transform' will cause 'position: fixed' elements to behave like
           'position: absolute' relative to this element. */
          transform: translate(0);
          margin-left: env(safe-area-inset-left);
          margin-right: env(safe-area-inset-right);
          padding-top: env(safe-area-inset-top);
          padding-bottom: env(safe-area-inset-bottom);
        }

        @media print {
          :host([has-scrolling-region]) #wrapper #contentContainer {
            overflow-y: visible;
          }
        }
      </style>

      <div id="wrapper" class="initializing">
        <slot id="headerSlot" name="header"></slot>

        <div id="contentContainer"><slot></slot></div>
        <slot id="fab" name="fab"></slot>
      </div>
    `}}customElements.define("ha-app-layout",r)},51153:(e,t,n)=>{n.a(e,(async e=>{n.d(t,{l$:()=>v,Z6:()=>w,Do:()=>_});n(49072),n(72225),n(26654);var i=n(10175),r=(n(80251),n(89894)),o=n(14888),a=n(69377),s=n(95035),l=n(6169),d=n(41043),c=n(57464),p=n(24617),h=n(82778),u=(n(55227),n(44921)),m=n(22720),f=n(7778),g=e([m,u,h,p,c,d,l,s,a,o,r,i]);[m,u,h,p,c,d,l,s,a,o,r,i]=g.then?await g:g;const y=new Set(["ais-easy-picker","ais-button","ais-files-list","entity","entities","button","entity-button","glance","grid","light","sensor","thermostat","weather-forecast","ais-zigbee2mqtt","ais-mini-media-player","ais-expansion-panel","tile"]),b={"alarm-panel":()=>Promise.all([n.e(98985),n.e(77639)]).then(n.bind(n,77639)),area:()=>Promise.all([n.e(97282),n.e(95795)]).then(n.bind(n,95795)),calendar:()=>Promise.resolve().then(n.bind(n,80251)),conditional:()=>n.e(68857).then(n.bind(n,68857)),"empty-state":()=>n.e(67284).then(n.bind(n,67284)),"energy-compare":()=>n.e(61046).then(n.bind(n,61046)),"energy-carbon-consumed-gauge":()=>Promise.all([n.e(21233),n.e(49915),n.e(43283),n.e(19490)]).then(n.bind(n,19490)),"energy-date-selection":()=>Promise.all([n.e(23754),n.e(2937)]).then(n.bind(n,10346)),"energy-devices-graph":()=>Promise.all([n.e(1671),n.e(62336),n.e(94576)]).then(n.bind(n,94576)),"energy-distribution":()=>n.e(9928).then(n.bind(n,9928)),"energy-gas-graph":()=>Promise.all([n.e(62336),n.e(41305)]).then(n.bind(n,41305)),"energy-water-graph":()=>Promise.all([n.e(62336),n.e(89127)]).then(n.bind(n,89127)),"energy-grid-neutrality-gauge":()=>Promise.all([n.e(64101),n.e(49915),n.e(32176)]).then(n.bind(n,32176)),"energy-solar-consumed-gauge":()=>Promise.all([n.e(66601),n.e(49915),n.e(43283),n.e(85930)]).then(n.bind(n,85930)),"energy-solar-graph":()=>Promise.all([n.e(62336),n.e(70310)]).then(n.bind(n,70310)),"energy-sources-table":()=>Promise.all([n.e(40299),n.e(16938)]).then(n.bind(n,16938)),"energy-usage-graph":()=>Promise.all([n.e(62336),n.e(9897)]).then(n.bind(n,9897)),"entity-filter":()=>n.e(33688).then(n.bind(n,33688)),error:()=>Promise.all([n.e(77426),n.e(55796)]).then(n.bind(n,55796)),gauge:()=>Promise.all([n.e(49915),n.e(43283)]).then(n.bind(n,43283)),"history-graph":()=>Promise.all([n.e(26545),n.e(62336),n.e(25825),n.e(38026)]).then(n.bind(n,38026)),"horizontal-stack":()=>n.e(89173).then(n.bind(n,89173)),humidifier:()=>n.e(68558).then(n.bind(n,68558)),iframe:()=>n.e(95018).then(n.bind(n,95018)),logbook:()=>Promise.all([n.e(99528),n.e(40967),n.e(90851)]).then(n.bind(n,8436)),map:()=>Promise.all([n.e(23956),n.e(60076)]).then(n.bind(n,60076)),markdown:()=>Promise.all([n.e(4940),n.e(26607)]).then(n.bind(n,51282)),"media-control":()=>Promise.all([n.e(28611),n.e(11866)]).then(n.bind(n,11866)),"picture-elements":()=>Promise.all([n.e(54909),n.e(97282),n.e(99810),n.e(15476)]).then(n.bind(n,83358)),"picture-entity":()=>Promise.all([n.e(97282),n.e(41500)]).then(n.bind(n,41500)),"picture-glance":()=>Promise.all([n.e(97282),n.e(66621)]).then(n.bind(n,66621)),picture:()=>n.e(45338).then(n.bind(n,45338)),"plant-status":()=>n.e(48723).then(n.bind(n,48723)),"safe-mode":()=>Promise.all([n.e(47398),n.e(24503)]).then(n.bind(n,24503)),"shopping-list":()=>Promise.all([n.e(98985),n.e(41985),n.e(43376)]).then(n.bind(n,43376)),starting:()=>n.e(47873).then(n.bind(n,47873)),"statistics-graph":()=>Promise.all([n.e(62336),n.e(95396)]).then(n.bind(n,95396)),statistic:()=>n.e(99897).then(n.bind(n,99897)),"vertical-stack":()=>n.e(26136).then(n.bind(n,26136)),"ais-list":()=>n.e(1401).then(n.t.bind(n,1401,23)),"ais-auto-entities":()=>n.e(82657).then(n.t.bind(n,82657,23)),"ais-monster":()=>n.e(47680).then(n.t.bind(n,47680,23)),"ais-fold-entity-row":()=>n.e(9795).then(n.t.bind(n,9795,23)),"ais-now-playing-poster":()=>n.e(86327).then(n.bind(n,86327)),"ais-light":()=>n.e(63238).then(n.bind(n,63238)),"ais-videoring":()=>Promise.all([n.e(49097),n.e(87795)]).then(n.bind(n,87795))},v=e=>(0,f.Xm)("card",e,y,b,void 0,void 0),w=e=>(0,f.Tw)("card",e,y,b,void 0,void 0),_=e=>(0,f.ED)(e,"card",y,b)}))},7778:(e,t,n)=>{n.d(t,{Pc:()=>o,N2:()=>a,Tw:()=>c,Xm:()=>p,ED:()=>h});var i=n(47181),r=n(9893);const o=e=>{const t=document.createElement("hui-error-card");return customElements.get("hui-error-card")?t.setConfig(e):(Promise.all([n.e(77426),n.e(55796)]).then(n.bind(n,55796)),customElements.whenDefined("hui-error-card").then((()=>{customElements.upgrade(t),t.setConfig(e)}))),t},a=(e,t)=>({type:"error",error:e,origConfig:t}),s=(e,t)=>{const n=document.createElement(e);return n.setConfig(t),n},l=(e,t)=>o(a(e,t)),d=e=>e.startsWith(r.Qo)?e.substr(r.Qo.length):void 0,c=(e,t,n,i,r,o)=>{try{return p(e,t,n,i,r,o)}catch(n){return console.error(e,t.type,n),l(n.message,t)}},p=(e,t,n,r,o,a)=>{if(!t||"object"!=typeof t)throw new Error("Config is not an object");if(!(t.type||a||o&&"entity"in t))throw new Error("No card type configured");const c=t.type?d(t.type):void 0;if(c)return((e,t)=>{if(customElements.get(e))return s(e,t);const n=l(`Custom element doesn't exist: ${e}.`,t);if(!e.includes("-"))return n;n.style.display="None";const r=window.setTimeout((()=>{n.style.display=""}),2e3);return customElements.whenDefined(e).then((()=>{clearTimeout(r),(0,i.B)(n,"ll-rebuild")})),n})(c,t);let p;if(o&&!t.type&&t.entity){p=`${o[t.entity.split(".",1)[0]]||o._domain_not_found}-entity`}else p=t.type||a;if(void 0===p)throw new Error("No type specified");const h=`hui-${p}-${e}`;if(r&&p in r)return r[p](),((e,t)=>{if(customElements.get(e))return s(e,t);const n=document.createElement(e);return customElements.whenDefined(e).then((()=>{try{customElements.upgrade(n),n.setConfig(t)}catch(e){(0,i.B)(n,"ll-rebuild")}})),n})(h,t);if(n&&n.has(p))return s(h,t);throw new Error(`Unknown type encountered: ${p}`)},h=async(e,t,n,i)=>{const r=d(e);if(r){const e=customElements.get(r);if(e)return e;if(!r.includes("-"))throw new Error(`Custom element not found: ${r}`);return new Promise(((e,t)=>{setTimeout((()=>t(new Error(`Custom element not found: ${r}`))),2e3),customElements.whenDefined(r).then((()=>e(customElements.get(r))))}))}const o=`hui-${e}-${t}`,a=customElements.get(o);if(n&&n.has(e))return a;if(i&&e in i)return a||i[e]().then((()=>customElements.get(o)));throw new Error(`Unknown type: ${e}`)}},89026:(e,t,n)=>{n.d(t,{t:()=>o,Q:()=>a});var i=n(7778);const r={picture:()=>n.e(69130).then(n.bind(n,69130)),buttons:()=>Promise.all([n.e(42109),n.e(32587)]).then(n.bind(n,32587)),graph:()=>n.e(23256).then(n.bind(n,28922))},o=e=>(0,i.Tw)("header-footer",e,void 0,r,void 0,void 0),a=e=>(0,i.ED)(e,"header-footer",void 0,r)},37482:(e,t,n)=>{n.a(e,(async e=>{n.d(t,{m:()=>f,T:()=>g});var i=n(12141),r=n(31479),o=n(23266),a=n(65716),s=n(99931),l=n(83896),d=n(45340),c=(n(56427),n(23658),n(7778)),p=e([d,l,s,a,o,r,i]);[d,l,s,a,o,r,i]=p.then?await p:p;const h=new Set(["media-player-entity","scene-entity","script-entity","sensor-entity","simple-entity","toggle-entity","button","call-service"]),u={"button-entity":()=>n.e(85611).then(n.bind(n,85611)),"climate-entity":()=>n.e(35642).then(n.bind(n,35642)),"cover-entity":()=>n.e(16755).then(n.bind(n,16755)),"group-entity":()=>n.e(81534).then(n.bind(n,81534)),"input-button-entity":()=>n.e(83968).then(n.bind(n,83968)),"humidifier-entity":()=>n.e(41102).then(n.bind(n,41102)),"input-datetime-entity":()=>Promise.all([n.e(98985),n.e(12545),n.e(32807),n.e(71163)]).then(n.bind(n,22350)),"input-number-entity":()=>Promise.all([n.e(98985),n.e(12335)]).then(n.bind(n,12335)),"input-select-entity":()=>n.e(25675).then(n.bind(n,25675)),"input-text-entity":()=>Promise.all([n.e(98985),n.e(73943)]).then(n.bind(n,73943)),"lock-entity":()=>n.e(61596).then(n.bind(n,61596)),"number-entity":()=>Promise.all([n.e(98985),n.e(66778)]).then(n.bind(n,66778)),"select-entity":()=>n.e(35994).then(n.bind(n,35994)),"text-entity":()=>Promise.all([n.e(98985),n.e(97600)]).then(n.bind(n,97600)),"timer-entity":()=>n.e(31203).then(n.bind(n,31203)),conditional:()=>n.e(97749).then(n.bind(n,97749)),"weather-entity":()=>n.e(71850).then(n.bind(n,71850)),divider:()=>n.e(41930).then(n.bind(n,41930)),section:()=>n.e(94832).then(n.bind(n,94832)),weblink:()=>n.e(44689).then(n.bind(n,44689)),cast:()=>n.e(25840).then(n.bind(n,25840)),buttons:()=>Promise.all([n.e(42109),n.e(82137)]).then(n.bind(n,82137)),attribute:()=>Promise.resolve().then(n.bind(n,45340)),text:()=>n.e(63459).then(n.bind(n,63459))},m={_domain_not_found:"simple",alert:"toggle",automation:"toggle",button:"button",climate:"climate",cover:"cover",fan:"toggle",group:"group",humidifier:"humidifier",input_boolean:"toggle",input_button:"input-button",input_number:"input-number",input_select:"input-select",input_text:"input-text",light:"toggle",lock:"lock",media_player:"media-player",number:"number",remote:"toggle",scene:"scene",script:"script",select:"select",sensor:"sensor",siren:"toggle",switch:"toggle",text:"text",timer:"timer",vacuum:"toggle",water_heater:"climate",input_datetime:"input-datetime",weather:"weather"},f=e=>(0,c.Tw)("row",e,h,u,m,void 0),g=e=>(0,c.ED)(e,"row",h,u)}))},44295:(e,t,n)=>{n.a(e,(async e=>{n.r(t);n(53268),n(12730);var i=n(37500),r=n(36924),o=n(14516),a=n(7323),s=(n(10983),n(48932),n(51444)),l=(n(27849),n(11654)),d=n(51153),c=e([d]);function p(){p=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(n){t.forEach((function(t){t.kind===n&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var n=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var r=t.placement;if(t.kind===i&&("static"===r||"prototype"===r)){var o="static"===r?e:n;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var n=t.descriptor;if("field"===t.kind){var i=t.initializer;n={enumerable:n.enumerable,writable:n.writable,configurable:n.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,n)},decorateClass:function(e,t){var n=[],i=[],r={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,r)}),this),e.forEach((function(e){if(!m(e))return n.push(e);var t=this.decorateElement(e,r);n.push(t.element),n.push.apply(n,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:n,finishers:i};var o=this.decorateConstructor(n,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,n){var i=t[e.placement];if(!n&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var n=[],i=[],r=e.decorators,o=r.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,r[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);n.push.apply(n,d)}}return{element:e,finishers:i,extras:n}},decorateConstructor:function(e,t){for(var n=[],i=t.length-1;i>=0;i--){var r=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(r)||r);if(void 0!==o.finisher&&n.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:n}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return b(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?b(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var n=y(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var r=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:n,placement:i,descriptor:Object.assign({},r)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(r,"get","The property descriptor of a field descriptor"),this.disallowProperty(r,"set","The property descriptor of a field descriptor"),this.disallowProperty(r,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:g(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var n=g(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:n}},runClassFinishers:function(e,t){for(var n=0;n<t.length;n++){var i=(0,t[n])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,n){if(void 0!==e[t])throw new TypeError(n+" can't have a ."+t+" property.")}};return e}function h(e){var t,n=y(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:n,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function u(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function m(e){return e.decorators&&e.decorators.length}function f(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function g(e,t){var n=e[t];if(void 0!==n&&"function"!=typeof n)throw new TypeError("Expected '"+t+"' to be a function");return n}function y(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var i=n.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function b(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,i=new Array(t);n<t;n++)i[n]=e[n];return i}function v(){return v="undefined"!=typeof Reflect&&Reflect.get?Reflect.get.bind():function(e,t,n){var i=w(e,t);if(i){var r=Object.getOwnPropertyDescriptor(i,t);return r.get?r.get.call(arguments.length<3?e:n):r.value}},v.apply(this,arguments)}function w(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=_(e)););return e}function _(e){return _=Object.setPrototypeOf?Object.getPrototypeOf.bind():function(e){return e.__proto__||Object.getPrototypeOf(e)},_(e)}d=(c.then?await c:c)[0];!function(e,t,n,i){var r=p();if(i)for(var o=0;o<i.length;o++)r=i[o](r);var a=t((function(e){r.initializeInstanceElements(e,s.elements)}),n),s=r.decorateClass(function(e){for(var t=[],n=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var r,o=e[i];if("method"===o.kind&&(r=t.find(n)))if(f(o.descriptor)||f(r.descriptor)){if(m(o)||m(r))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");r.descriptor=o.descriptor}else{if(m(o)){if(m(r))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");r.decorators=o.decorators}u(o,r)}else t.push(o)}return t}(a.d.map(h)),e);r.initializeClassElements(a.F,s.elements),r.runClassFinishers(a.F,s.finishers)}([(0,r.Mo)("ha-panel-shopping-list")],(function(e,t){class n extends t{constructor(...t){super(...t),e(this)}}return{F:n,d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_card",value:void 0},{kind:"field",key:"_conversation",value(){return(0,o.Z)((e=>(0,a.p)(this.hass,"conversation")))}},{kind:"method",key:"firstUpdated",value:function(e){v(_(n.prototype),"firstUpdated",this).call(this,e),this._card=(0,d.Z6)({type:"shopping-list"}),this._card.hass=this.hass}},{kind:"method",key:"updated",value:function(e){v(_(n.prototype),"updated",this).call(this,e),e.has("hass")&&(this._card.hass=this.hass)}},{kind:"method",key:"render",value:function(){return i.dy`
      <ha-app-layout>
        <app-header fixed slot="header">
          <app-toolbar>
            <ha-menu-button
              .hass=${this.hass}
              .narrow=${this.narrow}
            ></ha-menu-button>
            <div main-title>${this.hass.localize("panel.shopping_list")}</div>
            ${this._conversation(this.hass.config.components)?i.dy`
                  <ha-icon-button
                    .label=${this.hass.localize("ui.panel.shopping_list.start_conversation")}
                    .path=${"M12,2A3,3 0 0,1 15,5V11A3,3 0 0,1 12,14A3,3 0 0,1 9,11V5A3,3 0 0,1 12,2M19,11C19,14.53 16.39,17.44 13,17.93V21H11V17.93C7.61,17.44 5,14.53 5,11H7A5,5 0 0,0 12,16A5,5 0 0,0 17,11H19Z"}
                    @click=${this._showVoiceCommandDialog}
                  ></ha-icon-button>
                `:""}
          </app-toolbar>
        </app-header>
        <div id="columns">
          <div class="column">${this._card}</div>
        </div>
      </ha-app-layout>
    `}},{kind:"method",key:"_showVoiceCommandDialog",value:function(){(0,s._)(this)}},{kind:"get",static:!0,key:"styles",value:function(){return[l.Qx,i.iv`
        :host {
          display: block;
          height: 100%;
        }
        app-header {
          --mdc-theme-primary: var(--app-header-text-color);
        }
        :host([narrow]) app-toolbar mwc-button {
          width: 65px;
        }
        .heading {
          overflow: hidden;
          white-space: nowrap;
          margin-top: 4px;
        }
        #columns {
          display: flex;
          flex-direction: row;
          justify-content: center;
          margin-left: 4px;
          margin-right: 4px;
        }
        .column {
          flex: 1 0 0;
          max-width: 500px;
          min-width: 0;
        }
      `]}}]}}),i.oi)}))},19596:(e,t,n)=>{n.d(t,{sR:()=>p});var i=n(81563),r=n(38941);const o=(e,t)=>{var n,i;const r=e._$AN;if(void 0===r)return!1;for(const e of r)null===(i=(n=e)._$AO)||void 0===i||i.call(n,t,!1),o(e,t);return!0},a=e=>{let t,n;do{if(void 0===(t=e._$AM))break;n=t._$AN,n.delete(e),e=t}while(0===(null==n?void 0:n.size))},s=e=>{for(let t;t=e._$AM;e=t){let n=t._$AN;if(void 0===n)t._$AN=n=new Set;else if(n.has(e))break;n.add(e),c(t)}};function l(e){void 0!==this._$AN?(a(this),this._$AM=e,s(this)):this._$AM=e}function d(e,t=!1,n=0){const i=this._$AH,r=this._$AN;if(void 0!==r&&0!==r.size)if(t)if(Array.isArray(i))for(let e=n;e<i.length;e++)o(i[e],!1),a(i[e]);else null!=i&&(o(i,!1),a(i));else o(this,e)}const c=e=>{var t,n,i,o;e.type==r.pX.CHILD&&(null!==(t=(i=e)._$AP)&&void 0!==t||(i._$AP=d),null!==(n=(o=e)._$AQ)&&void 0!==n||(o._$AQ=l))};class p extends r.Xe{constructor(){super(...arguments),this._$AN=void 0}_$AT(e,t,n){super._$AT(e,t,n),s(this),this.isConnected=e._$AU}_$AO(e,t=!0){var n,i;e!==this.isConnected&&(this.isConnected=e,e?null===(n=this.reconnected)||void 0===n||n.call(this):null===(i=this.disconnected)||void 0===i||i.call(this)),t&&(o(this,e),a(this))}setValue(e){if((0,i.OR)(this._$Ct))this._$Ct._$AI(e,this);else{const t=[...this._$Ct._$AH];t[this._$Ci]=e,this._$Ct._$AI(t,this,0)}}disconnected(){}reconnected(){}}},81563:(e,t,n)=>{n.d(t,{E_:()=>f,i9:()=>u,_Y:()=>d,pt:()=>o,OR:()=>s,hN:()=>a,ws:()=>m,fk:()=>c,hl:()=>h});var i=n(15304);const{I:r}=i.Al,o=e=>null===e||"object"!=typeof e&&"function"!=typeof e,a=(e,t)=>void 0===t?void 0!==(null==e?void 0:e._$litType$):(null==e?void 0:e._$litType$)===t,s=e=>void 0===e.strings,l=()=>document.createComment(""),d=(e,t,n)=>{var i;const o=e._$AA.parentNode,a=void 0===t?e._$AB:t._$AA;if(void 0===n){const t=o.insertBefore(l(),a),i=o.insertBefore(l(),a);n=new r(t,i,e,e.options)}else{const t=n._$AB.nextSibling,r=n._$AM,s=r!==e;if(s){let t;null===(i=n._$AQ)||void 0===i||i.call(n,e),n._$AM=e,void 0!==n._$AP&&(t=e._$AU)!==r._$AU&&n._$AP(t)}if(t!==a||s){let e=n._$AA;for(;e!==t;){const t=e.nextSibling;o.insertBefore(e,a),e=t}}}return n},c=(e,t,n=e)=>(e._$AI(t,n),e),p={},h=(e,t=p)=>e._$AH=t,u=e=>e._$AH,m=e=>{var t;null===(t=e._$AP)||void 0===t||t.call(e,!1,!0);let n=e._$AA;const i=e._$AB.nextSibling;for(;n!==i;){const e=n.nextSibling;n.remove(),n=e}},f=e=>{e._$AR()}}}]);
//# sourceMappingURL=fe724bbd.js.map