import React from 'react';

console.log("loading left column");

/*
Left column: (js/Components/LeftColumn.js)
will be the filter section to find a place in AirBnB
width: 300px
*/

const styles = {
  leftcol: {
    width: '300px',
    borderStyle: 'solid'
  }
}

var LeftColumn = React.createClass({
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

export default LeftColumn;
