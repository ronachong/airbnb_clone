import React from 'react';

console.log("loading footer");

/*
Footer: (js/Components/Footer.js)
height: 40px
fixed in the bottom
*/

const styles = {
  footer: {
    height: '40px',
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

const Footer = (props)=> (
  <header style={styles.footer}>
    <p>Under construction.</p>
  </header>
);

export default Footer;
