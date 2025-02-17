import axios from "axios";
import { deleteCookie, getCookie, setCookie } from "./cookies";
import { goto } from "$app/navigation";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL + "/api/",
});

// List of urls that don't need the access token
const nonProtectedUrls = [
  'user/list/',
  'disciplines/',
  'user/create/',
  'user/token/',
  'user/message/list/'
]

// This is to add the access token to the request
api.interceptors.request.use((request) => {
  if (request.url && nonProtectedUrls.includes(request.url)) return request
  
  // Get the access token from the cookie
  const rawTokens = getCookie('auth');

  // If there is no access token, redirect to login
  if (!rawTokens) {
    goto('/login');
    return request
  }

  // Parse the access token
  const accessToken = JSON.parse(rawTokens).access

  // If there is an access token, add it to the request
  if (accessToken) {
    request.headers.Authorization = `Bearer ${accessToken}`;
  }

  return request; 
});


// This is to refresh the access token if it is expired
api.interceptors.response.use((response) => {
  
  // If the response is successful, return it
  return response;

}, async (error) => {
    
  // Get the original request
  const originalRequest = error.config;

  // If the request is in the list of non protected urls, return
  if (originalRequest.url && nonProtectedUrls.includes(originalRequest.url)) {
    // return Promise.resolve();
    return Promise.reject(error);
  }

  // If the original request is the refresh token, delete the cookie and redirect
  if (originalRequest.url == '/user/token/refresh/') {
    deleteCookie('auth')
    window.location.href = "/login";
    return Promise.reject(error);
  }

  // If the error is 401 and the original request is not a retry request, refresh the token
  if (
    error?.response?.status === 401 &&
    !originalRequest?.__isRetryRequest
  ) {
      // Set the original request as a retry request
      originalRequest.retry = true;

      // Get the refresh token from the cookie
      const rawTokens = getCookie('auth');

      // If there is no refresh token, delete the cookie and redirect
      if (!rawTokens) {
        deleteCookie('auth')
        window.location.href = "/login"
        return Promise.reject(error);
      }

      // Parse the refresh token
      const refreshToken = JSON.parse(rawTokens).refresh

      // If there is no refresh token, delete the cookie and redirect
      if(!refreshToken) {
        deleteCookie('auth')
        window.location.href = "/login"
        return Promise.reject(error);
      }

      // Refresh the token via API endpoint
      const response = await api.post('/user/token/refresh/', {"refresh":refreshToken});
      
      // If the response is successful, set the new access token and refresh token in the cookie
      setCookie("auth", JSON.stringify(response.data));

      // Add the new access token to the original request
      return api(originalRequest);
  }

  // If the error is not 401, return the error
  return Promise.reject(error);
});
