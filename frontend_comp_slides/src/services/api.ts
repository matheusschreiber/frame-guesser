import axios from "axios";
import { deleteCookie, getCookie, setCookie } from "./cookies";
import { goto } from "$app/navigation";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL + "/api/",
});


// This is to use the acess token on each request
api.interceptors.request.use((request) => {
  const rawTokens = getCookie('auth');
  if (!rawTokens) {
    goto('/login');
    return request
  }
  const accessToken = JSON.parse(rawTokens).access
  
  if (accessToken) {
    request.headers.Authorization = `Bearer ${accessToken}`;
  }

  return request; 
});


// This is to refresh the token when expired
api.interceptors.response.use((response) => {
  return response;
}, async (error) => {
  const originalRequest = error.config;

  if (originalRequest.url == '/user/token/refresh/') {
    deleteCookie('auth')
    window.location.href = "/login";
    return Promise.reject(error);
  }
  
  if (
    error?.response?.status === 401 &&
    !originalRequest?.__isRetryRequest
  ) {
      originalRequest.retry = true;
      
      const rawTokens = getCookie('auth');
      if (!rawTokens) {
        deleteCookie('auth')
        window.location.href = "/login"
        return Promise.reject(error);
      }
      const refreshToken = JSON.parse(rawTokens).refresh

      if(!refreshToken) {
        deleteCookie('auth')
        window.location.href = "/login"
        return Promise.reject(error);
      }

      const response = await api.post('/user/token/refresh/', {"refresh":refreshToken});
      const data = {
          accessToken: response.data.token,
          refreshToken: response.data.refreshToken,
      };

      setCookie("auth", JSON.stringify(response.data));
      return api(originalRequest);
  }
  
  return Promise.reject(error);
});
