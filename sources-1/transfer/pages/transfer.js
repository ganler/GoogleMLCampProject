import React, { Component } from 'react'
import Layout from '../components/layout'
// import Lightbox from 'react-images'
import Gallery from 'react-grid-gallery'
import axios from 'axios'
import { Upload, Icon, message } from 'antd'
import { MediumSpace } from '../components/styledComponent'
import styled, { hydrate, css, cx } from 'react-emotion'  // eslint-disable-line
import { baseUrl } from '../utils/utils.js'

// Adds server generated styles to emotion cache.
// '__NEXT_DATA__.ids' is set in '_document.js'
if (typeof window !== 'undefined') {
  hydrate(window.__NEXT_DATA__.ids)
}

// const MockList = [
//   { src: '/static/girl.jpg', width: 4, height: 3 },
//   { src: '/static/gold.jpg', width: 4, height: 3 },
//   { src: '/static/blocks.jpg', width: 3, height: 4 },
//   { src: '/static/star.jpg', width: 4, height: 3 },
//   { src: '/static/tree.jpg', width: 4, height: 3 },
//   { src: '/static/library1.jpg', width: 4, height: 3 },
//   { src: '/static/library2.jpg', width: 4, height: 3 }
// ]

function getBase64 (img, callback) {
  const reader = new FileReader() // eslint-disable-line
  reader.addEventListener('load', () => callback(reader.result))
  reader.readAsDataURL(img)
}

function beforeUpload (file) {
  const isJPG = file.type === 'image/jpeg' || file.type === 'image/png'
  if (!isJPG) {
    message.error('You can only upload JPG or PNG file!')
  }
  const isLt5M = file.size / 1024 / 1024 < 5
  if (!isLt5M) {
    message.error('Image must smaller than 5MB!')
  }
  return isJPG && isLt5M
}

class Avatar extends React.Component {
  constructor () {
    super()
    this.state = {
      loading: false
    }
    this.handleChange = this.handleChange.bind(this)
    this.customRequest = this.customRequest.bind(this)
    this.handleError = this.handleError.bind(this)
  }

  handleChange (info) {
    if (info.file.status === 'uploading') {
      this.setState({ loading: true })
      return
    }
    if (info.file.status === 'done') {
      // Get this url from response in real world.
      getBase64(info.file.originFileObj, imageUrl => this.setState({
        imageUrl,
        loading: false
      }))
    }
  }

  customRequest ({
    action,
    data,
    file,
    filename,
    headers,
    onError,
    onProgress,
    onSuccess,
    withCredentials
  }) {
    // EXAMPLE: post form-data with 'axios'
    const formData = new FormData() // eslint-disable-line
    const onTransferDone = this.props.onTransferDone
    // console.log(this.props)
    let newFile = new File([file], 'image.' + file.name.split('.').pop(), { type: file.type }) // eslint-disable-line
    // console.log('file-name', newFile.name)
    if (data) {
      Object.keys(data).map(key => {
        formData.append(key, data[key])
      })
    }
    formData.append(filename, newFile)

    // console.log(data.name)

    message.success('Image is uploading, please wait.', 0.8)

    axios
      .post(action, formData, {
        withCredentials,
        headers,
        onUploadProgress: ({ total, loaded }) => {
          onProgress({ percent: Math.round(loaded / total * 100).toFixed(2) }, file)
        }
      })
      .then(res => {
        switch (res.status) {
          case 200:
            onSuccess(res)
            onTransferDone(res.data)
            return res
          case 408:
            // console.log('408')
            throw new Error('Timeout, Please Try again')
          case 413:
            throw new Error('Image is too big. Please Try again')
          default:
            throw new Error('Unknow action.')
        }
      })
      .catch(onError)

    return {
      abort () {
        console.log('upload progress is aborted.')
      }
    }
  }

