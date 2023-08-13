export function setCookie(name: string, value: string, days = 2) {
  const expires = new Date();
  expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
  document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

export function getCookie(name: string) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  // let pop = parts.pop();
  // if (parts == undefined || pop == undefined) return "";
  // if (parts.length === 2) return pop.split(";").shift();
  if (parts.length === 2) return parts.pop()?.split(";").shift();
}

export function deleteCookie(name: string) {
  document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;`;
}
