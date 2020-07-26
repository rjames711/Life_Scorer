'use strict';
import LikeButton from './jsx_test.js';
import TaskList from './TaskList.js';
console.log('from wrapper');

class LikeButtonW extends React.Component {
  constructor(props) {
    super(props);
    this.state = { liked: false };
  }

  render() {

    return (
        <div>
           <TaskList/>
            <p>some added stuff</p>
        </div>
    );
  }
}

let domContainer = document.querySelector('#like_button_container');
ReactDOM.render(<LikeButtonW />, domContainer);