const twoDecimalPlacesNormalizer = value =>
  +(Math.round(value + "e+2") + "e-2");

export default twoDecimalPlacesNormalizer