/*! For license information please see 0276959b.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[88158,74844,22289,62293,63251,66896,31588,84977,86603,28066],{92685:(t,e,i)=>{i.d(e,{a:()=>u});var n=i(87480),a=i(72774),o={ROOT:"mdc-form-field"},r={LABEL_SELECTOR:".mdc-form-field > label"};const s=function(t){function e(i){var a=t.call(this,(0,n.__assign)((0,n.__assign)({},e.defaultAdapter),i))||this;return a.click=function(){a.handleClick()},a}return(0,n.__extends)(e,t),Object.defineProperty(e,"cssClasses",{get:function(){return o},enumerable:!1,configurable:!0}),Object.defineProperty(e,"strings",{get:function(){return r},enumerable:!1,configurable:!0}),Object.defineProperty(e,"defaultAdapter",{get:function(){return{activateInputRipple:function(){},deactivateInputRipple:function(){},deregisterInteractionHandler:function(){},registerInteractionHandler:function(){}}},enumerable:!1,configurable:!0}),e.prototype.init=function(){this.adapter.registerInteractionHandler("click",this.click)},e.prototype.destroy=function(){this.adapter.deregisterInteractionHandler("click",this.click)},e.prototype.handleClick=function(){var t=this;this.adapter.activateInputRipple(),requestAnimationFrame((function(){t.adapter.deactivateInputRipple()}))},e}(a.K);var l=i(78220),c=i(18601),d=i(14114),p=i(37500),h=i(36924),m=i(8636);class u extends l.H{constructor(){super(...arguments),this.alignEnd=!1,this.spaceBetween=!1,this.nowrap=!1,this.label="",this.mdcFoundationClass=s}createAdapter(){return{registerInteractionHandler:(t,e)=>{this.labelEl.addEventListener(t,e)},deregisterInteractionHandler:(t,e)=>{this.labelEl.removeEventListener(t,e)},activateInputRipple:async()=>{const t=this.input;if(t instanceof c.Wg){const e=await t.ripple;e&&e.startPress()}},deactivateInputRipple:async()=>{const t=this.input;if(t instanceof c.Wg){const e=await t.ripple;e&&e.endPress()}}}}get input(){var t,e;return null!==(e=null===(t=this.slottedInputs)||void 0===t?void 0:t[0])&&void 0!==e?e:null}render(){const t={"mdc-form-field--align-end":this.alignEnd,"mdc-form-field--space-between":this.spaceBetween,"mdc-form-field--nowrap":this.nowrap};return p.dy`
      <div class="mdc-form-field ${(0,m.$)(t)}">
        <slot></slot>
        <label class="mdc-label"
               @click="${this._labelClick}">${this.label}</label>
      </div>`}click(){this._labelClick()}_labelClick(){const t=this.input;t&&(t.focus(),t.click())}}(0,n.__decorate)([(0,h.Cb)({type:Boolean})],u.prototype,"alignEnd",void 0),(0,n.__decorate)([(0,h.Cb)({type:Boolean})],u.prototype,"spaceBetween",void 0),(0,n.__decorate)([(0,h.Cb)({type:Boolean})],u.prototype,"nowrap",void 0),(0,n.__decorate)([(0,h.Cb)({type:String}),(0,d.P)((async function(t){var e;null===(e=this.input)||void 0===e||e.setAttribute("aria-label",t)}))],u.prototype,"label",void 0),(0,n.__decorate)([(0,h.IO)(".mdc-form-field")],u.prototype,"mdcRoot",void 0),(0,n.__decorate)([(0,h.vZ)("",!0,"*")],u.prototype,"slottedInputs",void 0),(0,n.__decorate)([(0,h.IO)("label")],u.prototype,"labelEl",void 0)},92038:(t,e,i)=>{i.d(e,{W:()=>n});const n=i(37500).iv`.mdc-form-field{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87));display:inline-flex;align-items:center;vertical-align:middle}.mdc-form-field>label{margin-left:0;margin-right:auto;padding-left:4px;padding-right:0;order:0}[dir=rtl] .mdc-form-field>label,.mdc-form-field>label[dir=rtl]{margin-left:auto;margin-right:0}[dir=rtl] .mdc-form-field>label,.mdc-form-field>label[dir=rtl]{padding-left:0;padding-right:4px}.mdc-form-field--nowrap>label{text-overflow:ellipsis;overflow:hidden;white-space:nowrap}.mdc-form-field--align-end>label{margin-left:auto;margin-right:0;padding-left:0;padding-right:4px;order:-1}[dir=rtl] .mdc-form-field--align-end>label,.mdc-form-field--align-end>label[dir=rtl]{margin-left:0;margin-right:auto}[dir=rtl] .mdc-form-field--align-end>label,.mdc-form-field--align-end>label[dir=rtl]{padding-left:4px;padding-right:0}.mdc-form-field--space-between{justify-content:space-between}.mdc-form-field--space-between>label{margin:0}[dir=rtl] .mdc-form-field--space-between>label,.mdc-form-field--space-between>label[dir=rtl]{margin:0}:host{display:inline-flex}.mdc-form-field{width:100%}::slotted(*){-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}::slotted(mwc-switch){margin-right:10px}[dir=rtl] ::slotted(mwc-switch),::slotted(mwc-switch[dir=rtl]){margin-left:10px}`},11581:(t,e,i)=>{i.d(e,{H:()=>f});var n=i(87480),a=(i(91156),i(38103)),o=i(78220),r=i(14114),s=i(98734),l=i(72774),c={CHECKED:"mdc-switch--checked",DISABLED:"mdc-switch--disabled"},d={ARIA_CHECKED_ATTR:"aria-checked",NATIVE_CONTROL_SELECTOR:".mdc-switch__native-control",RIPPLE_SURFACE_SELECTOR:".mdc-switch__thumb-underlay"};const p=function(t){function e(i){return t.call(this,(0,n.__assign)((0,n.__assign)({},e.defaultAdapter),i))||this}return(0,n.__extends)(e,t),Object.defineProperty(e,"strings",{get:function(){return d},enumerable:!1,configurable:!0}),Object.defineProperty(e,"cssClasses",{get:function(){return c},enumerable:!1,configurable:!0}),Object.defineProperty(e,"defaultAdapter",{get:function(){return{addClass:function(){},removeClass:function(){},setNativeControlChecked:function(){},setNativeControlDisabled:function(){},setNativeControlAttr:function(){}}},enumerable:!1,configurable:!0}),e.prototype.setChecked=function(t){this.adapter.setNativeControlChecked(t),this.updateAriaChecked(t),this.updateCheckedStyling(t)},e.prototype.setDisabled=function(t){this.adapter.setNativeControlDisabled(t),t?this.adapter.addClass(c.DISABLED):this.adapter.removeClass(c.DISABLED)},e.prototype.handleChange=function(t){var e=t.target;this.updateAriaChecked(e.checked),this.updateCheckedStyling(e.checked)},e.prototype.updateCheckedStyling=function(t){t?this.adapter.addClass(c.CHECKED):this.adapter.removeClass(c.CHECKED)},e.prototype.updateAriaChecked=function(t){this.adapter.setNativeControlAttr(d.ARIA_CHECKED_ATTR,""+!!t)},e}(l.K);var h=i(37500),m=i(36924),u=i(51346);class f extends o.H{constructor(){super(...arguments),this.checked=!1,this.disabled=!1,this.shouldRenderRipple=!1,this.mdcFoundationClass=p,this.rippleHandlers=new s.A((()=>(this.shouldRenderRipple=!0,this.ripple)))}changeHandler(t){this.mdcFoundation.handleChange(t),this.checked=this.formElement.checked}createAdapter(){return Object.assign(Object.assign({},(0,o.q)(this.mdcRoot)),{setNativeControlChecked:t=>{this.formElement.checked=t},setNativeControlDisabled:t=>{this.formElement.disabled=t},setNativeControlAttr:(t,e)=>{this.formElement.setAttribute(t,e)}})}renderRipple(){return this.shouldRenderRipple?h.dy`
        <mwc-ripple
          .accent="${this.checked}"
          .disabled="${this.disabled}"
          unbounded>
        </mwc-ripple>`:""}focus(){const t=this.formElement;t&&(this.rippleHandlers.startFocus(),t.focus())}blur(){const t=this.formElement;t&&(this.rippleHandlers.endFocus(),t.blur())}click(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}firstUpdated(){super.firstUpdated(),this.shadowRoot&&this.mdcRoot.addEventListener("change",(t=>{this.dispatchEvent(new Event("change",t))}))}render(){return h.dy`
      <div class="mdc-switch">
        <div class="mdc-switch__track"></div>
        <div class="mdc-switch__thumb-underlay">
          ${this.renderRipple()}
          <div class="mdc-switch__thumb">
            <input
              type="checkbox"
              id="basic-switch"
              class="mdc-switch__native-control"
              role="switch"
              aria-label="${(0,u.o)(this.ariaLabel)}"
              aria-labelledby="${(0,u.o)(this.ariaLabelledBy)}"
              @change="${this.changeHandler}"
              @focus="${this.handleRippleFocus}"
              @blur="${this.handleRippleBlur}"
              @mousedown="${this.handleRippleMouseDown}"
              @mouseenter="${this.handleRippleMouseEnter}"
              @mouseleave="${this.handleRippleMouseLeave}"
              @touchstart="${this.handleRippleTouchStart}"
              @touchend="${this.handleRippleDeactivate}"
              @touchcancel="${this.handleRippleDeactivate}">
          </div>
        </div>
      </div>`}handleRippleMouseDown(t){const e=()=>{window.removeEventListener("mouseup",e),this.handleRippleDeactivate()};window.addEventListener("mouseup",e),this.rippleHandlers.startPress(t)}handleRippleTouchStart(t){this.rippleHandlers.startPress(t)}handleRippleDeactivate(){this.rippleHandlers.endPress()}handleRippleMouseEnter(){this.rippleHandlers.startHover()}handleRippleMouseLeave(){this.rippleHandlers.endHover()}handleRippleFocus(){this.rippleHandlers.startFocus()}handleRippleBlur(){this.rippleHandlers.endFocus()}}(0,n.__decorate)([(0,m.Cb)({type:Boolean}),(0,r.P)((function(t){this.mdcFoundation.setChecked(t)}))],f.prototype,"checked",void 0),(0,n.__decorate)([(0,m.Cb)({type:Boolean}),(0,r.P)((function(t){this.mdcFoundation.setDisabled(t)}))],f.prototype,"disabled",void 0),(0,n.__decorate)([a.L,(0,m.Cb)({attribute:"aria-label"})],f.prototype,"ariaLabel",void 0),(0,n.__decorate)([a.L,(0,m.Cb)({attribute:"aria-labelledby"})],f.prototype,"ariaLabelledBy",void 0),(0,n.__decorate)([(0,m.IO)(".mdc-switch")],f.prototype,"mdcRoot",void 0),(0,n.__decorate)([(0,m.IO)("input")],f.prototype,"formElement",void 0),(0,n.__decorate)([(0,m.GC)("mwc-ripple")],f.prototype,"ripple",void 0),(0,n.__decorate)([(0,m.SB)()],f.prototype,"shouldRenderRipple",void 0),(0,n.__decorate)([(0,m.hO)({passive:!0})],f.prototype,"handleRippleMouseDown",null),(0,n.__decorate)([(0,m.hO)({passive:!0})],f.prototype,"handleRippleTouchStart",null)},4301:(t,e,i)=>{i.d(e,{W:()=>n});const n=i(37500).iv`.mdc-switch__thumb-underlay{left:-14px;right:initial;top:-17px;width:48px;height:48px}[dir=rtl] .mdc-switch__thumb-underlay,.mdc-switch__thumb-underlay[dir=rtl]{left:initial;right:-14px}.mdc-switch__native-control{width:64px;height:48px}.mdc-switch{display:inline-block;position:relative;outline:none;user-select:none}.mdc-switch.mdc-switch--checked .mdc-switch__track{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786)}.mdc-switch.mdc-switch--checked .mdc-switch__thumb{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786);border-color:#018786;border-color:var(--mdc-theme-secondary, #018786)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__track{background-color:#000;background-color:var(--mdc-theme-on-surface, #000)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb{background-color:#fff;background-color:var(--mdc-theme-surface, #fff);border-color:#fff;border-color:var(--mdc-theme-surface, #fff)}.mdc-switch__native-control{left:0;right:initial;position:absolute;top:0;margin:0;opacity:0;cursor:pointer;pointer-events:auto;transition:transform 90ms cubic-bezier(0.4, 0, 0.2, 1)}[dir=rtl] .mdc-switch__native-control,.mdc-switch__native-control[dir=rtl]{left:initial;right:0}.mdc-switch__track{box-sizing:border-box;width:36px;height:14px;border:1px solid transparent;border-radius:7px;opacity:.38;transition:opacity 90ms cubic-bezier(0.4, 0, 0.2, 1),background-color 90ms cubic-bezier(0.4, 0, 0.2, 1),border-color 90ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-switch__thumb-underlay{display:flex;position:absolute;align-items:center;justify-content:center;transform:translateX(0);transition:transform 90ms cubic-bezier(0.4, 0, 0.2, 1),background-color 90ms cubic-bezier(0.4, 0, 0.2, 1),border-color 90ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-switch__thumb{box-shadow:0px 3px 1px -2px rgba(0, 0, 0, 0.2),0px 2px 2px 0px rgba(0, 0, 0, 0.14),0px 1px 5px 0px rgba(0,0,0,.12);box-sizing:border-box;width:20px;height:20px;border:10px solid;border-radius:50%;pointer-events:none;z-index:1}.mdc-switch--checked .mdc-switch__track{opacity:.54}.mdc-switch--checked .mdc-switch__thumb-underlay{transform:translateX(16px)}[dir=rtl] .mdc-switch--checked .mdc-switch__thumb-underlay,.mdc-switch--checked .mdc-switch__thumb-underlay[dir=rtl]{transform:translateX(-16px)}.mdc-switch--checked .mdc-switch__native-control{transform:translateX(-16px)}[dir=rtl] .mdc-switch--checked .mdc-switch__native-control,.mdc-switch--checked .mdc-switch__native-control[dir=rtl]{transform:translateX(16px)}.mdc-switch--disabled{opacity:.38;pointer-events:none}.mdc-switch--disabled .mdc-switch__thumb{border-width:1px}.mdc-switch--disabled .mdc-switch__native-control{cursor:default;pointer-events:none}:host{display:inline-flex;outline:none;-webkit-tap-highlight-color:transparent}`},63207:(t,e,i)=>{i(65660),i(15112);var n=i(9672),a=i(87156),o=i(50856),r=i(10994);(0,n.k)({_template:o.d`
    <style>
      :host {
        @apply --layout-inline;
        @apply --layout-center-center;
        position: relative;

        vertical-align: middle;

        fill: var(--iron-icon-fill-color, currentcolor);
        stroke: var(--iron-icon-stroke-color, none);

        width: var(--iron-icon-width, 24px);
        height: var(--iron-icon-height, 24px);
        @apply --iron-icon;
      }

      :host([hidden]) {
        display: none;
      }
    </style>
`,is:"iron-icon",properties:{icon:{type:String},theme:{type:String},src:{type:String},_meta:{value:r.XY.create("iron-meta",{type:"iconset"})}},observers:["_updateIcon(_meta, isAttached)","_updateIcon(theme, isAttached)","_srcChanged(src, isAttached)","_iconChanged(icon, isAttached)"],_DEFAULT_ICONSET:"icons",_iconChanged:function(t){var e=(t||"").split(":");this._iconName=e.pop(),this._iconsetName=e.pop()||this._DEFAULT_ICONSET,this._updateIcon()},_srcChanged:function(t){this._updateIcon()},_usesIconset:function(){return this.icon||!this.src},_updateIcon:function(){this._usesIconset()?(this._img&&this._img.parentNode&&(0,a.vz)(this.root).removeChild(this._img),""===this._iconName?this._iconset&&this._iconset.removeIcon(this):this._iconsetName&&this._meta&&(this._iconset=this._meta.byKey(this._iconsetName),this._iconset?(this._iconset.applyIcon(this,this._iconName,this.theme),this.unlisten(window,"iron-iconset-added","_updateIcon")):this.listen(window,"iron-iconset-added","_updateIcon"))):(this._iconset&&this._iconset.removeIcon(this),this._img||(this._img=document.createElement("img"),this._img.style.width="100%",this._img.style.height="100%",this._img.draggable=!1),this._img.src=this.src,(0,a.vz)(this.root).appendChild(this._img))}})},15112:(t,e,i)=>{i.d(e,{P:()=>a});i(10994);var n=i(9672);class a{constructor(t){a[" "](t),this.type=t&&t.type||"default",this.key=t&&t.key,t&&"value"in t&&(this.value=t.value)}get value(){var t=this.type,e=this.key;if(t&&e)return a.types[t]&&a.types[t][e]}set value(t){var e=this.type,i=this.key;e&&i&&(e=a.types[e]=a.types[e]||{},null==t?delete e[i]:e[i]=t)}get list(){if(this.type){var t=a.types[this.type];return t?Object.keys(t).map((function(t){return o[this.type][t]}),this):[]}}byKey(t){return this.key=t,this.value}}a[" "]=function(){},a.types={};var o=a.types;(0,n.k)({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(t,e,i){var n=new a({type:t,key:e});return void 0!==i&&i!==n.value?n.value=i:this.value!==n.value&&(this.value=n.value),n},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(t){t&&(this.value=this)},byKey:function(t){return new a({type:this.type,key:t}).value}})},54444:(t,e,i)=>{i(10994);var n=i(9672),a=i(87156),o=i(50856);(0,n.k)({_template:o.d`
    <style>
      :host {
        display: block;
        position: absolute;
        outline: none;
        z-index: 1002;
        -moz-user-select: none;
        -ms-user-select: none;
        -webkit-user-select: none;
        user-select: none;
        cursor: default;
      }

      #tooltip {
        display: block;
        outline: none;
        @apply --paper-font-common-base;
        font-size: 10px;
        line-height: 1;
        background-color: var(--paper-tooltip-background, #616161);
        color: var(--paper-tooltip-text-color, white);
        padding: 8px;
        border-radius: 2px;
        @apply --paper-tooltip;
      }

      @keyframes keyFrameScaleUp {
        0% {
          transform: scale(0.0);
        }
        100% {
          transform: scale(1.0);
        }
      }

      @keyframes keyFrameScaleDown {
        0% {
          transform: scale(1.0);
        }
        100% {
          transform: scale(0.0);
        }
      }

      @keyframes keyFrameFadeInOpacity {
        0% {
          opacity: 0;
        }
        100% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameFadeOutOpacity {
        0% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        100% {
          opacity: 0;
        }
      }

      @keyframes keyFrameSlideDownIn {
        0% {
          transform: translateY(-2000px);
          opacity: 0;
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameSlideDownOut {
        0% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(-2000px);
          opacity: 0;
        }
      }

      .fade-in-animation {
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameFadeInOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .fade-out-animation {
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 0ms);
        animation-name: keyFrameFadeOutOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-up-animation {
        transform: scale(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameScaleUp;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-down-animation {
        transform: scale(1);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameScaleDown;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation {
        transform: translateY(-2000px);
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownIn;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.0, 0.0, 0.2, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation-out {
        transform: translateY(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownOut;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.4, 0.0, 1, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .cancel-animation {
        animation-delay: -30s !important;
      }

      /* Thanks IE 10. */

      .hidden {
        display: none !important;
      }
    </style>

    <div id="tooltip" class="hidden">
      <slot></slot>
    </div>
