'use strict';
console.log('from jsx compile edit2');
class LikeButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { liked: false };
  }

  render() {
    if (this.state.liked) {
      return 'You liked this.';
    }

    return (
      <div>
      <button onClick={() => this.setState({ liked: true }) }>
        Like
      </button>
      <button onClick={() => this.setState({ liked: true }) }>
        Like
      </button>
      </div>
    );
  }
}

export default LikeButton