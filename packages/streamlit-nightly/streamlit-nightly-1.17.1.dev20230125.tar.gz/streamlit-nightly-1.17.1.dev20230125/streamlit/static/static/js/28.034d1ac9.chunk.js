(this["webpackJsonpstreamlit-browser"]=this["webpackJsonpstreamlit-browser"]||[]).push([[28],{1612:function(e,t,a){"use strict";a.r(t),a.d(t,"default",(function(){return A}));var n=a(20),r=a(14),o=a.n(r),i=a(65),s=a(2),l=a(3),c=a(6),d=a(7),u=a(0),g=a(75),h=a(1285),b=a(1094),p=a(1222),f=a(27),m=a(224),v=a(102),w=a(141),y=a(5),x=a(54),O=a(30);function j(e,t){var a={font:t.genericFonts.bodyFont,background:t.colors.bgColor,fieldTitle:"verbal",autosize:{type:"fit",contains:"padding"},title:{align:"left",anchor:"start",color:t.colors.headingColor,titleFontStyle:"normal",fontWeight:t.fontWeights.bold,fontSize:t.fontSizes.smPx+2,orient:"top",offset:26},axis:{labelFontSize:t.fontSizes.twoSmPx,labelFontWeight:t.fontWeights.normal,labelColor:Object(O.getGray70)(t),labelFontStyle:"normal",titleFontWeight:t.fontWeights.normal,titleFontSize:t.fontSizes.smPx,titleColor:Object(O.getGray70)(t),titleFontStyle:"normal",ticks:!1,gridColor:Object(O.getGray30)(t),domain:!1,domainWidth:1,domainColor:Object(O.getGray30)(t),labelFlush:!0,labelFlushOffset:1,labelBound:!1,labelLimit:100,titlePadding:t.spacing.lgPx,labelPadding:t.spacing.lgPx,labelSeparation:t.spacing.twoXSPx,labelOverlap:!0},legend:{labelFontSize:t.fontSizes.smPx,labelFontWeight:t.fontWeights.normal,labelColor:Object(O.getGray70)(t),titleFontSize:t.fontSizes.smPx,titleFontWeight:t.fontWeights.normal,titleFontStyle:"normal",titleColor:Object(O.getGray70)(t),titlePadding:t.spacing.mdPx,labelPadding:t.spacing.lgPx,columnPadding:t.spacing.smPx,rowPadding:t.spacing.twoXSPx,padding:7,symbolStrokeWidth:4},range:{category:Object(O.getCategoricalColorsArray)(t),diverging:Object(O.getDivergingColorsArray)(t),ramp:Object(O.getSequentialColorsArray)(t),heatmap:Object(O.getSequentialColorsArray)(t)},view:{columns:1,strokeWidth:0,stroke:"transparent",continuousHeight:350,continuousWidth:400},concat:{columns:1},facet:{columns:1},mark:Object(y.a)({tooltip:!0},Object(O.hasLightBackgroundColor)(t)?{color:"#0068C9"}:{color:"#83C9FF"}),bar:{binSpacing:t.spacing.twoXSPx,discreteBandSize:{band:.85}},axisDiscrete:{grid:!1},axisXPoint:{grid:!1},axisTemporal:{grid:!1},axisXBand:{grid:!1}};return e?Object(x.mergeWith)({},a,e,(function(e,t){return Object(x.isArray)(t)?t:void 0})):a}function S(e,t){var a=t.colors,n=t.fontSizes,r=t.genericFonts,o={labelFont:r.bodyFont,titleFont:r.bodyFont,labelFontSize:n.twoSmPx,titleFontSize:n.twoSmPx},i={background:a.bgColor,axis:Object(y.a)({labelColor:a.bodyText,titleColor:a.bodyText,gridColor:Object(O.getGray30)(t)},o),legend:Object(y.a)({labelColor:a.bodyText,titleColor:a.bodyText},o),title:Object(y.a)({color:a.bodyText,subtitleColor:a.bodyText},o),header:{labelColor:a.bodyText},view:{continuousHeight:350,continuousWidth:400},mark:{tooltip:!0}};return e?Object(x.merge)({},i,e):i}var C=a(12),F=Object(C.a)("div",{target:"everg990"})((function(e){var t=e.theme;return{"&.vega-embed":{"&:hover summary, .vega-embed:focus summary":{background:"transparent"},"&.has-actions":{paddingRight:0},".vega-actions":{zIndex:t.zIndices.popupMenu,backgroundColor:t.colors.bgColor,boxShadow:"rgb(0 0 0 / 16%) 0px 4px 16px",border:"1px solid ".concat(t.colors.fadedText10),a:{fontFamily:t.genericFonts.bodyFont,fontWeight:t.fontWeights.normal,fontSize:t.fontSizes.md,margin:0,padding:"".concat(t.spacing.twoXS," ").concat(t.spacing.twoXL),color:t.colors.bodyText},"a:hover":{backgroundColor:t.colors.secondaryBg,color:t.colors.bodyText},":before":{content:"none"},":after":{content:"none"}},summary:{opacity:0,height:"auto",zIndex:t.zIndices.menuButton,border:"none",boxShadow:"none",borderRadius:t.radii.md,color:t.colors.fadedText10,backgroundColor:"transparent",transition:"opacity 300ms 150ms,transform 300ms 150ms","&:active, &:focus-visible, &:hover":{border:"none",boxShadow:"none",color:t.colors.bodyText,opacity:"1 !important",background:t.colors.darkenedBgMix25}}}}}),""),k=a(1),z="(index)",V="source",P=new Set([w.a.DatetimeIndex,w.a.Float64Index,w.a.Int64Index,w.a.RangeIndex,w.a.UInt64Index]),D=function(e){Object(c.a)(a,e);var t=Object(d.a)(a);function a(){var e;Object(s.a)(this,a);for(var n=arguments.length,r=new Array(n),o=0;o<n;o++)r[o]=arguments[o];return(e=t.call.apply(t,[this].concat(r))).vegaView=void 0,e.vegaFinalizer=void 0,e.defaultDataName=V,e.element=null,e.state={error:void 0},e.finalizeView=function(){e.vegaFinalizer&&e.vegaFinalizer(),e.vegaFinalizer=void 0,e.vegaView=void 0},e.generateSpec=function(){var t,a,n=e.props,r=n.element,o=n.theme,i=JSON.parse(r.spec),s=r.useContainerWidth;if("streamlit"===r.vegaLiteTheme?i.config=j(i.config,o):"streamlit"===(null===(t=i.usermeta)||void 0===t||null===(a=t.embedOptions)||void 0===a?void 0:a.theme)?(i.config=j(i.config,o),i.usermeta.embedOptions.theme=void 0):i.config=S(i.config,o),e.props.height?(i.width=e.props.width,i.height=e.props.height):s&&(i.width=e.props.width),i.padding||(i.padding={}),null==i.padding.bottom&&(i.padding.bottom=20),i.datasets)throw new Error("Datasets should not be passed as part of the spec");return i},e}return Object(l.a)(a,[{key:"componentDidMount",value:function(){var e=Object(i.a)(o.a.mark((function e(){var t;return o.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,this.createView();case 3:e.next=9;break;case 5:e.prev=5,e.t0=e.catch(0),t=Object(v.a)(e.t0),this.setState({error:t});case 9:case"end":return e.stop()}}),e,this,[[0,5]])})));return function(){return e.apply(this,arguments)}}()},{key:"componentWillUnmount",value:function(){this.finalizeView()}},{key:"componentDidUpdate",value:function(){var e=Object(i.a)(o.a.mark((function e(t){var a,r,i,s,l,c,d,u,g,h,b,p,m,w,y,x,O,j,S,C,F,k;return o.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(a=t.element,r=t.theme,i=this.props,s=i.element,l=i.theme,c=a.spec,d=s.spec,this.vegaView&&c===d&&r===l&&t.width===this.props.width&&t.height===this.props.height&&t.element.vegaLiteTheme===this.props.element.vegaLiteTheme){e.next=16;break}return Object(f.c)("Vega spec changed."),e.prev=6,e.next=9,this.createView();case 9:e.next=15;break;case 11:e.prev=11,e.t0=e.catch(6),u=Object(v.a)(e.t0),this.setState({error:u});case 15:return e.abrupt("return");case 16:for(g=a.data,h=s.data,(g||h)&&this.updateData(this.defaultDataName,g,h),b=I(a)||{},p=I(s)||{},m=0,w=Object.entries(p);m<w.length;m++)y=Object(n.a)(w[m],2),x=y[0],O=y[1],j=x||this.defaultDataName,S=b[j],this.updateData(j,S,O);for(C=0,F=Object.keys(b);C<F.length;C++)k=F[C],p.hasOwnProperty(k)||k===this.defaultDataName||this.updateData(k,null,null);this.vegaView.resize().runAsync();case 24:case"end":return e.stop()}}),e,this,[[6,11]])})));return function(t){return e.apply(this,arguments)}}()},{key:"updateData",value:function(e,t,a){if(!this.vegaView)throw new Error("Chart has not been drawn yet");if(a&&0!==a.data.numRows)if(t&&0!==t.data.numRows){var n=t.dimensions,r=n.dataRows,o=n.dataColumns,i=a.dimensions,s=i.dataRows;if(function(e,t,a,n,r,o){if(a!==o)return!1;if(t>=r)return!1;if(0===t)return!1;var i=o-1,s=t-1;if(e.getDataValue(0,i)!==n.getDataValue(0,i)||e.getDataValue(s,i)!==n.getDataValue(s,i))return!1;return!0}(t,r,o,a,s,i.dataColumns))r<s&&this.vegaView.insert(e,N(a,r));else{var l=b.changeset().remove(b.truthy).insert(N(a));this.vegaView.change(e,l),Object(f.c)("Had to clear the ".concat(e," dataset before inserting data through Vega view."))}}else this.vegaView.insert(e,N(a));else this.vegaView._runtime.data.hasOwnProperty(e)&&this.vegaView.remove(e,b.truthy)}},{key:"createView",value:function(){var e=Object(i.a)(o.a.mark((function e(){var t,a,r,i,s,l,c,d,u,g,b,m,v,w,y,x,O;return o.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(Object(f.c)("Creating a new Vega view."),this.element){e.next=3;break}throw Error("Element missing.");case 3:return this.finalizeView(),t=this.props.element,a=this.generateSpec(),r={defaultStyle:!0,ast:!0,expr:p.a},e.next=9,Object(h.a)(this.element,a,r);case 9:if(i=e.sent,s=i.vgSpec,l=i.view,c=i.finalize,this.vegaView=l,this.vegaFinalizer=c,d=T(t),1===(u=d?Object.keys(d):[]).length?(g=Object(n.a)(u,1),b=g[0],this.defaultDataName=b):0===u.length&&s.data&&(this.defaultDataName=V),(m=W(t))&&l.insert(this.defaultDataName,m),d)for(v=0,w=Object.entries(d);v<w.length;v++)y=Object(n.a)(w[v],2),x=y[0],O=y[1],l.insert(x,O);return e.next=23,l.runAsync();case 23:this.vegaView.resize().runAsync();case 24:case"end":return e.stop()}}),e,this)})));return function(){return e.apply(this,arguments)}}()},{key:"render",value:function(){var e=this;if(this.state.error)throw this.state.error;return Object(k.jsx)(F,{"data-testid":"stArrowVegaLiteChart",ref:function(t){e.element=t}})}}]),a}(u.PureComponent);function W(e){var t=e.data;return t&&0!==t.data.numRows?N(t):null}function T(e){var t=I(e);if(null==t)return null;for(var a={},r=0,o=Object.entries(t);r<o.length;r++){var i=Object(n.a)(o[r],2),s=i[0],l=i[1];a[s]=N(l)}return a}function I(e){var t;if(0===(null===(t=e.datasets)||void 0===t?void 0:t.length))return null;var a={};return e.datasets.forEach((function(e){if(e){var t=e.hasName?e.name:null;a[t]=e.data}})),a}function N(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:0;if(e.isEmpty())return[];for(var a=[],n=e.dimensions,r=n.dataRows,o=n.dataColumns,i=w.b.getTypeName(e.types.index[0]),s=P.has(i),l=t;l<r;l++){var c={};if(s){var d=e.getIndexValue(l,0);c[z]="bigint"===typeof d?Number(d):d}for(var u=0;u<o;u++){var g=e.getDataValue(l,u);c[e.columns[0][u]]="bigint"===typeof g?Number(g):g}a.push(c)}return a}var A=Object(g.d)(Object(m.a)(D))}}]);