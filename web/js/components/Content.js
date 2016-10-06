import React from 'react';

console.log("loading content");

/*
Content: (js/Components/Content.js) (will be used after)
will be the mosaic of all places
*/

const styles = {
  leftcol: {
    borderStyle: 'solid'
  }
}

var Content = React.createClass({
  getInitialState: function() {
    return {
      //
    }
  },
  render: function () {
    return (
      <section style={styles.leftcol}>
        <p>Temp text.</p>
      </section>
    )
  }
});

export default Content;
