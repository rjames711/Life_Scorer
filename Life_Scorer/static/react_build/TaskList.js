'use strict';
/*
import React, { Component } from 'react';
import axios from 'axios'

import { Link, IndexLink } from 'react-router-dom'
*/

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

import AttrControl from './AttrControl.js';

var TaskList = function (_React$Component) {
    _inherits(TaskList, _React$Component);

    function TaskList() {
        var _ref;

        var _temp, _this, _ret;

        _classCallCheck(this, TaskList);

        for (var _len = arguments.length, args = Array(_len), _key = 0; _key < _len; _key++) {
            args[_key] = arguments[_key];
        }

        return _ret = (_temp = (_this = _possibleConstructorReturn(this, (_ref = TaskList.__proto__ || Object.getPrototypeOf(TaskList)).call.apply(_ref, [this].concat(args))), _this), _this.state = {
            tasks: [],
            select: '',
            name: ''
        }, _this.filterButtons = function () {
            var newlist = _this.state.initialTasks.filter(function (s) {
                return s.name.toLowerCase().indexOf(_this.state.select.toLowerCase()) !== -1 ? true : false;
            });
            _this.setState({
                name: _this.state.select,
                tasks: newlist
            });
        }, _this.handleSubmit = function (e) {
            return e.preventDefault();
        }, _this.clearButton = function (e) {
            return _this.setState({ select: '' }, function () {
                return _this.filterButtons();
            });
        }, _this.selectButton = function (e) {
            var select = _this.state.initialTasks.filter(function (t) {
                return t.name === e.target.innerText;
            });
            _this.setState({ select: e.target.innerText, tasks: select });
        }, _this.handleChange = function (e) {
            return _this.setState({ select: e.target.value }, function () {
                return _this.filterButtons();
            });
        }, _temp), _possibleConstructorReturn(_this, _ret);
    }

    _createClass(TaskList, [{
        key: 'componentDidMount',
        value: function componentDidMount() {
            var _this2 = this;

            var token = "552894b8-9f7d-11e9-afdf-1ed13a9a6117";
            axios.get('http://singlepoint.space:5000/api/tasks').then(function (res) {
                _this2.setState({
                    tasks: res.data,
                    initialTasks: res.data
                });
            });
        }
    }, {
        key: 'render',
        value: function render() {
            var _this3 = this;

            var buttons = this.state.tasks.map(function (t) {
                return React.createElement(
                    'button',
                    { data: t, onClick: _this3.selectButton },
                    ' ',
                    t.name,
                    ' '
                );
            });
            var attrControls = null;
            var note = null;
            var submit = null;
            if (this.state.tasks.length === 1) {
                attrControls = [];
                var task = this.state.tasks[0];
                var attrs = task.attributes;
                buttons.push(React.createElement(
                    'a',
                    { id: 'edit', href: "/edit/" + task.name },
                    React.createElement(
                        'button',
                        null,
                        'Edit-->'
                    )
                ));
                for (var key in attrs) {
                    attrControls.push(React.createElement(AttrControl, { attr: attrs[key], attrname: key }));
                }
                note = React.createElement('textarea', { name: 'note', id: 'note', placeholder: 'Enter notes here' });
                submit = React.createElement(
                    'button',
                    null,
                    'Submit'
                );
            }

            return React.createElement(
                'div',
                { className: 'app-content' },
                React.createElement('br', null),
                React.createElement(
                    'form',
                    { onSubmit: this.handleSubmit },
                    React.createElement(
                        'div',
                        { className: 'inline' },
                        React.createElement('input', { type: 'text', id: 'selection', className: 'perc75', autoComplete: 'off',
                            onChange: this.handleChange, value: this.state.select }),
                        React.createElement(
                            'button',
                            { className: 'perc25', onClick: this.clearButton },
                            'Clear'
                        )
                    )
                ),
                React.createElement(
                    'div',
                    { className: 'taskbuttons' },
                    buttons
                ),
                React.createElement(
                    'div',
                    null,
                    attrControls,
                    note
                ),
                submit
            );
        }
    }]);

    return TaskList;
}(React.Component);

export default TaskList;