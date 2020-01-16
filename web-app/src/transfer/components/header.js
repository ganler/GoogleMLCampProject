import React from 'react'
import Link from 'next/link'
// import styled, { css } from 'react-emotion'

import Logo from '../assets/svg/logo.svg'

const Header = () => (
  <div className='fixed top-0 left-0 right-0 z-2 bg-black shadow-3'>
    <div className='mw9 center flex flex-auto items-center justify-between'>
      <div className='pa2 ml2'>
        <Link href='/'>
          <a> <Logo width='56' height='56' /> </a>
        </Link>
      </div>
      <div className='mr2 tracked'>
        <Link href='/transfer'>
          <a className='link white ph4 pv2 fw6 f6 f5-ns'>Transfer</a>
        </Link>
        <Link href='/custom'>
          <a className='link white ph4 pv2 fw6 f6 f5-ns'>Custom</a>
        </Link>
      </div>
    </div>
  </div>
)

export default Header
