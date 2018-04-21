export function hasNumber(myString) {
  return /\d/.test(myString);
}

export function isPhoneNumber(string) {
  return /\+42\d \d\d\d \d\d\d \d\d\d/.test(string)
}

export function isZipCode(string) {
  return /\d\d\d \d\d/.test(string)
}