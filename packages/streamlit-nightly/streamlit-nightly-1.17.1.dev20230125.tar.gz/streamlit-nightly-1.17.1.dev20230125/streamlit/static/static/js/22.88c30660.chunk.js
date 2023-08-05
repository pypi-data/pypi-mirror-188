(this["webpackJsonpstreamlit-browser"]=this["webpackJsonpstreamlit-browser"]||[]).push([[22],{1166:function(e,t,r){"use strict";r.d(t,"b",(function(){return f})),r.d(t,"a",(function(){return n}));var n,o=r(0),a=r.n(o),i=r(75),s=r(74),c=r(30),u=r(1347),l=r(22),d=r(1);!function(e){e.EXTRASMALL="xs",e.SMALL="sm",e.MEDIUM="md",e.LARGE="lg",e.EXTRALARGE="xl"}(n||(n={}));var f=function(e){var t=e.value,r=e.width,o=e.size,f=void 0===o?n.SMALL:o,p=e.overrides,b=Object(i.g)(),g={xs:b.spacing.twoXS,sm:b.spacing.sm,md:b.spacing.lg,lg:b.spacing.xl,xl:b.spacing.twoXL},m=a.a.useContext(s.a).activeTheme,y=!Object(c.isPresetTheme)(m),h={BarContainer:{style:{marginTop:b.spacing.none,marginBottom:b.spacing.none,marginRight:b.spacing.none,marginLeft:b.spacing.none}},Bar:{style:function(e){var t=e.$theme;return{width:r?r.toString():void 0,marginTop:b.spacing.none,marginBottom:b.spacing.none,marginRight:b.spacing.none,marginLeft:b.spacing.none,height:g[f],backgroundColor:t.colors.progressbarTrackFill,borderTopLeftRadius:b.spacing.twoXS,borderTopRightRadius:b.spacing.twoXS,borderBottomLeftRadius:b.spacing.twoXS,borderBottomRightRadius:b.spacing.twoXS}}},BarProgress:{style:function(e){e.$theme;return{backgroundColor:y?b.colors.primary:b.colors.blue70,borderTopLeftRadius:b.spacing.twoXS,borderTopRightRadius:b.spacing.twoXS,borderBottomLeftRadius:b.spacing.twoXS,borderBottomRightRadius:b.spacing.twoXS}}}};return Object(d.jsx)(u.a,{value:t,overrides:Object(l.e)(h,p)})}},1347:function(e,t,r){"use strict";var n,o=r(0),a=r.n(o),i=r(22),s="small",c="medium",u="large",l=r(33),d=r(94);function f(){return f=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var n in r)Object.prototype.hasOwnProperty.call(r,n)&&(e[n]=r[n])}return e},f.apply(this,arguments)}function p(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function b(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?p(Object(r),!0).forEach((function(t){g(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):p(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function g(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function m(e){var t;return(t={},g(t,s,"2px"),g(t,c,"4px"),g(t,u,"8px"),t)[e]}var y=Object(l.a)("div",(function(e){return{width:"100%"}}));y.displayName="StyledRoot",y.displayName="StyledRoot";var h=Object(l.a)("div",(function(e){var t=e.$theme.sizing;return{display:"flex",marginLeft:t.scale500,marginRight:t.scale500,marginTop:t.scale500,marginBottom:t.scale500}}));h.displayName="StyledBarContainer",h.displayName="StyledBarContainer";var v=Object(l.a)("div",(function(e){var t=e.$theme,r=e.$size,n=e.$steps,o=t.colors,a=t.sizing,i=t.borders.useRoundedCorners?a.scale0:0;return b({borderTopLeftRadius:i,borderTopRightRadius:i,borderBottomRightRadius:i,borderBottomLeftRadius:i,backgroundColor:Object(d.b)(o.progressbarTrackFill,"0.16"),height:m(r),flex:1,overflow:"hidden"},n<2?{}:{marginLeft:a.scale300,":first-child":{marginLeft:"0"}})}));v.displayName="StyledBar",v.displayName="StyledBar";var O=Object(l.a)("div",(function(e){var t=e.$theme,r=e.$value,n=e.$successValue,o=e.$steps,a=e.$index,i=e.$maxValue,s=e.$minValue,c=void 0===s?0:s,u=i||n,l=t.colors,d=t.sizing,f=t.borders,p="".concat(100-100*(r-c)/(u-c),"%"),g="awaits",m="inProgress",y="completed",h="default";if(o>1){var v=(u-c)/o,O=(r-c)/(u-c)*100,j=Math.floor(O/v);h=a<j?y:a===j?m:g}var w=f.useRoundedCorners?d.scale0:0,R={transform:"translateX(-".concat(p,")")},P=h===m?{animationDuration:"2.1s",animationIterationCount:"infinite",animationTimingFunction:t.animation.linearCurve,animationName:{"0%":{transform:"translateX(-102%)",opacity:1},"50%":{transform:"translateX(0%)",opacity:1},"100%":{transform:"translateX(0%)",opacity:0}}}:h===y?{transform:"translateX(0%)"}:{transform:"translateX(-102%)"};return b({borderTopLeftRadius:w,borderTopRightRadius:w,borderBottomRightRadius:w,borderBottomLeftRadius:w,backgroundColor:l.accent,height:"100%",width:"100%",transform:"translateX(-102%)",transition:"transform 0.5s"},o>1?P:R)}));O.displayName="StyledBarProgress",O.displayName="StyledBarProgress";var j=Object(l.a)("div",(function(e){var t=e.$theme,r=e.$isLeft,n=void 0!==r&&r,o=e.$size,a=void 0===o?c:o,i=t.colors,s=t.sizing,u=t.borders.useRoundedCorners?s.scale0:0,l=m(a),d={display:"inline-block",flex:1,marginLeft:"auto",marginRight:"auto",transitionProperty:"background-position",animationDuration:"1.5s",animationIterationCount:"infinite",animationTimingFunction:t.animation.linearCurve,backgroundSize:"300% auto",backgroundRepeat:"no-repeat",backgroundPositionX:n?"-50%":"150%",backgroundImage:"linear-gradient(".concat(n?"90":"270","deg, transparent 0%, ").concat(i.accent," 25%, ").concat(i.accent," 75%, transparent 100%)"),animationName:n?{"0%":{backgroundPositionX:"-50%"},"33%":{backgroundPositionX:"50%"},"66%":{backgroundPositionX:"50%"},"100%":{backgroundPositionX:"150%"}}:{"0%":{backgroundPositionX:"150%"},"33%":{backgroundPositionX:"50%"},"66%":{backgroundPositionX:"50%"},"100%":{backgroundPositionX:"-50%"}}};return b(b({},n?{borderTopLeftRadius:u,borderBottomLeftRadius:u}:{borderTopRightRadius:u,borderBottomRightRadius:u}),{},{height:l},d)}));j.displayName="StyledInfiniteBar",j.displayName="StyledInfiniteBar";var w=Object(l.a)("div",(function(e){return b(b({textAlign:"center"},e.$theme.typography.font150),{},{color:e.$theme.colors.contentTertiary})}));w.displayName="StyledLabel",w.displayName="StyledLabel";var R=(g(n={},u,{d:"M47.5 4H71.5529C82.2933 4 91 12.9543 91 24C91 35.0457 82.2933 44 71.5529 44H23.4471C12.7067 44 4 35.0457 4 24C4 12.9543 12.7067 4 23.4471 4H47.5195",width:95,height:48,strokeWidth:8,typography:"LabelLarge"}),g(n,c,{d:"M39 2H60.5833C69.0977 2 76 9.16344 76 18C76 26.8366 69.0977 34 60.5833 34H17.4167C8.90228 34 2 26.8366 2 18C2 9.16344 8.90228 2 17.4167 2H39.0195",width:78,height:36,strokeWidth:4,typography:"LabelMedium"}),g(n,s,{d:"M32 1H51.6271C57.9082 1 63 6.37258 63 13C63 19.6274 57.9082 25 51.6271 25H12.3729C6.09181 25 1 19.6274 1 13C1 6.37258 6.09181 1 12.3729 1H32.0195",width:64,height:26,strokeWidth:2,typography:"LabelSmall"}),n),P=Object(l.a)("div",(function(e){var t=e.$size,r=e.$inline;return{width:R[t].width+"px",height:R[t].height+"px",position:"relative",display:r?"inline-flex":"flex",alignItems:"center",justifyContent:"center"}}));P.displayName="StyledProgressBarRoundedRoot",P.displayName="StyledProgressBarRoundedRoot";var S=Object(l.a)("svg",(function(e){var t=e.$size;return{width:R[t].width+"px",height:R[t].height+"px",position:"absolute",fill:"none"}}));S.displayName="_StyledProgressBarRoundedSvg",S.displayName="_StyledProgressBarRoundedSvg";Object(l.d)(S,(function(e){return function(t){return a.a.createElement(e,f({viewBox:"0 0 ".concat(R[t.$size].width," ").concat(R[t.$size].height),xmlns:"http://www.w3.org/2000/svg"},t))}}));var $=Object(l.a)("path",(function(e){var t=e.$theme,r=e.$size;return{stroke:t.colors.backgroundTertiary,strokeWidth:R[r].strokeWidth+"px"}}));$.displayName="_StyledProgressBarRoundedTrackBackground",$.displayName="_StyledProgressBarRoundedTrackBackground";Object(l.d)($,(function(e){return function(t){return a.a.createElement(e,f({d:R[t.$size].d},t))}}));var k=Object(l.a)("path",(function(e){var t=e.$theme,r=e.$size,n=e.$visible,o=e.$pathLength,a=e.$pathProgress;return{visibility:n?"visible":"hidden",stroke:t.colors.borderAccent,strokeWidth:R[r].strokeWidth+"px",strokeDasharray:o,strokeDashoffset:o*(1-a)+""}}));k.displayName="_StyledProgressBarRoundedTrackForeground",k.displayName="_StyledProgressBarRoundedTrackForeground";Object(l.d)(k,(function(e){return function(t){return a.a.createElement(e,f({d:R[t.$size].d},t))}}));var x=Object(l.a)("div",(function(e){var t=e.$theme,r=e.$size;return b({color:t.colors.contentPrimary},t.typography[R[r].typography])}));function B(e){return B="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},B(e)}x.displayName="StyledProgressBarRoundedText",x.displayName="StyledProgressBarRoundedText";var L=["overrides","getProgressLabel","value","size","steps","successValue","minValue","maxValue","showLabel","infinite","errorMessage","forwardedRef"];function T(){return T=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var n in r)Object.prototype.hasOwnProperty.call(r,n)&&(e[n]=r[n])}return e},T.apply(this,arguments)}function C(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var r=null==e?null:"undefined"!==typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null==r)return;var n,o,a=[],i=!0,s=!1;try{for(r=r.call(e);!(i=(n=r.next()).done)&&(a.push(n.value),!t||a.length!==t);i=!0);}catch(c){s=!0,o=c}finally{try{i||null==r.return||r.return()}finally{if(s)throw o}}return a}(e,t)||function(e,t){if(!e)return;if("string"===typeof e)return X(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);"Object"===r&&e.constructor&&(r=e.constructor.name);if("Map"===r||"Set"===r)return Array.from(e);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return X(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function X(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function N(e,t){if(null==e)return{};var r,n,o=function(e,t){if(null==e)return{};var r,n,o={},a=Object.keys(e);for(n=0;n<a.length;n++)r=a[n],t.indexOf(r)>=0||(o[r]=e[r]);return o}(e,t);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(n=0;n<a.length;n++)r=a[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(o[r]=e[r])}return o}function z(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function E(e,t){for(var r=0;r<t.length;r++){var n=t[r];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(e,n.key,n)}}function M(e,t){return M=Object.setPrototypeOf?Object.setPrototypeOf.bind():function(e,t){return e.__proto__=t,e},M(e,t)}function A(e){var t=function(){if("undefined"===typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"===typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,n=_(e);if(t){var o=_(this).constructor;r=Reflect.construct(n,arguments,o)}else r=n.apply(this,arguments);return V(this,r)}}function V(e,t){if(t&&("object"===B(t)||"function"===typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e)}function _(e){return _=Object.setPrototypeOf?Object.getPrototypeOf.bind():function(e){return e.__proto__||Object.getPrototypeOf(e)},_(e)}var H,I,D,F=function(e){!function(e,t){if("function"!==typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),Object.defineProperty(e,"prototype",{writable:!1}),t&&M(e,t)}(s,e);var t,r,n,a=A(s);function s(){return z(this,s),a.apply(this,arguments)}return t=s,(r=[{key:"componentDidMount",value:function(){}},{key:"render",value:function(){var e=this.props,t=e.overrides,r=void 0===t?{}:t,n=e.getProgressLabel,a=e.value,s=e.size,c=e.steps,u=e.successValue,l=e.minValue,d=e.maxValue,f=e.showLabel,p=e.infinite,b=e.errorMessage,g=e.forwardedRef,m=N(e,L),R=this.props["aria-label"]||this.props.ariaLabel,P=100!==d?d:u,S=C(Object(i.c)(r.Root,y),2),$=S[0],k=S[1],x=C(Object(i.c)(r.BarContainer,h),2),B=x[0],X=x[1],z=C(Object(i.c)(r.Bar,v),2),E=z[0],M=z[1],A=C(Object(i.c)(r.BarProgress,O),2),V=A[0],_=A[1],H=C(Object(i.c)(r.Label,w),2),I=H[0],D=H[1],F=C(Object(i.c)(r.InfiniteBar,j),2),W=F[0],G=F[1],J={$infinite:p,$size:s,$steps:c,$successValue:P,$minValue:l,$maxValue:P,$value:a};return o.createElement($,T({ref:g,"data-baseweb":"progress-bar",role:"progressbar","aria-label":R||n(a,P,l),"aria-valuenow":p?null:a,"aria-valuemin":p?null:l,"aria-valuemax":p?null:P,"aria-invalid":!!b||null,"aria-errormessage":b},m,J,k),o.createElement(B,T({},J,X),p?o.createElement(o.Fragment,null,o.createElement(W,T({$isLeft:!0,$size:J.$size},G)),o.createElement(W,T({$size:J.$size},G))):function(){for(var e=[],t=0;t<c;t++)e.push(o.createElement(E,T({key:t},J,M),o.createElement(V,T({$index:t},J,_))));return e}()),f&&o.createElement(I,T({},J,D),n(a,P,l)))}}])&&E(t.prototype,r),n&&E(t,n),Object.defineProperty(t,"prototype",{writable:!1}),s}(o.Component);D={getProgressLabel:function(e,t,r){return"".concat(Math.round((e-r)/(t-r)*100),"% Loaded")},infinite:!1,overrides:{},showLabel:!1,size:c,steps:1,successValue:100,minValue:0,maxValue:100,value:0},(I="defaultProps")in(H=F)?Object.defineProperty(H,I,{value:D,enumerable:!0,configurable:!0,writable:!0}):H[I]=D;var W=o.forwardRef((function(e,t){return o.createElement(F,T({forwardedRef:t},e))}));W.displayName="ProgressBar";t.a=W},1619:function(e,t,r){"use strict";r.r(t),r.d(t,"default",(function(){return u}));r(0);var n=r(1166),o=r(12),a=r(30),i=Object(o.a)("div",{target:"edb2rvg0"})((function(e){var t=e.theme;return{paddingBottom:t.spacing.smPx,lineHeight:t.lineHeights.normal,color:Object(a.getGray90)(t)}}),""),s=r(66),c=r(1);var u=function(e){var t=e.element,r=e.width;return Object(c.jsxs)("div",{className:"stProgress",children:[Object(c.jsx)(i,{children:Object(c.jsx)(s.a,{source:t.text,allowHTML:!1,isLabel:!0})}),Object(c.jsx)(n.b,{value:t.value,width:r})]})}}}]);