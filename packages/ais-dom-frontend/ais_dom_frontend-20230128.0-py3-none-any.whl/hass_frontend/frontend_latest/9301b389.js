"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[33137],{73728:(e,t,r)=>{r.d(t,{pV:()=>a,P3:()=>s,Ky:()=>c,D4:()=>d,XO:()=>p,zO:()=>f,oi:()=>h,d4:()=>u,D7:()=>m,ZJ:()=>g,V3:()=>y,WW:()=>v});var i=r(97330),n=r(38346),o=r(5986);const a=["bluetooth","dhcp","discovery","hardware","hassio","homekit","integration_discovery","mqtt","ssdp","unignore","usb","zeroconf"],s=["reauth"],l={"HA-Frontend-Base":`${location.protocol}//${location.host}`},c=(e,t)=>{var r;return e.callApi("POST","config/config_entries/flow",{handler:t,show_advanced_options:Boolean(null===(r=e.userData)||void 0===r?void 0:r.showAdvanced)},l)},d=(e,t)=>e.callApi("GET",`config/config_entries/flow/${t}`,void 0,l),p=(e,t,r)=>e.callApi("POST",`config/config_entries/flow/${t}`,r,l),f=(e,t,r)=>e.callWS({type:"config_entries/ignore_flow",flow_id:t,title:r}),h=(e,t)=>e.callApi("DELETE",`config/config_entries/flow/${t}`),u=(e,t)=>e.callApi("GET","config/config_entries/flow_handlers"+(t?`?type=${t}`:"")),m=e=>e.sendMessagePromise({type:"config_entries/flow/progress"}),w=(e,t)=>e.subscribeEvents((0,n.D)((()=>m(e).then((e=>t.setState(e,!0)))),500,!0),"config_entry_discovered"),g=e=>(0,i._)(e,"_configFlowProgress",m,w),y=(e,t)=>g(e.connection).subscribe(t),v=(e,t)=>t.context.title_placeholders&&0!==Object.keys(t.context.title_placeholders).length?e(`component.${t.handler}.config.flow_title`,t.context.title_placeholders)||("name"in t.context.title_placeholders?t.context.title_placeholders.name:(0,o.Lh)(e,t.handler)):(0,o.Lh)(e,t.handler)},2852:(e,t,r)=>{r.d(t,{t:()=>s});var i=r(37500),n=r(73728),o=r(5986),a=r(52871);const s=(e,t)=>(0,a.w)(e,t,{loadDevicesAndAreas:!0,createFlow:async(e,t)=>{const[r]=await Promise.all([(0,n.Ky)(e,t),e.loadBackendTranslation("config",t),e.loadBackendTranslation("selector",t),e.loadBackendTranslation("title",t)]);return r},fetchFlow:async(e,t)=>{const r=await(0,n.D4)(e,t);return await e.loadBackendTranslation("config",r.handler),await e.loadBackendTranslation("selector",r.handler),r},handleFlowStep:n.XO,deleteFlow:n.oi,renderAbortDescription(e,t){const r=e.localize(`component.${t.handler}.config.abort.${t.reason}`,t.description_placeholders);return r?i.dy`
            <ha-markdown allowsvg breaks .content=${r}></ha-markdown>
          `:""},renderShowFormStepHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`),renderShowFormStepDescription(e,t){const r=e.localize(`component.${t.handler}.config.step.${t.step_id}.description`,t.description_placeholders);return r?i.dy`
            <ha-markdown allowsvg breaks .content=${r}></ha-markdown>
          `:""},renderShowFormStepFieldLabel:(e,t,r)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.data.${r.name}`),renderShowFormStepFieldHelper(e,t,r){const n=e.localize(`component.${t.handler}.config.step.${t.step_id}.data_description.${r.name}`,t.description_placeholders);return n?i.dy`<ha-markdown breaks .content=${n}></ha-markdown>`:""},renderShowFormStepFieldError:(e,t,r)=>e.localize(`component.${t.handler}.config.error.${r}`,t.description_placeholders)||r,renderShowFormStepFieldLocalizeValue:(e,t,r)=>e.localize(`component.${t.handler}.selector.${r}`),renderExternalStepHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize("ui.panel.config.integrations.config_flow.external_step.open_site"),renderExternalStepDescription(e,t){const r=e.localize(`component.${t.handler}.config.${t.step_id}.description`,t.description_placeholders);return i.dy`
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.external_step.description")}
        </p>
        ${r?i.dy`
              <ha-markdown
                allowsvg
                breaks
                .content=${r}
              ></ha-markdown>
            `:""}
      `},renderCreateEntryDescription(e,t){const r=e.localize(`component.${t.handler}.config.create_entry.${t.description||"default"}`,t.description_placeholders);return i.dy`
        ${r?i.dy`
              <ha-markdown
                allowsvg
                breaks
                .content=${r}
              ></ha-markdown>
            `:""}
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.created_config","name",t.title)}
        </p>
      `},renderShowFormProgressHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`),renderShowFormProgressDescription(e,t){const r=e.localize(`component.${t.handler}.config.progress.${t.progress_action}`,t.description_placeholders);return r?i.dy`
            <ha-markdown allowsvg breaks .content=${r}></ha-markdown>
          `:""},renderMenuHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`),renderMenuDescription(e,t){const r=e.localize(`component.${t.handler}.config.step.${t.step_id}.description`,t.description_placeholders);return r?i.dy`
            <ha-markdown allowsvg breaks .content=${r}></ha-markdown>
          `:""},renderMenuOption:(e,t,r)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.menu_options.${r}`,t.description_placeholders),renderLoadingDescription(e,t,r,i){if("loading_flow"!==t&&"loading_step"!==t)return"";const n=(null==i?void 0:i.handler)||r;return e.localize(`ui.panel.config.integrations.config_flow.loading.${t}`,{integration:n?(0,o.Lh)(e.localize,n):e.localize("ui.panel.config.integrations.config_flow.loading.fallback_title")})}})},52871:(e,t,r)=>{r.d(t,{w:()=>o});var i=r(47181);const n=()=>Promise.all([r.e(98985),r.e(41985),r.e(85084),r.e(51882),r.e(45507),r.e(51644),r.e(68200),r.e(49842),r.e(1548),r.e(49075),r.e(7265),r.e(77576),r.e(29925),r.e(12545),r.e(26272),r.e(67681),r.e(4940),r.e(68101),r.e(48194),r.e(15483)]).then(r.bind(r,93990)),o=(e,t,r)=>{(0,i.B)(e,"show-dialog",{dialogTag:"dialog-data-entry-flow",dialogImport:n,dialogParams:{...t,flowConfig:r,dialogParentElement:e}})}},33137:(e,t,r)=>{r.r(t);r(53268),r(12730),r(60010),r(38353),r(63081);var i=r(37500),n=r(36924),o=r(2852),a=r(47181),s=r(11654);function l(){l=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!p(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return m(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?m(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=u(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:h(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=h(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function c(e){var t,r=u(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function p(e){return e.decorators&&e.decorators.length}function f(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function h(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function u(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var n=l();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var a=t((function(e){n.initializeInstanceElements(e,s.elements)}),r),s=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(f(o.descriptor)||f(n.descriptor)){if(p(o)||p(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(p(o)){if(p(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}d(o,n)}else t.push(o)}return t}(a.d.map(c)),e);n.initializeClassElements(a.F,s.elements),n.runClassFinishers(a.F,s.finishers)}([(0,n.Mo)("ha-config-ais-dom-config-wifi")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"isWide",value:()=>!0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"narrow",value:()=>!1},{kind:"method",key:"firstUpdated",value:async function(){}},{kind:"method",key:"render",value:function(){return this.hass?i.dy`
      <hass-subpage header="Konfiguracja bramki AIS dom">
        <div .narrow=${this.narrow}>
          <ha-config-section .isWide=${this.isWide}>
            <span slot="header">Połączenie WiFi</span>
            <span slot="introduction"
              >Możesz sprawdzić lub skonfigurować parametry połączenia
              WiFi</span
            >
            <ha-card header="Parametry sieci">
              <div class="card-content" style="display: flex;">
                <div style="text-align: center;">
                  <div class="aisInfoRow">Lokalna nazwa hosta</div>
                  <div class="aisInfoRow">
                    <mwc-button
                      >${this.hass.states["sensor.local_host_name"].state}
                      <ha-icon
                        class="user-button"
                        icon="hass:cog"
                        @click=${this.createFlowHostName}
                      ></ha-icon>
                    </mwc-button>
                  </div>
                </div>
                <div style="text-align: center;" @click=${this.showLocalIpInfo}>
                  <div class="aisInfoRow">Lokalny adres IP</div>
                  <div class="aisInfoRow">
                    <mwc-button
                      >${this.hass.states["sensor.internal_ip_address"].state}</mwc-button
                    >
                  </div>
                </div>
                <div
                  @click=${this.showWiFiSpeedInfo}
                  style="text-align: center;"
                >
                  <div class="aisInfoRow">Prędkość połączenia WiFi</div>
                  <div class="aisInfoRow">
                    <mwc-button
                      >${this.hass.states["sensor.ais_wifi_service_current_network_info"].state}</mwc-button
                    >
                  </div>
                </div>
              </div>
              <div class="card-actions">
                <ha-icon
                  class="user-button"
                  icon="hass:wifi"
                  @click=${this.showWiFiGroup}
                ></ha-icon
                ><mwc-button @click=${this.createFlowWifi}
                  >Konfigurator połączenia z siecą WiFi</mwc-button
                >
              </div>
            </ha-card>
          </ha-config-section>
        </div>
      </hass-subpage>
    `:i.dy``}},{kind:"get",static:!0,key:"styles",value:function(){return[s.Qx,i.iv`
        .content {
          padding-bottom: 32px;
        }
        .border {
          margin: 32px auto 0;
          border-bottom: 1px solid rgba(0, 0, 0, 0.12);
          max-width: 1040px;
        }
        .narrow .border {
          max-width: 640px;
        }
        div.aisInfoRow {
          display: inline-block;
        }
        .center-container {
          @apply --layout-vertical;
          @apply --layout-center-center;
          height: 70px;
        }
        div.card-actions {
          text-align: center;
        }
      `]}},{kind:"method",key:"showWiFiGroup",value:function(){(0,a.B)(this,"hass-more-info",{entityId:"group.internet_status"})}},{kind:"method",key:"showWiFiSpeedInfo",value:function(){(0,a.B)(this,"hass-more-info",{entityId:"sensor.ais_wifi_service_current_network_info"})}},{kind:"method",key:"showLocalIpInfo",value:function(){(0,a.B)(this,"hass-more-info",{entityId:"sensor.internal_ip_address"})}},{kind:"method",key:"_continueFlow",value:function(e){(0,o.t)(this,{continueFlowId:e,dialogClosedCallback:()=>{console.log("OK")}})}},{kind:"method",key:"createFlowHostName",value:function(){this.hass.callApi("POST","config/config_entries/flow",{handler:"ais_host"}).then((e=>{this._continueFlow(e.flow_id)}))}},{kind:"method",key:"createFlowWifi",value:function(){this.hass.callApi("POST","config/config_entries/flow",{handler:"ais_wifi_service"}).then((e=>{console.log(e),this._continueFlow(e.flow_id)}))}}]}}),i.oi)}}]);
//# sourceMappingURL=9301b389.js.map