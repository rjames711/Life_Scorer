'use strict';
/*
import React, { Component } from 'react';
import axios from 'axios'

import { Link, IndexLink } from 'react-router-dom'
*/
import AttrControl from './AttrControl.js';

class TaskList extends React.Component {
    componentDidMount() {
        let token = "552894b8-9f7d-11e9-afdf-1ed13a9a6117";
        axios.get(`http://singlepoint.space:5000/api/tasks`)
            .then(res => {
                this.setState({
                    tasks: res.data,
                    initialTasks: res.data
                })
            })
    }

    state = {
        tasks: [],
        select: '',
        name: ''
    }

    filterButtons = () => {
        var newlist = this.state.initialTasks.filter((s) => s.name.toLowerCase().indexOf(this.state.select.toLowerCase()) !== -1 ? true : false);
        this.setState({
            name: this.state.select,
            tasks: newlist
        })
    }

    handleSubmit = (e) => e.preventDefault();
    clearButton = (e) => this.setState({ select: '' }, () => this.filterButtons());
    selectButton = (e) => {
        let select = this.state.initialTasks.filter((t) => t.name === e.target.innerText);
        this.setState({ select: e.target.innerText, tasks: select });
    }
    handleChange = (e) => this.setState({ select: e.target.value }, () => this.filterButtons());

    render() {
        let buttons = this.state.tasks.map((t) => <button data={t} onClick={this.selectButton} > {t.name} </button>);
        let attrControls = null;
        let note=null;
        let submit = null;
        if (this.state.tasks.length === 1) {
            attrControls = []
            let task = this.state.tasks[0];
            let attrs = task.attributes;
            buttons.push( <a id='edit' href={"/edit/" + task.name}><button>Edit--></button></a> )
            for (var key in attrs) {
                attrControls.push(<AttrControl attr={attrs[key]} attrname={key}/>);
            }
            note=<textarea name="note" id="note" placeholder="Enter notes here" ></textarea>
            submit=<button>Submit</button>
        }

        return (
            
            <div className="app-content">
            <br/>
                <form onSubmit={this.handleSubmit}>
                    <div className="inline">
                    <input type="text" id="selection" className="perc75" autoComplete="off"
                    onChange={this.handleChange} value={this.state.select} />
                    <button className="perc25" onClick={this.clearButton} >Clear</button>
                    </div>
                </form>
                <div className="taskbuttons">
                {buttons}
                </div>
                <div>
                 {attrControls}
                {note}
                </div>
                {submit}
            </div>
           
        )
    }
}

export default TaskList;