  handleError (err) {
    switch (err.response.status) {
      case 408:
        message.error('Timeout, Please Try again', 2)
        break
      case 413:
        message.error('Image too big, Please Try again', 2)
        break
      default:
        message.error('Unknow Error', 2)
    }
    this.setState({
      loading: false
    })
  }

  render () {
    const uploadButton = (
      <div>
        <Icon type={this.state.loading ? 'loading' : 'plus'} />
        <div className='ant-upload-text'>Upload</div>
      </div>
    )
    const imageUrl = this.state.imageUrl
    const stylename = this.props.stylename
    return (
      <Upload
        name='file'
        listType='picture-card'
        className='avatar-uploader w-90'
        showUploadList={false}
        beforeUpload={beforeUpload}
        onChange={this.handleChange}
        customRequest={this.customRequest}
        action={baseUrl + '/submit'}
        data={{ name: stylename }}
        supportServerRender
        onError={this.handleError}
      >
        {imageUrl ? <img src={imageUrl} alt='avatar' /> : uploadButton}
      </Upload>
    )
  }
}

class Redraw extends Component {
  constructor () {
    super()
    this.state = {
      lightboxIsOpen: false,
      imageUrl: '',
      currentImage: 0,
      styleList: [],
      currentSelectedImage: 0
    }
    this.onTransferDone = this.onTransferDone.bind(this)
    // this.closeLightbox = this.closeLightbox.bind(this)
    // this.openLightbox = this.openLightbox.bind(this)
    // this.gotoNext = this.gotoNext.bind(this)
    // this.gotoPrevious = this.gotoPrevious.bind(this)
    this.onSelectImage = this.onSelectImage.bind(this)
    this.onCurrentImageChange = this.onCurrentImageChange.bind(this)
    this.onBoxSelectImage = this.onBoxSelectImage.bind(this)
  }

  static async getInitialProps () {
    // eslint-disable-next-line no-undef
    const res = await axios.get(baseUrl + '/style_list', {
      timeout: 2000
    })
      .then(res => {
        if (res.status !== 200) {
          return {}
        } else {
          return res.data
        }
        // throw new Error(`can't get the style list`)
      })
      .then(data => {
        return data
      })
      .catch(err => { // eslint-disable-line
        return {}
      })

    // Object.keys(res).map((key, index) => {
    //   console.log(key, res[key][1][0], res[key][1][1])
    // })
    return {
      styleList: Object.keys(res).map((key, index) => {
        let r = res[key][1][0] / 320
        return {
          name: key,
          src: baseUrl + res[key][0],
          thumbnail: baseUrl + res[key][0],
          thumbnailWidth: res[key][1][0] / r,
          thumbnailHeight: res[key][1][1] / r,
          isSelected: index === 0
        }
      })
    }
  }

  componentWillMount () {
    // console.log(this.props.styleList)
    this.setState({
      styleList: this.props.styleList,
      currentSelectedImage: 0
    })
  }

  onSelectImage (index, image) {
    console.log('onSelectImage: index', index)
    let styleList = this.state.styleList.slice()
    styleList = styleList.map(item => {
      return {
        ...item,
        isSelected: false
      }
    })
    let img = styleList[index]
    if (img.hasOwnProperty('isSelected')) {
      img.isSelected = !img.isSelected
    } else {
      img.isSelected = true
    }
    this.setState({
      styleList: styleList,
      currentSelectedImage: index
    })
  }

  onBoxSelectImage () {
    let index = this.state.currentImage
    console.log('onSelectImage: index', index)
    let styleList = this.state.styleList.slice()
    styleList = styleList.map(item => {
      return {
        ...item,
        isSelected: false
      }
    })
    let img = styleList[index]
    if (img.hasOwnProperty('isSelected')) {
      img.isSelected = !img.isSelected
    } else {
      img.isSelected = true
    }
    this.setState({
      styleList: styleList,
      currentSelectedImage: index
    })
  }

  onTransferDone (imageUrl) {
    // console.log(imageUrl)
    this.setState({
      imageUrl: imageUrl
    })
  }

