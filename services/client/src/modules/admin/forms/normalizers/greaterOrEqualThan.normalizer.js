const greaterOrEqualThan = border =>
  (value, previousValue) => value < border ? previousValue : value;

export default greaterOrEqualThan
