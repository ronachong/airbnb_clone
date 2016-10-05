console.log("loading app root")

import React from 'react';
import ReactDom from 'react-dom';

import Header from './components/header.js';

const styles = {
  header: {
    height: '60px',
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-between'
    //flexWrap: 'nowrap'
  }
}

var Site = React.createClass({
  getInitialState: function() {
    return {
      title: 'fairbnb'
    }
  },
  render: function () {
    return (
      <div>
        <Header />
      </div>
    )
  }
});

ReactDom.render(<Site />, document.getElementById('app'));