  onCurrentImageChange (index) {
    this.setState({ currentImage: index })
  }

  // openLightbox (event, obj) {
  //   this.setState({
  //     currentImage: obj.index,
  //     lightboxIsOpen: true
  //   })
  // }
  // closeLightbox () {
  //   this.setState({
  //     currentImage: 0,
  //     lightboxIsOpen: false
  //   })
  // }
  // gotoPrevious () {
  //   this.setState({
  //     currentImage: this.state.currentImage - 1
  //   })
  // }
  // gotoNext () {
  //   this.setState({
  //     currentImage: this.state.currentImage + 1
  //   })
  // }

  render () {
    let styleList = this.state.styleList
    // console.log(styleList)
    let currentSelectedImage = this.state.currentSelectedImage
    // console.log(currentImage)
    let imageUrl = this.state.imageUrl ? baseUrl + this.state.imageUrl : ''
    return (
      <Layout>
        <section className='relative min-vh-100 overflow-hidden bg-near-white' css={{
          paddingTop: '76px',
          minHeight: '40rem'
        }}>
          {/* <Lightbox images={styleList}
            onClose={this.closeLightbox}
            onClickPrev={this.gotoPrevious}
            onClickNext={this.gotoNext}
            currentImage={this.state.currentImage}
            isOpen={this.state.lightboxIsOpen}
      /> */ }
          <div className='center mw9 w-100 w-90-l h-100 pv2'>
            <div>
              <h1 className='tc black'>1. Choose your favorite style</h1>
              <p className='tc black'>On PC: click the left-top of image to choose style; <br /> On phone, click the image, and click 'select this' on the dialog.</p>
            </div>
            <div className='w-100 center' style={{
              display: 'block',
              minHeight: '1px',
              border: '1px solid #ddd',
              overflow: 'auto'
            }} css={`
              img {
                max-width: none;
              }
            `}>
              {
                styleList.length !== 0
                  ? (<Gallery images={styleList}
                    enableImageSelection
                    onSelectImage={this.onSelectImage}
                    margin={3}
                    enableLightbox
                    currentImageWillChange={this.onCurrentImageChange}
                    customControls={[
                      <a key='selectimage' onClick={this.onBoxSelectImage} className='flex justify-center items-center'>
                        <span className={`pv1 ph2 fw8 f6 ${this.state.currentImage === this.state.currentSelectedImage ? 'blue' : 'white underline'}`}>
                          { this.state.currentImage === this.state.currentSelectedImage ? 'Selected' : 'Select this'}
                        </span>
                      </a>
                    ]}
                  />)
                  : (
                    <h2 className='red pa3 tc'> Can't load the style, please refresh your page.</h2>
                  )
              }
            </div>

            <div className='mt4 flex flex-auto flex-wrap'>
              <div className='w-100 w-50-l br-l b--moon-gray'>
                <h1 className='tc black'>2. Upload your photo</h1>
                <div className='flex flex-auto items-center justify-center'>
                  <Avatar
                    onTransferDone={this.onTransferDone}
                    stylename={styleList.length === 0 ? '' : styleList[currentSelectedImage].name}
                  />
                </div>
              </div>
              <div className='w-100 w-50-l'>
                <h1 className='tc black'>3. Enjoy</h1>
                <div className='flex flex-auto flex-column items-center justify-center'>
                  <span className='avatar-uploader w-90'>
                    <div className='ant-upload ant-upload-select ant-upload-select-picture-card'>
                      <span className='ant-upload' role='button' >
                        <img src={imageUrl} />
                      </span>
                    </div>
                  </span>
                  {
                    this.state.imageUrl ? <a href={imageUrl} download={this.state.imageUrl} className='ba pv1 ph2 br1 mt2 f6'>Download</a> : ''
                  }
                </div>
              </div>
            </div>
            <MediumSpace />
          </div>
        </section>
      </Layout>
    )
  }
}

export default Redraw