`,is:"paper-tooltip",hostAttributes:{role:"tooltip",tabindex:-1},properties:{for:{type:String,observer:"_findTarget"},manualMode:{type:Boolean,value:!1,observer:"_manualModeChanged"},position:{type:String,value:"bottom"},fitToVisibleBounds:{type:Boolean,value:!1},offset:{type:Number,value:14},marginTop:{type:Number,value:14},animationDelay:{type:Number,value:500,observer:"_delayChange"},animationEntry:{type:String,value:""},animationExit:{type:String,value:""},animationConfig:{type:Object,value:function(){return{entry:[{name:"fade-in-animation",node:this,timing:{delay:0}}],exit:[{name:"fade-out-animation",node:this}]}}},_showing:{type:Boolean,value:!1}},listeners:{webkitAnimationEnd:"_onAnimationEnd"},get target(){var t=(0,a.vz)(this).parentNode,e=(0,a.vz)(this).getOwnerRoot();return this.for?(0,a.vz)(e).querySelector("#"+this.for):t.nodeType==Node.DOCUMENT_FRAGMENT_NODE?e.host:t},attached:function(){this._findTarget()},detached:function(){this.manualMode||this._removeListeners()},playAnimation:function(t){"entry"===t?this.show():"exit"===t&&this.hide()},cancelAnimation:function(){this.$.tooltip.classList.add("cancel-animation")},show:function(){if(!this._showing){if(""===(0,a.vz)(this).textContent.trim()){for(var t=!0,e=(0,a.vz)(this).getEffectiveChildNodes(),i=0;i<e.length;i++)if(""!==e[i].textContent.trim()){t=!1;break}if(t)return}this._showing=!0,this.$.tooltip.classList.remove("hidden"),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.updatePosition(),this._animationPlaying=!0,this.$.tooltip.classList.add(this._getAnimationType("entry"))}},hide:function(){if(this._showing){if(this._animationPlaying)return this._showing=!1,void this._cancelAnimation();this._onAnimationFinish(),this._showing=!1,this._animationPlaying=!0}},updatePosition:function(){if(this._target&&this.offsetParent){var t=this.offset;14!=this.marginTop&&14==this.offset&&(t=this.marginTop);var e,i,n=this.offsetParent.getBoundingClientRect(),a=this._target.getBoundingClientRect(),o=this.getBoundingClientRect(),r=(a.width-o.width)/2,s=(a.height-o.height)/2,l=a.left-n.left,c=a.top-n.top;switch(this.position){case"top":e=l+r,i=c-o.height-t;break;case"bottom":e=l+r,i=c+a.height+t;break;case"left":e=l-o.width-t,i=c+s;break;case"right":e=l+a.width+t,i=c+s}this.fitToVisibleBounds?(n.left+e+o.width>window.innerWidth?(this.style.right="0px",this.style.left="auto"):(this.style.left=Math.max(0,e)+"px",this.style.right="auto"),n.top+i+o.height>window.innerHeight?(this.style.bottom=n.height-c+t+"px",this.style.top="auto"):(this.style.top=Math.max(-n.top,i)+"px",this.style.bottom="auto")):(this.style.left=e+"px",this.style.top=i+"px")}},_addListeners:function(){this._target&&(this.listen(this._target,"mouseenter","show"),this.listen(this._target,"focus","show"),this.listen(this._target,"mouseleave","hide"),this.listen(this._target,"blur","hide"),this.listen(this._target,"tap","hide")),this.listen(this.$.tooltip,"animationend","_onAnimationEnd"),this.listen(this,"mouseenter","hide")},_findTarget:function(){this.manualMode||this._removeListeners(),this._target=this.target,this.manualMode||this._addListeners()},_delayChange:function(t){500!==t&&this.updateStyles({"--paper-tooltip-delay-in":t+"ms"})},_manualModeChanged:function(){this.manualMode?this._removeListeners():this._addListeners()},_cancelAnimation:function(){this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add("hidden")},_onAnimationFinish:function(){this._showing&&(this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add(this._getAnimationType("exit")))},_onAnimationEnd:function(){this._animationPlaying=!1,this._showing||(this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.add("hidden"))},_getAnimationType:function(t){if("entry"===t&&""!==this.animationEntry)return this.animationEntry;if("exit"===t&&""!==this.animationExit)return this.animationExit;if(this.animationConfig[t]&&"string"==typeof this.animationConfig[t][0].name){if(this.animationConfig[t][0].timing&&this.animationConfig[t][0].timing.delay&&0!==this.animationConfig[t][0].timing.delay){var e=this.animationConfig[t][0].timing.delay;"entry"===t?this.updateStyles({"--paper-tooltip-delay-in":e+"ms"}):"exit"===t&&this.updateStyles({"--paper-tooltip-delay-out":e+"ms"})}return this.animationConfig[t][0].name}},_removeListeners:function(){this._target&&(this.unlisten(this._target,"mouseenter","show"),this.unlisten(this._target,"focus","show"),this.unlisten(this._target,"mouseleave","hide"),this.unlisten(this._target,"blur","hide"),this.unlisten(this._target,"tap","hide")),this.unlisten(this.$.tooltip,"animationend","_onAnimationEnd"),this.unlisten(this,"mouseenter","hide")}})},3239:(t,e,i)=>{function n(t){if(!t||"object"!=typeof t)return t;if("[object Date]"==Object.prototype.toString.call(t))return new Date(t.getTime());if(Array.isArray(t))return t.map(n);var e={};return Object.keys(t).forEach((function(i){e[i]=n(t[i])})),e}i.d(e,{Z:()=>n})},21560:(t,e,i)=>{i.d(e,{ZH:()=>d,MT:()=>o,U2:()=>l,RV:()=>a,t8:()=>c});const n=function(){if(!(!navigator.userAgentData&&/Safari\//.test(navigator.userAgent)&&!/Chrom(e|ium)\//.test(navigator.userAgent))||!indexedDB.databases)return Promise.resolve();let t;return new Promise((e=>{const i=()=>indexedDB.databases().finally(e);t=setInterval(i,100),i()})).finally((()=>clearInterval(t)))};function a(t){return new Promise(((e,i)=>{t.oncomplete=t.onsuccess=()=>e(t.result),t.onabort=t.onerror=()=>i(t.error)}))}function o(t,e){const i=n().then((()=>{const i=indexedDB.open(t);return i.onupgradeneeded=()=>i.result.createObjectStore(e),a(i)}));return(t,n)=>i.then((i=>n(i.transaction(e,t).objectStore(e))))}let r;function s(){return r||(r=o("keyval-store","keyval")),r}function l(t,e=s()){return e("readonly",(e=>a(e.get(t))))}function c(t,e,i=s()){return i("readwrite",(i=>(i.put(e,t),a(i.transaction))))}function d(t=s()){return t("readwrite",(t=>(t.clear(),a(t.transaction))))}},93217:(t,e,i)=>{i.d(e,{Ud:()=>p});const n=Symbol("Comlink.proxy"),a=Symbol("Comlink.endpoint"),o=Symbol("Comlink.releaseProxy"),r=Symbol("Comlink.thrown"),s=t=>"object"==typeof t&&null!==t||"function"==typeof t,l=new Map([["proxy",{canHandle:t=>s(t)&&t[n],serialize(t){const{port1:e,port2:i}=new MessageChannel;return c(t,e),[i,[i]]},deserialize:t=>(t.start(),p(t))}],["throw",{canHandle:t=>s(t)&&r in t,serialize({value:t}){let e;return e=t instanceof Error?{isError:!0,value:{message:t.message,name:t.name,stack:t.stack}}:{isError:!1,value:t},[e,[]]},deserialize(t){if(t.isError)throw Object.assign(new Error(t.value.message),t.value);throw t.value}}]]);function c(t,e=self){e.addEventListener("message",(function i(a){if(!a||!a.data)return;const{id:o,type:s,path:l}=Object.assign({path:[]},a.data),p=(a.data.argumentList||[]).map(g);let h;try{const e=l.slice(0,-1).reduce(((t,e)=>t[e]),t),i=l.reduce(((t,e)=>t[e]),t);switch(s){case"GET":h=i;break;case"SET":e[l.slice(-1)[0]]=g(a.data.value),h=!0;break;case"APPLY":h=i.apply(e,p);break;case"CONSTRUCT":h=function(t){return Object.assign(t,{[n]:!0})}(new i(...p));break;case"ENDPOINT":{const{port1:e,port2:i}=new MessageChannel;c(t,i),h=function(t,e){return f.set(t,e),t}(e,[e])}break;case"RELEASE":h=void 0;break;default:return}}catch(t){h={value:t,[r]:0}}Promise.resolve(h).catch((t=>({value:t,[r]:0}))).then((t=>{const[n,a]=y(t);e.postMessage(Object.assign(Object.assign({},n),{id:o}),a),"RELEASE"===s&&(e.removeEventListener("message",i),d(e))}))})),e.start&&e.start()}function d(t){(function(t){return"MessagePort"===t.constructor.name})(t)&&t.close()}function p(t,e){return m(t,[],e)}function h(t){if(t)throw new Error("Proxy has been released and is not useable")}function m(t,e=[],i=function(){}){let n=!1;const r=new Proxy(i,{get(i,a){if(h(n),a===o)return()=>_(t,{type:"RELEASE",path:e.map((t=>t.toString()))}).then((()=>{d(t),n=!0}));if("then"===a){if(0===e.length)return{then:()=>r};const i=_(t,{type:"GET",path:e.map((t=>t.toString()))}).then(g);return i.then.bind(i)}return m(t,[...e,a])},set(i,a,o){h(n);const[r,s]=y(o);return _(t,{type:"SET",path:[...e,a].map((t=>t.toString())),value:r},s).then(g)},apply(i,o,r){h(n);const s=e[e.length-1];if(s===a)return _(t,{type:"ENDPOINT"}).then(g);if("bind"===s)return m(t,e.slice(0,-1));const[l,c]=u(r);return _(t,{type:"APPLY",path:e.map((t=>t.toString())),argumentList:l},c).then(g)},construct(i,a){h(n);const[o,r]=u(a);return _(t,{type:"CONSTRUCT",path:e.map((t=>t.toString())),argumentList:o},r).then(g)}});return r}function u(t){const e=t.map(y);return[e.map((t=>t[0])),(i=e.map((t=>t[1])),Array.prototype.concat.apply([],i))];var i}const f=new WeakMap;function y(t){for(const[e,i]of l)if(i.canHandle(t)){const[n,a]=i.serialize(t);return[{type:"HANDLER",name:e,value:n},a]}return[{type:"RAW",value:t},f.get(t)||[]]}function g(t){switch(t.type){case"HANDLER":return l.get(t.name).deserialize(t.value);case"RAW":return t.value}}function _(t,e,i){return new Promise((n=>{const a=new Array(4).fill(0).map((()=>Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16))).join("-");t.addEventListener("message",(function e(i){i.data&&i.data.id&&i.data.id===a&&(t.removeEventListener("message",e),n(i.data))})),t.start&&t.start(),t.postMessage(Object.assign({id:a},e),i)}))}},19596:(t,e,i)=>{i.d(e,{sR:()=>p});var n=i(81563),a=i(38941);const o=(t,e)=>{var i,n;const a=t._$AN;if(void 0===a)return!1;for(const t of a)null===(n=(i=t)._$AO)||void 0===n||n.call(i,e,!1),o(t,e);return!0},r=t=>{let e,i;do{if(void 0===(e=t._$AM))break;i=e._$AN,i.delete(t),t=e}while(0===(null==i?void 0:i.size))},s=t=>{for(let e;e=t._$AM;t=e){let i=e._$AN;if(void 0===i)e._$AN=i=new Set;else if(i.has(t))break;i.add(t),d(e)}};function l(t){void 0!==this._$AN?(r(this),this._$AM=t,s(this)):this._$AM=t}function c(t,e=!1,i=0){const n=this._$AH,a=this._$AN;if(void 0!==a&&0!==a.size)if(e)if(Array.isArray(n))for(let t=i;t<n.length;t++)o(n[t],!1),r(n[t]);else null!=n&&(o(n,!1),r(n));else o(this,t)}const d=t=>{var e,i,n,o;t.type==a.pX.CHILD&&(null!==(e=(n=t)._$AP)&&void 0!==e||(n._$AP=c),null!==(i=(o=t)._$AQ)&&void 0!==i||(o._$AQ=l))};class p extends a.Xe{constructor(){super(...arguments),this._$AN=void 0}_$AT(t,e,i){super._$AT(t,e,i),s(this),this.isConnected=t._$AU}_$AO(t,e=!0){var i,n;t!==this.isConnected&&(this.isConnected=t,t?null===(i=this.reconnected)||void 0===i||i.call(this):null===(n=this.disconnected)||void 0===n||n.call(this)),e&&(o(this,t),r(this))}setValue(t){if((0,n.OR)(this._$Ct))this._$Ct._$AI(t,this);else{const e=[...this._$Ct._$AH];e[this._$Ci]=t,this._$Ct._$AI(e,this,0)}}disconnected(){}reconnected(){}}},81563:(t,e,i)=>{i.d(e,{E_:()=>f,i9:()=>m,_Y:()=>c,pt:()=>o,OR:()=>s,hN:()=>r,ws:()=>u,fk:()=>d,hl:()=>h});var n=i(15304);const{I:a}=n.Al,o=t=>null===t||"object"!=typeof t&&"function"!=typeof t,r=(t,e)=>void 0===e?void 0!==(null==t?void 0:t._$litType$):(null==t?void 0:t._$litType$)===e,s=t=>void 0===t.strings,l=()=>document.createComment(""),c=(t,e,i)=>{var n;const o=t._$AA.parentNode,r=void 0===e?t._$AB:e._$AA;if(void 0===i){const e=o.insertBefore(l(),r),n=o.insertBefore(l(),r);i=new a(e,n,t,t.options)}else{const e=i._$AB.nextSibling,a=i._$AM,s=a!==t;if(s){let e;null===(n=i._$AQ)||void 0===n||n.call(i,t),i._$AM=t,void 0!==i._$AP&&(e=t._$AU)!==a._$AU&&i._$AP(e)}if(e!==r||s){let t=i._$AA;for(;t!==e;){const e=t.nextSibling;o.insertBefore(t,r),t=e}}}return i},d=(t,e,i=t)=>(t._$AI(e,i),t),p={},h=(t,e=p)=>t._$AH=e,m=t=>t._$AH,u=t=>{var e;null===(e=t._$AP)||void 0===e||e.call(t,!1,!0);let i=t._$AA;const n=t._$AB.nextSibling;for(;i!==n;){const t=i.nextSibling;i.remove(),i=t}},f=t=>{t._$AR()}}}]);
//# sourceMappingURL=0276959b.js.map