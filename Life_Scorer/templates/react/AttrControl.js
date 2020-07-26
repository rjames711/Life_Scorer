//import React, { Component } from 'react';

class AttrControl extends React.Component {
  componentDidMount() {
    this.setState({
      attrname: this.props.attrname,
      attr: this.props.attr,
      numin:parseFloat(this.props.attr.default)
    });
  }
  state = {}
  
  minusFine = () => this.setState({ numin: (this.state.numin - parseFloat(this.state.attr['min'])) })
  minusCoarse = () => this.setState({ numin: (this.state.numin - parseFloat(this.state.attr['max'])) })
  plusFine = () => this.setState({ numin: (this.state.numin + parseFloat(this.state.attr['min'])) })
  plusCoarse = () => this.setState({ numin: (this.state.numin + parseFloat(this.state.attr['max'])) })
  render() {
    return (
      <div>
        <label htmlFor='test'>{this.state.attrname}</label>
        <br/>
        <button onClick={this.minusCoarse}>--</button>
        <button onClick={this.minusFine}>-</button>
        <input type="number" value={this.state.numin} />
        <button onClick={this.plusFine}>+</button>
        <button onClick={this.plusCoarse}>++</button>
      </div>
    );
  }
}

export default AttrControl