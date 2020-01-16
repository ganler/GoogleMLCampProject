import React, { Component } from 'react'
import 'antd/dist/antd.css'
import 'tachyons/css/tachyons.css'
import '../static/css/style.css'
import { hydrate, css } from 'react-emotion' // eslint-disable-line

import Header from './header'

if (typeof window !== 'undefined') {
  hydrate(window.__NEXT_DATA__.ids)
}

class Layout extends Component {
  constructor () {
    super()
    this.handleScroll = this.handleScroll.bind(this)
  }
  handleScroll (e) {
    if (this.props.onScroll) {
      this.props.onScroll({
        offset: e.target.scrollTop
      })
    }
  }
  render () {
    let { children } = this.props
    return (
      <div
        className='relative vh-100 overflow-y-scroll bg-near-black avenir'
        css={`
          -webkit-overflow-scrolling: touch;
          z-index: 0;
        `}
        onScroll={this.handleScroll}
      >
        <Header />
        { children }
      </div>
    )
  }
}

export default Layout
