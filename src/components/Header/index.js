import React from 'react';
import { slide as Menu } from 'react-burger-menu'
import './header.css';

class Example extends React.Component {

  render () {
    return (
      <Menu right wdith={'25%'}>
        <a id="home" className="menu-item" href="/">Home</a>
        <a id="blog" className="menu-item" href="/blog">Paper summaries</a>
      </Menu>
    );
  }
}

export default Example;