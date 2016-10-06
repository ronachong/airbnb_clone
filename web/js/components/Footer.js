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
    textAlign: 'center'
  },
  logo: {
    height: '60px'
  },
  span: {
    width: '50vw'
  }
}

const Footer = (props)=> (
  <footer style={styles.footer}>
    <p>Under construction.</p>
  </footer>
);

export default Footer;
