(this["webpackJsonpstreamlit-browser"]=this["webpackJsonpstreamlit-browser"]||[]).push([[39],{1631:function(e,t,o){"use strict";o.r(t),o.d(t,"default",(function(){return d}));var i=o(2),n=o(3),r=o(6),a=o(7),l=o(0),u=o.n(l),s=o(223),m=o(193),p=o(43),c=o(1),f=function(e){Object(r.a)(o,e);var t=Object(a.a)(o);function o(){var e;Object(i.a)(this,o);for(var n=arguments.length,r=new Array(n),a=0;a<n;a++)r[a]=arguments[a];return(e=t.call.apply(t,[this].concat(r))).formClearHelper=new s.b,e.state={value:e.initialValue},e.commitWidgetValue=function(t){e.props.widgetMgr.setStringValue(e.props.element,e.state.value,t)},e.onFormCleared=function(){e.setState((function(e,t){return{value:t.element.default}}),(function(){return e.commitWidgetValue({fromUi:!0})}))},e.onColorClose=function(t){e.setState({value:t},(function(){return e.commitWidgetValue({fromUi:!0})}))},e}return Object(n.a)(o,[{key:"initialValue",get:function(){var e=this.props.widgetMgr.getStringValue(this.props.element);return void 0!==e?e:this.props.element.default}},{key:"componentDidMount",value:function(){this.props.element.setValue?this.updateFromProtobuf():this.commitWidgetValue({fromUi:!1})}},{key:"componentDidUpdate",value:function(){this.maybeUpdateFromProtobuf()}},{key:"componentWillUnmount",value:function(){this.formClearHelper.disconnect()}},{key:"maybeUpdateFromProtobuf",value:function(){this.props.element.setValue&&this.updateFromProtobuf()}},{key:"updateFromProtobuf",value:function(){var e=this,t=this.props.element.value;this.props.element.setValue=!1,this.setState({value:t},(function(){e.commitWidgetValue({fromUi:!1})}))}},{key:"render",value:function(){var e,t=this.props,o=t.element,i=t.width,n=t.disabled,r=t.widgetMgr,a=this.state.value;return this.formClearHelper.manageFormClearListener(r,o.formId,this.onFormCleared),Object(c.jsx)(m.a,{label:o.label,labelVisibility:Object(p.l)(null===(e=o.labelVisibility)||void 0===e?void 0:e.value),help:o.help,onChange:this.onColorClose,disabled:n,width:i,value:a})}}]),o}(u.a.PureComponent),d=f}}]);