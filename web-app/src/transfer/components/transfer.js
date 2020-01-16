import React, { Component } from 'react'
import Link from 'next/link'
import { css, cx } from 'react-emotion' // eslint-disable-line
import { Motion, spring, presets } from 'react-motion'
import { getElementOffset } from '../utils/utils.js'

import { SmallSpace, MediumSpace } from '../components/styledComponent'

import First from '../assets/svg/first.svg'
import Second from '../assets/svg/second.svg'
import Third from '../assets/svg/third.svg'

const bgImgMotionStyle = css({
  height: '100%',
  backgroundRepeat: 'no-repeat',
  backgroundSize: '18rem 100%',
  '@media (min-width: 30em) and (max-width: 60em)': {
    backgroundSize: '24rem 100%'
  },
  '@media (min-width: 60rem)': {
    backgroundSize: '32rem 100%'
  }
})

const bgImgStyle = css({
  width: '18rem',
  height: '13.5rem',
  backgroundSize: '100% 100%',
  backgroundRepeat: 'no-repeat',
  '@media (min-width: 30em) and (max-width: 60em)': {
    width: '24rem',
    height: '18rem'
  },
  '@media (min-width: 60rem)': {
    width: '32rem',
    height: '24rem'
  }
})

class Transfer extends Component {
  constructor () {
    super()
    this.r3 = null
    this.data = {
      top: 0
    }
  }
  componentDidMount () {
    let top = getElementOffset(this.r3).top
    this.data = {
      top
    }
  }
  getWidth () {
    let { scroll, height } = this.props
    let { top } = this.data
    if (scroll > top) {
      if (scroll > top + height) {
        return 1
      } else {
        return (scroll - top) / height
      }
    } else {
      return 0
    }
  }
  render () {
    let width = this.getWidth() * 100
    return (
      <section className='relative pa1'>
        <div className='center mw9 w-90'>
          <div className='pb2'>
            <h1 className='tc f1 fw7 f1-l white'>Transfer</h1>
            <h2 className='tc f3 fw5 f3-l white'>Transfer the style of one photo to another.</h2>
          </div>

          {/* Laptop */}
          <div className='dn vh-50 flex-l' css={{
            minHeight: '40rem'
          }}>
            <div className='relative w-10 h-100 br'>
              <First width='48' height='48' className='absolute right-0' css={{
                top: '50%',
                transform: 'translateY(-50%)'
              }} />
            </div>
            <div className='relative w-90 h-100'>
              <div className='absolute left-0 ml3' css={{
                top: '50%',
                transform: 'translateY(-50%)'
              }}>
                <span className='f4'>Pick your favorite style.</span>
              </div>
              <div className='absolute' css={{
                top: '50%',
                right: '4rem',
                transform: 'translateY(-50%)'
              }}>
                <div style={{ backgroundImage: 'url(/static/snow.jpg)' }} css={bgImgStyle} />
              </div>
            </div>
          </div>
          {/* Mobile */}
          <div className='db tc pa2 pt4 vh-50 dn-l' css={{
            minHeight: '32rem'
          }}>
            <First width='32' height='32' />
            <div className='mt2 tc'>
              <span className='f4'>Pick your favorite style.</span>
            </div>
            <div className='w-100 h-auto mt4'>
              <div style={{ backgroundImage: 'url(/static/snow.jpg)' }} css={bgImgStyle} className='center' />
            </div>
          </div>

          {/* Laptop */}
          <div className='dn vh-50 flex-l' css={{
            minHeight: '40rem'
          }}>
            <div className='relative w-10 h-100 br'>
              <Second width='48' height='48' className='absolute right-0' css={{
                top: '50%',
                transform: 'translateY(-50%)'
              }} />
            </div>
            <div className='relative w-90 h-100'>
              <div className='absolute left-0 ml3' css={{
                top: '50%',
                transform: 'translateY(-50%)'
              }}>
                <span className='f4'>Upload your photo.</span>
              </div>
              <div className='absolute' css={{
                top: '50%',
                right: '4rem',
                transform: 'translateY(-50%)'
              }}>
                <div style={{ backgroundImage: 'url(/static/gold.jpg)' }} css={bgImgStyle} />
              </div>
            </div>
          </div>
          {/* Mobile */}
          <div className='db tc pa2 pt4 vh-50 dn-l' css={{
            minHeight: '32rem'
          }}>
            <Second width='32' height='32' />
            <div className='mt2 tc'>
              <span className='f4'>Upload your photo.</span>
            </div>
            <div className='w-100 h-auto mt4'>
              <div style={{ backgroundImage: 'url(/static/gold.jpg)' }} css={bgImgStyle} className='center' />
            </div>
          </div>

        </div>

        <Motion defaultStyle={{ s: 0 }} style={{ s: spring(width, { ...presets.stiff }) }}>
          { style => (
            <div className='relative center mw9 w-90'>
              <div>
                <div className='flex flex-auto vh-100 flex-column flex-row-l'
                  ref={div => { this.r3 = div }}
                  css={{
                    minHeight: '48rem',
                    position: 'sticky',
                    top: '0px'
                  }}
                >
                  <div className='relative mt6 tc mt0-l w-10-l h-100-l br-l'>
                    <Third css={{
                      width: '32',
                      height: '32',
                      position: 'relative',
                      '@media (min-width: 60rem)': {
                        width: '48',
                        height: '48',
                        position: 'absolute',
                        top: '25%',
                        right: '0',
                        transform: 'translateY(-50%)'
                      }
                    }} />
                    <div className='mt2 tc dn-l'>
                      <span className='f4'>Enjoy!</span>
                    </div>
                  </div>
                  <div className='relative h5 w-90-l h-100-l'>
                    <div className='dn absolute left-0 ml3 db-l' css={{
                      top: '25%',
                      transform: 'translateY(-50%)'
                    }}>
                      <span className='f4'>Enjoy!</span>
                    </div>
                    <div className='mt4 mt0-l absolute-l' css={{
                      '@media (min-width: 60rem)': {
                        top: `50%`,
                        right: '64px',
                        transform: 'translateY(-50%)'
                      }
                    }}>
                      <div style={{ backgroundImage: 'url(/static/gold.jpg)' }} css={bgImgStyle} className='center'>
                        <div style={{
                          width: `${style.s}%`,
                          backgroundImage: 'url(/static/result.jpg)'
                        }} css={bgImgMotionStyle}
                        />
                      </div>
                    </div>
                  </div>
                </div>
                <div className='vh-100' />
              </div>
              <div className='pa3 tc'>
                <SmallSpace />
                <Link href='/transfer'>
                  <a className='ba pv2 ph4 f6 white link bg-animate hover-black hover-bg-white b'>Try it now</a>
                </Link>
                <MediumSpace />
              </div>
            </div>
          )}
        </Motion>
      </section>
    )
  }
}

export default Transfer
