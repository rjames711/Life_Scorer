var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

//import React, { Component } from 'react';

var AttrControl = function (_React$Component) {
  _inherits(AttrControl, _React$Component);

  function AttrControl() {
    var _ref;

    var _temp, _this, _ret;

    _classCallCheck(this, AttrControl);

    for (var _len = arguments.length, args = Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }

    return _ret = (_temp = (_this = _possibleConstructorReturn(this, (_ref = AttrControl.__proto__ || Object.getPrototypeOf(AttrControl)).call.apply(_ref, [this].concat(args))), _this), _this.state = {}, _this.minusFine = function () {
      return _this.setState({ numin: _this.state.numin - parseFloat(_this.state.attr['min']) });
    }, _this.minusCoarse = function () {
      return _this.setState({ numin: _this.state.numin - parseFloat(_this.state.attr['max']) });
    }, _this.plusFine = function () {
      return _this.setState({ numin: _this.state.numin + parseFloat(_this.state.attr['min']) });
    }, _this.plusCoarse = function () {
      return _this.setState({ numin: _this.state.numin + parseFloat(_this.state.attr['max']) });
    }, _temp), _possibleConstructorReturn(_this, _ret);
  }

  _createClass(AttrControl, [{
    key: 'componentDidMount',
    value: function componentDidMount() {
      this.setState({
        attrname: this.props.attrname,
        attr: this.props.attr,
        numin: parseFloat(this.props.attr.default)
      });
    }
  }, {
    key: 'render',
    value: function render() {
      return React.createElement(
        'div',
        null,
        React.createElement(
          'label',
          { htmlFor: 'test' },
          this.state.attrname
        ),
        React.createElement('br', null),
        React.createElement(
          'button',
          { onClick: this.minusCoarse },
          '--'
        ),
        React.createElement(
          'button',
          { onClick: this.minusFine },
          '-'
        ),
        React.createElement('input', { type: 'number', value: this.state.numin }),
        React.createElement(
          'button',
          { onClick: this.plusFine },
          '+'
        ),
        React.createElement(
          'button',
          { onClick: this.plusCoarse },
          '++'
        )
      );
    }
  }]);

  return AttrControl;
}(React.Component);

export default AttrControl;