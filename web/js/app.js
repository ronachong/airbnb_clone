console.log("loading app root")

import React from 'react';
import ReactDom from 'react-dom';

import Header from './components/Header.js';
import LeftColumn from './components/LeftColumn.js';
import Content from './components/Content.js';

const styles = {
  sitebody: {
    width: '100%',
    display: 'flex',
    flexDirection: 'row',
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
        <div style={styles.sitebody}>
          <LeftColumn />
          <Content />
        </div>
      </div>
    )
  }
});

ReactDom.render(<Site />, document.getElementById('app'));
