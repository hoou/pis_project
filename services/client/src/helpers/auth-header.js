export function authHeader() {
  // return authorization header with jwt token
  let accessToken = JSON.parse(localStorage.getItem('access_token'));

  if (accessToken) {
    return {'Authorization': 'Bearer ' + accessToken};
  } else {
    return {};
  }
}