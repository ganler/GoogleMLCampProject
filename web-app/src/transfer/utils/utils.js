const getElementOffset = (el) => {
  let top = 0
  let left = 0

  // grab the offset of the element relative to it's parent,
  // then repeat with the parent relative to it's parent,
  // ... until we reach an element without parents.
  do {
    top += el.offsetTop
    left += el.offsetLeft
    el = el.offsetParent
  } while (el)

  return { top, left }
}

const baseUrl = 'http://18.191.171.176:2333'

export {
  getElementOffset,
  baseUrl
}
