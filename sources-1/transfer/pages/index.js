import React, { Component } from 'react'
// import Link from 'next/link'
import styled, { hydrate, css, cx } from 'react-emotion'  // eslint-disable-line

import Layout from '../components/layout'
// import Redraw from '../components/redraw'
import Transfer from '../components/transfer'

import { SmallSpace, MediumSpace } from '../components/styledComponent'

import Logo from '../assets/svg/transfer.svg'
// import Arrow from '../assets/svg/arrow.svg'

// Adds server generated styles to emotion cache.
// '__NEXT_DATA__.ids' is set in '_document.js'
if (typeof window !== 'undefined') {
  hydrate(window.__NEXT_DATA__.ids)
}

// const IntroItem = ({ name, description, href }) => {
//   return (
//     <div className='flex flex-column justify-between br2 pa2 hover-expand'
//       css={`
//         box-shadow: 0 0 0 4px #fff;
//         @media (max-width: 768px) {
//           flex: 1 100%;
//           margin: auto;
//           margin-bottom: 20px;
//           max-width: 600px;
//         }
//         @media (min-width: 769px) {
//           flex: 0 0 calc((100% - 80px) / 4);
//           min-width: 19rem;
//         }
//       `}
//     >
//       <h2 className='tc f2 mb0'>{name}</h2>
//       <p className='f5 pa2'>{description}</p>
//       <Link href={href}>
//         <div className='tc pa2 link pointer'>
//           <a className='ph4 pv2 f4 white'>Start</a>
//           <Arrow />
//         </div>
//       </Link>
//     </div>
//   )
// }

export default class Index extends Component {
  constructor () {
    super()
    this.state = {
      height: 1,
      scroll: 0
    }
    this.onScroll = this.onScroll.bind(this)
  }
  onScroll ({ offset }) {
    this.setState({
      scroll: offset
    })
  }
  componentDidMount () {
    const height = typeof window !== 'undefined' ? window.innerHeight : 1
    this.setState({
      height
    })
  }
  render () {
    return (
      <Layout onScroll={this.onScroll}>
        <section className='relative vh-100 overflow-hidden' css={{
          paddingTop: '76px',
          minHeight: '40rem',
          maxHeight: '64rem'
        }}>
          <div className='h-100 flex flex-auto'>
            <div className='relative w-100 h-100 bg-yellow flex flex-auto flex-column items-center justify-center w-70-l'>
              <div className='lh-title tracked dn-l' css={{
                fontFamily: 'Jenna',
                color: '#E7040F',
                textShadow: '0px 4px 4px rgba(0, 0, 0, 0.25)',
                textStroke: '1px black'
              }}>
                <p className='f1 mt0'>Image Magic Filters</p>
              </div>
              <div className='tc'>
                <Logo css={{
                  width: '216px',
                  height: '240px',
                  '@media (min-width: 768px)': {
                    width: '288px',
                    height: '320px'
                  }
                }} />
              </div>
              <div className='center f5 lh-solid black b tracked f3-l mt2' css={{
                width: 'max-content'
              }}>
                <p>Choose your content and style.</p>
                <p>Upload them, wait a minute.</p>
                <p>Enjoy your creation!</p>
              </div>
            </div>
            <div className='dn relative-l w-30-l h-100-l bg-near-black-l db-l'>
              <div className='absolute lh-title tracked' css={{
                fontFamily: 'Jenna',
                color: '#E7040F',
                marginLeft: '-5rem',
                textShadow: '0px 4px 4px rgba(0, 0, 0, 0.25)',
                textStroke: '1px black',
                top: '45%'
              }}>
                <p className='f-headline ma0'>Image</p>
                <p className='f-headline ma0'>Magic Filters</p>
              </div>
            </div>
          </div>
        </section>

        <section className='relative pa1' css={{
          minHeight: '40rem'
        }}>
          <div className='center mw9 w-90 h-100'>
            <SmallSpace />
            <h1 className='tc f3 f2-l white'>What can you do with Magic Filters?</h1>
            <SmallSpace />
            <div className='mb4'>
              <h3 className='measure-wide tl db center white'>
                Magic Filters is a flexible photo filters application which is powered by neural style transfer techniques.
                With the help of neural network, Magic Filters is able to learn many imaginative and fancy style from sample pictures.
              </h3>
              <h3 className='measure-wide tl db center white'>
                For a quick start, we have picked out a bunch of well-learned and ready-to-use styles.
                You can easily use them to decorate your photos and make you stand out in the social Apps.
              </h3>
              <h3 className='measure-wide tl db center white'>
                Moreover, if you want your customized styles, you just need simply upload the style pictures, and Magic Filters will take care of the rest for you!
              </h3>
            </div>
            <MediumSpace />
          </div>
        </section>

        {/* <Redraw scroll={this.state.scroll} height={this.state.height} /> */}

        <Transfer scroll={this.state.scroll} height={this.state.height} />

      </Layout>
    )
  }
}
