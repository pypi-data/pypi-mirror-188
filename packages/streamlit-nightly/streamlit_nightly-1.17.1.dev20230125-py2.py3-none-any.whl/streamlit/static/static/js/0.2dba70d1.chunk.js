(this["webpackJsonpstreamlit-browser"]=this["webpackJsonpstreamlit-browser"]||[]).push([[0],{1135:function(e,t,r){"use strict";r.d(t,"g",(function(){return c})),r.d(t,"f",(function(){return u})),r.d(t,"e",(function(){return p})),r.d(t,"j",(function(){return f})),r.d(t,"d",(function(){return b})),r.d(t,"c",(function(){return y})),r.d(t,"h",(function(){return h})),r.d(t,"b",(function(){return g})),r.d(t,"i",(function(){return m})),r.d(t,"a",(function(){return v}));var o=r(33),n=r(63),i=r(408);function a(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);t&&(o=o.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,o)}return r}function l(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?a(Object(r),!0).forEach((function(t){s(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):a(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function s(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}var c=Object(o.a)("button",(function(e){var t,r=e.$theme,o=e.$size,i=e.$isFocusVisible,a=(t={},s(t,n.d.mini,r.sizing.scale400),s(t,n.d.compact,r.sizing.scale400),s(t,n.d.default,r.sizing.scale300),s(t,n.d.large,r.sizing.scale200),t)[o];return{display:"flex",alignItems:"center",borderTopStyle:"none",borderBottomStyle:"none",borderLeftStyle:"none",borderRightStyle:"none",background:"none",paddingLeft:a,paddingRight:a,outline:i?"solid 3px ".concat(r.colors.accent):"none",color:r.colors.contentPrimary}}));c.displayName="StyledMaskToggleButton",c.displayName="StyledMaskToggleButton";var u=Object(o.a)("div",(function(e){var t,r=e.$alignTop,o=void 0!==r&&r,i=e.$size,a=e.$theme,l=(t={},s(t,n.d.mini,a.sizing.scale200),s(t,n.d.compact,a.sizing.scale200),s(t,n.d.default,a.sizing.scale100),s(t,n.d.large,a.sizing.scale0),t)[i];return{display:"flex",alignItems:o?"flex-start":"center",paddingLeft:l,paddingRight:l,paddingTop:o?a.sizing.scale500:"0px",color:a.colors.contentPrimary}}));u.displayName="StyledClearIconContainer",u.displayName="StyledClearIconContainer";var p=Object(o.a)(i.a,(function(e){var t=e.$theme;return{cursor:"pointer",outline:e.$isFocusVisible?"solid 3px ".concat(t.colors.accent):"none"}}));function d(e,t){var r;return(r={},s(r,n.d.mini,t.font100),s(r,n.d.compact,t.font200),s(r,n.d.default,t.font300),s(r,n.d.large,t.font400),r)[e]}p.displayName="StyledClearIcon",p.displayName="StyledClearIcon";var f=function(e){var t=e.$isFocused,r=e.$adjoined,o=e.$error,i=e.$disabled,a=e.$positive,s=e.$size,c=e.$theme,u=e.$theme,p=u.borders,f=u.colors,b=u.sizing,y=u.typography,h=u.animation,g=e.$hasIconTrailing;return l(l(l(l({boxSizing:"border-box",display:"flex",overflow:"hidden",width:"100%",borderLeftWidth:"2px",borderRightWidth:"2px",borderTopWidth:"2px",borderBottomWidth:"2px",borderLeftStyle:"solid",borderRightStyle:"solid",borderTopStyle:"solid",borderBottomStyle:"solid",transitionProperty:"border",transitionDuration:h.timing200,transitionTimingFunction:h.easeOutCurve},function(e,t){var r=t.inputBorderRadius;return e===n.d.mini&&(r=t.inputBorderRadiusMini),{borderTopLeftRadius:r,borderBottomLeftRadius:r,borderTopRightRadius:r,borderBottomRightRadius:r}}(s,p)),d(s,y)),function(e,t,r){var o=arguments.length>3&&void 0!==arguments[3]&&arguments[3],n=arguments.length>4?arguments[4]:void 0;return e?{borderLeftColor:n.inputFillDisabled,borderRightColor:n.inputFillDisabled,borderTopColor:n.inputFillDisabled,borderBottomColor:n.inputFillDisabled,backgroundColor:n.inputFillDisabled}:t?{borderLeftColor:n.borderSelected,borderRightColor:n.borderSelected,borderTopColor:n.borderSelected,borderBottomColor:n.borderSelected,backgroundColor:n.inputFillActive}:r?{borderLeftColor:n.inputBorderError,borderRightColor:n.inputBorderError,borderTopColor:n.inputBorderError,borderBottomColor:n.inputBorderError,backgroundColor:n.inputFillError}:o?{borderLeftColor:n.inputBorderPositive,borderRightColor:n.inputBorderPositive,borderTopColor:n.inputBorderPositive,borderBottomColor:n.inputBorderPositive,backgroundColor:n.inputFillPositive}:{borderLeftColor:n.inputBorder,borderRightColor:n.inputBorder,borderTopColor:n.inputBorder,borderBottomColor:n.inputBorder,backgroundColor:n.inputFill}}(i,t,o,a,f)),function(e,t,r,o,i){var a=e===n.a.both||e===n.a.left&&"rtl"!==o||e===n.a.right&&"rtl"===o||i&&"rtl"===o,l=e===n.a.both||e===n.a.right&&"rtl"!==o||e===n.a.left&&"rtl"===o||i&&"rtl"!==o;return{paddingLeft:a?r.scale550:"0px",paddingRight:l?r.scale550:"0px"}}(r,0,b,c.direction,g))},b=Object(o.a)("div",f);b.displayName="Root",b.displayName="Root";var y=Object(o.a)("div",(function(e){var t=e.$size,r=e.$disabled,o=e.$isFocused,i=e.$error,a=e.$positive,c=e.$theme,u=c.colors,p=c.sizing,f=c.typography,b=c.animation;return l(l(l({display:"flex",alignItems:"center",justifyContent:"center",transitionProperty:"color, background-color",transitionDuration:b.timing200,transitionTimingFunction:b.easeOutCurve},d(t,f)),function(e,t){var r;return(r={},s(r,n.d.mini,{paddingRight:t.scale400,paddingLeft:t.scale400}),s(r,n.d.compact,{paddingRight:t.scale400,paddingLeft:t.scale400}),s(r,n.d.default,{paddingRight:t.scale300,paddingLeft:t.scale300}),s(r,n.d.large,{paddingRight:t.scale200,paddingLeft:t.scale200}),r)[e]}(t,p)),function(e,t,r,o,n){return e?{color:n.inputEnhancerTextDisabled,backgroundColor:n.inputFillDisabled}:t?{color:n.contentPrimary,backgroundColor:n.inputFillActive}:r?{color:n.contentPrimary,backgroundColor:n.inputFillError}:o?{color:n.contentPrimary,backgroundColor:n.inputFillPositive}:{color:n.contentPrimary,backgroundColor:n.inputFill}}(r,o,i,a,u))}));y.displayName="InputEnhancer",y.displayName="InputEnhancer";var h=function(e){var t=e.$isFocused,r=e.$error,o=e.$disabled,n=e.$positive,i=e.$size,a=e.$theme,s=a.colors,c=a.typography,u=a.animation;return l(l({display:"flex",width:"100%",transitionProperty:"background-color",transitionDuration:u.timing200,transitionTimingFunction:u.easeOutCurve},d(i,c)),function(e,t,r,o,n){return e?{color:n.inputTextDisabled,backgroundColor:n.inputFillDisabled}:t?{color:n.contentPrimary,backgroundColor:n.inputFillActive}:r?{color:n.contentPrimary,backgroundColor:n.inputFillError}:o?{color:n.contentPrimary,backgroundColor:n.inputFillPositive}:{color:n.contentPrimary,backgroundColor:n.inputFill}}(o,t,r,n,s))},g=Object(o.a)("div",h);g.displayName="InputContainer",g.displayName="InputContainer";var m=function(e){var t=e.$disabled,r=(e.$isFocused,e.$error,e.$size),o=e.$theme,i=o.colors,a=o.sizing;return l(l(l({boxSizing:"border-box",backgroundColor:"transparent",borderLeftWidth:0,borderRightWidth:0,borderTopWidth:0,borderBottomWidth:0,borderLeftStyle:"none",borderRightStyle:"none",borderTopStyle:"none",borderBottomStyle:"none",outline:"none",width:"100%",minWidth:0,maxWidth:"100%",cursor:t?"not-allowed":"text",margin:"0",paddingTop:"0",paddingBottom:"0",paddingLeft:"0",paddingRight:"0"},d(r,o.typography)),function(e,t){var r;return(r={},s(r,n.d.mini,{paddingTop:t.scale100,paddingBottom:t.scale100,paddingLeft:t.scale550,paddingRight:t.scale550}),s(r,n.d.compact,{paddingTop:t.scale200,paddingBottom:t.scale200,paddingLeft:t.scale550,paddingRight:t.scale550}),s(r,n.d.default,{paddingTop:t.scale400,paddingBottom:t.scale400,paddingLeft:t.scale550,paddingRight:t.scale550}),s(r,n.d.large,{paddingTop:t.scale550,paddingBottom:t.scale550,paddingLeft:t.scale550,paddingRight:t.scale550}),r)[e]}(r,a)),function(e,t,r,o){return e?{color:o.inputTextDisabled,"-webkit-text-fill-color":o.inputTextDisabled,caretColor:o.contentPrimary,"::placeholder":{color:o.inputPlaceholderDisabled}}:{color:o.contentPrimary,caretColor:o.contentPrimary,"::placeholder":{color:o.inputPlaceholder}}}(t,0,0,i))},v=Object(o.a)("input",m);v.displayName="Input",v.displayName="Input"},1197:function(e,t,r){"use strict";function o(e,t){var r=e.disabled,o=e.error,n=e.positive,i=e.adjoined,a=e.size,l=e.required,s=e.resize,c=e.readOnly;return{$isFocused:t.isFocused,$disabled:r,$error:o,$positive:n,$adjoined:i,$size:a,$required:l,$resize:s,$isReadOnly:c}}r.d(t,"a",(function(){return o}))},1254:function(e,t,r){"use strict";var o=r(0),n=r(22),i=r(63),a=r(1135),l=r(1197),s=r(33),c=r(138),u=["title","size","color","overrides"];function p(){return p=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var o in r)Object.prototype.hasOwnProperty.call(r,o)&&(e[o]=r[o])}return e},p.apply(this,arguments)}function d(e,t){if(null==e)return{};var r,o,n=function(e,t){if(null==e)return{};var r,o,n={},i=Object.keys(e);for(o=0;o<i.length;o++)r=i[o],t.indexOf(r)>=0||(n[r]=e[r]);return n}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(o=0;o<i.length;o++)r=i[o],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(n[r]=e[r])}return n}function f(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var r=null==e?null:"undefined"!==typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null==r)return;var o,n,i=[],a=!0,l=!1;try{for(r=r.call(e);!(a=(o=r.next()).done)&&(i.push(o.value),!t||i.length!==t);a=!0);}catch(s){l=!0,n=s}finally{try{a||null==r.return||r.return()}finally{if(l)throw n}}return i}(e,t)||function(e,t){if(!e)return;if("string"===typeof e)return b(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);"Object"===r&&e.constructor&&(r=e.constructor.name);if("Map"===r||"Set"===r)return Array.from(e);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return b(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function b(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,o=new Array(t);r<t;r++)o[r]=e[r];return o}function y(e,t){var r=f(Object(s.b)(),2)[1],i=e.title,a=void 0===i?"Hide":i,l=e.size,b=e.color,y=e.overrides,h=void 0===y?{}:y,g=d(e,u),m=Object(n.d)({component:r.icons&&r.icons.Hide?r.icons.Hide:null},h&&h.Svg?Object(n.f)(h.Svg):{});return o.createElement(c.a,p({viewBox:"0 0 20 20",ref:t,title:a,size:l,color:b,overrides:{Svg:m}},g),o.createElement("path",{d:"M12.81 4.36l-1.77 1.78a4 4 0 00-4.9 4.9l-2.76 2.75C2.06 12.79.96 11.49.2 10a11 11 0 0112.6-5.64zm3.8 1.85c1.33 1 2.43 2.3 3.2 3.79a11 11 0 01-12.62 5.64l1.77-1.78a4 4 0 004.9-4.9l2.76-2.75zm-.25-3.99l1.42 1.42L3.64 17.78l-1.42-1.42L16.36 2.22z"}))}var h=o.forwardRef(y),g=["title","size","color","overrides"];function m(){return m=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var o in r)Object.prototype.hasOwnProperty.call(r,o)&&(e[o]=r[o])}return e},m.apply(this,arguments)}function v(e,t){if(null==e)return{};var r,o,n=function(e,t){if(null==e)return{};var r,o,n={},i=Object.keys(e);for(o=0;o<i.length;o++)r=i[o],t.indexOf(r)>=0||(n[r]=e[r]);return n}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(o=0;o<i.length;o++)r=i[o],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(n[r]=e[r])}return n}function O(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var r=null==e?null:"undefined"!==typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null==r)return;var o,n,i=[],a=!0,l=!1;try{for(r=r.call(e);!(a=(o=r.next()).done)&&(i.push(o.value),!t||i.length!==t);a=!0);}catch(s){l=!0,n=s}finally{try{a||null==r.return||r.return()}finally{if(l)throw n}}return i}(e,t)||function(e,t){if(!e)return;if("string"===typeof e)return C(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);"Object"===r&&e.constructor&&(r=e.constructor.name);if("Map"===r||"Set"===r)return Array.from(e);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return C(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function C(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,o=new Array(t);r<t;r++)o[r]=e[r];return o}function j(e,t){var r=O(Object(s.b)(),2)[1],i=e.title,a=void 0===i?"Show":i,l=e.size,u=e.color,p=e.overrides,d=void 0===p?{}:p,f=v(e,g),b=Object(n.d)({component:r.icons&&r.icons.Show?r.icons.Show:null},d&&d.Svg?Object(n.f)(d.Svg):{});return o.createElement(c.a,m({viewBox:"0 0 20 20",ref:t,title:a,size:l,color:u,overrides:{Svg:b}},f),o.createElement("path",{d:"M.2 10a11 11 0 0119.6 0A11 11 0 01.2 10zm9.8 4a4 4 0 100-8 4 4 0 000 8zm0-2a2 2 0 110-4 2 2 0 010 4z"}))}var w=o.forwardRef(j);var F=r(53);function S(e){return S="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},S(e)}function k(){return k=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var o in r)Object.prototype.hasOwnProperty.call(r,o)&&(e[o]=r[o])}return e},k.apply(this,arguments)}function x(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var r=null==e?null:"undefined"!==typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null==r)return;var o,n,i=[],a=!0,l=!1;try{for(r=r.call(e);!(a=(o=r.next()).done)&&(i.push(o.value),!t||i.length!==t);a=!0);}catch(s){l=!0,n=s}finally{try{a||null==r.return||r.return()}finally{if(l)throw n}}return i}(e,t)||function(e,t){if(!e)return;if("string"===typeof e)return P(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);"Object"===r&&e.constructor&&(r=e.constructor.name);if("Map"===r||"Set"===r)return Array.from(e);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return P(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function P(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,o=new Array(t);r<t;r++)o[r]=e[r];return o}function T(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function R(e,t){for(var r=0;r<t.length;r++){var o=t[r];o.enumerable=o.enumerable||!1,o.configurable=!0,"value"in o&&(o.writable=!0),Object.defineProperty(e,o.key,o)}}function B(e,t){return B=Object.setPrototypeOf?Object.setPrototypeOf.bind():function(e,t){return e.__proto__=t,e},B(e,t)}function $(e){var t=function(){if("undefined"===typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"===typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,o=I(e);if(t){var n=I(this).constructor;r=Reflect.construct(o,arguments,n)}else r=o.apply(this,arguments);return E(this,r)}}function E(e,t){if(t&&("object"===S(t)||"function"===typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return z(e)}function z(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function I(e){return I=Object.setPrototypeOf?Object.getPrototypeOf.bind():function(e){return e.__proto__||Object.getPrototypeOf(e)},I(e)}function M(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}var L=function(){return null},D=function(e){!function(e,t){if("function"!==typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),Object.defineProperty(e,"prototype",{writable:!1}),t&&B(e,t)}(u,e);var t,r,s,c=$(u);function u(){var e;T(this,u);for(var t=arguments.length,r=new Array(t),n=0;n<t;n++)r[n]=arguments[n];return M(z(e=c.call.apply(c,[this].concat(r))),"inputRef",e.props.inputRef||o.createRef()),M(z(e),"state",{isFocused:e.props.autoFocus||!1,isMasked:"password"===e.props.type,initialType:e.props.type,isFocusVisibleForClear:!1,isFocusVisibleForMaskToggle:!1}),M(z(e),"onInputKeyDown",(function(t){e.props.clearOnEscape&&"Escape"===t.key&&e.inputRef.current&&!e.props.readOnly&&(e.clearValue(),t.stopPropagation())})),M(z(e),"onClearIconClick",(function(){e.inputRef.current&&e.clearValue(),e.inputRef.current&&e.inputRef.current.focus()})),M(z(e),"onFocus",(function(t){e.setState({isFocused:!0}),e.props.onFocus(t)})),M(z(e),"onBlur",(function(t){e.setState({isFocused:!1}),e.props.onBlur(t)})),M(z(e),"handleFocusForMaskToggle",(function(t){Object(F.d)(t)&&e.setState({isFocusVisibleForMaskToggle:!0})})),M(z(e),"handleBlurForMaskToggle",(function(t){!1!==e.state.isFocusVisibleForMaskToggle&&e.setState({isFocusVisibleForMaskToggle:!1})})),M(z(e),"handleFocusForClear",(function(t){Object(F.d)(t)&&e.setState({isFocusVisibleForClear:!0})})),M(z(e),"handleBlurForClear",(function(t){!1!==e.state.isFocusVisibleForClear&&e.setState({isFocusVisibleForClear:!1})})),e}return t=u,(r=[{key:"componentDidMount",value:function(){var e=this.props,t=e.autoFocus,r=e.clearable;this.inputRef.current&&(t&&this.inputRef.current.focus(),r&&this.inputRef.current.addEventListener("keydown",this.onInputKeyDown))}},{key:"componentWillUnmount",value:function(){this.props.clearable&&this.inputRef.current&&this.inputRef.current.removeEventListener("keydown",this.onInputKeyDown)}},{key:"clearValue",value:function(){var e=this.inputRef.current;if(e){var t=Object.getOwnPropertyDescriptor(this.props.type===i.b.textarea?HTMLTextAreaElement.prototype:HTMLInputElement.prototype,"value");if(t){var r=t.set;if(r){r.call(e,"");var o=function(e){var t;return"function"===typeof window.Event?t=new window.Event(e,{bubbles:!0,cancelable:!0}):(t=document.createEvent("Event")).initEvent(e,!0,!0),t}("input");e.dispatchEvent(o)}}}}},{key:"getInputType",value:function(){return"password"===this.props.type?this.state.isMasked?"password":"text":this.props.type}},{key:"renderMaskToggle",value:function(){var e,t=this;if("password"!==this.props.type)return null;var r=x(Object(n.c)(this.props.overrides.MaskToggleButton,a.g),2),l=r[0],s=r[1],c=x(Object(n.c)(this.props.overrides.MaskToggleShowIcon,w),2),u=c[0],p=c[1],d=x(Object(n.c)(this.props.overrides.MaskToggleHideIcon,h),2),f=d[0],b=d[1],y=this.state.isMasked?"Show password text":"Hide password text",g=(e={},M(e,i.d.mini,"12px"),M(e,i.d.compact,"16px"),M(e,i.d.default,"20px"),M(e,i.d.large,"24px"),e)[this.props.size];return o.createElement(l,k({$size:this.props.size,$isFocusVisible:this.state.isFocusVisibleForMaskToggle,"aria-label":y,onClick:function(){return t.setState((function(e){return{isMasked:!e.isMasked}}))},title:y,type:"button"},s,{onFocus:Object(F.b)(s,this.handleFocusForMaskToggle),onBlur:Object(F.a)(s,this.handleBlurForMaskToggle)}),this.state.isMasked?o.createElement(u,k({size:g,title:y},p)):o.createElement(f,k({size:g,title:y},b)))}},{key:"renderClear",value:function(){var e,t=this,r=this.props,s=r.clearable,c=r.value,u=r.disabled,p=r.readOnly,d=r.overrides,f=void 0===d?{}:d;if(u||p||!s||null==c||"string"===typeof c&&0===c.length)return null;var b=x(Object(n.c)(f.ClearIconContainer,a.f),2),y=b[0],h=b[1],g=x(Object(n.c)(f.ClearIcon,a.e),2),m=g[0],v=g[1],O="Clear value",C=Object(l.a)(this.props,this.state),j=(e={},M(e,i.d.mini,"14px"),M(e,i.d.compact,"14px"),M(e,i.d.default,"16px"),M(e,i.d.large,"22px"),e)[this.props.size];return o.createElement(y,k({$alignTop:this.props.type===i.b.textarea},C,h),o.createElement(m,k({size:j,tabIndex:0,title:O,"aria-label":O,onClick:this.onClearIconClick,onKeyDown:function(e){!e.key||"Enter"!==e.key&&" "!==e.key||(e.preventDefault(),t.onClearIconClick())},role:"button",$isFocusVisible:this.state.isFocusVisibleForClear},C,v,{onFocus:Object(F.b)(v,this.handleFocusForClear),onBlur:Object(F.a)(v,this.handleBlurForClear)})))}},{key:"render",value:function(){var e=this.props.overrides,t=e.InputContainer,r=e.Input,s=e.Before,c=e.After,p="password"===this.state.initialType&&this.props.autoComplete===u.defaultProps.autoComplete?"new-password":this.props.autoComplete,d=Object(l.a)(this.props,this.state),f=x(Object(n.c)(t,a.b),2),b=f[0],y=f[1],h=x(Object(n.c)(r,a.a),2),g=h[0],m=h[1],v=x(Object(n.c)(s,L),2),O=v[0],C=v[1],j=x(Object(n.c)(c,L),2),w=j[0],F=j[1];return o.createElement(b,k({"data-baseweb":this.props["data-baseweb"]||"base-input"},d,y),o.createElement(O,k({},d,C)),o.createElement(g,k({ref:this.inputRef,"aria-activedescendant":this.props["aria-activedescendant"],"aria-autocomplete":this.props["aria-autocomplete"],"aria-controls":this.props["aria-controls"],"aria-errormessage":this.props["aria-errormessage"],"aria-haspopup":this.props["aria-haspopup"],"aria-label":this.props["aria-label"],"aria-labelledby":this.props["aria-labelledby"],"aria-describedby":this.props["aria-describedby"],"aria-invalid":this.props.error,"aria-required":this.props.required,autoComplete:p,disabled:this.props.disabled,readOnly:this.props.readOnly,id:this.props.id,inputMode:this.props.inputMode,maxLength:this.props.maxLength,name:this.props.name,onBlur:this.onBlur,onChange:this.props.onChange,onFocus:this.onFocus,onKeyDown:this.props.onKeyDown,onKeyPress:this.props.onKeyPress,onKeyUp:this.props.onKeyUp,pattern:this.props.pattern,placeholder:this.props.placeholder,type:this.getInputType(),required:this.props.required,role:this.props.role,value:this.props.value,min:this.props.min,max:this.props.max,step:this.props.step,rows:this.props.type===i.b.textarea?this.props.rows:null},d,m)),this.renderClear(),this.renderMaskToggle(),o.createElement(w,k({},d,F)))}}])&&R(t.prototype,r),s&&R(t,s),Object.defineProperty(t,"prototype",{writable:!1}),u}(o.Component);M(D,"defaultProps",{"aria-activedescendant":null,"aria-autocomplete":null,"aria-controls":null,"aria-errormessage":null,"aria-haspopup":null,"aria-label":null,"aria-labelledby":null,"aria-describedby":null,adjoined:i.a.none,autoComplete:"on",autoFocus:!1,disabled:!1,error:!1,positive:!1,name:"",inputMode:"text",onBlur:function(){},onChange:function(){},onKeyDown:function(){},onKeyPress:function(){},onKeyUp:function(){},onFocus:function(){},onClear:function(){},clearable:!1,clearOnEscape:!0,overrides:{},pattern:null,placeholder:"",required:!1,role:null,size:i.d.default,type:"text",readOnly:!1});t.a=D}}]);