const floatNormalizer = value =>
  !value || !value.length || value[value.length - 1] === '.' ? value : parseFloat(value);

export default floatNormalizer