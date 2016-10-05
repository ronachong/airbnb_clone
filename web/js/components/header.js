import React from 'react';

console.log("loading header");

/*
height: 60px
logo on the left
div with a width of 200px of the right (will be used after)
*/

const styles = {
  header: {
    height: '60px',
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-between'
    //flexWrap: 'nowrap'
  },
  logo: {
    height: '60px'
  },
  span: {
    width: '50vw'
  }
}

const Header = (props)=> (
  <header style={styles.header}>
    <img
      style={styles.logo}
      src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Airbnb_Logo_B%C3%A9lo.svg/2000px-Airbnb_Logo_B%C3%A9lo.svg.png" />
    <span style={styles.span}>This is on the right.</span>
  </header>
);

export default Header;
