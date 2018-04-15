export function handleResponse(response) {
  if (!response.ok) {
    return response.json().then(data => Promise.reject(data["message"]))
  }

  return response.json();
}