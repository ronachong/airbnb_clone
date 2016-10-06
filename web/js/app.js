console.log("loading app root")

import React from 'react';
import ReactDom from 'react-dom';

import Header from './components/Header.js';
import LeftColumn from './components/LeftColumn.js';

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
        <LeftColumn />
      </div>
    )
  }
});

ReactDom.render(<Site />, document.getElementById('app'));
