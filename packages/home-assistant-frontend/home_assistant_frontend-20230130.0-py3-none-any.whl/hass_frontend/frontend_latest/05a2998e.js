"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[22844],{50842:(e,t,i)=>{i.d(t,{n:()=>s});var r=i(47181);const a=()=>Promise.all([i.e(85084),i.e(51882),i.e(77576),i.e(68101),i.e(33894)]).then(i.bind(i,4454)),s=(e,t)=>{(0,r.B)(e,"show-dialog",{dialogTag:"dialog-aliases",dialogImport:a,dialogParams:t})}},22844:(e,t,i)=>{i.r(t);i(51187),i(24103);var r=i(37500),a=i(36924),s=i(47181),n=i(85415),o=(i(9381),i(34821)),l=(i(59005),i(3555),i(50842)),c=i(11654);function d(){d=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var a=t.placement;if(t.kind===r&&("static"===a||"prototype"===a)){var s="static"===a?e:i;this.defineClassElement(s,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],a={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,a)}),this),e.forEach((function(e){if(!p(e))return i.push(e);var t=this.decorateElement(e,a);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var s=this.decorateConstructor(i,t);return r.push.apply(r,s.finishers),s.finishers=r,s},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],a=e.decorators,s=a.length-1;s>=0;s--){var n=t[e.placement];n.splice(n.indexOf(e.key),1);var o=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,a[s])(o)||o);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var a=this.fromClassDescriptor(e),s=this.toClassDescriptor((0,t[r])(a)||a);if(void 0!==s.finisher&&i.push(s.finisher),void 0!==s.elements){e=s.elements;for(var n=0;n<e.length-1;n++)for(var o=n+1;o<e.length;o++)if(e[n].key===e[o].key&&e[n].placement===e[o].placement)throw new TypeError("Duplicated element ("+e[n].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return v(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?v(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=y(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var a=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var s={kind:t,key:i,placement:r,descriptor:Object.assign({},a)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(a,"get","The property descriptor of a field descriptor"),this.disallowProperty(a,"set","The property descriptor of a field descriptor"),this.disallowProperty(a,"value","The property descriptor of a field descriptor"),s.initializer=e.initializer),s},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:m(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=m(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function h(e){var t,i=y(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function u(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function p(e){return e.decorators&&e.decorators.length}function f(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function m(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function y(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function v(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}const g={round:!1,type:"image/jpeg",quality:.75,aspectRatio:1.78};let k=function(e,t,i,r){var a=d();if(r)for(var s=0;s<r.length;s++)a=r[s](a);var n=t((function(e){a.initializeInstanceElements(e,o.elements)}),i),o=a.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===s.key&&e.placement===s.placement},r=0;r<e.length;r++){var a,s=e[r];if("method"===s.kind&&(a=t.find(i)))if(f(s.descriptor)||f(a.descriptor)){if(p(s)||p(a))throw new ReferenceError("Duplicated methods ("+s.key+") can't be decorated.");a.descriptor=s.descriptor}else{if(p(s)){if(p(a))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+s.key+").");a.decorators=s.decorators}u(s,a)}else t.push(s)}return t}(n.d.map(h)),e);return a.initializeClassElements(n.F,o.elements),a.runClassFinishers(n.F,o.finishers)}(null,(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.SB)()],key:"_name",value:void 0},{kind:"field",decorators:[(0,a.SB)()],key:"_aliases",value:void 0},{kind:"field",decorators:[(0,a.SB)()],key:"_picture",value:void 0},{kind:"field",decorators:[(0,a.SB)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,a.SB)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,a.SB)()],key:"_submitting",value:void 0},{kind:"method",key:"showDialog",value:async function(e){var t;this._params=e,this._error=void 0,this._name=this._params.entry?this._params.entry.name:"",this._aliases=this._params.entry?this._params.entry.aliases:[],this._picture=(null===(t=this._params.entry)||void 0===t?void 0:t.picture)||null,await this.updateComplete}},{kind:"method",key:"closeDialog",value:function(){this._error="",this._params=void 0,(0,s.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){if(!this._params)return r.dy``;const e=this._params.entry,t=!this._isNameValid();return r.dy`
      <ha-dialog
        open
        @closed=${this.closeDialog}
        .heading=${(0,o.i)(this.hass,e?e.name:this.hass.localize("ui.panel.config.areas.editor.default_name"))}
      >
        <div>
          ${this._error?r.dy`<ha-alert alert-type="error">${this._error}</ha-alert>`:""}
          <div class="form">
            ${e?r.dy`
                  <div>
                    ${this.hass.localize("ui.panel.config.areas.editor.area_id")}:
                    ${e.area_id}
                  </div>
                `:""}

            <ha-textfield
              .value=${this._name}
              @input=${this._nameChanged}
              .label=${this.hass.localize("ui.panel.config.areas.editor.name")}
              .errorMessage=${this.hass.localize("ui.panel.config.areas.editor.name_required")}
              .invalid=${t}
              dialogInitialFocus
            ></ha-textfield>

            <div class="label">
              ${this.hass.localize("ui.panel.config.areas.editor.aliases_section")}
            </div>
            <mwc-list class="aliases" @action=${this._handleAliasesClicked}>
              <mwc-list-item .twoline=${this._aliases.length>0} hasMeta>
                <span>
                  ${this._aliases.length>0?this.hass.localize("ui.panel.config.areas.editor.configured_aliases",{count:this._aliases.length}):this.hass.localize("ui.panel.config.areas.editor.no_aliases")}
                </span>
                <span slot="secondary">
                  ${[...this._aliases].sort(((e,t)=>(0,n.$)(e,t,this.hass.locale.language))).join(", ")}
                </span>
                <ha-svg-icon slot="meta" .path=${"M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z"}></ha-svg-icon>
              </mwc-list-item>
            </mwc-list>
            <div class="secondary">
              ${this.hass.localize("ui.panel.config.areas.editor.aliases_description")}
            </div>

            <ha-picture-upload
              .hass=${this.hass}
              .value=${this._picture}
              crop
              .cropOptions=${g}
              @change=${this._pictureChanged}
            ></ha-picture-upload>
          </div>
        </div>
        ${e?r.dy`
              <mwc-button
                slot="secondaryAction"
                class="warning"
                @click=${this._deleteEntry}
                .disabled=${this._submitting}
              >
                ${this.hass.localize("ui.panel.config.areas.editor.delete")}
              </mwc-button>
            `:r.dy``}
        <mwc-button
          slot="primaryAction"
          @click=${this._updateEntry}
          .disabled=${t||this._submitting}
        >
          ${e?this.hass.localize("ui.panel.config.areas.editor.update"):this.hass.localize("ui.panel.config.areas.editor.create")}
        </mwc-button>
      </ha-dialog>
    `}},{kind:"method",key:"_handleAliasesClicked",value:function(){(0,l.n)(this,{name:this._name,aliases:this._aliases,updateAliases:async e=>{this._aliases=e}})}},{kind:"method",key:"_isNameValid",value:function(){return""!==this._name.trim()}},{kind:"method",key:"_nameChanged",value:function(e){this._error=void 0,this._name=e.target.value}},{kind:"method",key:"_pictureChanged",value:function(e){this._error=void 0,this._picture=e.target.value}},{kind:"method",key:"_updateEntry",value:async function(){this._submitting=!0;try{const e={name:this._name.trim(),picture:this._picture,aliases:this._aliases};this._params.entry?await this._params.updateEntry(e):await this._params.createEntry(e),this.closeDialog()}catch(e){this._error=e.message||this.hass.localize("ui.panel.config.areas.editor.unknown_error")}finally{this._submitting=!1}}},{kind:"method",key:"_deleteEntry",value:async function(){this._submitting=!0;try{await this._params.removeEntry()&&this.closeDialog()}finally{this._submitting=!1}}},{kind:"get",static:!0,key:"styles",value:function(){return[c.yu,r.iv`
        ha-textfield {
          display: block;
          margin-bottom: 16px;
        }
      `]}}]}}),r.oi);customElements.define("dialog-area-registry-detail",k)}}]);
//# sourceMappingURL=05a2998e.js.map