'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

import LikeButton from './jsx_test.js';
import TaskList from './TaskList.js';
console.log('from wrapper');

var LikeButtonW = function (_React$Component) {
  _inherits(LikeButtonW, _React$Component);

  function LikeButtonW(props) {
    _classCallCheck(this, LikeButtonW);

    var _this = _possibleConstructorReturn(this, (LikeButtonW.__proto__ || Object.getPrototypeOf(LikeButtonW)).call(this, props));

    _this.state = { liked: false };
    return _this;
  }

  _createClass(LikeButtonW, [{
    key: 'render',
    value: function render() {

      return React.createElement(
        'div',
        null,
        React.createElement(TaskList, null),
        React.createElement(
          'p',
          null,
          'some added stuff'
        )
      );
    }
  }]);

  return LikeButtonW;
}(React.Component);

var domContainer = document.querySelector('#like_button_container');
ReactDOM.render(React.createElement(LikeButtonW, null), domContainer);